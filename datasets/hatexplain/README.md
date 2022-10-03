---
annotations_creators:
- crowdsourced
language_creators:
- crowdsourced
language:
- en
license:
- cc-by-4.0
multilinguality:
- monolingual
size_categories:
- 10K<n<100K
source_datasets:
- original
task_categories:
- text-classification
task_ids:
- text-classification-other-hate-speech-detection
paperswithcode_id: hatexplain
pretty_name: hatexplain
---

# Dataset Card for hatexplain

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

- **Homepage:** [Needs More Information]
- **Repository:** https://github.com/punyajoy/HateXplain/
- **Paper:** https://arxiv.org/abs/2012.10289
- **Leaderboard:** [Needs More Information]
- **Point of Contact:** Punyajoy Saha (punyajoys@iitkgp.ac.in)

### Dataset Summary

Hatexplain is the first benchmark hate speech dataset covering multiple aspects of the issue. Each post in the dataset is annotated from three different perspectives: the basic, commonly used 3-class classification (i.e., hate, offensive or normal), the target community (i.e., the community that has been the victim of hate speech/offensive speech in the post), and the rationales, i.e., the portions of the post on which their labeling decision (as hate, offensive or normal) is based.

WARNING: This dataset contains content that are offensive and/or hateful in nature.

### Supported Tasks and Leaderboards

[Needs More Information]

### Languages

The language supported is English.

## Dataset Structure

### Data Instances

Sample Entry:
```
{
    "id": "24198545_gab",
    "annotators": [
      {
        "label": 0,  # hatespeech
        "annotator_id": 4,
        "target": ["African"]
      },
      {
        "label": 0,  # hatespeech
        "annotator_id": 3,
        "target": ["African"]
      },
      {
        "label": 2,  # offensive
        "annotator_id": 5,
        "target": ["African"]
      }
    ],
    "rationales":[
    [0,0,0,0,0,0,0,0,1,0,0,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    ],
    "post_tokens": ["and","this","is","why","i","end","up","with","nigger","trainee","doctors","who","can","not","speak","properly","lack","basic","knowledge","of","biology","it","truly","scary","if","the","public","only","knew"]
  }
}
```

### Data Fields

:small_blue_diamond:post_id : Unique id for each post<br/>
:small_blue_diamond:annotators : The list of annotations from each annotator<br/>
:small_blue_diamond:annotators[label] : The label assigned by the annotator to this post. Possible values: `hatespeech` (0), `normal` (1) or `offensive` (2)<br/>
:small_blue_diamond:annotators[annotator_id] : The unique Id assigned to each annotator<br/>
:small_blue_diamond:annotators[target] : A list of target community present in the post<br/>
:small_blue_diamond:rationales : A list of rationales selected by annotators. Each rationales represents a list with values 0 or 1. A value of 1 means that the token is part of the rationale selected by the annotator. To get the particular token, we can use the same index position in "post_tokens"<br/>
:small_blue_diamond:post_tokens : The list of tokens representing the post which was annotated<br/>

### Data Splits

[Post_id_divisions](https://github.com/hate-alert/HateXplain/blob/master/Data/post_id_divisions.json) has a dictionary having train, valid and test post ids that are used to divide the dataset into train, val and test set in the ratio of 8:1:1.



## Dataset Creation

### Curation Rationale

The existing hate speech datasets do not provide human rationale which could justify the human reasoning behind their annotation process. This dataset allows researchers to move a step in this direction. The dataset provides token-level annotatoins for the annotation decision.

### Source Data

We collected the data from Twitter and Gab.

#### Initial Data Collection and Normalization

We combined the lexicon set provided by [Davidson 2017](https://arxiv.org/abs/1703.04009),  [Ousidhoum 2019](https://arxiv.org/abs/1908.11049), and [Mathew 2019](https://arxiv.org/abs/1812.01693) to generate a single lexicon. We do not consider reposts and remove duplicates. We also ensure that the posts do not contain links, pictures, or videos as they indicate additional information that mightnot be available to the annotators. However, we do not exclude the emojis from the text as they might carry importantinformation for the hate and offensive speech labeling task.

#### Who are the source language producers?

The dataset is human generated using Amazon Mechanical Turk (AMT).

### Annotations

#### Annotation process

Each post in our dataset contains three types of annotations. First, whether the text is a hate speech, offensive speech, or normal. Second, the target communities in the text. Third, if the text is considered as hate speech, or offensive by majority of the annotators, we further ask the annotators to annotate parts of the text, which are words orphrases that could be a potential reason for the given annotation.  

Before starting the annotation task, workers are explicitly warned that the annotation task displays some hateful or offensive content. We prepare instructions for workers that clearly explain the goal of the annotation task, how to annotate spans and also include a definition for each category. We provide multiple examples with classification, target community and span annotations to help the annotators understand the task.

#### Who are the annotators?

To ensure high quality dataset, we use built-in MTurk qualification requirements, namely the HITApproval Rate(95%) for all Requesters’ HITs and the Number of HITs Approved(5,000) requirements.

Pilot annotation: In the pilot task, each annotator was provided with 20 posts and they were required to do the hate/offensive speech classification as well as identify the target community (if any). In order to have a clear understanding of the task, they were provided with multiple examples along with explanations for the labelling process. The main purpose of the pilot task was to shortlist those annotators who were able to do the classification accurately. We also collected feedback from annotators to improve the main annotation task. A total of 621 annotators took part in the pilot task. Out of these, 253 were selected for the main task.


Main annotation: After the pilot annotation, once we had ascertained the quality of the annotators, we started with the main annotation task. In each round, we would select a batch of around 200 posts. Each post was annotated by three annotators, then majority voting was applied to decide the final label. The final dataset is composed of 9,055 posts from Twitter and 11,093 posts from Gab. The Krippendorff's alpha for the inter-annotator agreement is 0.46 which is higher than other hate speech datasets.

### Personal and Sensitive Information

The posts were anonymized by replacing the usernames with <user> token. 

## Considerations for Using the Data

### Social Impact of Dataset

The dataset could prove beneficial to develop models which are more explainable and less biased.

### Discussion of Biases

[Needs More Information]

### Other Known Limitations

The dataset has some limitations. First is the lack of external context. The dataset lacks any external context such as profile bio, user gender, history of posts etc., which might be helpful in the classification task. Another issue is the focus on English language and lack of multilingual hate speech.

## Additional Information

### Dataset Curators

Binny Mathew - IIT Kharagpur, India
Punyajoy Saha - IIT Kharagpur, India
Seid Muhie Yimam - Universit ̈at Hamburg, Germany
Chris Biemann - Universit ̈at Hamburg, Germany
Pawan Goyal - IIT Kharagpur, India
Animesh Mukherjee - IIT Kharagpur, India

### Licensing Information

MIT License

### Citation Information

```bibtex
@article{mathew2020hatexplain,
      title={HateXplain: A Benchmark Dataset for Explainable Hate Speech Detection}, 
      author={Binny Mathew and Punyajoy Saha and Seid Muhie Yimam and Chris Biemann and Pawan Goyal and Animesh Mukherjee},
      year={2021},
      conference={AAAI conference on artificial intelligence}
}

### Contributions

Thanks to [@kushal2000](https://github.com/kushal2000) for adding this dataset.
