#!/usr/bin/env python3
"""
Quantum Cube version bump script.
Usage: python3 scripts/bump-version.py [new_version]
  e.g. python3 scripts/bump-version.py 323
       (pass just the number — qc-v prefix is added automatically)

If no argument given, auto-increments current version by 1.

Touches ALL version strings in docs/app.html and docs/sw.js:
  - Cache version:         qc-vNNN
  - Sentry release tag:    release: "quantum-cube@qc-vNNN"
  - Anything else matching qc-v[digits]

Run this instead of hand-editing. Never use --no-verify to bypass the
pre-commit hook for version issues — fix the version, then commit clean.
"""
import re, sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
APP  = ROOT / "docs/app.html"
SW   = ROOT / "docs/sw.js"

def current_version():
    m = re.search(r"qc-v(\d+)", SW.read_text())
    if not m:
        sys.exit("✗ Could not find qc-vNNN in docs/sw.js")
    return int(m.group(1))

def bump(files, old_num, new_num):
    old, new = f"qc-v{old_num}", f"qc-v{new_num}"
    for f in files:
        c = f.read_text()
        updated = c.replace(old, new)
        if updated == c:
            print(f"  ⚠ no occurrences of {old} in {f.name}")
        else:
            count = c.count(old)
            f.write_text(updated)
            print(f"  ✓ {f.name}: {count}x  {old} → {new}")

old = current_version()
new = int(sys.argv[1]) if len(sys.argv) > 1 else old + 1

if new <= old:
    sys.exit(f"✗ New version ({new}) must be > current ({old})")

print(f"Bumping qc-v{old} → qc-v{new}")
bump([APP, SW], old, new)

# Verify the hook will pass
sw_ver  = re.search(r"qc-v(\d+)", SW.read_text()).group(1)
app_ver = re.search(r'quantum-cube@qc-v(\d+)', APP.read_text()).group(1)
if sw_ver != app_ver:
    sys.exit(f"✗ DRIFT after bump! sw={sw_ver} app={app_ver} — something went wrong")

print(f"✓ All in sync at qc-v{new}")
print(f"  Next: git add docs/app.html docs/sw.js && git commit -m 'chore: bump qc-v{new}'")
