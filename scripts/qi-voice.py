#!/usr/bin/env python3
"""
QI Voice Loop v3 — hard cooldown + minimum length + no interim results
"""
import os, sys, json, time, threading, tempfile, subprocess, difflib

def read_key(f):
    try: return open(os.path.expanduser(f"~/.config/qi/{f}")).read().strip()
    except: return ""

DEEPGRAM_KEY   = read_key("deepgram_api_key")
ELEVENLABS_KEY = read_key("elevenlabs_api_key")
ANTHROPIC_KEY  = open(os.path.expanduser("~/.config/anthropic/key")).read().strip()
TAVILY_KEY     = read_key("tavily_api_key")
QI_VOICE       = "giAoKpl5weRTCJK7uB9b"  # Owen

QI_SYSTEM = """You are QI — Quantum Integrator. Personal AI for Ronnie, founder of Quantum Cube.
Keep responses under 2 sentences for voice. Be direct and mission-focused.
North Star: 500 paying customers by August 15, 2026. Currently 3.
Never say "as an AI". You are QI."""

# ── State ─────────────────────────────────────────────────────────────────────
conversation  = []
audio_proc    = None
last_spoke_at = 0          # timestamp when Owen last finished speaking
COOLDOWN_SECS = 3.0        # ignore all mic input for this long after Owen speaks
MIN_WORDS     = 3          # ignore transcripts shorter than this

# ── Stop Owen ─────────────────────────────────────────────────────────────────
def stop_speaking():
    global audio_proc
    if audio_proc and audio_proc.poll() is None:
        audio_proc.terminate()
        audio_proc = None

# ── ElevenLabs ────────────────────────────────────────────────────────────────
def speak(text):
    global audio_proc, last_spoke_at
    stop_speaking()
    print(f"\n  QI: {text}\n")
    if not ELEVENLABS_KEY:
        return
    try:
        import urllib.request
        payload = json.dumps({
            "text": text, "model_id": "eleven_turbo_v2_5",
            "voice_settings": {"stability": 0.5, "similarity_boost": 0.75, "speed": 1.05}
        }).encode()
        req = urllib.request.Request(
            f"https://api.elevenlabs.io/v1/text-to-speech/{QI_VOICE}",
            data=payload,
            headers={"xi-api-key": ELEVENLABS_KEY, "Content-Type": "application/json"})
        with urllib.request.urlopen(req, timeout=20) as r:
            audio = r.read()
        f = tempfile.NamedTemporaryFile(suffix=".mp3", delete=False)
        f.write(audio); fname = f.name; f.close()
        audio_proc = subprocess.Popen(["afplay", fname])
        audio_proc.wait()
        os.unlink(fname)
    except Exception as e:
        print(f"  [speak error: {e}]")
    finally:
        last_spoke_at = time.time()  # cooldown starts when Owen FINISHES

# ── Tavily ────────────────────────────────────────────────────────────────────
SEARCH_WORDS = ["latest","news","today","current","war","price","weather",
                "who is","what happened","score","recently","2026","2025"]

def maybe_search(text):
    if not TAVILY_KEY: return ""
    t = text.lower()
    if not any(w in t for w in SEARCH_WORDS): return ""
    try:
        import urllib.request
        payload = json.dumps({"api_key": TAVILY_KEY, "query": text,
                              "search_depth": "basic", "max_results": 3}).encode()
        req = urllib.request.Request("https://api.tavily.com/search", data=payload,
            headers={"Content-Type": "application/json"})
        with urllib.request.urlopen(req, timeout=8) as r:
            results = json.loads(r.read()).get("results", [])
        return "\n".join(f"- {r['title']}: {r['content'][:200]}" for r in results[:3])
    except: return ""

