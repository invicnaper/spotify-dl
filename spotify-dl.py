#!/usr/bin/python

#from googleapiclient.discovery import build
#from apiclient.errors import HttpError
#from oauth2client.tools import argparser

import urllib
import urllib2
from bs4 import BeautifulSoup
import argparse
#import spotify
import json
from StringIO import StringIO
import subprocess
import traceback

RED     = "\033[31m"
GREEN   = "\033[32m"
BLUE    = "\033[34m"
YELLOW  = "\033[36m"
DEFAULT = "\033[0m"

ACTION  = BLUE + "[+] " + DEFAULT
ERROR   = RED + "[+] " + DEFAULT
OK      =  GREEN + "[+] " + DEFAULT

#=======================
#   Spotify application
#=======================
CLIENT_ID=""
CALL_BACK_URL=""

# Set DEVELOPER_KEY to the API key value from the APIs & auth > Registered apps
# tab of
#   https://cloud.google.com/console
# Please ensure that you have enabled the YouTube Data API for your project.
DEVELOPER_KEY = "REPLACE_ME"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

def youtube_search(options):
  youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
    developerKey=DEVELOPER_KEY)

  # Call the search.list method to retrieve results matching the specified
  # query term.
  search_response = youtube.search().list(
    q=options.q,
    part="id,snippet",
    maxResults=options.max_results
  ).execute()

  videos = []
  channels = []
  playlists = []

  # Add each result to the appropriate list, and then display the lists of
  # matching videos, channels, and playlists.
  for search_result in search_response.get("items", []):
    if search_result["id"]["kind"] == "youtube#video":
      videos.append("%s (%s)" % (search_result["snippet"]["title"],
                                 search_result["id"]["videoId"]))
    elif search_result["id"]["kind"] == "youtube#channel":
      channels.append("%s (%s)" % (search_result["snippet"]["title"],
                                   search_result["id"]["channelId"]))
    elif search_result["id"]["kind"] == "youtube#playlist":
      playlists.append("%s (%s)" % (search_result["snippet"]["title"],
                                    search_result["id"]["playlistId"]))

  print "Videos:\n", "\n".join(videos), "\n"
  print "Channels:\n", "\n".join(channels), "\n"
  print "Playlists:\n", "\n".join(playlists), "\n"

def searchYoutube(trackname):
    textToSearch = trackname
    query = urllib.quote(textToSearch)
    url = "https://www.youtube.com/results?search_query=" + query
    response = urllib2.urlopen(url)
    html = response.read()
    soup = BeautifulSoup(html, "html.parser")
    #we return the first result
    return "https://youtube.com" + soup.findAll(attrs={'class':'yt-uix-tile-link'})[0]['href']

def getTrackName(id, access_token):
    """ get the spotify track name from id """
    print ACTION + " getting track name"
    proc = subprocess.Popen('curl -sS -X GET "https://api.spotify.com/v1/tracks/'+ id +'?market=ES" -H "Authorization: Bearer '+ access_token +'"', shell=True, stdout=subprocess.PIPE)
    tmp = proc.stdout.read()
    #convert from json to string
    #io = StringIO()
    #json.dump(tmp, io)
    data = json.loads(tmp)
    if 'error' in data:
        print ERROR + "can't found song name"
        print ERROR + data['error']['message']
        return None
    else:
        print OK + "name is " + data["name"]
        return data["name"]

def genUrl():
    """ gen url for getting access token """
    print ACTION + " generating url for access token"
    print OK +  "https://accounts.spotify.com/authorize?client_id="+ CLIENT_ID + "&response_type=token&redirect_uri=" + CALL_BACK_URL

def getAccessToken():
    """ get access token """
    print ACTION + " getting access token"
    proc = subprocess.Popen('curl -sS -X GET "https://accounts.spotify.com/authorize?client_id='+ CLIENT_ID +'&response_type=token&redirect_uri='+ CALL_BACK_URL +'" -H "Accept: application/json"', shell=True, stdout=subprocess.PIPE)
    tmp = proc.stdout.read()
    data = json.loads(tmp)

    print data

def downloadYoutube(link):
    """ downloading the track """
    print ACTION + "downloading song .."
    proc = subprocess.Popen('youtube-dl --extract-audio --audio-format mp3 '+ link, shell=True, stdout=subprocess.PIPE)
    tmp = proc.stdout.read()
    print OK + "Song Downloaded"

def header():
	""" header informations """
	print RED + "@ spotify-dl.py version 0.0.1"
	print YELLOW + "@ author : Naper"
	print BLUE + "@ Designed for OSx/linux"
	print "" + DEFAULT


if __name__ == "__main__":
  parser = argparse.ArgumentParser(description='spotify-dl allows you to download your spotify songs')
  parser.add_argument('--verbose',
    action='store_true',
    help='verbose flag' )
  parser.add_argument('--dl', nargs=1, help="set the download methode")
  parser.add_argument('--user', nargs=1, help="set the spotify login")
  parser.add_argument('--password', nargs=1, help="set the spotify password")
  parser.add_argument('--traceback', action='store_true', help="enable traceback")
  parser.add_argument('--gen_url', action='store_true', help="generate url for getting access_token")
  parser.add_argument('--track', nargs=1, help="spotify track id")
  parser.add_argument('--access_token', nargs=1, help="set the access_token")
  parser.add_argument('-m', nargs=1, help="set a methode")

  args = parser.parse_args()

  try:
      header();
      if args.gen_url:
          genUrl()
      else:
          if args.dl and args.access_token and args.dl[0] == 'youtube':
              if args.track:
                  #genUrl()
                  #getAccessToken()
                  name = getTrackName(args.track[0], args.access_token[0])
              link = searchYoutube(name)
              downloadYoutube(link)
          else :
              print ERROR + "use --help for help"
  except Exception, err:
    print ERROR + "An HTTP error occurred\n"
    if args.traceback:
    	traceback.print_exc()
