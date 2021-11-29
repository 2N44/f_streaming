##
#
# functions to tag mp3 file
#
##

import eyed3, os
from eyed3.core import Date
import dler as dl
import command as cmd

#résoudre porblème encodage de texte dans metadata et pour les tags

def tag_v1(path: str, metadata: dict):

    '''
    tag the mp3 file with the featured artists in the title and main artist as
    the artist
    '''

    audiofile = eyed3.load(path)

    #classical song info
    audiofile.tag.title = metadata['title ft']
    audiofile.tag.artist = metadata['album artist']
    audiofile.tag.album = metadata['album']
    audiofile.tag.album_artist = metadata['album artist']
    audiofile.tag.track_num = metadata['track'],metadata['total track']

    #release date

    if metadata['date'] != '':

        audiofile.tag.release_date = Date(
            int(metadata['date'][:4]),
            int(metadata['date'][5:7]),
            int(metadata['date'][-2:]))
        audiofile.tag.original_release_date = Date(
            int(metadata['date'][:4]),
            int(metadata['date'][5:7]),
            int(metadata['date'][-2:]))
        audiofile.tag.recording_date = Date(
            int(metadata['date'][:4]),
            int(metadata['date'][5:7]),
            int(metadata['date'][-2:]))

    #add art as image
    path_img = audiofile.path.replace(
        audiofile.path.split(os.path.join(' ',' ')[1])[-1],'')
    
    if cmd.check_art(path_img,metadata):

        audiofile.tag.images.set(
            3,
            open(cmd.pic_path(path_img,metadata), 'rb').read(),
            cmd.pic_format(cmd.pic_path(path_img,metadata)))

    else:

        dl.dl_art(path_img,metadata)

        if cmd.check_art(path_img,metadata):

            audiofile.tag.images.set(
                3,
                open(cmd.pic_path(path_img,metadata), 'rb').read(),
                cmd.pic_format(cmd.pic_path(path_img,metadata)))

    #composer, writers and publishers
    audiofile.tag.composer = metadata['composer']
    audiofile.tag.publisher = metadata['publisher']
    #eyed3.id3.frames.createFrame('','',metadata['text writer'])

    #genre
    if metadata['genre'] != []:

        audiofile.tag.non_std_genre = metadata['genre']


    #lyrics
    audiofile.tag.lyrics.set(metadata['lyrics'],metadata['title'])

    #save tags

    audiofile.tag.save(version=eyed3.id3.ID3_V2_3)



def tag_v2(path: str, metadata: dict):

    #tag the mp3 file with the featured artists in the title and main artist as the artist
    audiofile = eyed3.load(path)

    #classical song info
    audiofile.tag.title = metadata['title']
    audiofile.tag.artist = metadata['artist']
    audiofile.tag.album = metadata['album']
    audiofile.tag.album_artist = metadata['album artist']
    audiofile.tag.track_num = metadata['track'],metadata['total track']

    #release date

    if metadata['date'] != '':

        audiofile.tag.release_date = Date(
            int(metadata['date'][:4]),
            int(metadata['date'][5:7]),
            int(metadata['date'][-2:]))
        audiofile.tag.original_release_date = Date(
            int(metadata['date'][:4]),
            int(metadata['date'][5:7]),
            int(metadata['date'][-2:]))
        audiofile.tag.recording_date = Date(
            int(metadata['date'][:4]),
            int(metadata['date'][5:7]),
            int(metadata['date'][-2:]))

    #add art as image
    path_img = audiofile.path.replace(
        audiofile.path.split(os.path.join(' ',' ')[1])[-1],'')

    if cmd.check_art(path_img,metadata):

        audiofile.tag.images.set(
            3,
            open(cmd.pic_path(path_img,metadata), 'rb').read(),
            cmd.pic_format(cmd.pic_path(path_img,metadata)))
    else:

        dl.dl_art(path_img,metadata)

        if cmd.check_art(path_img,metadata):

            audiofile.tag.images.set(
                3,
                open(cmd.pic_path(path_img,metadata), 'rb').read(),
                cmd.pic_format(cmd.pic_path(path_img,metadata)))

    #composer, writers and publishers
    audiofile.tag.composer = metadata['composer']
    audiofile.tag.publisher = metadata['publisher']
    #eyed3.id3.frames.createFrame('','',metadata['text writer'])

    #genre
    if metadata['genre'] != []:
        audiofile.tag.non_std_genre = metadata['genre']

    #lyrics
    audiofile.tag.lyrics.set(metadata['lyrics'],metadata['title'])

    #save tags
    audiofile.tag.save(version=eyed3.id3.ID3_V2_3)