import sqlite3
import re
import peewee

count_how_many_songs_were_added = 0


def init_database():
    db = sqlite3.connect("collection.sqlite", timeout=10)
    c = db.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS playlists (_id INTEGER PRIMARY KEY, title TEXT, type TEXT, source TEXT)")
    c.execute("CREATE TABLE IF NOT EXISTS songs (_id INTEGER PRIMARY KEY, song_string TEXT, videoId TEXT, "
              "source TEXT, playlist_id INTEGER, song_details_id INTEGER)")
    c.execute("CREATE TABLE IF NOT EXISTS song_details (_id INTEGER PRIMARY KEY, artist TEXT, title TEXT, "
              "time INTEGER, additional_info TEXT)")
    print("Tables created")
    db.commit()
    db.close()


def add_record_to_db(table, **kwargs):
    if not kwargs:
        print("value wasn't added to table {}, missing target column and value")
        return
    else:
        db = sqlite3.connect("collection.sqlite", timeout=10)
        c = db.cursor()
        if table == 'playlists':
            if 'title' not in kwargs.keys():
                print("To add values to table {}: you need to specify value for column title".format(table))
                return
            elif 'type' not in kwargs.keys():
                kwargs['type'] = determine_playlist_type(kwargs['title'])
            else:
                c.execute("SELECT * FROM " + table + " WHERE title = (?)", (kwargs['title'],))
        elif table == 'songs':
            if 'song_string' not in kwargs.keys():
                print("To add values to table {}: you need to specify value for column song_string".format(table))
                return
            else:
                c.execute("SELECT * FROM " + table + " WHERE song_string = (?)", (kwargs['song_string'],))
        elif table == 'song_details':
            if set(['artist', 'title']).issubset(set(kwargs.keys())):
                print("To add values to table {}: you need to specify value for column artist and title".format(table))
                return
            else:
                c.execute('SELECT * FROM ' + table + " WHERE artist = (?) AND title = (?)", (kwargs['artist'],
                                                                                             kwargs['title']))
        else:
            print("Table {} do not exist".format(table))

        is_in_db = c.fetchall()

        columns = list(get_columns_from_table(c, table))
        #c.execute("SELECT * FROM " + table + " ")
        #creats tuple with values for all avilable keys, if key dosn't exist in kwargs it will put None value
        data = tuple([kwargs[i] if i in kwargs.keys() else None for i in columns])
        if not db_content_with_data_to_be_added_are_the_same(is_in_db, data) or is_in_db is not None:
            #todo secure from injections
            c.execute("INSERT INTO " + table + " VALUES (" + (len(data)-1) * "?," + "?)", data)
            print("INSERT INTO " + table + " VALUES (" + (len(data)-1) * "?," + "?) : id {}".format(data, c.lastrowid))
            db.commit()
        db.close()


# def add_record_to_db_playlist(playlist, **kwargs):
#     # playlist :
#     db = sqlite3.connect("collection.sqlite", timeout=10)
#     c = db.cursor()
#     # print("Inside add_record_to_db_palylist: playlist.title: {}".format(playlist.title))
#     c.execute("SELECT title, _id from playlists WHERE title = (?)", (playlist.title,))
#     # print("Fetchone {}".format(c.fetchone()))
#     is_in_db = c.fetchone()
#     playlist_type = determine_playlist_type(playlist)
#     print("is_in_db for playlist: {}".format(is_in_db))
#     # todo refactor it so it can update values
#     if is_in_db:
#         print("I did not add playlist {} to db as it is already there".format(is_in_db))
#     else:
#         if kwargs['source'] == 'youtube':
#             # c.execute("INSERT INTO playlists(title, ?) VALUES(?, 1)", (kwargs['source'], playlist.title))
#             c.execute("INSERT INTO playlists (title, type, source) VALUES(?, ?, 1)", (playlist.title, playlist_type))
#             db.commit()
#             print("I did add playlist {} to db".format(playlist.title))
#
#     # playlist_id_in_db = c.execute("SELECT _id from playlists WHERE title = (?)", (playlist.title,))
#     db.close()
#     # print("playlist : {} id : {}".format(playlist.title, playlist_id_in_db))
#     # return playlist_id_in_db
#
#
# def add_update_record_to_db_songs(song_string, **kwargs):
#     db = sqlite3.connect("collection.sqlite", timeout=10)
#     c = db.cursor()
#     # print(count_how_many_songs_were_added + 1)
#     c.execute("SELECT * FROM songs WHERE song_string = (?)", (song_string,))
#     is_in_db = c.fetchall()
#     if len(is_in_db) >= 2:
#         #todo manage_duplicates funcionality not implemented yet
#         manage_duplicates(song_string)
#
#     print("is_in_db for songs: {}".format(is_in_db))
#     if not is_in_db:
#         c.execute("INSERT INTO songs (song_string) VALUES(?)", (song_string,))
#
#         update_song_record_in_db(c, song_string, **kwargs)
#         print("I did add song {} to db".format(song_string))
#     else:
#         update_song_record_in_db(c, song_string, **kwargs)
#     # print("Inside add_record_to_db_palylist: playlist.title: {}".format(playlist.title))
#     # c.execute("INSERT INTO songs(songString) VALUES(?)", (song,))
#     # db.commit()
#     db.commit()
#     db.close()


