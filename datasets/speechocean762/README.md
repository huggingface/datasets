---
pretty_name: speechocean762
annotations_creators:
- expert-generated
language_creators:
- expert-generated
language:
- en
license:
- cc-by-4.0
multilinguality:
- monolingual
size_categories:
- 100M<n<1B
source_datasets:
- original
task_categories:
- audio-classification
task_ids:
- pronunciation-scoring
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

This dataset aims to provide a free public dataset for the pronunciation scoring task.

Five experts made the scores at phoneme-level, word-level, and sentence-level. To avoid subjective bias, each expert scores independently under the same metric.

### Supported Tasks and Leaderboards

-`pronunciation scoring`: This dataset is designed for pronunciation assessment at sentence-level, word-level and phoneme-level.

There is a [leaderboard](https://paperswithcode.com/dataset/speechocean762) for phoneme-level scoring on Papers With Code.



### Languages

English. Note that the mother tongue of all the speakers is Mandarin. 

## Dataset Structure

### Data Instances

Below is a typical meta data of an instance of the dataset:

```
"014350017": {    ,
    "speaker": "1435",
    "gender": "m",
    "age": 7,
    "text": "STEEVEN IS GOING TO SEE WHALE",
    "accuracy": 7,
    "completeness": 10,
    "fluency": 7,
    "prosodic": 7,
    "total": 6,
    "words": [
        {
        "accuracy": 10,
        "phones": ["S", "T", "IY1", "V", "AH0", "N"],
        "phones-accuracy": [2, 2, 2, 1.6, 2, 2],
        "stress": 10,
        "text": "STEEVEN",
        "total": 10,
        "mispronunciations": []
        },
        {
        "accuracy": 10,
        "phones": ["IH0", "Z"],
        "phones-accuracy": [2, 2],
        "stress": 10,
        "text": "IS",
        "total": 10,
        "mispronunciations": []
        },
        {
        "accuracy": 10,
        "phones": ["G", "OW0", "IH0", "NG"],
        "phones-accuracy": [
            2, 2, 2, 2],
        "stress": 10,
        "text": "GOING",
        "total": 10,
        "mispronunciations": []
        },
        {
        "accuracy": 10,
        "phones": ["T", "UW0"],
        "phones-accuracy": [2, 1.8],
        "stress": 10,
        "text": "TO",
        "total": 10,
        "mispronunciations": []
        },
        {
        "accuracy": 10,
        "phones": ["S", "IY0"],
        "phones-accuracy": [2, 2],
        "stress": 10,
        "text": "SEE",
        "total": 10,
        "mispronunciations": []
        },
        {
        "accuracy": 2,
        "mispronunciations": [
            {
            "canonical-phone": "W",
            "index": 0,
            "pronounced-phone": "<DEL>"
            },
            {
            "canonical-phone": "EY",
            "index": 1,
            "pronounced-phone": "OW"
            },
            {
            "canonical-phone": "L",
            "index": 2,
            "pronounced-phone": "L*"
            }
       ],
        "phones": ["W", "EY0", "L"],
        "phones-accuracy": [0, 0, 0.4],
        "stress": 10,
        "text": "WHALE",
        "total": 3
        }
   ]
}
```

### Data Fields

- text: transcript text

- accuracy: the pronunciation accuracy

- completeness: the percentage of the words in the target text that are actually pronounced

- fluency: intonation, stable speaking speed and rhythm

- stress: whether the stress position is correct

- mispronunciation: only available when phone accuracy is lower than 0.5. Indicates which phoneme the current phone was actually pronounced.



### Data Splits

Two splits: Train and Test, each with 2500 sentences.

## Dataset Creation

### Curation Rationale

Pronunciation scoring is a crucial technology in computer-assisted language learning (CALL) systems. To our knowledge, none of the existing non-native English corpora for pronunciation assessment contains all the following features:

- It is available for free download for both commercial and non-commercial purposes.
- The speaker variety encompasses young children and adults.
- The manual annotations are in many aspects at sentence-level, word-level and phoneme-level.

To meet these features, we created this corpus to support researchers in their pronunciation assessment studies.

### Source Data

#### Initial Data Collection and Normalization

This dataset's text script is selected from daily life text, containing about 2,600 common English words. Speakers were asked to hold their mobile phones 20cm from their mouths and read the text as accurately as possible in a quiet 3x3 meters room. The mobile phones include the popular models of Apple, Samsung, Xiaomi, and Huawei. The number of sentences reads aloud by each speaker is 20, and the total duration of the audio is about 6 hours.

#### Who are the source language producers?

The speakers are 250 English learners whose mother tongue is Mandarin. The training set and test set are divided randomly, with 125 speakers for each. We carefully selected the speakers considering gender, age and proficiency in English. The experts roughly rated the speaker's English pronunciation proficiency into three levels: good, average, and poor. The gender ratio is 1:1 for both adults and children.

### Annotations

#### Annotation process

The detail of the annotation process could be found in the [paper](https://arxiv.org/abs/2104.01378).

#### Who are the annotators?

Each utterance in this corpus is scored manually by five experts independently under the same metrics.

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

This dataset was initially created by Xiaomi Corporation and SpeechOcean Ltd.

### Licensing Information

This dataset is free to use for both commercial and non-commercial purposes. License: Attribution 4.0 International (CC BY 4.0).

### Citation Information

```
@inproceedings{speechocean762,
  title={speechocean762: An Open-Source Non-native English Speech Corpus For Pronunciation Assessment},
  booktitle={Proc. Interspeech 2021},
  year=2021,
  author={Junbo Zhang, Zhiwen Zhang, Yongqing Wang, Zhiyong Yan, Qiong Song, Yukai Huang, Ke Li, Daniel Povey, Yujun Wang}
}
```

### Contributions

Thanks to [@jimbozhang](https://github.com/jimbozhang) for adding this dataset.
