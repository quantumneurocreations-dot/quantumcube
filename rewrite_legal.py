#!/usr/bin/env python3
"""
rewrite_legal.py
Replace the Privacy Policy, POPIA & Data, and Security sections of
quantum-cube-v10.html with the v2 (Supabase-era) versions.
"""

from __future__ import annotations

import argparse
import datetime as dt
import re
import shutil
import sys
from pathlib import Path

FILE = Path("/Users/qnc/Projects/quantumcube/quantum-cube-v10.html")

PRIVACY_NEW = """<!-- PRIVACY POLICY -->
    <div class="legal-doc active" id="doc-privacy">
      <div class="legal-h1">Privacy Policy</div>
      <span class="legal-updated">Effective date: 17 April 2026 &nbsp;&#183;&nbsp; Quantum Neuro Creations</span>
      <div class="legal-highlight"><p class="legal-p">When you complete a Quantum Cube reading, we do not store your name or birth date. Calculations happen instantly from the inputs you provide and nothing is saved. If you create an account, we store only your email address, your unlock status, and your marketing preference.</p></div>
      <div class="legal-h2">1. Who We Are</div>
      <p class="legal-p">Quantum Cube is a product of <strong>Quantum Neuro Creations</strong>, a South African business. This Privacy Policy explains how we handle information when you use the app.</p>
      <div class="legal-h2">2. Information We Collect</div>
      <p class="legal-p"><strong>Reading inputs (not stored):</strong> When you enter your name and date of birth to generate a reading, these inputs are used to calculate your numerology, Western astrology, and Chinese zodiac results. We do not save them. Every time you open the app, your results are generated fresh from the inputs you provide.</p>
      <p class="legal-p"><strong>Account data (stored):</strong> If you choose to create an account, we store your email address, your purchase status, whether you have opted in to marketing emails, and the date your account was created. That is all.</p>
      <p class="legal-p"><strong>Payment information:</strong> Your payment is processed by PayFast (Pty) Ltd, a registered South African payment service provider. We do not receive, see, or store your card number, banking details, or any payment credentials. PayFast&rsquo;s Privacy Policy governs how your payment data is handled.</p>
      <div class="legal-h2">3. Information We Do Not Collect</div>
      <p class="legal-p">We do not collect or store your reading history, your device identifiers, your location, your browsing history outside the app, or any behavioural tracking data. We do not sell your data, share it with advertisers, or build profiles on you.</p>
      <div class="legal-h2">4. How We Use Your Email</div>
      <p class="legal-p">We use your email only for: (a) sending the magic link that signs you in &mdash; we do not use passwords; (b) contacting you about your purchase or your account; and (c) product updates, if and only if you opted in on sign-up. The marketing checkbox is unchecked by default. You can withdraw consent any time from a link in any marketing email or by writing to privacy@qncacademy.com.</p>
      <div class="legal-h2">5. Where Your Data Is Stored</div>
      <p class="legal-p">Account data is stored in Frankfurt, Germany on infrastructure operated by Supabase Inc., our database provider. Your data is encrypted in transit and at rest. We chose the European Union for storage because it provides a strong data protection framework recognised under POPIA.</p>
      <div class="legal-h2">6. How Long We Keep Your Data</div>
      <p class="legal-p">If you delete your account or ask us to remove your data, we erase your account record from our database within 30 days. Email privacy@qncacademy.com to request deletion.</p>
      <div class="legal-h2">7. Third-Party Services</div>
      <p class="legal-p"><strong>Supabase:</strong> Database and authentication provider. Frankfurt region. Supabase&rsquo;s Privacy Policy applies to data stored on their infrastructure.</p>
      <p class="legal-p"><strong>PayFast:</strong> Payment processing only. Governed by PayFast&rsquo;s own Privacy Policy and PCI DSS Level 1 certification.</p>
      <p class="legal-p"><strong>Cloudflare:</strong> Our traffic is served through Cloudflare, which provides content delivery, TLS, and denial-of-service protection. Cloudflare&rsquo;s Privacy Policy applies to this routing.</p>
      <p class="legal-p"><strong>Google Fonts:</strong> The app loads fonts from Google Fonts. Google&rsquo;s Privacy Policy applies to the font request.</p>
      <div class="legal-h2">8. Children</div>
      <p class="legal-p">Quantum Cube is not intended for users under the age of 18. We do not knowingly collect information from minors. If you are a parent or guardian and believe a minor has provided us their information, email privacy@qncacademy.com and we will delete it.</p>
      <div class="legal-h2">9. Your Rights</div>
      <p class="legal-p">You have the right to access the data we hold about you, correct inaccurate information, request deletion, withdraw marketing consent, object to how we process your data, and complain to a data protection authority. Email privacy@qncacademy.com to exercise any of these rights. We respond within 30 days.</p>
      <div class="legal-h2">10. Cookies</div>
      <p class="legal-p">Quantum Cube uses a single authentication cookie to keep you signed in. We use no tracking cookies, no advertising cookies, and no third-party analytics cookies.</p>
      <div class="legal-h2">11. Changes to This Policy</div>
      <p class="legal-p">We may update this Privacy Policy. The effective date at the top reflects the most recent revision. If a change is significant, we will notify account holders at their registered email address before it takes effect.</p>
      <div class="legal-h2">12. Contact</div>
      <p class="legal-p">For privacy enquiries, contact our Information Officer at <strong>privacy@qncacademy.com</strong>.</p>
    </div>
"""

