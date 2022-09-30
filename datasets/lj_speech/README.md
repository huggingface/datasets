---
annotations_creators:
- expert-generated
language_creators:
- found
language:
- en
license:
- unlicense
multilinguality:
- monolingual
paperswithcode_id: ljspeech
pretty_name: LJ Speech
size_categories:
- 10K<n<100K
source_datasets:
- original
task_categories:
- automatic-speech-recognition
task_ids: []
train-eval-index:
- config: main
  task: automatic-speech-recognition
  task_id: speech_recognition
  splits:
    train_split: train
  col_mapping:
    file: path
    text: text
  metrics:
    - type: wer
      name: WER
    - type: cer
      name: CER
---

# Dataset Card for lj_speech

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

- **Homepage:** [The LJ Speech Dataset](https://keithito.com/LJ-Speech-Dataset/)
- **Repository:** [N/A]
- **Paper:** [N/A]
- **Leaderboard:** [Paperswithcode Leaderboard](https://paperswithcode.com/sota/text-to-speech-synthesis-on-ljspeech)
- **Point of Contact:** [Keith Ito](mailto:kito@kito.us)

### Dataset Summary

This is a public domain speech dataset consisting of 13,100 short audio clips of a single speaker reading passages from 7 non-fiction books in English. A transcription is provided for each clip. Clips vary in length from 1 to 10 seconds and have a total length of approximately 24 hours.

The texts were published between 1884 and 1964, and are in the public domain. The audio was recorded in 2016-17 by the LibriVox project and is also in the public domain.

### Supported Tasks and Leaderboards

The dataset can be used to train a model for Automatic Speech Recognition (ASR) or Text-to-Speech (TTS).
- `other:automatic-speech-recognition`: An ASR model is presented with an audio file and asked to transcribe the audio file to written text.
The most common ASR evaluation metric is the word error rate (WER).
- `other:text-to-speech`: A TTS model is given a written text in natural language and asked to generate a speech audio file.
A reasonable evaluation metric is the mean opinion score (MOS) of audio quality.
The dataset has an active leaderboard which can be found at https://paperswithcode.com/sota/text-to-speech-synthesis-on-ljspeech

### Languages

The transcriptions and audio are in English.

## Dataset Structure

### Data Instances

A data point comprises the path to the audio file, called `file` and its transcription, called `text`.
A normalized version of the text is also provided.

```
{
    'id': 'LJ002-0026',
    'file': '/datasets/downloads/extracted/05bfe561f096e4c52667e3639af495226afe4e5d08763f2d76d069e7a453c543/LJSpeech-1.1/wavs/LJ002-0026.wav',
	'audio': {'path': '/datasets/downloads/extracted/05bfe561f096e4c52667e3639af495226afe4e5d08763f2d76d069e7a453c543/LJSpeech-1.1/wavs/LJ002-0026.wav',
	  'array': array([-0.00048828, -0.00018311, -0.00137329, ...,  0.00079346,
			  0.00091553,  0.00085449], dtype=float32),
	  'sampling_rate': 22050},
    'text': 'in the three years between 1813 and 1816,'
    'normalized_text': 'in the three years between eighteen thirteen and eighteen sixteen,',
}
```

Each audio file is a single-channel 16-bit PCM WAV with a sample rate of 22050 Hz.

### Data Fields

- id: unique id of the data sample.

- file: a path to the downloaded audio file in .wav format.

- audio: A dictionary containing the path to the downloaded audio file, the decoded audio array, and the sampling rate. Note that when accessing the audio column: `dataset[0]["audio"]` the audio file is automatically decoded and resampled to `dataset.features["audio"].sampling_rate`. Decoding and resampling of a large number of audio files might take a significant amount of time. Thus it is important to first query the sample index before the `"audio"` column, *i.e.* `dataset[0]["audio"]` should **always** be preferred over `dataset["audio"][0]`.

- text: the transcription of the audio file.

- normalized_text: the transcription with numbers, ordinals, and monetary units expanded into full words.

### Data Splits

The dataset is not pre-split. Some statistics:

- Total Clips: 13,100
- Total Words: 225,715
- Total Characters: 1,308,678
- Total Duration: 23:55:17
- Mean Clip Duration: 6.57 sec
- Min Clip Duration: 1.11 sec
- Max Clip Duration: 10.10 sec
- Mean Words per Clip: 17.23
- Distinct Words: 13,821

## Dataset Creation

### Curation Rationale

[Needs More Information]

### Source Data

#### Initial Data Collection and Normalization

This dataset consists of excerpts from the following works:

- Morris, William, et al. Arts and Crafts Essays. 1893.
- Griffiths, Arthur. The Chronicles of Newgate, Vol. 2. 1884.
- Roosevelt, Franklin D. The Fireside Chats of Franklin Delano Roosevelt. 1933-42.
- Harland, Marion. Marion Harland's Cookery for Beginners. 1893.
- Rolt-Wheeler, Francis. The Science - History of the Universe, Vol. 5: Biology. 1910.
- Banks, Edgar J. The Seven Wonders of the Ancient World. 1916.
- President's Commission on the Assassination of President Kennedy. Report of the President's Commission on the Assassination of President Kennedy. 1964.

Some details about normalization:
- The normalized transcription has the numbers, ordinals, and monetary units expanded into full words (UTF-8)
- 19 of the transcriptions contain non-ASCII characters (for example, LJ016-0257 contains "raison d'être").
- The following abbreviations appear in the text. They may be expanded as follows:

| Abbreviation | Expansion |
|--------------|-----------|
| Mr. | Mister |
| Mrs. | Misess (*) |
| Dr. | Doctor |
| No. | Number |
| St. | Saint |
| Co. | Company |
| Jr. | Junior |
| Maj. | Major |
| Gen. | General |
| Drs. | Doctors |
| Rev. | Reverend |
| Lt. | Lieutenant |
| Hon. | Honorable |
| Sgt. | Sergeant |
| Capt. | Captain |
| Esq. | Esquire |
| Ltd. | Limited |
| Col. | Colonel |
| Ft. | Fort |
(*) there's no standard expansion for "Mrs."

#### Who are the source language producers?

[Needs More Information]

### Annotations

#### Annotation process

- The audio clips range in length from approximately 1 second to 10 seconds. They were segmented automatically based on silences in the recording. Clip boundaries generally align with sentence or clause boundaries, but not always.
- The text was matched to the audio manually, and a QA pass was done to ensure that the text accurately matched the words spoken in the audio.

#### Who are the annotators?

Recordings by Linda Johnson from LibriVox. Alignment and annotation by Keith Ito.

### Personal and Sensitive Information

The dataset consists of people who have donated their voice online. You agree to not attempt to determine the identity of speakers in this dataset.

## Considerations for Using the Data

### Social Impact of Dataset

[Needs More Information]

### Discussion of Biases

[Needs More Information]

### Other Known Limitations

- The original LibriVox recordings were distributed as 128 kbps MP3 files. As a result, they may contain artifacts introduced by the MP3 encoding.

## Additional Information

### Dataset Curators

The dataset was initially created by Keith Ito and Linda Johnson.

### Licensing Information

Public Domain ([LibriVox](https://librivox.org/pages/public-domain/))

### Citation Information

```
@misc{ljspeech17,
  author       = {Keith Ito and Linda Johnson},
  title        = {The LJ Speech Dataset},
  howpublished = {\url{https://keithito.com/LJ-Speech-Dataset/}},
  year         = 2017
}
```

### Contributions

Thanks to [@anton-l](https://github.com/anton-l) for adding this dataset.
