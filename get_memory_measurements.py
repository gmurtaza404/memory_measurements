"""
    Execution flow
        Parse all .trace files in ./traces folder using "run_metric" utility provided in catapult/tracing/bin -> Refer to link https://github.com/catapult-project/catapult
        Parse the .json files to get relevant metrics (Effective sizes) -> Why effective size, refer to link https://chromium.googlesource.com/chromium/src/+/master/docs/memory-infra/README.md under the discussion on effective size vs size

    #TODO Get arbitrary trace folder and get memory stats out of them       
"""
# imports 
import os, time, json
import pandas as pd
from collections import OrderedDict

#initialize folders
try:
    os.mkdir("traces")
    os.mkdir("trace_jsons")
except:
    print("Folders Already Initialized")
else:
    print("Initialized Folders")


path_to_run_metric = "/home/murtaza/Documents/PhD/fine_grained_memory_measurements/catapult/tracing/bin" #Fix this hardcode eventually



# Bad hard code, can we do better? 
# Process level breakdown metrics
process_level_breakdown_metrics = [
    "memory:chrome:all_processes:reported_by_chrome:effective_size",
    "memory:chrome:browser_process:reported_by_chrome:effective_size",
    "memory:chrome:gpu_process:reported_by_chrome:effective_size",
    "memory:chrome:renderer_processes:reported_by_chrome:effective_size"
]

# Components level breakdown metrics
component_level_breakdown_metrics = [
    "memory:chrome:browser_process:reported_by_chrome:cc:effective_size",
    "memory:chrome:browser_process:reported_by_chrome:discardable:effective_size",
    "memory:chrome:browser_process:reported_by_chrome:dom_storage:effective_size",
    "memory:chrome:browser_process:reported_by_chrome:gpu:effective_size",
    "memory:chrome:browser_process:reported_by_chrome:java_heap:effective_size",
    "memory:chrome:browser_process:reported_by_chrome:leveldatabase:effective_size",
    "memory:chrome:browser_process:reported_by_chrome:leveldb:effective_size",
    "memory:chrome:browser_process:reported_by_chrome:malloc:effective_size",
    "memory:chrome:browser_process:reported_by_chrome:net:effective_size",
    "memory:chrome:browser_process:reported_by_chrome:shared_memory:effective_size",
    "memory:chrome:browser_process:reported_by_chrome:skia:effective_size",
    "memory:chrome:browser_process:reported_by_chrome:sqlite:effective_size",
    "memory:chrome:browser_process:reported_by_chrome:tracing:effective_size",
    "memory:chrome:browser_process:reported_by_chrome:ui:effective_size",
    "memory:chrome:gpu_process:reported_by_chrome:gpu:effective_size",
    "memory:chrome:gpu_process:reported_by_chrome:java_heap:effective_size",
    "memory:chrome:gpu_process:reported_by_chrome:malloc:effective_size",
    "memory:chrome:gpu_process:reported_by_chrome:shared_memory:effective_size",
    "memory:chrome:gpu_process:reported_by_chrome:tracing:effective_size",
    "memory:chrome:renderer_processes:reported_by_chrome:blink_gc:effective_size",
    "memory:chrome:renderer_processes:reported_by_chrome:cc:effective_size",
    "memory:chrome:renderer_processes:reported_by_chrome:discardable:effective_size",
    "memory:chrome:renderer_processes:reported_by_chrome:font_caches:effective_size",
    "memory:chrome:renderer_processes:reported_by_chrome:gpu:effective_size",
    "memory:chrome:renderer_processes:reported_by_chrome:java_heap:effective_size",
    "memory:chrome:renderer_processes:reported_by_chrome:malloc:effective_size",
    "memory:chrome:renderer_processes:reported_by_chrome:partition_alloc:effective_size",
    "memory:chrome:renderer_processes:reported_by_chrome:shared_memory:effective_size",
    "memory:chrome:renderer_processes:reported_by_chrome:skia:effective_size",
    "memory:chrome:renderer_processes:reported_by_chrome:tracing:effective_size",
    "memory:chrome:renderer_processes:reported_by_chrome:v8:effective_size",
    "memory:chrome:renderer_processes:reported_by_chrome:web_cache:effective_size"
]

