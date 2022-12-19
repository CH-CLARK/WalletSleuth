#Generic Imports
import sys
import os
import json
import csv
import pathlib

#CCL Imports
import ccl_chrome_ldb_scripts.ccl_leveldb

maxInt = sys.maxsize

while True:
    # decrease the maxInt value by factor 10 
    # as long as the OverflowError occurs.
    try:
        csv.field_size_limit(maxInt)
        break
    except OverflowError:
        maxInt = int(maxInt/10)

ENCODING = "iso-8859-1"

def phantom_chrome_dump(ask_dir, output_dir):
    chrome_user_data = ask_dir + "/Local/Google/Chrome/User Data"

    folders_list = os.listdir(chrome_user_data)

    #Checking profiles locations
    profiles_check  = "Profile"
    profiles_list = [idx for idx in folders_list if idx.lower().startswith(profiles_check.lower())]
    profiles_list_len = len(profiles_list)

    #Checking default location
    default_check = "Default"
    default_list = [idx for idx in folders_list if idx.lower().startswith(default_check.lower())]

    output_path = ask_dir + r"\BK_phantom_LDB.csv"

    phantom_chrome_output = []

    if profiles_list:
        print('do profiles')



    if default_list:
        print("do default")