#!/usr/bin/env python3
"""
QI Research Layer — saves voice research notes to Google Drive
Notes auto-tagged with date + topic → load into NotebookLM manually

Usage:
  python3 scripts/qi-research.py save "topic" "note content"
  python3 scripts/qi-research.py list
  python3 scripts/qi-research.py export          → exports all as markdown

Requires: ~/.config/qi/gdrive-service-account.json  (Drive API service account)
Or uses OAuth token at ~/.config/qi/gdrive-token.json if available.
"""
import json, os, sys, urllib.request, urllib.parse, time
from datetime import datetime

NOTES_DIR    = os.path.expanduser("~/.config/qi/research-notes")
GDRIVE_KEY   = os.path.expanduser("~/.config/qi/gdrive-service-account.json")
OAUTH_TOKEN  = os.path.expanduser("~/.config/qi/gdrive-token.json")
FOLDER_NAME  = "QI Research Notes"

os.makedirs(NOTES_DIR, exist_ok=True)

# ── Local note storage (always works, no auth needed) ─────────────────────────
def save_local(topic, content):
    """Save note locally as markdown. Always available."""
    ts   = datetime.now().strftime("%Y-%m-%d_%H-%M")
    slug = topic.lower().replace(" ", "-")[:40]
    path = os.path.join(NOTES_DIR, f"{ts}_{slug}.md")
    body = f"# {topic}\n**Date:** {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n{content}\n"
    with open(path, "w") as f:
        f.write(body)
    print(f"Saved locally: {path}")
    return path

def list_notes():
    """List all saved research notes."""
    files = sorted(os.listdir(NOTES_DIR))
    if not files:
        print("No research notes yet.")
        return
    print(f"\n{'Date':<20} {'Topic':<50}")
    print("-" * 70)
    for f in files:
        parts = f.replace(".md", "").split("_", 2)
        date  = f"{parts[0]} {parts[1].replace('-', ':')}" if len(parts) >= 2 else f
        topic = parts[2].replace("-", " ").title() if len(parts) >= 3 else ""
        print(f"{date:<20} {topic:<50}")

def export_markdown():
    """Export all notes as a single markdown file for NotebookLM upload."""
    files = sorted(os.listdir(NOTES_DIR))
    if not files:
        print("No notes to export.")
        return
    out_path = os.path.expanduser("~/Desktop/qi-research-export.md")
    with open(out_path, "w") as out:
        out.write("# QI Research Notes Export\n")
        out.write(f"**Exported:** {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n---\n\n")
        for fname in files:
            fpath = os.path.join(NOTES_DIR, fname)
            with open(fpath) as f:
                out.write(f.read())
                out.write("\n\n---\n\n")
    print(f"Exported {len(files)} notes to: {out_path}")
    print("Load this file into NotebookLM as a source.")
    return out_path

# ── Google Drive upload (optional — requires service account) ─────────────────
def get_gdrive_token():
    """Get Drive access token. Tries service account first, then OAuth cache."""
    # Try OAuth cached token
    if os.path.exists(OAUTH_TOKEN):
        tok = json.load(open(OAUTH_TOKEN))
        if tok.get("access_token") and tok.get("expiry", 0) > time.time():
            return tok["access_token"]
    print("Drive upload not configured. Note saved locally only.")
    print("To enable Drive sync: run 'python3 scripts/qi-research.py auth'")
    return None

def upload_to_drive(local_path, topic):
    """Upload note to Google Drive QI Research Notes folder."""
    token = get_gdrive_token()
    if not token:
        return None
    # Find or create folder
    q = urllib.parse.quote(f"name='{FOLDER_NAME}' and mimeType='application/vnd.google-apps.folder' and trashed=false")
    req = urllib.request.Request(
        f"https://www.googleapis.com/drive/v3/files?q={q}",
        headers={"Authorization": f"Bearer {token}"}
    )
    folders = json.loads(urllib.request.urlopen(req).read()).get("files", [])
    if folders:
        folder_id = folders[0]["id"]
    else:
        # Create folder
        body = json.dumps({"name": FOLDER_NAME,
                           "mimeType": "application/vnd.google-apps.folder"}).encode()
        req = urllib.request.Request(
            "https://www.googleapis.com/drive/v3/files",
            data=body, headers={"Authorization": f"Bearer {token}",
                                 "Content-Type": "application/json"}
        )
        folder_id = json.loads(urllib.request.urlopen(req).read())["id"]

    # Upload file
    fname = os.path.basename(local_path)
    with open(local_path, "rb") as f:
        content = f.read()
    boundary = "qi_boundary_12345"
    meta = json.dumps({"name": fname, "parents": [folder_id]}).encode()
    body = (f"--{boundary}\r\nContent-Type: application/json\r\n\r\n".encode() +
            meta + f"\r\n--{boundary}\r\nContent-Type: text/markdown\r\n\r\n".encode() +
            content + f"\r\n--{boundary}--\r\n".encode())
    req = urllib.request.Request(
        "https://www.googleapis.com/upload/drive/v3/files?uploadType=multipart",
        data=body,
        headers={"Authorization": f"Bearer {token}",
                 "Content-Type": f"multipart/related; boundary={boundary}"}
    )
    result = json.loads(urllib.request.urlopen(req).read())
    print(f"Uploaded to Drive: {result.get('name')} (id: {result.get('id')})")
    return result.get("id")

# ── CLI interface ─────────────────────────────────────────────────────────────
def main():
    args = sys.argv[1:]
    if not args or args[0] == "list":
        list_notes()
    elif args[0] == "export":
        export_markdown()
    elif args[0] == "save" and len(args) >= 3:
        topic, content = args[1], " ".join(args[2:])
        local = save_local(topic, content)
        upload_to_drive(local, topic)
    elif args[0] == "save" and len(args) == 2:
        # Read content from stdin
        print("Enter note content (Ctrl+D to finish):")
        content = sys.stdin.read().strip()
        local = save_local(args[1], content)
        upload_to_drive(local, args[1])
    else:
        print("Usage: qi-research.py [save <topic> <content> | list | export]")

if __name__ == "__main__":
    main()