ordered_data_structure = OrderedDict({
    "website" : [],
    "all_processes": [],
    "browser_process": [],
    "gpu_process": [],
    "renderer_processes": [],
    "browser_process_cc": [],
    "browser_process_discardable": [],
    "browser_process_dom_storage": [],
    "browser_process_gpu": [],
    "browser_process_java_heap": [],
    "browser_process_leveldatabase": [],
    "browser_process_leveldb": [],
    "browser_process_malloc": [],
    "browser_process_net": [],
    "browser_process_shared_memory": [],
    "browser_process_skia": [],
    "browser_process_sqlite": [],
    "browser_process_tracing": [],
    "browser_process_ui": [],
    "gpu_process_gpu": [],
    "gpu_process_java_heap": [],
    "gpu_process_malloc": [],
    "gpu_process_shared_memory": [],
    "gpu_process_tracing": [],
    "renderer_processes_blink_gc": [],
    "renderer_processes_cc": [],
    "renderer_processes_discardable": [],
    "renderer_processes_font_caches": [],
    "renderer_processes_gpu": [],
    "renderer_processes_java_heap": [],
    "renderer_processes_malloc": [],
    "renderer_processes_partition_alloc": [],
    "renderer_processes_shared_memory": [],
    "renderer_processes_skia": [],
    "renderer_processes_tracing": [],
    "renderer_processes_v8": [],
    "renderer_processes_web_cache": []
})

def get_metric_value(data_row, metric):
    for element in data_row:
        cur_metric = (list(element.keys())[0])
        if cur_metric == metric:
            return element[cur_metric]
    return 0
   

def make_dataframe(parsed_data, csv_name = "results.csv"):
    for website_data in parsed_data:
        website = list(website_data.keys())[0]
        ordered_data_structure["website"].append(website)
        
        for key in ordered_data_structure.keys():
            if key == "website":
                continue
            ordered_data_structure[key].append(get_metric_value(website_data[website], key))

    data_frame = pd.DataFrame.from_dict(ordered_data_structure)
    data_frame = data_frame[[
    "website"                           ,
    "all_processes"                     ,
    "browser_process"                   ,
    "gpu_process"                       ,
    "renderer_processes"                ,
    "browser_process_cc"                ,
    "browser_process_discardable"       ,
    "browser_process_dom_storage"       ,
    "browser_process_gpu"               ,
    "browser_process_java_heap"         ,
    "browser_process_leveldatabase"     ,
    "browser_process_leveldb"           ,
    "browser_process_malloc"            ,
    "browser_process_net"               ,
    "browser_process_shared_memory"     ,    
    "browser_process_skia"              ,
    "browser_process_sqlite"            ,
    "browser_process_tracing"           ,
    "browser_process_ui"                ,
    "gpu_process_gpu"                   ,
    "gpu_process_java_heap"             ,
    "gpu_process_malloc"                ,
    "gpu_process_shared_memory"         ,
    "gpu_process_tracing"               ,
    "renderer_processes_blink_gc"       ,
    "renderer_processes_cc"             ,
    "renderer_processes_discardable"    ,
    "renderer_processes_font_caches"    ,
    "renderer_processes_gpu"            ,
    "renderer_processes_java_heap"      ,
    "renderer_processes_malloc"         ,
    "renderer_processes_partition_alloc",
    "renderer_processes_shared_memory"  ,
    "renderer_processes_skia"           ,
    "renderer_processes_tracing"        ,
    "renderer_processes_v8"             ,
    "renderer_processes_web_cache"      
    ]]
    data_frame.to_csv(csv_name)


def parse_intermediate_json_file(path_to_json_file):
    webpage_name = path_to_json_file.split("/")[-1].split(".")[0].split("-")[0]
    return_list = []
    with open(path_to_json_file) as f:
        data = json.load(f)
        for chunk in data:
            try:
                if chunk["name"] in process_level_breakdown_metrics:
                    title = chunk["name"].split(":")
                    title = title[2]
                    return_list.append( {title: float(chunk["sampleValues"][0])/(1024*1024)} )
                elif chunk["name"] in component_level_breakdown_metrics:
                    title = chunk["name"].split(":")
                    title = title[2] + "_"  + title[-2]
                    return_list.append( {title: float(chunk["sampleValues"][0])/(1024*1024)} )
            except KeyError:
                a=1
    return {webpage_name: return_list}




