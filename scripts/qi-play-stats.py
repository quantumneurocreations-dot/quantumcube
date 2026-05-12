#!/usr/bin/env python3
"""
QI Play Store Stats — fetches install/tester counts via Google Play Developer API
Requires: ~/.config/qi/play-service-account.json (service account JSON key)
Run: python3 scripts/qi-play-stats.py
"""
import json, os, sys, time, urllib.request, urllib.parse
from datetime import datetime, timezone

KEY_PATH = os.path.expanduser("~/.config/qi/play-service-account.json")
PACKAGE   = "app.quantumcube.twa"

def get_access_token():
    """Mint a short-lived OAuth2 bearer token from the service account key."""
    import base64, hashlib, hmac
    try:
        key_data = json.load(open(KEY_PATH))
    except FileNotFoundError:
        print("ERROR: Service account key not found at", KEY_PATH)
        sys.exit(1)

    # Build JWT for service account auth
    from urllib.request import urlopen
    now = int(time.time())
    header = base64.urlsafe_b64encode(json.dumps({"alg":"RS256","typ":"JWT"}).encode()).rstrip(b"=")
    payload = base64.urlsafe_b64encode(json.dumps({
        "iss": key_data["client_email"],
        "scope": "https://www.googleapis.com/auth/androidpublisher",
        "aud": "https://oauth2.googleapis.com/token",
        "iat": now, "exp": now + 3600
    }).encode()).rstrip(b"=")

    # Sign with RSA private key using cryptography library
    try:
        from cryptography.hazmat.primitives import hashes, serialization
        from cryptography.hazmat.primitives.asymmetric import padding
        private_key = serialization.load_pem_private_key(
            key_data["private_key"].encode(), password=None
        )
        signing_input = header + b"." + payload
        signature = private_key.sign(signing_input, padding.PKCS1v15(), hashes.SHA256())
        jwt = signing_input + b"." + base64.urlsafe_b64encode(signature).rstrip(b"=")
    except ImportError:
        print("ERROR: cryptography library needed. Run: pip3 install cryptography --break-system-packages")
        sys.exit(1)

    # Exchange JWT for access token
    body = urllib.parse.urlencode({
        "grant_type": "urn:ietf:params:oauth:grant-type:jwt-bearer",
        "assertion": jwt.decode()
    }).encode()
    req = urllib.request.Request("https://oauth2.googleapis.com/token", data=body)
    resp = json.loads(urllib.request.urlopen(req).read())
    return resp["access_token"]

def get_tester_count(token):
    """Get number of testers opted in to alpha track."""
    url = f"https://androidpublisher.googleapis.com/androidpublisher/v3/applications/{PACKAGE}/testers"
    req = urllib.request.Request(url, headers={"Authorization": f"Bearer {token}"})
    try:
        resp = json.loads(urllib.request.urlopen(req).read())
        testers = resp.get("testers", [])
        return len(testers)
    except Exception as e:
        return f"error: {e}"

def get_install_stats(token):
    """Get install count from Play Developer Reporting API."""
    # Use the installs metric set
    url = (f"https://playdeveloperreporting.googleapis.com/v1beta1/"
           f"apps/{PACKAGE}/deviceCountMetricSet:query")
    body = json.dumps({
        "dimensions": ["apiLevel"],
        "metrics": ["activeDeviceCount"],
        "dateRange": {
            "startDate": {"year": 2026, "month": 5, "day": 1},
            "endDate": {"year": 2026, "month": 5, "day": 31}
        }
    }).encode()
    req = urllib.request.Request(url, data=body,
          headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"})
    try:
        resp = json.loads(urllib.request.urlopen(req).read())
        rows = resp.get("rows", [])
        total = sum(r.get("metrics", {}).get("activeDeviceCount", {}).get("value", 0) for r in rows)
        return total
    except Exception as e:
        return f"error: {e}"

def get_play_stats():
    """Main entry — returns dict for QI briefing."""
    if not os.path.exists(KEY_PATH):
        return {"error": "service_account_not_configured", "installs": 0, "testers": 0}
    try:
        token = get_access_token()
        installs = get_install_stats(token)
        testers  = get_tester_count(token)
        return {"installs": installs, "testers": testers, "ok": True}
    except Exception as e:
        return {"error": str(e), "installs": 0, "testers": 0}

if __name__ == "__main__":
    print(json.dumps(get_play_stats(), indent=2))
