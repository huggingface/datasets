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
size_categories:
- 100K<n<1M
source_datasets:
- extended|drop
- extended|hotpot_qa
- extended|natural_questions
- extended|race
- extended|search_qa
- extended|squad
- extended|trivia_qa
task_categories:
- question-answering
task_ids:
- extractive-qa
---

# Dataset Card Creation Guide

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

- **Homepage:** [MRQA 2019 Shared Task](https://mrqa.github.io/2019/shared.html)
- **Repository:** [MRQA 2019 Github repository](https://github.com/mrqa/MRQA-Shared-Task-2019)
- **Paper:** [MRQA 2019 Shared Task: Evaluating Generalization in Reading Comprehension
](https://arxiv.org/abs/1910.09753)
- **Leaderboard:** [Shared task](https://mrqa.github.io/2019/shared.html)
- **Point of Contact:** [mrforqa@gmail.com](mrforqa@gmail.com)

### Dataset Summary

The MRQA 2019 Shared Task focuses on generalization in question answering. An effective question answering system should do more than merely interpolate from the training set to answer test examples drawn from the same distribution: it should also be able to extrapolate to out-of-distribution examples — a significantly harder challenge.

The dataset is a collection of 18 existing QA dataset (carefully selected subset of them) and converted to the same format (SQuAD format). Among these 18 datasets, six datasets were made available for training, six datasets were made available for development, and the final six for testing. The dataset is released as part of the MRQA 2019 Shared Task.

### Supported Tasks and Leaderboards

From the official repository:

*The format of the task is extractive question answering. Given a question and context passage, systems must find the word or phrase in the document that best answers the question. While this format is somewhat restrictive, it allows us to leverage many existing datasets, and its simplicity helps us focus on out-of-domain generalization, instead of other important but orthogonal challenges.*

*We have adapted several existing datasets from their original formats and settings to conform to our unified extractive setting. Most notably:*
- *We provide only a single, length-limited context.*
- *There are no unanswerable or non-span answer questions.*
- *All questions have at least one accepted answer that is found exactly in the context.*

*A span is judged to be an exact match if it matches the answer string after performing normalization consistent with the SQuAD dataset. Specifically:*
- *The text is uncased.*
- *All punctuation is stripped.*
- *All articles `{a, an, the}` are removed.*
- *All consecutive whitespace markers are compressed to just a single normal space `' '`.*

Answers are evaluated using exact match and token-level F1 metrics. One can refer to the [mrqa_official_eval.py](https://github.com/mrqa/MRQA-Shared-Task-2019/blob/master/mrqa_official_eval.py) for evaluation.

### Languages

The text in the dataset is in English. The associated BCP-47 code is `en`.

## Dataset Structure

### Data Instances

An examples looks like this:
```
{
  'qid': 'f43c83e38d1e424ea00f8ad3c77ec999',
  'subset': 'SQuAD'

  'context': 'CBS broadcast Super Bowl 50 in the U.S., and charged an average of $5 million for a 30-second commercial during the game. The Super Bowl 50 halftime show was headlined by the British rock group Coldplay with special guest performers Beyoncé and Bruno Mars, who headlined the Super Bowl XLVII and Super Bowl XLVIII halftime shows, respectively. It was the third-most watched U.S. broadcast ever.',
  'context_tokens': {
    'offsets': [0, 4, 14, 20, 25, 28, 31, 35, 39, 41, 45, 53, 56, 64, 67, 68, 70, 78, 82, 84, 94, 105, 112, 116, 120, 122, 126, 132, 137, 140, 149, 154, 158, 168, 171, 175, 183, 188, 194, 203, 208, 216, 222, 233, 241, 245, 251, 255, 257, 261, 271, 275, 281, 286, 292, 296, 302, 307, 314, 323, 328, 330, 342, 344, 347, 351, 355, 360, 361, 366, 374, 379, 389, 393],
    'tokens': ['CBS', 'broadcast', 'Super', 'Bowl', '50', 'in', 'the', 'U.S.', ',', 'and', 'charged', 'an', 'average', 'of', '$', '5', 'million', 'for', 'a', '30-second', 'commercial', 'during', 'the', 'game', '.', 'The', 'Super', 'Bowl', '50', 'halftime', 'show', 'was', 'headlined', 'by', 'the', 'British', 'rock', 'group', 'Coldplay', 'with', 'special', 'guest', 'performers', 'Beyoncé', 'and', 'Bruno', 'Mars', ',', 'who', 'headlined', 'the', 'Super', 'Bowl', 'XLVII', 'and', 'Super', 'Bowl', 'XLVIII', 'halftime', 'shows', ',', 'respectively', '.', 'It', 'was', 'the', 'third', '-', 'most', 'watched', 'U.S.', 'broadcast', 'ever', '.']
  },

  'question': "Who was the main performer at this year's halftime show?",
  'question_tokens': {
      'offsets': [0, 4, 8, 12, 17, 27, 30, 35, 39, 42, 51, 55],
      'tokens': ['Who', 'was', 'the', 'main', 'performer', 'at', 'this', 'year', "'s", 'halftime', 'show', '?']
  },

  'detected_answers': {
    'char_spans': [
      {
        'end': [201],
        'start': [194]
      }, {
        'end': [201],
        'start': [194]
      }, {
        'end': [201],
        'start': [194]
      }
    ],
    'text': ['Coldplay', 'Coldplay', 'Coldplay'],
    'token_spans': [
      {
        'end': [38],
        'start': [38]
      }, {
        'end': [38],
        'start': [38]
        }, {
        'end': [38],
        'start': [38]
      }
    ]
  },

  'answers': ['Coldplay', 'Coldplay', 'Coldplay'],
}
```

### Data Fields

- `subset`: which of the dataset does this examples come from?
- `context`: This is the raw text of the supporting passage. Three special token types have been inserted: `[TLE]` precedes document titles, `[DOC]` denotes document breaks, and `[PAR]` denotes paragraph breaks. The maximum length of the context is 800 tokens.
- `context_tokens`: A tokenized version of the supporting passage, using spaCy. Each token is a tuple of the token string and token character offset. The maximum number of tokens is 800.
  - `tokens`: list of tokens.
  - `offets`: list of offsets.
- `qas`: A list of questions for the given context.
- `qid`: A unique identifier for the question. The `qid` is unique across all datasets.
- `question`: The raw text of the question.
- `question_tokens`: A tokenized version of the question. The tokenizer and token format is the same as for the context.
  - `tokens`: list of tokens.
  - `offets`: list of offsets.
- `detected_answers`: A list of answer spans for the given question that index into the context. For some datasets these spans have been automatically detected using searching heuristics. The same answer may appear multiple times in the text --- each of these occurrences is recorded. For example, if `42` is the answer, the context `"The answer is 42. 42 is the answer."`, has two occurrences marked.
  - `text`: The raw text of the detected answer.
  - `char_spans`: Inclusive (start, end) character spans (indexing into the raw context).
    - `start`: start (single element)
    - `end`: end (single element)
  - `token_spans`: Inclusive (start, end) token spans (indexing into the tokenized context).
    - `start`: start (single element)
    - `end`: end (single element)



### Data Splits

**Training data**
| Dataset | Number of Examples |
| :-----: | :------: |
| [SQuAD](https://arxiv.org/abs/1606.05250)   | 86,588 |
| [NewsQA](https://arxiv.org/abs/1611.09830)  | 74,160 |
| [TriviaQA](https://arxiv.org/abs/1705.03551)| 61,688 |
| [SearchQA](https://arxiv.org/abs/1704.05179)| 117,384 |
| [HotpotQA](https://arxiv.org/abs/1809.09600)| 72,928 |
| [NaturalQuestions](https://ai.google/research/pubs/pub47761)| 104,071 |

**Development data**

This in-domain data may be used for helping develop models.

| Dataset | Examples |
| :-----: | :------: |
| [SQuAD](https://arxiv.org/abs/1606.05250) | 10,507 |
| [NewsQA](https://arxiv.org/abs/1611.09830) | 4,212 |
| [TriviaQA](https://arxiv.org/abs/1705.03551)| 7,785|
| [SearchQA](https://arxiv.org/abs/1704.05179)| 16,980 |
| [HotpotQA](https://arxiv.org/abs/1809.09600)| 5,904 |
| [NaturalQuestions](https://ai.google/research/pubs/pub47761)| 12,836 |

**Test data**

The final testing data only contain out-of-domain data.

| Dataset | Examples |
| :-----: | :------: |
| [BioASQ](http://bioasq.org/) | 1,504 |
| [DROP](https://arxiv.org/abs/1903.00161) | 1,503 |
| [DuoRC](https://arxiv.org/abs/1804.07927)| 1,501 |
| [RACE](https://arxiv.org/abs/1704.04683) | 674 |
| [RelationExtraction](https://arxiv.org/abs/1706.04115) | 2,948|
| [TextbookQA](http://ai2-website.s3.amazonaws.com/publications/CVPR17_TQA.pdf)| 1,503 |



From the official repository:

***Note:** As previously mentioned, the out-of-domain dataset have been modified from their original settings to fit the unified MRQA Shared Task paradigm. At a high level, the following two major modifications have been made:*

*1. All QA-context pairs are extractive. That is, the answer is selected from the context and not via, e.g., multiple-choice.*
*2. All contexts are capped at a maximum of `800` tokens. As a result, for longer contexts like Wikipedia articles, we only consider examples where the answer appears in the first `800` tokens.*

*As a result, some splits are harder than the original datasets (e.g., removal of multiple-choice in RACE), while some are easier (e.g., restricted context length in NaturalQuestions --- we use the short answer selection). Thus one should expect different performance ranges if comparing to previous work on these datasets.*

## Dataset Creation

### Curation Rationale

From the official repository:

*Both train and test datasets have the same format described above, but may differ in some of the following ways:*
- *Passage distribution: Test examples may involve passages from different sources (e.g., science, news, novels, medical abstracts, etc) with pronounced syntactic and lexical differences.*
- *Question distribution: Test examples may emphasize different styles of questions (e.g., entity-centric, relational, other tasks reformulated as QA, etc) which may come from different sources (e.g., crowdworkers, domain experts, exam writers, etc.)*
- *Joint distribution: Test examples may vary according to the relationship of the question to the passage (e.g., collected independent vs. dependent of evidence, multi-hop, etc)*

### Source Data

[More Information Needed]

#### Initial Data Collection and Normalization

[More Information Needed]

#### Who are the source language producers?

[More Information Needed]

### Annotations

[More Information Needed]

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

Unknown

### Citation Information

```
@inproceedings{fisch2019mrqa,
    title={{MRQA} 2019 Shared Task: Evaluating Generalization in Reading Comprehension},
    author={Adam Fisch and Alon Talmor and Robin Jia and Minjoon Seo and Eunsol Choi and Danqi Chen},
    booktitle={Proceedings of 2nd Machine Reading for Reading Comprehension (MRQA) Workshop at EMNLP},
    year={2019},
}
```
