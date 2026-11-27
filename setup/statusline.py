"""A Codex statusline provider using newline-delimited MCP over stdio."""

import json
import sys
from collections import OrderedDict


URI = "ui://workspace-statusline/footer"
USAGE_CACHE = OrderedDict()
TOOL = {
    "name": "statusline",
    "title": "Workspace statusline",
    "description": "Show model, usage, session, and permissions in the Codex footer.",
    "inputSchema": {"type": "object", "properties": {}},
    "_meta": {
        "openai/ui": {"entrypoints": [{"type": "statusline", "resourceUri": URI}]}
    },
}


def compact_tokens(count):
    if count >= 999_500:
        return f"{count / 1_000_000:.2f}".rstrip("0").rstrip(".") + "M"
    if count >= 1_000:
        return f"{count / 1_000:.0f}K"
    return str(count)


def segment(label, color, *, bold=False):
    props = {"color": color}
    if bold:
        props["weight"] = "bold"
    return {"type": "text", "props": props, "children": [label]}


def usage_metric(label, value, color, *, separated):
    children = [segment("·", "status-metadata")] if separated else []
    children.extend([segment(label, "status-metadata"), segment(value, color)])
    return {"type": "row", "props": {"gap": 1, "wrap": "nowrap"}, "children": children}


def retain_usage(state):
    """Keep last known usage during missing snapshots, isolated by thread ID."""
    thread = state.get("thread") or {}
    thread_id = thread.get("id")
    if not thread_id:
        return state
    previous = USAGE_CACHE.pop(thread_id, {})
    current = thread.get("usage") or {}
    merged = {}
    stale = []
    for section in ("context", "total", "cost"):
        values = dict(previous.get(section) or {})
        incoming = {key: value for key, value in (current.get(section) or {}).items()
                    if value is not None}
        if values.keys() - incoming.keys():
            stale.append(section)
        values.update(incoming)
        merged[section] = values
    USAGE_CACHE[thread_id] = merged
    if len(USAGE_CACHE) > 64:
        USAGE_CACHE.popitem(last=False)
    return {**state, "thread": {**thread, "usage": merged}, "_stale_usage": stale}


