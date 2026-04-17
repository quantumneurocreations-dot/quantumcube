#!/usr/bin/env python3
"""
rewrite_terms.py
Replace the Terms of Use section of quantum-cube-v10.html with the
Supabase/account-era version. Follows same safety pattern as rewrite_legal.py.
"""

from __future__ import annotations

import argparse
import datetime as dt
import re
import shutil
import sys
from pathlib import Path

FILE = Path("/Users/qnc/Projects/quantumcube/quantum-cube-v10.html")

TERMS_NEW = """<!-- TERMS OF USE -->
    <div class="legal-doc" id="doc-terms">
      <div class="legal-h1">Terms of Use</div>
      <span class="legal-updated">Effective date: 17 April 2026 &nbsp;&#183;&nbsp; Quantum Neuro Creations</span>
      <p class="legal-p">Please read these Terms of Use carefully before using Quantum Cube. By creating an account or continuing to use the app, you agree to be bound by these Terms.</p>
      <div class="legal-h2">1. The Service</div>
      <p class="legal-p">Quantum Cube generates numerology, Western astrology, and Chinese zodiac readings from the name and date of birth you enter. The app is offered for entertainment and personal self-reflection purposes only. It is not a substitute for professional advice of any kind.</p>
      <div class="legal-h2">2. Your Account</div>
      <p class="legal-p">To unlock the full reading you create an account using your email address. We use passwordless magic-link authentication &mdash; we send a one-time sign-in link to your email, and we do not store any password.</p>
      <p class="legal-p">You are responsible for keeping your email account secure. If your email is compromised, the attacker could gain access to your Quantum Cube account. Contact us at privacy@qncacademy.com if you suspect unauthorised access.</p>
      <div class="legal-h2">3. Licence</div>
      <p class="legal-p">Quantum Neuro Creations grants you a personal, non-exclusive, non-transferable, revocable licence to use Quantum Cube for your own personal, non-commercial purposes. You may not copy, distribute, modify, reverse engineer, or create derivative works based on the app or its content.</p>
      <div class="legal-h2">4. Payment and Unlock</div>
      <p class="legal-p">The full profile unlock is available for a once-off payment of $8.00 (USD), processed by PayFast. Once your payment is confirmed, your unlock is tied to your account. You can sign in from any device with your email address and your unlock will be available.</p>
      <div class="legal-h2">5. Cooling-off Waiver and Refunds</div>
      <p class="legal-p">Your unlock gives you immediate digital access to the complete reading. By clicking Unlock and completing payment, you confirm that you want the content delivered immediately and you expressly waive any statutory cooling-off right that would otherwise apply to digital content (including under the South African Consumer Protection Act and equivalent EU consumer-law provisions).</p>
      <p class="legal-p"><strong>Refund policy:</strong> Because the content is digital and immediately delivered, all sales are final. No refunds will be issued once the unlock has been activated. If you experience a technical issue that prevents access to your purchased content, email privacy@qncacademy.com and we will resolve the issue or provide equivalent access at no charge.</p>
      <div class="legal-h2">6. Account Deletion</div>
      <p class="legal-p">You can request deletion of your account at any time by emailing privacy@qncacademy.com. When we delete your account, all data associated with it &mdash; including your unlock status &mdash; is permanently removed within 30 days. Deleting your account also ends your access to the paid content; please make sure you have finished reading any part you want to revisit before requesting deletion.</p>
      <div class="legal-h2">7. Acceptable Use</div>
      <p class="legal-p">You agree not to use Quantum Cube for any unlawful purpose, to attempt to circumvent the payment system or account controls, to decompile or reverse engineer the application, or to reproduce or redistribute the content of any reading.</p>
      <div class="legal-h2">8. Disclaimer of Warranties</div>
      <p class="legal-p">Quantum Cube is provided &ldquo;as is&rdquo; without warranties of any kind. Quantum Neuro Creations does not warrant that the app will be error-free, uninterrupted, or suitable for any particular purpose. Numerology and astrology interpretations are provided for entertainment and self-reflection only and do not constitute professional psychological, medical, financial, legal, or life advice.</p>
      <div class="legal-h2">9. Limitation of Liability</div>
      <p class="legal-p">To the maximum extent permitted by law, Quantum Neuro Creations shall not be liable for any indirect, incidental, special, or consequential damages arising from your use of or inability to use the app.</p>
      <div class="legal-h2">10. Governing Law</div>
      <p class="legal-p">These Terms are governed by the laws of the Republic of South Africa. Any disputes shall be subject to the jurisdiction of the South African courts.</p>
      <div class="legal-h2">11. Changes to These Terms</div>
      <p class="legal-p">We may modify these Terms from time to time. The effective date at the top of this document reflects the most recent revision. If a change is significant, we will notify account holders at their registered email address before it takes effect. Continued use of the app after changes constitutes acceptance of the revised Terms.</p>
      <div class="legal-h2">12. Contact</div>
      <p class="legal-p">For Terms enquiries: <strong>privacy@qncacademy.com</strong>.</p>
    </div>
"""

TERMS_RE = re.compile(
    r"<!-- TERMS OF USE -->.*?</div>\s*(?=\n\s*<!-- DISCLAIMER -->)",
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

    matches = TERMS_RE.findall(text)
    if len(matches) == 0:
        die("Terms: anchor pattern matched 0 times -- aborting.")
    if len(matches) > 1:
        die(f"Terms: anchor pattern matched {len(matches)} times -- aborting.")

    text = TERMS_RE.sub(TERMS_NEW.rstrip() + "\n", text, count=1)

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
