---
annotations_creators:
- crowdsourced
language_creators:
- crowdsourced
languages:
- en
licenses:
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
---

# Dataset Card for hatexplain

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

- **Homepage:** [Needs More Information]
- **Repository:** https://github.com/punyajoy/HateXplain/
- **Paper:** https://arxiv.org/abs/2012.10289
- **Leaderboard:** [Needs More Information]
- **Point of Contact:** [Needs More Information]

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

[Post_id_divisions](https://github.com/punyajoy/HateXplain/blob/master/Data/post_id_divisions.json) has a dictionary having train, valid and test post ids that are used to divide the dataset into train, val and test set in the ratio of 8:1:1.



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

[Needs More Information]

### Discussion of Biases

[Needs More Information]

### Other Known Limitations

[Needs More Information]

## Additional Information

### Dataset Curators

[Needs More Information]

### Licensing Information

[Needs More Information]

### Citation Information

```bibtex
@misc{mathew2020hatexplain,
      title={HateXplain: A Benchmark Dataset for Explainable Hate Speech Detection}, 
      author={Binny Mathew and Punyajoy Saha and Seid Muhie Yimam and Chris Biemann and Pawan Goyal and Animesh Mukherjee},
      year={2020},
      eprint={2012.10289},
      archivePrefix={arXiv},
      primaryClass={cs.CL}
}

### Contributions

Thanks to [@kushal2000](https://github.com/kushal2000) for adding this dataset.