def render(state):
    """Return the UI tree for this resource read's thread."""
    thread = state.get("thread", {})
    model = thread.get("model", {})
    model_label = model.get("display_name") or "Codex"
    model_name = f"{model.get('id') or ''} {model_label}".casefold()
    model_icon = next(
        (icon for family, icon in (
            ("luna", "🌙"), ("terra", "🌍"), ("sol", "☀️"), ("astra", "✨")
        ) if family in model_name),
        "◆",
    )
    model_group = [segment(f"{model_icon} {model_label}", "status-model", bold=True)]
    if reasoning := model.get("reasoning_level"):
        model_group.append(segment(reasoning, "status-model"))

    usage = thread.get("usage") or {}
    context = usage.get("context") or {}
    stale = state.get("_stale_usage", [])
    usage_group = []
    if (used := context.get("used_percentage")) is not None:
        filled = max(0, min(8, round(used * 8 / 100)))
        color = "red" if used >= 90 else "yellow" if used >= 75 else "status-usage"
        meter = {
            "type": "text",
            "children": [
                segment("▧" * filled, color),
                segment("□" * (8 - filled), "status-metadata"),
            ],
        }
        usage_group.append({
            "type": "row",
            "props": {"gap": 1, "wrap": "nowrap"},
            "children": [
                segment("Context (last)" if "context" in stale else "Context", "status-metadata"),
                meter,
                segment(f"{used:g}%", color, bold=True),
            ],
        })
    if (window := context.get("context_window_size")) is not None:
        usage_group.append(usage_metric(
            "Window (last)" if "context" in stale else "Window",
            compact_tokens(window), "status-usage", separated=bool(usage_group)
        ))
    if total := usage.get("total"):
        used_tokens = (
            max(0, total["total_input_tokens"] - total["cache_read_input_tokens"])
            + max(0, total["output_tokens"])
        )
        usage_group.append(usage_metric(
            "Used (last)" if "total" in stale else "Used",
            compact_tokens(used_tokens), "status-usage", separated=bool(usage_group)
        ))
    if (credits := (usage.get("cost") or {}).get("total_credits")) is not None:
        usage_group.append(usage_metric(
            "Credits (last)" if "cost" in stale else "Credits",
            f"{credits:,.1f}", "status-limit", separated=bool(usage_group)
        ))

    limits = (state.get("account") or {}).get("rate_limits", [])
    codex_limits = next((limit for limit in limits if limit["limit_id"] == "codex"), None)
    if codex_limits is None and len(limits) == 1:
        codex_limits = limits[0]
    limits_group = []
    if codex_limits:
        labels = {300: "5h", 10080: "7d"}
        for window in (codex_limits.get("primary_limit"), codex_limits.get("secondary_limit")):
            if window and window["window_minutes"] in labels:
                duration = labels[window["window_minutes"]]
                remaining = max(0, 100 - window["used_percent"])
                limits_group.append(segment(f"{duration} {remaining:g}% left", "status-limit"))

    session_group = []
    if agent := (thread.get("agent") or {}).get("state"):
        color = {"ready": "green", "waiting": "yellow"}.get(agent, "status-state")
        session_group.append(segment(f"● {agent.title()}", color))
    if permissions := thread.get("permissions"):
        if label := permissions.get("display_name"):
            color = "status-mode"
            if permissions.get("type") == "disabled":
                color = "red"
            session_group.append(segment(label, color))

    title_group = []
    if title := thread.get("name"):
        title_group.append(segment(title, "status-thread"))

    app_group = []
    app = state.get("app") or {}
    tier = model.get("service_tier_display_name")
    if not tier:
        tier = {"flex": "Flex", "priority": "Fast", "ultrafast": "Ultra Fast"}.get(
            model.get("service_tier"), "Standard"
        )
    app_group.append(segment(tier, "status-mode"))
    if version := app.get("cli_version"):
        app_group.append(segment(f"v{version}", "status-metadata"))

    children = []
    for group in (model_group, usage_group, limits_group, session_group, title_group, app_group):
        if not group:
            continue
        if children:
            children.append(segment("│", "status-metadata"))
        children.extend(group)

    return {
        "type": "row",
        "props": {"gap": 1, "wrap": "wrap"},
        "children": children,
    }


def respond(method, params):
    if method == "initialize":
        return {
            "protocolVersion": "2025-06-18",
            "capabilities": {"tools": {}, "resources": {}},
            "serverInfo": {"name": "workspace-statusline", "version": "1.0"},
        }
    if method == "ping":
        return {}
    if method == "tools/list":
        return {"tools": [TOOL]}
    if method == "tools/call":
        if params.get("name") != TOOL["name"]:
            raise ValueError("Unknown tool name")
        return {
            "content": [{"type": "text", "text": f"The statusline resource is {URI}."}]
        }
    if method == "resources/list":
        return {
            "resources": [
                {"name": "footer", "uri": URI, "mimeType": "application/json"}
            ]
        }
    if method == "resources/templates/list":
        return {"resourceTemplates": []}
    if method == "resources/read":
        if params.get("uri") != URI:
            raise ValueError("Unknown resource URI")
        state = params.get("_meta", {}).get("com.openai/codex-statusline-state", {})
        return {
            "contents": [
                {
                    "uri": URI,
                    "mimeType": "application/json",
                    "text": json.dumps(render(retain_usage(state)), ensure_ascii=False),
                }
            ]
        }
    raise KeyError(method)


def main():
    for line in sys.stdin.buffer:
        reply = {"jsonrpc": "2.0", "id": None}
        try:
            request = json.loads(line)
            if not isinstance(request, dict) or not isinstance(
                request.get("method"), str
            ):
                reply["error"] = {"code": -32600, "message": "Invalid request"}
            elif "id" not in request:
                continue
            else:
                reply["id"] = request["id"]
                reply["result"] = respond(request["method"], request.get("params", {}))
        except json.JSONDecodeError:
            reply["error"] = {"code": -32700, "message": "Parse error"}
        except KeyError:
            reply["error"] = {"code": -32601, "message": "Method not found"}
        except (TypeError, ValueError, AttributeError):
            reply["error"] = {"code": -32602, "message": "Invalid parameters"}
        print(json.dumps(reply), flush=True)


if __name__ == "__main__":
    main()
