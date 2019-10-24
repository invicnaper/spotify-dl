[![GitHub license](https://img.shields.io/badge/license-GPLv2-blue.svg)](https://raw.githubusercontent.com/Facetracker-project/facetracker-core/master/COPYING)
[![GitHub license](https://img.shields.io/badge/packages-youtube--dl%2Fbs4-red.svg)](https://raw.githubusercontent.com/Facetracker-project/facetracker-core/master/COPYING)
[![GitHub license](https://img.shields.io/badge/author-naper-blue.svg)](https://raw.githubusercontent.com/Facetracker-project/facetracker-core/master/COPYING)
[![GitHub license](https://img.shields.io/badge/version-0.0.2-orange.svg)](https://raw.githubusercontent.com/Facetracker-project/facetracker-core/master/COPYING)
# spotify-dl
A script written in Python that extracts song or playlist information from Spotify and downloads them from YouTube if found.

This README would normally document whatever steps are necessary to get spotify-dl up and running.

### What is this repository for? ###

* spotify-dl allows you to download spotify songs or playlist
* Version 0.0.2
* This repo contains spotify-dl source code

### Screen ###

![alt text](http://nsa37.casimages.com/img/2016/02/13/160213111903934479.png "spotfy-dl screen")

# How to Install ?
to use spotify-dl , you need to install thoses packages :
  * bs4
  * youtube-dl
  
# MAC OSx
you can use brew to install youtube-dl :
  
    $ brew install youtube-dl
    
and pip to install bs4
  
    $ pip install beautifulsoup4
    
# Linux (debian)
use apt-get install to install youtube-dl

    $ sudo apt-get install youtube-dl
    
and pip to install bs4
  
    $ pip install beautifulsoup4
    
# How to use ?
you can either use your spotify account or downloading single track or playlist by providing an ID , ex:

    $ ./spotify-dl --track {spotify_song_id} --dl youtube
    
this will download the track and save it as mp3 format

you can get the song ID by getting the spotify URI of the song

{spotify_song_id_ex} : 28Ct4qwkQXY2W5yyNCLuVI

# Spotify API
The new version of the spotify api require an access_token for requests, you can check out https://developer.spotify.com/migration-guide-for-unauthenticated-web-api-calls/.

the new patch of spotify-dl have a new argument called:  --access_token , so the new usage of spotify-dl would be:
  
    $ ./spotify-dl --track {spotify_song_id} --dl youtube --access_token <your_access_token>
    
you can get the access token from the url generated while executing : 

    $ ./spotify-dl --gen_url 
    
you also have to create an application on https://developer.spotify.com/

change:

    CLIENT_ID=""
    CALL_BACK_URL=""

### Contributors ###

* Hamza Bourrahim
