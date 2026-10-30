#!/bin/bash
# Copies the post media (marketing/images/x, marketing/video/x) to the Raspberry Pi
# folder served at https://media.getunclock.app/. Adds and updates only, never deletes:
# the Pi may hold files of posts already scheduled on Buffer. Run hourly by the
# LaunchAgent app.getunclock.syncmedia; details in docs/social/MEDIA_HOST.md.
set -u

REPO="$(cd "$(dirname "$0")/../.." && pwd)"
HOST="unclock-pi"                 # alias in ~/.ssh/config
DEST="/"                          # the Pi key runs rrsync, rooted at /home/pasquale/media
LOG="$HOME/Library/Logs/unclock-sync.log"

log() { echo "$(date '+%Y-%m-%d %H:%M:%S') $*" >> "$LOG"; }

shopt -s nullglob nocaseglob
files=()
for dir in "$REPO/marketing/images/x" "$REPO/marketing/video/x"; do
    files+=("$dir"/*.png "$dir"/*.jpg "$dir"/*.jpeg "$dir"/*.gif "$dir"/*.mp4)
done
[ ${#files[@]} -eq 0 ] && exit 0

# Away from home the Pi is not reachable: one line in the log, no error.
# Probe the SSH port, not a shell: the key on the Pi may only run rsync.
ip=$(ssh -G "$HOST" | awk '$1 == "hostname" { print $2 }')
if ! nc -z -G 5 "$ip" 22 2>/dev/null; then
    log "Pi non raggiungibile, salto (${#files[@]} file in attesa)"
    exit 0
fi

# --modify-window=1: the Pi folder is on a FAT32 disk, which keeps times to 2 seconds.
if out=$(/usr/bin/rsync -tp --modify-window=1 --chmod=u=rw,go=r --itemize-changes "${files[@]}" "$HOST:$DEST" 2>&1); then
    copied=$(printf '%s\n' "$out" | grep -c '^<f')
    [ "$copied" -gt 0 ] && log "copiati $copied file"
    exit 0
fi
err="$(printf '%s' "$out" | tail -1)"
# Slack only on the first failure of a streak, not every hour (docs/social/SLACK.md).
if ! tail -1 "$LOG" 2>/dev/null | grep -q 'errore rsync'; then
    msg="<@U0CDER0KVRS> :x: *Copia dei media sul Pi non riuscita:* $err. I post su X con immagini nuove potrebbero uscire senza. Dettagli in ~/Library/Logs/unclock-sync.log"
    /usr/bin/python3 -c 'import json,sys; print(json.dumps({"text": sys.argv[1]}))' "$msg" |
        curl -s -m 20 -X POST -H 'Content-type: application/json' --data @- \
            "$(cat "$HOME/.config/unclock/slack_webhook")" >/dev/null
fi
log "errore rsync: $err"
exit 1
