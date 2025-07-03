from lib.helpers import *
import os
import csv
import re
from datetime import datetime

def time_to_24h(time_str):
    """
    Converts 12h time like '9a', '5p', '1a', '12p', '12a', '17:30p', etc. to integer 24h hour.
    """
    m = re.match(r'(\d{1,2})(?::\d{2})?([ap])', time_str)
    if not m:
        return None
    hour = int(m.group(1))
    ampm = m.group(2)
    if ampm == 'a':
        if hour == 12:
            hour = 0
    elif ampm == 'p':
        if hour != 12:
            hour += 12
    return hour

def get_shift(start_time):
    """
    Shift 1 (Day):   09-17
    Shift 2 (Even):  17-01 (17:00-24:00 or 0:00-1:00)
    Shift 3 (Night): 01-09
    """
    h = time_to_24h(start_time)
    if h is None:
        return ''
    if 9 <= h < 17:
        return '1'
    elif (17 <= h < 24) or h == 0:
        return '2'
    elif 1 <= h < 9:
        return '3'
    return ''

def preprocess_eweb_csv_files(eweb_csv_files, processed_dir):
    os.makedirs(processed_dir, exist_ok=True)
    current_year = datetime.now().year

    if not eweb_csv_files:
        print("No EWEB CSV file to process.")
        return

    csv_path = eweb_csv_files[0]
    processed_rows = []
    with open(csv_path, 'r', newline='', encoding='utf-8') as f:
        reader = csv.reader(f)
        rows = list(reader)

    for row in rows:
        if len(row) < 7:
            continue  # skip incomplete rows

        # 1. Remove non-digit chars from sixth column (index 5)
        row[5] = re.sub(r'\D', '', row[5])

        # 2. Skip rows where 7th column (index 6) is empty
        if not row[6].strip():
            continue

        # 3. Remove the first, third, and fourth columns (0,2,3)
        for drop_index in sorted([3,2,0], reverse=True):
            del row[drop_index]
        # Now: row[0]=M, row[1]=D, row[2]=d, row[3]=Notes

        M = row[0].strip()
        D = row[1].strip()
        d = row[2].strip()
        Notes = row[3].strip() if len(row) > 3 else ""

        # 5. Create date column
        month_num = month_name_to_number(M)
        try:
            day_num = int(d)
        except ValueError:
            day_num = None
        if month_num and day_num and 1 <= day_num <= 31:
            date_str = f"{current_year:04d}-{month_num:02d}-{day_num:02d}"
        else:
            date_str = ""

        # 6. Only keep Notes and date
        processed_rows.append([Notes, date_str])

    # Remove duplicate rows using helper
    unique_rows = remove_duplicate_rows(processed_rows)

    # Split Notes into Time and Name columns, split time to start/end, assign shift
    split_rows = []
    for row in unique_rows[1:]:  # skip header for now if present
        notes, date = row
        # Regex: time is everything up to the first space, name is the rest
        match = re.match(r'([^ ]+)\s+(.*)', notes)
        if match:
            time, name = match.groups()
        else:
            time, name = '', notes

        # Split time into start and end
        if '-' in time:
            start, end = time.split('-', 1)
            start = start.strip()
            end = end.strip()
        else:
            start = time
            end = ''

        shift = get_shift(start)
        split_rows.append([name, time, date, shift, start, end])

    # Add new header
    header = ['Name', 'Time', 'date', 'shift', 'start', 'end']
    split_rows.insert(0, header)

    # 7. Save to PROCESSED directory
    processed_name = "EWEB.csv"
    processed_path = os.path.join(processed_dir, processed_name)
    with open(processed_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerows(split_rows)
    print(f"Processed and saved: {processed_path}")
