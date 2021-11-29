##
#
#file where function to founds informations about the music is coded
#
##

from __future__ import unicode_literals
import youtube_dl, lyricsgenius, spotipy, os
from spotipy.oauth2 import SpotifyClientCredentials
import command as cmd


saved_param = cmd.read_param(os.path.join(cmd.file_path(),'parameters.json'))
client_id = saved_param['spotify client id']
client_secret = saved_param['spotify client secret']
token_genius = saved_param['token genius']

client_credentials_manager = SpotifyClientCredentials(
    client_id=client_id,
    client_secret=client_secret)
sp = spotipy.Spotify(client_credentials_manager = client_credentials_manager)
genius = lyricsgenius.Genius(token_genius)


def clean_title(title: str) -> str:

    '''
    delete certain word patern
    '''

    #delete strings in black_list.txt

    forbiden_str = cmd.read_txt(os.path.join(cmd.file_path(), 'black_list.txt'))

    for word in forbiden_str :

        word = word[:-1]

        if word in title:

            pos_word_init = title.find(word)
            pos_word_end = pos_word_init + len(word) - 1

            if pos_word_init >= 1:

                title = title[:pos_word_init]+title[pos_word_end+1:]

            else:

                title = title[pos_word_end+1:]

    #delete what is in parentheses/bracket

    n = len(title)
    open_paren = []
    open_bracket = []
    close_paren = []
    close_bracket = []

    for char_index in range(n):

        if title[char_index] == '(':

            open_paren.append(char_index )

        if title[char_index] == ')':

            close_paren.append(char_index )

        if title[char_index] == '[':

            open_bracket.append(char_index )

        if title[char_index] == ']':

            close_bracket.append(char_index )

    n_paren = len(open_paren)
    n_bracket = len(open_bracket)
    delta_char = 0

    for index_paren in range(n_paren):

        pos_paren_init = open_paren[index_paren] - delta_char
        pos_paren_end = close_paren[index_paren] - delta_char

        if pos_paren_init >= 1:

            title = title[:pos_paren_init-1]+title[pos_paren_end+1:]

        else:

            title = title[pos_paren_end+1:]

        delta_char += pos_paren_end - pos_paren_init + 1

    for index_bracket in range(n_bracket):

        pos_bracket_init = open_bracket[index_bracket] - delta_char
        pos_bracket_end = close_bracket[index_bracket] - delta_char

        if pos_bracket_init >= 1:

            title = title[:pos_bracket_init-1]+title[pos_bracket_end+1:]

        else:

            title = title[pos_bracket_end+1:]

        delta_char += pos_bracket_end - pos_bracket_init + 1

    #delete featuring

    if ' ft.' in title.lower():

        pos_ft = title.find(' ft.')
        title = title[0:pos_ft]

    if ' feat' in title.lower():

        pos_ft = title.find(' feat')
        title = title[0:pos_ft]

    return title


def info_playlist(url_playlist: str) -> list:

    '''
    Exract list of videos url from a playlist url
    '''

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
        'progress_hooks': [my_hook]
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:

        result = ydl.extract_info(url_playlist, download=False)
        n_vid = len(result['entries']) if 'entries' in result else 1
        video = result['entries'][0] if 'entries' in result else result
        videos = [video['webpage_url']]

        if n_vid > 1:

            for i in range(1,n_vid):

                video = result['entries'][i]['webpage_url']
                videos.append(video)

    return videos


def info_url(url_video: str) -> (str, str):



    #extract info from youtube page
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
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        result = ydl.extract_info(url_video, download=False)
        video = result['entries'][0] if 'entries' in result else result

    #define search title
    search_title = video['title']
    search_title = clean_title(search_title)

    if (not ' - ' in search_title) and 'artist' in result:

        search_title = search_title + ' - ' + result['artist']

        if ', ' in search_title:

            pos_coma = search_title.find(',')
            search_title = search_title[:pos_coma]

    if 'soundcloud' in url_video:

        search_title = search_title + ' - ' + video['uploader']

    length = cmd.convert_time(video['duration'])

    return (search_title, length)


