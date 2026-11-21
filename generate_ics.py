#!/usr/bin/env python3
"""Generate VA benefits payment calendars from one annual configuration file."""

from __future__ import annotations

import argparse
import calendar
import json
import sys
from dataclasses import dataclass
from datetime import date, datetime, timedelta
from pathlib import Path


ROOT = Path(__file__).resolve().parent
DEFAULT_CONFIG = ROOT / "calendar_config.json"


@dataclass(frozen=True)
class CalendarEvent:
    uid: str
    start: date
    summary: str
    description: str
    status: str = "CONFIRMED"


def observed_day(day: date) -> date:
    if day.weekday() == calendar.SATURDAY:
        return day - timedelta(days=1)
    if day.weekday() == calendar.SUNDAY:
        return day + timedelta(days=1)
    return day


def nth_weekday(year: int, month: int, weekday: int, occurrence: int) -> date:
    first = date(year, month, 1)
    offset = (weekday - first.weekday()) % 7
    return first + timedelta(days=offset + (occurrence - 1) * 7)


def last_weekday(year: int, month: int, weekday: int) -> date:
    last = date(year, month, calendar.monthrange(year, month)[1])
    return last - timedelta(days=(last.weekday() - weekday) % 7)


def federal_holidays_observed_in(year: int) -> set[date]:
    """Return the standard US federal holidays observed in a calendar year."""
    holidays: set[date] = set()

    # Include adjacent actual years so an observed New Year's Day on December 31
    # is assigned to the calendar year in which the closure occurs.
    for actual_year in (year - 1, year, year + 1):
        fixed = (
            date(actual_year, 1, 1),
            date(actual_year, 6, 19),
            date(actual_year, 7, 4),
            date(actual_year, 11, 11),
            date(actual_year, 12, 25),
        )
        holidays.update(observed_day(day) for day in fixed)

        holidays.update(
            {
                nth_weekday(actual_year, 1, calendar.MONDAY, 3),
                nth_weekday(actual_year, 2, calendar.MONDAY, 3),
                last_weekday(actual_year, 5, calendar.MONDAY),
                nth_weekday(actual_year, 9, calendar.MONDAY, 1),
                nth_weekday(actual_year, 10, calendar.MONDAY, 2),
                nth_weekday(actual_year, 11, calendar.THURSDAY, 4),
            }
        )

    return {day for day in holidays if day.year == year}


def is_banking_day(day: date) -> bool:
    return day.weekday() < calendar.SATURDAY and day not in federal_holidays_observed_in(day.year)


def roll_back_to_banking_day(day: date) -> date:
    while not is_banking_day(day):
        day -= timedelta(days=1)
    return day


def roll_forward_to_banking_day(day: date) -> date:
    while not is_banking_day(day):
        day += timedelta(days=1)
    return day


def subtract_banking_days(day: date, count: int) -> date:
    if count < 0:
        raise ValueError("banking-day count must be non-negative")
    remaining = count
    while remaining:
        day -= timedelta(days=1)
        if is_banking_day(day):
            remaining -= 1
    return day


def official_payment_date(benefit_year: int, benefit_month: int) -> date:
    """Calculate the payment date for one month of accrued VA benefits."""
    if benefit_month == 12:
        scheduled = date(benefit_year + 1, 1, 1)
    else:
        scheduled = date(benefit_year, benefit_month + 1, 1)
    return roll_back_to_banking_day(scheduled)


def ach_notice_date(payment_date: date, lead_calendar_days: int) -> date:
    """Return an estimated notice date, moved forward off non-banking days."""
    if lead_calendar_days < 0:
        raise ValueError("ACH lead days must be non-negative")
    return roll_forward_to_banking_day(payment_date - timedelta(days=lead_calendar_days))


def escape_ics(text: str) -> str:
    return (
        text.replace("\\", "\\\\")
        .replace(";", "\\;")
        .replace(",", "\\,")
        .replace("\n", "\\n")
    )


def fold_ics_line(line: str, limit: int = 75) -> list[str]:
    """Fold ASCII calendar lines to the RFC 5545 content-line limit."""
    if len(line) <= limit:
        return [line]
    folded = [line[:limit]]
    remainder = line[limit:]
    while remainder:
        folded.append(" " + remainder[: limit - 1])
        remainder = remainder[limit - 1 :]
    return folded


def render_calendar(name: str, events: list[CalendarEvent], dtstamp: str) -> str:
    lines = [
        "BEGIN:VCALENDAR",
        "VERSION:2.0",
        "CALSCALE:GREGORIAN",
        "METHOD:PUBLISH",
        "PRODID:-//VA Benefits Payment Calendar//EN",
        f"X-WR-CALNAME:{escape_ics(name)}",
    ]

    for event in events:
        lines.extend(
            [
                "BEGIN:VEVENT",
                f"UID:{event.uid}",
                f"DTSTAMP:{dtstamp}",
                f"DTSTART;VALUE=DATE:{event.start:%Y%m%d}",
                f"DTEND;VALUE=DATE:{event.start + timedelta(days=1):%Y%m%d}",
                f"SUMMARY:{escape_ics(event.summary)}",
                f"DESCRIPTION:{escape_ics(event.description)}",
                f"STATUS:{event.status}",
                "TRANSP:TRANSPARENT",
                "END:VEVENT",
            ]
        )

    lines.append("END:VCALENDAR")
    folded = [part for line in lines for part in fold_ics_line(line)]
    return "\r\n".join(folded) + "\r\n"


