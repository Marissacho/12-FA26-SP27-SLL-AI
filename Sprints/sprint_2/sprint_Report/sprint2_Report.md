# Sprint 2 Report (October 12th to November 11th)

## YouTube link of Sprint * Video (Make this video unlisted)

## What's New (User Facing)
 * Obtained server space for storing corpus data and fine-tuning models and set up remote access for every team member.
 * Created a TalkBank audio downloader that downloads an entire corpus with one command, skips files that are already downloaded, retries failed downloads, and checks corpus size before downloading.
 * Created a TalkBank transcript downloader to download and extract .cha files from a corpus.
 * Updated the client's .cha to .rttm conversion scripts to work with different corpora using TOML configuration files, and added configurations for 12 corpora.
 * Added speaker label checks to catch blank or misspelled labels before they end up in the .rttm files.
 * Fixed several conversion issues, including duplicate file names in different folders, overlapping segments, multi-line speech, files without timed speech, and unmapped speakers.
 * Created a script to calculate the total hours of audio available for each corpus.
 * Worked on the system architecture, including a component diagram and documentation for each subsystem.

## Work Summary (Developer Facing)
Sprint 2 moved the team from planning into implementation. After obtaining server space through VCEA, we each set up remote SSH access and cloned the repository on the server. Half of our team worked on building the data pipeline. We started by downloading audio and transcripts from TalkBank, then worked together to prepare the scripts that generate the final .rttm files for fine-tuning in the upcoming sprint. The main challenge was that these scripts were originally hard-coded for the VanDam-5minute corpus. We updated them to use separate configuration files for each corpus, which revealed several issues with other corpora, such as repeated file names and transcript entries spanning multiple lines. We fixed these issues as we found them. Privacy is important as all data stays on restricted server storage, new files are only accessible to the project group, and audio and transcript files are excluded from GitHub.

## Unfinished Work
The following issues were not completed during Sprint 2 and have been moved into the appropriate stages of the Kanban board for continued work in Sprint 3:

* PyTorch is in [Ready] and assigned to Marissa and Quan. The team prioritized setting up the server and building the data pipeline, which the PyTorch practice experiment depends on.

## Completed Issues/User Stories

Here are links to the issues that we completed in this sprint:

* [Get Server Space](https://github.com/Marissacho/12-FA26-SP27-SLL-AI/issues/8)
* [Environment Setup](https://github.com/Marissacho/12-FA26-SP27-SLL-AI/issues/10)
* [Data Ingestion](https://github.com/Marissacho/12-FA26-SP27-SLL-AI/issues/1)
* [Data Conversion](https://github.com/Marissacho/12-FA26-SP27-SLL-AI/issues/5)
* [Data Cleansing](https://github.com/Marissacho/12-FA26-SP27-SLL-AI/issues/3)

## Incomplete Issues/User Stories

Here are links to issues we worked on but did not complete in this sprint:

* [PyTorch](https://github.com/Marissacho/12-FA26-SP27-SLL-AI/issues/6) We prioritized setting up the server and building the data pipeline, which the PyTorch practice experiment depends on, so it was moved to Sprint 3.

## Code Files for Review
Please review the following code files, which were actively developed during this sprint, for quality:

* [talkbank_audio_scrapper.py](https://github.com/Marissacho/12-FA26-SP27-SLL-AI/blob/main/data_preparation/talkbank_audio_scrapper.py)
* [talkbank_transcript_scrapper.py](https://github.com/Marissacho/12-FA26-SP27-SLL-AI/blob/main/data_preparation/talkbank_transcript_scrapper.py)
* [map_cha_to_rttm.py](https://github.com/Marissacho/12-FA26-SP27-SLL-AI/blob/main/data_preparation/cha_to_rttm/map_cha_to_rttm.py)
* [cha_vtc_map_by_file.py](https://github.com/Marissacho/12-FA26-SP27-SLL-AI/blob/main/data_preparation/cha_to_rttm/cha_vtc_map_by_file.py)
* [calculate_audio_hours.py](https://github.com/Marissacho/12-FA26-SP27-SLL-AI/blob/main/data_preparation/calculate_audio_hours.py)

## Retrospective Summary
Here's what went well:
* We obtained server space and every member can work in the same environment.
* The data pipeline now runs from TalkBank download to reference .rttm files.
* Configuration files let us add corpora without changing code.
* We have 3000 hours of data in our server

Here's what we'd like to improve:
* Assign milestones, story points, and assignees to every issue.
* Start PyTorch earlier so it does not block fine-tuning.
* Adjust dataset so that data that could cause problems is removed/watched carefully

Here are changes we plan to implement in the next sprint:
* Identify and implement appropriate evaluation metrics to measure model performance
* Begin training and testing the selected model using the available data
* Use the evaluation results to identify areas for improvement and refine the model that we choose to move forward with
