---
YAML tags:
- copy-paste the tags obtained with the tagging app: https://github.com/huggingface/datasets-tagging
---

# Dataset Card for [Dataset Name]

## Table of Contents
- [Table of Contents](#table-of-contents)
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

- **Homepage:** 
- **Repository:** [Github](https://github.com/jing-qian/A-Benchmark-Dataset-for-Learning-to-Intervene-in-Online-Hate-Speech)
- **Paper:** [A Benchmark Dataset for Learning to Intervene in Online Hate Speech](https://aclanthology.org/D19-1482.pdf)
- **Leaderboard:**
- **Point of Contact:** [Jing Qian](mailto:jing_qian@cs.ucsb.edu)

### Dataset Summary

*This dataset and accompanying dataset card contain examples of offensive language and hate speech.*

The Hate Speech Intervention Benchmark dataset contains two fully-labeled large-scale hate speech intervention datasets with 5K conversations retrieved from Reddit and 12k conversations retrieved from Gab. These datasets provide conversation segments, hate speech labels, as well as intervention responses written by Mechanical Turk Workers.

### Supported Tasks and Leaderboards

The authors propose a novel task of generative hate speech intervention, where the goal is to automatically generate responses to intervene during online conversations that contain hate speech.

### Languages

The dataset is in English (BCP-47 code en). 

## Dataset Structure

### Data Instances

```
id,text,hate_speech_idx,response
{'id': '1. e8q18lf
	2. 	e8q9w5s
	3. 		e8qbobk
	4. 			e8qfn91',
 'text': '1. A subsection of retarded Hungarians? Ohh boy. brace for a livid Bulbasaur coming in here trying to hate a hole in some of her stupider countrymen.
	2. 	Hiii. Just got off work. 444 is mainly the typa guys you imagine writing for US stupid sites, but basically they just try to fit in with the Western European and US big city hipsters.   Rich kids from Budapest who feel they are brave journalistic heroes.  
	3. 		wow i guess soyboys are the same in every country
	4. 			Owen Benjamin's soyboy song goes for every country and that's why it's so amazing.'
 'hate_speech_idx': [1]
 'response': ['I don't see a reason why it's okay to insult others based on their ethnic background.', 'Language people. You can express your ire respectfully and we insist that you do so. Thank you.', 'Stop using mental impairments for insults on posts']}
```

### Data Fields


- `id`: a string with the indexed ids of the post in a conversation segment
- `text`: a string with the indexed text of the posts in a conversation segment
- `hate_speech_idx`: a list of the indices of the hateful posts in this conversation
- `response`: a list of human-written interventions responding to the hateful posts

### Data Splits

From Reddit, the curators collected 5,020 conversations, including 22,324 comments. On average, each conversation consists of 4.45 comments and the length of each comment is 58.0 tokens. 5,257 of the comments are labeled as hate speech and 17,067 are labeled as non-hate speech. A majority of the conversations, 3,847 (76.6%), contain hate speech. Each conversation with hate speech has 2.66 responses on average, for a total of 10,243 intervention responses. The average length of the intervention responses is 17.96 tokens.

From Gab, the curators collected 11,825 conversations, consisting of 33,776 posts. On average, each conversation consists of 2.86 posts and the average length of each post is 35.6 tokens. 14,614 of the posts are labeled as hate speech and 19,162 are
labeled as non-hate speech. Nearly all the conversations, 11,169 (94.5%), contain hate speech. 31,487 intervention responses were originally collected for conversations with hate speech, or 2.82 responses per conversation on average. The average length of the intervention responses is 17.27 tokens.

## Dataset Creation

### Curation Rationale

In order to encourage strategies of countering online hate speech, the curators propose a novel task of generative hate speech intervention and introduce two new datasets for this task. The datasets retain their conversational context and introduce human-written intervention responses. The conversational context and intervention responses are critical in order
to build generative models to automatically mitigate the spread of these types of conversations

### Source Data

#### Initial Data Collection and Normalization

**Reddit**: To retrieve high-quality conversational data that would likely include hate speech, the curators
referenced the list of the [whiniest most low-key toxic subreddits](https://www.vice.com/en us/article/8xxymb/here-are-reddits-whiniest-most-low-key-toxic-subreddits). Skipping the three subreddits
that have been removed, they collected data from ten subreddits: r/DankMemes, r/Imgoingtohellforthis,
r/KotakuInAction, r/MensRights, r/MetaCanada, r/MGTOW, r/PussyPass, r/PussyPassDenied, r/The Donald, and r/TumblrInAction. For each of these subreddits, they retrieved the top 200 hottest submissions using Reddit’s API. To further focus on conversations with hate speech in each submission, they used hate keywords ([ElSherief et al., 2018b](https://ojs.aaai.org/index.php/ICWSM/article/view/15038/14888)) to identify potentially hateful comments and then reconstructed the conversational context of each comment. This context consists of all comments preceding and following a potentially hateful comment. Thus for each potentially hateful comment, the curators rebuilt the conversation where the comment appears. Because a conversation may contain more than one comments
with hate keywords, the curators removed any duplicated conversations.

**Gab**: The curators collected data from all the Gab posts in October 2018. Similar to Reddit, they used hate keywords ([ElSherief et al., 2018b](https://ojs.aaai.org/index.php/ICWSM/article/view/15038/14888)) to identify potentially hateful posts, rebuild the conversation context and clean duplicate conversations.

#### Who are the source language producers?

[More Information Needed]

### Annotations

#### Annotation process

Each conversation is assigned to three different workers  to label and create intervention suggestions. In order not to over-burden the workers, the curators filtered out conversations consisting of more than 20 comments. Each assignment consists of 5 conversations. For Reddit, the curators also present the title and content of the corresponding submission in order to give workers more information about the topic and context. For each conversation, a worker is asked to answer two questions:

• Q1: Which posts or comments in this conversation are hate speech?

• Q2: If there exists hate speech in the conversation, how would you respond to intervene? Write down a response that can probably hold it back (word limit: 140 characters).

If the worker thinks no hate speech exists in the conversation, then the answers to both questions
are “n/a”. To provide context, the definition of hate speech from [Facebook](https://m.facebook.com/communitystandards/hate speech/): “We define hate
speech as a direct attack on people based on what we call protected characteristics race, ethnicity,
national origin, religious affiliation, sexual orientation, caste, sex, gender, gender identity, and se-
rious disease or disability.” is presented to the workers. Also, to prevent workers from using hate
speech in the response or writing responses that are too general, such as “Please do not say that”,
we provide additional instructions and rejected examples.

#### Who are the annotators?

The workers were from English speaking countries including Australia, Canada, Ireland, New Zealand,
the United Kingdom, and the United States. The task required potential workers to have a HIT approval rate higher than 95%. Excluding the rejected answers, the collected data involves 926 different workers. 

### Personal and Sensitive Information

All personally identifiable information such as user names is masked in the
datasets.

## Considerations for Using the Data

### Social Impact of Dataset

The study got approval from their institutional Internal Review Board. Workers were warned about the offensive content before they read the data and they were informed by our instructions to feel free to quit the task at any time if they are uncomfortable with the content. Additionally, all personally identifiable information such as user names is masked in the datasets.

### Discussion of Biases

Despite the large diversity of the collected responses for intervention, the curators find workers tend to have certain strategies for intervention.

**Identify Hate Keywords**: One of the most common strategies is to identify the inappropriate terms in the post and then urge the user to stop using that work. For example, “The C word and language attacking gender is unacceptable. Please refrain from future use.” This strategy is often used when the hatred in the post is mainly conveyed by specific hate keywords.

**Categorize Hate Speech**: The workers commonly classify hate speech into different categories, such as racist, sexist, homophobic, etc. This strategy is often combined with identifying hate keywords or targets of hatred. For example, “The term ””fa**ot”” comprises homophobic hate, and as such is not permitted here.”

**Positive Tone Followed by Transitions**: This is a strategy where the response consists of two parts combined with a transitional word, such as “but” and “even though”. The first part starts with affirmative terms, such as “I understand”, “You have the right to”, and “You are free to express”, showing kindness and understanding, while the second part is to alert the users that their post is inappropriate. For example, “I understand your frustration, but the term you have used is offensive towards the disabled community. Please be more aware of your words.”. The curators suggest this strategy is likely more acceptable for the users and be more likely to end the use hate speech, compared with the response that directly warns.

**Suggest Proper Actions**: Besides warning and discouraging the users from continuing hate speech, workers also suggest the actions that the user should take. This strategy can either be combined with other strategies mentioned above or be used alone. In the latter case, a negative tone can be greatly alleviated. For example, “I think that you should do more research on how resources are allocated in this country.”

### Other Known Limitations

[More Information Needed]

## Additional Information

### Dataset Curators

This dataset was curated by Jing Qian, Elizabeth Belding, and William Yang Wang of University of California, Santa Barbara and Anna Bethke and Yinyin Liu of Intel AI.

### Licensing Information

[More Information Needed]

### Citation Information

```
@inproceedings{qian-etal-2019-benchmark,
    title = "A Benchmark Dataset for Learning to Intervene in Online Hate Speech",
    author = "Qian, Jing  and
      Bethke, Anna  and
      Liu, Yinyin  and
      Belding, Elizabeth  and
      Wang, William Yang",
    booktitle = "Proceedings of the 2019 Conference on Empirical Methods in Natural Language Processing and the 9th International Joint Conference on Natural Language Processing (EMNLP-IJCNLP)",
    month = nov,
    year = "2019",
    address = "Hong Kong, China",
    publisher = "Association for Computational Linguistics",
    url = "https://aclanthology.org/D19-1482",
    doi = "10.18653/v1/D19-1482",
    pages = "4755--4764",
    abstract = "Countering online hate speech is a critical yet challenging task, but one which can be aided by the use of Natural Language Processing (NLP) techniques. Previous research has primarily focused on the development of NLP methods to automatically and effectively detect online hate speech while disregarding further action needed to calm and discourage individuals from using hate speech in the future. In addition, most existing hate speech datasets treat each post as an isolated instance, ignoring the conversational context. In this paper, we propose a novel task of generative hate speech intervention, where the goal is to automatically generate responses to intervene during online conversations that contain hate speech. As a part of this work, we introduce two fully-labeled large-scale hate speech intervention datasets collected from Gab and Reddit. These datasets provide conversation segments, hate speech labels, as well as intervention responses written by Mechanical Turk Workers. In this paper, we also analyze the datasets to understand the common intervention strategies and explore the performance of common automatic response generation methods on these new datasets to provide a benchmark for future research.",
}
```


### Contributions

Thanks to [@mcmillanmajora](https://github.com/mcmillanmajora) for adding this dataset.
