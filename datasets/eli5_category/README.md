---
annotations_creators:
- found
language_creators:
- found
languages:
- en
licenses:
- unknown
multilinguality:
- monolingual
paperswithcode_id: null
pretty_name: ELI5-Category
size_categories:
- 100K<n<1M
source_datasets:
- extended|eli5
task_categories:
- text2text-generation
task_ids:
- abstractive-qa
- open-domain-abstractive-qa
---

# Dataset Card for ELI5-Category

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


- **Homepage:** [ELI5-Category homepage](https://celeritasml.netlify.app/posts/2021-12-01-eli5c/)
- **Repository:** [ELI5-Category repository](https://github.com/rexarski/ANLY580-final-project)
- **Point of Contact:** [Jingsong Gao](mailto:jg2109@georgetown.edu)

### Dataset Summary

The ELI5-Category dataset is a smaller but newer and categorized version of the original ELI5 dataset. It's an English-language dataset of questions and answers gathered from the [r/explainlikeimfive](https://www.reddit.com/r/explainlikeimfive/) subreddit where users ask factual questions requiring paragraph-length or longer answers. After 2017, a tagging system was introduced to this subreddit so that the questions can be categorized into different topics according to their tags. Since the training and validation set is built by questions in different topics, the dataset is expected to alleviate the train/validation overlapping issue in the original [ELI5 dataset](https://huggingface.co/datasets/eli5).

### Supported Tasks and Leaderboards

- `abstractive-qa`, `open-domain-abstractive-qa`: The dataset can be used to train a model for Open Domain Long Form Question Answering. An LFQA model is presented with a non-factoid and asked to retrieve relevant information from a knowledge source (such as [Wikipedia](https://www.wikipedia.org/)), then use it to generate a multi-sentence answer. 

### Languages

The text in the dataset is in English, as spoken by Reddit users on the  [r/explainlikeimfive](https://www.reddit.com/r/explainlikeimfive/) subreddit. The associated BCP-47 code is `en`.

## Dataset Structure

### Data Instances

The structure of this dataset is very similar to the original [ELI5 dataset](https://huggingface.co/datasets/eli5). A typical data point comprises a question, with a `title` containing the main question and a `selftext` which sometimes elaborates on it, and a list of answers from the forum sorted by scores they obtained. Additionally, the URLs in each of the text fields have been extracted to respective lists and replaced by generic tokens in the text.   
In addition to the original ELI5 dataset, the data point also has a `category` field. There are 11 common values of `category` in this dataset: `Biology`,`Chemistry`,`Culture`,`Earth Science`,`Economics`,`Engineering`,`Mathematics`,`Other`,`Physics`,`Psychology`,`Technology`, and a special `category`: `Repost` indicates the same question has been asked before.
 
An example from the ELI5-Category set looks as follows:
```
{'q_id': '5lcm18',
 'title': 'Why do old games running on new hardware still have technical issues ?',
 'selftext': 'I am playing some mega man games on my Xbox One and experience slowdown when there are a lot of enemies on screen . but the Xbox One is significantly more powerful than the NES , so why is there still slowdown on this hardware ?',
 'category': 'Engineering',
 'subreddit': 'explainlikeimfive',
 'answers': {'a_id': ['dbuo48e', 'dbusfve'],
  'text': ["The XBox is emulating NES hardware and running the emulation at a set speed . If it ran it at as fast as possible , then it would be several times faster than the original NES game and would be unplayable . I ca n't speak for Mega Man exactly , but older games tended to run on a cycle locked to the screen refresh which was a fixed 60Hz or 50Hz . There was only one piece of hardware they ran on , so there was no need to adjust for different hardware speeds .",
            "In that case , it 's probably on purpose - they want to emulate the experience as closely as possible , even including the slowdown and sprite flickering . Some emulators let you turn it off , but it 's usually turned on by default . In other cases , like if you 're trying to emulate PS2 games on your PC , the game might just run really slow in general . Even though your PC is way more powerful than a PS2 , it has to \" translate \" from PS2 language to PC language in realtime , which is much more difficult than running PS2 code on the PS2 itself ."],
  'score': [13, 3],
  'text_urls': [[],[]]},
 'title_urls': {'url': []},
 'selftext_urls': {'url': []}}
```

### Data Fields

- `q_id`: a string question identifier for each example, corresponding to its ID in the [Pushshift.io](https://files.pushshift.io/reddit/submissions/) Reddit submission dumps
- `subreddit`: always `explainlikeimfive`, indicating which subreddit the question came from
- `category`: tag of the question, the possible values are listed above.
- `title`: title of the question, with URLs extracted and replaced by `URL_n` tokens
- `title_urls`: list of the extracted URLs, the `n`th element of the list was replaced by `URL_n`
- `selftext`: either an empty string or an elaboration of the question
- `selftext_urls`: similar to `title_urls` but for `self_text`
- `answers`: a list of answers, each answer has:
  - `a_id`: a string answer identifier for each answer, corresponding to its ID in the [Pushshift.io](https://files.pushshift.io/reddit/comments/) Reddit comments dumps.
  - `text`: the answer text with the URLs normalized
  - `score`: the number of upvotes - the number of downvotes the answer had received when the dumps were created
  - `text_urls`: lists of the extracted URLs for every answer

### Data Splits

In order to avoid having duplicate questions across sets, three non-overlapping subsets of `category` are used in the training, validation and test set. Also, a special validation set contains all the questions in the `Repost` category. A valid retriever-generator model should have consistent performances on both validation sets.  
The final split sizes are as follows:

|                   | Train   | Valid | Valid2 |Test |
| -----             | ------ | ----- | ---- | ---- |
| `Biology`         | 32769 |       |       |      |
| `Chemistry`       | 6633  |       |       |      |
| `Culture`         |       | 5446  |       |      |
| `Earth Science`   | 677   |       |       |      |
| `Economics`       | 5901  |       |       |      |
| `Engineering`     |       |       |       | 5411 |
| `Mathematics`     | 1912  |       |       |      |
| `Other`           | 19312 |       |       |      |
| `Physics`         | 10196 |       |       |      |
| `Psychology`      | 338   |       |       |      |
| `Technology`      | 14034 |       |       |      |
| `Repost`          |       |       | 2375  |      |
| **Total**         | 91772 | 5446  | 2375  | 5411 |

## Dataset Creation

### Curation Rationale

ELI5-Category was built to provide a testbed for machines to learn how to answer more complex questions, which requires them to find and combine the information in a coherent manner. The dataset was built by gathering questions that were asked by community members of three subreddits, including [r/explainlikeimfive](https://www.reddit.com/r/explainlikeimfive/), along with the answers that were provided by other users. The [rules of the subreddit](https://www.reddit.com/r/explainlikeimfive/wiki/detailed_rules) make this data particularly well suited to training a model for abstractive question answering: the questions need to seek an objective explanation about well-established facts, and the answers provided need to be understandable to a layperson without any particular knowledge domain.

### Source Data

#### Initial Data Collection and Normalization

The data was obtained by filtering submissions and comments from the subreddits of interest from the XML dumps of the [Reddit forum](https://www.reddit.com/) hosted on [Pushshift.io](https://files.pushshift.io/reddit/).

In order to further improve the quality of the selected examples, only questions with a score of at least 2 and at least one answer with a score of at least 2 were selected for the dataset. The dataset questions and answers span a period from January 2017 to June 2021.

#### Who are the source language producers?

The language producers are users of the [r/explainlikeimfive](https://www.reddit.com/r/explainlikeimfive/) subreddit between 2017 and 2021. No further demographic information was available from the data source.

### Annotations

The dataset contains the `category` as an additional annotation for the topics of questions.

#### Annotation process

The dataset is auto-annotated by the tags of posts in the [Reddit forum](https://www.reddit.com/). 

#### Who are the annotators?

The annotators are users/administrators of the [r/explainlikeimfive](https://www.reddit.com/r/explainlikeimfive/) subreddit between 2017 and 2021. No further demographic information was available from the data source.

### Personal and Sensitive Information

The authors removed the speaker IDs from the [Pushshift.io](https://files.pushshift.io/reddit/) dumps but did not otherwise anonymize the data. Some questions and answers are about contemporary public figures or individuals who appeared in the news.

## Considerations for Using the Data

### Social Impact of Dataset

The dataset has a similar social impact to the original ELI5 dataset [Social Impact of Dataset](https://huggingface.co/datasets/eli5#social-impact-of-dataset).

### Discussion of Biases

The dataset has similar considerations of biases to the original ELI5 dataset [Discussion of Biases](https://huggingface.co/datasets/eli5#discussion-of-biases).

### Other Known Limitations

The dataset has similar limitations to the original ELI5 dataset [Other Known Limitations](https://huggingface.co/datasets/eli5#other-known-limitations).

## Additional Information

### Dataset Curators

The dataset was initially created by Jingsong Gao, Qinren Zhou, Rui Qiu, during a course project of `ANLY 580`: NLP for Data Analytics at Georgetown University.

### Licensing Information

The licensing status of the dataset hinges on the legal status of the [Pushshift.io](https://files.pushshift.io/reddit/) data which is unclear.

### Citation Information

```
@inproceedings{eli5-category,
  author    = {Jingsong Gao and
               Qingren Zhou and
               Rui Qiu},
  title     = {{ELI5-Category:} A categorized open-domain QA dataset},
  year      = {2021}
}
```

### Contributions

Thanks to [@jingshenSN2](https://github.com/jingshenSN2), [@QinrenZhou](https://github.com/QinrenZhou), [@rexarski](https://github.com/rexarski) for adding this dataset.