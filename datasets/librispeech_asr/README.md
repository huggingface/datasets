---
annotations_creators:
- expert-generated
language_creators:
- crowdsourced
- expert-generated
languages:
- en
licenses:
- cc-by-4.0
multilinguality:
- monolingual
size_categories:
- 100K<n<1M
source_datasets:
- original
task_categories:
- other
task_ids:
- other-other-automatic speech recognition
---

# Dataset Card for librispeech_asr

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
  - [Contributions](#contributions)

## Dataset Description

- **Homepage:** [LibriSpeech ASR corpus](http://www.openslr.org/12)
- **Repository:** [Needs More Information]
- **Paper:** [LibriSpeech: An ASR Corpus Based On Public Domain Audio Books](https://www.danielpovey.com/files/2015_icassp_librispeech.pdf)
- **Leaderboard:** [Paperswithcode Leaderboard](https://paperswithcode.com/sota/speech-recognition-on-librispeech-test-other)
- **Point of Contact:** [Daniel Povey](mailto:dpovey@gmail.com)

### Dataset Summary

LibriSpeech is a corpus of approximately 1000 hours of 16kHz read English speech, prepared by Vassil Panayotov with the assistance of Daniel Povey. The data is derived from read audiobooks from the LibriVox project, and has been carefully segmented and aligned.

### Supported Tasks and Leaderboards

- `automatic-speech-recognition`, `speaker-identification`: The dataset can be used to train a model for Automatic Speech Recognition (ASR). The model is presented with an audio file and asked to transcribe the audio file to written text. The most common evaluation metric is the word error rate (WER). The task has an active leaderboard which can be found at https://paperswithcode.com/sota/speech-recognition-on-librispeech-test-clean and ranks models based on their WER.

### Languages

The audio is in English. There are two configurations: `clean` and `other`. 
The speakers in the corpus were ranked according to the WER of the transcripts of a model trained on
a different dataset, and were divided roughly in the middle,
with the lower-WER speakers designated as "clean" and the higher WER speakers designated as "other".

## Dataset Structure

### Data Instances

A typical data point comprises the path to the audio file, usually called `file` and its transcription, called `text`. Some additional information about the speaker and the passage which contains the transcription is provided.

```
{'chapter_id': 141231,
 'file': '/home/patrick/.cache/huggingface/datasets/downloads/extracted/b7ded9969e09942ab65313e691e6fc2e12066192ee8527e21d634aca128afbe2/dev_clean/1272/141231/1272-141231-0000.flac',
 'id': '1272-141231-0000',
 'speaker_id': 1272,
 'text': 'A MAN SAID TO THE UNIVERSE SIR I EXIST'}
```


### Data Fields

- file: A path to the downloaded audio file in .flac format.

- text: the transcription of the audio file.

- id: unique id of the data sample.

- speaker_id: unique id of the speaker. The same speaker id can be found for multiple data samples.

- chapter_id: id of the audiobook chapter which includes the transcription.

### Data Splits

The size of the corpus makes it impractical, or at least inconvenient
for some users, to distribute it as a single large archive. Thus the
training portion of the corpus is split into three subsets, with approximate size 100, 360 and 500 hours respectively.
A simple automatic
procedure was used to select the audio in the first two sets to be, on
average, of higher recording quality and with accents closer to US
English. An acoustic model was trained on WSJ’s si-84 data subset
and was used to recognize the audio in the corpus, using a bigram
LM estimated on the text of the respective books. We computed the
Word Error Rate (WER) of this automatic transcript relative to our
reference transcripts obtained from the book texts.
The speakers in the corpus were ranked according to the WER of
the WSJ model’s transcripts, and were divided roughly in the middle,
with the lower-WER speakers designated as "clean" and the higher-WER speakers designated as "other".

For "clean", the data is split into train, validation, and test set. The train set is further split into train.100 and train.360
respectively accounting for 100h and 360h of the training data. 
For "other", the data is split into train, validation, and test set. The train set contains approximately 500h of recorded speech.

|                             | Train.500 | Train.360 | Train.100  | Valid | Test |
| -----                       | ------ | ----- | ---- | ---- | ---- | 
| clean | - | 104014 | 28539 |  2703 | 2620|
| other | 148688 | - | - | 2864 | 2939 |



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

[More Information Needed]

### Discussion of Biases

[More Information Needed]

### Other Known Limitations

[Needs More Information]

## Additional Information

### Dataset Curators

The dataset was initially created by Vassil Panayotov, Guoguo Chen, Daniel Povey, and Sanjeev Khudanpur.

### Licensing Information

CC BY 4.0

### Citation Information

[Needs More Information]

### Contributions

Thanks to [@patrickvonplaten](https://github.com/patrickvonplaten) for adding this dataset.