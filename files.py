import os


#print(b)
# print all files... and extract in most cases folder album and artist name
'''
for path, directories, files in os.walk(root):
    if files:
        print(path)
        #print(os.path)
        first_split = os.path.split(path)
        print(first_split)
        second_split = os.path.split(first_split[0])
        print(second_split)
        for f in files:
            #print("\t{}".format(f))
            song_details = f.strip('.mp3')
            print(song_details)
        print("*" * 40)
'''
'''
sum_b = 0
for path, directories, files in os.walk(root):
    if files:
        for f in files:
            #print(f)
            #print(len(f))
            f = os.path.join(path, f)
            #print(f)
            #print(len(f))
            #f = os.path.abspath(f)
            #print(f)
            b = os.stat(f).st_size
            sum_b += b
            #print(b)
'''
#print("Total space {}".format(sum_b))
#print("Total space {}".format(sizeof_fmt(sum_b)))


