
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


def read_tidal_data(filename):
    tide_data = pd.read_txt(filename, header=None)
    tide_data['Date'] = pd.to_datetime(dict(year=tide_data[0], month=tide_data[1], day=tide_data[2], hour=tide_data[3]))
    # col 0 is year, col 1 is month, col2 is day, col3 hour
    tide_data = tide_data.drop([0,1,2,3], axis = 1)
    tide_data = tide_data.rename(columns={4: "Tide"})
    tide_data = tide_data.set_index('Date')
    tide_data = tide_data.mask(tide_data['Tide'] < -300)
    return tide_data
    

    filename = "C:/Users/marbd/SEPwC/SEPwC_summative/SEPwC_tidal_assessment/data/1947ABE.txt"


    for url in urls:
        file_name = os.path.basename(url) # get the full path to the file
        if os.path.exists(file_name):
                os.remove(file_name) # if exists, remove it directly
        file_name = wget.download(url, out=".")






  

def extract_single_year_remove_mean(year, data):
    year_string_start = str(year)+"0101"
    year_string_end = str(year)+"1231"
    year_data = data.loc[year_string_start:year_string_end, ['Tide']]
   # remove mean to oscillate around zero
    mmm = np.mean(year_data['Tide'])
    year_data['Tide'] -= mmm
    

    return year_data


def extract_section_remove_mean(start, end, data):

    return


def join_data(data1, data2):

    return


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
