##
#
#File where every utility fonctions are coded
#
##

import os
import json
import sys
import requests


def int2str(n: int) -> str:

	'''
	convert integer between 0 and 60 to '00' string
	'''

	if n < 10:

		return '0'+str(n)

	else:

		return str(n)


def sub_time(time_1: str, time_2: str) -> str:

	'''
	substract time_2 to time_1 in 'hh:mm:ss' format
	''' 

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

	return (int2str(delta_h)
		+ ':'
		+ int2str(delta_min)
		+ ':'
		+ int2str(delta_sec))


def add_time(time_1: str, time_2: str) -> str:

	'''
	add time_1 and time_2 in 'hh:mm:ss' format
	'''

	sigma_sec = int(time_1[-2:]) + int(time_2[-2:])
	sigma_min = int(time_1[3:5]) + int(time_2[3:5])
	sigma_h = int(time_1[:2]) + int(time_2[:2])

	if sigma_sec >= 60 :

		sigma_sec -= 60
		sigma_min += 1

	if sigma_min >= 60:

		sigma_min -= 60
		simga_h += 1

	return (int2str(sigma_h)
		+ ':'
		+ int2str(sigma_min)
		+ ':'
		+ int2str(sigma_sec))


def convert_time(time: int) -> str:

	'''
	convert time in second to 'hh:mm:ss' format
	'''

	time_int = int(time)
	ms = int(1000 * time % 1000)
	hh = time_int // 3600
	mm = time_int % 3600 // 60
	ss = time_int % 3600 % 60

	hms = int2str(hh) + ':' + int2str(mm) + ':' + int2str(ss)

	if ms > 200:

		hms = add_time(hms,'00:00:01')

	return hms


def check_filename(file_name: str) -> str:

	'''
	check if any forbiden character is in the filename and remove it
	'''

	char_list = ['<', '>', '\\', '/', '*', '?', '|']

	for char in char_list:

		if char in file_name:

			file_name = file_name.replace(char,'')

	while file_name[-1] == ' ':

		file_name = file_name[:-1]

	return file_name


def check_dirname(dir_name: str) -> str:

	'''
	check and remove any forbiden character in the directory name
	(windows friendly)
	'''

	dir_name = check_filename(dir_name)

	if ' : ' in dir_name:

		dir_name = dir_name.replace(' : ', '')

	if ': ' in dir_name:

		dir_name = dir_name.replace(': ', '')

	if ':' in dir_name:

		dir_name = dir_name.replace(':', '')

	return dir_name

def img_from_url(image_url):

	r = requests.get(image_url, stream=True)

 	# Check if the image was retrieved successfully

	if r.status_code == 200 :

		# Set decode_content value to True, otherwise the downloaded image file's size will be zero.

		r.raw.decode_content = True
		return r.raw

	else:

		print('Image Couldn\'t be retreived')
		return None

def pic_path(path: os.path, info_doc: dict) -> os.path:

	#return the cover art path

	return os.path.join(
		path,
		(info_doc['album_path']
			+ '.'
			+ info_doc['art url'].split('.')[-1]))


def pic_format(path: str) -> str:

	#return the format of a pic

	ext = path.split('.')[-1]

	if ext == 'jpg':

		return 'image/jpeg'

	if ext == 'png':

		return 'image/png'


def check_art(path: str, info_doc: dict) -> str:

	#check if cover art file exists

	return os.path.exists(pic_path(path,info_doc))


def check_audiofile(saved_par: dict, info_doc: dict) -> bool:

	#chekc if audiofile as already been downloaded
	if saved_par['format'] == 'mp3':

		path = os.path.join(
			saved_par['path'],
			info_doc['album_path'],
			check_filename(info_doc['title'])+'.mp3')

	elif saved_par['format'] == 'aac':

		path = os.path.join(
			path,
			info_doc['album_path'],
			check_filename(self.song_tag['title'])+'.m4a')

	else:

		path = os.path.join(
			path,
			info_doc['album_path'],
			check_filename(self.song_tag['title'])+'.ogg')
		
	return os.path.exists(path)


def read_txt(path: str) -> list:

	'''
	read a txt and put it in a list
	'''

	with open(path, 'r') as f:

		data = f.readlines()

	return data


def mkdir_album(path: str):

	os.makedirs(path, exist_ok=True)


def read_param(path):

	
	with open(path) as f:

		data = json.load(f)

	return data


def file_path() -> str:

	#return current file.py path

	if getattr(sys, 'frozen', False):

		# If the application is run as a bundle, the PyInstaller bootloader
		# extends the sys module by a flag frozen=True and sets the app 
		# path into variable _MEIPASS'

		application_path = sys._MEIPASS

	else:

		application_path = os.path.dirname(os.path.abspath(__file__))

	return application_path


def save_param(parameters: dict, path: str):

	'''
	save parameters in json file
	'''

	with open(path,'w') as outfile:

		json.dump(parameters, outfile)
		outfile.close()