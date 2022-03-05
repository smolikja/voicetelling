# import logging
import msvcrt
import os
from datetime import datetime, timedelta, time
import sys
from pydub import AudioSegment, effects  
import shutil

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path,
                        relative_path)

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

def group_files_by_date(ungrouped_files, date_range):
    grouped_files = {}

    for date in ungrouped_files:
        group_date = datetime.date(date)
        if datetime.time(date) < time(5, 0, 0):
            group_date = group_date - timedelta(days=1)

        if date_range[0] <= group_date <= date_range[1]:
            if group_date in grouped_files.keys():
                grouped_files[group_date][date] = ungrouped_files[date]
            else:
                grouped_files[group_date] = {date : ungrouped_files[date]}

    return grouped_files

# Print iterations progress
def printProgressBar (iteration, total, prefix = 'Progress:', suffix = 'Complete', decimals = 1, length = 50, fill = '▒', printEnd = "\r"):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end = printEnd)
    # Print New Line on Complete
    if iteration == total: 
        print()

def process_audio_files(grouped_files):
    print("This takes a while, merging is in progress...\n")
    printProgressBar(0,
                    len(grouped_files.keys()))

    if os.path.isdir("export"):
        shutil.rmtree("export")
    os.mkdir("export")

    for group_key in grouped_files:
        to_be_merged = AudioSegment.empty()

        for file_key in grouped_files[group_key]:
            to_be_merged += AudioSegment.from_file(grouped_files[group_key][file_key],
                                                format="mp4")

        to_be_merged += AudioSegment.from_file(resource_path("beep.wav"), format="wav")

        normalized_audio = effects.normalize(to_be_merged)
        normalized_audio.export("export/{}.mp3".format(group_key.strftime("%Y-%m-%d")), format="mp3")

        printProgressBar(list(grouped_files).index(group_key) + 1,
                            len(grouped_files.keys()))

    print("\nDONE | Your merged voice messages are located in 'export' directory!")

def is_valid_range_date_format(str_date):
    try:
        datetime.strptime(str_date, '%Y.%m.%d')
        return True
    except ValueError:
        return False

# Get date range from user
def get_process_range():
    range = [datetime(1900, 1, 1).date(), datetime(3000, 1, 1).date()]

    range_from_str = input("Process messages from [yyyy.mm.dd] (empty for no limit): ")
    while range_from_str != '' and not is_valid_range_date_format(range_from_str):
        range_from_str = input("typo ► Process messages from [yyyy.mm.dd] (empty for no limit): ")

    if range_from_str != '':
        range[0] = datetime.strptime(range_from_str, '%Y.%m.%d').date()

    range_to_str = input("Process messages to [yyyy.mm.dd] (empty for no limit): ")
    while range_to_str != '' and not is_valid_process_range_date_format(range_to_str):
        range_to_str = input("typo ► Process messages to [yyyy.mm.dd] (empty for no limit): ")

    if range_to_str != '':
        range[1] = datetime.strptime(range_to_str, '%Y.%m.%d').date()

    return range
    

def main(args=None):
    print("          ╔════════════════════════════════╗")
    print("          ║          Voicetelling          ║")  
    print("          ╚════════════════════════════════╝")
    print("This tool merges facebook voice messages by date into stories.")
    print("► url") # TODO: repository url
    print("Developed by smolikja: https://github.com/smolikja")
    print("==================================================")

    # # for debug
    # logging.basicConfig(filename="std.log",
    #                     format='%(asctime)s %(message)s',
    #                     filemode='w',
    #                     level= logging.DEBUG)

    # Files into dictionary {<datetime: created> : <str: file name>}
    dict_voice_files = get_voice_files()

    if bool(dict_voice_files):
        range = get_process_range()

        # Files into dictionary {<datetime: group time> : {<datetime: created> : <str: file name>}}
        dict_grouped_files = group_files_by_date(dict_voice_files, date_range= range)

        # Merge and export audio files
        process_audio_files(dict_grouped_files)
    else:
        print("\n>>> No voice files found. <<<\n")

    print("Press any key to exit.")
    msvcrt.getch()

if __name__ == '__main__':
    main()