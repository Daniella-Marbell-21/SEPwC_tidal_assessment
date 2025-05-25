
# import the modules we need
import pandas as pd
import matplotlib.pyplot as plt
import datetime
import wget
import os
import numpy as np
import uptide
import pytz
import math
import argparse
import scipy.stats


def read_tidal_data(filename):
    if not os.path.exists(filename):
        raise FileNotFoundError(f"Tidal data file not found at: '{filename}'")
    try:
        # Read the raw data.
        # na_values will now only apply to exact matches of 'N' or 'T'.
        # The 'M' from '2.1336M' will be handled manually.
        tide_data = pd.read_csv(filename,
                                sep=r'\s+',      # Uses one or more whitespace as separator
                                header=None,     # No header row
                                na_values=['N', 'T'], # 'N' and 'T' are missing values
                                engine='python', # Robust engine
                                skiprows=11      # Skip initial metadata rows
                               )

        # Step 1: Create the 'Date' column by combining original columns 1 and 2
        # tide_data[1] is 'YYYY/MM/DD', tide_data[2] is 'HH:MM:SS'
        tide_data['Date'] = pd.to_datetime(tide_data[1] + ' ' + tide_data[2])

        # Step 2: Extract 'Sea Level' from original column 3
        # It comes as a string (e.g., '2.1336M').
        # First, convert to string type (if not already) and remove the 'M'.
        # Then, convert to numeric, coercing any non-numeric values (like leftover 'N' or 'T' if not caught by na_values) to NaN.
        tide_data['Sea Level'] = tide_data[3].astype(str).str.replace('M', '', regex=False)
        tide_data['Sea Level'] = pd.to_numeric(tide_data['Sea Level'], errors='coerce') # Convert to float, turn errors into NaN

        # Step 3: Drop the original raw columns that are no longer needed
        # Original column 0: the row index (e.g., '1)'). Drop it.
        # Original column 1: date part. Drop it, it's in 'Date'.
        # Original column 2: time part. Drop it, it's in 'Date'.
        # Original column 4: the second data column (e.g., '0.6109M'). Drop it, not 'Sea Level'.
        tide_data = tide_data.drop(columns=[0, 1, 2, 4])

        # Step 4: Set the 'Date' column as the DataFrame's index
        tide_data = tide_data.set_index('Date')

        # Step 5: Apply the mask for values less than -300
        tide_data["Sea Level"] = tide_data["Sea Level"].mask(tide_data["Sea Level"] < -300)

        # The 'Sea Level' column is already float due to pd.to_numeric(errors='coerce')
        # so tide_data['Sea Level'] = tide_data['Sea Level'].astype(float) is redundant.

        return tide_data

    except pd.errors.ParserError as e:
        # This will now hopefully not be triggered if the data format is clean after skiprows.
        raise ValueError(f"Error parsing tidal data from '{filename}'. Check file format. Original error: {e}")
    except Exception as e:
        # This will catch other errors, including the 'Unable to parse string "1)"' if it somehow reoccurs
        # or other issues during data transformation.
        raise ValueError(f"An unexpected error occurred while processing '{filename}': {e}")

def join_data(df1: pd.DataFrame, df2: pd.DataFrame):
    """
    Combines two tidal data DataFrames by concatenating them and sorting by index.
    """
    combined_data = pd.concat([df1, df2])
    combined_data = combined_data.sort_index()
    return combined_data

def extract_single_year_remove_mean(year, data):
    year_string_start = str(year)+"0101"
    year_string_end = str(year)+"1231"
    year_data = data.loc[year_string_start:year_string_end, ['Sea Level']]
   # remove mean to oscillate around zero
    mmm = np.mean(year_data['Sea Level'])
    year_data['Sea Level'] -= mmm
    

    return year_data


def extract_section_remove_mean(start, end, data):

    # Use pandas' convenient slicing with string dates for DatetimeIndex
    section_data = data.loc[start:end, ['Sea Level']]

    # Remove mean to oscillate around zero
    mmm = np.mean(section_data['Sea Level'])
    section_data['Sea Level'] -= mmm

    return section_data

def sea_level_rise(data):

    return


def tidal_analysis(data, constituents, start_datetime):

    return


def get_longest_contiguous_data(data):

    return


if __name__ == '__main__':

    parser = argparse.ArgumentParser(
        prog="UK Tidal analysis",
        description="Calculate tidal constiuents and RSL from tide gauge data",
        epilog="Copyright 2024, Jon Hill"
    )

    parser.add_argument("directory",
                        help="the directory containing txt files with data")
    parser.add_argument('-v', '--verbose',
                        action='store_true',
                        default=False,
                        help="Print progress")

    args = parser.parse_args()
    dirname = args.directory
    verbose = args.verbose
