##
#
# functions to tag mp3 file
#
##

import eyed3, os
from eyed3.core import Date
import dler as dl
import command as cmd

#résoudre porblème encodage de texte dans info_doc et pour les tags

def tag_v1(path,info_doc):

    #tag the mp3 file with the featured artists in the title and main artist as the artist
    audiofile = eyed3.load(path)

    #classical song info
    audiofile.tag.title = info_doc['title ft']
    audiofile.tag.artist = info_doc['album artist']
    audiofile.tag.album = info_doc['album']
    audiofile.tag.album_artist = info_doc['album artist']
    audiofile.tag.track_num = info_doc['track'],info_doc['total track']

    #release date

    if info_doc['date'] != '':

        audiofile.tag.release_date = Date(int(info_doc['date'][:4]),int(info_doc['date'][5:7]),int(info_doc['date'][-2:]))
        audiofile.tag.original_release_date = Date(int(info_doc['date'][:4]),int(info_doc['date'][5:7]),int(info_doc['date'][-2:]))
        audiofile.tag.recording_date = Date(int(info_doc['date'][:4]),int(info_doc['date'][5:7]),int(info_doc['date'][-2:]))

    #add art as image
    path_img = audiofile.path.replace(audiofile.path.split(os.path.join(' ',' ')[1])[-1],'')
    
    if cmd.check_art(path_img,info_doc):

        audiofile.tag.images.set(3, open(cmd.pic_path(path_img,info_doc), 'rb').read(), cmd.pic_format(cmd.pic_path(path_img,info_doc)))

    else:

        dl.dl_art(path_img,info_doc)

        if cmd.check_art(path_img,info_doc):

            audiofile.tag.images.set(3, open(cmd.pic_path(path_img,info_doc), 'rb').read(), cmd.pic_format(cmd.pic_path(path_img,info_doc)))

    #composer, writers and publishers
    audiofile.tag.composer = info_doc['composer']
    audiofile.tag.publisher = info_doc['publisher']
    #eyed3.id3.frames.createFrame('','',info_doc['text writer'])

    #genre
    if info_doc['genre'] != []:

        audiofile.tag.non_std_genre = info_doc['genre']


    #lyrics
    audiofile.tag.lyrics.set(info_doc['lyrics'],info_doc['title'])


    #save tags
    audiofile.tag.save(version=eyed3.id3.ID3_V2_3)



def tag_v2(path,info_doc):

    #tag the mp3 file with the featured artists in the title and main artist as the artist
    audiofile = eyed3.load(path)

    #classical song info
    audiofile.tag.title = info_doc['title']
    audiofile.tag.artist = info_doc['artist']
    audiofile.tag.album = info_doc['album']
    audiofile.tag.album_artist = info_doc['album artist']
    audiofile.tag.track_num = info_doc['track'],info_doc['total track']

    #release date

    if info_doc['date'] != '':

        audiofile.tag.release_date = Date(int(info_doc['date'][:4]),int(info_doc['date'][5:7]),int(info_doc['date'][-2:]))
        audiofile.tag.original_release_date = Date(int(info_doc['date'][:4]),int(info_doc['date'][5:7]),int(info_doc['date'][-2:]))
        audiofile.tag.recording_date = Date(int(info_doc['date'][:4]),int(info_doc['date'][5:7]),int(info_doc['date'][-2:]))

    #add art as image
    path_img = audiofile.path.replace(audiofile.path.split(os.path.join(' ',' ')[1])[-1],'')

    if cmd.check_art(path_img,info_doc):

        audiofile.tag.images.set(3, open(cmd.pic_path(path_img,info_doc), 'rb').read(), cmd.pic_format(cmd.pic_path(path_img,info_doc)))
    else:

        dl.dl_art(path_img,info_doc)

        if cmd.check_art(path_img,info_doc):

            audiofile.tag.images.set(3, open(cmd.pic_path(path_img,info_doc), 'rb').read(), cmd.pic_format(cmd.pic_path(path_img,info_doc)))

    #composer, writers and publishers
    audiofile.tag.composer = info_doc['composer']
    audiofile.tag.publisher = info_doc['publisher']
    #eyed3.id3.frames.createFrame('','',info_doc['text writer'])

    #genre
    if info_doc['genre'] != []:
        audiofile.tag.non_std_genre = info_doc['genre']

    #lyrics
    audiofile.tag.lyrics.set(info_doc['lyrics'],info_doc['title'])

    #save tags
    audiofile.tag.save(version=eyed3.id3.ID3_V2_3)