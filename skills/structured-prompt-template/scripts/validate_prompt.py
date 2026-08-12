"""제한된 Jinja2 시스템 프롬프트를 렌더하고 구조 계약을 검증한다.

이 스크립트는 Skill의 예제 템플릿과 같은 닫힌 context shape를 검사한 뒤
Jinja2 ``StrictUndefined``로 렌더한다. 렌더 전에는 include, import, safe 같은
불필요한 템플릿 기능을 차단하고, 렌더 후에는 상위 섹션 순서와 태그 위계,
P/STEP 연속성, Skill·Tool 이름 중복을 검사한다.

데이터 흐름::

    template + context JSON
             │
             ├─ source/context validation
             ▼
       restricted Jinja2 render
             │
             ├─ tag stack/order validation
             ▼
        rendered prompt bytes within the configured budget

이 스크립트는 provider request를 만들거나 네트워크를 호출하지 않는다.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections.abc import Mapping, Sequence
from pathlib import Path
from typing import Any, Final

from jinja2 import Environment, StrictUndefined, TemplateError, meta, nodes
from markupsafe import escape

_CONTEXT_KEYS: Final = frozenset(
    {
        "role",
        "priorities",
        "boundaries",
        "skills",
        "tools",
        "workflow_steps",
        "output_contract",
    }
)
_TOP_LEVEL_ORDER: Final = (
    "ROLE",
    "PRIORITIES",
    "BOUNDARIES",
    "SKILLS",
    "TOOLS",
    "WORKFLOW",
    "OUTPUT_CONTRACT",
)
_BANNED_STATEMENTS: Final = (
    "include",
    "import",
    "from",
    "extends",
    "macro",
    "call",
    "set",
    "block",
    "filter",
)
_IDENTIFIER_RE: Final = re.compile(r"^[A-Za-z0-9_.:-]+$")
_TAG_RE: Final = re.compile(r"<(/?)([A-Z][A-Z0-9_]*)([^<>]*)>")
_FOR_BINDINGS: Final = {
    "priorities": "priority",
    "boundaries": "boundary",
    "skills": "skill",
    "tools": "tool",
    "workflow_steps": "step",
}
_GETATTR_ALLOWLIST: Final = {
    "priority": frozenset({"level", "instruction"}),
    "skill": frozenset({"name", "description", "use_when", "recommended_tools"}),
    "tool": frozenset({"name", "description", "usage_guidance"}),
    "loop": frozenset({"index"}),
}
_ALLOWED_NODE_TYPES: Final = (
    nodes.Template,
    nodes.Output,
    nodes.TemplateData,
    nodes.Filter,
    nodes.Name,
    nodes.For,
    nodes.Getattr,
)


class PromptValidationError(ValueError):
    """프롬프트 source, context 또는 렌더 구조가 계약을 위반했음을 나타낸다.

    Args:
        message (str): 검증 실패 설명.

    Returns:
        없음.

    Raises:
        없음.

    Side Effects:
        없음.
    """


def _expect_string(value: object, field: str) -> str:
    """공백이 아닌 문자열을 검증한다.

    Args:
        value (object): 검사할 값.
        field (str): 오류 메시지에 사용할 필드 경로.

    Returns:
        str: 원본 문자열.

    Raises:
        PromptValidationError: 값이 공백 없는 문자열이 아닌 경우.

    Side Effects:
        없음.
    """

    if not isinstance(value, str) or value.strip() != value or not value:
        raise PromptValidationError(f"{field} must be a non-blank, non-normalized string")
    return value


def _expect_record(value: object, field: str, keys: frozenset[str]) -> Mapping[str, object]:
    """exact-key JSON object를 검증한다.

    Args:
        value (object): 검사할 값.
        field (str): 오류 메시지에 사용할 필드 경로.
        keys (frozenset[str]): 허용하는 exact key 집합.

    Returns:
        Mapping[str, object]: 검증된 mapping.

    Raises:
        PromptValidationError: object가 아니거나 key가 일치하지 않는 경우.

    Side Effects:
        없음.
    """

    if not isinstance(value, Mapping):
        raise PromptValidationError(f"{field} must be an object")
    actual = frozenset(str(key) for key in value)
    if actual != keys:
        raise PromptValidationError(f"{field} keys must be exactly {sorted(keys)}; got {sorted(actual)}")
    return value


def _expect_list(value: object, field: str) -> Sequence[object]:
    """문자열이 아닌 JSON 배열을 검증한다.

    Args:
        value (object): 검사할 값.
        field (str): 오류 메시지에 사용할 필드 경로.

    Returns:
        Sequence[object]: 검증된 배열.

    Raises:
        PromptValidationError: 배열이 아닌 경우.

    Side Effects:
        없음.
    """

    if not isinstance(value, Sequence) or isinstance(value, (str, bytes, bytearray)):
        raise PromptValidationError(f"{field} must be an array")
    return value


def _expect_positive_int(value: object, field: str) -> int:
    """양의 정수를 검증한다.

    Args:
        value (object): 검사할 값.
        field (str): 오류 메시지에 사용할 필드 이름.

    Returns:
        int: 검증된 양의 정수.

    Raises:
        PromptValidationError: 값이 양의 정수가 아닌 경우.

    Side Effects:
        없음.
    """

    if not isinstance(value, int) or isinstance(value, bool) or value <= 0:
        raise PromptValidationError(f"{field} must be a positive integer")
    return value


def validate_context(raw: object) -> Mapping[str, object]:
    """템플릿 context의 닫힌 shape와 정렬 계약을 검증한다.

    Args:
        raw (object): JSON에서 읽은 context.

    Returns:
        Mapping[str, object]: 검증된 context.

    Raises:
        PromptValidationError: context가 계약을 위반한 경우.

    Side Effects:
        없음.
    """

    context = _expect_record(raw, "context", _CONTEXT_KEYS)
    _expect_string(context["role"], "role")
    _expect_string(context["output_contract"], "output_contract")

    priorities = _expect_list(context["priorities"], "priorities")
    if not priorities:
        raise PromptValidationError("priorities must not be empty")
    levels: list[str] = []
    for index, value in enumerate(priorities):
        item = _expect_record(value, f"priorities[{index}]", frozenset({"level", "instruction"}))
        level = _expect_string(item["level"], f"priorities[{index}].level")
        _expect_string(item["instruction"], f"priorities[{index}].instruction")
        levels.append(level)
    if levels != [f"P{index}" for index in range(len(levels))]:
        raise PromptValidationError("priority levels must be contiguous and ordered from P0")

    for field in ("boundaries", "workflow_steps"):
        values = _expect_list(context[field], field)
        if not values:
            raise PromptValidationError(f"{field} must not be empty")
        for index, value in enumerate(values):
            _expect_string(value, f"{field}[{index}]")

    for field, keys in (
        ("skills", frozenset({"name", "description", "use_when", "recommended_tools"})),
        ("tools", frozenset({"name", "description", "usage_guidance"})),
    ):
        values = _expect_list(context[field], field)
        names: list[str] = []
        for index, value in enumerate(values):
            item = _expect_record(value, f"{field}[{index}]", keys)
            name = _expect_string(item["name"], f"{field}[{index}].name")
            if _IDENTIFIER_RE.fullmatch(name) is None:
                raise PromptValidationError(f"{field}[{index}].name contains unsupported characters")
            for key in keys - {"name", "recommended_tools"}:
                _expect_string(item[key], f"{field}[{index}].{key}")
            if field == "skills":
                recommended = _expect_list(item["recommended_tools"], f"{field}[{index}].recommended_tools")
                recommended_names = [
                    _expect_string(tool_name, f"{field}[{index}].recommended_tools[{tool_index}]")
                    for tool_index, tool_name in enumerate(recommended)
                ]
                if len(recommended_names) != len(set(recommended_names)):
                    raise PromptValidationError(f"{field}[{index}].recommended_tools must be unique")
            names.append(name)
        if len(names) != len(set(names)):
            raise PromptValidationError(f"{field} names must be unique")
        if field == "skills" and names != sorted(names):
            raise PromptValidationError("skills must be sorted by name")

    role_tool_names = {
        str(item["name"]) for item in _expect_list(context["tools"], "tools") if isinstance(item, Mapping)
    }
    for index, value in enumerate(_expect_list(context["skills"], "skills")):
        if not isinstance(value, Mapping):
            continue
        recommended_tool_names = {str(item) for item in _expect_list(value["recommended_tools"], "recommended_tools")}
        unknown = sorted(recommended_tool_names - role_tool_names)
        if unknown:
            raise PromptValidationError(f"skills[{index}] recommends unavailable role Tools: {unknown}")

    return context


def validate_template_source(source: str) -> Environment:
    """Jinja2 source를 제한된 문법과 변수 allowlist로 검증한다.

    Args:
        source (str): Jinja2 템플릿 source.

    Returns:
        Environment: 렌더에 사용할 제한된 environment.

    Raises:
        PromptValidationError: 금지 문법·필터·변수가 있는 경우.

    Side Effects:
        없음.
    """

    lowered = source.lower()
    if "|safe" in lowered:
        raise PromptValidationError("the safe filter is forbidden")
    for statement in _BANNED_STATEMENTS:
        if re.search(r"{%-?\s*" + statement + r"\b", lowered):
            raise PromptValidationError(f"Jinja2 statement {statement!r} is forbidden")

    environment = Environment(
        undefined=StrictUndefined,
        autoescape=True,
        trim_blocks=True,
        lstrip_blocks=True,
    )
    environment.globals.clear()
    environment.filters.clear()
    environment.filters["e"] = escape
    environment.tests.clear()
    parsed = environment.parse(source)
    undeclared = meta.find_undeclared_variables(parsed)
    if undeclared != _CONTEXT_KEYS:
        raise PromptValidationError(
            f"template variables must be exactly {sorted(_CONTEXT_KEYS)}; got {sorted(undeclared)}"
        )
    pending: list[nodes.Node] = [parsed]
    while pending:
        node = pending.pop()
        pending.extend(node.iter_child_nodes())
        if not isinstance(node, _ALLOWED_NODE_TYPES):
            raise PromptValidationError(f"Jinja2 node {type(node).__name__!r} is forbidden")
        if isinstance(node, nodes.Filter) and node.name != "e":
            raise PromptValidationError(f"Jinja2 filter {node.name!r} is forbidden")
        if isinstance(node, nodes.Getattr):
            allowed_attributes = (
                _GETATTR_ALLOWLIST.get(node.node.name, frozenset())
                if isinstance(node.node, nodes.Name)
                else frozenset()
            )
            if node.attr not in allowed_attributes:
                raise PromptValidationError(f"Jinja2 attribute access {node.attr!r} is forbidden")
        if isinstance(node, nodes.For):
            top_level_binding = (
                isinstance(node.target, nodes.Name)
                and isinstance(node.iter, nodes.Name)
                and _FOR_BINDINGS.get(node.iter.name) == node.target.name
            )
            recommended_tool_binding = (
                isinstance(node.target, nodes.Name)
                and node.target.name == "tool_name"
                and isinstance(node.iter, nodes.Getattr)
                and isinstance(node.iter.node, nodes.Name)
                and node.iter.node.name == "skill"
                and node.iter.attr == "recommended_tools"
            )
            if (
                not (top_level_binding or recommended_tool_binding)
                or node.test is not None
                or node.else_
                or node.recursive
            ):
                raise PromptValidationError("Jinja2 loops must use the approved context bindings")
    return environment


def _tag_allowed(parent: str | None, name: str) -> bool:
    """렌더 태그가 고정 위계에서 허용되는지 판정한다.

    Args:
        parent (str | None): 열린 직계 부모 태그 또는 최상위 표식.
        name (str): 검사할 태그 이름.

    Returns:
        bool: 허용된 부모·자식 조합이면 참.

    Raises:
        없음.

    Side Effects:
        없음.
    """

    return (
        (parent is None and name in _TOP_LEVEL_ORDER)
        or (parent == "PRIORITIES" and re.fullmatch(r"P\d+", name) is not None)
        or (parent == "BOUNDARIES" and name == "BOUNDARY")
        or (parent == "SKILLS" and name == "SKILL")
        or (parent == "SKILL" and name in {"DESCRIPTION", "USE_WHEN", "RECOMMENDED_TOOLS"})
        or (parent == "RECOMMENDED_TOOLS" and name == "TOOL_REF")
        or (parent == "TOOLS" and name in {"TOOL_SCHEMA_AUTHORITY", "TOOL_AUTHORIZATION", "TOOL"})
        or (parent == "TOOL" and name in {"PURPOSE", "USAGE"})
        or (parent == "WORKFLOW" and re.fullmatch(r"STEP_\d+", name) is not None)
    )


def _parse_rendered_tags(rendered: str) -> tuple[list[str], list[str]]:
    """태그 문법·위계를 검사하고 최상위·opening 태그를 반환한다.

    Args:
        rendered (str): 렌더된 시스템 프롬프트.

    Returns:
        tuple[list[str], list[str]]: 최상위 태그와 모든 opening 태그.

    Raises:
        PromptValidationError: attribute, nesting 또는 tag 문법이 잘못된 경우.

    Side Effects:
        없음.
    """

    stack: list[str] = []
    top_level: list[str] = []
    opening_tags: list[str] = []
    for match in _TAG_RE.finditer(rendered):
        closing, name, attributes = match.groups()
        if closing and attributes:
            raise PromptValidationError(f"closing tag </{name}> must not have attributes")
        if not closing and name in {"SKILL", "TOOL"}:
            if re.fullmatch(r' name="[A-Za-z0-9_.:-]+"', attributes) is None:
                raise PromptValidationError(f"<{name}> must have exactly one safe name attribute")
        elif not closing and attributes:
            raise PromptValidationError(f"<{name}> must not have attributes")
        if closing:
            if not stack or stack.pop() != name:
                raise PromptValidationError(f"malformed closing tag </{name}>")
            continue
        parent = stack[-1] if stack else None
        if not _tag_allowed(parent, name):
            raise PromptValidationError(f"tag <{name}> is not allowed under {parent!r}")
        if parent is None:
            top_level.append(name)
        opening_tags.append(name)
        stack.append(name)
    if stack:
        raise PromptValidationError(f"unclosed tags: {stack}")
    if "<" in _TAG_RE.sub("", rendered) or ">" in _TAG_RE.sub("", rendered):
        raise PromptValidationError("rendered prompt contains an unknown or malformed tag")
    return top_level, opening_tags


def validate_rendered_prompt(rendered: str, context: Mapping[str, object], max_bytes: int) -> None:
    """렌더된 태그 위계와 크기, Skill·Tool·STEP 결속을 검증한다.

    Args:
        rendered (str): 렌더된 시스템 프롬프트.
        context (Mapping[str, object]): 검증된 context.
        max_bytes (int): 허용하는 렌더 결과의 최대 UTF-8 byte 수.

    Returns:
        없음.

    Raises:
        PromptValidationError: 태그·순서·중복 계약이 깨진 경우.

    Side Effects:
        없음.
    """

    budget = _expect_positive_int(max_bytes, "max_bytes")
    rendered_size = len(rendered.encode("utf-8"))
    if rendered_size > budget:
        raise PromptValidationError(
            f"rendered prompt is {rendered_size} bytes, exceeding max_bytes={budget}"
        )

    top_level, opening_tags = _parse_rendered_tags(rendered)
    if tuple(top_level) != _TOP_LEVEL_ORDER:
        raise PromptValidationError(f"top-level sections must be {_TOP_LEVEL_ORDER}; got {tuple(top_level)}")

    priority_tags = [name for name in opening_tags if re.fullmatch(r"P\d+", name)]
    expected_priorities = [f"P{index}" for index in range(len(_expect_list(context["priorities"], "priorities")))]
    if priority_tags != expected_priorities:
        raise PromptValidationError("rendered priority tags do not match context")

    step_tags = [name for name in opening_tags if re.fullmatch(r"STEP_\d+", name)]
    workflow_steps = _expect_list(context["workflow_steps"], "workflow_steps")
    expected_steps = [f"STEP_{index}" for index in range(1, len(workflow_steps) + 1)]
    if step_tags != expected_steps:
        raise PromptValidationError("rendered STEP tags must be contiguous and match workflow_steps")

    skill_names = re.findall(r'<SKILL name="([^"]+)">', rendered)
    tool_names = re.findall(r'<TOOL name="([^"]+)">', rendered)
    expected_skill_names = [
        str(item["name"]) for item in _expect_list(context["skills"], "skills") if isinstance(item, Mapping)
    ]
    expected_tool_names = [
        str(item["name"]) for item in _expect_list(context["tools"], "tools") if isinstance(item, Mapping)
    ]
    if skill_names != expected_skill_names:
        raise PromptValidationError("rendered Skill order does not match context")
    if tool_names != expected_tool_names:
        raise PromptValidationError("rendered Tool order does not match context")
    expected_tool_refs = [
        str(tool_name)
        for item in _expect_list(context["skills"], "skills")
        if isinstance(item, Mapping)
        for tool_name in _expect_list(item["recommended_tools"], "recommended_tools")
    ]
    tool_refs = re.findall(r"<TOOL_REF>([^<>]+)</TOOL_REF>", rendered)
    if tool_refs != expected_tool_refs:
        raise PromptValidationError("rendered Skill Tool references do not match context")
    if re.search(r"<(?:INPUT|ARGUMENT|OUTPUT)_SCHEMA\b", rendered):
        raise PromptValidationError("native Tool/output schemas must not be duplicated in the prompt")


def render_prompt(template_path: Path, context_path: Path, *, max_bytes: int) -> str:
    """템플릿과 JSON context를 읽어 검증된 프롬프트를 렌더한다.

    Args:
        template_path (Path): Jinja2 template 경로.
        context_path (Path): JSON context 경로.
        max_bytes (int): 허용하는 렌더 결과의 최대 UTF-8 byte 수.

    Returns:
        str: 검증된 렌더 결과.

    Raises:
        PromptValidationError: source, context 또는 렌더 계약이 깨진 경우.
        OSError: 입력 파일을 읽지 못한 경우.
        json.JSONDecodeError: context JSON이 잘못된 경우.

    Side Effects:
        입력 파일을 읽는다.
    """

    source = template_path.read_text(encoding="utf-8")
    raw_context: Any = json.loads(context_path.read_text(encoding="utf-8"))
    context = validate_context(raw_context)
    environment = validate_template_source(source)
    rendered = environment.from_string(source).render(**context).strip() + "\n"
    validate_rendered_prompt(rendered, context, max_bytes)
    return rendered


def main() -> int:
    """CLI 인자를 읽어 프롬프트를 검증·렌더한다.

    Args:
        없음.

    Returns:
        int: 성공이면 0, 검증 실패이면 2.

    Raises:
        없음. 사용자 입력 오류는 stderr와 종료 코드 2로 반환한다.

    Side Effects:
        입력 파일을 읽고 선택적으로 렌더 결과를 파일 또는 stdout에 쓴다.
    """

    parser = argparse.ArgumentParser(description="Validate and render a budgeted structured Jinja2 system prompt.")
    parser.add_argument("--template", type=Path, required=True)
    parser.add_argument("--context", type=Path, required=True)
    parser.add_argument("--max-bytes", type=int, required=True)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    try:
        rendered = render_prompt(args.template, args.context, max_bytes=args.max_bytes)
    except (OSError, json.JSONDecodeError, PromptValidationError, TemplateError) as exc:
        print(f"prompt validation failed: {exc}", file=sys.stderr)
        return 2
    if args.output is None:
        sys.stdout.write(rendered)
    else:
        args.output.write_text(rendered, encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
