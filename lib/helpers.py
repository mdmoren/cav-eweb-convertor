import os
from datetime import datetime

def find_csv_files(directory):
    csv_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.csv'):
                csv_files.append(os.path.join(root, file))
    return csv_files

def month_name_to_number(month_name):
    try:
        return datetime.strptime(month_name, "%B").month
    except ValueError:
        try:
            return datetime.strptime(month_name, "%b").month
        except ValueError:
            return None

def remove_duplicate_rows(rows):
    """
    Remove duplicate rows from a list of lists, preserving order.
    """
    unique_rows = []
    seen = set()
    for row in rows:
        row_tuple = tuple(row)
        if row_tuple not in seen:
            seen.add(row_tuple)
            unique_rows.append(row)
    return unique_rows