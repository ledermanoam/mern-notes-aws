#!/bin/bash
# PreToolUse hook for Bash. Blocks any rm command that targets a .env file.
# Reads the JSON payload from stdin; exits 2 to block, with the reason on stderr.
CMD="$(jq -r '.tool_input.command')"

if echo "$CMD" | grep -Eq '(^|[ |&;])rm[[:space:]][^|&;]*\.env([[:space:]]|$|[^[:alnum:]_])'; then
  echo "Blocked by hook: deleting .env files is not allowed in this project." >&2
  exit 2
fi

exit 0
