#Generic Imports
import sys
import os
import json
import csv
import pathlib

def bravebrowser_dump(ask_dir, output_dir):
    bravebrowser_userdata = ask_dir + "/Local/BraveSoftware/Brave-Browser/User Data"

    folders_list = os.listdir(bravebrowser_userdata)

    #checking for profile locations
    profiles_check  = "Profile"
    profiles_list = [idx for idx in folders_list if idx.lower().startswith(profiles_check.lower())]
    profiles_list_len = len(profiles_list)

    #checking for default location
    default_check = "Default"
    default_list = [idx for idx in folders_list if idx.lower().startswith(default_check.lower())]

    bravebrowser_output = []

    if default_list:
        print("DO DEFAULT LOCATION")

    if profiles_list:
        print("DO PROFILES LOCATIONS")
    