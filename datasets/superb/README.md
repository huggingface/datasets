---
annotations_creators:
- other
language_creators:
- other
languages:
- en
licenses:
- unknown
multilinguality:
- monolingual
pretty_name: SUPERB
size_categories:
- unknown
source_datasets:
- original
- extended|librispeech_asr
- extended|other-librimix
- extended|other-speech_commands
task_categories:
- speech-processing
task_ids:
- automatic-speech-recognition
- phoneme-recognition
- keyword-spotting
- query-by-example-spoken-term-detection
- speaker-identification
- automatic-speaker-verification
- speaker-diarization
- intent-classification
- slot-filling
- emotion-recognition
---

# Dataset Card for SUPERB

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

- **Homepage:** [http://superbbenchmark.org](http://superbbenchmark.org)
- **Repository:** [https://github.com/s3prl/s3prl](https://github.com/s3prl/s3prl)
- **Paper:** [SUPERB: Speech processing Universal PERformance Benchmark](https://arxiv.org/abs/2105.01051)
- **Leaderboard:** [More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)
- **Point of Contact:** [Lewis Tunstall](mailto:lewis@huggingface.co) and [Albert Villanova](mailto:albert@huggingface.co)

### Dataset Summary

SUPERB is a leaderboard to benchmark the performance of a shared model across a wide range of speech processing tasks with minimal architecture changes and labeled data.

### Supported Tasks and Leaderboards

The SUPERB leaderboard can be found here **ADD LINK WHEN LIVE** and consists of the following tasks:

#### pr

Phoneme Recognition (PR) transcribes an utterance into the smallest content units. This task includes alignment modeling to avoid potentially inaccurate forced alignment. [LibriSpeech](https://huggingface.co/datasets/librispeech_asr) train-clean-100/dev-clean/test-clean subsets are adopted in SUPERB for training/validation/testing. Phoneme transcriptions are obtained from the LibriSpeech official g2p-model-5 and the conversion script in Kaldi librispeech s5 recipe. The evaluation metric is phone error rate (PER).

#### asr

Automatic Speech Recognition (ASR) transcribes utterances into words. While PR analyzes the improvement in modeling phonetics, ASR reflects the significance of the improvement in a real-world scenario. [LibriSpeech](https://huggingface.co/datasets/librispeech_asr) train-clean-100/devclean/test-clean subsets are used for training/validation/testing. The evaluation metric is word error rate (WER).

#### ks

Keyword Spotting (KS) detects preregistered keywords by classifying utterances into a predefined set of words. The task is usually performed on-device for the fast response time. Thus, accuracy, model size, and inference time are all crucial. SUPERB uses the widely used [Speech Commands dataset v1.0](https://www.tensorflow.org/datasets/catalog/speech_commands) for the task. The dataset consists of ten classes of keywords, a class for silence, and an unknown class to include the false positive. The evaluation metric is accuracy (ACC)

#### qbe

Query by Example Spoken Term Detection (QbE) detects a spoken term (query) in an audio database (documents) by binary discriminating a given pair of query and document into a match or not. The English subset in [QUESST 2014 challenge](https://github.com/s3prl/s3prl/tree/master/downstream#qbe-query-by-example-spoken-term-detection) is adopted since we focus on investigating English as the first step. The evaluation metric is maximum term weighted value (MTWV) which balances misses and false alarms.

#### ic

Intent Classification (IC) classifies utterances into predefined classes to determine the intent of speakers. SUPERB uses the [Fluent Speech Commands dataset](https://github.com/s3prl/s3prl/tree/master/downstream#ic-intent-classification---fluent-speech-commands), where each utterance is tagged with three intent labels: action, object, and location. The evaluation metric is accuracy (ACC).

#### sf

Slot Filling (SF) predicts a sequence of semantic slot-types from an utterance, like a slot-type FromLocation for a spoken word Taipei, which is known as a slot-value. Both slot-types and slot-values are essential for an SLU system to function. The evaluation metrics thus include slot-type F1 score and slotvalue CER. [Audio SNIPS](https://github.com/s3prl/s3prl/tree/master/downstream#sf-end-to-end-slot-filling) is adopted, which synthesized multi-speaker utterances for SNIPS. Following the standard split in SNIPS, US-accent speakers are further selected for training, and others are for validation/testing.

#### si
Speaker Identification (SI) classifies each utterance for its speaker identity as a multi-class classification, where speakers are in the same predefined set for both training and testing. The widely used [VoxCeleb1 dataset](https://www.robots.ox.ac.uk/~vgg/data/voxceleb/vox1.html) is adopted, and the evaluation metric is accuracy (ACC).

#### asv

Automatic Speaker Verification (ASV) verifies whether the speakers of a pair of utterances match as a binary classification, and speakers in the testing set may not appear in the training set. Thus, ASV is more challenging than SID. VoxCeleb1 is used without VoxCeleb2 training data and noise augmentation. The evaluation metric is equal error rate (EER).

#### sd

Speaker Diarization (SD) predicts *who is speaking when* for each timestamp, and multiple speakers can speak simultaneously. The model has to encode rich speaker characteristics for each frame and should be able to represent mixtures of signals. [LibriMix](https://github.com/s3prl/s3prl/tree/master/downstream#sd-speaker-diarization) is adopted where LibriSpeech train-clean-100/dev-clean/test-clean are used to generate mixtures for training/validation/testing. We focus on the two-speaker scenario as the first step. The time-coded speaker labels were generated using alignments from Kaldi LibriSpeech ASR model. The evaluation metric is diarization error rate (DER).

##### Example of usage

Use these auxiliary functions to:
- load the audio file into an audio data array
- generate the label array

```python
def load_audio_file(example, frame_shift=160):
    import soundfile as sf

    example["array"], example["sample_rate"] = sf.read(
        example["file"], start=example["start"] * frame_shift, stop=example["end"] * frame_shift
    )
    return example


def generate_label(example, frame_shift=160, num_speakers=2, rate=16000):
    import numpy as np

    start = example["start"]
    end = example["end"]
    frame_num = end - start
    speakers = sorted({speaker["speaker_id"] for speaker in example["speakers"]})
    label = np.zeros((frame_num, num_speakers), dtype=np.int32)
    for speaker in example["speakers"]:
        speaker_index = speakers.index(speaker["speaker_id"])
        start_frame = np.rint(speaker["start"] * rate / frame_shift).astype(int)
        end_frame = np.rint(speaker["end"] * rate / frame_shift).astype(int)
        rel_start = rel_end = None
        if start <= start_frame < end:
            rel_start = start_frame - start
        if start < end_frame <= end:
            rel_end = end_frame - start
        if rel_start is not None or rel_end is not None:
            label[rel_start:rel_end, speaker_index] = 1
    example["label"] = label
    return example
```

#### er

Emotion Recognition (ER) predicts an emotion class for each utterance. The most widely used ER dataset [IEMOCAP](https://github.com/s3prl/s3prl/tree/master/downstream#er-emotion-recognition) is adopted, and we follow the conventional evaluation protocol: we drop the unbalance emotion classes to leave the final four classes with a similar amount of data points and cross-validates on five folds of the standard splits. The evaluation metric is accuracy (ACC).

### Languages

The language data in SUPERB is in English (BCP-47 `en`)


## Dataset Structure

### Data Instances

#### pr

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)


#### asr

An example from each split looks like:

```python
{'chapter_id': 1240,
 'file': 'path/to/file.flac',
 'id': '103-1240-0000',
 'speaker_id': 103,
 'text': 'CHAPTER ONE MISSUS RACHEL LYNDE IS SURPRISED MISSUS RACHEL LYNDE '
         'LIVED JUST WHERE THE AVONLEA MAIN ROAD DIPPED DOWN INTO A LITTLE '
         'HOLLOW FRINGED WITH ALDERS AND LADIES EARDROPS AND TRAVERSED BY A '
         'BROOK'}
```

#### ks

An example from each split looks like:

```python
{
  'file': '/path/yes/af7a8296_nohash_1.wav', 
  'label': 'yes'
}
```

#### qbe

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)


#### ic

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)


#### sf

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)


#### si

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)


#### asv

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)


#### sd

An example from each split looks like:
```python
{
  'record_id': '1578-6379-0038_6415-111615-0009',
  'file': 'path/to/file.wav',
  'start': 0,
  'end': 1590,
  'speakers': [
    {'speaker_id': '1578', 'start': 28, 'end': 657},
    {'speaker_id': '6415', 'start': 28, 'end': 1576}
  ]
}
```


#### er

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)




### Data Fields

#### pr

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)


#### asr

- `file`: a `string` feature.
- `text`: a `string` feature.
- `speaker_id`: a `int64` feature.
- `chapter_id`: a `int64` feature.
- `id`: a `string` feature.

#### ks

- `file` (`string`): Path to the WAV audio file.
- `label` (`string`): Label of the spoken command.

#### qbe

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)


#### ic

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)


#### sf

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)


#### si

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)


