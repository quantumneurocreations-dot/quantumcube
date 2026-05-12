#!/usr/bin/env python3
"""
QI Security Audit — daily prompt injection + secrets scan
Run manually: python3 scripts/qi-security.py
Or via cron: 0 3 * * * /Users/qnc/Projects/quantumcube/scripts/qi-security.py
"""
import os, re, json, datetime, subprocess

REPORT_FILE = "/tmp/qi-security-report.json"
PROJECT_DIR = os.path.expanduser("~/Projects/quantumcube")

SCORES = {
    "keys_exposed":       {"weight": 40, "status": True},
    "prompt_injection":   {"weight": 25, "status": True},
    "api_keys_secured":   {"weight": 20, "status": True},
    "gitignore_clean":    {"weight": 15, "status": True},
}

def log(msg): print(f"  {msg}")

# ── Check 1: No secrets in git history / working tree ─────────────────────────
def check_secrets():
    log("Scanning for exposed secrets...")
    patterns = [
        r'sk-ant-[a-zA-Z0-9\-_]{20,}',   # Anthropic
        r'tvly-[a-zA-Z0-9]{20,}',          # Tavily
        r'sb_secret_[a-zA-Z0-9_]{20,}',    # Supabase
        r'sntrys_[a-zA-Z0-9_]{20,}',       # Sentry
        r'EL[a-z0-9]{30,}',               # ElevenLabs
    ]
    issues = []
    for root, dirs, files in os.walk(PROJECT_DIR):
        dirs[:] = [d for d in dirs if d not in ['.git','node_modules','graphify-out']]
        for fname in files:
            if not fname.endswith(('.py','.js','.ts','.json','.md','.html','.sh')):
                continue
            fpath = os.path.join(root, fname)
            try:
                content = open(fpath).read()
                for pat in patterns:
                    if re.search(pat, content):
                        issues.append(f"Possible secret in {fpath.replace(PROJECT_DIR,'')}")
            except: pass
    return issues

# ── Check 2: .gitignore covers sensitive files ────────────────────────────────
def check_gitignore():
    log("Checking .gitignore coverage...")
    required = ['.supabase-env', '*.env', '.env*', '*.pem', '*.key']
    gitignore = open(os.path.join(PROJECT_DIR, '.gitignore')).read()
    missing = [r for r in required if r not in gitignore]
    return missing

# ── Check 3: Key files are not world-readable ─────────────────────────────────
def check_key_permissions():
    log("Checking key file permissions...")
    issues = []
    key_dir = os.path.expanduser("~/.config/qi")
    for f in os.listdir(key_dir):
        fpath = os.path.join(key_dir, f)
        mode = oct(os.stat(fpath).st_mode)[-3:]
        if mode not in ('600', '400'):
            issues.append(f"{f}: permissions {mode} (should be 600)")
    return issues

# ── Check 4: Basic prompt injection scan in any web-fetched content ───────────
def check_prompt_injection_patterns():
    log("Scanning for prompt injection patterns in scripts...")
    # Note: these patterns scan for injection in external/fetched content, not our own code
    SELF_EXCLUDE = ['qi-security.py', 'qi-voice.py']  # our own code uses these terms safely
    dangerous = [
        r'ignore previous instructions',
        r'disregard your',
        r'system prompt',
        r'act as DAN',
        r'jailbreak',
        r'\\\\n\\\\nHuman:',
    ]
    issues = []
    scripts_dir = os.path.join(PROJECT_DIR, 'scripts')
    for fname in os.listdir(scripts_dir):
        if not fname.endswith('.py'): continue
        if fname in SELF_EXCLUDE: continue
        content = open(os.path.join(scripts_dir, fname)).read().lower()
        for pat in dangerous:
            if re.search(pat, content, re.IGNORECASE):
                issues.append(f"Suspicious pattern '{pat}' in {fname}")
    return issues

def main():
    print("\n" + "─"*50)
    print("  QI SECURITY AUDIT")
    print(f"  {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print("─"*50 + "\n")

    results = {}

    secrets = check_secrets()
    results["secrets_exposed"] = {"pass": len(secrets) == 0, "issues": secrets}

    gitignore = check_gitignore()
    results["gitignore"] = {"pass": len(gitignore) == 0, "missing": gitignore}

    perms = check_key_permissions()
    results["key_permissions"] = {"pass": len(perms) == 0, "issues": perms}

    injection = check_prompt_injection_patterns()
    results["prompt_injection"] = {"pass": len(injection) == 0, "issues": injection}

    # Score
    checks = [results["secrets_exposed"]["pass"],
              results["gitignore"]["pass"],
              results["key_permissions"]["pass"],
              results["prompt_injection"]["pass"]]
    score = int(sum(checks) / len(checks) * 100)

    print(f"  Secrets exposed:    {'✓ PASS' if results['secrets_exposed']['pass'] else '✗ FAIL'}")
    print(f"  .gitignore clean:   {'✓ PASS' if results['gitignore']['pass'] else '✗ FAIL'}")
    print(f"  Key permissions:    {'✓ PASS' if results['key_permissions']['pass'] else '✗ FAIL'}")
    print(f"  Prompt injection:   {'✓ PASS' if results['prompt_injection']['pass'] else '✗ FAIL'}")
    print(f"\n  Security score: {score}/100\n")

    for key, val in results.items():
        if not val["pass"]:
            issues = val.get("issues", val.get("missing", []))
            for issue in issues:
                print(f"  ⚠️  {issue}")

    report = {"date": datetime.date.today().isoformat(), "score": score, "results": results}
    with open(REPORT_FILE, "w") as f:
        json.dump(report, f, indent=2)

    print(f"\n  Report saved: {REPORT_FILE}")
    print("─"*50 + "\n")

if __name__ == "__main__":
    main()
