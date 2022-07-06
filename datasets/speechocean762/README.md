---
annotations_creators:
- expert-generated
language_creators:
- expert-generated
languages:
- en
licenses:
- cc-by-4.0
multilinguality:
- monolingual
pretty_name: speechocean762
size_categories:
- 100M<n<1B
source_datasets:
- original
task_categories:
- automatic-speech-recognition
- audio-classification
- pronunciation-scoring
task_ids: []
---

# Dataset Card for speechocean762

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

- **Homepage:** https://www.openslr.org/101/
- **Repository:** https://github.com/jimbozhang/speechocean762
- **Paper:** https://arxiv.org/abs/2104.01378
- **Leaderboard:** https://paperswithcode.com/dataset/speechocean762
- **Point of Contact:** [Junbo Zhang](mailto:dr.jimbozhang@gmail.com)

### Dataset Summary

Pronunciation scoring is a crucial technology in computer-assisted language learning (CALL) systems. The pronunciation quality scores might be given at phoneme-level, word-level, and sentence-level for a typical pronunciation scoring task.

This corpus aims to provide a free public dataset for the pronunciation scoring task. Key features:

It is available for free download for both commercial and non-commercial purposes.
* The speaker variety encompasses young children and adults.
* The manual annotations are in multiple aspects at sentence-level, word-level and phoneme-level.
* This corpus consists of 5000 English sentences. All the speakers are non-native, and their mother tongue is Mandarin. Half of the speakers are Children, and the others are adults. The information on age and gender are provided.

Five experts made the scores. To avoid subjective bias, each expert scores independently under the same metric.

### Supported Tasks and Leaderboards

-`pronunciation scoring`: This dataset is designed for pronunciation assessment at sentence-level, word-level and phoneme-level.

https://paperswithcode.com/dataset/speechocean762


### Languages

English. The mother tongue of the speakers is Mandarin. 

## Data Splits

The dataset is split into a training and test set.


## Scoring metric

The experts score at three levels: phoneme-level, word-level, and sentence-level.

### Phoneme level
Score the pronunciation goodness of each phoneme within the words.

Score range: 0-2
* 2: pronunciation is correct
* 1: pronunciation is right but has a heavy accent
* 0: pronunciation is incorrect or missed

### Word level
Score the accuracy and stress of each word's pronunciation.

#### Accuracy
Score range: 0 - 10
* 10: The pronunciation of the word is perfect
* 7-9: Most phones in this word are pronounced correctly but have accents
* 4-6: Less than 30% of phones in this word are wrongly pronounced
* 2-3: More than 30% of phones in this word are wrongly pronounced. In another case, the word is mispronounced as some other word. For example, the student mispronounced the word "bag" as "bike"
* 1: The pronunciation is hard to distinguish
* 0: no voice

#### Stress
Score range: {5, 10}
* 10: The stress is correct, or this is a mono-syllable word
* 5: The stress is wrong

### Sentence level
Score the accuracy, fluency, completeness and prosodic at the sentence level.

#### Accuracy
Score range: 0 - 10
* 9-10: The overall pronunciation of the sentence is excellent, with accurate phonology and no obvious pronunciation mistakes
* 7-8: The overall pronunciation of the sentence is good, with a few pronunciation mistakes
* 5-6: The overall pronunciation of the sentence is understandable, with many pronunciation mistakes and accent, but it does not affect the understanding of basic meanings
* 3-4: Poor, clumsy and rigid pronunciation of the sentence as a whole, with serious pronunciation mistakes
* 0-2: Extremely poor pronunciation and only one or two words are recognizable

#### Completeness
Score range: 0.0 - 1.0
The percentage of the words with good pronunciation.

#### Fluency
Score range: 0 - 10
* 8-10: Fluent without noticeable pauses or stammering
* 6-7: Fluent in general, with a few pauses, repetition, and stammering
* 4-5: the speech is a little influent, with many pauses, repetition, and stammering
* 0-3: intermittent, very influent speech, with lots of pauses, repetition, and stammering

#### Prosodic
Score range: 0 - 10
* 9-10: Correct intonation at a stable speaking speed, speak with cadence, and can speak like a native
* 7-8:  Nearly correct intonation at a stable speaking speed, nearly smooth and coherent, but with little stammering and few pauses
* 5-6: Unstable speech speed, many stammering and pauses with a poor sense of rhythm
* 3-4: Unstable speech speed, speak too fast or too slow, without the sense of rhythm
* 0-2: Poor intonation and lots of stammering and pauses, unable to read a complete sentence
