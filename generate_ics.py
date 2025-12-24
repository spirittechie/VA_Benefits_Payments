import os
from datetime import datetime, date, timedelta

# Current time
now = datetime.utcnow().strftime('%Y%m%dT%H%M%SZ')

# Adjusted dates for each file
adjustments = {
    '1Day': {
        'January': '20260130',
        'February': '20260227',
        'March': '20260331',
        'April': '20260430',
        'May': '20260529',
        'June': '20260628',
        'July': '20260731',
        'August': '20260828',
        'September': '20260930',
        'October': '20261030',
        'November': '20261128',
        'December': '20261230'
    },
    '2Days': {
        'January': '20260129',
        'February': '20260226',
        'March': '20260328',
        'April': '20260429',
        'May': '20260528',
        'June': '20260627',
        'July': '20260730',
        'August': '20260827',
        'September': '20260927',
        'October': '20261029',
        'November': '20261127',
        'December': '20261229'
    },
    '3Days': {
        'January': '20260128',
        'February': '20260225',
        'March': '20260328',
        'April': '20260428',
        'May': '20260527',
        'June': '20260628',
        'July': '20260729',
        'August': '20260826',
        'September': '20260928',
        'October': '20261025',
        'November': '20261128',
        'December': '20261227'
    },
    '4Days': {
        'January': '20260127',
        'February': '20260224',
        'March': '20260328',
        'April': '20260425',
        'May': '20260526',
        'June': '20260627',
        'July': '20260725',
        'August': '20260825',
        'September': '20260927',
        'October': '20261025',
        'November': '20261128',
        'December': '20261226'
    }
}

def generate_ics(filename, dates):
    content = 'BEGIN:VCALENDAR\nVERSION:2.0\nPRODID:-//Jesse Paul//VA Disability Calendar//EN\n'
    for month, dtstart in dates.items():
        uid = f'va-2026-{month.lower()}-{filename.split("_")[2].lower()}@jessepaul.com'
        year = int(dtstart[:4])
        month_num = int(dtstart[4:6])
        day = int(dtstart[6:])
        start_date = date(year, month_num, day)
        end_date = start_date + timedelta(days=1)  # next day
        dtend = end_date.strftime('%Y%m%d')
        summary = f'VA Disability Payment - {month} 2026'
        description = 'Estimated early deposit; confirm with your bank. This is an estimate based on bank early deposit policies; actual dates may vary [5][6][7].'
        event = f'BEGIN:VEVENT\nUID:{uid}\nDTSTAMP:{now}\nDTSTART;VALUE=DATE:{dtstart}\nDTEND;VALUE=DATE:{dtend}\nSUMMARY:{summary}\nDESCRIPTION:{description}\nEND:VEVENT\n'
        content += event
    content += 'END:VCALENDAR\n'
    with open(filename, 'w') as f:
        f.write(content)

for key, dates in adjustments.items():
    filename = f'VA_EarlyDeposit_{key}.ics'
    generate_ics(filename, dates)