POPIA_NEW = """<!-- POPIA & DATA -->
    <div class="legal-doc" id="doc-popia">
      <div class="legal-h1">POPIA &amp; Data Compliance</div>
      <span class="legal-updated">Effective date: 17 April 2026 &nbsp;&#183;&nbsp; Quantum Neuro Creations</span>
      <div class="legal-highlight"><p class="legal-p">Quantum Neuro Creations is a South African business and complies with the Protection of Personal Information Act 4 of 2013 (POPIA). Where users are located in the European Economic Area, we also comply with the EU General Data Protection Regulation (GDPR).</p></div>
      <div class="legal-h2">Information Officer</div>
      <p class="legal-p">Under POPIA, every responsible party must designate an Information Officer. The designated Information Officer for Quantum Neuro Creations is reachable at <strong>privacy@qncacademy.com</strong>. All POPIA enquiries, access requests, and deletion requests should be directed to this address.</p>
      <div class="legal-h2">What POPIA Calls &ldquo;Personal Information&rdquo;</div>
      <p class="legal-p">Personal information includes your name, date of birth, email address, and any other data that can identify you as an individual. The email address you provide on sign-up is the only piece of identifying information we hold on our systems.</p>
      <div class="legal-h2">Lawful Basis for Processing</div>
      <p class="legal-p">We process your account data on the basis of the contract between us &mdash; providing the Quantum Cube service you signed up for. Marketing emails are sent only on the basis of your specific, affirmative, opt-in consent.</p>
      <div class="legal-h2">How We Protect the POPIA Conditions</div>
      <p class="legal-p"><strong>Accountability:</strong> Our Information Officer is responsible for compliance and responds to data subject requests within 30 days.</p>
      <p class="legal-p"><strong>Processing limitation:</strong> We process only what is necessary to provide the service. We use your email to sign you in and to contact you about your account; we use your unlock status to remember what you have purchased.</p>
      <p class="legal-p"><strong>Purpose specification:</strong> Your data is used only for the purposes described in our Privacy Policy.</p>
      <p class="legal-p"><strong>Further processing limitation:</strong> We do not repurpose your data for analytics, profiling, advertising, or resale.</p>
      <p class="legal-p"><strong>Information quality:</strong> You can update your email address and marketing preference at any time from within the app or by emailing privacy@qncacademy.com.</p>
      <p class="legal-p"><strong>Openness:</strong> Our data handling is documented in this Privacy Policy and POPIA notice.</p>
      <p class="legal-p"><strong>Security safeguards:</strong> See our separate Security tab for technical details.</p>
      <p class="legal-p"><strong>Data subject participation:</strong> You may access, correct, or delete your data at any time.</p>
      <div class="legal-h2">Cross-Border Transfer</div>
      <p class="legal-p">Your account data is stored in Frankfurt, Germany, on infrastructure operated by Supabase Inc. Section 72 of POPIA permits transfers to a jurisdiction that provides an adequate level of data protection. The European Union&rsquo;s GDPR is widely regarded as providing that standard.</p>
      <div class="legal-h2">PayFast and POPIA</div>
      <p class="legal-p">When you make a payment, PayFast processes your payment information as a registered operator under POPIA and PCI DSS. PayFast maintains its own POPIA compliance programme. Quantum Neuro Creations receives only a payment confirmation &mdash; no card or banking details.</p>
      <div class="legal-h2">Your POPIA Rights</div>
      <p class="legal-p">Under POPIA you have the right to: know what personal information is held about you; request a copy of that information; request correction of inaccurate information; request deletion of your information; object to direct marketing; object to processing; and lodge a complaint with the Information Regulator.</p>
      <p class="legal-p">To exercise any of these rights, email <strong>privacy@qncacademy.com</strong>. We respond within 30 days.</p>
      <div class="legal-h2">Information Regulator</div>
      <p class="legal-p">The Information Regulator of South Africa can be contacted at <strong>inforegulator.org.za</strong>, by email at enquiries@inforegulator.org.za, or on 010 023 5207.</p>
      <div class="legal-h2">Data Breach Notification</div>
      <p class="legal-p">If we become aware of a breach that compromises your personal information, we will notify you and the Information Regulator within 72 hours of becoming aware of it, as required by POPIA and GDPR.</p>
    </div>
"""

