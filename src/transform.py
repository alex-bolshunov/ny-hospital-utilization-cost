import pandas as pd
from constants import (
    EXPECTED_VALUES, 
    TEXT_COLUMNS, 
    MORTALITY_RISK_RANKS, 
    ED_SERVICES_MAPPING
)

#ADD DOC COMMENTS TO FUNCTIONS 

def clean_data(
    df: pd.DataFrame,
    filename: str
    ) -> pd.DataFrame:

    #normalize text, remove extra spaces, change empty string to missing value
    for col in TEXT_COLUMNS:
        df[col] = (
            df[col]
            .str.strip()
            .str.replace(r"\s+", " ", regex = True)
            .replace('', pd.NA)
        )
    
    #check for expected values
    for col in EXPECTED_VALUES:
        actual_values = set(df[col].dropna().unique())
        expected_values = EXPECTED_VALUES[col]

        unexpected_values = actual_values - expected_values

        if unexpected_values:
                raise ValueError(f"Unexpected values detected in '{filename}': col: {col}, value:{unexpected_values}")
    
     #preserve the original data, update datatype
    df["length_of_stay_120_plus_flag"] = df["length_of_stay"].eq("120+")
    df["length_of_stay"] = df["length_of_stay"].replace("120+", "120").astype("Int64")

    #change data types of charges and costs
    cols = ["total_charges", "total_costs"]
    df[cols] = df[cols].apply(pd.to_numeric, errors="raise")

    #change datatype apr_severity_of_illness_code
    cols = ["apr_severity_of_illness_code", "discharge_year"]
    df[cols] = df[cols].astype("Int64")

    #add has ccsr procedure column
    df["has_ccsr_procedure"] = df["ccsr_procedure_description"].notna()

    #add mortality risk rank
    df["mortality_risk_rank"] = df["apr_risk_of_mortality"].map(MORTALITY_RISK_RANKS)

    #add has ed services 
    df["has_ed_services"] = df["emergency_department_indicator"].map(ED_SERVICES_MAPPING)

    return df


def get_duplicate_raws(
    df: pd.DataFrame,
    keep = False
    ) -> pd.DataFrame:

    #copy and sort duplicated rows into a separate dataframe
    df_duplicates = df[df.duplicated(keep=keep)].copy().sort_values(by = df.columns.tolist(), na_position="first").reset_index(drop=True)

    return df_duplicates