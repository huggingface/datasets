---
annotations_creators:
- expert-generated
language_creators:
- crowdsourced
languages:
- en
licenses:
- cc-by-4.0
multilinguality:
- monolingual
pretty_name: VCTK
size_categories:
- 10K<n<100K
source_datasets:
- original
task_categories:
- automatic-speech-recognition
task_ids: []
paperswithcode_id: vctk
---

# Dataset Card for VCTK

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

- **Homepage:** [Edinburg DataShare](https://doi.org/10.7488/ds/2645)
- **Repository:** 
- **Paper:**
- **Leaderboard:**
- **Point of Contact:**

### Dataset Summary

This CSTR VCTK Corpus includes speech data uttered by 110 English speakers with various accents. Each speaker reads out about 400 sentences, which were selected from a newspaper, the rainbow passage and an elicitation paragraph used for the speech accent archive.

### Supported Tasks and Leaderboards

[More Information Needed]

### Languages

[More Information Needed]

## Dataset Structure

### Data Instances

A data point comprises the path to the audio file, called `file` and its transcription, called `text`. 

```
{
  'speaker_id': 'p225',
  'text_id': '001',
  'text': 'Please call Stella.',
  'age': '23', 
  'gender': 'F', 
  'accent': 'English', 
  'region': 'Southern England', 
  'file': '/datasets/downloads/extracted/8ed7dad05dfffdb552a3699777442af8e8ed11e656feb277f35bf9aea448f49e/wav48_silence_trimmed/p225/p225_001_mic1.flac', 
  'audio': 
    {
      'path': '/datasets/downloads/extracted/8ed7dad05dfffdb552a3699777442af8e8ed11e656feb277f35bf9aea448f49e/wav48_silence_trimmed/p225/p225_001_mic1.flac', 
      'array': array([0.00485229, 0.00689697, 0.00619507, ..., 0.00811768, 0.00836182, 0.00854492], dtype=float32), 
      'sampling_rate': 48000
    }, 
  'comment': ''
}
```

Each audio file is a single-channel FLAC with a sample rate of 48000 Hz.

### Data Fields

Each row consists of the following fields:

- `speaker_id`: Speaker ID
- `audio`: Audio recording
- `file`: Path to audio file
- `text`: Text transcription of corresponding audio
- `text_id`: Text ID
- `age`: Speaker's age
- `gender`: Speaker's gender
- `accent`: Speaker's accent
- `region`: Speaker's region, if annotation exists
- `comment`: Miscellaneous comments, if any

### Data Splits

The dataset has no predefined splits.

## Dataset Creation

### Curation Rationale

[More Information Needed]

### Source Data

#### Initial Data Collection and Normalization

[More Information Needed]

#### Who are the source language producers?

[More Information Needed]

### Annotations

#### Annotation process

[More Information Needed]

#### Who are the annotators?

[More Information Needed]

### Personal and Sensitive Information

The dataset consists of people who have donated their voice online.  You agree to not attempt to determine the identity of speakers in this dataset.

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

Public Domain, Creative Commons Attribution 4.0 International Public License ([CC-BY-4.0](https://creativecommons.org/licenses/by/4.0/legalcode))

### Citation Information

```bibtex
@inproceedings{Veaux2017CSTRVC,
    title        = {CSTR VCTK Corpus: English Multi-speaker Corpus for CSTR Voice Cloning Toolkit},
    author       = {Christophe Veaux and Junichi Yamagishi and Kirsten MacDonald},
    year         = 2017
}
```

### Contributions

Thanks to [@jaketae](https://github.com/jaketae) for adding this dataset.
