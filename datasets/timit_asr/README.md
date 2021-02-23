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
testing.  The criteria for the subdivision is described in the file
"testset.doc".  THIS SUBDIVISION HAS NO RELATION TO THE DATA DISTRIBUTED ON
THE PROTOTYPE VERSION OF THE CDROM.


Core Test Set:

The test data has a core portion containing 24 speakers, 2 male and 1 female
from each dialect region.  The core test speakers are shown in Table 3.  Each
speaker read a different set of SX sentences.  Thus the core test material
contains 192 sentences, 5 SX and 3 SI for each speaker, each having a distinct
text prompt.


    Table 3:  The core test set of 24 speakers

     Dialect        Male      Female
     -------       ------     ------
        1        DAB0, WBT0    ELC0    
        2        TAS1, WEW0    PAS0    
        3        JMP0, LNT0    PKT0    
        4        LLL0, TLS0    JLM0    
        5        BPM0, KLT0    NLP0    
        6        CMJ0, JDH0    MGD0    
        7        GRT0, NJM0    DHC0
        8        JLN0, PAM0    MLD0    



Complete Test Set:

A more extensive test set was obtained by including the sentences from all
speakers that read any of the SX texts included in the core test set.  In
doing so, no sentence text appears in both the training and test sets.  This
complete test set contains a total of 168 speakers and 1344 utterances,
accounting for about 27% of the total speech material.  The resulting dialect
distribution of the 168 speaker test set is given in Table 4.  The complete
test material contains 624 distinct texts.


     Table 4:  Dialect distribution for complete test set

      Dialect    #Male   #Female   Total
      -------    -----   -------   -----
        1           7        4       11
        2          18        8       26
        3          23        3       26
        4          16       16       32
        5          17       11       28
        6           8        3       11
        7          15        8       23
        8           8        3       11
      -----      -----   -------   ------
      Total       112       56      168



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

[Needs More Information]

### Contributions

Thanks to [@patrickvonplaten](https://github.com/patrickvonplaten) for adding this dataset.
