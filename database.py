import sqlite3
import re
count_how_many_songs_were_added = 0

def init_database():

    #init playlist d
    db = sqlite3.connect("collection.sqlite", timeout=10)
    c = db.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS playlists (_id INTEGER PRIMARY KEY, title TEXT, type TEXT, youtube INTEGER, disk INTEGER)")
    c.execute("CREATE TABLE IF NOT EXISTS songs (_id INTEGER PRIMARY KEY, songString TEXT, youtube INTEGER, disk INTEGER, playlist INTEGER)")
    print("Tabels created")
    db.commit()
    db.close()

def add_record_to_db_playlist(playlist, **kwargs):
    #playlist :
    db = sqlite3.connect("collection.sqlite", timeout=10)
    c = db.cursor()
    #print("Inside add_record_to_db_palylist: playlist.title: {}".format(playlist.title))
    c.execute("SELECT title, _id from playlists WHERE title = (?)", (playlist.title,))
    #print("Fetchone {}".format(c.fetchone()))
    isInDb = c.fetchone()
    playlist_type = determin_playlist_type(playlist)
    print("isInDb for playlist: {}".format(isInDb))
    if isInDb:
        print("I did not add playlist {} to db as it is already there".format(isInDb))
    else:
        if kwargs['source'] == 'youtube':
            #c.execute("INSERT INTO playlists(title, ?) VALUES(?, 1)", (kwargs['source'], playlist.title))
            c.execute("INSERT INTO playlists (title, type, youtube) VALUES(?, ?, 1)", (playlist.title, playlist_type))
            db.commit()
            print("I did add playlist {} to db".format(playlist.title))

    #playlist_id_in_db = c.execute("SELECT _id from playlists WHERE title = (?)", (playlist.title,))
    db.close()
    #print("playlist : {} id : {}".format(playlist.title, playlist_id_in_db))
    #return playlist_id_in_db

def add_record_to_db_songs(song_string, playlist, **kwargs):
    db = sqlite3.connect("collection.sqlite", timeout=10)
    c = db.cursor()
    #print(count_how_many_songs_were_added + 1)
    c.execute("SELECT * from songs WHERE songString = (?)", (song_string,))
    isInDb = c.fetchone()
    print("isInDb for songs: {}".format(isInDb))
    if isInDb:
        if kwargs['source'] == 'youtube' and isInDb[2] == None:
            c.execute("UPDATE songs SET youtube = 1 WHERE songString = (?)", (song_string,))
            db.commit()
            print("I updated source of song {} that was already in db".format(isInDb))
        else:
            print("I did not add song {} to db as it is already there".format(isInDb))
    else:
        #c.execute()
        #check what source tries do update db
        c.execute("SELECT _id FROM playlists WHERE title = (?)", (playlist.title,))
        playlist_id_in_db = c.fetchone()
        print("Song: {} belongs to playlist with id {}".format(song_string, playlist_id_in_db))
        print("playlist_id_in_db type: {}".format(type(playlist_id_in_db)))
        playlist_id_in_db = int(playlist_id_in_db[0])
        print("trans playlist_id_in_db type: {}".format(type(playlist_id_in_db)))

        if kwargs['source'] == 'youtube':
            c.execute("INSERT INTO songs (songString, playlist) VALUES(?, ?)", (song_string, playlist_id_in_db))
        else:
            print("Unknown source tries to update db")
        db.commit()
        print("I did add song {} to db".format(song_string))
    #print("Inside add_record_to_db_palylist: playlist.title: {}".format(playlist.title))
    #c.execute("INSERT INTO songs(songString) VALUES(?)", (song,))
    #db.commit()
    db.close()

def determin_playlist_type(playlist):

    if re.match(r"\d|\w\d",playlist.title):
        playlist_type = "regular"
    elif re.match(r"Klimacik",playlist.title):
        playlist_type = "klimacik"
    elif re.match(r"Absolutny", playlist.title):
        playlist_type = "chillout"
    elif re.match(r"Koledy|Christmas|Chritmas", playlist.title):
        playlist_type = "carols"
    elif re.match(r"wyjazdowa", playlist.title):
        playlist_type = "wyjazdowa"
    else:
        playlist_type = "impreza"

    #print("Playlist {} is categorized as : {}".format(playlist.title, type))
    return playlist_type



def print_db_playlist():
    db = sqlite3.connect("collection.sqlite", timeout=10)
    c = db.cursor()
    c.execute("SELECT * FROM playlists")
    for row in c:
        print(row)
    db.close()