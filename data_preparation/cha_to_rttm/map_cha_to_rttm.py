# map_cha_to_rttm.py - read .cha files and output a matching rttm file.

import glob
import re
import os
import os.path
import json
import csv
import itertools

BASE_PATH = "/media/joe/slepnir1/Datasets/ALSSA/VanDam-5minute"
CHA_BASE_PATH = os.path.join(BASE_PATH, "VanDam-5minute")
MAP_PATH = os.path.join(BASE_PATH, "cha_file_to_speakers.json")

def compress_list_rows(lst):
    last = len(lst)-1

    i = 0
    current = lst[i]
    while i < last:
        i += 1
        nxt = lst[i]
        if current[0] == nxt[0]:
            current[2] += nxt[2]
        else:
            yield current
            current = nxt
    # last item
    yield current


def read_speaker_map(pth):
    with open(pth, "r") as spfd:
        return json.load(spfd)

def str_to_decimal(str):
    return float(str)/1000 # the string is in milliseconds

def safe_mkdir(pth):
    if not os.path.isdir(pth):
        os.mkdir(pth)
    return pth

# create the output directory for rttm if it doesn't exist
OUT_PATH = safe_mkdir(os.path.join(BASE_PATH, "rttm"))

pattern = re.compile(r"\*([A-Z0-9]+).+\x15(\d+_\d+)") # cha speech segment pattern. x15 is a control character in the cha file (ctrl-U)

files = glob.glob(BASE_PATH + '/**/*.cha', recursive=True)

sp_map = read_speaker_map(MAP_PATH)
cha_speakers = {}
for pth in files:
    cha_filename = os.path.split(pth)[1]
    cha_dir = cha_filename[0:4]
    cha_name = os.path.splitext(cha_filename)[0]
    # make sure the write directory esists
    rttm_dir = safe_mkdir(os.path.join(OUT_PATH, cha_dir))

    #read the list of speech segments from the .cha file
    cha_segs = []
    with open(pth, "r") as rfd:
        for line in rfd:
            m = pattern.match(line)
            if m is not None:
                speaker = m[1]
                start, end = m[2].split('_')
                start_sp = str_to_decimal(start)
                end_sp = str_to_decimal(end)
                duration = round(end_sp - start_sp, 3)
                #print(speaker, start_sp, duration)

                rttm_speaker = sp_map[cha_filename][speaker]
                #print(rttm_speaker)
                cha_segs.append([rttm_speaker, start_sp, duration])

        # compress the lines when consecutive speakers are identical
        compressed = [x for x in compress_list_rows(cha_segs)]

        with open(os.path.join(rttm_dir, cha_name + ".rttm"), "w") as rttm:
            for seg in compressed:
                speaker = seg[0]
                start = seg[1]
                duration = seg[2]

                print(cha_name, start, duration, speaker)

                line = f"SPEAKER {cha_name} 1 {start:4.3f} {duration:4.3f} <NA> <NA> {speaker} <NA> <NA>\n"
                rttm.write(line)
                print(line)




