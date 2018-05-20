
# -*- coding: utf-8 -*-

#import os

#import google.oauth2.credentials

#import google_auth_oauthlib.flow
from googleapiclient.discovery import build
import json
#from googleapiclient.errors import HttpError
#from google_auth_oauthlib.flow import InstalledAppFlow

# The CLIENT_SECRETS_FILE variable specifies the name of a file that contains
# the OAuth 2.0 information for this application, including its client_id and
# client_secret.
#CLIENT_SECRETS_FILE = "client_secret.json"
DEVELOPER_KEY = ""
#AIzaSyBVs7UfOJVTfr5nrd0N9LiMPuqWxRqoxWM"

# This OAuth 2.0 access scope allows for full read/write access to the
# authenticated user's account and requires requests to use an SSL connection.
SCOPES = ['https://www.googleapis.com/auth/youtube.force-ssl']
API_SERVICE_NAME = 'youtube'
API_VERSION = 'v3'
CHANNEL_ID = "UCRI-p_uLzQ_plYueAF-qqYw"


class PlaylistCollection(object):

    def __init__(self):
        self.playlist = []
        #self.titleList = []
        #self.idList = []

    def add_playlist(self, title, playlistId):
        self.playlist.append(Playlist(title,playlistId))
        #self.titleList.append(title)
        #self.idList.append(playlistId)

    def get_playlist_id_by_title(self, title):
        for x in self.playlist:
            if x.title == title:
                ret = x.id
                break
        else:
            ret = None
            print("There is no playlist with title: {}".format(title))
        return ret

    def get_one_playlists(self):
        if self.playlist is not None:
            for x in self.playlist:
                yield x
        #return self.IDs

    def retrieve_playlist_from_youtube(self, client, channel_id):
        #function
        #nextPage initial condition to the loop
        nextPage = 1
        while nextPage:
            if nextPage == 1:
                nextPage=None

            response = list_playlists(client, part='snippet,contentDetails', channelId=channel_id, pageToken=nextPage)
            #print(response)
            if 'nextPageToken' in response.keys():
                nextPage = response['nextPageToken']
            else:
                nextPage = None

            for json in response['items']:
                self.add_playlist(json['snippet']['title'], json['id'])

    def __str__(self):
        ret = ''
        for x in self.playlist:
            ret += "Playlist title: {}, ID {}\n".format(x.title, x.id)
        return ret


class Playlist(object):

    def __init__(self, title, id):
        self.title = title
        self.id = id
        self.songs = []

    def retrieve_songs_from_playlist_by_id(self, client, playlistid):

        nextPage = 1
        while nextPage:
            if nextPage == 1:
                nextPage=None

            response = client.playlistItems().list(part='snippet',playlistId=playlistid, pageToken=nextPage).execute()

            if 'nextPageToken' in response.keys():
                nextPage = response['nextPageToken']
            else:
                nextPage = None

            #print(response['items'][0]['snippet']['title'])
            for json in response['items']:
                self.addSongToPlaylist(json['snippet']['title'])
                #print(json['snippet']['title'])

        return response

    def addSongToPlaylist(self, songTitle):
        self.songs.append(Song(songTitle))

    def getPlaylistID(self,):
        return self.id

    def get_number_of_songs(self):
        return len(self.songs)

    def get_song(self):
        if self.songs is not None:
            for song in self.songs:
                #print(type(song))
                yield song

    def __str__(self):
        ret = "Playlist title: {}, ID {}\n".format(self.title, self.id)
        return ret


class Song(object):

    def __init__(self, songString):
        self.songString = songString
        self.artist = ''
        self.title = ''
        self.additonalInfo = ''
        self.time = ''

    def get_song_songString(self):
        return self.songString


def get_authenticated_service():
    client =  build(API_SERVICE_NAME, API_VERSION, developerKey=DEVELOPER_KEY)
    return client

def list_playlists(client, **kwargs):
    response = client.playlists().list(**kwargs).execute()
    return response

def set_developer_key(key):
    global DEVELOPER_KEY
    DEVELOPER_KEY = key
    #print("key {}, DEVELOPER_KEY {}".format(key, DEVELOPER_KEY))
    return 0

def test_developer_key():
    print(DEVELOPER_KEY)
    return 0
