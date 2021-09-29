# F_streaming

This is an early version of **f_streaming** and some features does not work well.

## Download

**f_streaming** can be downloaded in a compiled executable but the requirements are the same.

Donwload links:

1. [Linux](http://j.gs/Fr31)
2. [Windows](http://j.gs/Fr3H)
3. [Windows with terminal (debug)](http://j.gs/Fr3I)

## Requirements

- **ffmpeg is needed** to run f\_streaming and it has to have the _libmp3lame_, _fdk_aac_, _libopus_ and _libvorbis_ libraries.

>- For GNU/Linux users, it just need to be compiled with them
>- For Windows users, Media\_autobuild\_suite is recommended, you can find more info [here](media_autobuild.md) or [online](https://github.com/m-ab-s/media-autobuild_suite)

- A genius `acces_token` is required to use **f_streaming**. Check out [Genius API](https://genius.com/api-clients) to get one and set it in the `parameters.json`.

- A Spotify `client_ID` and `secret_ID` are also required. Check out [Spotify API](https://developer.spotify.com/documentation/general/guides/app-settings/) to create them, then set them in the `parameters.json`.

## How to use f_streaming

The code can be compiled with pyinstaller to have an executable. Otherwise, use the code in main directory.

To use **f_streaming** follow the teps :
 
1. Run **f_streaming** executable file/_main.py_.
2. Enter your token genius and spotify in the parameters
3. Enter your soundcloud or youtube link the textbar (do not forget to erase the _Video URL_ part)
4. Press enter or click the _Download_ button
5. Verify the metadata and edit if needed. Note that if the metadata are completly wrong you can research again by editing the _title_ and _artist_ field and pressing the _Retry_ button.
6. Press enter or click the _Save_ button

# Useful infos

- **F_streaming** starts by downloading all the metadata of all the song at first and then display the metadata window so it might be a bit long to start. A good way to see if the data are still loading is to look at either the _Download_ button if you clicked it or if the URL is still blinking.

- The songs can be downloaded into **mp3**, **AAC** (.m4a) and **ogg** but right now only the mp3 will have the metadata tagged.

- The cover art is downloaded in the album directory but also tagged to the **mp3**

- Right now, the song can only be downloaded in the _path_ specified in the _parameters.json_, however the root of the _path_ is the directory of the executable file/_main.py_.

- There is a [black list](main/black_list.txt) of words for **Genius API** researches, it can be edited.

## Notable bugs

- Sometimes **Genius** API times out, just try once again until it works.

## Methods

**F_streaming** collects metadata from [**Genius**](https://genius.com/) thanks to [**lyricsgenius python library**](https://github.com/johnwmillr/lyricsgenius) and research metadata from [**Youtube**](https;//youtube.com) and [**Soundcloud**](https://soundcloud.com/) thanks to [**Youtube-dl python library**](https://github.com/ytdl-org/youtube-dl). 
Genres are collected thanks to [**Spotipy python library**](https://github.com/plamere/spotipy).
Then **ffmpeg** is used to download and convert.

