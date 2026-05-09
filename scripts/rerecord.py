#!/usr/bin/env python3
"""
Batch re-record narration MP3s via ElevenLabs TTS.

Reads scripts from the manifest embedded in docs/audit-narration.html,
applies the Life Phase rewrite for num_pc_*, then either prints a dry-run
preview or POSTs each script to ElevenLabs and saves the result.

Usage:
  ELEVENLABS_API_KEY=... python3 scripts/rerecord.py --dry-run
  ELEVENLABS_API_KEY=... python3 scripts/rerecord.py
"""
import argparse
import hashlib
import json
import os
import re
import sys
import time
import urllib.request
from pathlib import Path

VOICE_ID = "VhxAIIZM8IRmnl5fyeyk"
MODEL_ID = "eleven_turbo_v2_5"
VOICE_SETTINGS = {
    "stability": 0.5,
    "similarity_boost": 0.75,
    "speed": 1.15,
}
THROTTLE_S = 0.5

REPO = Path(__file__).resolve().parent.parent
HTML_PATH = REPO / "docs" / "audit-narration.html"
OUTPUT_DIR = REPO / "docs" / "Sounds" / "Narration"

FILES = [
    "num_lp_1_v2.mp3", "num_lp_3_v3.mp3", "num_lp_4_v1.mp3", "num_lp_7_v3.mp3",
    "num_lp_9_v1.mp3", "num_lp_9_v3.mp3", "num_lp_11_v1.mp3", "num_lp_22_v1.mp3",
    "num_bd_1_v1.mp3", "num_bd_1_v2.mp3", "num_bd_1_v3.mp3",
    "num_bd_2_v1.mp3", "num_bd_2_v2.mp3", "num_bd_2_v3.mp3",
    "num_bd_3_v1.mp3", "num_bd_3_v2.mp3", "num_bd_3_v3.mp3",
    "num_bd_4_v1.mp3", "num_bd_4_v2.mp3", "num_bd_4_v3.mp3",
    "num_bd_5_v1.mp3", "num_bd_5_v2.mp3", "num_bd_5_v3.mp3",
    "num_bd_6_v1.mp3", "num_bd_6_v2.mp3", "num_bd_6_v3.mp3",
    "num_bd_7_v1.mp3", "num_bd_7_v2.mp3", "num_bd_7_v3.mp3",
    "num_bd_8_v1.mp3", "num_bd_8_v2.mp3", "num_bd_8_v3.mp3",
    "num_bd_9_v1.mp3", "num_bd_9_v2.mp3", "num_bd_9_v3.mp3",
    "num_bd_11_v1.mp3", "num_bd_11_v2.mp3", "num_bd_11_v3.mp3",
    "num_bd_22_v1.mp3", "num_bd_22_v2.mp3", "num_bd_22_v3.mp3",
    "num_ex_2_v1.mp3", "num_ex_3_v1.mp3", "num_ex_4_v2.mp3",
    "num_ex_5_v1.mp3", "num_ex_5_v2.mp3", "num_ex_6_v2.mp3",
    "num_ex_7_v1.mp3", "num_ex_7_v3.mp3", "num_ex_11_v1.mp3", "num_ex_22_v1.mp3",
    "num_su_1_v1.mp3", "num_su_3_v3.mp3", "num_su_5_v3.mp3",
    "num_su_7_v1.mp3", "num_su_7_v2.mp3", "num_su_7_v3.mp3",
    "num_su_9_v2.mp3", "num_su_11_v3.mp3", "num_su_22_v3.mp3",
    "num_su_33_v2.mp3", "num_su_33_v3.mp3",
    "num_hp_2_v3.mp3", "num_hp_4_v3.mp3", "num_hp_5_v3.mp3",
    "num_hp_6_v1.mp3", "num_hp_6_v3.mp3", "num_hp_7_v1.mp3", "num_hp_8_v3.mp3",
    "num_kl_1_v1.mp3", "num_kl_2_v1.mp3", "num_kl_2_v2.mp3",
    "num_kl_3_v1.mp3", "num_kl_3_v2.mp3", "num_kl_4_v1.mp3", "num_kl_4_v2.mp3",
    "num_kl_5_v2.mp3", "num_kl_6_v1.mp3", "num_kl_6_v2.mp3",
    "num_kl_7_v1.mp3", "num_kl_7_v2.mp3", "num_kl_9_v1.mp3",
    "num_pc_2_v1.mp3", "num_pc_3_v1.mp3", "num_pc_4_v1.mp3", "num_pc_5_v1.mp3",
    "num_pc_6_v1.mp3", "num_pc_7_v1.mp3", "num_pc_8_v1.mp3", "num_pc_9_v1.mp3",
    "west_aries_career.mp3", "west_gemini_str.mp3",
    "west_virgo_core.mp3", "west_pisces_core.mp3",
    "chin_ox_core.mp3", "chin_ox_shadow.mp3", "chin_ox_love.mp3",
    "chin_dog_core.mp3",
]


