annotations_creators:
- expert-generated
language_creators:
- expert-generated
languages:
- en
licenses:
- cc-by-nc-nd-3-0
multilinguality:
- monolingual
size_categories:
- 10K<n<100K
source_datasets:
- original
task_categories:
- automatic-speech-recognition
task_ids:
- automatic-speech-recognition

# Dataset Card for tedlium

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

- **Homepage:** [TED-LIUM homepage](https://www.openslr.org/7/)
- **Repository:** [Needs More Information]
- **Paper:** [TED-LIUM: an Automatic Speech Recognition dedicated corpus](https://aclanthology.org/L12-1405/)
- **Leaderboard:** [Paperswithcode Leaderboard](https://paperswithcode.com/sota/speech-recognition-on-tedlium)
- **Point of Contact:** [Sanchit Gandhi](mailto:sanchit@huggingface.co)

### Dataset Summary

The TED-LIUM corpus is English-language TED talks, with transcriptions, sampled at 16kHz. It contains about 118 hours of speech.

### Supported Tasks and Leaderboards

- `automatic-speech-recognition`: The dataset can be used to train a model for Automatic Speech Recognition (ASR). The model is presented with an audio file and asked to transcribe the audio file to written text. The most common evaluation metric is the word error rate (WER). The task has an active leaderboard which can be found at https://paperswithcode.com/sota/speech-recognition-on-tedlium that ranks models based on their WER.

### Languages

The audio and transcriptions are in English, as per the TED talks at http://www.ted.com.

## Dataset Structure

### Data Instances

TODO

### Data Fields

- gender: an integer value corresponding to the gender of the speaker.
- id: unique id of the data sample.
- speaker_id: unique id of the speaker. The same speaker id can be found for multiple data samples.
- speech: A dictionary containing the path to the downloaded audio file, the decoded audio array, and the sampling rate. Note that when accessing the audio column: `dataset[0]["audio"]` the audio file is automatically decoded and resampled to `dataset.features["audio"].sampling_rate`. Decoding and resampling of a large number of audio files might take a significant amount of time. Thus it is important to first query the sample index before the "audio" column, i.e. `dataset[0]["audio"]` should always be preferred over `dataset["audio"][0]`.
- text: the transcription of the audio file.

### Data Splits

The data is split into a training, validation and test set.

| Split      | Examples |
|------------|----------|
| Train      |   56,803 |
| Validation |      591 |
| Test       |    1,469 |


## Dataset Creation

### Curation Rationale

TED-LIUM was built during [The International Workshop on Spoken Language Trans- lation (IWSLT) 2011 Evaluation Campaign](https://aclanthology.org/2011.iwslt-evaluation.1/), an annual workshop focused on the automatic translation of public talks and included tracks for speech recognition, speech translation, text translation, and system combination. The corpus was entered 

### Source Data

#### Initial Data Collection and Normalization

The data was obtained from publicly availably TED talks at http://www.ted.com. Proper alignments between the speech and the transcribed text were generated using an in-house speaker segmentation and clustering tool (LIUM_SpkDiarization). Speech disfluencies (e.g. repetitions, hesitations, false starts) were treated in the following way: the repetitions were transcribed, the hesitations were mapped to a specific filler word and the false starts were not taken into account. For full details on the data collection and processing, refer to the [TED-LIUM paper](https://aclanthology.org/L12-1405/).

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

[Needs More Information]

### Other Known Limitations

[Needs More Information]

## Additional Information

### Dataset Curators

[Needs More Information]

### Licensing Information

Licensed under Creative Commons BY-NC-ND 3.0 (http://creativecommons.org/licenses/by-nc-nd/3.0/deed.en).

### Citation Information

@inproceedings{rousseau2012tedlium,
  title={TED-LIUM: an Automatic Speech Recognition dedicated corpus},
  author={Rousseau, Anthony and Del{\'e}glise, Paul and Est{\`e}ve, Yannick},
  booktitle={Conference on Language Resources and Evaluation (LREC)},
  pages={125--129},
  year={2012}
}