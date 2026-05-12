#!/usr/bin/env python3
"""
QI Voice Loop — Quantum Integrator
Listens via Deepgram → thinks via Claude → speaks via Owen (ElevenLabs)
Run: python3 scripts/qi-voice.py
Say "QI" to wake, speak your request, QI responds.
Stop: Ctrl+C
"""

import os, sys, json, time, threading, tempfile, subprocess
import urllib.request, urllib.parse

# ── State ───────────────────────────────────────────────────────────────────────
QI_SPEAKING = False  # mute mic while Owen talks

# ── Keys ──────────────────────────────────────────────────────────────────────
def read_key(f):
    try: return open(os.path.expanduser(f"~/.config/qi/{f}")).read().strip()
    except: return os.environ.get(f.upper().replace('-','_'), '')

DEEPGRAM_KEY   = read_key('deepgram_api_key')
ELEVENLABS_KEY = read_key('elevenlabs_api_key')
ANTHROPIC_KEY  = open(os.path.expanduser('~/.config/anthropic/key')).read().strip()
QI_VOICE       = 'giAoKpl5weRTCJK7uB9b'  # Owen

# ── QI system prompt ──────────────────────────────────────────────────────────
QI_SYSTEM = """You are QI — Quantum Integrator. You are the personal AI assistant for Ronnie, 
founder of Quantum Cube (quantumcube.app). You are concise, direct, and mission-focused.

Your North Star: 500 paying customers by August 15, 2026. $17 one-time payment. Currently 3 paying customers.

Key facts you always know:
- Quantum Cube is a numerology + astrology PWA, live at quantumcube.app
- Play Store closed testing in progress — 14-day clock needs 12 testers to opt in first
- Tech stack: Supabase (Postgres + Edge Functions), GitHub Pages, Dodo Payments, ElevenLabs narration
- You speak through Owen's voice (ElevenLabs)

Rules:
- Keep responses under 3 sentences for voice — you are being spoken aloud
- Always tie recommendations back to the 500 customer goal
- Never say "as an AI" or "I'm an AI" — you are QI
- Be direct and confident, like a trusted COO"""

conversation = [{"role": "user", "content": "QI, introduce yourself briefly."}]

# ── ElevenLabs TTS ────────────────────────────────────────────────────────────
def speak(text):
    global QI_SPEAKING
    QI_SPEAKING = True
    print(f"\n  QI: {text}\n")
    if not ELEVENLABS_KEY:
        QI_SPEAKING = False; print("  [no ElevenLabs key]"); return
    try:
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
        f.write(audio); f.close()
        subprocess.run(['afplay', f.name], check=True)
        os.unlink(f.name)
    except Exception as e:
        print(f"  [speak error: {e}]")
    finally:
        QI_SPEAKING = False

# ── Claude API ────────────────────────────────────────────────────────────────
def think(user_input):
    conversation.append({"role": "user", "content": user_input})
    payload = json.dumps({
        "model": "claude-sonnet-4-20250514",
        "max_tokens": 200,
        "system": QI_SYSTEM,
        "messages": conversation[-10:]  # keep last 10 turns
    }).encode()
    req = urllib.request.Request(
        "https://api.anthropic.com/v1/messages",
        data=payload,
        headers={
            "x-api-key": ANTHROPIC_KEY,
            "anthropic-version": "2023-06-01",
            "Content-Type": "application/json"
        }
    )
    with urllib.request.urlopen(req, timeout=30) as r:
        result = json.loads(r.read())
    reply = result['content'][0]['text']
    conversation.append({"role": "assistant", "content": reply})
    return reply

# ── Deepgram live transcription ───────────────────────────────────────────────
def listen_and_transcribe(callback):
    """Stream mic audio to Deepgram, call callback(text) on each utterance."""
    if not DEEPGRAM_KEY:
        print("  [no Deepgram key — using keyboard fallback]")
        return keyboard_fallback(callback)

    try:
        import websocket
        import pyaudio
    except ImportError:
        print("  Installing audio deps...")
        subprocess.run(['/opt/homebrew/opt/python@3.12/libexec/bin/pip3', 'install',
                        'websocket-client', 'pyaudio', '--break-system-packages', '-q'])
        import websocket, pyaudio

    CHUNK  = 8000
    FORMAT = pyaudio.paInt16
    CHANS  = 1
    RATE   = 16000

    pa    = pyaudio.PyAudio()
    stream = pa.open(format=FORMAT, channels=CHANS, rate=RATE,
                     input=True, frames_per_buffer=CHUNK)

    dg_url = (f"wss://api.deepgram.com/v1/listen"
              f"?encoding=linear16&sample_rate={RATE}&channels={CHANS}"
              f"&model=nova-3&language=en&punctuate=true&endpointing=800")

    def on_message(ws, msg):
        d = json.loads(msg)
        try:
            t = d['channel']['alternatives'][0]['transcript']
            if t.strip() and d.get('is_final') and not QI_SPEAKING:
                print(f"\n  You: {t}")
                callback(t)
        except: pass

    def on_error(ws, err): print(f"  [WS error: {err}]")
    def on_close(ws, *a):  print("  [Deepgram closed]")
    def on_open(ws):
        print("  QI is listening... (speak naturally, Ctrl+C to stop)\n")
        def send_audio():
            while ws.sock and ws.sock.connected:
                data = stream.read(CHUNK, exception_on_overflow=False)
                ws.send(data, websocket.ABNF.OPCODE_BINARY)
        threading.Thread(target=send_audio, daemon=True).start()

    ws = websocket.WebSocketApp(
        dg_url,
        header=[f"Authorization: Token {DEEPGRAM_KEY}"],
        on_open=on_open, on_message=on_message,
        on_error=on_error, on_close=on_close
    )
    ws.run_forever()
    stream.stop_stream(); stream.close(); pa.terminate()

def keyboard_fallback(callback):
    """Text input fallback when no Deepgram key."""
    print("  [Keyboard mode — type your message, Enter to send, 'quit' to exit]\n")
    while True:
        try:
            text = input("  You: ").strip()
            if text.lower() in ('quit', 'exit', 'bye'): break
            if text: callback(text)
        except (EOFError, KeyboardInterrupt): break

# ── Main ──────────────────────────────────────────────────────────────────────
def handle_input(text):
    if not text.strip(): return
    reply = think(text)
    speak(reply)

if __name__ == '__main__':
    print("\n" + "─"*50)
    print("  QI — QUANTUM INTEGRATOR")
    print("  Owen voice · Deepgram ears · Claude mind")
    print("─"*50 + "\n")

    # Intro
    intro = think("QI, introduce yourself briefly.")
    speak(intro)

    # Start listening
    try:
        listen_and_transcribe(handle_input)
    except KeyboardInterrupt:
        speak("Going offline. Talk soon.")
        print("\n  QI offline.\n")
