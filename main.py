import logging
import os
from datetime import datetime
import logging

# Returns dictionary {date : filename} of voice files
def get_voice_files():
    dict_voice_files = {}
    all_files = os.listdir()

    for file in all_files:
        if file.startswith('audioclip'):
            try:
                file_timestamp = file[9:19]
                file_date = datetime.fromtimestamp(int(file_timestamp))
                dict_voice_files[file_date] = file
                logging.info("Detected date: {} | file name: {}".format(file_date.strftime("%d/%m/%Y, %H:%M:%S"), file))
            except (ValueError, TypeError):
                logging.error("Error while getting int timestamp from str | file: {}".format(file))
                break

    return dict_voice_files

def main(args=None):
    logging.basicConfig(filename="std.log",
                        format='%(asctime)s %(message)s',
                        filemode='w',
                        level= logging.DEBUG)

    # TODO: nacist fily ze slozky
    print(get_voice_files())

    # TODO: group files via date

    # TODO: merge skupin filu
    print("hello world")

if __name__ == '__main__':
    main()