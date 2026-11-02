# map_cha_to_rttm.py - read .cha files and output a matching rttm file.

import glob
import re
import os
import os.path
import json
import csv
import itertools
import sys
import tomllib

# Usage: python <this script> configs/corpora/<Corpus>.toml
with open(sys.argv[1], "rb") as cfg_fd:
    CONFIG = tomllib.load(cfg_fd)

BASE_PATH = CONFIG["paths"]["output"]
CHA_BASE_PATH = CONFIG["paths"]["transcripts"]
MAP_PATH = os.path.join(BASE_PATH, "cha_file_to_speakers.json")

def compress_list_rows(lst):
    if not lst:  # fix #5: a file with no timed utterances
        return
    last = len(lst)-1

    i = 0
    current = lst[i]
    while i < last:
        i += 1
        nxt = lst[i]
        # fix #2: merge only when the next segment touches or overlaps this one,
        # and end the merged segment where the later one ends
        if current[0] == nxt[0] and nxt[1] <= current[1] + current[2]:
            current[2] = round(max(current[1] + current[2], nxt[1] + nxt[2]) - current[1], 3)
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
    os.makedirs(pth, exist_ok=True)  # also creates nested folders
    return pth

# create the output directory for rttm if it doesn't exist
OUT_PATH = safe_mkdir(os.path.join(BASE_PATH, "rttm"))

pattern = re.compile(CONFIG["regex"]["utterance"]) # cha speech segment pattern. x15 is a control character in the cha file (ctrl-U)

files = glob.glob(CHA_BASE_PATH + '/**/*.cha', recursive=True)

sp_map = read_speaker_map(MAP_PATH)
cha_speakers = {}
for pth in files:
    # fix #1: use the file's folder inside the transcripts folder, not filename[0:4]
    cha_filename = os.path.relpath(pth, CHA_BASE_PATH)
    cha_dir = os.path.dirname(cha_filename)
    cha_name = os.path.splitext(os.path.basename(cha_filename))[0]
    # older speaker maps list bare file names, so fall back to the name alone
    file_map = sp_map.get(cha_filename, sp_map.get(os.path.basename(cha_filename), {}))
    # make sure the write directory esists
    rttm_dir = safe_mkdir(os.path.join(OUT_PATH, cha_dir))

    #read the list of speech segments from the .cha file
    cha_segs = []
    with open(pth, "r") as rfd:
        # fix #3: join continuation lines (they start with a tab) onto their utterance,
        # so a time bullet on the second line isn't missed
        text = rfd.read().replace("\r\n", "\n").replace("\n\t", " ")
        for line in text.split("\n"):
            m = pattern.match(line)
            if m is not None:
                speaker = m[1]
                start, end = m[2].split('_')
                start_sp = str_to_decimal(start)
                end_sp = str_to_decimal(end)
                duration = round(end_sp - start_sp, 3)
                #print(speaker, start_sp, duration)

                rttm_speaker = file_map.get(speaker)
                if rttm_speaker is None:  # fix #6: warn and skip instead of crashing
                    print(f"WARNING: {cha_filename}: speaker {speaker} isn't in the speaker map, skipped")
                    continue
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