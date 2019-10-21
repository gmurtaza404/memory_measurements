"""
    Add all the functions that deal with parsing the website list.
    This file currently contain:
        1. get_website_name
        2. parse_website_input_list
"""

# Imports


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
