#!/usr/bin/env python3
"""
QI Morning Briefing — Quantum Cube
Pulls live data from Supabase, PostHog, and Sentry.
Run standalone: python3 scripts/morning-briefing.py
Or pipe to ElevenLabs for voice: python3 scripts/morning-briefing.py --speak
"""

import os, sys, json, urllib.request, urllib.parse, datetime

# ── Config ────────────────────────────────────────────────────────────────────
SUPABASE_URL     = "https://auth.quantumcube.app"
SUPABASE_REST    = "https://auth.quantumcube.app/rest/v1"
SUPABASE_KEY     = os.environ.get("SUPABASE_SERVICE_ROLE_KEY", "")
POSTHOG_KEY      = os.environ.get("POSTHOG_API_KEY", "")
POSTHOG_HOST     = "https://eu.posthog.com"
POSTHOG_PROJECT  = "172921"
SENTRY_TOKEN     = os.environ.get("SENTRY_AUTH_TOKEN", "")
SENTRY_ORG       = "quantum-neuro-creations"
SENTRY_PROJECT   = "javascript"
ELEVENLABS_KEY   = os.environ.get("ELEVENLABS_API_KEY", "")
ELEVENLABS_VOICE = "giAoKpl5weRTCJK7uB9b"  # Owen — QI voice  # Valory

GOAL_CUSTOMERS   = 500
GOAL_DATE        = datetime.date(2026, 8, 15)
PRICE            = 17

SPEAK = "--speak" in sys.argv

# ── Helpers ───────────────────────────────────────────────────────────────────
def get(url, headers={}):
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=10) as r:
            return json.loads(r.read())
    except Exception as e:
        return {"error": str(e)}

def post(url, data, headers={}):
    try:
        body = json.dumps(data).encode()
        headers["Content-Type"] = "application/json"
        req = urllib.request.Request(url, data=body, headers=headers, method="POST")
        with urllib.request.urlopen(req, timeout=15) as r:
            return json.loads(r.read())
    except Exception as e:
        return {"error": str(e)}

# ── Data pulls ────────────────────────────────────────────────────────────────
def get_customers():
    if not SUPABASE_KEY:
        return {"total": "?", "today": "?", "week": "?"}
    now = datetime.datetime.utcnow()
    day_ago  = (now - datetime.timedelta(hours=24)).isoformat() + "Z"
    week_ago = (now - datetime.timedelta(days=7)).isoformat() + "Z"
    url = f"{SUPABASE_REST}/profiles?select=created_at&has_paid=eq.true"
    rows = get(url, {
        "apikey": SUPABASE_KEY,
        "Authorization": f"Bearer {SUPABASE_KEY}",
        "Range": "0-9999"
    })
    if isinstance(rows, list):
        total = len(rows)
        today = sum(1 for r in rows if r.get("created_at","") >= day_ago)
        week  = sum(1 for r in rows if r.get("created_at","") >= week_ago)
        return {"total": total, "today": today, "week": week}
    return {"total": "?", "today": "?", "week": "?"}

def get_sessions():
    if not POSTHOG_KEY:
        return {"sessions": "?", "pageviews": "?"}
    query = {
        "query": {
            "kind": "HogQLQuery",
            "query": """
                SELECT count(DISTINCT properties.$session_id) as sessions,
                       count() as pageviews
                FROM events
                WHERE event = '$pageview'
                  AND properties.$current_url LIKE '%quantumcube.app/app%'
                  AND timestamp >= now() - INTERVAL 1 DAY
            """
        }
    }
    url = f"{POSTHOG_HOST}/api/projects/{POSTHOG_PROJECT}/query/"
    r = post(url, query, {"Authorization": f"Bearer {POSTHOG_KEY}"})
    try:
        row = r["results"][0]
        return {"sessions": row[0], "pageviews": row[1]}
    except:
        return {"sessions": "?", "pageviews": "?"}

