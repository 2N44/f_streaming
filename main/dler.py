##
#
#File where every function to download video are coded
#
##

from __future__ import unicode_literals
import youtube_dl, subprocess, os, requests, shutil
import command as cmd


#useful class and function
class MyLogger(object):
    def debug(self, msg):
        pass

    def warning(self, msg):
        pass

    def error(self, msg):
        print(msg)


def my_hook(d):
    if d['status'] == 'finished':
        print('Done downloading, now converting ...')

#right options to download mp3
ydl_opts = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '320',
    }],
    'logger': MyLogger(),
    'progress_hooks': [my_hook],

}



def dl_from_to(yt_url,from_time,to_time,target,format,br):

#URL, FROM and TARGET are strings (FROM and TOO example : "00:00:25")

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:

        result = ydl.extract_info(yt_url, download=False)
        video = result['entries'][0] if 'entries' in result else result

    init_time = cmd.sub_time(from_time,'00:00:30')
    url = video['formats'][0]['url']
    ext = video['formats'][0]['ext']
    codec = video['formats'][0]['acodec'] if 'codec' in video['formats'][0] else 'unknown_codec'

    if format == 'mp3':

        target += '.mp3'
        subprocess.call([
        'ffmpeg',
        '-ss', '%s' % init_time,
        '-i', '%s' % url,
        '-vn',
        '-ss', '%s' % from_time,
        '-t', '%s'% to_time,
        '-acodec', 'libmp3lame','-b:a', '%s' %br, '%s' %target,
        ])

    elif format == 'aac':

        target += '.m4a'
        subprocess.call([
        'ffmpeg',
        '-ss', '%s' % init_time,
        '-i', '%s' % url,
        '-vn',
        '-ss', '%s' % from_time,
        '-t', '%s'% to_time,
        '-c:a', 'libfdk_aac','-b:a', '%s' % br, '%s' %target,
        ])

    elif format == None:

        target += '_' + codec + '.ogg'
        subprocess.call([
        'ffmpeg',
        '-ss', '%s' % init_time,
        '-i', '%s' % url,
        '-vn',
        '-ss', '%s' % from_time,
        '-t', '%s'% to_time,
        '-c', '-copy', '%s' %target,
        ])



def dl_art(path,info_doc):

    image_url = info_doc['art url']
    filename = cmd.pic_path(path,info_doc)
    r = requests.get(image_url, stream = True)

    # Check if the image was retrieved successfully

    if r.status_code == 200 and filename[-1] == "g" :

        # Set decode_content value to True, otherwise the downloaded image file's size will be zero.

        r.raw.decode_content = True

        # Open a local file with wb ( write binary ) permission.

        with open(filename,'wb') as f:

            shutil.copyfileobj(r.raw, f)

        print('Image sucessfully Downloaded: ',filename)

    else:

        print('Image Couldn\'t be retreived')