SECURITY_NEW = """<!-- SECURITY -->
    <div class="legal-doc" id="doc-security">
      <div class="legal-h1">Security</div>
      <span class="legal-updated">Effective date: 17 April 2026 &nbsp;&#183;&nbsp; Quantum Neuro Creations</span>
      <div class="legal-highlight"><p class="legal-p">We take reasonable technical and organisational steps to protect your data. Because readings are generated without being stored and the only personal data we keep is your email address, the attack surface on user data is deliberately small.</p></div>
      <div class="legal-h2">In Transit</div>
      <p class="legal-p">All traffic between your device and our servers is encrypted using TLS 1.2 or higher. Our domains are served through Cloudflare, which provides content delivery, TLS termination, and protection against denial-of-service attacks.</p>
      <div class="legal-h2">At Rest</div>
      <p class="legal-p">Account data is stored in Supabase&rsquo;s managed Postgres database, encrypted at rest. Supabase maintains SOC 2 Type II certification and publishes the results of third-party audits.</p>
      <div class="legal-h2">Authentication</div>
      <p class="legal-p">We use magic-link authentication. You sign in by clicking a one-time link sent to your email. No password is stored on our servers or yours. If your email is compromised, the attacker would gain access to your Quantum Cube account &mdash; which holds only your email, your unlock status, and your marketing preference &mdash; and you should change your email password and contact us at privacy@qncacademy.com immediately.</p>
      <div class="legal-h2">No Readings History</div>
      <p class="legal-p">We do not store your reading results. Calculations are deterministic &mdash; the same inputs always produce the same output &mdash; so there is no need to keep a history, and we do not. Nothing about your character analysis is held by us.</p>
      <div class="legal-h2">Access Controls</div>
      <p class="legal-p">Only members of the Quantum Neuro Creations team have administrative access to our production database. All administrative access passes through the Supabase dashboard and Google Workspace, both of which support and require strong account security controls.</p>
      <div class="legal-h2">Payment Data</div>
      <p class="legal-p">We never see, process, or store your payment card details. Payments are handled by PayFast, which holds PCI DSS Level 1 certification. Your card details are entered directly on PayFast&rsquo;s secure pages and never pass through Quantum Cube&rsquo;s code.</p>
      <div class="legal-h2">Incident Response</div>
      <p class="legal-p">If we become aware of a security incident that affects your personal information, we will notify you and the Information Regulator within 72 hours, as required by POPIA and GDPR.</p>
      <div class="legal-h2">What We Cannot Protect Against</div>
      <p class="legal-p">No system is perfectly secure. We cannot protect against malware on your own device that intercepts what you type, nor against someone with physical access to your unlocked device. Standard device hygiene &mdash; keeping your device updated, using a screen lock, installing apps only from trusted sources, and using a strong unique password on the email account tied to Quantum Cube &mdash; is essential.</p>
      <div class="legal-h2">Responsible Disclosure</div>
      <p class="legal-p">If you discover a security vulnerability in Quantum Cube, please report it responsibly to <strong>privacy@qncacademy.com</strong> before public disclosure, giving us reasonable opportunity to address it. We take all reports seriously and respond promptly.</p>
      <div class="legal-h2">Updates</div>
      <p class="legal-p">Security improvements are delivered through app updates. Keep Quantum Cube up to date for the latest protections.</p>
    </div>
"""

