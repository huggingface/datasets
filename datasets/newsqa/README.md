---
annotations_creators:
- crowdsourced
language_creators:
- crowdsourced
languages:
- en
licenses:
- mit
multilinguality:
- monolingual
size_categories:
  combined-json:
  - 10K<n<100K
  split:
  - 100K<n<1M
source_datasets:
- original
task_categories:
- question-answering
task_ids:
- extractive-qa
---

# Dataset Card for NewsQA

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

- **Homepage:** https://www.microsoft.com/en-us/research/project/newsqa-dataset/
- **Repository:** https://github.com/Maluuba/newsqa
- **Paper:** https://www.aclweb.org/anthology/W17-2623/
- **Leaderboard:** [Needs More Information]
- **Point of Contact:** [Needs More Information]

### Dataset Summary

NewsQA is a challenging machine comprehension dataset of over 100,000 human-generated question-answer pairs. 
Crowdworkers supply questions and answers based on a set of over 10,000 news articles from CNN, with answers consisting of spans of text from the corresponding articles.

### Supported Tasks and Leaderboards

[Needs More Information]

### Languages

English

## Dataset Structure

### Data Instances

Configuration: combined-csv
 - `story_id`: An identifier of the story
- `story_text`: text of the story
- `question`: A question about the story.
- `answer_char_ranges`: The raw data collected for character based indices to answers in story_text. E.g. 196:228|196:202,217:228|None. Answers from different crowdsourcers are separated by |, within those, multiple selections from the same crowdsourcer are separated by ,. None means the crowdsourcer thought there was no answer to the question in the story. The start is inclusive and the end is exclusive. The end may point to whitespace after a token.

Configuration: combined-csv
- `storyId`: An identifier of the story.
- `text`: Text of the story
- `type`: Split type - train, validation or test
- `questions`: A list containing the following. 
  - `q`: A question
  - `isAnswerAbsent`: Proportion of crowdsourcers that said there was no answer to the question in the story.
  - `isQuestionBad`: Proportion of crowdsourcers that said the question does not make sense.
  - `consensus`: The consensus answer. Use this field to pick the best continuous answer span from the text. If you want to know about a question having multiple answers in the text then you can use the more detailed "answers" and "validatedAnswers". The object can have start and end positions like in the example above or can be {"badQuestion": true} or {"noAnswer": true}. Note that there is only one consensus answer since it's based on the majority agreement of the crowdsourcers.
  - `s`: start of the answer
  - `e`: end of the answer
  - `badQuestion`: The validator said that the question did not make sense.
  - `noAnswer`: The crowdsourcer said that there was no answer to the question in the text.
  - `answers`: The answers from various crowdsourcers.
    - `sourcerAnswers`: The answer provided from one crowdsourcer.
      - `s`: start
      - `e`: end
      - `noAnswer`: The crowdsourcer said that there was no answer to the question in the text.
  - `validated_answers`: The answers from the validators.
    - `sourcerAnswers`: The answer provided from one crowdsourcer.
      - `s`: start
      - `e`: end
      - `noAnswer`: The crowdsourcer said that there was no answer to the question in the text.
      - `count`: The number of validators that agreed with this answer.

Configuration: split
 - `story_id`: An identifier of the story
- `story_text`: text of the story
- `question`: A question about the story.
- `answer_token_ranges`: Word based indices to answers in story_text. E.g. 196:202,217:228. Multiple selections from the same answer are separated by ,. The start is inclusive and the end is exclusive. The end may point to whitespace after a token.

### Data Fields

[Needs More Information]

### Data Splits

split: Train, Validation and Test.
combined-csv and combined-json: train (whole dataset)

## Dataset Creation

### Curation Rationale

[Needs More Information]

### Source Data

#### Initial Data Collection and Normalization

[Needs More Information]

#### Who are the source language producers?

[Needs More Information]

### Annotations

#### Annotation process

[Needs More Information]

#### Who are the annotators?

[Needs More Information]

### Personal and Sensitive Information

[Needs More Information]

## Considerations for Using the Data

### Social Impact of Dataset

[Needs More Information]

### Discussion of Biases

[Needs More Information]

### Other Known Limitations

[Needs More Information]

## Additional Information

### Dataset Curators

[Needs More Information]

### Licensing Information

NewsQA Code 
Copyright (c) Microsoft Corporation
All rights reserved.
MIT License
Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
THE SOFTWARE IS PROVIDED *AS IS*, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
© 2020 GitHub, Inc.

### Citation Information

@inproceedings{trischler2017newsqa,
  title={NewsQA: A Machine Comprehension Dataset},
  author={Trischler, Adam and Wang, Tong and Yuan, Xingdi and Harris, Justin and Sordoni, Alessandro and Bachman, Philip and Suleman, Kaheer},
  booktitle={Proceedings of the 2nd Workshop on Representation Learning for NLP},
  pages={191--200},
  year={2017}
