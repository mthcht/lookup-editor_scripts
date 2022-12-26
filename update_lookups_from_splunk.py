#!/usr/bin/env python3
# coding: utf-8
# Simple python script using Splunk lookup-editor https://splunkbase.splunk.com/app/1724 rest endpoint to update lookups, can be used by automation processes

import json
import requests
import csv
import logging
from requests.packages.urllib3.exceptions import InsecureRequestWarning
import time 
import argparse
import sys

# Disable warning for insecure requests
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

# Setup logging
logging.basicConfig(level=logging.INFO)

# Methods
parser = argparse.ArgumentParser(description="Script upload_lookups_from_splunk.py: Update one or multiple lookups on Splunk, can be used for automation processes")
parser.add_argument("-i", "--ask_input", help="Ask the user the input for each line to add",action="store_true")
parser.add_argument("-p", "--paste_csv_data", help="Paste the values in this format (line separated by \\n):\nfield1,field2,field3 ...\n,value2,value3 ...\nvalue4,,value5 ...\nvalue6,, ...\n",action="store_true")
parser.add_argument("-f", "--csv_file", help="give the full path of a csv files to merge with the lookups (separated by comma)")
parser.add_argument("-l", "--lookups", nargs='+', help="Enter the name of the lookup(s) to update (don't forget the .csv), if the argument is not given, will take the default list declared in the script")
args = parser.parse_args()

# Check the arguments
if args.csv_file and args.paste_csv_data:
    logging.error("Error: you can't use -f and -p as arguments at the same time, please use only one of them.")
    parser.print_help()
    sys.exit(1)
elif args.ask_input and args.paste_csv_data:
    logging.error("Error: you can't use -i and -p as arguments at the same time, please use only one of them.")
    parser.print_help()
    sys.exit(1)
elif args.ask_input and args.csv_file:
    logging.error("Error, you can't use -i and -f as arguments at the same time, please use only one of them.")
    parser.print_help()
    sys.exit(1)
if len(sys.argv)==1:
    # display help message when no args are passed.
    parser.print_help()
    print("example usages:\n./update_lookups_from_splunk.py -i -l Subnet_Scan_Exclusion_List.csv Port_Scan_Exclusion_List.csv\n./update_lookups_from_splunk.py -p -l Subnet_Scan_Exclusion_List.csv Port_Scan_Exclusion_List.csv\n\
./update_lookups_from_splunk.py -i\n./update_lookups_from_splunk.py -p\n./update_lookups_from_splunk.py -f\n\
./update_lookups_from_splunk.py -i -l Attackers_List_IOC.csv IPS_Detections_Exclusion_List.csv\n./update_lookups_from_splunk.py -p -l Attackers_List_IOC.csv\n\
./update_lookups_from_splunk.py' -f \"C:\\Users\\mthcht\\Documents\\mylist.csv\" -l Port_Scan_Exclusion_List.csv\n\
./update_lookups_from_splunk.py' -f \"/home/mthcht/IOC_list.csv\" -l MISP_IOC_list.csv Attackers_List_IOC.csv")
    logging.error("Error: you must choose a method, either -i, -p or -f")
    sys.exit(1)
if args.ask_input is None and args.paste_csv_data is None and args.csv_file is None:
    parser.print_help()
    logging.error("Error: you choose a method, use method -i, -p or -f")
    sys.exit(1)

# Declare variables (change them) 
splunk_management_protocol = "https" # http or https
splunk_management_dest = "FIXME" #example: myserver.local or 127.0.0.1
splunk_management_port = "FIXME" #example default: 8089
splunk_management_service = "/services/data/lookup_edit/lookup_contents"
splunk_app = "search" #splunk app name, example: search
splunk_username = "FIXME" #splunk user with needed permissions
splunk_password = "FIXME" #splunk user password (i know..)
lookup_folder = "FIXME" #folder path which contains all the lookups you want to upload example (do not forget to put the / or \ at the end of the path) : "C:\\lookups\" or "/home/mthcht/lookups/"
lookup_type = "csv"
date = time.time()
if args.lookups:
    lookup_file_names_list=args.lookups
     logging.info("list of lookups to update: {}".format(lookup_file_names_list))
else:
    lookup_file_names_list = ["test.csv"] # change this value with the lookup(s) you want to update automatically without giving the -l argument


def create_dict_field_values_list():
    field_values_list = []
    num_dict = int(input("How many exclusions or inclusions do you want to create in the lookup ?: "))
    for i in range(num_dict):
        fields = input("Enter the fields for the exclusion/inclusion separated by comma (example: src_ip,dest_ip,metadata) {}: ".format(i+1))
        values = input("Enter the values for the exclusion/inclusion separated by comma (example: 192.168.1.1,192.168.1.2,mthcht test) {}: ".format(i+1))
        dictionary = dict(zip(fields.split(','), values.split(',')))
        field_values_list.append(dictionary)
    return field_values_list

def create_dict_field_values_list_from_text():
    print("Paste the values in this format (line separated by \\n):\n\nfield1,field2,field3 ...\n,value2,value3 ...\nvalue4,,value5 ...\nvalue6,, ...\n\n:")
    field_values_list = []
    field_names = None
    while True:
        data = input("line (or type 'ok' to confirm the list) : ")
        if data == 'ok':
            break
        elif not field_names:
            field_names = data.split(',')
        else:
            dict_ = {}
            for i, item in enumerate(data.split(',')):
                dict_[field_names[i]] = item
            field_values_list.append(dict_)
    return field_values_list

