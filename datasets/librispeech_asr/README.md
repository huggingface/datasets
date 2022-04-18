---
pretty_name: LibriSpeech
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
paperswithcode_id: librispeech-1
size_categories:
- 100K<n<1M
source_datasets:
- original
task_categories:
- automatic-speech-recognition
- audio-classification
task_ids:
- audio-speaker-identification
---

# Dataset Card for librispeech_asr

## Table of Contents
- [Dataset Description](#dataset-description)
  - [Dataset Summary](#dataset-summary)
  - [Supported Tasks and Leaderboards](#supported-tasks-and-leaderboards)
  - [Languages](#languages)
- [Dataset Structure](#dataset-structure)
  - [Data Instances](#data-instances)
  - [Data Fields](#data-fields)
  - [Data Splits](#data-splits)
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

- `automatic-speech-recognition`, `audio-speaker-identification`: The dataset can be used to train a model for Automatic Speech Recognition (ASR). The model is presented with an audio file and asked to transcribe the audio file to written text. The most common evaluation metric is the word error rate (WER). The task has an active leaderboard which can be found at https://paperswithcode.com/sota/speech-recognition-on-librispeech-test-clean and ranks models based on their WER.

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
  'audio': {'path': '/home/patrick/.cache/huggingface/datasets/downloads/extracted/b7ded9969e09942ab65313e691e6fc2e12066192ee8527e21d634aca128afbe2/dev_clean/1272/141231/1272-141231-0000.flac',
  'array': array([-0.00048828, -0.00018311, -0.00137329, ...,  0.00079346,
          0.00091553,  0.00085449], dtype=float32),
  'sampling_rate': 16000},
 'id': '1272-141231-0000',
 'speaker_id': 1272,
 'text': 'A MAN SAID TO THE UNIVERSE SIR I EXIST'}
```


### Data Fields

- file: A path to the downloaded audio file in .flac format.

- audio: A dictionary containing the path to the downloaded audio file, the decoded audio array, and the sampling rate. Note that when accessing the audio column: `dataset[0]["audio"]` the audio file is automatically decoded and resampled to `dataset.features["audio"].sampling_rate`. Decoding and resampling of a large number of audio files might take a significant amount of time. Thus it is important to first query the sample index before the `"audio"` column, *i.e.* `dataset[0]["audio"]` should **always** be preferred over `dataset["audio"][0]`.

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

The dataset consists of people who have donated their voice online. You agree to not attempt to determine the identity of speakers in this dataset.

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

[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)

### Citation Information

```
@inproceedings{panayotov2015librispeech,
  title={Librispeech: an ASR corpus based on public domain audio books},
  author={Panayotov, Vassil and Chen, Guoguo and Povey, Daniel and Khudanpur, Sanjeev},
  booktitle={Acoustics, Speech and Signal Processing (ICASSP), 2015 IEEE International Conference on},
  pages={5206--5210},
  year={2015},
  organization={IEEE}
}
```

### Contributions

Thanks to [@patrickvonplaten](https://github.com/patrickvonplaten) for adding this dataset.
