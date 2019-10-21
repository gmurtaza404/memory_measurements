"""
    Execution flow
        Parse all .trace files in ./traces folder using "run_metric" utility provided in catapult/tracing/bin -> Refer to link https://github.com/catapult-project/catapult
        Parse the .json files to get relevant metrics (Effective sizes) -> Why effective size, refer to link https://chromium.googlesource.com/chromium/src/+/master/docs/memory-infra/README.md under the discussion on effective size vs size

    #TODO Get arbitrary trace folder and get memory stats out of them       
"""
# imports 
import os, time, json, time
import pandas as pd
from collections import OrderedDict
from src import phone_state, folder_state, weblist_manip, parsing

import subprocess

"""
    This function calls the get_memory_trace.js file by passing CLI arguments (Can I do it in a better way?) and saves a trace file with meminfra information in ./traces folder
    @params website_address, Type: String, <website to execute on the connected android phone> 
    @params website_name, Type: String, <name of the website> 
    @returns None
"""
def get_trace_file(website_address, website_name, device_name):
    try:
        cmd = ["node", "get_memory_trace.js", website_name+str(time.time()), website_address, device_name]
        subprocess.call(cmd, timeout = 60)
    except Exception as e:
        print("Page load process timed out for website {}".format(website_name), e)
        

def get_memory_traces(list_of_websites, device_name):
    for website_name, url in list_of_websites:
        print("Getting trace of {}".format(website_name))
        get_trace_file(url, website_name, device_name)
        time.sleep(5)



"""
    Main function call that binds all the routines together.
"""

def main():
    # Folder Setup
    folder_state.make_required_folders()
    folder_state.clean_folders()

    # Phone Setup
    adb_id, device_name = phone_state.get_current_connected_phone()
    phone_state.setup_phone_state(adb_id)

    # Parse Website List
    websites = weblist_manip.parse_website_input_list()

    # Get Memory Trace Files
    get_memory_traces(websites, device_name)

    
    # Convert Trace files to a parsable JSON format 
    parsing.convert_all_traces_to_json()
    
    
    # Parse the JSON files to get required metrics
    parsed_data = parsing.parse_all_intermediate_json_files()
    
    # Clumping them up in a CSV file
    parsing.make_dataframe(parsed_data)
    
main()