def create_dict_field_values_list_from_csv(file_path_csv_input):
    field_names = []
    field_values_list = []
    with open(file_path_csv_input, 'r') as csvfile:
        content = csvfile.readlines()
        for i, line in enumerate(content):
            if i == 0:
                field_names = line.strip().split(',')
            else:
                data = line.strip()
                if data:
                    dict_ = {}
                    for j, item in enumerate(data.split(',')):
                        dict_[field_names[j]] = item
                    field_values_list.append(dict_)
    return field_values_list

# create new inclusions/exclusions lists in field_values_list
if (args.ask_input):
    field_values_list = create_dict_field_values_list()
if (args.paste_csv_data):
    field_values_list = create_dict_field_values_list_from_text()
if (args.csv_file):
    field_values_list = create_dict_field_values_list_from_csv(args.csv_file)
    
# Update lookups on Splunk
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
        logging.info("[success] file: \'{}\' in {} app has been downloaded from Lookup editor handler {} and saved in {}".format(lookup_file_name,splunk_app,r.url,lookup_folder))
        lookup_content_json_backup = r.json()
        # save the file downloaded
        try:
            old_lookup_file_name = "{}_{}.csv".format(lookup_file_name.split('.csv')[0],date)
            with open("{}{}".format(lookup_folder,old_lookup_file_name), 'w', newline='') as myfile:
                wr = csv.writer(myfile)
                for row in lookup_content_json_backup:
                    wr.writerow(row)
                myfile.close
                logging.info("[sucess] Backup of the File {} saved in folder {}".format(lookup_file_name,lookup_folder))
        except Exception as e:
            logging.error("[failed] Error: Cannot save a a backup of the file {} in {}, reason: {}".format(lookup_file_name,lookup_folder,e))
        lookup_content_json = r.json()
        lookup_file_name_path = "{}{}".format(lookup_folder,lookup_file_name)
        for field_values_dict in field_values_list:
            for key, value in field_values_dict.items():
                logging.info("Adding Key: {}, Value: {} from {} to the lookup {}".format(key, value,field_values_dict,lookup_file_name))
                try:
                    myfield_index = lookup_content_json[0].index(key)
                except ValueError as e:
                    logging.warning("Warning: {}. adding {} to the columns list for the file {}".format(e,key,lookup_file_name))
                    lookup_content_json[0].append(key)
                    for row in lookup_content_json[1:]:
                        row.append('')
                    if 'new_row' in locals():
                        new_row.append('')
                    myfield_index = lookup_content_json[0].index(key)
                if myfield_index >= 0:
                    if 'new_row' not in locals():
                        new_row = [''] * len(lookup_content_json[0])
                    new_row[myfield_index] = value
                else:
                    logging.error("[failed] Error: cannot add {}:{} to the lookup {}, problem defining 'myfield_index' , trace: myfield_index='{}', field_values_dict='{}'".format(key,value,lookup_file_name,myfield_index,field_values_dict))
            try:
                if 'new_row' in locals():
                    lookup_content_json.append(new_row)
                    logging.info("new row '{}' has been added to the lookup content of the file {}".format(new_row,lookup_file_name))
            except Exception as e:
                logging.error("[failed] Error: cannot add row '{}' to the lookup {}, trace: myfield_index='{}', field_values_dict='{}'".format(new_row,lookup_file_name,myfield_index,field_values_dict))
            del new_row

        # Save a backup of the new file and delete duplicates rows
        try:
            lookup_content_json_new = []
            for row in lookup_content_json:
                if row not in lookup_content_json_new:
                    lookup_content_json_new.append(row)
            new_lookup_file_name = "{}{}_updated_{}.csv".format(lookup_folder,lookup_file_name,date)
            with open(new_lookup_file_name, 'w', newline='') as myfile:
                wr = csv.writer(myfile)
                for row in lookup_content_json_new:
                    wr.writerow(row)
                myfile.close
                logging.info("[sucess] Removed duplicated rows and saved as the new file {} in folder {} as {}".format(lookup_file_name,lookup_folder,new_lookup_file_name))
        except Exception as e:
            logging.error("[failed] Error: Cannot save the new file {} in {} as {}, reason: {}".format(lookup_file_name,lookup_folder,new_lookup_file_name,e))
        
        # Sent the new lookup to Splunk
        try:
            r = requests.post("{}://{}:{}{}".format(splunk_management_protocol,splunk_management_dest,splunk_management_port,splunk_management_service),
                verify=False,
                auth=(splunk_username, splunk_password),
                data={"output_mode": "json",
                    "namespace": splunk_app,
                    "lookup_file": lookup_file_name,
                    "contents": json.dumps(lookup_content_json_new)},
                timeout=60
            )
            if r.status_code == 200:
                logging.info("[success] file: \'{}\' updated and uploaded to Lookup editor handler {} and saved in splunk app \'{}\'".format(lookup_file_name,r.url,splunk_app))
            else:
                logging.error("[failed] Error: file: \'{}\', status:{}, reason:{}, url:{}".format(lookup_file_name,r.status_code,r.reason,r.url))
        except Exception as e:
            logging.error("[failed] Error: Sending updated file {} to Splunk server, reason: {}".format(lookup_file_name,e))
    else:
        logging.error("[failed] Error: Downloading file: \'{}\', status:{}, reason:{}, url:{}".format(lookup_file_name,r.status_code,r.reason,r.url))
