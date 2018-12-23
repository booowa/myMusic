# -*- coding: utf-8 -*-

# import os

# import google.oauth2.credentials

# import google_auth_oauthlib.flow
from googleapiclient.discovery import build
from database import *
import logging
import json

# from googleapiclient.errors import HttpError
# from google_auth_oauthlib.flow import InstalledAppFlow

# The CLIENT_SECRETS_FILE variable specifies the name of a file that contains
# the OAuth 2.0 information for this application, including its client_id and
# client_secret.

# CLIENT_SECRETS_FILE = "client_secret.json"
DEVELOPER_KEY = ""
# AIzaSyBVs7UfOJVTfr5nrd0N9LiMPuqWxRqoxWM"

# This OAuth 2.0 access scope allows for full read/write access to the
# authenticated user's account and requires requests to use an SSL connection.
SCOPES = ['https://www.googleapis.com/auth/youtube.force-ssl']
API_SERVICE_NAME = 'youtube'
API_VERSION = 'v3'
CHANNEL_ID = "UCRI-p_uLzQ_plYueAF-qqYw"


class PlaylistCollection(object):

    def __init__(self):
        self.playlist = []
        # self.titleList = []
        # self.idList = []

    def add_playlist(self, title, playlistId):
        self.playlist.append(Playlist(title, playlistId))
        # self.titleList.append(title)
        # self.idList.append(playlistId)

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
        # return self.IDs

    def retrieve_playlist_from_youtube(self, client, channel_id):
        # function
        # nextPage initial condition to the loop

        nextPage = 1
        while nextPage:
            if nextPage == 1:
                nextPage = None

            response = list_playlists(client, part='snippet,contentDetails', channelId=channel_id, pageToken=nextPage)
            # print(response)
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
                nextPage = None

            response = client.playlistItems().list(part='snippet', playlistId=playlistid, pageToken=nextPage).execute()

            if 'nextPageToken' in response.keys():
                nextPage = response['nextPageToken']
            else:
                nextPage = None

            # print(response['items'][0]['snippet']['title'])
            for json in response['items']:
                title = json['snippet']['title']
                videoId = json['snippet']['resourceId']['videoId']
                self.addSongToPlaylist(title, videoId)
                # print("Title {} VideoId {}".format(title, videoId))
                # print(json['snippet']['title'])

        return response

    def addSongToPlaylist(self, songTitle, videoId):
        self.songs.append(Song(songTitle, videoId))


    def getPlaylistID(self, ):
        return self.id

    def get_number_of_songs(self):
        return len(self.songs)

    def get_song(self):
        if self.songs is not None:
            for song in self.songs:
                # print(type(song))
                yield song

    def __str__(self):
        ret = "Playlist title: {}, ID {}\n".format(self.title, self.id)
        return ret


class Song(object):


    def __init__(self, songString, videoId):
        self.songString = songString
        self.videoId = videoId
        self.artist = ''
        self.title = ''
        self.additonalInfo = ''
        self.time = ''

    def get_song_songString(self):
        return self.songString


    ###TODO NOT USED YET
    def add_videoid_to_song(self, videoid):
        self.videoId = videoid

    ##TODO needs some contents

    def get_song_duration(self, client, **kwargs):
        if 'id' not in kwargs.keys():
            kwargs['id'] = self.videoId
        response = client.videos().list(**kwargs).execute()
        #print(response)
        logging.debug(response)
        self.time = response['items'][0]['contentDetails']['duration']
        self.time = self.convert_youtube_time_to_seconds(self.time)
        print("Song: {} duration: {}".format(self.songString, self.time))

        return self.time

    @staticmethod
    def convert_youtube_time_to_seconds(time):
        '''Function should parese values for minutes and seconds
           form text like: PT3M28S
           More over function is roobust to deal with songs that
           have only minutes part PT3M           '''
        pattern_obj = re.compile(r'''
                        PT(\d{1,2})M       #minutes
                        (?:(\d{1,2})S)?    #seconds optional
                        ''', re.VERBOSE)
        m = re.search(pattern_obj, time)
        time = 60 * int(m.group(1))
        if (m.group(2)):
            time += int(m.group(2))
        print("Converted time {}".format(time))
        return time


def init_tables_youtube():
    '''Fuctions checks if table in db exists, if not it creates them
       and updates'''

    init_database()

    youtubePlaylists.retrieve_playlist_from_youtube(client, CHANNEL_ID)
    for playlist in youtubePlaylists.get_one_playlists():
        itemsJson = playlist.retrieve_songs_from_playlist_by_id(client, playlist.getPlaylistID())
        print("******* Playlista: {}, Number of songs: {}".format(playlist.title, playlist.get_number_of_songs()))
        add_record_to_db('playlists', title=playlist.title, source='youtube')
        db_playlist_id = get_db_playlist_id(playlist.title)
        # playlist_id = add_record_to_db_playlist(playlist, source='youtube')
        print("******* " + playlist.getPlaylistID())
        for song in playlist.songs:
            print(song.get_song_songString())
            song_string = song.get_song_songString()
            time = song.get_song_duration(client, part='contentDetails')
            song_id_in_db = add_record_to_db('songs', song_string=song_string, source='youtube', playlist_id=db_playlist_id)
            add_record_to_db('song_details', )

            # add_update_record_to_db_songs(song_string, playlist_id=db_playlist_id, source='youtube')
        #    update
        # , playlist, source='youtube')

        # print(playlist.retrieve_songs_from_playlist_by_id(client, playlist.getPlaylistID()))

    # for playlist in youtubePlaylists.get_one_playlists():


def update_song_db_youtube():
    pass


def get_authenticated_service():
    client = build(API_SERVICE_NAME, API_VERSION, developerKey=DEVELOPER_KEY)
    return client


def list_playlists(client, **kwargs):
    response = client.playlists().list(**kwargs).execute()
    return response


def set_developer_key(key):
    global DEVELOPER_KEY
    DEVELOPER_KEY = key
    # print("key {}, DEVELOPER_KEY {}".format(key, DEVELOPER_KEY))
    return 0


def test_developer_key():
    print(DEVELOPER_KEY)
    return 0

#------------- logging configuration ---------------------#
logging.basicConfig(format='%(levelname)s:%(module)s:%(funcName)s:%(lineno)d:%(message)s', filename='youtube.log',level=logging.DEBUG, filemode='w')
#logging.basicConfig(filename='youtube.log',level=logging.DEBUG, filemode='w')

logger = logging.getLogger(__name__)

youtubePlaylists = PlaylistCollection()
with open('ApiKey.txt') as f:
    set_developer_key(f.readline())
client = get_authenticated_service()
logging.info("did i get to all lines in youtube module when running main.py")

