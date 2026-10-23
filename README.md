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

## Functionality

- Python program runs
- Excel sheet is exported
- audio recordings are organized with the participants identified

## Known Problems

- We still have to manually insert some information into the excel sheet because not all of the information correctly is identified from the audio recordings
- Understanding the data and recordings that we are presented with and make sure that privacy is HIGHLY taken into account
- Understanding and comparing the metric data from previous research done 
