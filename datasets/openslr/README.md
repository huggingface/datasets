---
annotations_creators:
- crowdsourced
language_creators:
- crowdsourced
languages:
- "jv"
- "km"
- "ne"
- "su"
licenses:
- Creative Commons Attribution-ShareAlike 4.0
multilinguality:
- multilingual
size_categories:
- 100K<n<1M
source_datasets:
- openslr
task_categories:
- other
task_ids:
- other-other-automatic-speech-recognition
---

# Dataset Card for common_voice

## Table of Contents
- [Dataset Description](#dataset-description)
  - [Dataset Summary](#dataset-summary)
  - [Supported Tasks](#supported-tasks-and-leaderboards)
  - [Languages](#languages)
- [Dataset Structure](#dataset-structure)
  - [Data Instances](#data-instances)
  - [Data Fields](#data-instances)
  - [Data Splits](#data-instances)
- [Dataset Creation](#dataset-creation)
  - [Curation Rationale](#curation-rationale)
  - [Source Data](#source-data)
  - [Annotations](#annotations)
  - [Personal and Sensitive Information](#personal-and-sensitive-information)
- [Considerations for Using the Data](#considerations-for-using-the-data)
  - [Social Impact of Dataset](#social-impact-of-dataset)
  - [Discussion of Biases](#discussion-of-biases)
  - [Other Known Limitations](#other-known-limitations)
- [Additional Information](#additional-information)
  - [Dataset Curators](#dataset-curators)
  - [Licensing Information](#licensing-information)
  - [Citation Information](#citation-information)

## Dataset Description

- **Homepage:** https://www.openslr.org/
- **Repository:** [Needs More Information]
- **Paper:** [Needs More Information]
- **Leaderboard:** [Needs More Information]
- **Point of Contact:** [Needs More Information]

### Dataset Summary

OpenSLR is a site devoted to hosting speech and language resources, such as training corpora for speech recognition, 
and software related to speech recognition. Currently, following resources are available: 

#### SLR41: High quality TTS data for Javanese.
This data set contains high-quality transcribed audio data for Javanese. The data set consists of wave files, 
and a TSV file. The file line_index.tsv contains a filename and the transcription of audio in the file. Each 
filename is prepended with a speaker identification number.

The data set has been manually quality checked, but there might still be errors.

This dataset was collected by Google in collaboration with Gadjah Mada University in Indonesia.

#### SLR42: High quality TTS data for Khmer.
This data set contains high-quality transcribed audio data for Khmer. The data set consists of wave files, 
and a TSV file. The file line_index.tsv contains a filename and the transcription of audio in the file. 
Each filename is prepended with a speaker identification number.

The data set has been manually quality checked, but there might still be errors.

This dataset was collected by Google.

#### SLR43: High quality TTS data for Nepali.
This data set contains high-quality transcribed audio data for Nepali. The data set consists of wave files, 
and a TSV file. The file line_index.tsv contains a filename and the transcription of audio in the file. 
Each filename is prepended with a speaker identification number.

The data set has been manually quality checked, but there might still be errors.

This dataset was collected by Google in Nepal.

#### SLR44: High quality TTS data for Sundanese.
This data set contains high-quality transcribed audio data for Sundanese. The data set consists of wave files, 
and a TSV file. The file line_index.tsv contains a filename and the transcription of audio in the file. 
Each filename is prepended with a speaker identification number.

The data set has been manually quality checked, but there might still be errors.

This dataset was collected by Google in collaboration with Universitas Pendidikan Indonesia.

### Supported Tasks and Leaderboards

[Needs More Information]

### Languages

Javanese, Khmer, Nepali, Sundanese

## Dataset Structure

### Data Instances

A typical data point comprises the path to the audio file, called path and its sentence. 

#### SLR41, SLR42, SLR43, SLR44 
```
{
  'path': 'suf_00297_00037352660'
  'sentence': 'Panonton ting haruleng ningali Kelly Clarkson keur nyanyi di tipi',
}
```

### Data Fields

path: The path to the audio file

sentence: The sentence the user was prompted to speak

### Data Splits

The speech material has only train dataset.

## Dataset Creation

### Curation Rationale

[Needs More Information]

### Source Data

#### Initial Data Collection and Normalization

[Needs More Information]

#### Who are the source language producers?

[Needs More Information]

### Annotations

#### Annotation process

[Needs More Information]

#### Who are the annotators?

[Needs More Information]

### Personal and Sensitive Information

[Needs More Information]

## Considerations for Using the Data

### Social Impact of Dataset

[Needs More Information]

### Discussion of Biases

[More Information Needed] 

### Other Known Limitations

[More Information Needed] 

## Additional Information

### Dataset Curators

[More Information Needed] 

### Licensing Information

[More Information Needed] 

### Citation Information

#### SLR41, SLR42, SLR43, SLR44 
```
@inproceedings{kjartansson-etal-tts-sltu2018,
    title = {{A Step-by-Step Process for Building TTS Voices Using Open Source Data and Framework for Bangla, Javanese, Khmer, Nepali, Sinhala, and Sundanese}},
    author = {Keshan Sodimana and Knot Pipatsrisawat and Linne Ha and Martin Jansche and Oddur Kjartansson and Pasindu De Silva and Supheakmungkol Sarin},
    booktitle = {Proc. The 6th Intl. Workshop on Spoken Language Technologies for Under-Resourced Languages (SLTU)},
    year  = {2018},
    address = {Gurugram, India},
    month = aug,
    pages = {66--70},
    URL   = {http://dx.doi.org/10.21437/SLTU.2018-14}
  }
```
