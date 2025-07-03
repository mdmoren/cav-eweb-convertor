"""
This module processes preprocessed CAV and EWEB CSV files to generate a FINAL.csv file.

Workflow:
1. Grab the preprocessed csv files (CAV.csv and EWEB.csv) from the preprocessed directory.
2. For each row in EWEB, check if there is a missing entry in CAV.
3. For each row in EWEB, check in CAV if there's a match on date (EWEB col 3, CAV col 1) AND if EWEB column 1 Name contains the Staff_Last_Name from CAV column 3.
4. If there is no match, create a new row in FINAL.csv with the following columns:
   - House: consumer_house
   - Date: EWEB column 3
   - Shift: EWEB column 4
   - Staff's Name: EWEB column 1
   - Notes: EWEB column 2

The FINAL.csv file will be saved in the processed directory.
"""
import csv
import os

def process_final_csv(preprocessed_dir, processed_dir, consumer_house):
    """
    Compare preprocessed CAV and EWEB files and write missing entries to FINAL.csv.

    Args:
        preprocessed_dir (str): Directory containing CAV.csv and EWEB.csv.
        processed_dir (str): Directory to save FINAL.csv.
        consumer_house (str): Value to use for the 'House' column in FINAL.csv.

    Logic:
        - For each row in EWEB.csv, check if there is a matching row in CAV.csv.
        - A match is defined as:
            * EWEB column 3 (date) == CAV column 1 (date)
            * EWEB column 1 (Name) contains the Staff_Last_Name from CAV column 3
        - If no match is found, add a row to FINAL.csv with:
            * House: consumer_house
            * Date: EWEB column 3
            * Shift: EWEB column 4
            * Staff's Name: EWEB column 1
            * Notes: EWEB column 2
    """
    cav_path = os.path.join(preprocessed_dir, 'CAV.csv')
    eweb_path = os.path.join(preprocessed_dir, 'EWEB.csv')
    final_path = os.path.join(processed_dir, 'FINAL.csv')

    if not (os.path.exists(cav_path) and os.path.exists(eweb_path)):
        print("CAV.csv or EWEB.csv not found in preprocessed directory.")
        return

    # Read CAV.csv
    with open(cav_path, 'r', newline='', encoding='utf-8') as f:
        cav_reader = csv.reader(f)
        cav_rows = list(cav_reader)
    cav_header = cav_rows[0] if cav_rows else []
    cav_data = cav_rows[1:] if len(cav_rows) > 1 else []

    # Read EWEB.csv
    with open(eweb_path, 'r', newline='', encoding='utf-8') as f:
        eweb_reader = csv.reader(f)
        eweb_rows = list(eweb_reader)
    eweb_header = eweb_rows[0] if eweb_rows else []
    eweb_data = eweb_rows[1:] if len(eweb_rows) > 1 else []

    # Prepare FINAL.csv header
    final_header = ['House', 'Date', 'Shift', "Staff's Name", 'Notes']
    final_rows = [final_header]

    # For each EWEB row, check if there is a match in CAV
    for eweb_row in eweb_data:
        # EWEB: [Name, Time, date, shift]
        if len(eweb_row) < 4:
            continue
        eweb_name, eweb_time, eweb_date, eweb_shift = eweb_row[:4]
        # Notes is the time column (per your mapping)
        eweb_notes = eweb_time
        found = False
        for cav_row in cav_data:
            # CAV: [date, ..., staff_last_name, ...]
            if len(cav_row) < 3:
                continue
            cav_date = cav_row[0]
            cav_staff_last_name = cav_row[2].strip(',').lower()
            if eweb_date == cav_date and cav_staff_last_name in eweb_name.lower():
                found = True
                break
        if not found:
            final_rows.append([
                consumer_house,
                eweb_date,
                eweb_shift,
                eweb_name,
                eweb_notes
            ])
    # Write FINAL.csv
    os.makedirs(processed_dir, exist_ok=True)
    with open(final_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerows(final_rows)
    print(f"Processed and saved: {final_path}")
