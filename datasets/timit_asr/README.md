---
annotations_creators:
- expert-generated
language_creators:
- expert-generated
languages:
- en
licenses:
- LDC User Agreement for Non-Members
multilinguality:
- monolingual
size_categories:
- 1K<n<10K
source_datasets:
- original
task_categories:
- other
task_ids:
- other-other-automatic speech recognition
---

# Dataset Card for timit_asr

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

- **Homepage:** [TIMIT Acoustic-Phonetic Continuous Speech Corpus](https://catalog.ldc.upenn.edu/LDC93S1)
- **Repository:** [Needs More Information]
- **Paper:** [TIMIT: Dataset designed to provide speech data for acoustic-phonetic studies and for the development and evaluation of automatic speech recognition systems.](https://catalog.ldc.upenn.edu/LDC93S1)
- **Leaderboard:** [Paperswithcode Leaderboard](https://paperswithcode.com/sota/speech-recognition-on-timit)
- **Point of Contact:** [Needs More Information]

### Dataset Summary

The TIMIT corpus of read speech is designed to provide speech data for acoustic-phonetic studies and for the development and evaluation of automatic speech recognition systems. TIMIT contains broadband recordings of 630 speakers of eight major dialects of American English, each reading ten phonetically rich sentences. The TIMIT corpus includes time-aligned orthographic, phonetic and word transcriptions as well as a 16-bit, 16kHz speech waveform file for each utterance. Corpus design was a joint effort among the Massachusetts Institute of Technology (MIT), SRI International (SRI) and Texas Instruments, Inc. (TI). The speech was recorded at TI, transcribed at MIT and verified and prepared for CD-ROM production by the National Institute of Standards and Technology (NIST).

### Supported Tasks and Leaderboards

- `automatic-speech-recognition`, `speaker-identification`: The dataset can be used to train a model for Automatic Speech Recognition (ASR). The model is presented with an audio file and asked to transcribe the audio file to written text. The most common evaluation metric is the word error rate (WER). The task has an active leaderboard which can be found at https://paperswithcode.com/sota/speech-recognition-on-timit and ranks models based on their WER.

### Languages

The audio is in English. 
The TIMIT corpus transcriptions have been hand verified. Test and training subsets, balanced for phonetic and dialectal coverage, are specified. Tabular computer-searchable information is included as well as written documentation.

## Dataset Structure

### Data Instances

A typical data point comprises the path to the audio file, usually called `file` and its transcription, called `text`. Some additional information about the speaker and the passage which contains the transcription is provided.

```
{
'file': wav_path,
'text': 'Would such an act of refusal be useful?',
'phonetic_detail': phonemes,
'word_detail': words,
'dialect_region': 'DR4',
'sentence_type': 'SI',
'speaker_id': 'MMDM0',
'id': '681'
```


### Data Fields

- file: A path to the downloaded audio file in .wav format.

- text: The transcription of the audio file.

- phonetic_detail: The phonemes that make up the sentence. The PHONCODE.DOC contains a table of all the phonemic and phonetic symbols used in TIMIT lexicon.

- word_detail: Word level split of the transcript.

- dialect_region: The dialect code of the recording.

- sentence_type: The type of the sentence - 'SA':'Dialect', 'SX':'Compact' or 'SI':'Diverse'.

- id: Unique id of the data sample. Contains the <SENTENCE_TYPE><SENTENCE_NUMBER>.  

- speaker_id: Unique id of the speaker. The same speaker id can be found for multiple data samples.


### Data Splits

The speech material has been subdivided into portions for training and
testing. The default train-test split will be made available on data download.

The test data alone has a core portion containing 24 speakers, 2 male and 1 female
from each dialect region. More information about the test set can 
be found [here](https://catalog.ldc.upenn.edu/docs/LDC93S1/TESTSET.TXT)


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

The dataset was created by John S. Garofolo, Lori F. Lamel, William M. Fisher, Jonathan G. Fiscus, David S. Pallett, Nancy L. Dahlgren, Victor Zue

### Licensing Information

LDC User Agreement for Non-Members

### Citation Information
```
@inproceedings{
  title={TIMIT Acoustic-Phonetic Continuous Speech Corpus},
  author={Garofolo, John S., et al},
  ldc_catalog_no={LDC93S1},
  DOI={https://doi.org/10.35111/17gk-bn40},
  journal={Linguistic Data Consortium, Philadelphia},
  year={1983}
}
```

### Contributions
Thanks to [@vrindaprabhu](https://github.com/vrindaprabhu) for adding this dataset.
