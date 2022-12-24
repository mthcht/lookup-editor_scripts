#!/usr/bin/env python3
# coding: utf-8

# Simple python script using Splunk lookup-editor https://splunkbase.splunk.com/app/1724 rest endpoint to upload lookups

import json
import requests
import csv
import re
import logging
import pathlib
from requests.packages.urllib3.exceptions import InsecureRequestWarning

# Disable warning for insecure requests
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

# Setup logging
logging.basicConfig(level=logging.INFO)

# Declare variables (change them) 
splunk_management_protocol = "https" # http or https
splunk_management_dest = "FIXME" #example: myserver.local or 127.0.0.1
splunk_management_port = "FIXME" #example default: 8089

# GET requests to this endpoint will execute get_lookup_contents() and POST requests to this endpoint will execute post_lookup_contents() from the lookup_editor_rest_handler.py in the lookup-editor app
splunk_management_service = "/services/data/lookup_edit/lookup_contents" #endpoint lookup-editor 

splunk_app = "search" #splunk app name, example: search
splunk_username = "FIXME" #splunk user with needed permissions
splunk_password = "FIXME" #splunk user password (i know..)
lookup_folder = "FIXME" #folder path which contains all the lookups you want to upload example: "C:\\lookups\" or "/home/mthcht/lookups/"


for lookup_file in pathlib.Path(lookup_folder).iterdir():
    lookup_name = pathlib.Path(lookup_file).name
    lookup_name = str(lookup_name.replace(" ","_"))

    # Read data from CSV file
    lookup_content = []
    try:
        with open(lookup_file, encoding='utf-8', errors='ignore',newline='') as f:
            reader = csv.reader(f, delimiter=',')
            for row in reader:
                lookup_content.append(row)
    except  Exception as e:
        logging.error("Error reading {} : {}".format(lookup_file,e))

    # Send POST request to Splunk server
    try:
        r = requests.post("{}://{}:{}{}".format(splunk_management_protocol,splunk_management_dest,splunk_management_port,splunk_management_service) ,
            verify=False,
            auth=(splunk_username, splunk_password),
            data={"output_mode": "json",
                "namespace": splunk_app,
                "lookup_file": lookup_name,
                "contents": json.dumps(lookup_content)},
            timeout=60
        )
        if r.status_code == 200:
            logging.info("[success] file: \'{}\' uploaded to Lookup editor handler {} and saved in splunk app \'{}\'".format(lookup_name,r.url,splunk_app))
        else:
            logging.error("[failed] file: \'{}\', status:{}, reason:{}, url:{}".format(lookup_name,r.status_code,r.reason,r.url))
    except Exception as e:
        logging.error("Error sending request to Splunk server: {}".format(e))
