---
annotations_creators:
- no-annotation  
language_creators:
- crowdsourced  
languages:
- en  
licenses:
- cc-by-4.0  
multilinguality:
- monolingual    
pretty_name: 
- SpeechCommands  
size_categories:
- unknown  
source_datasets:
- original  
task_categories:
- automatic-speech-recognition  
task_ids:
- automatic-speech-recognition-other-keyword-spotting
---

# Dataset Card for SpeechCommands

## Table of Contents
- [Table of Contents](#table-of-contents)
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

- **Homepage:** https://www.tensorflow.org/datasets/catalog/speech_commands
- **Repository:** [More Information Needed]
- **Paper:** [Speech Commands: A Dataset for Limited-Vocabulary Speech Recognition](https://arxiv.org/pdf/1804.03209.pdf)
- **Leaderboard:** [More Information Needed]
- **Point of Contact:** Pete Warden, petewarden@google.com

### Dataset Summary

This is a set of one-second .wav audio files, each containing a single spoken
English word or background noise. These words are from a small set of commands, and are spoken by a
variety of different speakers. This data set is designed to help train simple
machine learning models. This dataset is covered in more detail at [https://arxiv.org/abs/1804.03209](https://arxiv.org/abs/1804.03209).

Version 0.01 of the data set (configuration `"v0.01"`) was released on August 3rd 2017 and contains
64,727 audio files. 

Version 0.02 of the data set (configuration `"v0.02"`) was released on April 11th 2018 and 
contains 105,829 audio files.


### Supported Tasks and Leaderboards

* `keyword-spotting`: the dataset can be used to train and evaluate keyword
spotting systems. The task is to detect preregistered keywords by classifying utterances 
into a predefined set of words. The task is usually performed on-device for the 
fast response time. Thus, accuracy, model size, and inference time are all crucial.

### Languages

The language data in SpeechCommands is in English (BCP-47 `en`).

## Dataset Structure

### Data Instances

Example of target class:
```python
{
  "file": "path_to_data/down/a929f9b9_nohash_0.wav", 
  "audio": {
    "path": "path_to_data/down/a929f9b9_nohash_0.wav", 
    "array": array([ 3.0517578e-05, -3.0517578e-05, -6.1035156e-05, ...,
          3.0517578e-05,  1.5258789e-04, -3.0517578e-05], dtype=float32), 
    "sampling_rate": 16000
    },
  "label": 3,  # "down"
  "speaker_id": "a929f9b9",
  "utterance_id": 0
}
```

Example of `_unknown_` class:
```python
{
  "file": "path_to_data/bird/0b40aa8e_nohash_1.wav", 
  "audio": {
    "path": "path_to_data/bird/0b40aa8e_nohash_1.wav", 
    "array": array([-0.00018311, -0.00119019, -0.00076294, ...,  0.0007019 ,
          0.        , -0.00073242], dtype=float32),
    "sampling_rate": 16000
    },
  "label": 24,
  "speaker_id": "0b40aa8e",
  "utterance_id": 1
}
```

Example of `_background_noise_` class:
```python
{
  "file": "path_to_data/_background_noise_/doing_the_dishes.wav", 
  "audio": {
    "path": "path_to_data/_background_noise_/doing_the_dishes.wav", 
    "array": array([ 0.        ,  0.        ,  0.        , ..., -0.00592041,
         -0.00405884, -0.00253296], dtype=float32), 
    "sampling_rate": 16000
    }, 
  "label": 25,  # "_background_noise_"
  "speaker_id": "None",
  "utterance_id": 0
}
```


### Data Fields

* `file`: path to the downloaded audio file in .wav format.
* `audio`: dictionary containing the path to the downloaded audio file, 
the decoded audio array, and the sampling rate. Note that when accessing 
the audio column: `dataset[0]["audio"]` the audio file is automatically decoded 
and resampled to `dataset.features["audio"].sampling_rate`. 
Decoding and resampling of a large number of audio files might take a significant 
amount of time. Thus it is important to first query the sample index before 
the `"audio"` column, i.e. `dataset[0]["audio"]` should always be preferred 
over `dataset["audio"][0]`.
* `label`: label of an audio sample. Can be one of a set of target words, `_unknown_` or `_background_noise_`.
* `speaker_id`: unique id of a speaker. Equals to `"None"` if label is `_background_noise_`.
* `utterance_id`: incremental id of a word utterance. Doesn't make sense if label is `_unknown_` or `_background_noise_`.

### Data Splits

The dataset has two versions (=configurations): `"v0.01"` and `"v0.02"`. `"v0.02"` contains more target and 
`_unknown_` words (see section [Source Data](#source-data) for more details).

|       | train | validation | test |
|-----  |------:|-----------:|-----:|
| v0.01 | 51094 |       6798 | 3081 |
| v0.02 | 84849 |       9981 | 4890 |

#### #TODO: correct num of samples in sets after review

## Dataset Creation

### Curation Rationale

The primary goal of the dataset is to provide a way to build and test small 
models that detect when a single word is spoken, from a set of target words, 
with as few false positives as possible from background noise or unrelated speech. 

### Source Data

#### Initial Data Collection and Normalization

The audio files were collected using crowdsourcing, see
[aiyprojects.withgoogle.com/open_speech_recording](https://github.com/petewarden/extract_loudest_section)
for some of the open source audio collection code that was used. The goal was to gather examples of
people speaking single-word commands, rather than conversational sentences, so
they were prompted for individual words over the course of a five minute
session. In version 0.01 ten command words were recoded, with most speakers saying each
of them five times.: "Yes", "No", "Up", "Down", "Left",
"Right", "On", "Off", "Stop", "Go". More command words were added in the version 0.02: 
"Zero", "One", "Two", "Three", "Four", "Five", "Six", "Seven", "Eight", "Nine", "Backward", 
"Forward", "Follow", "Learn".
To help distinguish unrecognized words, there are also ten auxiliary words, which most speakers only said once.
These include "Bed", "Bird", "Cat", "Dog", "Happy", "House", "Marvin", "Sheila",
"Tree", and "Wow".

The `_background_noise_` class contains a set of  longer audio clips that are either recordings or 
a mathematical simulations of noise.

#### Who are the source language producers?

The audio files were collected using crowdsourcing.

### Annotations

#### Annotation process

[More Information Needed]

#### Who are the annotators?

[More Information Needed]

### Personal and Sensitive Information

[More Information Needed]

## Considerations for Using the Data

### Social Impact of Dataset

[More Information Needed]

### Discussion of Biases

[More Information Needed]

### Other Known Limitations

[More Information Needed]

## Additional Information

### Dataset Curators

[More Information Needed]

### Licensing Information

Creative Commons BY 4.0 License.

### Citation Information

```
@article{speechcommandsv2,
   author = { {Warden}, P.},
    title = "{Speech Commands: A Dataset for Limited-Vocabulary Speech Recognition}",
  journal = {ArXiv e-prints},
  archivePrefix = "arXiv",
  eprint = {1804.03209},
  primaryClass = "cs.CL",
  keywords = {Computer Science - Computation and Language, Computer Science - Human-Computer Interaction},
    year = 2018,
    month = apr,
    url = {https://arxiv.org/abs/1804.03209},
}
```
### Contributions

Thanks to [@polinaeterna](https://github.com/polinaeterna) and ... for adding this dataset.
