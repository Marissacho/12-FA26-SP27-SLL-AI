# audio_hours.py - Total length of the audio recordings for each corpus.
#
# Reads only each WAV file's header, so it's quick and doesn't load any audio.
# Non-WAV files (e.g. .mp3) are counted but not included in the hours.
#
# Usage
#   python data_preparation/calculate_audio_hours.py

import collections
import glob
import os
import sys
import wave

RAW_PATH = "/mnt/na1/eecs/srdesign/csar/data/raw"


def main():
    root = sys.argv[1] if len(sys.argv) > 1 else RAW_PATH
    if not os.path.isdir(root):
        sys.exit(f"Folder not found: {root}")

    hours = collections.Counter()
    wav_files = collections.Counter()
    other_files = collections.Counter()
    unreadable = []

    for corpus in sorted(os.listdir(root)):
        recordings = os.path.join(root, corpus, "recordings")
        if not os.path.isdir(recordings):
            continue
        for path in glob.glob(os.path.join(recordings, "**", "*"), recursive=True):
            if not os.path.isfile(path) or path.endswith(".part"):
                continue
            if path.lower().endswith(".wav"):
                try:
                    with wave.open(path) as w:
                        hours[corpus] += w.getnframes() / w.getframerate() / 3600
                        wav_files[corpus] += 1
                except (wave.Error, EOFError, OSError):
                    unreadable.append(path)
            else:
                other_files[corpus] += 1

    corpora = sorted(set(wav_files) | set(other_files))
    if not corpora:
        sys.exit(f"No recordings found under {root}/*/recordings/")

    print(f"{'corpus':20} {'wav files':>9} {'hours':>9}   other files")
    for c in corpora:
        print(f"{c:20} {wav_files[c]:>9} {hours[c]:>9.1f}   {other_files[c] or ''}")
    print(f"{'TOTAL':20} {sum(wav_files.values()):>9} {sum(hours.values()):>9.1f}   "
          f"{sum(other_files.values()) or ''}")

    if unreadable:
        print(f"\n{len(unreadable)} WAV files couldn't be read (non-standard format), e.g.:")
        for p in unreadable[:5]:
            print(f"  {p}")


if __name__ == "__main__":
    main()