def info_title(search_title: str,length: str) -> dict:

    '''
        input : string of youtube url

        output : dictionnary with song the following infos
                'title'             title with featuring (string)
                'album'             title of the album (string)
                'artist'            name of the artists (list of strings)
                'album artist'      either main artist of the album or various artist if it's a mixtape (string)
                'track'             number of the track on the album (integer or None)
                'track total'       total number of track (integer or None)
                'date'              release date (strings in the format ['YYYY','MM','DD']'
                'art url'           url of the artwork of the album (string)
                'bpm'               beat per minute (integer)
                'publisher'         publishers (writers) of the song (list of strings)
                'lyrics'            lyrics of the song (string)
                'genre'             genre of the song (string)
                'length'            lentgh of the file (string in the format hh:mm:ss)
                'language'          language of the lyrics (string or None)
                'composer'          composer/beat maker of the song (string or None)
                'mix artist'        mix artist of the song (string or None)
                'disc number'       number of the disc (integer)
                'disc total number' total number of disc (integer)
                'year'              year of release (integer)
    '''

    #define info dictionnary
    metadata = {
                'title' :             '',
                'title ft' :          '',
                'album' :             '',
                'artist' :          [''],
                'album artist':       '',
                'track' :              0,
                'total track' :        0,
                'date' :              '',
                'publisher' :       [''],
                'lyrics' :            '',
                'genre' :           [''],
                'length' :             0,
                'language' :          '',
                'composer' :        [''],
                'text writer' :     [''],
                'year' :               0,
                'art url' :           '',
                'album_path' :      'music',
                }

    #search on genius
    song = genius.search_song(search_title)

    #duration
    metadata['length'] = length

    if song is None:

        song = genius.search_song('404 not found')

    #song info
    metadata['title'] = song.title
    metadata['title ft'] = song._body['title_with_featured']
    metadata['album'] = song.album
    metadata['artist'][0] = song.artist

    if song._body['featured_artists']!=[]:

        for i in range(len(song._body['featured_artists'])):

            metadata['artist'].append(song._body['featured_artists'][i]['name'])

    if song.year != None:

        metadata['date'] = song.year

    if song.year != '':

        metadata['year'] = metadata['date'][0:4]

    metadata['lyrics'] = song.lyrics

    #rajouter custom performance

    if song.writer_artists != []:

        metadata['text writer'][0] = song.writer_artists[0]['name']

        if len(song.writer_artists)>1:

            for i in range(1,len(song.writer_artists)):

                metadata['text writer'].append(song.writer_artists[i]['name'])

    if song.producer_artists != []:

        metadata['composer'][0] = song.producer_artists[0]['name']

        if len(song.producer_artists)>1:

            for i in range(1,len(song.producer_artists)):

                metadata['composer'].append(song.producer_artists[i]['name'])

    for custom_perf in song._body['custom_performances']:

        lbl_perf =  custom_perf['label']

        if ('publisher' in lbl_perf.lower()
                or 'publié' in lbl_perf.lower()
                or 'label' in lbl_perf.lower()):

            strg = ''

            for j in range(len(custom_perf['artists'])):

                strg = strg + custom_perf['artists'][j]['name']

                if j != len(custom_perf['artists'])-1:

                    strg += '; '

    #album info

    if metadata['album']is None:

        metadata['album'] = song.title
        metadata['track'] = 1
        metadata['total track'] = 1
        metadata['album artist'] = song.artist

        #genres (spotipy)
        result = sp.search(metadata['artist'])
        len_res = min([len(result['tracks']['items']),9])

        if len_res == 0:

            artist = {'genres' : []}

        for i in range(len_res):

            track = result['tracks']['items'][i]
            artist = sp.artist(track["artists"][0]["external_urls"]["spotify"])

            if artist['name'].lower() == metadata['album artist'].lower():

                break

        metadata['genre'] = artist['genres']

        if metadata['genre'] == []:

            metadata['genre'] = ['']

        metadata['art url'] = song._body['song_art_image_url']

    else:

        metadata['album_path'] = cmd.check_dirname(metadata['album'])
        album_id = song._body['album']['id']
        album_tracks = genius.album_tracks(album_id)['tracks']

        for track in album_tracks:

            if track['song']['id'] == song._body['id']:

                metadata['track'] = track['number']

        index_total_track = 1
        len_tracks = len(album_tracks)

        while (album_tracks[-index_total_track]['number'] is None
                and index_total_track < len_tracks):

            index_total_track += 1

        metadata['total track'] = album_tracks[-index_total_track]['number']

        if metadata['track'] is None:

            metadata['track'] = ''
            metadata['total track'] = ''

        metadata['album artist'] = genius.album(album_id)['album']['artist']['name']
        
        #genres (spotipy)

        album = {'genres' : []}#if not able to find album
        result = sp.search(metadata['album'])

        for i in range(len(result['tracks']['items'])):

            track = result['tracks']['items'][i]
            album = sp.album(track["album"]["external_urls"]["spotify"])

            if album['name'].lower() == song.album.lower():

                break

            else:

                album = {'genres' : []}


        if album['genres'] == []:

            result = sp.search(metadata['artist'])

            for track in result['tracks']['items']:

                artist = sp.artist(
                    track["artists"][0]["external_urls"]["spotify"])

                if artist['name'].lower() == metadata['album artist'].lower():

                    metadata['genre'] = artist['genres']
                    break                

        else:

            metadata['genre'] = album['genres']

        if metadata['genre'] == []:

            metadata['genre'] = ['']

        metadata['art url'] = genius.album(album_id)['album']['cover_art_url']

        if 'png?' in metadata['art url']:

            metadata['art url'] = song._body['song_art_image_url']

    return metadata


