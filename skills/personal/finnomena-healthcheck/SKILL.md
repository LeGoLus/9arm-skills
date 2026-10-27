---
name: finnomena-healthcheck
description: >
  Make Finnomena advisor Health Check reports (AI Wealth Healthcheck, advisors.finnomena.com/healthcheck,
  Portfolio Simulator) through the site's own JSON API with the user's login: check codes, create the report,
  wait, save both PDFs unlocked to Drive. Page layout notes kept for manual checks.
---

# Finnomena Healthcheck (advisor back office)

> Normal runs use the API (section "How it runs"). The page notes below are for manual checks and a fallback.

## Hard rules

- The user logs in. Never type passwords, OTPs, ID or account numbers.
- Read and navigate freely. Ask before any click that saves, submits, sends a report,
  creates/deletes a portfolio, or places/changes an order — every time.
- Client names and figures stay in the browser and the chat; never write them into this
  file, a repo, or any outside service.
- Report what the system shows; do not give investment advice of your own.

## Pages

| Page | URL | Title |
|---|---|---|
| Dashboard | `https://advisors.finnomena.com/healthcheck/` | Portfolio Dashboard |
| Portfolio Simulator | `https://advisors.finnomena.com/healthcheck/simulator` | Portfolio Simulator |

### Dashboard
- Cards: TODAY, SCHEDULED, ALL, COMPLETED.
- Lists (row › opens it): Overdue, Ready to Report, In Progress, New — count on the right.
- Blue link at the bottom: **Portfolio Simulator ›**.

### Portfolio Simulator
- Back arrow (top-left) → Dashboard.
- Search box + filter button (right of search).
- **+ Create Portfolio** button (creates data — ask first).
- Saved portfolios grouped by month, then day. Each row: name, a type tag
  (e.g. Mutual Fund, Bond) and a document icon on the right.

The list on the Simulator page holds **simulation reports only** (not real portfolios or
orders). Creating one makes a new simulation report; it does not trade.

### Create Portfolio, screen 1 (opens over `/healthcheck/simulator`, same URL)
- **Customer Name**, optional text box (placeholder "John Dee").
- **Choose asset type**, radio (exactly one): Mutual Fund (`FUND`, default) ·
  Thai Stock (`STOCK`) · Bond (`BOND`).
- Bottom: **Cancel** (left) · **Next →** (right).

## Manual steps in the page (fallback only: when the API calls stop working)

1. Open the Dashboard URL. If counts are `–`/empty, the session may be logged out:
   ask the user to log in themselves.
2. Click **Portfolio Simulator ›** (or open `/healthcheck/simulator` directly).
3. Click **+ Create Portfolio**.
4. Customer Name: type what the user gives (may be blank). Pick the asset type.
   Click **Next →**.
5. Screen 2 (Mutual Fund, mode มูลค่า): for each holding the **user** names
   (never pick funds or amounts yourself):
   - click the ชื่อกองทุน box of an empty row, type the fund code exactly
     (e.g. `SCBSEMI(A)`, `KKP TECH RMF-H`), wait ~2 s for the spinner;
   - it must show green **✓ ข้อมูลถูกต้อง** under the row. No tick → stop and ask
     the user for the exact code;
   - click the มูลค่า box, type digits only (`100000`; the page adds the comma);
   - next fund: **+ เพิ่มกองทุน** adds an empty row. Each row has **×** to remove it.
   - click blank page area, screenshot, and check every row against the input.
   **View Report** turns dark when all rows are valid.
6. Click **View Report** (user-approved step: it saves the simulation and starts
   generating reports). A toast says **ส่งคำขอสร้างรายงานแล้ว**, then the page
   becomes **Portfolio Detail**.
7. Append the log line now (report exists from this point).
8. Wait ~20-30 s (check every 10 s) until both sections show a **Download** button
   instead of a % spinner.
