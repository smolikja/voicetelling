from asyncio.log import logger
import os
from datetime import datetime
import logging

def set_logger():
    logging.basicConfig(filename="std.log",
                        format='%(asctime)s %(message)s',
                        filemode='w')
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)


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
                logger.info("Detected date: {} | file name: {}".format(file_date.strftime("%d/%m/%Y, %H:%M:%S"), file))
            except (ValueError, TypeError):
                logger.error("Error while getting int timestamp from str | file: {}".format(file))
                break

    return dict_voice_files

def main(args=None):
    set_logger()
    # TODO: nacist fily ze slozky
    print(get_voice_files())

    # TODO: zjistit jejich data a roztridit je do skupin
    # TODO: merge skupin filu
    print("hello world")

if __name__ == '__main__':
    main()