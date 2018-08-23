import requests
import os
import re


def get_user_input(user_input):
	"""Reads in user folder name and build directory name"""
	directory_name = "Y:/RWC/Melissa/Projects/Promos/"+user_input+"/final"
	return directory_name

def get_directory_files():
	"""get all files from the directory that the user selected"""
	directory = get_user_input(user_input)
	arr_of_files = os.listdir(directory)
	return arr_of_files


def tpb_url_builder():
	"""Construct url for request based on assets location"""
	tpb_home_links = ['1UP','Overlay','SMB']

	files_w_location = []
	files_to_check = file_handler()

	for file in files_to_check:
	# if contains subnav add /subnav
		if re.search('subnav',file):
			tp_file_1 = '/subnav/'+file
			files_w_location.append(tp_file_1)
	#if contains HP and m add /home/mobile
		if re.search('(HP)(m)',file):
			print (file)
	#if contains HP,hero, 1UP SMB add /home
		if any(x in file for x in tpb_home_links):
			tp_file = '/home/'+file
			files_w_location.append(tp_file)
		else:
			print('nope')
	
	#if contains SO add /sales
	#if contains TMB or CAT add /store
	return files_w_location
	
	

def filter_directory_by_type():
	"""Filter directory based whether it's a SFLY, TinyPrints or TWS asset"""
	directory = get_user_input(user_input)
	if re.search('TPB',directory):
		tpb_files_final = []
		url_start = "/tp"
		files_to_add_path = tpb_url_builder()
		for file in files_to_add_path:
			final_file = url_start + file
			tpb_files_final.append(final_file)
		return tpb_files_final
	if re.search('TWS',directory):
		print('Wedding shop')
		
	else:
		print('Shutterfly')
	

def file_handler():
	"""Iterate through files and filter out jpegs"""
	filtered_files = []
	files = get_directory_files()
	for file in files:
		if file.endswith('.png') or file.endswith('.jpg') :
			filtered_files.append(file)
	return filtered_files

def make_request():
	final_files = filter_directory_by_type()
	image_url = 'http://cdn-image.staticsfly.com/i/'
	for file in final_files:
		 url_to_check = image_url + file
		 # r = requests.get(url_to_check)
		 # print (r.status_code)

user_input = input("Copy in the folder name:")
get_user_input(user_input)
print(tpb_url_builder())
# print(make_request())