---
annotations_creators:
- expert-generated
language_creators:
- expert-generated
languages:
- bg
licenses:
- unknown
multilinguality:
- monolingual
size_categories:
- 1K<n<10K
source_datasets:
- original
task_categories:
- text-classification
task_ids:
- fact-checking
paperswithcode_id: null
---

# Dataset Card for Clickbait/Fake News in Bulgarian

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

- **Homepage:** [Data Science Society / Case Fake News](https://gitlab.com/datasciencesociety/case_fake_news)
- **Repository:** [Data Science Society / Case Fake News / Data](https://gitlab.com/datasciencesociety/case_fake_news/-/tree/master/data)
- **Paper:** [This paper uses the dataset.](https://www.acl-bg.org/proceedings/2017/RANLP%202017/pdf/RANLP045.pdf)
- **Leaderboard:**
- **Point of Contact:**

### Dataset Summary

This is a corpus of Bulgarian news over a fixed period of time, whose factuality had been questioned. 
The news come from 377 different sources from various domains, including politics, interesting facts and tips&tricks.

The dataset was prepared for the Hack the
Fake News hackathon. It was provided by the
[Bulgarian Association of PR Agencies](http://www.bapra.bg/) and is
available in [Gitlab](https://gitlab.com/datasciencesociety/). 

The corpus was automatically collected, and then annotated by students of journalism. 

The training dataset contains 2,815 examples, where 1,940 (i.e., 69%) are fake news
and 1,968 (i.e., 70%) are click-baits; There are 761 testing examples. 

There is 98% correlation between fake news and clickbaits.

One important aspect about the training dataset is that it contains many repetitions.
This should not be surprising as it attempts to represent a natural distribution of factual
vs. fake news on-line over a period of time. As publishers of fake news often have a group of
websites that feature the same deceiving content, we should expect some repetition.
In particular, the training dataset contains
434 unique articles with duplicates. These articles have three reposts each on average, with
the most reposted article appearing 45 times.
If we take into account the labels of the reposted articles, we can see that if an article
is reposted, it is more likely to be fake news.
The number of fake news that have a duplicate in the training dataset are 1018 whereas,
the number of articles with genuine content
that have a duplicate article in the training set is 322.

(The dataset description is from the following [paper](https://www.acl-bg.org/proceedings/2017/RANLP%202017/pdf/RANLP045.pdf).)

### Supported Tasks and Leaderboards

[More Information Needed]

### Languages

Bulgarian

## Dataset Structure

### Data Instances

[More Information Needed]

### Data Fields

Each entry in the dataset consists of the following elements: 

* `fake_news_score` - a label indicating whether the article is fake or not

* `click_bait_score` - another label indicating whether it is a click-bait

* `content_title` - article heading

* `content_url` - URL of the original article

* `content_published_time` - date of publication

* `content` - article content 


### Data Splits

The **training dataset** contains 2,815 examples, where 1,940 (i.e., 69%) are fake news
and 1,968 (i.e., 70%) are click-baits; 

The **validation dataset** contains 761 testing examples. 

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

[More Information Needed]

### Citation Information

[More Information Needed]

### Contributions

Thanks to [@tsvm](https://github.com/tsvm), [@lhoestq](https://github.com/lhoestq) for adding this dataset.