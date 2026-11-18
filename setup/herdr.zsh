# Bare `herdr` selects a persistent session for the current project.
function herdr() {
  # Preserve explicit commands, session overrides, and the caller's Herdr context.
  if (( $# )) || [[ ${HERDR_ENV:-} == 1 || -n ${HERDR_SESSION:-} || -n ${HERDR_SOCKET_PATH:-} ]]; then
    command herdr "$@"
    return
  fi

  local project_root session_hash
  project_root="$(command git -C "$PWD" rev-parse --show-toplevel 2>/dev/null)" || project_root="${PWD:A}"
  project_root="${project_root:A}"
  session_hash="$(printf '%s' "$project_root" | command shasum -a 256)" || return
  command herdr --session "project-${session_hash[1,16]}"
}

# Keep Codex's executor in the terminal that launched it (TUI or herdr-core).
function codex() {
  if [[ ${HERDR_ENV:-} == 1 || -n ${HC_TERMINAL_ID:-} ]]; then
    local arg
    for arg in "$@"; do
      if [[ $arg == --no-daemon || $arg == --remote || $arg == --remote=* ]]; then
        command codex "$@"
        return
      fi
    done
    command codex --no-daemon "$@"
  else
    command codex "$@"
  fi
}
