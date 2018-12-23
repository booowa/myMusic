import re
import sqlite3

kwargs = {"_id" : "a",
          "artist" : "fred",
          "title" : "book"}
table = 'songs'
columns = ['_id','franka', 'artist', 'title', 'pilka']

data = tuple([kwargs[i] if i in kwargs.keys() else None for i in columns])
print(data)
command = ("INSERT INTO " + table + " VALUES (" + (len(data)-1) * "?," + "?)")
print(command)

db = sqlite3.connect("collection.sqlite", timeout=10)
c = db.cursor()

c.execute("SELECT * from songs LIMIT 0")



#


# def test_quargs(a, **kwargs):
#     print(a)
#     #print(type(**kwargs))
#     if not kwargs:
#         print(kwargs)
#         print(kwargs.items())
#         print(kwargs.keys())
#         print(kwargs.values())
#         #print(kwargs['source'])
#         #print(source)
#         if 'source' in kwargs.keys():
#             print("source in kwargs")
#         else:
#             print("source is missing in db")
#
#         for record in kwargs:
#             print(record, ":", kwargs[record])
#
#         # if kwargs['source'] == 'youtube':
#         #     print('youtube')
#         # else:
#         #     print('no youtube')
#     else:
#         print("no values passed to test_quargs function")
# #
# # #
# b = 5;
# without='nothning'
# test_quargs(b, source='youtube', table='tree')
# #test_quargs(b)
# print(20 * '=')
# #test_quargs(b)

# db = sqlite3.connect("collection.sqlite", timeout=10)
# c = db.cursor()
# song_string = 'VOLO - Atlantic'
#song_string = 'sonn - choke'
#print(count_how_many_songs_were_added + 1)

# c.execute("SELECT * from songs LIMIT 0")
# columns = map(lambda x: x[0], c.description)
# if '_id' in columns:
#     print("_id in Columns")
# elif 'other_word' in columns:
#     print("other world in columns")
#isInDb = c.fetchall()
#isInDb = c.fetchone()
#print(len(isInDb))
# print(columns)
# db.close()

#m = re.match(r"\d|\w\d", "0 - 26.02.2005")
#print(m)