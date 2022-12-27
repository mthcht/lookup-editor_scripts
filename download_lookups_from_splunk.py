#!/usr/bin/env python3
# coding: utf-8
# Simple python script using Splunk lookup-editor https://splunkbase.splunk.com/app/1724 rest endpoint to download lookups, can be used by automation processes (wokring on splunk cloud)

import requests
import csv
import logging
from requests.packages.urllib3.exceptions import InsecureRequestWarning
import time 
import argparse
import sys
import pathlib

# Disable warning for insecure requests
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

# Setup logging
logging.basicConfig(level=logging.INFO)

# Methods
parser = argparse.ArgumentParser(description="Script download_lookups_from_splunk.py: download multiple lookups from Splunk, can be used for automation processes")
parser.add_argument("-app", "--app", help="Specify the Splunk application, default to 'search' app")
parser.add_argument("-f", "--folder", help="Folder path to save the lookups, default to same directory")
parser.add_argument("-l", "--lookups", nargs='+', help="Enter the name of the lookup(s) to download")
args = parser.parse_args()

# Check the arguments
if len(sys.argv)==1:
    # display help message when no args are passed.
    parser.print_help()
    print("example usages:\n./download_lookups_from_splunk.py\n./download_lookups_from_splunk.py -app search -l Subnet_Scan_Exclusion_List.csv Port_Scan_Exclusion_List.csv\n\
./download_lookups_from_splunk.py -app search -f \"/home/mthcht/lookups/\" -l Subnet_Scan_Exclusion_List.csv Port_Scan_Exclusion_List.csv IOC_List.csv\n")
    logging.warning("warning: no arguments given to the script, will use default values declared in the script:")
    

# Declare variables (change them) 
splunk_management_protocol = "https" # http or https
splunk_management_dest = "FIXME" #example: myserver.local or 127.0.0.1
splunk_management_port = "FIXME" #example default: 8089
splunk_management_service = "/services/data/lookup_edit/lookup_contents"
if args.app:
    splunk_app = args.app #splunk app name, example: search
else:
    splunk_app = "search" #splunk app default name, example: search
splunk_username = "FIXME" #splunk user with needed permissions
splunk_password = "FIXME" #splunk user password (i know..)
if args.folder:
    lookup_folder = args.folder #folder path, it will contain all the lookups you want to download example (do not forget to put the / or \ at the end of the path and escape the \ for windows path) : "C:\\lookups\\" or "/home/mthcht/lookups/"
else:
    lookup_folder = pathlib.Path().absolute() #If no folder path, use default current directory of the script
lookup_type = "csv"
date = time.time()
if args.lookups:
    lookup_file_names_list=args.lookups
    logging.info("list of lookups to download: {}".format(lookup_file_names_list))
else:
    lookup_file_names_list = ["geo_attr_countries.csv","geo_attr_us_states.csv"] # change these values with the lookup(s) you want to download automatically without giving the -l argument
    
# download lookups from Splunk
for lookup_file_name in lookup_file_names_list:
    # Send GET request to Splunk server
    try:
        r = requests.get("{}://{}:{}{}?lookup_type={}&namespace={}&lookup_file={}".format(
            splunk_management_protocol,splunk_management_dest,splunk_management_port,splunk_management_service,lookup_type,splunk_app,lookup_file_name),
            verify=False,
            auth=(splunk_username, splunk_password)
        )
    except Exception as e:
        logging.error("Error sending request to Splunk server: {}".format(e))

    if r.status_code == 200:
        logging.info("[success] file: \'{}\' in {} app has been downloaded from Lookup editor handler {} and will be saved in {}".format(lookup_file_name,splunk_app,r.url,lookup_folder))
        lookup_content_json_backup = r.json()
        # save the file downloaded
        try:
            lookup_file_name_downloaded = "{}_{}.csv".format(lookup_file_name.split('.csv')[0],date)
            with open("{}/{}".format(lookup_folder,lookup_file_name_downloaded), 'w', newline='') as myfile:
                wr = csv.writer(myfile)
                for row in lookup_content_json_backup:
                    wr.writerow(row)
                myfile.close
                logging.info("[sucess] File {} saved in folder {}".format(lookup_file_name,lookup_folder))
        except Exception as e:
            logging.error("[failed] Error: Cannot save a a backup of the file {} in {}, reason: {}".format(lookup_file_name,lookup_folder,e))
    else:
        logging.error("[failed] Error: Downloading file: \'{}\', status:{}, reason:{}, url:{}".format(lookup_file_name,r.status_code,r.reason,r.url))
