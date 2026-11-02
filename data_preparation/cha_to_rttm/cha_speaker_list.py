# cha_speaker_list.py - List out all the speaker info from
# gold-standard cha files in the vandam-5-minute dataset.
# find the dataset at 
# https://talkbank.org/homebank/access/Public/VanDam-5minute.html

import glob
import re
import os.path
import json
import csv
import sys
import tomllib

# Usage: python <this script> configs/corpora/<Corpus>.toml
with open(sys.argv[1], "rb") as cfg_fd:
    CONFIG = tomllib.load(cfg_fd)

########################### CONFIGURATION
BASE_PATH = CONFIG["paths"]["transcripts"]
OUT_BASE_PATH = CONFIG["paths"]["output"]
os.makedirs(OUT_BASE_PATH, exist_ok=True)
OUT_PATH_JSONL = os.path.join(OUT_BASE_PATH, "cha_speakers.jsonl")
OUT_PATH_CSV = os.path.join(OUT_BASE_PATH, "cha_to_vtc2_speaker_map.csv")

pattern = re.compile(CONFIG["regex"]["speaker_id"])
replace = re.compile(r"\|+")

files = glob.glob(BASE_PATH + '/**/*.cha', recursive=True)
###########################
cha_speakers = {}
for pth in files:
    filename = os.path.relpath(pth, BASE_PATH)  # fix #1: keep the folder, since CHILDES reuses file names
    with open(pth, "r") as fd:
        for line in fd:
            m = pattern.match(line)
            if m is not None:
                key = replace.sub(", ", m[2])
                if key not in cha_speakers:
                    cha_speakers[key] = []
                # record the key and where it was found 
                # in case we need to verify anything by 
                # listening to the file.
                cha_speakers[key].append(filename)

output_lst = []
for (key, val) in cha_speakers.items():
    print(f"{key} -> {val}")
    output_lst.append({key:val})

with open(OUT_PATH_JSONL, "w") as fd:
    for o in output_lst:
        fd.write(json.dumps(o)+'\n')

with open(OUT_PATH_CSV, "w") as fd:
    csv_file = csv.writer(fd, delimiter=',')
    for k, v in cha_speakers.items():
        csv_file.writerow([k, v])