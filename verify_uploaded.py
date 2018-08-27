import requests
import os
import re


def get_user_input(user_input):
    """Reads in user folder name and build directory name"""
    directory_name = "Y:/RWC/Melissa/Projects/Promos/" + user_input + "/final"
    return directory_name


def get_directory_files():
    """get all files from the directory that the user selected"""
    directory = get_user_input(user_input)
    arr_of_files = os.listdir(directory)
    return arr_of_files


def tpb_url_builder():
    """Construct url for TPB request based on assets location"""
    tpb_home_links = ['HP', '1UP', 'Overlay', 'SMB', 'hero']

    files_w_location = []
    files_to_check = file_handler()

    for file in files_to_check:
        # if contains subnav add /subnav
        if re.search('subnav', file):
            tp_file_1 = '/subnav/' + file
            files_w_location.append(tp_file_1)

        # if contains HP and m add /home/mobile
        elif re.search(r'(_HP_)+.*(_m_)+', file):
            tp_file_2 = '/home/mobile/' + file
            files_w_location.append(tp_file_2)

        # if contains HP,hero, 1UP SMB add /home
        elif any(x in file for x in tpb_home_links) and not re.search('_m_', file):
            tp_file_3 = '/home/' + file
            files_w_location.append(tp_file_3)

        # if contains SO add /sales
        elif re.search(r'SO', file):
            tp_file_4 = '/sales/' + file
            files_w_location.append(tp_file_4)

        # if contains TMB or CAT add /store
        elif re.search(r'(_TMB_)+.*|(_CAT_)+', file):
            tp_file_5 = '/store/' + file
            files_w_location.append(tp_file_5)

    return files_w_location


def tws_url_builder():
    """Construct url for TPB request based on assets location"""
    tpb_home_links = ['HP', '1UP', 'Overlay', 'SMB', 'hero']
    files_w_location = []
    files_to_check = file_handler()

    for file in files_to_check:

        # if contains HP and m add /home/mobile
        if re.search(r'(_HP_)+.*(_m_)+', file):
            tws_file_1 = '/home/mobile/' + file
            files_w_location.append(tws_file_1)

        # if contains HP,hero, 1UP SMB add /home
        elif any(x in file for x in tpb_home_links) and not re.search('_m_', file):
            tp_file_3 = '/home/' + file
            files_w_location.append(tp_file_3)

        # mobile assests other than HP
        elif re.search(r'_m_', file) and not re.search('_HP_', file):
            tws_file_1 = '/mobile/' + file
            files_w_location.append(tws_file_1)

        # everything else
        else:
            tp_file_5 = '/store/' + file
            files_w_location.append(tp_file_5)

    return files_w_location
#not working
def sfly_url_builder():

    sfly_home_links = ['HP', '1UP', 'Overlay', 'SMB', 'hero']
    files_w_location = []
    files_to_check = file_handler()

    for file in files_to_check:
        if re.search(r'(_HP_)+.*(_m_)+', file):
            sfly_file_1 = '/mobile/' + file
            files_w_location.append(sfly_file_1)

        # mobile assests other than HP
        elif re.search(r'_m_', file) and not re.search('_HP_', file):
            sfly_file_3 = '/mobile/sales/' + file
            files_w_location.append(sfly_file_3)

        elif re.search(r'SO', file):
            sfly_file_4 = '/sales/' + file
            files_w_location.append(sfly_file_4)
 
        elif re.search(r'(_TMB_)+.*|(_CAT_)+', file):
            sfly_file_5 = '/store/' + file
            files_w_location.append(sfly_file_5)

        # if contains HP,hero, 1UP SMB add /home
        elif any(x in file for x in sfly_home_links) and not re.search('_m_', file):
            sfly_file_2 = '/home/' + file
            files_w_location.append(sfly_file_2)

    return files_w_location


def filter_directory_by_type():
    """Filter directory based whether it's a SFLY, TinyPrints or TWS asset"""
    directory = get_user_input(user_input)
    if re.search('TWS', directory):
        tws_files_final = []
        url_start = "/tws"
        files_to_add_path = tws_url_builder()
        for file in files_to_add_path:
            final_file = url_start + file
            tws_files_final.append(final_file)
        return tws_files_final

    elif re.search('TPB', directory):
        tpb_files_final = []
        url_start = "/tp"
        files_to_add_path = tpb_url_builder()
        for file in files_to_add_path:
            final_file = url_start + file
            tpb_files_final.append(final_file)
        return tpb_files_final

    else:
        sfly_files_final = []
        url_start = "/sfly"
        files_to_add_path = sfly_url_builder()
        for file in files_to_add_path:
            final_file = url_start + file
            sfly_files_final.append(final_file)
        return sfly_files_final

def file_handler():
    """Iterate through files and filter out jpegs"""
    filtered_files = []
    files = get_directory_files()
    for file in files:
        if file.endswith('.png') or file.endswith('.jpg'):
            filtered_files.append(file)
    return filtered_files


def make_request():
    """Retrieve files in directory and check status """
    requested_files = {}
    final_files = filter_directory_by_type()
    image_url = 'http://cdn-image.staticsfly.com/i'
    for file in final_files:
        url_to_check = image_url + file
        r = requests.get(url_to_check)
        if r.status_code == 200:
            if "found" not in requested_files:
                requested_files["found"] = [url_to_check]
            else:
                requested_files["found"].append(url_to_check)
        if r.status_code == 404:
            if "not found" not in requested_files:
                requested_files["not found"] = [url_to_check]
            else:
                requested_files["not found"].append(url_to_check)
    return requested_files


def print_requested_files(request_key):
    """ Print out all files that are requested with total files and if was success"""
    requested_files = make_request()
    if request_key == "found":
        try:
            files_found = len(requested_files[request_key])
            print('{} files found'.format(files_found))
            for key, value in requested_files.items():
                for x in value:
                    print(x)
            return 0
        except KeyError:
            print("no files found from that folder")
    if request_key == "not found":
        try:
            files_found = len(requested_files[request_key])
            print("{} files not found, check the image path " .format(files_found))
            for key, value in requested_files.items():
                for x in value:
                    print(x)
            return 0
        except KeyError:
            print("all files were found")
 


user_input = input("Copy in the folder name:")
get_user_input(user_input)
print_requested_files("found")
print_requested_files("not found")
