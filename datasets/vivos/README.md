---
pretty_name: VIVOS
annotations_creators:
- expert-generated
language_creators:
- crowdsourced
- expert-generated
languages:
- vi
licenses:
- cc-by-sa-4.0
multilinguality:
- monolingual
size_categories:
- 10K<n<100K
source_datasets:
- original
task_categories:
- speech-processing
task_ids:
- automatic-speech-recognition
---

# Dataset Card for VIVOS

## Table of Contents
- [Dataset Card for VIVOS](#dataset-card-for-vivos)
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
      - [Initial Data Collection and Normalization](#initial-data-collection-and-normalization)
      - [Who are the source language producers?](#who-are-the-source-language-producers)
    - [Annotations](#annotations)
      - [Annotation process](#annotation-process)
      - [Who are the annotators?](#who-are-the-annotators)
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

- **Homepage:** https://ailab.hcmus.edu.vn/vivos
- **Repository:** [Needs More Information]
- **Paper:** [A non-expert Kaldi recipe for Vietnamese Speech Recognition System](https://ailab.hcmus.edu.vn/assets/WLSI3_2016_Luong_non_expert.pdf)
- **Leaderboard:** [Needs More Information]
- **Point of Contact:** [AILAB](mailto:ailab@hcmus.edu.vn)

### Dataset Summary

VIVOS is a free Vietnamese speech corpus consisting of 15 hours of recording speech prepared for Vietnamese Automatic Speech Recognition task.

The corpus was prepared by AILAB, a computer science lab of VNUHCM - University of Science, with Prof. Vu Hai Quan is the head of.

We publish this corpus in hope to attract more scientists to solve Vietnamese speech recognition problems.

### Supported Tasks and Leaderboards

[Needs More Information]

### Languages

Vietnamese

## Dataset Structure

### Data Instances

A typical data point comprises the path to the audio file, called `path` and its transcription, called `sentence`. Some additional information about the speaker and the passage which contains the transcription is provided.

```
{'speaker_id': 'VIVOSSPK01',
 'path': '/home/admin/.cache/huggingface/datasets/downloads/extracted/b7ded9969e09942ab65313e691e6fc2e12066192ee8527e21d634aca128afbe2/vivos/train/waves/VIVOSSPK01/VIVOSSPK01_R001.wav',
 'sentence': 'KHÁCH SẠN'}
```

### Data Fields

- speaker_id: An id for which speaker (voice) made the recording
- path: The path to the audio file
- sentence: The sentence the user was prompted to speak

### Data Splits

The speech material has been subdivided into portions for train and test.

Speech was recorded in a quiet environment with high quality microphone, speakers were asked to read one sentence at a time.

|                  | Train | Test  |
| ---------------- | ----- | ----- |
| Speakers         | 46    | 19    | 
| Utterances       | 11660 | 760   |
| Duration         | 14:55 | 00:45 |
| Unique Syllables | 4617  | 1692  |

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

The dataset consists of people who have donated their voice online.  You agree to not attempt to determine the identity of speakers in the Common Voice dataset.

## Considerations for Using the Data

### Social Impact of Dataset

[More Information Needed]

### Discussion of Biases

[More Information Needed] 

### Other Known Limitations

[More Information Needed] 

## Additional Information

### Dataset Curators

The dataset was initially prepared by AILAB, a computer science lab of VNUHCM - University of Science.

### Licensing Information

Creative Commons Attribution NonCommercial ShareAlike v4.0 (CC BY-NC-SA 4.0)

### Citation Information

```
@InProceedings{vivos:2016,
Address = {Ho Chi Minh, Vietnam}
title = {VIVOS: 15 hours of recording speech prepared for Vietnamese Automatic Speech Recognition},
author={Prof. Vu Hai Quan},
year={2016}
}
```

### Contributions

Thanks to [@binh234](https://github.com/binh234) for adding this dataset.
