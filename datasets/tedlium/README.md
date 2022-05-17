---
pretty_name: TED-LIUM
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
task_ids: []
---

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

The TED-LIUM corpus is English-language TED talks, with transcriptions, sampled at 16kHz. The three releases of the corpus range from 118 to 452 hours of transcribed speech data.


### Example 

```python
from datasets import load_dataset

tedlium = load_dataset("LIUM/tedlium", "release1") # for Release 1

# see structure
print(tedlium)

# load audio sample on the fly
audio_input = tedlium["train"][0]["audio"]  # first decoded audio sample
transcription = tedlium["train"][0]["text"]  # first transcription
```

### Supported Tasks and Leaderboards

- `automatic-speech-recognition`: The dataset can be used to train a model for Automatic Speech Recognition (ASR). The model is presented with an audio file and asked to transcribe the audio file to written text. The most common evaluation metric is the word error rate (WER). The task has an active leaderboard which can be found at https://paperswithcode.com/sota/speech-recognition-on-tedlium that ranks models based on their WER.

### Languages

The audio and transcriptions are in English, as per the TED talks at http://www.ted.com.

## Dataset Structure

### Data Instances
```
{'audio': {'path': '/home/sanchitgandhi/cache/downloads/extracted/6e3655f9e735ae3c467deed1df788e0dabd671c1f3e2e386e30aa3b571bd9761/TEDLIUM_release1/train/stm/PaulaScher_2008P.stm', 
  'array': array([-0.00048828, -0.00018311, -0.00137329, ...,  0.00079346,
          0.00091553,  0.00085449], dtype=float32),
  'sampling_rate': 16000},
'text': '{COUGH} but <sil> i was so {COUGH} utterly unqualified for(2) this project and {NOISE} so utterly ridiculous {SMACK} and ignored the brief {SMACK} <sil>', 
'speaker_id': 'PaulaScher_2008P', 
'gender': 'female', 
'file': '/home/sanchitgandhi/cache/downloads/extracted/6e3655f9e735ae3c467deed1df788e0dabd671c1f3e2e386e30aa3b571bd9761/TEDLIUM_release1/train/stm/PaulaScher_2008P.stm', 
'id': 'PaulaScher_2008P-1003.35-1011.16-<o,f0,female>'}
```
### Data Fields

- audio: A dictionary containing the path to the downloaded audio file, the decoded audio array, and the sampling rate. Note that when accessing the audio column: `dataset[0]["audio"]` the audio file is automatically decoded and resampled to `dataset.features["audio"].sampling_rate`. Decoding and resampling of a large number of audio files might take a significant amount of time. Thus it is important to first query the sample index before the `"audio"` column, *i.e.* `dataset[0]["audio"]` should **always** be preferred over `dataset["audio"][0]`. 
- file: A path to the downloaded audio file in .sth format.
- text: the transcription of the audio file.
- gender: the gender of the speaker. One of: male, female or N/A.
- id: unique id of the data sample.
- speaker_id: unique id of the speaker. The same speaker id can be found for multiple data samples.

### Data Splits
There are three releases for the TED-LIUM corpus, progressively increasing the number of transcribed speech training data from 118 hours (Release 1), to 207 hours (Release 2), to 452 hours (Release 3).

Release 1 (default config):
- 774 audio talks and automatically aligned transcriptions.
- Contains 118 hours of speech audio data.
- Homepage: https://www.openslr.org/7/

Release 2:
- 1495 audio talks and automatically aligned transcriptions.
- Contains 207 hours of speech audio data.
- Dictionary with pronunciations (159848 entries).
- Selected monolingual data for language modeling from WMT12 publicly available corpora.
- Homepage: https://www.openslr.org/19/

Release 3:
- 2351 audio talks and automatically aligned transcriptions.
- Contains 452 hours of speech audio data.
- TED-LIUM 2 validation and test data: 19 TED talks with their corresponding manual transcriptions.
- Dictionary with pronunciations (159848 entries), the same file as the one included in TED-LIUM 2.
- Selected monolingual data for language modeling from WMT12 publicly available corpora: these files come from the TED-LIUM 2 release, but have been modified to produce a tokenization more relevant for English language.
- Homepage: https://www.openslr.org/51/

Each release is split into a training, validation and test set:

| Split      | Release 1 | Release 2 | Release 3 |
|------------|-----------|-----------|-----------|
| Train      | 56,803    | 92,973    | 268,263   |
| Validation | 591       | 591       | 591       |
| Test       | 1,469     | 1,469     | 1,469     |


## Dataset Creation

### Curation Rationale

TED-LIUM was built during [The International Workshop on Spoken Language Trans- lation (IWSLT) 2011 Evaluation Campaign](https://aclanthology.org/2011.iwslt-evaluation.1/), an annual workshop focused on the automatic translation of public talks and included tracks for speech recognition, speech translation, text translation, and system combination. The corpus was entered 

### Source Data

#### Initial Data Collection and Normalization

The data was obtained from publicly available TED talks at http://www.ted.com. Proper alignments between the speech and the transcribed text were generated using an in-house speaker segmentation and clustering tool (LIUM_SpkDiarization). Speech disfluencies (e.g. repetitions, hesitations, false starts) were treated in the following way: the repetitions were transcribed, the hesitations were mapped to a specific filler word and the false starts were not taken into account. For full details on the data collection and processing, refer to the [TED-LIUM paper](https://aclanthology.org/L12-1405/).

#### Who are the source language producers?

TED Talks are influential videos from expert speakers on education, business, science, tech and creativity.

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

```
@inproceedings{rousseau2012tedlium,
  title={TED-LIUM: an Automatic Speech Recognition dedicated corpus},
  author={Rousseau, Anthony and Del{\'e}glise, Paul and Est{\`e}ve, Yannick},
  booktitle={Conference on Language Resources and Evaluation (LREC)},
  pages={125--129},
  year={2012}
}
```