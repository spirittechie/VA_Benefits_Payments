# VA Benefits Payment Calendar (2027)

This repository provides importable `.ics` calendars for monthly VA benefits payments. It separates the calculated VA payment date, estimated institution-specific early availability, and an estimated ACH notice window so those three events are not mistaken for one another.

VA benefits are paid in arrears. VA generally releases a monthly payment on the first day of the following month. When the first is a weekend or federal holiday, the calculated payment date moves to the preceding banking day. Early access is a courtesy or policy of the receiving bank, credit union, payment app, or other financial institution; it is not the official VA payment date.

## Calendar files

| File | Meaning |
| --- | --- |
| [`VA_Standard.ics`](VA_Standard.ics) | Calculated VA payment dates |
| [`VA_EarlyDeposit_1Day.ics`](VA_EarlyDeposit_1Day.ics) | Estimated availability one banking day early |
| [`VA_EarlyDeposit_2Days.ics`](VA_EarlyDeposit_2Days.ics) | Estimated availability two banking days early |
| [`VA_EarlyDeposit_3Days.ics`](VA_EarlyDeposit_3Days.ics) | Estimated availability three banking days early |
| [`VA_EarlyDeposit_4Days.ics`](VA_EarlyDeposit_4Days.ics) | Estimated availability four banking days early |
| [`VA_ACH_Notice.ics`](VA_ACH_Notice.ics) | Estimated date to begin watching for a VA notice or pending ACH information |

Choose one payment calendar based on the observed policy of your receiving institution. Importing multiple early-deposit calendars will create overlapping estimates.

## Subscribe to automatic updates

Apple users can click the appropriate button below to add a read-only calendar subscription. Because the subscription points to the stable file on `master`, future annual calendar updates will appear without downloading and importing another file.

