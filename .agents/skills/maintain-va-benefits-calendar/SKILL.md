---
name: maintain-va-benefits-calendar
description: Maintain and validate the annual VA benefits payment, early-deposit estimate, and ACH notice calendars in this repository. Use when rolling the repository to a new benefit year, correcting payment dates, changing banking-day or ACH-notice rules, regenerating ICS files, or reviewing a calendar-related contribution.
---

# Maintain the VA benefits calendars

Read `AGENTS.md`, `calendar_config.json`, `generate_ics.py`, `README.md`, and the tests before changing dates or rules.

Establish the target benefit year. Remember that each row describes a benefit month paid in arrears, so the January benefit is normally paid on or near February 1.

Verify the governing VA payment rule from an authoritative VA source. Verify observed federal holidays against the OPM schedule for the payment year and the following New Year's Day. Treat the published VA rule and OPM calendar as authority; do not infer official dates from bank blogs, search snippets, or user reports.

Keep three concepts distinct. Calculate the VA payment date from the first of the following month and roll backward over weekends and observed federal holidays. Calculate early-deposit estimates in banking days from the calculated payment date. Calculate the ACH notice watch date from the configured calendar-day lead, then move a non-banking-day estimate forward to the next banking day. Never state that an early or pending date guarantees spendable funds.

For an annual roll-forward, update `benefit_year` and `generated_at_utc` in `calendar_config.json`. Change the ACH lead or enabled early-deposit variants only when the maintainer requests it. Run `python3 generate_ics.py` rather than editing `.ics` files.

Update the README title and schedule table from the generated dates. Preserve the distinction between benefit month and payment date. Keep links to the authoritative VA and OPM sources current.

Run `python3 -m unittest discover -s tests -v` and `python3 generate_ics.py --check`. Inspect every generated calendar for twelve events, stable UIDs, all-day start and end values, tentative status on estimates, and dates that do not fall on weekends or observed federal holidays.

Submit changes through a focused branch and pull request. Do not grant or request repository, credential, secret, or vault access. Treat access changes as a separate owner-authorized security decision, never as a consequence of a calendar contribution.
