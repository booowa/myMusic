# -*- coding: utf-8 -*-

import os

# import google.oauth2.credentials

# import google_auth_oauthlib.flow
import re
from googleapiclient.discovery import build
#import database as db
#import logg
import logging
#import json
import pickle


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
exclude_playlists = ['Filmy']


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
        # function takes data from youtube and create list of playlist
        # playlist at begingg have arguments tittle and playlist_id
        # nextPage initial condition to the loop

        next_page = 1
        while next_page:
            if next_page == 1:
                next_page = None

            response = get_list_of_playlist_from_youtube(client, part='snippet,contentDetails', channelId=channel_id, pageToken=next_page)
            # print(response)
            if 'nextPageToken' in response.keys():
                next_page = response['nextPageToken']
            else:
                next_page = None

            for json in response['items']:
                logging.debug(json)
                playlist_title = json['snippet']['title']
                playlist_id = json['id']
                if playlist_title not in exclude_playlists:
                    self.add_playlist(playlist_title, playlist_id)

    def __str__(self):
        ret = ''
        for x in self.playlist:
            ret += "Playlist title: {}, ID {}\n\tSongs {}\n".format(x.title, x.youtube_id, len(x.songs))
            for y in x.songs:
                ret += "\t\t{}\n".format(y.songString)
        return ret


class Playlist(object):

    def __init__(self, title, id):
        self.title = title
        self.youtube_id = id
        self.delete_counter = 0
        self.private_video_counter = 0
        self.songs = []

    def retrieve_songs_from_source_by_playlist_id(self, client, youtube_playlist_id):
        next_page = 1
        while next_page:
            if next_page == 1:
                next_page = None

            response = client.playlistItems().list(part='snippet', playlistId=youtube_playlist_id, pageToken=next_page).execute()
            # print("Response before encode {}".format(response))
            # temp = json.dumps(dictt)
            # temp.encode(encoding="UTF-8")
            # print(temp)
            # print(type(temp))
            # dictt2 = json.loads(temp)
            # response_str = json.dumps(response)
            # response_str = response_str.encode(encoding="utf-8", errors='ignore')
            # response = json.loads(response_str)
            # print("Response after encode {}".format(response))
            if 'nextPageToken' in response.keys():
                next_page = response['nextPageToken']
            else:
                next_page = None
            # print(response['items'][0]['snippet']['title'])
            # print("Response type: {}".format(type(response)))
            for json_element in response['items']:
                title = json_element['snippet']['title']
                video_id = json_element['snippet']['resourceId']['videoId']
                # logging.debug("Songs from playlist {}".format(json_element))
                self.addSongToPlaylist(title, video_id)
                # print("Title {} VideoId {}".format(title, videoId))
                # print(json['snippet']['title'])

        return response

    def addSongToPlaylist(self, songTitle, videoId):
        self.songs.append(Song(songTitle, videoId))


    def getPlaylistID(self):
        return self.youtube_id

    def get_number_of_songs(self):
        return len(self.songs)

    def get_song(self):
        if self.songs is not None:
            for song in self.songs:
                # print(type(song))
                yield song

    def __str__(self):
        ret = "Playlist title: {}, ID {}\n".format(self.title, self.youtube_id)
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
    def add_videoid_to_song(self, videoId):
        self.videoId = videoId

    ##TODO needs some contents

    def get_song_duration(self, client, **kwargs):
        if 'id' not in kwargs.keys():
            kwargs['id'] = self.videoId
        response = client.videos().list(**kwargs).execute()
        logging.debug("Response {}".format(response))

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


def get_data_from_youtube(args) -> PlaylistCollection:
    '''Fuctions dpending if there get data from youtube and populate instance of
    PlaylistCollection with apropriate information. At the and it store it on disk as
    pickle. There is also option to read data from pickle. It is enabled by using
    argument --local_source'''


    #If pickle is missing or it was specified that data should be taken from local_source.
    #Then take data from youtube (soruce)
    if not (os.path.exists("youtubePlaylist.pickle") or args.local_source):
        print("Getting data from youtube (source)")
        youtube_playlists = PlaylistCollection()
        #fill youtubePlaylists with playlist each one have title and playlist_id from source
        youtube_playlists.retrieve_playlist_from_youtube(client, CHANNEL_ID)
        for playlist in youtube_playlists.get_one_playlists():

            items_json = playlist.retrieve_songs_from_source_by_playlist_id(client, playlist.getPlaylistID())
            print("******* Playlista: {}, Number of songs: {}".format(playlist.title, playlist.get_number_of_songs()))
            #playlist_instance = db.add_record_to_db(db.Playlist, title=playlist.title, source='youtube',
            #                                        playlist_id=playlist.getPlaylistID())
            for song in playlist.songs:
                print(20 * '^' + " song separator " + 20 * '^')
                song_string = song.get_song_songString()
                print("Song string: {}".format(song_string))
                if song_string == "Deleted video":
                    playlist.delete_counter += 1
                elif song_string == "Private video":
                    playlist.private_video_counter += 1
                else:
                    pass
                    #time = song.get_song_duration(client, part='contentDetails')
                    #song_instance = db.add_record_to_db(db.Song, song_string=song_string, source='youtube', belongs_to_playlist=playlist_instance)
                    #database.add_record_to_db(Song_details)
        with open("youtubePlaylists.pickle", "wb") as pickle_write_file:
            print("Pickle youtubePlaylists")
            pickle.dump(youtube_playlists, pickle_write_file)
    else:
        #If local_source defined and file exists, read data from pickle
        with open("youtubePlaylists.pickle", "rb") as pickle_read_file:
            print("Load data from pickle")
            youtube_playlists = pickle.load(pickle_read_file)
            print(youtube_playlists)
    return youtube_playlists

def update_song_db_youtube():
    pass


def get_authenticated_service():
    client = build(API_SERVICE_NAME, API_VERSION, developerKey=DEVELOPER_KEY)
    return client


def get_list_of_playlist_from_youtube(client, **kwargs):
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



#logger = logg.getLogger(__name__)


with open('ApiKey.txt') as f:
    set_developer_key(f.readline())
client = get_authenticated_service()
logging.info("did i get to all lines in youtube module when running main.py")

