---
name: finnomena-investment-view
description: >
  Track Finnomena's advisor "Investment View" page (advisors.finnomena.com/investment-view): take a dated snapshot of
  every model portfolio's funds and weights through the page's own read-only JSON API, store it, and report what
  shifted since the last snapshot ("fund X 60→55%", asset classes equity/bond/...), plus asset-allocation trends per
  portfolio. Use for "เช็ค Investment View", "Finnomena ปรับพอร์ตอะไร", "model port เปลี่ยนสัดส่วนไหม", "trend asset allocation".
---

# Finnomena Investment View tracker

Code: `~/projects/decision-finance-tools/pipeline/finno_invest_view.py` (tests: `test_finno_invest_view.py`,
`uv run pytest test_finno_invest_view.py` from `pipeline/`). Data: `~/Documents/Finnomena/investment-view/` only.

## Hard rules

- Read-only. Only the two GET calls below. Never click, save, submit or "notify" anything on the page.
- The user logs in. Never type passwords or OTPs. Logged out → stop and ask the user to log in to Chrome.
- The detail response also carries `affected_port` (client portfolios): the scripts delete it before returning
  anything. Never store, print or summarise it. Fund commentary text is not stored either.
- No Finnomena data in this repo (it is public): no fund codes, weights, dates or portfolio lists here.
- Report what Finnomena shows. No investment advice of our own.

## Endpoints (read from the bundle 2026-10-26; Vite/React app, not Nuxt)

| Call | Returns |
|---|---|
| `GET /private/api/v1/investment-view/list` | `data.current[]` / `data.upcoming[]`: `investment_view_id, plan_name, plan_type_display, plan_type_group, plan_type_shortcode, approved_at, published_at, status` |
| `GET /private/api/v1/investment-view/detail?view_id=<id>` or `?risk_level=<n>` | `data.plan_name` (portfolio name), `plan_type`, `views_list[]` (that portfolio's last 5 dated views), `investment_view{id, risk_level, iv_date, status, assets[{fund_shortcode, percent_old, percent_new}]}` |

- Auth: the login cookie `f4a_auth_token_prod`, also sent as header `x-authenticated-uuid` (the page's own axios
  helper does this). The scripts read it at run time inside the tab. It is never printed or written down.
- Plans with risk levels are fetched once per level (`risk_level` is unique across plans): `goal-based` 1-7,
  `1stm` 201-204, `goe` 50001-50016 (levels the account cannot see return nothing and are skipped).
  Every other plan is fetched by its `view_id`. Key = `shortcode` or `shortcode:risk_level`.
- Each view has its own `percent_old → percent_new`, so even the first snapshot shows Finnomena's latest change.

## How it runs (the user's Chrome, logged in)

All commands are `python3 finno_invest_view.py ...` from `~/projects/decision-finance-tools/pipeline`.

1. ToolSearch once for the claude-in-chrome tools (tabs_context_mcp, tabs_create_mcp, navigate, javascript_tool,
   tabs_close_mcp). Call `tabs_context_mcp`, open your own new tab on `https://advisors.finnomena.com/investment-view`.
2. `--js` prints one expression. Run it unchanged in that tab with `javascript_tool` (one call; about 60 requests,
   six at a time, done in a few seconds, far below the 45 s limit).
   - `{error: "logged out"}` → stop, ask the user to log in.
   - Otherwise it returns a JSON **array of short text lines** (`T|…`, one `P|…` per portfolio, `C|…` checksum).
3. Write that array **exactly as returned** to a scratchpad file, then `--save <file>`. The checksum line catches
   any copying mistake ("does not match its checksum" → copy again). It stores the snapshot and prints the diff.
4. If it says "N older views not in history yet": `--backfill-js` → run it in the tab → save → `--save-views <file>`.
   Repeat until "nothing to backfill" (60 views per batch).
5. Close your tab.

Why lines and not JSON: the javascript tool cuts any single string at about 1,000 characters, and the extension
blanks any value that looks like cookie or query-string data (`a=b;c=d`). So each portfolio is one line with
`fund:old>new` joined by `^`. Do not change those separators.

Unattended: `uv run finno_invest_view.py --run` does the same with Playwright over
`~/.local/share/decision-stock/hc-browser` (no page opened). That profile is not logged in (checked 2026-10-25);
the user logs in there once with `uv run hc_runner.py --login`. "session expired" → ask the user to do that again.

## Output files (`~/Documents/Finnomena/investment-view/`)

| File | What |
|---|---|
| `snapshots/YYYY-MM-DD.json` | one per day (Bangkok date): every portfolio with funds, old/new weights, view ids. A second run the same day replaces that day's file. |
| `weights.csv` | append-only, one row per day × portfolio × fund: `date,key,plan,name,risk_level,view_id,iv_date,fund,asset_class,theme,old,new` (a day is written once). |
| `history.csv` | append-only, one row per Finnomena view × fund: `view_id,iv_date,key,...,weight`. Use this for trends: it is dated by Finnomena's view date and includes backfilled older views. |

Asset class comes from this project's fund data (`site/data/funds.json`, SEC policy type): ตราสารทุน = equity,
ตราสารหนี้ = bond, ผสม = mixed, ทรัพย์สินทางเลือก = alternative (gold, commodities, REITs and similar); `theme` is the
project's theme tag (global, tech, gold, ...). Funds that are not in that file show as `unknown` (usually closed or
renamed funds). Refresh the file with the project's own fund build if many show `unknown`.

## Reading the output

- First snapshot: count of portfolios and funds, then "Finnomena's latest changes": each portfolio whose current
  view moved weights, `fund old→new%`, then `| class old→new%`.
- Later: `key name: new view <date>: fund a→b% (in|out) ... | equity a→b%, bond ...`. `(in)` = newly added,
  `(out)` = dropped to 0. `same view, edited` = Finnomena changed weights without a new date. `new portfolio` /
  `dropped` = a plan or risk level appeared or went away. `upcoming` = approved, not yet published.
- Last line: average asset-class weight across all portfolios (each portfolio counts equally; it is not a
  money-weighted figure and not a recommendation).
- `--trend <key>` (for example `--trend goal-based:7`, keys are in `weights.csv`): asset-class weights for each of
  that portfolio's views, oldest first. `--diff` repeats the diff of the last two snapshots.

## When Finnomena changes the site

A 404, an empty list or a missing field means the bundle changed. Steps (no clicking needed):
1. `curl -sSL https://advisors.finnomena.com/investment-view` into the scratchpad, take the `/assets/index-*.js`
   name from it and `curl` that file too (the Chrome tool redacts bundle text, so use curl).
2. Search it for `investment-view`: the route table lists the page chunks, and a small `investment-view-*.js` chunk
   holds the endpoint paths. Search the request helper for `x-authenticated-uuid` and the cookie name.
3. In the detail page chunk, look for `percent_old`, `percent_new`, `fund_shortcode`, `views_list`, `risk_level`, and
   the risk-level map (`"1stm":{201:...}`, Goals Navigator `50001...`).
4. Update the constants at the top of `finno_invest_view.py` (`LIST`, `DETAIL`, `TOKEN_COOKIE`, `RISK_LEVELS`) and
   the field names in `_record` and the JS `rec`. Keep the tests green, then run one snapshot.
cli-anything does not fit here: this is a web page, not a desktop app with source.