| Calendar | Apple Calendar | Public subscription address |
| --- | --- | --- |
| Calculated VA payment dates | [![Subscribe with Apple Calendar](https://img.shields.io/badge/Apple_Calendar-Subscribe-000000?logo=apple)](https://raw.githubusercontent.com/spirittechie/VA_Benefits_Payments/master/VA_Standard.ics) | [HTTPS feed](https://raw.githubusercontent.com/spirittechie/VA_Benefits_Payments/master/VA_Standard.ics) |
| Estimated one banking day early | [![Subscribe with Apple Calendar](https://img.shields.io/badge/Apple_Calendar-Subscribe-000000?logo=apple)](https://raw.githubusercontent.com/spirittechie/VA_Benefits_Payments/master/VA_EarlyDeposit_1Day.ics) | [HTTPS feed](https://raw.githubusercontent.com/spirittechie/VA_Benefits_Payments/master/VA_EarlyDeposit_1Day.ics) |
| Estimated two banking days early | [![Subscribe with Apple Calendar](https://img.shields.io/badge/Apple_Calendar-Subscribe-000000?logo=apple)](https://raw.githubusercontent.com/spirittechie/VA_Benefits_Payments/master/VA_EarlyDeposit_2Days.ics) | [HTTPS feed](https://raw.githubusercontent.com/spirittechie/VA_Benefits_Payments/master/VA_EarlyDeposit_2Days.ics) |
| Estimated three banking days early | [![Subscribe with Apple Calendar](https://img.shields.io/badge/Apple_Calendar-Subscribe-000000?logo=apple)](https://raw.githubusercontent.com/spirittechie/VA_Benefits_Payments/master/VA_EarlyDeposit_3Days.ics) | [HTTPS feed](https://raw.githubusercontent.com/spirittechie/VA_Benefits_Payments/master/VA_EarlyDeposit_3Days.ics) |
| Estimated four banking days early | [![Subscribe with Apple Calendar](https://img.shields.io/badge/Apple_Calendar-Subscribe-000000?logo=apple)](https://raw.githubusercontent.com/spirittechie/VA_Benefits_Payments/master/VA_EarlyDeposit_4Days.ics) | [HTTPS feed](https://raw.githubusercontent.com/spirittechie/VA_Benefits_Payments/master/VA_EarlyDeposit_4Days.ics) |
| Estimated ACH notice window | [![Subscribe with Apple Calendar](https://img.shields.io/badge/Apple_Calendar-Subscribe-000000?logo=apple)](https://raw.githubusercontent.com/spirittechie/VA_Benefits_Payments/master/VA_ACH_Notice.ics) | [HTTPS feed](https://raw.githubusercontent.com/spirittechie/VA_Benefits_Payments/master/VA_ACH_Notice.ics) |

For Google Calendar, copy the appropriate HTTPS feed, open [Google Calendar's From URL settings](https://calendar.google.com/calendar/u/0/r/settings/addbyurl) on a computer, paste the address, and select **Add calendar**. Google does not support adding a URL subscription from its Android, iPhone, or iPad app.

## 2027 schedule

The month column identifies the month in which benefits accrue, not necessarily the month in which the payment reaches the account.

| Benefit month | Calculated VA payment date | Estimated one-banking-day-early date | Estimated ACH notice window |
| --- | --- | --- | --- |
| January | February 1, 2027 | January 29, 2027 | January 25, 2027 |
| February | March 1, 2027 | February 26, 2027 | February 22, 2027 |
| March | April 1, 2027 | March 31, 2027 | March 24, 2027 |
| April | April 30, 2027 | April 29, 2027 | April 22, 2027 |
| May | June 1, 2027 | May 28, 2027 | May 24, 2027 |
| June | July 1, 2027 | June 30, 2027 | June 23, 2027 |
| July | July 30, 2027 | July 29, 2027 | July 22, 2027 |
| August | September 1, 2027 | August 31, 2027 | August 24, 2027 |
| September | October 1, 2027 | September 30, 2027 | September 23, 2027 |
| October | November 1, 2027 | October 29, 2027 | October 25, 2027 |
| November | December 1, 2027 | November 30, 2027 | November 23, 2027 |
| December | December 30, 2027 | December 29, 2027 | December 22, 2027 |

The ACH notice calendar uses a configurable eight-calendar-day lead and moves a weekend or federal-holiday estimate forward to the next banking day. It is an informational watch date, not a confirmed VA transmission date, an official release date, or a guarantee that funds are available.

## Import a calendar

Download the single `.ics` payment calendar that matches your situation. You may also download `VA_ACH_Notice.ics` if you want the separate notice-window reminders.

In Google Calendar, open **Settings**, select **Import & export**, choose the downloaded file, select the destination calendar, and import it.

In Apple Calendar, select **File**, then **Import**, choose the downloaded file, and select the destination calendar.

Outlook supports `.ics` imports through its calendar import or add-calendar controls. The exact menu name varies between classic Outlook, new Outlook, and Outlook on the web.

## Source authority and limitations

The date calculation follows [VA payment guidance](https://www.knowva.ebenefits.va.gov/system/templates/selfservice/va_ssnew/help/customer/locale/en-US/portal/554400000001018/content/554400000256488/VA-Payments), which states that VA payments are generally released on the first and move to the preceding weekday when the first is a federal holiday or weekend. Federal holiday handling follows the [U.S. Office of Personnel Management holiday schedule](https://www.opm.gov/policy-data-oversight/pay-leave/federal-holidays/).

No early-deposit estimate is a promise by VA or a financial institution. Institution policies can change, transaction processing can vary, and a pending entry does not necessarily mean funds are spendable. Confirm actual availability with the bank, credit union, payment app, prepaid account provider, or other institution receiving the direct deposit.

This project is not affiliated with the U.S. Department of Veterans Affairs or any other government agency.

## Maintenance and contributions

`calendar_config.json` is the annual control file. `generate_ics.py` calculates banking days and produces every committed calendar. Do not hand-edit generated `.ics` files.

Run the generator and validation locally with:

```bash
python3 generate_ics.py
python3 -m unittest discover -s tests -v
python3 generate_ics.py --check
```

See [`CONTRIBUTING.md`](CONTRIBUTING.md) before proposing a change. Calendar corrections and institution-timing reports need a source or a concrete, dated observation. Direct repository, credential, secret, or vault access is not required to contribute.
