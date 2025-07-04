from lib.eweb import *
from lib.cav import *
from lib.helpers import *
from lib.processor import *
import os

def main():
    cav_directory = 'CAV'
    eweb_directory = 'EWEB'
    preprocessed_directory = 'PREPROCESSED' 
    processed_directory = 'PROCESSED' 
    cav_csv_files = find_csv_files(cav_directory)
    eweb_csv_files = find_csv_files(eweb_directory)
    all_csv_files = cav_csv_files + eweb_csv_files

    # get consumer house
    consumer_house = get_consumer_house(cav_csv_files)
    print(f"Consumer house: {consumer_house}")

    if all_csv_files:
        print("CSV files found:")
        for csv_file in all_csv_files:
            print(csv_file)
    else:
        print("No CSV files found in CAV or EWEB directories.")

    if eweb_csv_files:
        preprocess_eweb_csv_files(eweb_csv_files, preprocessed_directory)
    else:
        print("No EWEB CSV files to process.")

    if cav_csv_files:
        preprocess_cav_csv_files(cav_csv_files, preprocessed_directory)
    else:
        print("No CAV CSV files to process.")

    process_final_csv(preprocessed_directory, processed_directory, consumer_house)

    def delete_files_in_directories(*directories):
        for directory in directories:
            if os.path.exists(directory):
                for filename in os.listdir(directory):
                    file_path = os.path.join(directory, filename)
                    if os.path.isfile(file_path):
                        os.remove(file_path)

    # Delete files from CAV and EWEB directories
    delete_files_in_directories(cav_directory, eweb_directory, preprocessed_directory)

if __name__ == "__main__":
    main()
