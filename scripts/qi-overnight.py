#!/usr/bin/env python3
"""
QI Overnight Tasks — runs at 2am via cron
Pulls data, checks health, prepares morning briefing file.
Cron: 0 2 * * * /Users/qnc/Projects/quantumcube/scripts/qi-overnight.py
"""
import os, sys, json, datetime, urllib.request

def read_key(f):
    try: return open(os.path.expanduser(f"~/.config/qi/{f}")).read().strip()
    except: return ""

SUPABASE_KEY = read_key("supabase_service_role")
POSTHOG_KEY  = read_key("posthog_api_key")
SENTRY_TOKEN = read_key("sentry_auth_token")
REPORT_FILE  = "/tmp/qi-overnight-report.json"

def log(msg):
    print(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] {msg}")

def get(url, headers={}):
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=10) as r:
            return json.loads(r.read())
    except Exception as e:
        return {"error": str(e)}

def check_supabase():
    log("Checking Supabase...")
    if not SUPABASE_KEY:
        return {"status": "no_key"}
    rows = get("https://auth.quantumcube.app/rest/v1/profiles?select=created_at&has_paid=eq.true",
               {"apikey": SUPABASE_KEY, "Authorization": f"Bearer {SUPABASE_KEY}"})
    if isinstance(rows, list):
        today = (datetime.datetime.utcnow() - datetime.timedelta(hours=24)).isoformat() + "Z"
        return {"total": len(rows), "new_24h": sum(1 for r in rows if r.get("created_at","") >= today)}
    return {"error": str(rows)}

def check_sentry():
    log("Checking Sentry overnight errors...")
    if not SENTRY_TOKEN:
        return {"count": "no_key"}
    since = (datetime.datetime.utcnow() - datetime.timedelta(hours=8)).isoformat()
    r = get(
        f"https://sentry.io/api/0/projects/quantum-neuro-creations/javascript/issues/?query=firstSeen:>{since}&limit=10",
        {"Authorization": f"Bearer {SENTRY_TOKEN}"}
    )
    if isinstance(r, list):
        return {"count": len(r), "issues": [i["title"] for i in r[:3]]}
    return {"count": 0}

def check_posthog():
    log("Checking PostHog overnight sessions...")
    if not POSTHOG_KEY:
        return {"sessions": "no_key"}
    query = {
        "query": {
            "kind": "HogQLQuery",
            "query": """SELECT count(DISTINCT properties.$session_id) as sessions
                        FROM events
                        WHERE event = '$pageview'
                          AND properties.$current_url LIKE '%quantumcube.app/app%'
                          AND timestamp >= now() - INTERVAL 1 DAY"""
        }
    }
    body = json.dumps(query).encode()
    req = urllib.request.Request(
        "https://eu.posthog.com/api/projects/172921/query/",
        data=body,
        headers={"Authorization": f"Bearer {POSTHOG_KEY}", "Content-Type": "application/json"}
    )
    try:
        with urllib.request.urlopen(req, timeout=10) as r:
            data = json.loads(r.read())
        return {"sessions": data["results"][0][0]}
    except:
        return {"sessions": "?"}

def main():
    log("QI overnight tasks starting...")
    report = {
        "generated_at": datetime.datetime.utcnow().isoformat(),
        "date": datetime.date.today().isoformat(),
        "customers": check_supabase(),
        "sentry": check_sentry(),
        "sessions": check_posthog(),
    }

    # Write report for morning briefing to read
    with open(REPORT_FILE, "w") as f:
        json.dump(report, f, indent=2)

    log(f"Report saved to {REPORT_FILE}")
    log(f"Customers: {report['customers']}")
    log(f"Sentry: {report['sentry']}")
    log(f"Sessions: {report['sessions']}")
    log("Overnight tasks complete.")

if __name__ == "__main__":
    main()
