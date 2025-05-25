# Copyright (c) 2025 Daniella Marbell
#
# This code is licensed under the MIT License.
# See the LICENSE file in the project root for the full license text.

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
        tide_data = pd.read_csv(filename,
                                sep=r'\s+',      # Uses one or more whitespace as separator
                                header=None,    
                                na_values=['N', 'T'], 
                                engine='python', # Robust engine
                                skiprows=11      # Skip initial metadata rows 
                               )

        tide_data['Date'] = pd.to_datetime(tide_data[1] + ' ' + tide_data[2], utc=True)
        tide_data['Sea Level'] = tide_data[3].astype(str).str.replace('M', '', regex=False)
        tide_data['Sea Level'] = pd.to_numeric(tide_data['Sea Level'], errors='coerce') # Convert to float, turn errors into NaN
        
        tide_data = tide_data.drop(columns=[0, 1, 2, 4])   

        tide_data = tide_data.set_index('Date')

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
    
    #Combines two tidal data DataFrames by concatenating them and sorting by index.
    
    combined_data = pd.concat([df1, df2])
    combined_data = combined_data.sort_index()
    if combined_data.index.tz is not None:
        combined_data.index = combined_data.index.tz_localize(None)
        
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
    
    time_numeric = (data.index - data.index[0]).total_seconds() / (3600 * 24)
    sea_level = data['Sea Level'].dropna()
    time_numeric = time_numeric[sea_level.index]
    slope, intercept, r_value, p_value, std_err = scipy.stats.linregress(time_numeric, sea_level)
    slope_mm_per_year = slope * 1000 * 365.25

    return slope_mm_per_year, p_value


def tidal_analysis(data, constituents, start_datetime):
    
    resampled_data = data['Sea Level'].resample('h').mean()
    interpolated_data = resampled_data.interpolate(method='linear')
    cleaned_interpolated_segment = interpolated_data.dropna()
    sea_level = cleaned_interpolated_segment.values.astype(np.float64)
    times_in_seconds = (cleaned_interpolated_segment.index - start_datetime).total_seconds().to_numpy().astype(np.float64)

    print(f"DEBUG: Length of sea_level (x): {len(sea_level)}")
    print(f"DEBUG: Length of times_in_seconds (t): {len(times_in_seconds)}")
    print(f"DEBUG: Type of sea_level: {type(sea_level)}, dtype: {sea_level.dtype}")
    print(f"DEBUG: Type of times_in_seconds: {type(times_in_seconds)}, dtype: {times_in_seconds.dtype}")
    if len(sea_level) > 0:
        print(f"DEBUG: First 5 sea_level values: {sea_level[:5]}")
        print(f"DEBUG: First 5 times_in_seconds values: {times_in_seconds[:5]}")
        # Verify the first time point is approximately zero
        print(f"DEBUG: First time in seconds: {times_in_seconds[0]}")

    # This check is mostly for debugging, as the above steps *should* make them equal
    if len(sea_level) != len(times_in_seconds):
        print("Warning: Length mismatch after cleaning data in tidal_analysis.")
        # Return placeholders if an unexpected mismatch occurs
        return [0.0 for _ in constituents], [0.0 for _ in constituents]
    aberdeen_latitude = 57.1497
    try:
        tide_analysis_result = uptide.harmonic_analysis(
            times_in_seconds,
            sea_level,
            constituents
        )
    except Exception as e:
        print(f"Error during tidal analysis: {e}")
        # For debugging, you might want to return zeros or raise the error
        return [0.0 for _ in constituents], [0.0 for _ in constituents]
    amp = [tide_analysis_result[c][0] for c in constituents]
    pha = [tide_analysis_result[c][1] for c in constituents]

    return amp, pha


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
