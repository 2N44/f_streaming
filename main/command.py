##
#
# functions to manage files and strings
#
##

import os, json, sys


def int2str(n):

	#convert integer betwenn 0 and 60 to '00' string

	if n < 10:

		return '0'+str(n)

	else:

		return str(n)



def sub_time(time_1, time_2):

	#substract time_2 to time_1 in 'hh:mm:ss' format 

	delta_sec = int(time_1[-2:]) - int(time_2[-2:])
	delta_min = int(time_1[3:5]) - int(time_2[3:5])
	delta_h = int(time_1[:2]) - int(time_2[:2])

	if delta_sec < 0:

		delta_sec += 60
		delta_min -= 1

	if delta_min < 0:

		delta_min += 60
		delta_h -=1

	if delta_h < 0:

		return '00:00:00'

	return int2str(delta_h) + ':' + int2str(delta_min) + ':' + int2str(delta_sec)



def add_time(time_1, time_2):

	#add time_1 and time_2 in 'hh:mm:ss' format

	sigma_sec = int(time_1[-2:]) + int(time_2[-2:])
	sigma_min = int(time_1[3:5]) + int(time_2[3:5])
	sigma_h = int(time_1[:2]) + int(time_2[:2])

	if sigma_sec >= 60 :

		sigma_sec -= 60
		sigma_min += 1

	if sigma_min >= 60:

		sigma_min -= 60
		simga_h += 1

	return int2str(sigma_h) + ':' + int2str(sigma_min) + ':' + int2str(sigma_sec)



def convert_time(time):

	#convert time in second to 'hh:mm:ss' format

	time_int = int(time)
	ms = int(1000 * time % 1000)
	hh = time_int // 3600
	mm = time_int % 3600 // 60
	ss = time_int % 3600 % 60

	hms = int2str(hh) + ':' + int2str(mm) + ':' + int2str(ss)

	if ms > 200:

		hms = add_time(hms,'00:00:01')

	return hms



def check_filename(file_name):

	#check and remove if any forbiden character is in the filename*

	char_list = ['<', '>', '\\', '/', '*', '?', '|']

	for char in char_list:

		if char in file_name:

			file_name = file_name.replace(char,'')

	while file_name[-1] == ' ':

		file_name = file_name[:-1]

	return file_name




def pic_path(path, info_doc):

	#return the cover art path

	return os.path.join(path, info_doc['album_path'] + '.' + info_doc['art url'].split('.')[-1])



def pic_format(path):

	#return the format of a pic

	ext = path.split('.')[-1]

	if ext == 'jpg':

		return 'image/jpeg'

	if ext == 'png':

		return 'image/png'



def check_art(path, info_doc):

	#check if cover art file exists

	return os.path.exists(pic_path(path,info_doc))



def read_txt(path):

	#read a txt and put it in a list

	with open(path, 'r') as f:

		data = f.readlines()

	return data



def mkdir_album(path):

	os.makedirs(path, exist_ok=True)



def read_param(path):

	
	with open(path) as f:

		data = json.load(f)

	return data



def file_path():

	#return current file.py path

	if getattr(sys, 'frozen', False):

		# If the application is run as a bundle, the PyInstaller bootloader
		# extends the sys module by a flag frozen=True and sets the app 
		# path into variable _MEIPASS'

		application_path = sys._MEIPASS

	else:

		application_path = os.path.dirname(os.path.abspath(__file__))

	return application_path



def save_param(parameters, path):

	#save parameters in json

	with open(path,'w') as outfile:

		json.dump(parameters, outfile)
		outfile.close()
