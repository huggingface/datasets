---
annotations_creators:
- crowdsourced
language_creators:
- crowdsourced
languages:
- en
licenses:
- unknown
multilinguality:
- monolingual
size_categories:
- 10K<n<100K
source_datasets:
- original
task_categories:
- question-answering
task_ids:
- open-domain-qa
paperswithcode_id: tweetqa
---

# Dataset Card for TweetQA

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

- **Homepage: [TweetQA homepage](https://tweetqa.github.io/)**
- **Repository: **
- **Paper: [TweetQA paper]([TweetQA repository](https://tweetqa.github.io/)**
- **Leaderboard:**
- **Point of Contact: [Wenhan Xiong](xwhan@cs.ucsb.edu)**

### Dataset Summary


### Supported Tasks and Leaderboards

[More Information Needed]

### Languages

[More Information Needed]

## Dataset Structure

### Data Instances
Sample data:
```
{
    "Question": "who is the tallest host?",
    "Answer": ["sam bee","sam bee"],
    "Tweet": "Don't believe @ConanOBrien's height lies. Sam Bee is the tallest host in late night. #alternativefacts\u2014 Full Frontal (@FullFrontalSamB) January 22, 2017",
    "qid": "3554ee17d86b678be34c4dc2c04e334f"
}
```
### Data Fields

Question: a question based on information from a tweet
Answer: list of possible answers from the tweet
Tweet: source tweet
qid: question id

### Data Splits

The dataset is split in train, validation and test.
The test split doesn't include answers so the Answer field is an empty list.

[More Information Needed]

## Dataset Creation

### Curation Rationale

With social media becoming increasingly popular on which lots of news and real-time events are reported, developing automated question answering systems is critical to the effectiveness of many applications that rely on realtime knowledge. While previous datasets have concentrated on question answering (QA) for formal text like news and Wikipedia, we present the first large-scale dataset for QA over social media data. To ensure that the tweets we collected are useful, we only gather tweets used by journalists to write news articles. We then ask human annotators to write questions and answers upon these tweets. Unlike other QA datasets like SQuAD in which the answers are extractive, we allow the answers to be abstractive

### Source Data

#### Initial Data Collection and Normalization

We first describe the three-step data collection process of TWEETQA: tweet crawling, question-answer writing and answer validation.  Next, we define the specific task of TWEETQA and discuss several evaluation metrics. To better understand the characteristics of the TWEETQA task, we also include our analysis on the answer and question characteristics using a subset of QA pairs from the development set.

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

[Wenhan Xiong](xwhan@cs.ucsb.edu) of UCSB

### Licensing Information

[More Information Needed]

### Citation Information

@misc{xiong2019tweetqa,
      title={TWEETQA: A Social Media Focused Question Answering Dataset},
      author={Wenhan Xiong and Jiawei Wu and Hong Wang and Vivek Kulkarni and Mo Yu and Shiyu Chang and Xiaoxiao Guo and William Yang Wang},
      year={2019},
      eprint={1907.06292},
      archivePrefix={arXiv},
      primaryClass={cs.CL}
}

### Contributions

Thanks to [@anaerobeth](https://github.com/anaerobeth) for adding this dataset.