def parse_all_intermediate_json_files(path_to_json_files="./trace_jsons"):
    all_json_paths = os.listdir(path_to_json_files)
    all_json_paths = list(map((lambda x: path_to_json_files+'/'+x), all_json_paths))
    all_parsed_results = []
    for json_path in all_json_paths:
        all_parsed_results.append(parse_intermediate_json_file(json_path))
    
    return all_parsed_results

"""
    This functions assumes the url is in format, "http[s]://www.<websitename>.com 
    @params url, Type: String, <website url>
    @returns Type: (String, String) <first element is the website name, second element is url>
"""
def get_website_name(url):
    website_name = url.split("://")[-1].split(".")[1]
    return (website_name, url)


"""
    Parses the website list and which is in format 
                        https://www.<website_1>.com
                        https://www.<website_2>.com
                        .
                        .
                        .
                        https://www.<website_n>.com
                        
    and returns a list which contains url and the name of the website in format
                        [
                            (website_1 ,https://www.<website_1>.com),
                            (website_2 ,https://www.<website_2>.com),
                            .
                            .
                            .
                            (website_n ,https://www.<website_n>.com)
                        ]                     

    @params path_to_website_input_list, Type: String, <path to the website input list, by default its in the same folder with name website_list.txt
    @return Type: [(String,String)] <a list as described above with tuples of website name and url> 

"""
def parse_website_input_list(path_to_website_input_list="website_list.txt"):
    with open(path_to_website_input_list, "r") as f:
        list_of_websites = f.read().split("\n")
        list_of_websites = list(map(get_website_name, list_of_websites))
    return list_of_websites



"""
    This function calls the get_memory_trace.js file by passing CLI arguments (Can I do it in a better way?) and saves a trace file with meminfra information in ./traces folder
    @params website_address, Type: String, <website to execute on the connected android phone> 
    @params website_name, Type: String, <name of the website> 
    @returns None
"""
def get_trace_file(website_address, website_name):
    os.system("node get_memory_trace.js {} {}".format(website_name, website_address))


"""
    This function calls the run_metric routine implemented in catapult/tracing code to convert trace file into an easily parseable json format and stores that file in ./trace_jsons folder
    @params path_to_trace_file, Type: String, <relative path to trace file, absolute path will work as well (Is absolute path prefered?)> 
    @returns None 
"""
def convert_trace2json(path_to_trace_file):
    website_name = path_to_trace_file.split("/")[-1].split(".")[0]
    print(website_name)
    os.system("{}/run_metric {} memoryMetric --filename=result --also-output-json".format(path_to_run_metric, path_to_trace_file))  
    os.system("mv ./result.json ./trace_jsons/{}.json".format(website_name))
    os.system("rm result.html")

"""
    Converts all the trace files in traces folder into json files using covert_trace2json function defined in this file.
    @params path_to_traces Type: String <path of the folder that houses all the trace files>
    @returns None
"""
def convert_all_traces_to_json(path_to_traces="./traces"):
    all_trace_paths = os.listdir(path_to_traces)
    all_trace_paths = list(map( (lambda x: path_to_traces+'/'+x), all_trace_paths))
    for trace_path in all_trace_paths:
        convert_trace2json(trace_path)



def get_memory_traces(list_of_websites):
    for website_name, url in list_of_websites:
        print("Getting trace of {}".format(website_name))
        get_trace_file(url, website_name)
        time.sleep(5)


"""
    Prepares the android phone for measurements, instantiates a new instance of Google Chrome and establishes a link between chrome-remote-interface and the chrome instance running on the phoen.
    @params None
    @returns None
"""
def setup_phone_state():
    print("Setting up phone state!")
    os.system("adb shell am start -n com.android.chrome/com.google.android.apps.chrome.Main")
    time.sleep(5)
    os.system("adb forward tcp:9222 localabstract:chrome_devtools_remote")

"""
    #TODO Not working as of now, need more permissions.
    Kills the chrome process in the connected phone
    @params None
    @returns None
"""
def tear_down_chrome_process():
    os.system("adb shell ps | grep com.android.chrome | awk '{print $2}' | xargs adb shell kill")



"""
    Main function call that binds all the routines together.
"""

def main():
    setup_phone_state()
    time.sleep(10)
    get_memory_traces(parse_website_input_list())
    convert_all_traces_to_json()
    parsed_data=parse_all_intermediate_json_files()
    make_dataframe(parsed_data)
    #tear_down_chrome_process()
    
    #print(parsed_data)

main()
