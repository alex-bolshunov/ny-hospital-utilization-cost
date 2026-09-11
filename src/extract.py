import requests
import time
from typing import Iterator
import pandas as pd

from config import SODA3_QUERY_ENDPOINT, SOCRATA_APP_TOKEN

def query_sparcs(
    query: str, 
    page_number: int = 1, 
    page_size: 
    int = 1000) -> pd.DataFrame:

    """
    Query one page of the 2024 NY SPARCS de-identified inpatient discharge dataset.

    This function sends a POST request to the SODA3 API endpoint using a SQL-like
    query string and pagination settings. The API response is converted into a
    pandas DataFrame.

    Parameters
    ----------
    query:
        SQL-like SODA query to send to the API.
        Defalut: "SELECT *".

    page_number:
        Page number to request from the API.
        Defaults to 1.

    page_size:
        Number of rows to request per page.
        Defaults to 1,000.

    Returns
    -------
    pd.DataFrame
        A DataFrame containing the records returned for the requested page.
    """

    headers = {
        'Content-Type': 'application/json'
        }

    if SOCRATA_APP_TOKEN: 
        headers['X-App-Token'] = SOCRATA_APP_TOKEN

    payload = {
        'query': query,
        'page': {
            'pageNumber': page_number,
            'pageSize': page_size
        },
        'includeSynthetic':False
    }

    response = requests.post(
        SODA3_QUERY_ENDPOINT,
        headers = headers,
        json = payload,
        timeout = 120
    )

    response.raise_for_status()
    data = response.json()

    if isinstance(data, list):
        return pd.DataFrame(data)
    
    raise ValueError(f'Unexpected response structure: {data.keys()}')
    

def extract_all_rows(
    query: str = 'SELECT *',
    page_size: int = 50000,
    sleep_seconds: int | None = None,
    max_pages: int | None = None
) -> Iterator[tuple[int, pd.DataFrame]]:
    page_number = 1
    total_rows = 0

    """
    Extract all rows from the SPARCS 2024 dataset page by page.

    Parameters
    ----------
    query:
        SODA3 query to send to the API.
        Default is SELECT *.

    page_size:
        Number of rows to request per page.
        50,000 is a reasonable maximum page size.

    sleep_seconds:
        Small pause between API requests to avoid sending requests too aggressively.

    max_pages:
        Optional limit for testing.
        Example: max_pages=2 extracts only the first two pages.

    Yields
    ------
    tuple[int, pd.DataFrame]
        Page number and DataFrame for that page.
    """

    while True:
        df = query_sparcs(query, page_number, page_size)

        if df.empty:
            print('No more rows returned. Extraction complete.')
            break
        
        rows_in_page = len(df)
        total_rows += rows_in_page

        yield page_number, df

        if rows_in_page < page_size:
            print('Last page reached. Extraction complete.')
            break
        
        if max_pages is not None and page_number >= max_pages:
            print(f'Stopped after {max_pages} pages(s).')
            break

        page_number += 1
        time.sleep(sleep_seconds)
    