from pathlib import Path
from dotenv import load_dotenv
import os 

load_dotenv()

BASE_DIR = Path(__file__).resolve().parents[1]

SODA3_QUERY_ENDPOINT = f"https://health.data.ny.gov/api/v3/views/sf4k-39ay/query.json"

SOCRATA_APP_TOKEN = os.getenv("SOCRATA_APP_TOKEN")

FILENAME_RAW_PAGES = "sparcs_2024_raw_pages"
FILENAME_PROCESSED_PAGES = "sparcs_2024_processed_pages"
EXT = "parquet"

RAW_DIR = BASE_DIR / "data" / "raw"
PROCESSED_DIR = BASE_DIR / "data" / "processed"
SAMPLE_DIR = BASE_DIR / "data" / "sample"
MASTER_DIR = BASE_DIR / "data" / "master"
QUALITY_DIR = BASE_DIR / "data" / "quality_checks"

SAMPLE_FILE_PATH = SAMPLE_DIR / f"sample.{EXT}"
MASTER_FILE_PATH = MASTER_DIR / f"master.{EXT}"
DUPLICATES_FILE_PATH = QUALITY_DIR / f'duplicates.{EXT}'

SAMPLE_SIZE = 200_000
RANDOM_STATE = 2024

RUN_EXTRACTION = False
RUN_SAMPLE = True
RUN_TRANSFORM = True
RUN_MASTER = True
RUN_DUPLICATES = True