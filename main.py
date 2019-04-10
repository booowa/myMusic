import youtube
import database
import argparse
from database import *




if __name__ == '__main__':


    # todo use function that will allow read argument from command line ,getopt()
    parser =  argparse.ArgumentParser()
    parser.add_argument("-l", "--local_source", action="store_true",
                        help="Input data will be taken from youtubePlaylists.pickle file instead of "
                             "default youtubeAPI. It is usefull for development process")
    args = parser.parse_args()

    # for now it options will be choose by hard
    # FLAG_UPDATE_YOUTUBE = 0
    FLAG_INIT_YOUTUBE = 1

    #if FLAG_INIT_YOUTUBE or FLAG_UPDATE_YOUTUBE:
    if FLAG_INIT_YOUTUBE:

        database.init_database()
        youtube.get_data_from_youtube(args)
        # elif FLAG_UPDATE_YOUTUBE:
        #    update_tables_youtube()
    else:
        print("no flag used, please read help and choose one of the avilable options")
