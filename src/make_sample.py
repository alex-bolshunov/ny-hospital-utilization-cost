import pandas as pd
import pyarrow.parquet as pq
from utils import get_files_by_extension
from config import (
    RAW_DIR, 
    EXT
    )

def get_sample_df(
    sample_size: int = 200_000,
    random_state: int = 42
) -> pd.DataFrame:
    """
    Create a reproducible random sample from raw Parquet files.

    The function reads raw Parquet files from RAW_DIR, samples rows from each file,
    combines the sampled rows, and returns a single DataFrame.

    Parameters
    ----------
    sample_size:
        Number of rows to include in the final sample.

    random_state:
        Seed used for reproducible random sampling.

    Returns
    -------
    pd.DataFrame:
        A DataFrame containing the sampled rows.
    """

    if sample_size <= 0:
        raise ValueError("sample_size must be greater than 0.")

    parquet_files = get_files_by_extension(RAW_DIR, EXT)

    if not parquet_files:
        raise ValueError(f"No {EXT} files found in {RAW_DIR}.")

    total_num_rows = 0

    for file_path in parquet_files:
        total_num_rows += pq.ParquetFile(file_path).metadata.num_rows

    if total_num_rows == 0:
        raise ValueError("The Parquet files contain zero rows.")

    if sample_size >= total_num_rows:
        sampled_dfs = []

        for file_path in parquet_files:
            df_current = pd.read_parquet(file_path)
            sampled_dfs.append(df_current)

        return pd.concat(sampled_dfs, ignore_index=True)

    frac = sample_size / total_num_rows

    sampled_dfs = []
    rows_collected = 0

    for file_index, file_path in enumerate(parquet_files):
        df_current = pd.read_parquet(file_path)

        is_last_file = file_index == len(parquet_files) - 1

        if is_last_file:
            current_sample_size = sample_size - rows_collected
        else:
            current_sample_size = round(len(df_current) * frac)

        if current_sample_size <= 0:
            continue

        if current_sample_size > len(df_current):
            current_sample_size = len(df_current)

        df_sample = df_current.sample(
            n=current_sample_size,
            random_state=random_state + file_index
        )

        sampled_dfs.append(df_sample)
        rows_collected += len(df_sample)

        if rows_collected >= sample_size:
            break

    sample_df = pd.concat(sampled_dfs, ignore_index=True)

    if len(sample_df) > sample_size:
        sample_df = sample_df.sample(
            n=sample_size,
            random_state=random_state
        ).reset_index(drop=True)

    return sample_df.reset_index(drop=True)


