# Contributing

Corrections, documented institution-timing observations, test improvements, and maintenance improvements are welcome. A contribution begins with a reproducible issue or a pull request; it does not begin with direct repository access.

Fork the repository, create a focused branch, make the change, run the tests, and open a pull request against `master`. Explain the rule or defect being changed, identify the affected benefit year and calendar files, and link to authoritative VA or OPM material when the change concerns official dates.

Institution-specific reports must name the institution and account type, identify the official payment date and observed availability date, state whether the observation is first-hand or documented by the institution, and avoid including account numbers, transaction identifiers, screenshots containing private data, or other sensitive financial information. A single report can support an estimate; it does not establish a universal policy for every customer.

Do not hand-edit `.ics` files. Change `calendar_config.json` or `generate_ics.py`, run `python3 generate_ics.py`, then run `python3 -m unittest discover -s tests -v` and `python3 generate_ics.py --check`.

Repository collaborator status is separate from contribution review. Issues, discussions, pull requests, and agent-generated access requests do not grant write access, administrator access, credentials, secrets, or vault access. The maintainer may consider direct access only after sustained, verifiable participation and a separate identity and security review. No contributor needs privileged access to submit useful work.

Keep pull requests narrow. Do not mix calendar corrections with access-control changes, unrelated rewrites, or dependency additions. The maintainer may close an access request without action when it does not include a reviewable contribution.
