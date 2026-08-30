import pandas as pd
from extract import extract_all_rows
from make_sample import get_sample_df
from transform import (
    clean_data,
    get_duplicate_raws
    )
from utils import (
    remove_files,
    get_files_by_extension
    )
from constants import USE_COLS
from config import (
    RAW_DIR, 
    PROCESSED_DIR,
    MASTER_DIR,
    FILENAME_RAW_PAGES, 
    FILENAME_PROCESSED_PAGES, 
    EXT,
    SAMPLE_DIR, 
    RUN_SAMPLE,
    RUN_EXTRACTION,
    RUN_TRANSFORM,
    RUN_DUPLICATES,
    RUN_MASTER,
    SAMPLE_SIZE,
    RANDOM_STATE,
    SAMPLE_FILE_PATH,
    MASTER_FILE_PATH,
    DUPLICATES_FILE_PATH
    )

#WRITE LOGIC TO CREATE FOLDERS IF THEY DO NOT EXIST
#WRITE README 
#ADD TESTS 

def main():

    #extract files
    if RUN_EXTRACTION:
        print("\nRunning extract block.")

        removed_raw_files = remove_files(RAW_DIR, EXT)
        if removed_raw_files:
            print(f"{len(removed_raw_files)} old raw files were deleted.")

        #get files from api
        for page_number, df in extract_all_rows(sleep_seconds = 0.1):
            output_path = RAW_DIR / f'{FILENAME_RAW_PAGES}_{page_number:04d}.{EXT}'
            df.to_parquet(output_path, index = False)

            print(f"Saved page {page_number} to {output_path}.")
        
        print(f"{page_number} files saved. Extract block completed.")

    #create sample for EDA
    if RUN_SAMPLE:
        print("\nRunning sample block.")

        files_to_sample = get_files_by_extension(RAW_DIR, EXT)

        if not files_to_sample:
            raise ValueError(f"No files to sample found in {RAW_DIR}.")

        removed_sample = remove_files(SAMPLE_FILE_PATH)

        if removed_sample:
            print(f"{SAMPLE_FILE_PATH} was deleted.")

        #generate new sample
        df = get_sample_df(sample_size = SAMPLE_SIZE, random_state = RANDOM_STATE)
        df.to_parquet(SAMPLE_FILE_PATH, index = False)

        print(f"{SAMPLE_FILE_PATH} is saved to {SAMPLE_DIR}. Sample block completed.")

    #transform files 
    if RUN_TRANSFORM:
        print("\nRunning transform block.")

        files_to_process = sorted(get_files_by_extension(RAW_DIR, EXT))

        if not files_to_process:
            raise ValueError(f"No raw files to process found in {RAW_DIR}.")
            
        #delete all processed files
        removed_files = remove_files(PROCESSED_DIR, EXT)

        if removed_files:
            print(f"Deleted {len(removed_files)} old processed files from {PROCESSED_DIR}.")
            
        #read, clean, write to separate files
        for file_path_read in files_to_process: 
            df = pd.read_parquet(file_path_read, columns = USE_COLS)
            df = clean_data(df, file_path_read)

            raw_page_id = file_path_read.stem.removeprefix(f"{FILENAME_RAW_PAGES}_")
            output_path = PROCESSED_DIR / f"{FILENAME_PROCESSED_PAGES}_{raw_page_id}.{EXT}"
            df.to_parquet(output_path, index = False)

            print(f"Saved {file_path_read.name} to {output_path.name}.")
            
        print(f"{len(files_to_process)} files were processed. Transform block completed.")

    #write master file
    if RUN_MASTER:
        print("\nRunning master block.")

        processed_files = get_files_by_extension(PROCESSED_DIR, EXT)

        if not processed_files:
            raise ValueError(f"No processed files found in {PROCESSED_DIR}. Master file was not created.")
        
        removed_master_file = remove_files(MASTER_FILE_PATH)
            
        #delete old master file
        if removed_master_file:
            print(f"{MASTER_FILE_PATH} was deleted.")
            
        #read all processed files, write master file
        df = pd.read_parquet(PROCESSED_DIR)
        df.to_parquet(MASTER_FILE_PATH, index = False)

        print(f"{len(processed_files)} processed files combines. Master file saved to {MASTER_DIR}. Master block completed.")

    if RUN_DUPLICATES:
        print("\nRunning duplicates block.")

        if not MASTER_FILE_PATH.exists():
            raise ValueError(f"{MASTER_FILE_PATH} doesn't exists. Duplicates file was not created.")

        #remove old file
        removed_duplicates_file = remove_files(DUPLICATES_FILE_PATH)

        if removed_duplicates_file:
            print(f"{DUPLICATES_FILE_PATH} was deleted.")
        
        #read master file, write duplicates 
        df = pd.read_parquet(MASTER_FILE_PATH)
        df_duplicates = get_duplicate_raws(df)
        df_duplicates.to_parquet(DUPLICATES_FILE_PATH, index = False)

        print(f"Duplicates file saved to {DUPLICATES_FILE_PATH}. The file contains {df_duplicates.shape[0]} instances.")
        

if __name__ == "__main__":
    main()