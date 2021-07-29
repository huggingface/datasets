---
annotations_creators:
- expert-generated
language_creators:
- found
languages:
- th
licenses:
- cc-by-nc-3.0
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
paperswithcode_id: null
---

# Dataset Card for `thai_toxicity_tweet`

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

- **Homepage:** https://github.com/tmu-nlp/ThaiToxicityTweetCorpus/
- **Repository:** https://github.com/tmu-nlp/ThaiToxicityTweetCorpus/
- **Paper:** https://www.ta-cos.org/sites/ta-cos.org/files/1_W32.pdf
- **Leaderboard:** 
- **Point of Contact:** https://www.ta-cos.org/sites/ta-cos.org/files/1_W32.pdf

### Dataset Summary

Thai Toxicity Tweet Corpus contains 3,300 tweets (506 tweets with texts missing) annotated by humans with guidelines including a 44-word dictionary.
The author obtained 2,027 and 1,273 toxic and non-toxic tweets, respectively; these were labeled by three annotators. The result of corpus
analysis indicates that tweets that include toxic words are not always toxic. Further, it is more likely that a tweet is toxic, if it contains
toxic words indicating their original meaning. Moreover, disagreements in annotation are primarily because of sarcasm, unclear existing
target, and word sense ambiguity.

Notes from data cleaner: The data is included into [huggingface/datasets](https://www.github.com/huggingface/datasets) in Dec 2020. By this time, 506 of the tweets are not available publicly anymore. We denote these by `TWEET_NOT_FOUND` in `tweet_text`.
Processing can be found at [this PR](https://github.com/tmu-nlp/ThaiToxicityTweetCorpus/pull/1).

### Supported Tasks and Leaderboards

text classification

### Languages

Thai (`th`)

## Dataset Structure

### Data Instances

```
{'is_toxic': 0, 'nontoxic_votes': 3, 'toxic_votes': 0, 'tweet_id': '898576382384418817', 'tweet_text': 'วันๆ นี่คุยกะหมา แมว หมู ไก่ ม้า ควาย มากกว่าคุยกับคนไปละ'}
{'is_toxic': 1, 'nontoxic_votes': 0, 'toxic_votes': 3, 'tweet_id': '898573084981985280', 'tweet_text': 'ควายแดงเมิงด่ารัฐบาลจนรองนายกป่วย พวกมึงกำลังทำลายชาติรู้มั้ย มั้ย มั้ย มั้ยยยยยยยยย news.voicetv.co.th/thailand/51672…'}
```

### Data Fields

"tweet_id": Id of tweet on Twitter
"tweet_text":  text of the tweet
"toxic_votes": how many annotators say it is toxic, out of 3 annotators
"nontoxic_votes":  how many annotators say it is NOT toxic, out of 3 annotators
"is_toxic": 1 if tweet is toxic else 0 (majority rules)

### Data Splits

No explicit split is given.

## Dataset Creation

### Curation Rationale

The dataset is created as part of [Sirihattasak et al (2019)](https://www.ta-cos.org/sites/ta-cos.org/files/1_W32.pdf).

### Source Data

#### Initial Data Collection and Normalization

The authors used the public Twitter Search API to collect 9,819 tweets from January–December 2017 based on our keyword dictionary. Then, they selected 75 tweets for each keyword. In total, they collected 3,300 tweets for annotation. To ensure quality of data, they set the following selection criteria.

1. All tweets are selected by humans to prevent word ambiguity. (The Twitter API selected the tweets based on characters in the keyword. For example, in the case of “บ้า(crazy),” the API will also select “บ้านนอก” (countryside)” which is not our target.) 
2. The length of the tweet should be sufficiently long to discern the context of the tweet. Hence, they set five words as the minimum limit.
3. The tweets that contain only extremely toxic words, (for example: “damn, retard, bitch, f*ck, slut!!!”) are not considered.
4. In addition, they allowed tweets with English words if they were not critical elements in the labeling decision, for example, the word “f*ck.” As a result, our corpus contains English words, but they are less than 2% of the total.

All hashtags, re-tweets, and links were removed from these tweets. However, they did not delete emoticons because these emotional icons can imply the real intent of the post owners. Furthermore, only in the case of annotation, some entries such as the names of famous people were replaced with a tag <ไม่ขอเปิดเผยชื่อ>, for anonymity to prevent individual bias.

#### Who are the source language producers?

Twitter users in Thailand

### Annotations

#### Annotation process

We manually annotated our dataset with two labels: Toxic and Non-Toxic. We define a message as toxic if it indicates any harmful, damage, or negative intent based on our definition of toxicity. Furthermore, all the tweets were annotated by three annotators to identify toxicity; the conditions used for this identification are presented in the following list.

- A toxic message is a message that should be deleted or not be allowed in public.
- A message’s target or consequence must exist. It can either be an individual or a generalized group based on a commonality such as religion or ethnicity, or an entire community.
- Self-complain is not considered toxic, because it is not harmful to anyone. However, if self-complain is intended to indicate something bad, it will be considered as toxic.
- Both direct and indirect messages including those with sarcasm are taken into consideration.

We strictly instructed all the annotators about these concepts and asked them to perform a small test to ensure they understood these conditions. The annotation process was divided into two rounds. We asked the candidates to annotate their answers in the first round to learn our annotation standard. Then, we asked them to annotate a different dataset and selected the ones who obtained a full-score for the second round as an annotator. From among these annotators, 20% of the annotators failed the first round and were not involved in the final annotation.

#### Who are the annotators?

Three annotators hired by [Sirihattasak et al (2019)](https://www.ta-cos.org/sites/ta-cos.org/files/1_W32.pdf)

### Personal and Sensitive Information

Despite all tweets being public, due to the nature of toxic tweets, there might be personal attacks and toxic language used.

## Considerations for Using the Data

### Social Impact of Dataset

- toxic social media message classification dataset

### Discussion of Biases

- Users are masked before annotation by the annotators to prevent biases based on tweet authors

### Other Known Limitations

- The data is included into [huggingface/datasets](https://www.github.com/huggingface/datasets) in Dec 2020. By this time, 506 of the tweets are not available publicly anymore. We denote these by `TWEET_NOT_FOUND` in `tweet_text`.

## Additional Information

### Dataset Curators

[Sirihattasak et al (2019)](https://www.ta-cos.org/sites/ta-cos.org/files/1_W32.pdf)

### Licensing Information

CC-BY-NC 3.0

### Citation Information

Please cite the following if you make use of the dataset:

```
@article{sirihattasak2019annotation,
  title={Annotation and Classification of Toxicity for Thai Twitter},
  author={Sirihattasak, Sugan and Komachi, Mamoru and Ishikawa, Hiroshi},
  year={2019}
}
```

### Contributions

Thanks to [@cstorm125](https://github.com/cstorm125) for adding this dataset.