# ── Claude ────────────────────────────────────────────────────────────────────
def think(user_input):
    import urllib.request
    ctx = maybe_search(user_input)
    msg = user_input + (f"\n\n[Web search results]:\n{ctx}" if ctx else "")
    conversation.append({"role": "user", "content": msg})
    payload = json.dumps({
        "model": "claude-sonnet-4-20250514", "max_tokens": 120,
        "system": QI_SYSTEM, "messages": conversation[-8:]
    }).encode()
    req = urllib.request.Request("https://api.anthropic.com/v1/messages",
        data=payload,
        headers={"x-api-key": ANTHROPIC_KEY,
                 "anthropic-version": "2023-06-01",
                 "Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=30) as r:
        result = json.loads(r.read())
    reply = result["content"][0]["text"]
    conversation.append({"role": "assistant", "content": reply})
    return reply

# ── Handle input ──────────────────────────────────────────────────────────────
def handle_input(text):
    text = text.strip()
    # Hard cooldown — ignore everything for COOLDOWN_SECS after Owen speaks
    if time.time() - last_spoke_at < COOLDOWN_SECS:
        print(f"  [cooldown — ignored: {text[:40]}]")
        return
    # Minimum word count — ignore noise/partial picks
    if len(text.split()) < MIN_WORDS:
        print(f"  [too short — ignored: {text}]")
        return
    print(f"  You: {text}")
    stop_speaking()  # barge-in
    reply = think(text)
    threading.Thread(target=speak, args=(reply,), daemon=True).start()

# ── Deepgram ──────────────────────────────────────────────────────────────────
def listen(callback):
    if not DEEPGRAM_KEY:
        return keyboard_fallback(callback)
    try:
        import websocket, pyaudio
    except ImportError:
        subprocess.run(["/opt/homebrew/opt/python@3.12/libexec/bin/pip3",
                        "install", "websocket-client", "pyaudio",
                        "--break-system-packages", "-q"])
        import websocket, pyaudio

    RATE, CHUNK = 16000, 8000
    pa     = pyaudio.PyAudio()
    stream = pa.open(format=pyaudio.paInt16, channels=1,
                     rate=RATE, input=True, frames_per_buffer=CHUNK)

    # No interim_results, no utterance_end — clean final transcripts only
    url = (f"wss://api.deepgram.com/v1/listen"
           f"?encoding=linear16&sample_rate={RATE}&channels=1"
           f"&model=nova-3&language=en&punctuate=true&endpointing=800")

    def on_message(ws, msg):
        d = json.loads(msg)
        try:
            t = d["channel"]["alternatives"][0]["transcript"]
            if t.strip() and d.get("is_final"):
                callback(t)
        except: pass

    def on_open(ws):
        print("  QI is listening — speak naturally, interrupt anytime\n")
        def send():
            while ws.sock and ws.sock.connected:
                ws.send(stream.read(CHUNK, exception_on_overflow=False),
                        websocket.ABNF.OPCODE_BINARY)
        threading.Thread(target=send, daemon=True).start()

    ws = websocket.WebSocketApp(url,
        header=[f"Authorization: Token {DEEPGRAM_KEY}"],
        on_open=on_open, on_message=on_message,
        on_error=lambda ws, e: print(f"  [WS error: {e}]"),
        on_close=lambda ws, *a: None)
    ws.run_forever()
    stream.stop_stream(); stream.close(); pa.terminate()

def keyboard_fallback(callback):
    print("  [Keyboard mode]\n")
    while True:
        try:
            t = input("  You: ").strip()
            if t.lower() in ("quit","exit"): break
            if t: callback(t)
        except (EOFError, KeyboardInterrupt): break

# ── Main ──────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("\n" + "─"*50)
    print("  QI — QUANTUM INTEGRATOR  v3")
    print("  Speak naturally · interrupt anytime")
    print("─"*50 + "\n")
    intro = think("Introduce yourself in one sentence.")
    threading.Thread(target=speak, args=(intro,), daemon=True).start()
    try:
        listen(handle_input)
    except KeyboardInterrupt:
        stop_speaking()
        print("\n  QI offline.\n")