PRIVACY_RE  = re.compile(
    r"<!-- PRIVACY POLICY -->.*?</div>\s*(?=\n\s*<!-- TERMS OF USE -->)",
    re.DOTALL,
)
POPIA_RE    = re.compile(
    r"<!-- POPIA & DATA -->.*?</div>\s*(?=\n\s*<!-- SECURITY -->)",
    re.DOTALL,
)
SECURITY_RE = re.compile(
    r"<!-- SECURITY -->.*?</div>\s*(?=\n\s*</div><!-- /legalBody -->)",
    re.DOTALL,
)

RUNCALC_MARKER = "function runCalculation"


def die(msg, code=1):
    print(f"ERROR: {msg}", file=sys.stderr)
    sys.exit(code)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--file", default=str(FILE))
    args = ap.parse_args()

    src = Path(args.file)
    if not src.exists():
        die(f"File not found: {src}")

    text = src.read_text(encoding="utf-8")

    if RUNCALC_MARKER not in text:
        die(f"'{RUNCALC_MARKER}' not found in {src} -- aborting.")
    pre_linenum = text[: text.index(RUNCALC_MARKER)].count("\n") + 1
    print(f"Pre-check OK: '{RUNCALC_MARKER}' at line {pre_linenum}")

    def replace_one(label, pattern, new, body):
        matches = pattern.findall(body)
        if len(matches) == 0:
            die(f"{label}: anchor pattern matched 0 times -- aborting.")
        if len(matches) > 1:
            die(f"{label}: anchor pattern matched {len(matches)} times -- aborting.")
        return pattern.sub(new.rstrip() + "\n", body, count=1)

    text = replace_one("Privacy",  PRIVACY_RE,  PRIVACY_NEW,  text)
    text = replace_one("POPIA",    POPIA_RE,    POPIA_NEW,    text)
    text = replace_one("Security", SECURITY_RE, SECURITY_NEW, text)

    if RUNCALC_MARKER not in text:
        die(f"'{RUNCALC_MARKER}' missing after replacement -- aborting (not writing).")
    post_linenum = text[: text.index(RUNCALC_MARKER)].count("\n") + 1
    print(f"Post-check OK: '{RUNCALC_MARKER}' at line {post_linenum}")

    if args.dry_run:
        print("DRY-RUN complete. No files written.")
        print(f"  runCalculation shift: {pre_linenum} -> {post_linenum}")
        return

    stamp = dt.datetime.now().strftime("%Y%m%d-%H%M%S")
    bak = src.with_suffix(src.suffix + f".bak-{stamp}")
    shutil.copy2(src, bak)
    print(f"Backup written: {bak}")

    src.write_text(text, encoding="utf-8")
    print(f"Wrote: {src}")
    print(f"  runCalculation shift: {pre_linenum} -> {post_linenum}")


if __name__ == "__main__":
    main()
