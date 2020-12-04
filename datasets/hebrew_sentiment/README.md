---
annotations_creators:
- expert-generated
language_creators:
- found
languages:
- he
licenses:
- mit
multilinguality:
- monolingual
size_categories:
- 10K<n<100K
source_datasets:
- original
task_categories:
- text-classification
task_ids:
- sentiment-classification
---

# Dataset Card for HebrewSentiment

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

- **Homepage:** https://github.com/omilab/Neural-Sentiment-Analyzer-for-Modern-Hebrew
- **Repository:** https://github.com/omilab/Neural-Sentiment-Analyzer-for-Modern-Hebrew
- **Paper:** http://aclweb.org/anthology/C18-1190
- **Leaderboard:**
- **Point of Contact:** 

### Dataset Summary

HebrewSentiment is a data set consists of 12,804 user comments to posts on the official Facebook page of Israel’s
president, Mr. Reuven Rivlin. In October 2015, we used the open software application Netvizz (Rieder,
2013) to scrape all the comments to all of the president’s posts in the period of June – August 2014,
the first three months of Rivlin’s presidency.2 While the president’s posts aimed at reconciling tensions
and called for tolerance and empathy, the sentiment expressed in the comments to the president’s posts
was polarized between citizens who warmly thanked the president, and citizens that fiercely critiqued his
policy. Of the 12,804 comments, 370 are neutral; 8,512 are positive, 3,922 negative.

Data Annotation: 

### Supported Tasks and Leaderboards

Sentiment Analysis

### Languages

Hebrew

## Dataset Structure

tsv format:
{hebrew_sentence}\t{sentiment_label}

### Data Instances

רובי הייתי רוצה לראות ערביה נישאת ליהודי	1
תמונה יפיפיה-שפו	0
חייבים לעשות סוג של חרם כשכתבים שונאי ישראל עולים לשידור צריכים להעביר לערוץ אחר ואז תראו מה יעשה כוחו של הרייטינג ( בהקשר לדבריה של רינה מצליח )	2


### Data Fields

- `text`: The modern hebrew inpput text.
- `label`: The sentiment label. 0=positive , 1=negative, 2=off-topic.

### Data Splits

|                          | train  | test    |
|--------------------------|--------|---------|
| HebrewSentiment (token)  | 10243  | 2559    |
| HebrewSentiment (morph)  | 10243  | 2559    |


## Dataset Creation

### Curation Rationale

[More Information Needed]

### Source Data

#### Initial Data Collection and Normalization

User comments to posts on the official Facebook page of Israel’s
president, Mr. Reuven Rivlin. In October 2015, we used the open software application Netvizz (Rieder,
2013) to scrape all the comments to all of the president’s posts in the period of June – August 2014,
the first three months of Rivlin’s presidency.

#### Who are the source language producers?

[More Information Needed]

### Annotations

#### Annotation process

A trained researcher examined each comment and determined its sentiment value,
where comments with an overall positive sentiment were assigned the value 0, comments with an overall
negative sentiment were assigned the value 1, and comments that are off-topic to the post’s content
were assigned the value 2. We validated the coding scheme by asking a second trained researcher to
code the same data. There was substantial agreement between raters (N of agreements: 10623, N of
disagreements: 2105, Coehn’s Kappa = 0.697, p = 0).

#### Who are the annotators?

Researchers

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

OMIlab, The Open University of Israel

### Licensing Information


MIT License

Copyright (c) 2018 OMIlab, The Open University of Israel

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

### Citation Information

@inproceedings{amram-etal-2018-representations,
    title = "Representations and Architectures in Neural Sentiment Analysis for Morphologically Rich Languages: A Case Study from {M}odern {H}ebrew",
    author = "Amram, Adam  and
      Ben David, Anat  and
      Tsarfaty, Reut",
    booktitle = "Proceedings of the 27th International Conference on Computational Linguistics",
    month = aug,
    year = "2018",
    address = "Santa Fe, New Mexico, USA",
    publisher = "Association for Computational Linguistics",
    url = "https://www.aclweb.org/anthology/C18-1190",
    pages = "2242--2252",
    abstract = "This paper empirically studies the effects of representation choices on neural sentiment analysis for Modern Hebrew, a morphologically rich language (MRL) for which no sentiment analyzer currently exists. We study two dimensions of representational choices: (i) the granularity of the input signal (token-based vs. morpheme-based), and (ii) the level of encoding of vocabulary items (string-based vs. character-based). We hypothesise that for MRLs, languages where multiple meaning-bearing elements may be carried by a single space-delimited token, these choices will have measurable effects on task perfromance, and that these effects may vary for different architectural designs {---} fully-connected, convolutional or recurrent. Specifically, we hypothesize that morpheme-based representations will have advantages in terms of their generalization capacity and task accuracy, due to their better OOV coverage. To empirically study these effects, we develop a new sentiment analysis benchmark for Hebrew, based on 12K social media comments, and provide two instances of these data: in token-based and morpheme-based settings. Our experiments show that representation choices empirical effects vary with architecture type. While fully-connected and convolutional networks slightly prefer token-based settings, RNNs benefit from a morpheme-based representation, in accord with the hypothesis that explicit morphological information may help generalize. Our endeavour also delivers the first state-of-the-art broad-coverage sentiment analyzer for Hebrew, with over 89{\%} accuracy, alongside an established benchmark to further study the effects of linguistic representation choices on neural networks{'} task performance.",
}