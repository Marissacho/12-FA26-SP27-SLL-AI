# 12-FA26-SP27-SLL-AI

## Project summary

### One-sentence description of the project

Our project aims to improve AI speaker segmentation models to more accurately identify children's speech in audio recordings, making early childhood speech research more efficient.

### Additional information about the project

AI speaker segmentation models struggle to accurately distinguish young children's voices from adult voices. This makes it harder to have accurate analysis of recordings from HomeBank. HomeBank is where all of the audio recordings are stored from past experiments that have been done. Our project focuses on improving the existing AI models to identify and separate different speakers in audio recordings, especially the young children speaking in those recordings. Our team will evaluate and fine-tune models to improve their accuracy and performance. Our goal is to reduce the need for manual audio analysis and help researchers better understand childhood speech.

## Installation

### Prerequisites
- Must have access to compute power large enough to train a ML Model.

### Add-ons

- Required to have access to HomeBank to view the recordings

## Installation
 
### Prerequisites
- Must have access to compute power large enough to train a ML Model.
### Add-ons
 
- Required to have access to HomeBank to view the recordings
### Installation Steps
 
- Clone the GitHub repository
- Create python environment and install dependencies.
```bash
  python3 -m venv .venv
  source .venv/bin/activate
  pip install -r requirements.txt
```
 
#### Steps to run data_preparation scripts
 
##### talkbank_audio_scrapper
```bash
python data_preparation/talkbank_audio_scrapper.py homebank Password/<Corpus> --list #to check the size of a corpus
python data_preparation/talkbank_audio_scrapper.py homebank Password/<Corpus> #to download a corpus
```
 
##### talkbank_transcript_scrapper
```bash
python data_preparation/talkbank_transcript_scrapper.py homebank Password/<Corpus>
```
 
##### Arguments for the download scripts
- `<database>`: `homebank`, `childes`, or `phon`
- `<corpus path>`: the part of the TalkBank URL after the database name (e.g. `Password/DavisKean`, `Public/VanDam-5minute`, `Eng-NA/Brent`)
- Both scripts ask for your TalkBank email and password when they start (the password is hidden as you type)
- Audio is saved to `/mnt/na1/eecs/srdesign/csar/data/raw/<Corpus>/recordings/`, set by `DOWNLOAD_DIR` at the top of `talkbank_audio_scrapper.py`
- Transcripts are saved and unzipped to `/mnt/na1/eecs/srdesign/csar/data/raw/<Corpus>/transcripts/`
- Rerunning a download skips files that are already there
```bash
python data_preparation/talkbank_audio_scrapper.py childes Eng-NA/<Corpus> #to download a CHILDES corpus
python data_preparation/talkbank_transcript_scrapper.py homebank Password/<Corpus> --list #to check the transcript zip's size
python data_preparation/talkbank_transcript_scrapper.py homebank Password/<Corpus> --delete-zip #to delete the zip after unzipping
```
 
##### check_corpus_sizes
Checks the audio size of every corpus listed in `data_preparation/corpora_to_check.txt` (one `<database> <corpus path>` per line). Downloads nothing.
```bash
python data_preparation/check_corpus_sizes.py
```
 
##### audio_hours
Prints the number of WAV files and total hours of audio for each corpus in `data/raw/`.
```bash
python data_preparation/audio_hours.py
python data_preparation/audio_hours.py <raw folder> #to check a different folder
```
 
#### Steps to convert transcripts (.cha) to RTTM labels
 
Each corpus has a config file in `configs/corpora/<Corpus>.toml` with its paths and regular expressions:
```toml
name = "<Corpus>"
 
[paths]
transcripts = "/mnt/na1/eecs/srdesign/csar/data/raw/<Corpus>/transcripts"
output      = "/mnt/na1/eecs/srdesign/csar/data/processed/<Corpus>"
 
[regex]
speaker_id = '(.+)<language>\|<corpus name>\|([A-Z0-9]+\|*.+)'
utterance  = '\*([A-Z0-9]+).+\x15(\d+_\d+)'
```
To fill in `speaker_id`, look at one `@ID` line in the corpus's `.cha` files and copy its language and corpus fields (e.g. `eng\|Brent\|`):
```bash
grep -rh "^@ID:" <transcripts folder> | cut -d'|' -f1,2 | sort | uniq -c
```
 
##### 1. cha_speaker_list
Lists every speaker type in the corpus and writes `cha_to_vtc2_speaker_map.csv` to the output folder.
```bash
python data_preparation/cha_to_rttm/cha_speaker_list.py configs/corpora/<Corpus>.toml
```
 
##### Label the speakers
Add a label column after the speaker column in `cha_to_vtc2_speaker_map.csv`, give every row one of `KCHI`, `OCH`, `FEM`, `MAL`, or `SIL` (not a speaker; left out of the RTTMs), and save it as `cha_to_vtc2_speaker_map_done.csv` in the same folder.
 
##### 2. cha_vtc_map_by_file
Builds `cha_file_to_speakers.json`, the speaker labels for each transcript. Stops and names the row if a label is blank or misspelled.
```bash
python data_preparation/cha_to_rttm/cha_vtc_map_by_file.py configs/corpora/<Corpus>.toml
```
 
##### 3. map_cha_to_rttm
Writes one RTTM file per transcript to `<output>/rttm/`. Prints a `WARNING` for any speaker missing from the map.
```bash
mkdir -p logs
python data_preparation/cha_to_rttm/map_cha_to_rttm.py configs/corpora/<Corpus>.toml > logs/rttm_<Corpus>.txt
```
 
See `data_preparation/cha_to_rttm/KNOWN_ISSUES.md` for the checks to run after converting a corpus.
 
#### Fine-tuning environment (segma)
 
Clone segma into your home folder (not inside this repository, and not in `csar`) and check out the version this project uses:
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh #to install uv
source ~/.bashrc
cd ~
git clone https://github.com/arxaqapi/segma.git
cd segma
git checkout fe45b66b19b1f44675add0fa708e83df35e5346e
uv venv .venv-finetuning
source .venv-finetuning/bin/activate
uv sync --active
python -c "import torch; print(torch.cuda.is_available(), torch.cuda.device_count())" #should print True 2
```

## Functionality

- Python program runs
- Excel sheet is exported
- audio recordings are organized with the participants identified

## Known Problems

- We still have to manually insert some information into the excel sheet because not all of the information correctly is identified from the audio recordings
- Understanding the data and recordings that we are presented with and make sure that privacy is HIGHLY taken into account
- Understanding and comparing the metric data from previous research done 
