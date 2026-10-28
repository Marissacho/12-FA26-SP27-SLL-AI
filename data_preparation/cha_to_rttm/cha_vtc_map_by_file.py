# cha_vtc_map_by_file.py - Create a table of cha files to map
# the file's speaker codes to codes needed for VTC training.

import os.path
import csv
import re
import json

BASE_PATH = "/media/joe/slepnir1/Datasets/ALSSA/VanDam-5minute"
OUT_PATH_JSON = os.path.join(BASE_PATH, "cha_file_to_speakers.json")
IN_PATH_CSV = os.path.join(BASE_PATH, "cha_to_vtc2_speaker_map_done.csv")

line_pattern = re.compile(r"\'([^']+)\'")  # parse file names
cha_speaker_pattern = re.compile(r"[^,]+") # select the cha speaker code

def get_file_list(lst):
    return [m[1] for m in line_pattern.finditer(lst) if m is not None]

ctov_map = {}
with open(IN_PATH_CSV) as fd:
    reader = csv.reader(fd)
    for row in reader:
        cha_speaker = cha_speaker_pattern.match(row[0])[0]
        vtc_speaker = row[1]

        for cha in get_file_list(row[2]):
            if cha not in ctov_map:
                ctov_map[cha] = {}

            if cha_speaker not in ctov_map[cha]:
                ctov_map[cha][cha_speaker] = vtc_speaker

with open(OUT_PATH_JSON, "w") as fd:
    json.dump(ctov_map, fd)

#for (cha, map_lst) in ctov_map.items():
#    print(f"{cha} -> {map_lst}")








