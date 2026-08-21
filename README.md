HVSS V7 — OPERATIONAL CORE UPGRADE
CREATED BY: Mbah Pri

Basis:
- Upgraded the supplied hvss2.html package instead of creating a new unrelated app.
- Central Spreadsheet ID:
  1z8oI95w0JITz9ILxLUjAszg0ijg4qz75huQiwRSkVBA

Operational core:
- Central database enforcement through Apps Script.
- Transaction ID generated server-side.
- Server timestamp Asia/Jakarta.
- LockService concurrency protection.
- Visitor state machine: OUTSIDE -> INSIDE -> OUTSIDE.
- Key state machine: AVAILABLE -> OUT -> AVAILABLE.
- Master visitor auto-fill/search.
- Current Visitors / Currently Inside.
- Active Keys / Currently Borrowed.
- Immutable AUDIT_LOG (append-only from application functions).
- No hard-delete is used by the operational core.
- Reports read from central logs.

Sheets created if missing:
VISITOR_MASTER
KEY_MASTER
VISITOR_LOG
KEY_LOG
AUDIT_LOG
SETTINGS

Important:
The existing UI is preserved as the base. A compact Operational Core panel is appended.
Set the deployed Apps Script /exec URL in the existing app's Central Database configuration, or:
localStorage.setItem('HVSS_CENTRAL_URL','YOUR_APPS_SCRIPT_EXEC_URL')
Then reload.
Deploy Code.gs as Web App: Execute as Me, access appropriate to your organization/use case.


CENTRAL URL EMBEDDED:
https://script.google.com/macros/s/AKfycbzpbab3_fYUaDGQpooOvK_uhp6IvXhojeua4-3YQ4hMAzJwYTePGkts8hUmoCiyKLyGjQ/exec

The endpoint is hard-wired into hvss2.html and seeded into localStorage on first load.
No manual Central URL entry is required for this build.
