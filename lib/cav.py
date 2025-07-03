import os
import csv
from datetime import datetime
from lib.helpers import remove_duplicate_rows

def get_consumer_house(cav_csv_files):
    """
    Returns the value at column 7, row 2 from the first CAV CSV file, or None if not found.
    """
    if cav_csv_files:
        try:
            with open(cav_csv_files[0], 'r', newline='', encoding='utf-8') as f:
                reader = csv.reader(f)
                rows = list(reader)
                if len(rows) > 1 and len(rows[1]) > 6:
                    return rows[1][6]
        except Exception as e:
            print(f"Error reading consumer house: {e}")
    return None

def preprocess_cav_csv_files(cav_csv_files, processed_dir):
    os.makedirs(processed_dir, exist_ok=True)
    if not cav_csv_files:
        print("No CAV CSV file to process.")
        return
    csv_path = cav_csv_files[0]
    processed_rows = []
    with open(csv_path, 'r', newline='', encoding='utf-8') as f:
        reader = csv.reader(f)
        rows = list(reader)
    for row in rows:
        if len(row) < 7:
            continue
        selected = [row[0], row[3], row[4], row[6]]
        try:
            date_obj = datetime.strptime(selected[0], "%Y-%m-%d %I:%M %p")
            selected[0] = date_obj.strftime("%Y-%m-%d")
        except Exception:
            try:
                date_obj = datetime.strptime(selected[0], "%Y-%m-%d")
                selected[0] = date_obj.strftime("%Y-%m-%d")
            except Exception:
                pass
        processed_rows.append(selected)
    # Remove duplicate rows using helper
    unique_rows = remove_duplicate_rows(processed_rows)
    processed_name = "CAV.csv"
    processed_path = os.path.join(processed_dir, processed_name)
    with open(processed_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerows(unique_rows)
    print(f"Processed and saved: {processed_path}")
