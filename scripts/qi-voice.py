#!/usr/bin/env python3
"""
QI Voice Loop v4 — streaming pipeline for low latency
Claude streams tokens → sentence detected → ElevenLabs immediately → queue playback
Target: <1.5s from end of speech to first word from Owen
"""
import os, sys, json, re, time, queue, threading, tempfile, subprocess
from datetime import datetime

# ── Security layer — prompt injection protection ──────────────────────────────
INJECTION_PATTERNS = [
    r'ignore\s+(previous|all|your|prior)\s+(instructions?|prompts?|rules?|constraints?)',
    r'(system\s+prompt|system\s+message)',
    r'(jailbreak|jail\s*break)',
    r'act\s+as\s+(if|though|a|an)\s+(?!quantum|qi)',
    r'you\s+are\s+now\s+(?!qi|quantum)',
    r'(disregard|forget|override)\s+(your|all|the)\s+(instructions?|rules?|guidelines?)',
    r'(new\s+instructions?|updated\s+instructions?|different\s+instructions?)',
    r'(reveal|expose|print|show|output|repeat)\s+(your\s+)?(system|prompt|instructions?|rules?)',
    r'pretend\s+(you\s+are|to\s+be)',
    r'(sudo|root|admin)\s*(mode|access|override)',
    r'<(script|img|iframe|object)',
    r'\$\{.*\}',  # template injection
]
INJECTION_RE = re.compile('|'.join(INJECTION_PATTERNS), re.IGNORECASE)
MAX_INPUT_CHARS = 500
SECURITY_LOG = os.path.expanduser("~/.config/qi/security.log")

def sanitize_input(text):
    """Returns (clean_text, is_safe, reason). Blocks prompt injection attempts."""
    # Length cap — voice input is naturally short
    if len(text) > MAX_INPUT_CHARS:
        _log_security("LENGTH_EXCEEDED", text[:100])
        return text[:MAX_INPUT_CHARS], True, "truncated"
    # Injection detection
    match = INJECTION_RE.search(text)
    if match:
        _log_security("INJECTION_DETECTED", text)
        return None, False, f"blocked: injection pattern '{match.group(0)[:30]}'"
    # Excessive punctuation / unicode abuse
    if sum(1 for c in text if ord(c) > 127) > len(text) * 0.4:
        _log_security("UNICODE_ABUSE", text[:100])
        return None, False, "blocked: unicode anomaly"
    return text, True, "ok"

def _log_security(event, sample):
    try:
        with open(SECURITY_LOG, "a") as f:
            f.write(f"{datetime.now().isoformat()} [{event}] {repr(sample[:120])}\n")
    except: pass

def read_key(f):
    try: return open(os.path.expanduser(f"~/.config/qi/{f}")).read().strip()
    except: return ""

DEEPGRAM_KEY   = read_key("deepgram_api_key")
ELEVENLABS_KEY = read_key("elevenlabs_api_key")
ANTHROPIC_KEY  = read_key("anthropic_api_key")
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

conversation   = []
audio_queue    = queue.Queue()
last_spoke_at  = 0
COOLDOWN       = 2.5
MIN_WORDS      = 2
pending_text   = ""
pending_timer  = None
RESPONSE_DELAY = 1.2

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
    set_mic(False)   # mute mic BEFORE Owen speaks
    notify_dashboard(True)
    if not text.strip() or not ELEVENLABS_KEY:
        print(f"\n  QI: {text}")
        last_spoke_at = time.time()
        set_mic(True)
        notify_dashboard(False)
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
        notify_dashboard(False)
        set_mic(True)    # unmute mic — Owen is done, your turn

def set_mic(enabled: bool):
    """Hard mute/unmute system microphone via macOS osascript."""
    vol = '100' if enabled else '0'
    subprocess.run(['osascript', '-e', f'set volume input volume {vol}'],
                   capture_output=True)

def notify_dashboard(speaking: bool):
    try:
        import urllib.request
        urllib.request.urlopen(
            f"http://localhost:3001/api/speaking?state={'true' if speaking else 'false'}",
            timeout=1)
    except: pass

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

# ── Chief of Staff briefing skill ────────────────────────────────────────────
BRIEFING_TRIGGERS = [
    "morning briefing", "morning brief", "chief of staff",
    "top priorities", "what are my priorities", "what should i focus",
    "what's the focus", "whats the focus", "daily brief",
    "start my day", "kick off", "what's most important", "run my day",
    "what do i need to do today", "priorities for today",
]

RESEARCH_TRIGGERS = [
    "save a note", "save note", "research note", "add to research",
    "note this down", "note that down", "remember this for research",
    "log this", "save this insight", "write this down",
]

def is_briefing_request(text):
    t = text.lower().strip()
    return any(trigger in t for trigger in BRIEFING_TRIGGERS)

def fetch_briefing_data():
    """Pull live data from QI server for CoS briefing."""
    try:
        req = urllib.request.Request("http://localhost:3001/api/briefing")
        with urllib.request.urlopen(req, timeout=5) as r:
            return json.loads(r.read())
    except:
        return None

