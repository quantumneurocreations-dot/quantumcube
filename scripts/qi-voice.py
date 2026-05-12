#!/usr/bin/env python3
"""
QI Voice Loop — Quantum Integrator
Deepgram ears · Claude mind · Owen voice
Features: barge-in (interrupt Owen mid-sentence) + echo cancellation
Run: qi   (alias in ~/.zshrc)
Stop: Ctrl+C
"""

import os, sys, json, time, threading, tempfile, subprocess, difflib

def read_key(f):
    try: return open(os.path.expanduser(f"~/.config/qi/{f}")).read().strip()
    except: return ''

DEEPGRAM_KEY   = read_key('deepgram_api_key')
ELEVENLABS_KEY = read_key('elevenlabs_api_key')
ANTHROPIC_KEY  = open(os.path.expanduser('~/.config/anthropic/key')).read().strip()
TAVILY_KEY     = read_key('tavily_api_key')
QI_VOICE       = 'giAoKpl5weRTCJK7uB9b'  # Owen

QI_SYSTEM = """You are QI — Quantum Integrator. Personal AI for Ronnie, founder of Quantum Cube.
Be concise — max 2-3 sentences for voice. Direct and mission-focused.
North Star: 500 paying customers by August 15, 2026. Currently 3.
Never say "as an AI". You are QI."""

# ── State ─────────────────────────────────────────────────────────────────────
conversation  = []
recent_output = []        # what Owen said recently (for echo cancellation)
audio_proc    = None      # current afplay process (killable for barge-in)
speaking_lock = threading.Lock()

# ── Echo cancellation ─────────────────────────────────────────────────────────
def is_echo(text):
    """Return True if text closely matches something Owen just said."""
    cutoff = time.time() - 4.0  # ignore echoes within 4 seconds
    for t, said in recent_output:
        if t < cutoff:
            continue
        ratio = difflib.SequenceMatcher(None, text.lower(), said.lower()).ratio()
        if ratio > 0.6:
            return True
    # Clean old entries
    recent_output[:] = [(t, s) for t, s in recent_output if t > cutoff]
    return False

# ── Barge-in: kill Owen mid-sentence ─────────────────────────────────────────
def stop_speaking():
    global audio_proc
    with speaking_lock:
        if audio_proc and audio_proc.poll() is None:
            audio_proc.terminate()
            audio_proc = None

# ── ElevenLabs TTS ────────────────────────────────────────────────────────────
def speak(text):
    global audio_proc
    stop_speaking()  # kill any previous audio first
    print(f"\n  QI: {text}\n")
    recent_output.append((time.time(), text))
    if not ELEVENLABS_KEY:
        return
    try:
        import urllib.request
        payload = json.dumps({
            "text": text,
            "model_id": "eleven_turbo_v2_5",
            "voice_settings": {"stability": 0.5, "similarity_boost": 0.75, "speed": 1.05}
        }).encode()
        req = urllib.request.Request(
            f"https://api.elevenlabs.io/v1/text-to-speech/{QI_VOICE}",
            data=payload,
            headers={"xi-api-key": ELEVENLABS_KEY, "Content-Type": "application/json"}
        )
        with urllib.request.urlopen(req, timeout=20) as r:
            audio = r.read()
        f = tempfile.NamedTemporaryFile(suffix='.mp3', delete=False)
        f.write(audio); fname = f.name; f.close()
        with speaking_lock:
            audio_proc = subprocess.Popen(['afplay', fname])
        audio_proc.wait()
        os.unlink(fname)
    except Exception as e:
        print(f"  [speak error: {e}]")

# ── Tavily web search ────────────────────────────────────────────────────────
def web_search(query):
    if not TAVILY_KEY:
        return None
    import urllib.request
    payload = json.dumps({"api_key": TAVILY_KEY, "query": query,
                          "search_depth": "basic", "max_results": 3}).encode()
    req = urllib.request.Request(
        "https://api.tavily.com/search", data=payload,
        headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=10) as r:
            results = json.loads(r.read()).get("results", [])
        return "\n".join(f"- {r['title']}: {r['content'][:200]}" for r in results[:3])
    except Exception as e:
        return None

SEARCH_TRIGGERS = ["latest", "news", "today", "current", "who is", "what is",
                   "how much", "price", "weather", "score", "when did",
                   "recently", "2026", "2025", "war", "stock", "rate"]

