---
annotations_creators:
- no-annotation
language_creators:
- found
languages:
- en
licenses:
- unknown
multilinguality:
- monolingual
size_categories:
- 100K<n<1M
source_datasets:
- original
task_categories:
- question-answering
task_ids:
- abstractive-qa
- open-domain-qa
---

# Dataset Card for ELI5

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

- **Homepage:** [ELI5 homepage](https://facebookresearch.github.io/ELI5/explore.html)
- **Repository:** [ELI5 repository](https://github.com/facebookresearch/ELI5)
- **Paper:** [ELI5: Long Form Question Answering](https://arxiv.org/abs/1907.09190)
- **Point of Contact:** [Yacine Jernite](mailto:yacine@huggingface.co)

### Dataset Summary

The ELI5 dataset is an English-language dataset of questions and answers gathered from three subreddits were users ask factual questions requiring paragraph-length or longer answers. The dataset was created to support the task of open-domain long form abstractive question answering, and covers questions about general topics in its [r/explainlikeimfive](https://www.reddit.com/r/explainlikeimfive/) subset, science in it [r/askscience](https://www.reddit.com/r/askscience/) subset, and History in its [r/AskHistorians](https://www.reddit.com/r/AskHistorians/) subset.

### Supported Tasks and Leaderboards

- `abstractive-qa`, `open-domain-qa`: The dataset can be used to train a model for Open Domain Long Form Question Answering. An LFQA model is presented with a non-factoid and asked to retrieve relevant information from a knowledge source (such as [Wikipedia](https://www.wikipedia.org/)), then use it to generate a multi-sentence answer. The model performance is measured by how high its [ROUGE](https://huggingface.co/metrics/rouge) score to the reference is. A [BART-based model](https://huggingface.co/yjernite/bart_eli5) with a [dense retriever](https://huggingface.co/yjernite/retribert-base-uncased) trained to draw information from [Wikipedia passages](https://huggingface.co/datasets/wiki_snippets) achieves a [ROUGE-L of 0.149](https://yjernite.github.io/lfqa.html#generation).

### Languages

The text in the dataset is in English, as spoken by Reddit users on the  [r/explainlikeimfive](https://www.reddit.com/r/explainlikeimfive/), [r/askscience](https://www.reddit.com/r/askscience/), and [r/AskHistorians](https://www.reddit.com/r/AskHistorians/) subreddits. The associated BCP-47 code is `en`.

## Dataset Structure

### Data Instances

A typical data point comprises a question, with a `title` containing the main question and a `selftext` which sometimes elaborates on it, and a list of answers from the forum sorted by the number of upvotes they obtained. Additionally, the URLs in each of the text fields have been  extracted to respective lists and replaced by generic tokens in the text.

An example from the ELI5 test set looks as follows:
```
{'q_id': '8houtx',
 'title': 'Why does water heated to room temperature feel colder than the air around it?',
 'selftext': '',
 'document': '',
 'subreddit': 'explainlikeimfive',
 'answers': {'a_id': ['dylcnfk', 'dylcj49'],
  'text': ["Water transfers heat more efficiently than air. When something feels cold it's because heat is being transferred from your skin to whatever you're touching. Since water absorbs the heat more readily than air, it feels colder.",
   "Air isn't as good at transferring heat compared to something like water or steel (sit on a room temperature steel bench vs. a room temperature wooden bench, and the steel one will feel more cold).\n\nWhen you feel cold, what you're feeling is heat being transferred out of you.  If there is no breeze, you feel a certain way.  If there's a breeze, you will get colder faster (because the moving air is pulling the heat away from you), and if you get into water, its quite good at pulling heat from you.   Get out of the water and have a breeze blow on you while you're wet, all of the water starts evaporating, pulling even more heat from you."],
  'score': [5, 2]},
 'title_urls': {'url': []},
 'selftext_urls': {'url': []},
 'answers_urls': {'url': []}}
```

### Data Fields

- `q_id`: a string question identifier for each example, corresponding to its ID in the [Pushshift.io](https://files.pushshift.io/reddit/submissions/) Reddit submission dumps.
- `subreddit`: One of `explainlikeimfive`, `askscience`, or `AskHistorians`, indicating which subreddit the question came from
- `title`: title of the question, with URLs extracted and replaced by `URL_n` tokens
- `title_urls`: list of the extracted URLs, the `n`th element of the list was replaced by `URL_n`
- `selftext`: either an empty string or an elaboration of the question
- `selftext_urls`: similar to `title_urls` but for `self_text`
- `answers`: a list of answers, each answer has:
  - `a_id`: a string answer identifier for each answer, corresponding to its ID in the [Pushshift.io](https://files.pushshift.io/reddit/comments/) Reddit comments dumps.
  - `text`: the answer text with the URLs normalized
  - `score`: the number of upvotes the answer had received when the dumps were created
- `answers_urls`: a list of the extracted URLs. All answers use the same list, the numbering of the normalization token continues across answer texts

### Data Splits

The data is split into a training, validation and test set for each of the three subreddits. In order to avoid having duplicate questions in across sets, the `title` field of each of the questions were ranked by their tf-idf match to their nearest neighbor and the ones with the smallest value were used in the test and validation sets. The final split sizes are as follow:

|                             | Tain   | Valid | Test |
| -----                       | ------ | ----- | ---- |
| r/explainlikeimfive examples| 272634 |  9812 | 24512|
| r/askscience examples       | 131778 |  2281 | 4462 |
| r/AskHistorians examples    | 98525  |  4901 | 9764 |

## Dataset Creation

### Curation Rationale

ELI5 was built to provide a testbed for machines to learn how to answer more complex questions, which requires them to find and combine information in a coherent manner. The dataset was built by gathering questions that were asked by community members of three subreddits, including [r/explainlikeimfive](https://www.reddit.com/r/explainlikeimfive/), along with the answers that were provided by other users. The [rules of the subreddit](https://www.reddit.com/r/explainlikeimfive/wiki/detailed_rules) make this data particularly well suited to training a model for abstractive question answering: the questions need to seek an objective explanation about well established facts, and the answers provided need to be understandable to a layperson without any particular knowledge domain.

### Source Data

#### Initial Data Collection and Normalization

The data was obtained by filtering submissions and comments from the subreddits of interest from the XML dumps of the [Reddit forum](https://www.reddit.com/) hosted on [Pushshift.io](https://files.pushshift.io/reddit/).

In order to further improve the quality of the selected examples, only questions with a score of at least 2 and at least one answer with a score of at least 2 were selected for the dataset. The dataset questions and answers span a period form August 2012 to August 2019.

#### Who are the source language producers?

The language producers are users of the [r/explainlikeimfive](https://www.reddit.com/r/explainlikeimfive/), [r/askscience](https://www.reddit.com/r/askscience/), and [r/AskHistorians](https://www.reddit.com/r/AskHistorians/) subreddits between 2012 and 2019. No further demographic information was available from the data source.

### Annotations

The dataset does not contain any additional annotations.

#### Annotation process

[N/A]

#### Who are the annotators?

[N/A]

### Personal and Sensitive Information

The authors removed the speaker IDs from the [Pushshift.io](https://files.pushshift.io/reddit/) dumps but did not otherwise anonymize the data. Some of the questions and answers are about contemporary public figures or individuals who appeared in the news.

## Considerations for Using the Data

### Social Impact of Dataset

The purpose of this dataset is to help develop better question answering systems.

A system that succeeds at the supported task would be able to provide a coherent answer to even complex questions requiring a multi-step explanation, which is beyond the ability of even the larger existing models. The task is also thought as a test-bed for retrieval model which can show the users which source text was used in generating the answer and allow them to confirm the information provided to them.

It should be noted however that the provided answers were written by Reddit users, an information which may be lost if models trained on it are deployed in down-stream applications and presented to users without context. The specific biases this may introduce are discussed in the next section.

### Discussion of Biases

While Reddit hosts a number of thriving communities with high quality discussions, it is also widely known to have corners where sexism, hate, and harassment are significant issues. See for example the  [recent post from Reddit founder u/spez](https://www.reddit.com/r/announcements/comments/gxas21/upcoming_changes_to_our_content_policy_our_board/)  outlining some of the ways he thinks the website's historical policies have been responsible for this problem,  [Adrienne Massanari's 2015 article on GamerGate](https://www.researchgate.net/publication/283848479_Gamergate_and_The_Fappening_How_Reddit's_algorithm_governance_and_culture_support_toxic_technocultures)  and follow-up works, or a  [2019 Wired article on misogyny on Reddit](https://www.wired.com/story/misogyny-reddit-research/).

While there has been some recent work in the NLP community on  *de-biasing*  models (e.g.  [Black is to Criminal as Caucasian is to Police: Detecting and Removing Multiclass Bias in Word Embeddings](https://arxiv.org/abs/1904.04047)  for word embeddings trained specifically on Reddit data), this problem is far from solved, and the likelihood that a trained model might learn the biases present in the data remains a significant concern.

We still note some encouraging signs for all of these communities:  [r/explainlikeimfive](https://www.reddit.com/r/explainlikeimfive/)  and  [r/askscience](https://www.reddit.com/r/askscience/)  have similar structures and purposes, and  [r/askscience](https://www.reddit.com/r/askscience/)  was found in 2015 to show medium supportiveness and very low toxicity when compared to other subreddits (see a  [hackerfall post](https://hackerfall.com/story/study-and-interactive-visualization-of-toxicity-in),  [thecut.com write-up](https://www.thecut.com/2015/03/interactive-chart-of-reddits-toxicity.html)  and supporting  [data](https://chart-studio.plotly.com/~bsbell21/210/toxicity-vs-supportiveness-by-subreddit/#data)). Meanwhile, the  [r/AskHistorians rules](https://www.reddit.com/r/AskHistorians/wiki/rules)  mention that the admins will not tolerate "_racism, sexism, or any other forms of bigotry_". However, further analysis of whether and to what extent these rules reduce toxicity is still needed.

We also note that given the audience of the Reddit website which is more broadly used in the US and Europe, the answers will likely present a Western perspectives, which is particularly important to note when dealing with historical topics.

### Other Known Limitations

The answers provided in the dataset are represent the opinion of Reddit users. While these communities strive to be helpful, they should not be considered to represent a ground truth.

## Additional Information

### Dataset Curators

The dataset was initially created by Angela Fan, Ethan Perez, Yacine Jernite, Jason Weston, Michael Auli, and David Grangier, during work done at Facebook AI Research (FAIR).

### Licensing Information

The licensing status of the dataset hinges on the legal status of the [Pushshift.io](https://files.pushshift.io/reddit/) data which is unclear.

### Citation Information

```
@inproceedings{eli5_lfqa,
  author    = {Angela Fan and
               Yacine Jernite and
               Ethan Perez and
               David Grangier and
               Jason Weston and
               Michael Auli},
  editor    = {Anna Korhonen and
               David R. Traum and
               Llu{\'{\i}}s M{\`{a}}rquez},
  title     = {{ELI5:} Long Form Question Answering},
  booktitle = {Proceedings of the 57th Conference of the Association for Computational
               Linguistics, {ACL} 2019, Florence, Italy, July 28- August 2, 2019,
               Volume 1: Long Papers},
  pages     = {3558--3567},
  publisher = {Association for Computational Linguistics},
  year      = {2019},
  url       = {https://doi.org/10.18653/v1/p19-1346},
  doi       = {10.18653/v1/p19-1346}
}
```
