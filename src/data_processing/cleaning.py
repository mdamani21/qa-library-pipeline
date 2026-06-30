"""Data cleaning functions for library pipeline.

The cleaning module
This module contains functions for cleaning and standardizing data.
All functions return new DataFrames without modifying the input.
"""

# Uncomment when needed:
# import pandas as pd
# from typing import List, Optional

import logging

logger = logging.getLogger(__name__)


def remove_duplicates(df, subset=None):
    """Remove duplicate rows from DataFrame.

    Args:
        df (pd.DataFrame): Input DataFrame
        subset (list, optional): Columns to consider for duplicates

    Returns:
        pd.DataFrame: DataFrame with duplicates removed

    Example:
        >>> df_clean = remove_duplicates(df, subset=['transaction_id'])
    """
    df = df.copy()  # Work on a copy!

    initial_rows = len(df)
    df = df.drop_duplicates(subset=subset, keep='first')
    removed = initial_rows - len(df)

    if removed > 0:
        print(f"Remove duplicates - Removed {removed} duplicate rows")

        logger.info(f"Removed {removed} duplicate rows")

    return df


def handle_missing_values(df, strategy='drop', fill_value=None, columns=None):
    """Handle missing values in DataFrame.

    Args:
        df (pd.DataFrame): Input DataFrame
        strategy (str): 'drop', 'fill', or 'forward_fill'
        fill_value: Value to fill if strategy='fill'
        columns (list, optional): Specific columns to handle

    Returns:
        pd.DataFrame: DataFrame with missing values handled

    Example:
        >>> df_clean = handle_missing_values(df, strategy='drop')
        >>> df_filled = handle_missing_values(df, strategy='fill', fill_value=0)
    """
    df = df.copy()

    if columns:
        target_cols = columns
    else:
        target_cols = df.columns

    initial_rows = len(df)

    if strategy == 'drop':
        df = df.dropna(subset=target_cols)
        
        print(f"Missing Values - Dropped {initial_rows - len(df)} rows with missing values")
        logger.info(f"Dropped {initial_rows - len(df)} rows with missing values")

    elif strategy == 'fill':
        if fill_value is None:
            raise ValueError("fill_value must be provided when strategy='fill'")
        df[target_cols] = df[target_cols].fillna(fill_value)
        print(f"Missing Values - Filled missing values with {fill_value}")
        logger.info(f"Filled missing values with {fill_value}")

    elif strategy == 'forward_fill':
        df[target_cols] = df[target_cols].ffill()
        print("Missing Values - Forward filled missing values")
        logger.info("Forward filled missing values")

    else:
        raise ValueError(f"Unknown strategy: {strategy}")

    return df


def standardize_dates(df, date_columns, date_format='%Y-%m-%d'):
    """Standardize date columns to consistent format.

    Args:
        df (pd.DataFrame): Input DataFrame
        date_columns (list): Column names containing dates
        date_format (str): Target date format

    Returns:
        pd.DataFrame: DataFrame with standardized dates

    Example:
        >>> df_clean = standardize_dates(df, ['checkout_date', 'return_date'])
    """
    df = df.copy()

    for col in date_columns:
        if col not in df.columns:
            print(f"standardize_dates - Column {col} not found in DataFrame")
            logger.warning(f"Column {col} not found in DataFrame")
            continue

        try:
            df[col] = pd.to_datetime(df[col], errors='coerce')
            print(f"standardize_dates - Standardized dates in column: {col}")
            logger.info(f"Standardized dates in column: {col}")
        except Exception as e:
            print(f"standardize_dates - Error standardizing dates in {col}: {e}")
            logger.error(f"Error standardizing dates in {col}: {e}")
            raise

    return df