def build_calendars(config: dict) -> dict[str, str]:
    year = int(config["benefit_year"])
    dtstamp = str(config["generated_at_utc"])
    ach_lead_days = int(config["ach_notice_lead_calendar_days"])
    early_offsets = [int(value) for value in config["early_deposit_banking_days"]]

    if not (2000 <= year <= 2100):
        raise ValueError("benefit_year must be between 2000 and 2100")
    try:
        datetime.strptime(dtstamp, "%Y%m%dT%H%M%SZ")
    except ValueError as exc:
        raise ValueError("generated_at_utc must use YYYYMMDDTHHMMSSZ") from exc
    if not early_offsets or any(value < 1 for value in early_offsets):
        raise ValueError("early_deposit_banking_days must contain positive integers")
    if len(set(early_offsets)) != len(early_offsets):
        raise ValueError("early_deposit_banking_days must not contain duplicates")

    official_dates = {
        month: official_payment_date(year, month) for month in range(1, 13)
    }

    official_events = []
    for month, payment_day in official_dates.items():
        month_name = calendar.month_name[month]
        official_events.append(
            CalendarEvent(
                uid=f"va-benefits-{year}-{month:02d}-official@va-benefits-payments",
                start=payment_day,
                summary=f"VA Benefits Payment - {month_name} {year}",
                description=(
                    f"Calculated VA payment date for {month_name} {year} benefits. "
                    "VA pays benefits in arrears and generally releases payment on the "
                    "first of the following month, or the preceding banking day when the "
                    "first is a weekend or federal holiday."
                ),
            )
        )

    calendars = {
        "VA_Standard.ics": render_calendar(
            f"VA Benefits Payments {year}", official_events, dtstamp
        )
    }

    for offset in sorted(early_offsets):
        events = []
        plural = "day" if offset == 1 else "days"
        for month, payment_day in official_dates.items():
            month_name = calendar.month_name[month]
            estimated = subtract_banking_days(payment_day, offset)
            events.append(
                CalendarEvent(
                    uid=f"va-benefits-{year}-{month:02d}-early-{offset}@va-benefits-payments",
                    start=estimated,
                    summary=(
                        f"Estimated VA Early Deposit ({offset} banking {plural}) - "
                        f"{month_name} {year}"
                    ),
                    description=(
                        f"Estimate for an institution that usually makes VA funds available "
                        f"{offset} banking {plural} before the calculated official payment "
                        "date. This is not a VA promise. Confirm timing with the bank, credit "
                        "union, payment app, or other receiving institution."
                    ),
                    status="TENTATIVE",
                )
            )
        filename = f"VA_EarlyDeposit_{offset}Day{'s' if offset != 1 else ''}.ics"
        calendars[filename] = render_calendar(
            f"Estimated VA Early Deposits - {offset} Banking {plural.title()} - {year}",
            events,
            dtstamp,
        )

    notice_events = []
    for month, payment_day in official_dates.items():
        month_name = calendar.month_name[month]
        notice_day = ach_notice_date(payment_day, ach_lead_days)
        notice_events.append(
            CalendarEvent(
                uid=f"va-benefits-{year}-{month:02d}-ach-notice@va-benefits-payments",
                start=notice_day,
                summary=f"Estimated VA ACH Notice Window - {month_name} {year}",
                description=(
                    f"Informational watch date approximately {ach_lead_days} calendar days "
                    "before the calculated payment date. A VA notice or pending transaction "
                    "may appear around this time. This is not the official payment date, a "
                    "confirmed ACH transmission date, or a guarantee that funds are available. "
                    "Timing varies by VA processing and receiving institution."
                ),
                status="TENTATIVE",
            )
        )
    calendars["VA_ACH_Notice.ics"] = render_calendar(
        f"Estimated VA ACH Notice Windows {year}", notice_events, dtstamp
    )

    return calendars


def load_config(path: Path) -> dict:
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def write_calendars(calendars: dict[str, str], output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    for filename, content in calendars.items():
        (output_dir / filename).write_text(content, encoding="utf-8", newline="")


def check_calendars(calendars: dict[str, str], output_dir: Path) -> bool:
    clean = True
    for filename, expected in calendars.items():
        path = output_dir / filename
        if not path.exists():
            print(f"missing generated calendar: {filename}", file=sys.stderr)
            clean = False
            continue
        with path.open("r", encoding="utf-8", newline="") as handle:
            actual = handle.read()
        if actual != expected:
            print(f"generated calendar is out of date: {filename}", file=sys.stderr)
            clean = False
    return clean


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, default=DEFAULT_CONFIG)
    parser.add_argument("--output-dir", type=Path, default=ROOT)
    parser.add_argument(
        "--check",
        action="store_true",
        help="verify committed calendars match the annual configuration",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    calendars = build_calendars(load_config(args.config))
    if args.check:
        return 0 if check_calendars(calendars, args.output_dir) else 1
    write_calendars(calendars, args.output_dir)
    for filename in calendars:
        print(filename)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
