# import logging
# import json
import msvcrt
import os
from datetime import datetime, timedelta, time
import sys
from pydub import AudioSegment
import shutil

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

# Returns dictionary {<datetime: created> : <str: file name>} of voice files
def get_voice_files():
    dict_voice_files = {}
    all_files = os.listdir()

    for file in all_files:
        if file.startswith('audioclip') and file.endswith('.mp4'):
            try:
                file_timestamp = file[9:19]
                file_date = datetime.fromtimestamp(int(file_timestamp))
                dict_voice_files[file_date] = file

                # for debug
                # logging.info("Detected file -> created: {} | file name: {}".format(file_date.strftime("%d/%m/%Y, %H:%M:%S"), file))

            except (ValueError, TypeError):
                print("Error while getting int timestamp from str | file name: {}".format(file))
                break

    return dict_voice_files

def group_files_by_date(ungrouped_files):
    grouped_files = {}

    for date in ungrouped_files:
        group_date = datetime.date(date)
        if datetime.time(date) < time(5, 0, 0):
            group_date = group_date - timedelta(days=1)

        if group_date in grouped_files.keys():
            grouped_files[group_date][date] = ungrouped_files[date]
        else:
            grouped_files[group_date] = {date : ungrouped_files[date]}

        # # for debug
        # if group_date.strftime("%m/%d/%Y") in grouped_files.keys():
        #     grouped_files[group_date.strftime("%m/%d/%Y")][date.strftime("%m/%d/%Y, %H:%M:%S")] = ungrouped_files[date]
        # else:
        #     grouped_files[group_date.strftime("%m/%d/%Y")] = {date.strftime("%m/%d/%Y, %H:%M:%S") : ungrouped_files[date]}
        
    # # for debug
    # with open('grouped_files.json', 'w') as outfile:
    #     json.dump(grouped_files, outfile)

    return grouped_files

def process_audio_files(grouped_files):
    print("This takes a while, merging is in progress...")

    if os.path.isdir("export"):
        shutil.rmtree("export")
    os.mkdir("export")

    for group_key in grouped_files:
        to_be_merged = AudioSegment.empty()

        for file_key in grouped_files[group_key]:
            to_be_merged += AudioSegment.from_file(grouped_files[group_key][file_key], format="mp4")

        to_be_merged += AudioSegment.from_file(resource_path("beep.wav"), format="wav")
        to_be_merged.export("export/{}.mp3".format(group_key.strftime("%Y-%m-%d")), format="mp3")
    print("DONE | Your merged voice messages are located in 'export' directory!")

def main(args=None):
    print("\nThis tool merges facebook voice messages by date. For more infos and cotribution visit: ")
    print("Developed by smolikja: https://github.com/smolikja")
    print("==================================================")
    # # for debug
    # logging.basicConfig(filename="std.log",
    #                     format='%(asctime)s %(message)s',
    #                     filemode='w',
    #                     level= logging.DEBUG)

    # Files into dictionary {<datetime: created> : <str: file name>}
    dict_voice_files = get_voice_files()

    # Files into dictionary {<datetime: group time> : {<datetime: created> : <str: file name>}}
    dict_grouped_files = group_files_by_date(dict_voice_files)

    # Merge and export audio files
    process_audio_files(dict_grouped_files)

    print("Press any key to exit.")
    msvcrt.getch()

if __name__ == '__main__':
    main()