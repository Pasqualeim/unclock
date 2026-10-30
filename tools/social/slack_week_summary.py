#!/usr/bin/env python3
"""Sends a week of X posts, read from a plan in marketing/x/, to Slack #unclock-x
through the "Unclock avvisi" webhook (docs/social/SLACK.md).

    python3 tools/social/slack_week_summary.py <plan.md> "<header>" "<note>"
    python3 tools/social/slack_week_summary.py --check <plan.md>   # parse only, print

The webhook URL is secret: it is read from ~/.config/unclock/slack_webhook, never
from the repo. Plan format: "## N. <day>, <time>: <title>", a "Media: `path`" line,
the post in ```text blocks, the first reply in the ```text block after "Prima risposta".
"""
import json
import re
import sys
import urllib.request
from pathlib import Path

MEDIA = "https://media.getunclock.app/"
MENTION = "<@U0CDER0KVRS>"
WEBHOOK = Path.home() / ".config/unclock/slack_webhook"


def parse(plan):
    posts = []
    for sec in re.split(r"^## (?=\d+\.)", plan, flags=re.M)[1:]:
        head = sec.splitlines()[0]
        when, _, title = re.sub(r"^\d+\.\s*", "", head).partition(": ")
        media = re.search(r"^Media: `([^`]+)`", sec, re.M)
        body, _, after = sec.partition("Prima risposta")
        blocks = re.findall(r"```text\n(.*?)\n```", body, re.S)
        reply = re.findall(r"```text\n(.*?)\n```", after, re.S)
        posts.append({
            "when": when.strip(), "title": title.strip(),
            "media": Path(media.group(1)).name if media else None,
            "text": "\n".join(blocks),
            "reply": reply[0] if reply else "(link nell'ultimo post del thread)",
        })
    return posts


def blocks(posts, header, note):
    out = [{"type": "header", "text": {"type": "plain_text", "text": header}},
           {"type": "section", "text": {"type": "mrkdwn", "text": f"{MENTION} {note}"}}]
    for p in posts:
        quote = ">" + p["text"].replace("\n", "\n>")
        out += [{"type": "divider"},
                {"type": "section", "text": {"type": "mrkdwn",
                 "text": f"*{p['when']}* · {p['title']}\n{quote}\n_Prima risposta:_ {p['reply']}"[:2900]}}]
        if p["media"] and p["media"].endswith((".png", ".jpg", ".jpeg", ".gif")):
            out.append({"type": "image", "image_url": MEDIA + p["media"], "alt_text": p["title"]})
        elif p["media"]:
            out.append({"type": "section", "text": {"type": "mrkdwn", "text": f"🎬 <{MEDIA + p['media']}|Guarda il video>"}})
    return out


def main(argv):
    if argv[:1] == ["--check"]:
        for p in parse(Path(argv[1]).read_text()):
            print(p["when"], "|", p["title"], "|", p["media"], "|", len(p["text"]), "car.")
        return 0
    plan, header, note = argv
    posts = parse(Path(plan).read_text())
    assert posts, f"nessun post trovato in {plan}"
    payload = {"text": header, "blocks": blocks(posts, header, note)}
    req = urllib.request.Request(WEBHOOK.read_text().strip(), data=json.dumps(payload).encode(),
                                 headers={"Content-Type": "application/json"})
    answer = urllib.request.urlopen(req, timeout=20).read().decode()
    print(answer)
    return 0 if answer == "ok" else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