def info_query(url: str) -> dict:

    search_title, length = info_url(url)
    metadata = info_title(search_title, length)

    return metadata


def info_query_url(url: str) -> dict:

    '''
    Return metadata from url input
    '''

    metadata = info_query(url)
    str_artist = metadata['artist'][0]

    if len(metadata['artist'])>1:

        for artist in range(1,len(metadata['artist'])):

            str_artist = str_artist+'; '+metadata['artist'][artist]

    metadata['artist'] = str_artist

    str_publisher = metadata['publisher'][0]

    if len(metadata['publisher'])>1:

        for pub in range(1,len(metadata['publisher'])):

            str_publisher = str_publisher+'; '+metadata['publisher'][pub]

    metadata['publisher'] = str_publisher

    str_genre = metadata['genre'][0]

    if len(metadata['genre'])>1:

        for genre in range(1,len(metadata['genre'])):

            str_genre = str_genre+'; '+metadata['genre'][genre]

    metadata['genre'] = str_genre

    str_comp = metadata['composer'][0]

    if len(metadata['composer'])>1:

        for comp in range(1,len(metadata['composer'])):

            str_comp = str_comp+'; '+metadata['composer'][comp]

    metadata['composer'] = str_comp

    str_tw = metadata['text writer'][0]

    if len(metadata['text writer'])>1:

        for tw in range(1,len(metadata['text writer'])):

            str_tw = str_tw+'; '+metadata['text writer'][tw]

    metadata['text writer'] = str_tw

    return metadata


def info_query_title(title: str,length: str) -> dict:

    '''
    Return metadata with a title input
    '''

    metadata = info_title(title,length)
    str_artist = metadata['artist'][0]

    if len(metadata['artist'])>1:

        for artist in range(1,len(metadata['artist'])):

            str_artist = str_artist+'; '+metadata['artist'][artist]

    metadata['artist'] = str_artist

    str_publisher = metadata['publisher'][0]

    if len(metadata['publisher'])>1:

        for pub in range(1,len(metadata['publisher'])):

            str_publisher = str_publisher+'; '+metadata['publisher'][pub]

    metadata['publisher'] = str_publisher

    str_genre = metadata['genre'][0]

    if len(metadata['genre'])>1:

        for genre in range(1,len(metadata['genre'])):

            str_genre = str_genre+'; '+metadata['genre'][genre]

    metadata['genre'] = str_genre

    str_comp = metadata['composer'][0]

    if len(metadata['composer'])>1:

        for comp in range(1,len(metadata['composer'])):

            str_comp = str_comp+'; '+metadata['composer'][comp]

    metadata['composer'] = str_comp

    str_tw = metadata['text writer'][0]

    if len(metadata['text writer'])>1:

        for tw in range(1,len(metadata['text writer'])):

            str_tw = str_tw+'; '+metadata['text writer'][tw]

    metadata['text writer'] = str_tw

    return metadata