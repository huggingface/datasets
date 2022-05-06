---
pretty_name: AMI Corpus
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
size_categories:
- 100K<n<1M
source_datasets:
- original
task_categories:
- automatic-speech-recognition
task_ids: []
---

# Dataset Card for AMI Corpus

## Table of Contents
- [Dataset Description](#dataset-description)
  - [Dataset Summary](#dataset-summary)
  - [Dataset Preprocessing](#dataset-preprocessing)
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

- **Homepage:** [AMI corpus](https://groups.inf.ed.ac.uk/ami/corpus/)
- **Repository:** [Needs More Information]
- **Paper:** [Needs More Information]
- **Leaderboard:** [Needs More Information]
- **Point of Contact:** [Needs More Information]

### Dataset Summary

The AMI Meeting Corpus consists of 100 hours of meeting recordings. The recordings use a range of signals
synchronized to a common timeline. These include close-talking and far-field microphones, individual and
room-view video cameras, and output from a slide projector and an electronic whiteboard. During the meetings,
the participants also have unsynchronized pens available to them that record what is written. The meetings
were recorded in English using three different rooms with different acoustic properties, and include mostly
non-native speakers.

### Dataset Preprocessing

Individual samples of the AMI dataset contain very large audio files (between 10 and 60 minutes). 
Such lengths are unfeasible for most speech recognition models. In the following, we show how the
dataset can effectively be chunked into multiple segments as defined by the dataset creators.

The following function cuts the long audio files into the defined segment lengths:

```python
import librosa
import math
from datasets import load_dataset

SAMPLE_RATE = 16_000

def chunk_audio(batch):
    new_batch = {
        "audio": [],
        "words": [],
        "speaker": [],
        "lengths": [],
        "word_start_times": [],
        "segment_start_times": [],
    }

    audio, _ = librosa.load(batch["file"][0], sr=SAMPLE_RATE)

    word_idx = 0
    num_words = len(batch["words"][0])
    for segment_idx in range(len(batch["segment_start_times"][0])):
        words = []
        word_start_times = []
        start_time = batch["segment_start_times"][0][segment_idx]
        end_time = batch["segment_end_times"][0][segment_idx]

        # go back and forth with word_idx since segments overlap with each other
        while (word_idx > 1) and (start_time < batch["word_end_times"][0][word_idx - 1]):
            word_idx -= 1

        while word_idx < num_words and (start_time > batch["word_start_times"][0][word_idx]):
            word_idx += 1

        new_batch["audio"].append(audio[int(start_time * SAMPLE_RATE): int(end_time * SAMPLE_RATE)])

        while word_idx < num_words and batch["word_start_times"][0][word_idx] < end_time:
            words.append(batch["words"][0][word_idx])
            word_start_times.append(batch["word_start_times"][0][word_idx])
            word_idx += 1

        new_batch["lengths"].append(end_time - start_time)
        new_batch["words"].append(words)
        new_batch["speaker"].append(batch["segment_speakers"][0][segment_idx])
        new_batch["word_start_times"].append(word_start_times)

        new_batch["segment_start_times"].append(batch["segment_start_times"][0][segment_idx])

    return new_batch
    
ami = load_dataset("ami", "headset-single")
ami = ami.map(chunk_audio, batched=True, batch_size=1, remove_columns=ami["train"].column_names)
```

The segmented audio files can still be as long as a minute. To further chunk the data into shorter 
audio chunks, you can use the following script.

```python
MAX_LENGTH_IN_SECONDS = 20.0

def chunk_into_max_n_seconds(batch):
    new_batch = {
        "audio": [],
        "text": [],
    }

    sample_length = batch["lengths"][0]
    segment_start = batch["segment_start_times"][0]

    if sample_length > MAX_LENGTH_IN_SECONDS:
        num_chunks_per_sample = math.ceil(sample_length / MAX_LENGTH_IN_SECONDS)
        avg_chunk_length = sample_length / num_chunks_per_sample
        num_words = len(batch["words"][0])

        # start chunking by times
        start_word_idx = end_word_idx = 0
        chunk_start_time = 0
        for n in range(num_chunks_per_sample):
            while (end_word_idx < num_words - 1) and (batch["word_start_times"][0][end_word_idx] < segment_start + (n + 1) * avg_chunk_length):
                end_word_idx += 1

            chunk_end_time = int((batch["word_start_times"][0][end_word_idx] - segment_start) * SAMPLE_RATE)
            new_batch["audio"].append(batch["audio"][0][chunk_start_time: chunk_end_time])
            new_batch["text"].append(" ".join(batch["words"][0][start_word_idx: end_word_idx]))

            chunk_start_time = chunk_end_time
            start_word_idx = end_word_idx
    else:
        new_batch["audio"].append(batch["audio"][0])
        new_batch["text"].append(" ".join(batch["words"][0]))

    return new_batch
    
ami = ami.map(chunk_into_max_n_seconds, batched=True, batch_size=1, remove_columns=ami["train"].column_names, num_proc=64)
```

A segmented and chunked dataset of the config `"headset-single"`can be found [here](https://huggingface.co/datasets/ami-wav2vec2/ami_single_headset_segmented_and_chunked).

### Supported Tasks and Leaderboards

- `automatic-speech-recognition`: The dataset can be used to train a model for Automatic Speech Recognition (ASR). The model is presented with an audio file and asked to transcribe the audio file to written text. The most common evaluation metric is the word error rate (WER). The task does not have an active leaderboard at the moment.

- `speaker-diarization`: The dataset can be used to train model for Speaker Diarization (SD). The model is presented with an audio file and asked to predict which speaker spoke at what time.

### Languages

The audio is in English.

## Dataset Structure

### Data Instances 

A typical data point comprises the path to the audio file (or files in the case of 
the multi-headset or multi-microphone dataset), called `file` and its transcription as 
a list of words, called `words`. Additional information about the `speakers`, the `word_start_time`, `word_end_time`, `segment_start_time`, `segment_end_time` is given.
In addition 

and its transcription, called `text`. Some additional information about the speaker and the passage which contains the transcription is provided.
 
```
{'word_ids': ["ES2004a.D.words1", "ES2004a.D.words2", ...],
 'word_start_times': [0.3700000047683716, 0.949999988079071, ...],
 'word_end_times': [0.949999988079071, 1.5299999713897705, ...],
 'word_speakers': ['A', 'A', ...], 
 'segment_ids': ["ES2004a.sync.1", "ES2004a.sync.2", ...]
 'segment_start_times': [10.944000244140625, 17.618999481201172, ...],
 'segment_end_times': [17.618999481201172, 18.722000122070312, ...],
 'segment_speakers': ['A', 'B', ...], 
 'words', ["hmm", "hmm", ...]
 'channels': [0, 0, ..], 
 'file': "/.cache/huggingface/datasets/downloads/af7e748544004557b35eef8b0522d4fb2c71e004b82ba8b7343913a15def465f"
 'audio': {'path': "/.cache/huggingface/datasets/downloads/af7e748544004557b35eef8b0522d4fb2c71e004b82ba8b7343913a15def465f",
	  	   'array': array([-0.00048828, -0.00018311, -0.00137329, ...,  0.00079346, 0.00091553,  0.00085449], dtype=float32),
	  	   'sampling_rate': 16000},
}
```

### Data Fields

- word_ids: a list of the ids of the words

- word_start_times: a list of the start times of when the words were spoken in seconds

- word_end_times: a list of the end times of when the words were spoken in seconds

- word_speakers: a list of speakers one for each word

- segment_ids: a list of the ids of the segments

- segment_start_times: a list of the start times of when the segments start

- segment_end_times: a list of the start times of when the segments ends

- segment_speakers: a list of speakers one for each segment

- words: a list of all the spoken words

- channels: a list of all channels that were used for each word

- file: a path to the audio file

- audio: A dictionary containing the path to the downloaded audio file, the decoded audio array, and the sampling rate. Note that when accessing the audio column: `dataset[0]["audio"]` the audio file is automatically decoded and resampled to `dataset.features["audio"].sampling_rate`. Decoding and resampling of a large number of audio files might take a significant amount of time. Thus it is important to first query the sample index before the `"audio"` column, *i.e.* `dataset[0]["audio"]` should **always** be preferred over `dataset["audio"][0]`.

### Data Splits

The dataset consists of several configurations, each one having train/validation/test splits:

- headset-single: Close talking audio of single headset. This configuration only includes audio belonging to the headset of the person currently speaking.

- headset-multi (4 channels): Close talking audio of four individual headset. This configuration includes audio belonging to four individual headsets. For each annotation there are 4 audio files 0, 1, 2, 3.

- microphone-single: Far field audio of single microphone. This configuration only includes audio belonging the first microphone, *i.e.* 1-1, of the microphone array.

- microphone-multi (8 channels): Far field audio of microphone array. This configuration includes audio of the first microphone array 1-1, 1-2, ..., 1-8.

In general, `headset-single` and `headset-multi` include significantly less noise than 
`microphone-single` and `microphone-multi`.

|                             | Train | Valid | Test |
| -----                       | ------ | ----- | ---- |
| headset-single | 136 (80h) |  18 (9h) | 16 (9h) |
| headset-multi (4 channels) | 136 (320h) |  18 (36h) | 16 (36h) |
| microphone-single | 136 (80h) |  18 (9h) | 16 (9h) |
| microphone-multi (8 channels) | 136 (640h) |  18 (72h) | 16 (72h) |

Note that each sample contains between 10 and 60 minutes of audio data which makes it 
impractical for direct transcription. One should make use of the segment and word start times and end times to chunk the samples into smaller samples of manageable size.

## Dataset Creation

All information about the dataset creation can be found 
[here](https://groups.inf.ed.ac.uk/ami/corpus/overview.shtml)

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

CC BY 4.0

### Citation Information
#### TODO

### Contributions

Thanks to [@cahya-wirawan](https://github.com/cahya-wirawan) and [@patrickvonplaten](https://github.com/patrickvonplaten) for adding this dataset.
#### TODO
