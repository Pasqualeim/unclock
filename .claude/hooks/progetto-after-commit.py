#!/usr/bin/env python3
"""PostToolUse hook: after a Bash call that made a git commit, tell Claude to update PROGETTO.md now."""
import json
import re
import sys

event = json.load(sys.stdin)
command = event.get("tool_input", {}).get("command", "")
output = json.dumps(event.get("tool_response", ""))

made_commit = re.search(r"\bgit\b[^|;&]*\bcommit\b", command) and "--dry-run" not in command
if made_commit and "nothing to commit" not in output:
    print(json.dumps({
        "hookSpecificOutput": {
            "hookEventName": "PostToolUse",
            "additionalContext": (
                "Hai appena fatto un commit. In questo stesso turno: aggiorna la tabella Task di "
                "PROGETTO.md (segna fatto, aggiungi il punto nuovo, riordina) e la lista dei task "
                "della sessione, poi docs/ROADMAP.md se una voce è cambiata."
            ),
        }
    }))
