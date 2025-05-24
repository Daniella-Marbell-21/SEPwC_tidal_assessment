#!/usr/bin/env python3

# import the modules you need here
# i am suppose to make a dataframe that has columns of time, date and Sea level,
#float integers for Sea level, with at least one value missing
import os
import datetime
import numpy as np
import pandas as pd
import argparse

tidal_file = "data/1947ABE.txt"

def read_tidal_data(filename):
    if not os.path.exists(filename):                          #ErrorHandling
        print("Not able to read tidal data yet.")
        return
    with open(filename, "r", encoding="utf-8") as file:       #Open file to read
        tidal_data = file.readlines()
        
#Parse string so python can understand
        
    date_string = "1947-1-1-0"                              
    date_object = datetime.datetime.strptime(date_string, "%Y-%m-%d-%H")
    print(date_object)
        
#make dataframe    
    string = "sea_level"                                       #
    dates = pd.date_range("19470101", periods=8760, freq='h')
    dates
    df = pd.DataFrame(np.random.randn(8760, 1), index=dates, columns=["Sea_level"])
    df
    return 0
    
def extract_single_year_remove_mean(year, data):
   

    return 


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
    


