---
annotations_creators:
- crowdsourced
language_creators:
- crowdsourced
languages:
- en
licenses:
- cc-by-sa-4.0
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
pretty_name: TweetQA
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

- **Homepage:** [TweetQA homepage](https://tweetqa.github.io/)
- **Repository:**
- **Paper:** [TWEETQA: A Social Media Focused Question Answering Dataset](https://arxiv.org/abs/1907.06292)
- **Leaderboard:** [TweetQA Leaderboard](https://tweetqa.github.io/)
- **Point of Contact:** [Wenhan Xiong](xwhan@cs.ucsb.edu)

### Dataset Summary

With social media becoming increasingly popular on which lots of news and real-time events are reported, developing automated question answering systems is critical to the effectiveness of many applications that rely on real-time knowledge. While previous question answering (QA) datasets have concentrated on formal text like news and Wikipedia, the first large-scale dataset for QA over social media data is presented. To make sure the tweets are meaningful and contain interesting information, tweets used by journalists to write news articles are gathered. Then human annotators are asked to write questions and answers upon these tweets. Unlike other QA datasets like SQuAD in which the answers are extractive, the answer are allowed to be abstractive. The task requires model to read a short tweet and a question and outputs a text phrase (does not need to be in the tweet) as the answer.

### Supported Tasks and Leaderboards

- `question-answering`: The dataset can be used to train a model for Open-Domain Question Answering where the task is to answer the given questions for a tweet. The performance is measured by comparing the model answers to the the annoted groundtruth and calculating the BLEU-1/Meteor/ROUGE-L score. This task has an active leaderboard which can be found [here](https://tweetqa.github.io/) and ranks models based on [BLEU-1](https://huggingface.co/metrics/blue), [Meteor](https://huggingface.co/metrics/meteor) and [ROUGLE-L](https://huggingface.co/metrics/rouge).

### Languages

English.

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

The test split doesn't include answers so the Answer field is an empty list.

### Data Fields

- `Question`: a question based on information from a tweet
- `Answer`: list of possible answers from the tweet
- `Tweet`: source tweet
- `qid`: question id

### Data Splits

The dataset is split in train, validation and test set. The train set cointains 10692 examples, the validation set 1086 and the test set 1979 examples.

## Dataset Creation

### Curation Rationale

With social media becoming increasingly popular on which lots of news and real-time events are reported, developing automated question answering systems is critical to the effectiveness of many applications that rely on real-time knowledge. While previous question answering (QA) datasets have concentrated on formal text like news and Wikipedia, the first large-scale dataset for QA over social media data is presented. To make sure the tweets are meaningful and contain interesting information, tweets used by journalists to write news articles are gathered. Then human annotators are asked to write questions and answers upon these tweets. Unlike other QA datasets like SQuAD in which the answers are extractive, the answer are allowed to be abstractive. The task requires model to read a short tweet and a question and outputs a text phrase (does not need to be in the tweet) as the answer.

### Source Data

#### Initial Data Collection and Normalization

The authors look into the the archived snapshots of two major news websites (CNN, NBC), and then extract the tweet blocks that are embedded in the news articles. In order to get enough data, they first extract the URLs of all section pages (e.g. World, Politics, Money, Tech) from the snapshot of each home page and then crawl all articles with tweets from these section pages. Then, they filter out the tweets that heavily rely on attached media to convey information, for which they utilize a state-of-the-art semantic role labeling model trained on CoNLL-2005 (He et al., 2017) to analyze the predicate-argument structure of the tweets collected from news articles and keep
only the tweets with more than two labeled arguments. This filtering process also automatically
filters out most of the short tweets. For the tweets collected from CNN, 22.8% of them were filtered
via semantic role labeling. For tweets from NBC, 24.1% of the tweets were filtered.

#### Who are the source language producers?

Twitter users.

### Annotations

#### Annotation process

The Amazon Mechanical Turk workers were used to collect question-answer
pairs for the filtered tweets. For each Human Intelligence Task (HIT), the authors ask the worker to read three tweets and write two question-answer pairs for each tweet. To ensure the quality, they require the workers to be located in major English speaking countries (i.e. Canada, US, and UK) and have an acceptance rate larger than 95%. Since the authors use tweets as context, lots of important information are contained in hashtags or even emojis. Instead of only showing the text to the workers, they use javascript to directly embed the whole tweet into each HIT. This gives workers the same experience as reading tweets via web browsers and help them to better compose questions. To avoid trivial questions that can be simply answered by superficial text matching methods or too challenging questions that require background knowledge, the authors explicitly state the following items in the HIT instructions for question writing:
- No Yes-no questions should be asked.
- The question should have at least five words.
- Videos, images or inserted links should not
be considered.
- No background knowledge should be required to answer the question.
To help the workers better follow the instructions, they also include a representative example showing both good and bad questions or answers in the instructions. As for the answers, since the context they consider is relatively shorter than the context of previous datasets, they do not restrict the answers to be in the tweet, otherwise, the task may potentially be simplified as a classification problem. The workers are allowed to write their answers in their own words, but the authors require the answers to be brief and can be directly inferred from the tweets. After they retrieve the QA pairs from all HITs, they conduct further post-filtering to filter out the pairs from workers that obviously do not follow instructions. They remove QA pairs with yes/no answers. Questions with less than five words are also filtered out. This process filtered 13% of the QA pairs. The dataset now includes 10,898 articles, 17,794 tweets, and 13,757 crowdsourced question-answer pairs. All QA pairs were written by 492 individual workers. 

#### Who are the annotators?

Amazon Mechanical Turk workers.

### Personal and Sensitive Information

[More Information Needed]

## Considerations for Using the Data

### Social Impact of Dataset

[More Information Needed]

### Discussion of Biases

From the paper:
> It is also worth noting that the data collected from social media can not only capture events and developments in real-time but also capture individual opinions and thus requires reasoning related to the authorship of the content as is illustrated in Table 1.

> Specifically, a significant amount of questions require certain reasoning skills that are specific to social media data:
- Understanding authorship: Since tweets are highly personal, it is critical to understand how questions/tweets related to the authors.
- Oral English & Tweet English: Tweets are often oral and informal. QA over tweets requires the understanding of common oral English. Our TWEETQA also requires understanding some tweet-specific English, like conversation-style English.
- Understanding of user IDs & hashtags: Tweets often contains user IDs and hashtags, which are single special tokens. Understanding these special tokens is important to answer person- or event-related questions.

### Other Known Limitations

[More Information Needed]

## Additional Information

The annotated answers are validated by the authors as follows:
For the purposes of human performance evaluation and inter-annotator agreement checking, the authors launch a different set of HITs to ask workers to answer questions in the test and development set. The workers are shown with the tweet blocks as well as the questions collected in the previous step. At this step, workers are allowed to label the questions as “NA” if they think the questions are not answerable. They find that 3.1% of the questions are labeled as unanswerable by the workers (for SQuAD, the ratio is 2.6%). Since the answers collected at this step and previous step are written by different workers, the answers can be written in different text forms even they are semantically equal to each other. For example, one answer can be “Hillary Clinton” while the other is “@HillaryClinton”. As it is not straightforward to automatically calculate the overall agreement, they manually check the agreement on a subset of 200 random samples from the development set and ask an independent human moderator to verify the result. It turns out that 90% of the answers pairs are semantically equivalent, 2% of them are partially equivalent (one of them is incomplete) and 8% are totally inconsistent. The answers collected at this step are also used to measure the human performance. 59 individual workers participated in this process.

### Dataset Curators

Xiong, Wenhan and Wu, Jiawei and Wang, Hong and Kulkarni, Vivek and Yu, Mo and Guo, Xiaoxiao and Chang, Shiyu and Wang, William Yang.

### Licensing Information

CC BY-SA 4.0.

### Citation Information

```
@inproceedings{xiong2019tweetqa,
  title={TweetQA: A Social Media Focused Question Answering Dataset},
  author={Xiong, Wenhan and Wu, Jiawei and Wang, Hong and Kulkarni, Vivek and Yu, Mo and Guo, Xiaoxiao and Chang, Shiyu and Wang, William Yang},
  booktitle={Proceedings of the 57th Annual Meeting of the Association for Computational Linguistics},
  year={2019}
}
```

### Contributions

Thanks to [@anaerobeth](https://github.com/anaerobeth) for adding this dataset.
