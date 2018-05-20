from youtube import *
from database import *

if __name__ == '__main__':

    with open('ApiKey.txt') as f:
        set_developer_key(f.readline())
        #test_developer_key()


    client = get_authenticated_service()
    init_database()
    youtubePlaylists = PlaylistCollection()
    youtubePlaylists.retrieve_playlist_from_youtube(client, CHANNEL_ID)
    for playlist in youtubePlaylists.get_one_playlists():
        itemsJson = playlist.retrieve_songs_from_playlist_by_id(client, playlist.getPlaylistID())
        print("Playlista: {}, Number of songs: {}".format(playlist.title,playlist.get_number_of_songs()))
        playlist_id = add_record_to_db_playlist(playlist, source='youtube')
        print(playlist.getPlaylistID())
        #for song in playlist.songs:
        #    #print(song.get_song_songString())
        #    songString = song.get_song_songString()
        #    add_record_to_db_songs(songString, playlist, source='youtube')

        #print(playlist.retrieve_songs_from_playlist_by_id(client, playlist.getPlaylistID()))

    #for playlist in youtubePlaylists.get_one_playlists():


