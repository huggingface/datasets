---
pretty_name: TIMIT
annotations_creators:
- expert-generated
language_creators:
- expert-generated
language:
- en
license:
- other
license_details: "LDC-User-Agreement-for-Non-Members"
multilinguality:
- monolingual
size_categories:
- 1K<n<10K
source_datasets:
- original
task_categories:
- automatic-speech-recognition
task_ids: []
paperswithcode_id: timit
train-eval-index:
- config: clean
  task: automatic-speech-recognition
  task_id: speech_recognition
  splits:
    train_split: train
    eval_split: test
  col_mapping:
    file: path
    text: text
  metrics:
  - type: wer
    name: WER
  - type: cer
    name: CER
---

# Dataset Card for timit_asr

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

- **Homepage:** [TIMIT Acoustic-Phonetic Continuous Speech Corpus](https://catalog.ldc.upenn.edu/LDC93S1)
- **Repository:** [Needs More Information]
- **Paper:** [TIMIT: Dataset designed to provide speech data for acoustic-phonetic studies and for the development and evaluation of automatic speech recognition systems.](https://catalog.ldc.upenn.edu/LDC93S1)
- **Leaderboard:** [Paperswithcode Leaderboard](https://paperswithcode.com/sota/speech-recognition-on-timit)
- **Point of Contact:** [Needs More Information]

### Dataset Summary

The TIMIT corpus of read speech is designed to provide speech data for acoustic-phonetic studies and for the development and evaluation of automatic speech recognition systems. TIMIT contains broadband recordings of 630 speakers of eight major dialects of American English, each reading ten phonetically rich sentences. The TIMIT corpus includes time-aligned orthographic, phonetic and word transcriptions as well as a 16-bit, 16kHz speech waveform file for each utterance. Corpus design was a joint effort among the Massachusetts Institute of Technology (MIT), SRI International (SRI) and Texas Instruments, Inc. (TI). The speech was recorded at TI, transcribed at MIT and verified and prepared for CD-ROM production by the National Institute of Standards and Technology (NIST).

The dataset needs to be downloaded manually from https://catalog.ldc.upenn.edu/LDC93S1:

```
To use TIMIT you have to download it manually.
Please create an account and download the dataset from https://catalog.ldc.upenn.edu/LDC93S1
Then extract all files in one folder and load the dataset with:
`datasets.load_dataset('timit_asr', data_dir='path/to/folder/folder_name')`
```

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
    'file': '/data/TRAIN/DR4/MMDM0/SI681.WAV',
    'audio': {'path': '/data/TRAIN/DR4/MMDM0/SI681.WAV',
	  		  'array': array([-0.00048828, -0.00018311, -0.00137329, ...,  0.00079346, 0.00091553,  0.00085449], dtype=float32),
	  		  'sampling_rate': 16000},
    'text': 'Would such an act of refusal be useful?',
    'phonetic_detail': [{'start': '0', 'stop': '1960', 'utterance': 'h#'},
                        {'start': '1960', 'stop': '2466', 'utterance': 'w'},
                        {'start': '2466', 'stop': '3480', 'utterance': 'ix'},
                        {'start': '3480', 'stop': '4000', 'utterance': 'dcl'},
                        {'start': '4000', 'stop': '5960', 'utterance': 's'},
                        {'start': '5960', 'stop': '7480', 'utterance': 'ah'},
                        {'start': '7480', 'stop': '7880', 'utterance': 'tcl'},
                        {'start': '7880', 'stop': '9400', 'utterance': 'ch'},
                        {'start': '9400', 'stop': '9960', 'utterance': 'ix'},
                        {'start': '9960', 'stop': '10680', 'utterance': 'n'},
                        {'start': '10680', 'stop': '13480', 'utterance': 'ae'},
                        {'start': '13480', 'stop': '15680', 'utterance': 'kcl'},
                        {'start': '15680', 'stop': '15880', 'utterance': 't'},
                        {'start': '15880', 'stop': '16920', 'utterance': 'ix'},
                        {'start': '16920', 'stop': '18297', 'utterance': 'v'},
                        {'start': '18297', 'stop': '18882', 'utterance': 'r'},
                        {'start': '18882', 'stop': '19480', 'utterance': 'ix'},
                        {'start': '19480', 'stop': '21723', 'utterance': 'f'},
                        {'start': '21723', 'stop': '22516', 'utterance': 'y'},
                        {'start': '22516', 'stop': '24040', 'utterance': 'ux'},
                        {'start': '24040', 'stop': '25190', 'utterance': 'zh'},
                        {'start': '25190', 'stop': '27080', 'utterance': 'el'},
                        {'start': '27080', 'stop': '28160', 'utterance': 'bcl'},
                        {'start': '28160', 'stop': '28560', 'utterance': 'b'},
                        {'start': '28560', 'stop': '30120', 'utterance': 'iy'},
                        {'start': '30120', 'stop': '31832', 'utterance': 'y'},
                        {'start': '31832', 'stop': '33240', 'utterance': 'ux'},
                        {'start': '33240', 'stop': '34640', 'utterance': 's'},
                        {'start': '34640', 'stop': '35968', 'utterance': 'f'},
                        {'start': '35968', 'stop': '37720', 'utterance': 'el'},
                        {'start': '37720', 'stop': '39920', 'utterance': 'h#'}],
    'word_detail': [{'start': '1960', 'stop': '4000', 'utterance': 'would'},
                    {'start': '4000', 'stop': '9400', 'utterance': 'such'},
                    {'start': '9400', 'stop': '10680', 'utterance': 'an'},
                    {'start': '10680', 'stop': '15880', 'utterance': 'act'},
                    {'start': '15880', 'stop': '18297', 'utterance': 'of'},
                    {'start': '18297', 'stop': '27080', 'utterance': 'refusal'},
                    {'start': '27080', 'stop': '30120', 'utterance': 'be'},
                    {'start': '30120', 'stop': '37720', 'utterance': 'useful'}],

    'dialect_region': 'DR4',
    'sentence_type': 'SI',
    'speaker_id': 'MMDM0',
    'id': 'SI681'
}
```


### Data Fields

- file: A path to the downloaded audio file in .wav format.

- audio: A dictionary containing the path to the downloaded audio file, the decoded audio array, and the sampling rate. Note that when accessing the audio column: `dataset[0]["audio"]` the audio file is automatically decoded and resampled to `dataset.features["audio"].sampling_rate`. Decoding and resampling of a large number of audio files might take a significant amount of time. Thus it is important to first query the sample index before the `"audio"` column, *i.e.* `dataset[0]["audio"]` should **always** be preferred over `dataset["audio"][0]`.

- text: The transcription of the audio file.

- phonetic_detail: The phonemes that make up the sentence. The PHONCODE.DOC contains a table of all the phonemic and phonetic symbols used in TIMIT lexicon.

- word_detail: Word level split of the transcript.

- dialect_region: The dialect code of the recording.

- sentence_type: The type of the sentence - 'SA':'Dialect', 'SX':'Compact' or 'SI':'Diverse'.

- speaker_id: Unique id of the speaker. The same speaker id can be found for multiple data samples.

- id: ID of the data sample. Contains the <SENTENCE_TYPE><SENTENCE_NUMBER>.


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

The dataset consists of people who have donated their voice online. You agree to not attempt to determine the identity of speakers in this dataset.

## Considerations for Using the Data

### Social Impact of Dataset

[More Information Needed]

### Discussion of Biases

[More Information Needed]

### Other Known Limitations

Dataset provided for research purposes only. Please check dataset license for additional information.

## Additional Information

### Dataset Curators

The dataset was created by John S. Garofolo, Lori F. Lamel, William M. Fisher, Jonathan G. Fiscus, David S. Pallett, Nancy L. Dahlgren, Victor Zue

### Licensing Information

[LDC User Agreement for Non-Members](https://catalog.ldc.upenn.edu/license/ldc-non-members-agreement.pdf)

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
