# Mapping Speakers from VanDam-5minute Corpus to VTC2-Compatible Speaker IDs

Resources:

[VanDam-5minute Dataset](https://talkbank.org/homebank/access/Public/VanDam-5minute.html)

[VTC2.0 Speaker Type Info](https://github.com/LAAC-LSCP/VTC/blob/main/README.md)

## What is the Process for Generating RTTM files from CHA files?

### Get a List of Speakers from the original Transcripts (cha files)
Create a csv file with each row containing: a speaker type including gender if available, a space for the VTC speaker type to map to, and a list of files where that cha speaker type was found.

file: cha_speaker_list.py

### Manually Map cha Speaker Types to VTC2.0 Speaker Types

Open the csv and map the speaker types.  If there isn't enough information in the cha speaker type field, you need to listen to the audio in one of the file to tell how to map it.  When the mapping is complete, append "_Done" to the file name and save as "csv".

### Rewrite the csv to a list of input wav file names and the speaker types found in them.

file: cha_vtc_map_by_file.py - Create a table of cha files to map the file's speaker codes to codes needed for VTC output evaluation.  This script outputs a json file with each wav file's anticipated speaker type mapping.

### Write the rttm file out for each WAV file to indcate the segmentations to expect for gold standard data.

file: map_cha_to_rttm.py - read .cha files and output a matching rttm file.

now that we know the speaker mappings, we go back to the gold standard cha files and, for each line in the cha file transcript:

1. Get the speaker type code and the segmentation data (start time and duration of speech)
2. Translate the speaker type to VTC.
3. Write out a line to a corresponding rttm file.  The rttms match exactly to the cha files but are created in a different directory tree.


;;