def needs_search(text):
    t = text.lower()
    return any(w in t for w in SEARCH_TRIGGERS)

# ── Claude ────────────────────────────────────────────────────────────────────
def think(user_input):
    import urllib.request
    # Web search if needed
    search_ctx = ""
    if needs_search(user_input) and TAVILY_KEY:
        results = web_search(user_input)
        if results:
            search_ctx = f"\n\n[Live web search results]:\n{results}\n[End search results]"
    conversation.append({"role": "user", "content": user_input + search_ctx})
    payload = json.dumps({
        "model": "claude-sonnet-4-20250514",
        "max_tokens": 150,
        "system": QI_SYSTEM,
        "messages": conversation[-10:]
    }).encode()
    req = urllib.request.Request(
        "https://api.anthropic.com/v1/messages",
        data=payload,
        headers={"x-api-key": ANTHROPIC_KEY,
                 "anthropic-version": "2023-06-01",
                 "Content-Type": "application/json"}
    )
    with urllib.request.urlopen(req, timeout=30) as r:
        result = json.loads(r.read())
    reply = result['content'][0]['text']
    conversation.append({"role": "assistant", "content": reply})
    return reply

def handle_input(text):
    if not text.strip() or len(text.strip()) < 3:
        return
    if is_echo(text):
        print(f"  [echo filtered: {text[:40]}]")
        return
    stop_speaking()  # barge-in: interrupt Owen immediately
    reply = think(text)
    threading.Thread(target=speak, args=(reply,), daemon=True).start()

# ── Deepgram live STT ─────────────────────────────────────────────────────────
def listen(callback):
    if not DEEPGRAM_KEY:
        return keyboard_fallback(callback)
    try:
        import websocket, pyaudio
    except ImportError:
        subprocess.run(['/opt/homebrew/opt/python@3.12/libexec/bin/pip3',
                        'install', 'websocket-client', 'pyaudio',
                        '--break-system-packages', '-q'])
        import websocket, pyaudio

    RATE, CHUNK = 16000, 8000
    pa     = pyaudio.PyAudio()
    stream = pa.open(format=pyaudio.paInt16, channels=1, rate=RATE,
                     input=True, frames_per_buffer=CHUNK)

    url = (f"wss://api.deepgram.com/v1/listen"
           f"?encoding=linear16&sample_rate={RATE}&channels=1"
           f"&model=nova-3&language=en&punctuate=true"
           f"&endpointing=600&interim_results=true&utterance_end_ms=1200")

    def on_message(ws, msg):
        d = json.loads(msg)
        try:
            t = d['channel']['alternatives'][0]['transcript']
            if t.strip() and d.get('is_final'):
                callback(t)
        except: pass

    def on_open(ws):
        print("  QI is listening — speak anytime, interrupt anytime\n")
        def stream_audio():
            while ws.sock and ws.sock.connected:
                ws.send(stream.read(CHUNK, exception_on_overflow=False),
                        websocket.ABNF.OPCODE_BINARY)
        threading.Thread(target=stream_audio, daemon=True).start()

    ws = websocket.WebSocketApp(
        url,
        header=[f"Authorization: Token {DEEPGRAM_KEY}"],
        on_open=on_open,
        on_message=on_message,
        on_error=lambda ws, e: print(f"  [WS: {e}]"),
        on_close=lambda ws, *a: None
    )
    ws.run_forever()
    stream.stop_stream(); stream.close(); pa.terminate()

def keyboard_fallback(callback):
    print("  [Keyboard mode — no Deepgram key]\n")
    while True:
        try:
            t = input("  You: ").strip()
            if t.lower() in ('quit','exit'): break
            if t: callback(t)
        except (EOFError, KeyboardInterrupt): break

# ── Main ──────────────────────────────────────────────────────────────────────
if __name__ == '__main__':
    print("\n" + "─"*50)
    print("  QI — QUANTUM INTEGRATOR")
    print("  Interrupt anytime — QI will stop and listen")
    print("─"*50 + "\n")
    intro = think("Introduce yourself in one sentence.")
    threading.Thread(target=speak, args=(intro,), daemon=True).start()
    try:
        listen(handle_input)
    except KeyboardInterrupt:
        stop_speaking()
        print("\n  QI offline.\n")
