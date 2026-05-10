---
tags: [features, edge-function, payments]
---
# Dodo Payments Webhook

- Listens for payment events from Dodo
- On success: sets `profiles.has_paid = true` in Supabase
- Triggers welcome email via Resend
- EU Merchant of Record — handles VAT, refunds, compliance

→ [[supabase]] · [[resend]] · [[ADR-001]] · [[PROJECT_BRIEF]]
