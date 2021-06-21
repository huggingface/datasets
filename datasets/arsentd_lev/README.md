---
annotations_creators:
- crowdsourced
language_creators:
- found
languages:
- apc
- apj
licenses:
- other-Copyright-2018-by-[American-University-of-Beirut]
multilinguality:
- monolingual
size_categories:
- 1K<n<10K
source_datasets:
- original
task_categories:
- text-classification
task_ids:
- sentiment-classification
- topic-classification
paperswithcode_id: arsentd-lev
---

# Dataset Card for ArSenTD-LEV

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

- **Homepage:** [ArSenTD-LEV homepage](http://oma-project.com/)
- **Paper:** [ArSentD-LEV: A Multi-Topic Corpus for Target-based Sentiment Analysis in Arabic Levantine Tweets](https://arxiv.org/abs/1906.01830)

### Dataset Summary

The Arabic Sentiment Twitter Dataset for Levantine dialect (ArSenTD-LEV) contains 4,000 tweets written in Arabic and equally retrieved from Jordan, Lebanon, Palestine and Syria.

### Supported Tasks and Leaderboards

Sentriment analysis

### Languages

Arabic Levantine Dualect

## Dataset Structure

### Data Instances

{'Country': 0,
 'Sentiment': 3,
 'Sentiment_Expression': 0,
 'Sentiment_Target': 'هاي سوالف عصابات ارهابية',
 'Topic': 'politics',
 'Tweet': 'ثلاث تفجيرات في #كركوك الحصيلة قتيل و 16 جريح بدأت اكلاوات كركوك كانت امان قبل دخول القوات العراقية ، هاي سوالف عصابات ارهابية'}

### Data Fields

`Tweet`: the text content of the tweet \
`Country`: the country from which the tweet was collected ('jordan', 'lebanon', 'syria', 'palestine')\
`Topic`: the topic being discussed in the tweet (personal, politics, religion, sports, entertainment and others) \
`Sentiment`: the overall sentiment expressed in the tweet (very_negative, negative, neutral, positive and very_positive) \
`Sentiment_Expression`: the way how the sentiment was expressed: explicit, implicit, or none (the latter when sentiment is neutral) \
`Sentiment_Target`: the segment from the tweet to which sentiment is expressed. If sentiment is neutral, this field takes the 'none' value.

### Data Splits

No standard splits are provided

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

Make sure to read and agree to the [license](http://oma-project.com/ArSenL/ArSenTD_Lev_Intro)

### Citation Information

```
@article{baly2019arsentd,
  title={Arsentd-lev: A multi-topic corpus for target-based sentiment analysis in arabic levantine tweets},
  author={Baly, Ramy and Khaddaj, Alaa and Hajj, Hazem and El-Hajj, Wassim and Shaban, Khaled Bashir},
  journal={arXiv preprint arXiv:1906.01830},
  year={2019}
}
```

### Contributions

Thanks to [@moussaKam](https://github.com/moussaKam) for adding this dataset.