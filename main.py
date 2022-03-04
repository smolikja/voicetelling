import logging
import os
from datetime import datetime, timedelta, time
from pydub import AudioSegment
import shutil
import json

# Returns dictionary {<datetime: created> : <str: file name>} of voice files
def get_voice_files():
    dict_voice_files = {}
    all_files = os.listdir()

    for file in all_files:
        if file.startswith('audioclip'):
            try:
                file_timestamp = file[9:19]
                file_date = datetime.fromtimestamp(int(file_timestamp))
                dict_voice_files[file_date] = file
                logging.info("Detected file -> created: {} | file name: {}".format(file_date.strftime("%d/%m/%Y, %H:%M:%S"), file))
            except (ValueError, TypeError):
                logging.error("Error while getting int timestamp from str | file name: {}".format(file))
                break

    return dict_voice_files

def group_files_by_date(ungrupped_files):
    grupped_files = {}

    for date in ungrupped_files:
        group_date = datetime.date(date)
        if datetime.time(date) < time(5, 0, 0):
            group_date = group_date - timedelta(days=1)

        if group_date in grupped_files.keys():
            grupped_files[group_date][date] = ungrupped_files[date]
        else:
            grupped_files[group_date] = {date : ungrupped_files[date]}

        # # for debug
        # if group_date.strftime("%m/%d/%Y") in grupped_files.keys():
        #     grupped_files[group_date.strftime("%m/%d/%Y")][date.strftime("%m/%d/%Y, %H:%M:%S")] = ungrupped_files[date]
        # else:
        #     grupped_files[group_date.strftime("%m/%d/%Y")] = {date.strftime("%m/%d/%Y, %H:%M:%S") : ungrupped_files[date]}
        
    # # for debug
    # with open('grupped_files.json', 'w') as outfile:
    #     json.dump(grupped_files, outfile)

    return grupped_files

def process_audio_files(groupped_files):
    print("in progress...")

    try:
        shutil.rmtree("export")
    except OSError as e:
        logging.error("Error: %s : %s" % ("export", e.strerror))
    os.mkdir("export")

    for group_key in groupped_files:
        to_be_merged = AudioSegment.empty()

        for file_key in groupped_files[group_key]:
            to_be_merged += AudioSegment.from_file(groupped_files[group_key][file_key], format="mp4")

        to_be_merged += AudioSegment.from_file("beep.wav", format="wav")
        to_be_merged.export("export/{}.mp3".format(group_key.strftime("%d-%m-%Y")), format="mp3")
    print("done")

def main(args=None):
    logging.basicConfig(filename="std.log",
                        format='%(asctime)s %(message)s',
                        filemode='w',
                        level= logging.DEBUG)

    # Files into dictionary {<datetime: created> : <str: file name>}
    dict_voice_files = get_voice_files()

    # Files into dictionary {<datetime: grupe time> : {<datetime: created> : <str: file name>}}
    dict_groupped_files = group_files_by_date(dict_voice_files)

    # Merge and export audio files
    process_audio_files(dict_groupped_files)

if __name__ == '__main__':
    main()