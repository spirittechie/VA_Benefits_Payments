# Repository Instructions

Treat `calendar_config.json` and `generate_ics.py` as the source of truth. Treat every `.ics` file as generated output. Never hand-edit a calendar file.

Use authoritative VA material for payment-release rules and OPM material for federal holidays. Describe institution-specific availability as an estimate unless a primary source supports a stronger claim. Do not convert user reports, search snippets, or marketing language into universal banking rules.

Keep these concepts separate in code and documentation: the calculated VA payment date, a receiving institution's estimated early-availability date, and the estimated ACH notice window. Never describe an ACH notice or pending transaction as proof that funds are available.

For an annual update, change `calendar_config.json`, regenerate all calendars, update the dated README table, and run both the unit tests and `python3 generate_ics.py --check`.

Preserve stable event UIDs for a given benefit year, benefit month, and calendar type. Use all-day events with an exclusive next-day `DTEND`. Keep generated content deterministic so validation can detect drift.

Contributors work through forks, branches, and pull requests. Do not grant, request, or imply repository, credential, secret, or vault access as part of an ordinary contribution. Do not change access controls unless the repository owner explicitly makes that a separate task.