9. Save both PDFs (the user asked for this as part of the task, 2026-10-23):
   - **Download** opens the PDF in a new tab instead of saving. Take its URL
     (`https://storage.googleapis.com/scontent.finnomena.com/health-check/reports/<file>`),
     `curl -sSf -o` it to the scratchpad, check the first bytes are `%PDF`, then close the tab.
     The Customer Report URL has **no `.pdf`** suffix (`.../<uuid>`); the Advisor Script
     URL ends in `.pdf`.
   - Copy with `cp -n` (never overwrite) into
     `~/Library/CloudStorage/GoogleDrive-<user>/My Drive/Finance/IC License/Finnomena/`
   - File names (user's convention; the password in the name is the user's choice):
     `<YYYY-MM-DD>_<HHMM>_<CustomerName|NoName>_<FUND|STOCK|BOND>_1-AdvisorScript_PW-<pw>.pdf`
     `<YYYY-MM-DD>_<HHMM>_<CustomerName|NoName>_<FUND|STOCK|BOND>_2-CustomerReport_PW-<pw>.pdf`
     Date/time = the report name. `NoName` until the form supplies a customer name.
   - Read each password by zooming on its row.
10. Make unlocked copies (user's request: easier to use, these are the user's own
    reports): decrypt each `_PW-<pw>.pdf` with its password via pypdf and write the same
    name without `_PW-<pw>` (never overwrite). "WRONG PASSWORD" → re-read the password
    from the screen. Script: `python3 scripts/unlock_pdf.py "<folder>"/*_PW-*.pdf`
    (run from `~`, not from the Drive folder). Check with `pdfinfo` (`Encrypted: no`) and render page 1 with
    `pdftoppm` to look at it. Then move the two `_PW-` originals to the macOS Trash
    (`mv -n` into `~/.Trash/`, recoverable; user's choice 2026-10-23) so the folder
    holds exactly 2 files per report, both without password. Never `rm`.
    (Finder `delete` via osascript timed out on the Drive folder; use `mv`.)
    First run: Advisor Script 12 pages ("Fund Health Check Pitch Buddy"),
    Customer Report 9 pages ("Fund Health Check Report").
11. _(next step: to be taught)_

### Portfolio Detail (still `/healthcheck/simulator`)
- Header: report name + type tag · **Edit** (changes the holdings, ask first).
- **Holdings**: Fund · Amount (4 decimals, e.g. `100,000.0000`). Check it matches the input.
- **Advisor Script**: file `pitch_buddy_<uuid>.pdf` (for the advisor), Password + copy icon,
  PDF **Download**.
- **Customer Reports**: file `<uuid>.pdf` (for the customer), Password + copy icon,
  PDF **Download**.
- Both start at 0-10 % and fill to 100 %; the Customer Report finished first (~20 s),
  the Advisor Script ~30 s.
- **PDF passwords are secrets**: they go only into the saved PDF file names (the user's
  choice). Never into the log, this file or chat summaries.
N. After it is saved, append one line to the creation log (see below).

### Create Portfolio, screen 2: Mutual Fund (same URL)
- Header: report name = creation timestamp `YYYY-MM-DD HH:MM:SS` + type tag. With no
  customer name, this timestamp is the name shown in the Simulator list.
- Toggle: **มูลค่า** (by value, default) · **หน่วยและ NAV** (units and NAV).
- Row: **ชื่อกองทุน** (fund code, placeholder `ASP-DIGIBLOC`) · **มูลค่า** (placeholder `10,000`).
  Grey text is a placeholder, not a value.
- **+ เพิ่มกองทุน** adds a row · **ล้างค่า** clears all rows.
- Privacy note on the page: the system only analyses portfolio data; hide account
  numbers or user IDs before uploading.
- Bottom: **Cancel** · **View Report** (grey/disabled until the rows are filled).
- **หน่วยและ NAV** mode row: **ชื่อกองทุน** · **จำนวนหน่วย** (placeholder `1000.0000`) ·
  **NAV ต้นทุนเฉลี่ย** (placeholder `15.000`). Seen 2026-10-23, not yet used for a report.
- Mutual Fund goes straight to the rows (no upload screen, unlike Stock and Bond).

**Cancel** at any point before View Report saves nothing (checked 2026-10-23: the list did not
change). Next → only opens screen 2; the report exists only after View Report.

### Create Portfolio, screen 2: Thai Stock (seen 2026-10-23, no report made yet)
- First a choice: **อัปโหลดรูปพอร์ต** (drop or **เลือกไฟล์**, JPG/PNG/WEBP only: a screenshot of
  the portfolio, read by Finnomena) or **กรอกข้อมูลเอง** (type it in). We use กรอกข้อมูลเอง.
- Toggle: **มูลค่า** (default) · **หน่วยและราคา**.
  - มูลค่า row: **ชื่อหุ้น** (placeholder `CPALL`) · **มูลค่า** (placeholder `10,000`).
  - หน่วยและราคา row: **ชื่อหุ้น** · **จำนวนหุ้น** (`100`) · **ราคาซื้อเฉลี่ย** (`10.00`).
- Symbol check like funds: `PTT` → green **✓ ข้อมูลถูกต้อง**; unknown (`ZZZQ`) → red
  **ไม่พบข้อมูล** and View Report stays grey. View Report turned dark with only a valid symbol
  (amount boxes still blank): always fill the amounts before clicking.
- **+ เพิ่มหุ้น** adds a row · paperclip = attach an image · **ล้างค่า** clears.

### Create Portfolio, screen 2: Bond (seen 2026-10-23, no report made yet)
- Same upload-or-**กรอกข้อมูลเอง** choice first.
- Row: **ประเภท** select (`บริษัท` = value `issuer`, default · `หุ้นกู้` = value `issue_number`) ·
  **ชื่อ/รหัสหุ้นกู้** · **ต้นทุน** (placeholder `2,000,000.00`).
  - บริษัท: issuer symbol, placeholder `BANPU` → `BANPU` gave ✓ ข้อมูลถูกต้อง.
  - หุ้นกู้: ThaiBMA bond code, placeholder `CPALL266A`; that placeholder itself gave
    **ไม่พบข้อมูล** (probably matured): a real outstanding code is needed.
  - The select ignores keyboard arrows; set it with form_input (value `issue_number`).
- **+ เพิ่มหุ้นกู้** adds a row · paperclip · **ล้างค่า**.
- Portfolio Detail of a saved bond report shows Holdings as **Issuer · Issue No. · Cost**
  (an issuer-only row shows Issue No. `—`).

## How it runs: Finnomena's own web API (since 2026-10-25), not clicking the page

The Simulator page only calls a small JSON API on the same site, authorised by the login cookie. The pipeline calls it
directly (`~/projects/decision-finance-tools/pipeline/finno_api.py`; endpoints and payloads documented at its top,
read from the page's `_nuxt` JS bundle). Same output as before: the same report in the Simulator list, both PDFs saved
unlocked to the Drive folder with the same names, the same history row. What changed: no form filling, no spinners,
no screen reading, no matching rows by text.

1. `GET /auth/verify` → the advisor (`profile.id`); no profile = logged out.
2. `POST validate-{fund|stock|bond}-data` for **every** holding (`{fund_code}` / `{stock_name}` / `{issuer}` or
   `{issue_number}` → `data.valid`). Any `false` → stop, nothing is created, mark the request failed with the codes.
3. `POST generate-report-by-f4a` `{asset_type, created_by, customer_id, firstname, lastname, portfolio}` → `request_id`.
   This is the View Report step (creates the simulation report). Items as the form sends them:
   FUND value `{fund_code, amount, input_mode:"amount"}` · units `{fund_code, shares, avg_cost, input_mode:"unit"}` ·
   STOCK `{stock_name, amount|volume+avg_cost, input_mode}` · BOND `{issuer, issue_number, cost, maturity_date:null,
   interest_rate:null}`. Customer name is split at the first space (first name / rest).
   `created_by` must be the advisor id **as a string** (a number gets HTTP 422, nothing created).
   First live run 2026-10-25 (TEST, SCBSEMI(A) 100,000): Customer Report 100 % within ~10 s, Advisor Script
   ~1 min; Finnomena filled NAV/units itself exactly as for a page-made report; PDFs 7 + 12 pages, unlocked OK.
4. Poll `GET requests/<id>/state` every 10 s **and** `GET requests/<id>`'s `report_status_progress` /
   `pitch_buddy_report_status_progress` (/state reads 0 once a job is finished).
5. `GET requests/<id>` → `report_url` + `report_password`, `pitch_buddy_report_url` + `pitch_buddy_report_password`
   → `hc_runner.finish()` (download, unlock, Drive, log, mark ready). Passwords never go to chat.

If Finnomena changes the site and a call 404s: open the Simulator, list `_nuxt/*.js`, and search the bundle for
`ai-wealth-healthcheck` to find the new paths. cli-anything does not fit here (it wraps desktop apps from their source).

## Unattended runner (needs its own login once)
`uv run hc_runner.py` (Hermes job `decision-finance-tools-healthcheck-runner`, every 30 min 08-21h) does steps 1-5
with Playwright's request context over its own profile (`~/.local/share/decision-stock/hc-browser`); no page is
opened. The user logs in there once: `uv run hc_runner.py --login` (never type the password for them). When it
prints "session expired", ask the user to run that again. (Checked 2026-10-25: that profile is not logged in.)

## Model routing (model-ladder: tier from ~/.agents/tiers.json "skills.finnomena-healthcheck")

Proven 2026-10-27 (`~/Documents/model-ladder/ledger.md`): MiniMax 3/3 and Haiku 3/3 match Opus on the API run
(validate, create, wait, download, unlock). Route: MiniMax → Haiku → Sonnet → Opus.

- **Queue, every 30 min:** `hc_runner.py` (plain Python, no model). Nothing to route.
- **A one-off report asked in chat:** do the heavy part on the routed tier, not in this session:
  ```
  python3 ~/9arm-skills/skills/personal/model-ladder/scripts/ladder.py run --skill finnomena-healthcheck \
    --cwd ~/projects/decision-finance-tools/pipeline --prompt-file <task.txt> --unattended \
    --tools "Read,Write,Edit,Bash(uv run *),Bash(python3 *),Bash(ls *)" \
    --check "test -s {out}/customer.pdf && test -s {out}/advisor.pdf" \
    --goal "one Health Check report via the API" \
    --rubric "both PDFs unlocked, page counts as Finnomena gives, real request_id, no passwords in files or reply"
  ```
  `task.txt` = the proven case prompt (`~/Documents/model-ladder/cases/finnomena-healthcheck-api.case.json`) with
  the customer, asset type and holdings filled in. It saves only to `{out}`.
- Then, in this session: check both PDFs open and the page counts, copy them to the Drive folder with the naming
  convention (`cp -n`), and append the history row. Those steps were not part of the proof, so they stay here.
- A failed tier prints a report: read it, tell the user the cause, `ladder.py feedback finnomena-healthcheck bad "..."`.

## Run the site queue ("ทำ Health Check ที่ค้าง"): assisted, in the user's own Chrome

The user's Chrome is logged in, so the API calls run there with the javascript tool (fetch with the user's cookie;
nothing is clicked or typed). Everything else is `hc_runner.py` (plain `python3`, from
`~/projects/decision-finance-tools/pipeline`). Asking for this is the user's approval to create the queued reports and
save their PDFs; sending an email is a separate step, approved each time.

Loop until the queue is empty:
1. `python3 hc_runner.py --next` → `{"id", "name", "left", "js"}` (`id` null = nothing waiting; marks it "running").
2. In a tab on `https://advisors.finnomena.com/healthcheck/simulator`, run `js` → `{saved, request_id}` or
   `{saved: false, refused, reason}`. Refused → `python3 hc_runner.py --fail <id> "<reason>"`, tell the user.
   `reason: "logged out"` → ask the user to log in to Finnomena in Chrome, then retry the same `js`.
3. `python3 hc_runner.py --saved <id>` → prints `created_at` (history row written).
4. Every ~20 s (wait with the computer tool's `wait`; one javascript call must finish within 45 s, so never loop
   inside it) run the output of `python3 hc_runner.py --read-js <request_id>` → `{full, pitch, customer, advisor,
   pw}`; done when `customer` is set and `pitch` is 100 (or after ~5 min take the Customer Report alone).
5. `echo '<that JSON>' | python3 hc_runner.py --finish <id> --created "<created_at>"` → saves both PDFs unlocked
   to the Drive folder, fills `customer_pdf`, reads Deep Analysis requests into `data/deep/`, marks the request ready.
   Never echo the passwords in chat; they only travel inside that JSON.
6. After a Deep Analysis batch: `python3 deep_analysis.py --site` (the page data; the next scheduled deploy publishes it).

### Deep Analysis requests (note starts with `deep:`)
Queued by `python3 deep_analysis.py --queue` (decision-finance-tools/pipeline): one request per theme,
customer name `Deep <YYYY-MM> <theme>`, 100,000 per fund, `send_to` empty. They are the user's own research:
make the report exactly as for a client (steps above, Advisor Script optional), then instead of mailing:
`python3 deep_analysis.py --read "<Drive>/<file>_2-CustomerReport.pdf" --theme <theme> --month <YYYY-MM> --request <id>`
(note `deep:<month>:<theme>` gives both). That reads the PDF into `data/deep/<month>/<theme>.json` and marks the
request ready. Never send these to anyone. File names use the customer name as usual (`Deep 2026-11 หุ้นโลก`).

## Input format (what the user's app hands over)

The page = the products the customer is interested in. One request = one report, one asset type:

```yaml
customer_name: ""          # optional, blank → report is named by timestamp
customer_email: ""         # where the unlocked Customer Report goes (the app sends it, not this skill)
asset_type: FUND           # FUND | STOCK | BOND
mode: value                # FUND: value | units_nav · STOCK: value | units_price · BOND: always cost
holdings:                  # FUND
  - fund: SCBSEMI(A)       # exact fund code as Finnomena knows it
    value: 100000          # baht, digits only        (units_nav: units: 1000.0000, nav: 15.000)
# STOCK:  - stock: PTT, value: 100000                 (units_price: shares: 100, price: 34.50)
# BOND:   - kind: issuer | issue_number, code: BANPU | <ThaiBMA code>, cost: 2000000
```

## TODO (user will do later)

- [ ] Build the input form in the user's app that outputs the format above
      (added 2026-10-23).
- [x] Screens for `units_nav`, STOCK and BOND seen (2026-10-23).
- [x] First STOCK and BOND reports (2026-10-23, customer name TEST; holdings chosen by the
      assistant on the user's instruction: PTT/CPALL/KBANK 100,000 each; issuer BANPU/CPALL
      1,000,000 each):
      - Portfolio Detail does **not** update by itself: go back to the list and reopen the
        report to see new progress.
      - STOCK: Customer Report "Stock Health Check Report" (Definit by Finnomena) 12 pages,
        ready after ~3 min; Advisor Script 10 pages. Holdings show Stock · Amount.
      - BOND: Customer Report "Bond Health Check Report" 10 pages, ready ~2 min; Advisor
        Script was still 10 % after 5 min. Issuer-only rows give "Time to Maturity N/A":
        use ThaiBMA bond codes for a real client.
      - With a customer name, the report name is that name (not the timestamp); file names
        still use the creation time (HHMM).
      - Download links can be read without clicking: every `a[href*="storage.googleapis"]`
        on Portfolio Detail (Customer Report link has no `.pdf`).
- [ ] Teach how the report appears in the Simulator list afterwards.
- [ ] Customer name comes from the form → use it in the report name and the PDF file
      names instead of `NoName` (pending, 2026-10-23).

## Creation log

`~/Documents/Finnomena/simulator-log.csv` (user's Mac, outside any repo; confirmed 2026-10-23).
Header: `created_at,customer_name,asset_type,report_name,url,funds,customer_pdf,sent_at,sent_to`
(the last three added 2026-10-23; backup of the old file: `simulator-log.bak-20261023.csv`).
One line per report, appended right after it is saved; fill `customer_pdf` with the unlocked
Customer Report file name once it is in the Drive folder. `sent_at` / `sent_to` are written by
`pipeline/healthcheck_send.py` (decision-finance-tools) when the report is emailed; never by hand
from a guess. See the whole history: `python3 healthcheck_send.py --list`.
Never commit or upload this file.
The log is a record only: every request gets a **fresh** report, even for holdings made before
(the report uses current market data; user's decision 2026-10-23). Never resend an old PDF in
place of a new one.
