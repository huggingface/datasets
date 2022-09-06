---
pretty_name: MultiLingual LibriSpeech
annotations_creators:
- expert-generated
language_creators:
- crowdsourced
- expert-generated
language:
- de
- es
- fr
- it
- nl
- pl
- pt
license:
- cc-by-4.0
multilinguality:
- multilingual
paperswithcode_id: librispeech-1
size_categories:
- 100K<n<1M
source_datasets:
- original
task_categories:
- automatic-speech-recognition
- audio-classification
task_ids:
- speaker-identification
---

# Dataset Card for MultiLingual LibriSpeech

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

- **Homepage:** [MultiLingual LibriSpeech ASR corpus](http://www.openslr.org/94)
- **Repository:** [Needs More Information]
- **Paper:** [MLS: A Large-Scale Multilingual Dataset for Speech Research](https://arxiv.org/abs/2012.03411)
- **Leaderboard:** [Paperswithcode Leaderboard](https://paperswithcode.com/dataset/multilingual-librispeech)

### Dataset Summary

Multilingual LibriSpeech (MLS) dataset is a large multilingual corpus suitable for speech research. The dataset is derived from read audiobooks from LibriVox and consists of 8 languages - English, German, Dutch, Spanish, French, Italian, Portuguese, Polish.

### Supported Tasks and Leaderboards

- `automatic-speech-recognition`, `audio-speaker-identification`: The dataset can be used to train a model for Automatic Speech Recognition (ASR). The model is presented with an audio file and asked to transcribe the audio file to written text. The most common evaluation metric is the word error rate (WER). The task has an active leaderboard which can be found at https://paperswithcode.com/dataset/multilingual-librispeech and ranks models based on their WER.

### Languages

The dataset is derived from read audiobooks from LibriVox and consists of 8 languages - English, German, Dutch, Spanish, French, Italian, Portuguese, Polish

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

|                             | Train | Train.9h | Train.1h  | Dev | Test |
| -----                       | ------ | ----- | ---- | ---- | ---- | 
| german | 469942 | 2194 | 241 | 3469 | 3394 |
| dutch | 374287 | 2153 | 234 | 3095 | 3075 |
| french | 258213 | 2167 | 241 | 2416 | 2426 |
| spanish | 220701 | 2110 | 233 | 2408 | 2385 |
| italian | 59623 | 2173 | 240 | 1248 | 1262 |
| portuguese | 37533 | 2116 | 236 | 826 | 871 |
| polish | 25043 | 2173 | 238 | 512 | 520 |



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

[Needs More Information]

### Licensing Information

Public Domain, Creative Commons Attribution 4.0 International Public License ([CC-BY-4.0](https://creativecommons.org/licenses/by/4.0/legalcode))

### Citation Information

```
@article{Pratap2020MLSAL,
  title={MLS: A Large-Scale Multilingual Dataset for Speech Research},
  author={Vineel Pratap and Qiantong Xu and Anuroop Sriram and Gabriel Synnaeve and Ronan Collobert},
  journal={ArXiv},
  year={2020},
  volume={abs/2012.03411}
}
```

### Contributions

Thanks to [@patrickvonplaten](https://github.com/patrickvonplaten) for adding this dataset.
