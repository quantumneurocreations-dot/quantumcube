#!/usr/bin/env python3
"""
QI Voice Loop v4 — streaming pipeline for low latency
Claude streams tokens → sentence detected → ElevenLabs immediately → queue playback
Target: <1.5s from end of speech to first word from Owen
"""
import os, sys, json, re, time, queue, threading, tempfile, subprocess

def read_key(f):
    try: return open(os.path.expanduser(f"~/.config/qi/{f}")).read().strip()
    except: return ""

DEEPGRAM_KEY   = read_key("deepgram_api_key")
ELEVENLABS_KEY = read_key("elevenlabs_api_key")
ANTHROPIC_KEY  = open(os.path.expanduser("~/.config/anthropic/key")).read().strip()
TAVILY_KEY     = read_key("tavily_api_key")
QI_VOICE       = "giAoKpl5weRTCJK7uB9b"

# ── System prompt tuned for voice latency ────────────────────────────────────
QI_SYSTEM = """You are QI — Quantum Integrator. Personal AI for Ronnie, founder of Quantum Cube.

VOICE RULES — follow exactly:
- Start EVERY response with a filler: "Hmm," or "Got it," or "Right," or "Sure,"
- Max 2 short sentences total. Under 15 words each.
- No lists, no bullet points, no markdown.
- Spell out numbers: "seventeen" not "17", "fifty" not "50".
- End with a question only when it genuinely moves things forward.

Mission: 500 paying customers by August 15 2026. Currently 3."""

conversation  = []
audio_queue   = queue.Queue()   # sentences waiting to be spoken
last_spoke_at = 0
COOLDOWN      = 2.5
MIN_WORDS     = 3

# ── Audio player thread ───────────────────────────────────────────────────────
current_audio = None

def audio_player():
    """Dedicated thread: pulls sentences from queue and plays them sequentially."""
    global current_audio, last_spoke_at
    while True:
        text = audio_queue.get()
        if text is None: break
        _speak_sentence(text)
        audio_queue.task_done()

def _speak_sentence(text):
    global current_audio, last_spoke_at
    if not text.strip() or not ELEVENLABS_KEY:
        print(f"\n  QI: {text}")
        last_spoke_at = time.time()
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
        with urllib.request.urlopen(req, timeout=15) as r:
            audio = r.read()
        f = tempfile.NamedTemporaryFile(suffix=".mp3", delete=False)
        f.write(audio); fname = f.name; f.close()
        current_audio = subprocess.Popen(["afplay", fname])
        current_audio.wait()
        os.unlink(fname)
    except Exception as e:
        print(f"  [speak error: {e}]")
    finally:
        last_spoke_at = time.time()

def stop_speaking():
    global current_audio
    # Clear the queue
    while not audio_queue.empty():
        try: audio_queue.get_nowait()
        except: pass
    if current_audio and current_audio.poll() is None:
        current_audio.terminate()
        current_audio = None

# ── Tavily search ─────────────────────────────────────────────────────────────
SEARCH_WORDS = ["latest","news","today","current","war","price","weather",
                "who is","what happened","score","recently","2026","2025","just"]

def maybe_search(text):
    if not TAVILY_KEY or not any(w in text.lower() for w in SEARCH_WORDS):
        return ""
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

# ── Claude streaming → sentence chunker ──────────────────────────────────────
SENTENCE_END = re.compile(r'(?<=[.!?])\s+')

