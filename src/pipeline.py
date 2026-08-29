import pandas as pd
from extract import extract_all_rows
from utils import remove_files
from make_sample import get_sample_df
from transform import clean_data, get_duplicate_raws
from constants import USE_COLS
from config import (
    RAW_DIR, 
    PROCESSED_DIR,
    MASTER_DIR,
    QUALITY_DIR,
    FILENAME_RAW_PAGES, 
    FILENAME_PROCESSED_PAGES, 
    EXT,
    QC_EXT, 
    SAMPLE_DIR, 
    RUN_SAMPLE,
    RUN_EXTRACTION,
    RUN_TRANSFORM,
    RUN_MASTER,
    SAMPLE_SIZE,
    RANDOM_STATE
    )

#WRITE HELPER FUNCITONS TO CHECK FILES
#WRITE FUNCTION TO REMOVE FILES FROM A FOLDER 
#ADD DUPLICATE BLOCK
#WRITE README 
#ADD TESTS 

def main():

    #extract files
    if RUN_EXTRACTION:
        print("\nRunning extract block.")

        # RAW_DIR.parent.mkdir(parents=True, exist_ok=True)

        #delete all raw files
        old_raw_files = [
            file_path
            for file_path in RAW_DIR.iterdir()
            if file_path.is_file() and file_path.suffix[1:] == EXT
        ]

        for file_path in old_raw_files:
            file_path.unlink()
        
        if old_raw_files:
            print(f"{len(old_raw_files)} old raw files were deleted.")

        #get files from api
        for page_number, df in extract_all_rows(sleep_seconds = 0.1):
            output_path = RAW_DIR / f'{FILENAME_RAW_PAGES}_{page_number:04d}.{EXT}'
            df.to_parquet(output_path, index = False)

            print(f"Saved page {page_number} to {output_path}")

    #create sample for EDA
    if RUN_SAMPLE:
        print("\nRunning sample block.")

        sample_file_name = f"sample.{EXT}"
        sample_path = SAMPLE_DIR / sample_file_name

        #remove old one
        if sample_path.is_file():
            sample_path.unlink()
            print("Old sample file was deleted.")

        #generate new sample
        df = get_sample_df(sample_size = SAMPLE_SIZE, random_state = RANDOM_STATE)
        df.to_parquet(sample_path, index = False)

        print(f"{sample_file_name} is saved to {SAMPLE_DIR}.")  

    #transform files 
    if RUN_TRANSFORM:
        print("\nRunning transform block.")

        #delete all processed files
        removed_files = remove_files(PROCESSED_DIR, EXT)

        # old_processed_files = [
        #     file_path
        #     for file_path in PROCESSED_DIR.iterdir()
        #     if file_path.is_file() and file_path.suffix[1:] == EXT
        # ]

        # for file_path in old_processed_files:
        #     file_path.unlink()
    
        if removed_files:
            print(f"Deleted {len(removed_files)} old processed files from {PROCESSED_DIR}.")

        #read, clean, write to separate files
        files_to_process = sorted(
            file_path for file_path in RAW_DIR.iterdir() if file_path.is_file() and file_path.suffix[1:] == EXT
        )

        for file_path_read in files_to_process: 
            df = pd.read_parquet(file_path_read, columns = USE_COLS)
            df = clean_data(df, file_path_read)

            raw_page_id = file_path_read.stem.removeprefix(f"{FILENAME_RAW_PAGES}_")
            output_path = PROCESSED_DIR / f"{FILENAME_PROCESSED_PAGES}_{raw_page_id}.{EXT}"
            df.to_parquet(output_path, index = False)

            print(f"Saved {file_path_read.name} to {output_path.name}.")
        
        print(f"Preprocessing completed. {len(files_to_process)} files were processed.")

    #write master file
    if RUN_MASTER:
        print("\nRunning master block.")

        processed_files = [
            file_path 
            for file_path in PROCESSED_DIR.iterdir() 
            if file_path.is_file() and file_path.suffix[1:] == EXT
        ]

        if not processed_files:
            print(f"No processed files found in {PROCESSED_DIR}. Master file was not created")
        else:
            master_file_path = MASTER_DIR / f"master.{EXT}"

            #delete old master file
            if master_file_path.is_file():
                master_file_path.unlink()
                print("Old masster file was deleted.")
            
            #read all processed files, write master file
            df = pd.read_parquet(PROCESSED_DIR)
            df.to_parquet(master_file_path, index = False)

            print(f"{len(processed_files)} processed files combines. Master file saved to {MASTER_DIR}")

    #WORK WITH DUPLICATES, WRITE FILE, CALCULATE THE NUMBER OF DUPLICATES
    # #remove the duplicate file if exists
    # duplicates_output_path = QUALITY_DIR / f'duplicates.{QC_EXT}'
    # if duplicates_output_path.exists():
    #     duplicates_output_path.unlink()

    # print(df.duplicated(keep = "first").sum())

    # #check for duplicates, append to a file if the file contains duplicates
    # df_duplicates = get_duplicate_raws(df)

if __name__ == "__main__":
    main()