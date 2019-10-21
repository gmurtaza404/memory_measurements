#initialize 
import os

"""
    Makes or Validates that required folders exist
"""
def make_required_folders():
    try:
        os.mkdir("traces")
        os.mkdir("trace_jsons")
        os.mkdir("archive")
    except:
        print("Folders Already Initialized")
    else:
        print("Initialized Folders")


"""
    Deletes all the files inside the traces and trace_jsons folder
"""

def clean_folders():
    os.system("rm traces/*")
    os.system("rm trace_jsons/*")
    os.system("rm results.csv")