def update_song_record_in_db(c, song_string, **kwargs):
    """ fuction that supposed to update db with data in specific columns

    :arg
    c - db cursor handler
    song_string - string that represents song (fetch from soruce in most cases it will be 'artist - title'
    is_in_db - list of tuples: content (all columns) of record that hold song with song_string
                for one record: [(254, 'sonn - choke', None, None)]
                for 2 records: [(13, 'VOLO - Atlantic', None, None), (950, 'VOLO - Atlantic', None, None)]
                _id, song_string TEXT, source TEXT, playlist INTEGER
    **kwargs - dictionary that hold names of columns and values that should be updated
    :return

    """

    if 'source' in kwargs.keys():
        c.execute("SELECT source FROM songs WHERE song_string = (?)", (song_string,))
        already_in_table, = c.fetchone()
        if already_in_table:
            if kwargs['source'] not in already_in_table.split(','):
                value = ','.join(already_in_table,kwargs['source'])
            c.execute("UPDATE songs SET source =(?)", (value,))
        else:
            print("Function: update_song_record_in_db, did't found record to be updated")
    if 'playlist_id' in kwargs.keys():
        pass
    if 'source' in kwargs.keys():
        pass
    if 'title' in kwargs.keys():
        pass
    if 'artist' in kwargs.keys():
        pass
    if 'time' in kwargs.keys():
        pass
    if 'additional_info' in kwargs.keys():
        pass
    if 'videoId' in kwargs.keys():
        pass

    #     c.execute("UPDATE songs SET youtube = 1 WHERE songString = (?)", (song_string,))
    #     db.commit()
    #     print("I updated source of song {} that was already in db".format(isInDb))
    # else:
    #     print("I did not add song {} to db as it is already there".format(isInDb))
    #
    # pass


def get_db_playlist_id(playlist):
    db = sqlite3.connect("collection.sqlite", timeout=10)
    c = db.cursor()
    c.execute("SELECT _id from playlists WHERE title = (?)", (playlist,))
    (db_playlist_id,) = c.fetchone()
    return db_playlist_id


def get_columns_from_table(c, table):
    c.execute("SELECT * from " + table + " LIMIT 0")
    return map(lambda x: x[0], c.description)


def db_content_with_data_to_be_added_are_the_same(is_in_db, data):
    '''Function checks if data that is intended to be putted in db
       isn;t already there. It will detect if there are any difference
       in corresponding tuples. If difference is present it will return TRUE
       otherwise it will return FALSE

       return TRUE or FALSE'''

    for record in is_in_db:
        for y in range(len(record)):
            if ((record[y] and data[y]) is not None) and record[y] != data[y]:
                return False
    return True


def determine_playlist_type(playlist):
    if re.match(r"\d|\w\d", playlist):
        playlist_type = "regular"
    elif re.match(r"Klimacik", playlist):
        playlist_type = "klimacik"
    elif re.match(r"Absolutny", playlist):
        playlist_type = "chillout"
    elif re.match(r"Koledy|Christmas|Chritmas", playlist):
        playlist_type = "carols"
    elif re.match(r"wyjazdowa", playlist):
        playlist_type = "wyjazdowa"
    else:
        playlist_type = "impreza"

   # print("Playlist {} is categorized as : {}".format(playlist.title, type))
    return playlist_type


def manage_duplicates(song_string):
    pass
    #todo think about how to manage duplicates


def print_db_playlist():
    db = sqlite3.connect("collection.sqlite", timeout=10)
    c = db.cursor()
    c.execute("SELECT * FROM playlists")
    for row in c:
        print(row)
    db.close()

