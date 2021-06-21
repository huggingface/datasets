---
annotations_creators:
- crowdsourced
language_creators:
- other
languages:
- ar
licenses:
- unknown
multilinguality:
- monolingual
size_categories:
- 10K<n<100K
source_datasets:
- original
task_categories:
- text-classification
task_ids:
- text-classification-other-question-identification
paperswithcode_id: null
---

# Dataset Card for journalists_questions

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

- **Homepage:** http://qufaculty.qu.edu.qa/telsayed/datasets/
- **Repository:** [Needs More Information]
- **Paper:** https://www.aaai.org/ocs/index.php/ICWSM/ICWSM16/paper/download/13221/12856
- **Leaderboard:** [Needs More Information]
- **Point of Contact:** [Maram Hasanain]
maram.hasanain@qu.edu.qa

### Dataset Summary

The journalists_questions dataset supports question identification over Arabic tweets of journalists.


### Supported Tasks and Leaderboards

[More Information Needed]

### Languages

Arabic

## Dataset Structure

### Data Instances

Our dataset supports question identification task. It includes 10K Arabic tweets crawled from journalists accounts. Tweets were labelled by crowdsourcing. Each tweet is associated with one label: question tweet or not.  A question tweet is a tweet that has at least one interrogative question.  Each label is associated with a number that represents the confidence in the label, given that each tweet was labelled by 3 annotators and an aggregation method was followed to choose the final label.
Below is an example:
{
 'tweet_id': '493235142128074753',
 'label': 'yes',
 'label_confidence':0.6359
}


### Data Fields

tweet_id: the Twitter assigned ID for the tweet object.
label: annotation of the tweet by whether it is a question or not
label_confidence: confidence score for the label given annotations of multiple annotators per tweet

### Data Splits

[More Information Needed]

## Dataset Creation

### Curation Rationale

The dataset includes tweet IDs only due to Twitter content re-distribution policy. It was created and shared for research purposes for parties interested in understanding questions expecting answers by Arab journalists on Twitter.

### Source Data

#### Initial Data Collection and Normalization

To construct our dataset of question tweets posted by journalists, we first acquire a list of Twitter accounts of 389 Arab journalists. We use the Twitter API to crawl their available tweets, keeping only those that are identified by Twitter to be both Arabic, and not retweets (as these would contain content that was not originally authored by journalists). We apply a rule-based question filter to this dataset of 465,599 tweets, extracting 49,119 (10.6%) potential question tweets from 363 (93.3%) Arab journalists.

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

Thanks to [@MaramHasanain](https://github.com/MaramHasanain) for adding this dataset.