def load_manifest():
    html = HTML_PATH.read_text(encoding="utf-8")
    m = re.search(
        r'<script type="application/json" id="manifest-data">(.*?)</script>',
        html, re.S
    )
    if not m:
        raise RuntimeError("manifest-data script tag not found")
    rows = json.loads(m.group(1))
    return {r["filename"]: r["text"] for r in rows}


LIFE_PHASE_RE = re.compile(r"^An?\s+(\d+)\s+Life Phase marks\b")


def transform(filename: str, text: str) -> str:
    """Apply per-filename script tweaks before TTS."""
    if re.match(r"^num_pc_[2-9]_v1\.mp3$", filename):
        new_text, n = LIFE_PHASE_RE.subn(
            lambda mm: f"A Life Phase governed by the {mm.group(1)} marks",
            text, count=1,
        )
        if n == 0:
            raise RuntimeError(f"{filename}: Life Phase opening not found")
        return new_text
    return text


def tts(api_key: str, text: str) -> bytes:
    body = json.dumps({
        "text": text,
        "model_id": MODEL_ID,
        "voice_settings": VOICE_SETTINGS,
    }).encode("utf-8")
    req = urllib.request.Request(
        f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}",
        data=body,
        headers={
            "xi-api-key": api_key,
            "Content-Type": "application/json",
            "Accept": "audio/mpeg",
        },
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=120) as resp:
        audio = resp.read()
    if len(audio) < 1000:
        raise RuntimeError(f"suspiciously small response: {len(audio)} bytes")
    return audio


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    scripts = load_manifest()

    missing = [f for f in FILES if f not in scripts]
    if missing:
        print(f"ERROR: {len(missing)} filenames not in manifest:", file=sys.stderr)
        for f in missing:
            print(f"  {f}", file=sys.stderr)
        sys.exit(1)

    if args.dry_run:
        print(f"DRY RUN — {len(FILES)} files\n")
        for fn in FILES:
            text = transform(fn, scripts[fn])
            print(f"{fn}: {text[:100]}")
        return

    api_key = os.environ.get("ELEVENLABS_API_KEY")
    if not api_key:
        print("ERROR: ELEVENLABS_API_KEY env var not set", file=sys.stderr)
        sys.exit(1)

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    hashes = {}
    ok = 0
    fail = 0
    for i, fn in enumerate(FILES, 1):
        text = transform(fn, scripts[fn])
        out = OUTPUT_DIR / fn
        prefix = f"[{i}/{len(FILES)}]"
        try:
            audio = tts(api_key, text)
            out.write_bytes(audio)
            digest = hashlib.sha256(audio).hexdigest()
            hashes[fn] = digest
            print(f"{prefix} ✓ {fn} ({len(audio)/1024:.1f}KB)")
            ok += 1
        except Exception as e:
            print(f"{prefix} ✗ {fn}: {e}")
            fail += 1
        if i < len(FILES):
            time.sleep(THROTTLE_S)

    print(f"\nDone. OK: {ok}  FAIL: {fail}")
    print("\n--- SHA256 JSON for manifest update ---")
    print(json.dumps(hashes, indent=2))


if __name__ == "__main__":
    main()
