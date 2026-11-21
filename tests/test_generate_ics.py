import calendar
import tempfile
import unittest
from datetime import date
from pathlib import Path

from generate_ics import (
    ach_notice_date,
    build_calendars,
    check_calendars,
    is_banking_day,
    load_config,
    official_payment_date,
    subtract_banking_days,
    write_calendars,
)


ROOT = Path(__file__).resolve().parents[1]


class CalendarDateTests(unittest.TestCase):
    def test_2027_official_payment_dates(self):
        expected = {
            1: date(2027, 2, 1),
            2: date(2027, 3, 1),
            3: date(2027, 4, 1),
            4: date(2027, 4, 30),
            5: date(2027, 6, 1),
            6: date(2027, 7, 1),
            7: date(2027, 7, 30),
            8: date(2027, 9, 1),
            9: date(2027, 10, 1),
            10: date(2027, 11, 1),
            11: date(2027, 12, 1),
            12: date(2027, 12, 30),
        }
        actual = {
            month: official_payment_date(2027, month) for month in range(1, 13)
        }
        self.assertEqual(expected, actual)

    def test_early_estimates_use_banking_days(self):
        official = official_payment_date(2027, 5)
        self.assertEqual(date(2027, 5, 28), subtract_banking_days(official, 1))
        for month in range(1, 13):
            payment = official_payment_date(2027, month)
            for offset in range(1, 5):
                self.assertTrue(is_banking_day(subtract_banking_days(payment, offset)))

    def test_requested_2026_ach_notice_example(self):
        self.assertEqual(
            date(2026, 11, 23), ach_notice_date(date(2026, 12, 1), 8)
        )

    def test_new_year_observed_holiday_moves_december_payment(self):
        self.assertEqual(date(2027, 12, 30), official_payment_date(2027, 12))


class CalendarOutputTests(unittest.TestCase):
    def setUp(self):
        self.config = load_config(ROOT / "calendar_config.json")
        self.calendars = build_calendars(self.config)

    def test_expected_calendar_set(self):
        self.assertEqual(
            {
                "VA_Standard.ics",
                "VA_EarlyDeposit_1Day.ics",
                "VA_EarlyDeposit_2Days.ics",
                "VA_EarlyDeposit_3Days.ics",
                "VA_EarlyDeposit_4Days.ics",
                "VA_ACH_Notice.ics",
            },
            set(self.calendars),
        )

    def test_each_calendar_has_twelve_complete_events(self):
        for filename, content in self.calendars.items():
            with self.subTest(filename=filename):
                self.assertEqual(12, content.count("BEGIN:VEVENT"))
                self.assertEqual(12, content.count("END:VEVENT"))
                self.assertEqual(12, content.count("UID:"))
                self.assertEqual(12, content.count("DTSTAMP:"))
                self.assertEqual(12, content.count("DTSTART;VALUE=DATE:"))
                self.assertEqual(12, content.count("DTEND;VALUE=DATE:"))
                self.assertTrue(content.endswith("END:VCALENDAR\r\n"))

    def test_estimated_calendars_are_tentative(self):
        for filename, content in self.calendars.items():
            expected_status = (
                "STATUS:CONFIRMED" if filename == "VA_Standard.ics" else "STATUS:TENTATIVE"
            )
            self.assertEqual(12, content.count(expected_status))

    def test_committed_calendars_match_configuration(self):
        self.assertTrue(check_calendars(self.calendars, ROOT))

    def test_readme_schedule_matches_configuration(self):
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        year = int(self.config["benefit_year"])
        lead_days = int(self.config["ach_notice_lead_calendar_days"])
        for month in range(1, 13):
            official = official_payment_date(year, month)
            early = subtract_banking_days(official, 1)
            notice = ach_notice_date(official, lead_days)

            def display(day):
                return f"{day:%B} {day.day}, {day.year}"

            expected_row = (
                f"| {calendar.month_name[month]} | {display(official)} | "
                f"{display(early)} | {display(notice)} |"
            )
            self.assertIn(expected_row, readme)

    def test_check_detects_drift(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            output = Path(temp_dir)
            write_calendars(self.calendars, output)
            self.assertTrue(check_calendars(self.calendars, output))
            (output / "VA_Standard.ics").write_text("stale", encoding="utf-8")
            self.assertFalse(check_calendars(self.calendars, output))


if __name__ == "__main__":
    unittest.main()