def think_and_stream(user_input):
    """Stream Claude response, detect sentence boundaries, queue each sentence."""
    import urllib.request, http.client

    ctx = maybe_search(user_input)
    msg = user_input + (f"\n\n[Web search]:\n{ctx}" if ctx else "")
    conversation.append({"role": "user", "content": msg})

    payload = json.dumps({
        "model": "claude-haiku-4-5",   # fastest Claude model for voice
        "max_tokens": 120,
        "stream": True,
        "system": QI_SYSTEM,
        "messages": conversation[-8:]
    }).encode()

    buffer = ""
    full_reply = ""
    first_sentence_sent = False

    try:
        conn = http.client.HTTPSConnection("api.anthropic.com")
        conn.request("POST", "/v1/messages", payload, {
            "x-api-key": ANTHROPIC_KEY,
            "anthropic-version": "2023-06-01",
            "Content-Type": "application/json",
            "Accept": "text/event-stream"
        })
        resp = conn.getresponse()

        for raw_line in resp:
            line = raw_line.decode("utf-8").strip()
            if not line.startswith("data:"): continue
            data = line[5:].strip()
            if data == "[DONE]": break
            try:
                chunk = json.loads(data)
                if chunk.get("type") == "content_block_delta":
                    token = chunk["delta"].get("text", "")
                    buffer += token
                    full_reply += token

                    # Check for sentence boundary
                    parts = SENTENCE_END.split(buffer)
                    if len(parts) > 1:
                        # Send all complete sentences immediately
                        for sentence in parts[:-1]:
                            s = sentence.strip()
                            if s:
                                print(f"\n  QI: {s}")
                                audio_queue.put(s)
                                first_sentence_sent = True
                        buffer = parts[-1]
            except: pass

        conn.close()

        # Send any remaining text
        if buffer.strip():
            print(f"\n  QI: {buffer.strip()}")
            audio_queue.put(buffer.strip())

    except Exception as e:
        print(f"  [Claude error: {e}]")
        audio_queue.put("Got it. Something went wrong on my end.")
        full_reply = ""

    if full_reply:
        conversation.append({"role": "assistant", "content": full_reply})

# ── Handle user input ─────────────────────────────────────────────────────────
def handle_input(text):
    text = text.strip()
    if time.time() - last_spoke_at < COOLDOWN:
        return
    if len(text.split()) < MIN_WORDS:
        return
    print(f"\n  You: {text}")
    stop_speaking()
    threading.Thread(target=think_and_stream, args=(text,), daemon=True).start()

# ── Deepgram listener ─────────────────────────────────────────────────────────
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
    pa = pyaudio.PyAudio()
    stream = pa.open(format=pyaudio.paInt16, channels=1, rate=RATE,
                     input=True, frames_per_buffer=CHUNK)

    # endpointing=1500 — waits 1.5s silence before cutting, catches full sentences
    url = (f"wss://api.deepgram.com/v1/listen"
           f"?encoding=linear16&sample_rate={RATE}&channels=1"
           f"&model=nova-3&language=en&punctuate=true&endpointing=1500")

    def on_message(ws, msg):
        d = json.loads(msg)
        try:
            t = d["channel"]["alternatives"][0]["transcript"]
            if t.strip() and d.get("is_final"):
                callback(t)
        except: pass

    def on_open(ws):
        print("  QI is listening — speak naturally\n")
        def send():
            while ws.sock and ws.sock.connected:
                ws.send(stream.read(CHUNK, exception_on_overflow=False),
                        websocket.ABNF.OPCODE_BINARY)
        threading.Thread(target=send, daemon=True).start()

    ws = websocket.WebSocketApp(url,
        header=[f"Authorization: Token {DEEPGRAM_KEY}"],
        on_open=on_open, on_message=on_message,
        on_error=lambda ws, e: print(f"  [WS: {e}]"),
        on_close=lambda ws, *a: None)
    ws.run_forever()
    stream.stop_stream(); stream.close(); pa.terminate()

def keyboard_fallback(callback):
    print("  [Keyboard mode — no Deepgram]\n")
    while True:
        try:
            t = input("  You: ").strip()
            if t.lower() in ("quit","exit"): break
            if t: callback(t)
        except (EOFError, KeyboardInterrupt): break

# ── Main ──────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("\n" + "─"*50)
    print("  QI — QUANTUM INTEGRATOR  v4")
    print("  Streaming pipeline · sentence-by-sentence")
    print("─"*50 + "\n")

    # Start audio player thread
    player = threading.Thread(target=audio_player, daemon=True)
    player.start()

    # Intro via streaming
    think_and_stream("Introduce yourself in one sentence. Start with 'Hmm,'")

    try:
        listen(handle_input)
    except KeyboardInterrupt:
        stop_speaking()
        audio_queue.put(None)
        print("\n  QI offline.\n")