def get_sentry_issues():
    if not SENTRY_TOKEN:
        return {"count": "?", "top": None}
    yesterday = (datetime.datetime.utcnow() - datetime.timedelta(hours=24)).strftime("%Y-%m-%dT%H:%M:%S")
    url = f"https://sentry.io/api/0/projects/{SENTRY_ORG}/{SENTRY_PROJECT}/issues/?query=firstSeen:>{yesterday}&limit=5"
    r = get(url, {"Authorization": f"Bearer {SENTRY_TOKEN}"})
    if isinstance(r, list):
        return {"count": len(r), "top": r[0]["title"] if r else None}
    return {"count": "?", "top": None}

# ── Briefing composer ─────────────────────────────────────────────────────────
def compose_briefing(cust, sessions, sentry):
    today      = datetime.date.today()
    days_left  = (GOAL_DATE - today).days
    total      = cust["total"]
    revenue    = f"${total * PRICE:,}" if isinstance(total, int) else "?"
    remaining  = GOAL_CUSTOMERS - total if isinstance(total, int) else "?"
    run_rate   = round(remaining / days_left, 1) if isinstance(remaining, int) and days_left > 0 else "?"

    # Sentry summary
    s_count = sentry["count"]
    s_line  = f"{s_count} new issues — {sentry['top']}" if s_count and s_count != "?" and int(str(s_count)) > 0 else "all clear"

    # One action logic
    if isinstance(total, int) and total < 12:
        # Placeholder — real tester count comes from Play Console
        action = f"Chase tester opt-ins — this is the only thing that starts the 14-day clock."
    elif isinstance(s_count, int) and s_count > 0:
        action = f"Fix Sentry issue: {sentry['top']}"
    elif isinstance(sessions['sessions'], int) and isinstance(total, int):
        conv = round(total / max(sessions['sessions'], 1) * 100, 1) if sessions['sessions'] else "?"
        if isinstance(conv, float) and conv < 5:
            action = f"Funnel needs work — {sessions['sessions']} sessions but conversion is low. Check the paywall flow."
        else:
            action = "Everything looks healthy. Run one paid ad test today."
    else:
        action = "Pull your Play Store tester count and chase anyone who hasn't opted in yet."

    briefing = f"""
QI MORNING BRIEFING — {today.strftime('%A, %B %-d')}

Revenue:     {revenue} total  ·  {total} paying customers  ·  {cust['today']} new today  ·  {cust['week']} this week
Goal:        {total} of {GOAL_CUSTOMERS}  ·  {days_left} days to August 15  ·  need {run_rate}/day to hit target
Sessions:    {sessions['sessions']} unique sessions on /app yesterday
Errors:      {s_line}

TODAY'S ONE ACTION:
{action}
""".strip()
    return briefing

# ── Optional: speak via ElevenLabs ───────────────────────────────────────────
def speak(text):
    if not ELEVENLABS_KEY:
        print("[speak] ELEVENLABS_API_KEY not set — skipping voice output")
        return
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{ELEVENLABS_VOICE}"
    payload = {
        "text": text,
        "model_id": "eleven_turbo_v2_5",
        "voice_settings": {"stability": 0.5, "similarity_boost": 0.75, "speed": 1.0}
    }
    headers = {"xi-api-key": ELEVENLABS_KEY}
    req = urllib.request.Request(url, data=json.dumps(payload).encode(),
                                  headers={**headers, "Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            audio = r.read()
        out = "/tmp/qi-briefing.mp3"
        with open(out, "wb") as f:
            f.write(audio)
        os.system(f"afplay {out}")  # macOS
        print(f"[speak] played {out}")
    except Exception as e:
        print(f"[speak] error: {e}")

# ── Main ──────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("QI: pulling briefing data...")
    cust     = get_customers()
    sessions = get_sessions()
    sentry   = get_sentry_issues()
    briefing = compose_briefing(cust, sessions, sentry)
    print("\n" + "─" * 60)
    print(briefing)
    print("─" * 60 + "\n")
    if SPEAK:
        speak(briefing)
