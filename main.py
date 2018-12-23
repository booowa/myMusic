from youtube import *
from database import *


from youtube import init_tables_youtube

if __name__ == '__main__':

    # todo use function that will allow read argument from command line ,getopt()
    # for now it options will be choose by hard
    # FLAG_UPDATE_YOUTUBE = 0
    FLAG_INIT_YOUTUBE = 1

    #if FLAG_INIT_YOUTUBE or FLAG_UPDATE_YOUTUBE:
    if FLAG_INIT_YOUTUBE:
        init_tables_youtube()
        # elif FLAG_UPDATE_YOUTUBE:
        #    update_tables_youtube()
    else:
        print("no flag used, please read help and choose one of the avilable options")
