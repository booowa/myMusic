import urllib.request

x = urllib.request.urlopen("http://ws.audioscrobbler.com/2.0/?method=track.search&track=Maroon%205%20-%20What%20Lovers%20Do%20ft.%20SZA%20(A-Trak%20Remix)&api_key=e6891fbd784ce9ddcc3c08e05f283f8c&format=json")

print(x.read())q


def convert_song_string_to_artist_and_title(song_string):
    """fucnction will use last.fm db to figure out which part of
       songString represent artist and which represent track name (title)
       songString (str)
       return tuple (artist, title)
       """
    pass
