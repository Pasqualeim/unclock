#!/usr/bin/env python3
"""PostToolUse hook: after a Bash call that made a git commit, tell Claude to sync Trello now."""
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
                "Hai appena fatto un commit. In questo stesso turno, prima di chiudere: "
                "aggiorna la bacheca Trello Unclock (aggiungi il punto alla carta del diario di oggi "
                "in \"✅ Fatto\", o creala; sposta o chiudi la carta del task se è finito; crea la carta "
                "di un task nuovo), poi PROGETTO.md e docs/ROADMAP.md se un task è cambiato."
            ),
        }
    }))
