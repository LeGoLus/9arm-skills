---
name: find
description: >
  Cross-category best-price finder. Use when the user invokes `/find` or asks to
  find the cheapest / best-value option for shopping items, flights, hotels, rental
  cars, or software subscriptions — especially across regions, currencies, and
  payment methods. Computes a true "net price" (base + FX fee + DCC + hidden fees
  − cashback) and compares sources transparently. Analyzes and recommends only;
  it never books or pays, and never bypasses any seller's Terms of Service.
---

# /find — Cross-Category Best-Price Finder

Find the genuinely cheapest **net price** for a purchase across multiple sources,
regions, currencies, and payment methods — then say plainly where to buy and how
to pay. Analyze and recommend only. **Never book, never pay, never automate checkout.**

## Hard ethical line (non-negotiable)

This skill helps with **legitimate, transparent** price optimization only:
- Comparing prices across regions/currencies that a seller openly offers.
- Choosing the card with the lowest FX/foreign-transaction fee.
- Avoiding DCC (Dynamic Currency Conversion) traps by paying in local currency.
- Identifying services that legitimately allow signup from another country.

It will **NOT** help with anything that deceives a seller or payment system:
- Faking geolocation/IP, billing address, or residency to defeat geo-pricing.
- Bypassing fraud detection, region locks, or signup restrictions by misrepresentation.
- Using a payment method in a way that violates the seller's Terms of Service.

When a path to a lower price *requires* any of the above, **flag it RED**, explain
why it breaks ToS, and offer the closest legitimate alternative instead. Do not
provide step-by-step instructions for the disallowed method, even in passing.

## Workflow

1. **Detect category** from the user's request: `shopping`, `flights`, `hotels`,
   `rental-cars`, or `software-sub`. If ambiguous, ask once.
2. **Run the category checklist** (below). If any required field is missing, ask
   for it before searching — group missing items into one short question.
3. **Load card profile** (see "Card profile" below) to know real FX fees / cashback.
4. **Search & fetch** prices across multiple sources and, where relevant, multiple
   regions/currencies. Snapshot once.
5. **Compute net price** per option using the 3-tier model.
6. **Output**: comparison table + a single decisive recommendation.

## Category checklists (required fields)

- **shopping** — item/model · region(s) selling it · ship-to-Thailand vs use-abroad
- **flights** — origin · destination · date(s) (out/return) · pax · direct-or-connecting · cabin class
- **hotels** — city/area · check-in/out · pax & rooms · cancellation policy wanted
- **rental-cars** — pickup/dropoff city or airport · date-time · car type · has IDP (intl driving permit)?
- **software-sub** — service name · feature to unlock · region(s) of interest · is there a legitimate payment method / address in that region?

For `software-sub`: only proceed if there is a **legitimate** way to sign up in the
target region (e.g. a real address, a properly issued card valid there). If the only
way to unlock the feature is to misrepresent location/identity — flag RED and stop.

## The 3-tier scoring model

**Tier 1 — folds into a single NET PRICE (the only ranking number):**
- `base` — list/fare/room price in its native currency
- `FX fee` — the paying card's foreign-transaction fee (from card profile)
- `DCC` — if the merchant offers to charge in THB, that's a DCC trap; always assume
  pay-in-**local**-currency and add a reminder. Never let DCC inflate the price.
- `hidden fees` — resort fees, airport/booking fees, taxes, shipping/duties; note
  any VAT that's refundable
- `cashback/points` — only count rewards realistically convertible to money, scoped
  to the correct foreign-spend category for that card; subtract from net

Net price = base + FX fee + hidden fees − realistic cashback. Convert all to THB
for the final comparison.

**Tier 2 — filters, not price:**
- features unlocked by region (relevant mainly for software-sub)
- **ToS risk** — RED = drop or warn; never rank a ToS-violating path as "best"

**Tier 3 — soft factors (tie-breakers only):**
- source trustworthiness, refund/cancellation policy. A 200-baht saving on a
  non-refundable booking usually isn't worth it — say so.

Do not arithmetic-mix tiers. Only Tier 1 produces the ranking number; Tier 2/3 are
conditions stated alongside it.

## Card profile

Read the user's card data from LifeVault (e.g. `cards-profile.md` / `.json`) when
available (Claude Desktop / Code / Hermes). If running where local files aren't
readable (e.g. Mobile), ask the user to paste card details, or fall back to the
embedded summary below.

Embedded summary (override with real numbers when the profile is available):
- **TTB Absolute — FX 1%** — the go-to card for any foreign-currency spend.
- KTC (most cards), UOB Premier, KBank Platinum, SCB First — assume **~2.5% FX**
  until real figures are filled in. Each card may have foreign-spend cashback/points
  worth counting — fill per-card values into the profile.

Always recommend paying with the **lowest net-cost card** for the chosen currency,
factoring FX fee minus realistic cashback — not just the lowest headline FX rate.

## Fetching prices

- Use `web_search` + `web_fetch` as the primary method. Take a **single snapshot**.
- Always warn that prices are live and may change; tell the user to **verify at
  the actual checkout** before paying.
- When a source can't be fetched (JS-rendered, login-walled, blocked): **say which
  source failed and why**, then give a **direct link plus the exact search/filter
  terms** so the user can open it themselves quickly. Don't silently drop it.

## Output format

1. **Comparison table** — columns: Source | Region | Currency | Net price (THB) |
   Pay-with card | Notes (DCC/ToS/refund). Sort by net price ascending.
2. **Verdict** — one decisive line: buy *here*, pay in *this currency* with *this
   card*, because *X*. Note the runner-up if it's close.
3. **Caveats** — live-price warning, any RED ToS flags, any sources you couldn't fetch.

## Acceptance criteria

- Every option ranked by a single THB net price; no mixed-tier math.
- TTB Absolute (or true lowest-net card) correctly recommended for FX spend.
- DCC reminder present whenever a foreign-currency payment is involved.
- Any ToS-risky path flagged RED with a legitimate alternative, never instructions.
- Unfetchable sources reported with reason + direct link + filter terms.