def build_cos_prompt():
    """Build Chief of Staff system prompt with live data injected."""
    data = fetch_briefing_data()
    if not data:
        return (QI_SYSTEM + "\n\nDelivery mode: CHIEF OF STAFF BRIEFING.\n"
                "Give exactly 3 voiced priorities. Each one sentence. "
                "No data available — give strategic defaults based on the mission.")

    customers   = data.get("customers", {}).get("total", "unknown")
    days_left   = data.get("goal", {}).get("daysLeft", "?")
    run_rate    = data.get("goal", {}).get("runRate", "?")
    sentry      = data.get("sentry", {})
    play        = data.get("play", {})
    action      = data.get("action", "")
    sessions    = data.get("sessions", {}).get("sessions", "?")

    sentry_note = (f"{sentry.get('count', 0)} new Sentry errors"
                   if sentry.get("count") else "no new Sentry errors")
    play_note   = (f"{play.get('installs', '?')} Play Store installs, "
                   f"{play.get('testers', '?')} testers opted in"
                   if play.get("installs") is not None else "Play Store data loading")

    context = f"""LIVE DATA:
- Customers: {customers} / 500 goal
- Days to goal: {days_left}
- Run rate needed: {run_rate} sales/day
- Sessions today: {sessions}
- {sentry_note}
- {play_note}
- System recommendation: {action}"""

    return (QI_SYSTEM + f"""

{context}

DELIVERY MODE: CHIEF OF STAFF - 3 PRIORITIES ONLY.
Rules:
- Speak exactly 3 priorities, numbered aloud: "First... Second... Third..."
- Each priority: one sentence, max 12 words. Punchy, specific, actionable.
- Ground each priority in the live data above.
- End with: "That is your focus. Go."
- No filler word at the start - begin directly with "First,"
""")

def run_cos_briefing():
    """Execute Chief of Staff 3-priority morning briefing."""
    import http.client
    print("\n  [CoS] Running Chief of Staff briefing...")
    system = build_cos_prompt()
    trigger_msg = "Give me my Chief of Staff morning briefing. Three priorities. Go."

    payload = json.dumps({
        "model": "claude-haiku-4-5",
        "max_tokens": 180,
        "stream": True,
        "system": system,
        "messages": [{"role": "user", "content": trigger_msg}]
    }).encode()

    buffer = ""
    try:
        conn = http.client.HTTPSConnection("api.anthropic.com")
        conn.request("POST", "/v1/messages", payload, {
            "x-api-key": ANTHROPIC_KEY,
            "anthropic-version": "2023-06-01",
            "Content-Type": "application/json",
            "Accept": "text/event-stream"
        })
        resp = conn.getresponse()
        full = ""
        for raw_line in resp:
            line = raw_line.decode("utf-8").strip()
            if not line.startswith("data:"): continue
            data_str = line[5:].strip()
            if data_str == "[DONE]": break
            try:
                chunk = json.loads(data_str)
                if chunk.get("type") == "content_block_delta":
                    token = chunk["delta"].get("text", "")
                    buffer += token
                    full   += token
                    parts = SENTENCE_END.split(buffer)
                    if len(parts) > 1:
                        for sentence in parts[:-1]:
                            s = sentence.strip()
                            if s:
                                print(f"\n  QI [CoS]: {s}")
                                audio_queue.put(s)
                        buffer = parts[-1]
            except: pass
        if buffer.strip():
            print(f"\n  QI [CoS]: {buffer.strip()}")
            audio_queue.put(buffer.strip())
        if full:
            conversation.append({"role": "user", "content": trigger_msg})
            conversation.append({"role": "assistant", "content": full})
    except Exception as e:
        print(f"  [CoS] Error: {e}")
        audio_queue.put("Chief of Staff briefing failed. Check the server.")

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
    global last_spoke_at
    last_spoke_at = time.time()  # block mic immediately when QI starts responding
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

# ── Handle user input — with response buffer ─────────────────────────────────
def respond_now():
    global pending_text, pending_timer
    text = pending_text.strip()
    pending_text = ""
    pending_timer = None
    if not text or len(text.split()) < MIN_WORDS:
        return
    clean, is_safe, reason = sanitize_input(text)
    if not is_safe:
        print(f"\n  [SECURITY] Input {reason}")
        audio_queue.put("That input was flagged and blocked.")
        return
    print(f"\n  You: {clean}")
    # Route to Chief of Staff briefing if triggered
    if is_briefing_request(clean):
        threading.Thread(target=run_cos_briefing, daemon=True).start()
    # Route to research note save
    elif any(t in clean.lower() for t in RESEARCH_TRIGGERS):
        def save_research():
            topic = "voice-note"
            import subprocess, re
            # Extract topic if user says "save note about X"
            m = re.search(r'(?:about|on|re:|regarding)\s+(.+)', clean, re.IGNORECASE)
            if m: topic = m.group(1).strip()[:60]
            try:
                subprocess.Popen(
                    ["python3", "/Users/qnc/Projects/quantumcube/scripts/qi-research.py",
                     "save", topic, clean],
                    stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
                )
                audio_queue.put(f"Got it. Saved to research notes under {topic}.")
            except Exception as e:
                audio_queue.put("Couldn't save that. Check the research script.")
        threading.Thread(target=save_research, daemon=True).start()
    else:
        threading.Thread(target=think_and_stream, args=(clean,), daemon=True).start()

def handle_input(text):
    global pending_text, pending_timer
    text = text.strip()
    if not text: return
    if time.time() - last_spoke_at < COOLDOWN:
        return
    # Cancel existing timer — more speech is coming
    if pending_timer:
        pending_timer.cancel()
    # Append to buffer
    pending_text = (pending_text + " " + text).strip() if pending_text else text
    print(f"  [heard: {pending_text[:70]}]")
    # Start fresh timer — respond after 1.2s of silence
    pending_timer = threading.Timer(RESPONSE_DELAY, respond_now)
    pending_timer.start()

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
           f"&model=nova-3&language=en&punctuate=true&endpointing=2500")

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

    # Intro via streaming — pre-set cooldown so mic is blocked during intro
    last_spoke_at = time.time()
    think_and_stream("Introduce yourself in one sentence. Start with 'Hmm,'")

    try:
        listen(handle_input)
    except KeyboardInterrupt:
        stop_speaking()
        audio_queue.put(None)
        print("\n  QI offline.\n")