#### asv

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)


#### sd

The data fields in all splits are:
- `record_id` (`string`): ID of the record.
- `file` (`string`): Path to the WAV audio file.
- `start` (`integer`): Start frame of the audio.
- `end` (`integer`): End frame of the audio.
- `speakers` (`list` of `dict`): List of speakers in the audio. Each item contains the fields:
  - `speaker_id` (`string`): ID of the speaker.
  - `start` (`integer`): Frame when the speaker starts speaking.
  - `end` (`integer`): Frame when the speaker stops speaking.

#### er

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

### Data Splits

#### pr

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)


#### asr

|     | train | validation | test |
|-----|------:|-----------:|-----:|
| asr | 28539 |       2703 | 2620 |

#### ks

|    | train | validation | test |
|----|------:|-----------:|-----:|
| ks | 51094 |       6798 | 3081 |

#### qbe

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)


#### ic

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)


#### sf

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)


#### si

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)


#### asv

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)


#### sd

The data is split into "train", "dev" and "test" sets, each containing the following number of examples:

|    | train |  dev | test |
|----|------:|-----:|-----:|
| sd | 13901 | 3014 | 3002 |

#### er

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

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

[More Information Needed]

### Citation Information

```
@article{DBLP:journals/corr/abs-2105-01051,
  author    = {Shu{-}Wen Yang and
               Po{-}Han Chi and
               Yung{-}Sung Chuang and
               Cheng{-}I Jeff Lai and
               Kushal Lakhotia and
               Yist Y. Lin and
               Andy T. Liu and
               Jiatong Shi and
               Xuankai Chang and
               Guan{-}Ting Lin and
               Tzu{-}Hsien Huang and
               Wei{-}Cheng Tseng and
               Ko{-}tik Lee and
               Da{-}Rong Liu and
               Zili Huang and
               Shuyan Dong and
               Shang{-}Wen Li and
               Shinji Watanabe and
               Abdelrahman Mohamed and
               Hung{-}yi Lee},
  title     = {{SUPERB:} Speech processing Universal PERformance Benchmark},
  journal   = {CoRR},
  volume    = {abs/2105.01051},
  year      = {2021},
  url       = {https://arxiv.org/abs/2105.01051},
  archivePrefix = {arXiv},
  eprint    = {2105.01051},
  timestamp = {Thu, 01 Jul 2021 13:30:22 +0200},
  biburl    = {https://dblp.org/rec/journals/corr/abs-2105-01051.bib},
  bibsource = {dblp computer science bibliography, https://dblp.org}
}

Note that each SUPERB dataset has its own citation. Please see the source to see
the correct citation for each contained dataset.
```

### Contributions

Thanks to [@lewtun](https://github.com/lewtun), [@albertvillanova](https://github.com/albertvillanova) and [@anton-l](https://github.com/anton-l) for adding this dataset.
