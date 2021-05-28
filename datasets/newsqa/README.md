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
  combined-csv:
  - 100K<n<1M
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
paperswithcode_id: newsqa
---

# Dataset Card for NewsQA

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

```
{'questions': {'answers': [{'sourcerAnswers': [{'e': [297], 'noAnswer': [False], 's': [294]}, {'e': [0], 'noAnswer': [True], 's': [0]}, {'e': [0], 'noAnswer': [True], 's': [0]}]}, {'sourcerAnswers': [{'e': [271], 'noAnswer': [False], 's': [261]}, {'e': [271], 'noAnswer': [False], 's': [258]}, {'e': [271], 'noAnswer': [False], 's': [261]}]}, {'sourcerAnswers': [{'e': [33], 'noAnswer': [False], 's': [26]}, {'e': [0], 'noAnswer': [True], 's': [0]}, {'e': [640], 'noAnswer': [False], 's': [624]}]}, {'sourcerAnswers': [{'e': [218], 'noAnswer': [False], 's': [195]}, {'e': [218], 'noAnswer': [False], 's': [195]}]}, {'sourcerAnswers': [{'e': [0], 'noAnswer': [True], 's': [0]}, {'e': [218, 271], 'noAnswer': [False, False], 's': [195, 232]}, {'e': [0], 'noAnswer': [True], 's': [0]}]}, {'sourcerAnswers': [{'e': [192], 'noAnswer': [False], 's': [129]}, {'e': [151], 'noAnswer': [False], 's': [129]}, {'e': [151], 'noAnswer': [False], 's': [133]}]}, {'sourcerAnswers': [{'e': [218], 'noAnswer': [False], 's': [195]}, {'e': [218], 'noAnswer': [False], 's': [195]}]}, {'sourcerAnswers': [{'e': [297], 'noAnswer': [False], 's': [294]}, {'e': [297], 'noAnswer': [False], 's': [294]}]}, {'sourcerAnswers': [{'e': [297], 'noAnswer': [False], 's': [294]}, {'e': [297], 'noAnswer': [False], 's': [294]}]}], 'consensus': [{'badQuestion': False, 'e': 297, 'noAnswer': False, 's': 294}, {'badQuestion': False, 'e': 271, 'noAnswer': False, 's': 261}, {'badQuestion': False, 'e': 640, 'noAnswer': False, 's': 624}, {'badQuestion': False, 'e': 218, 'noAnswer': False, 's': 195}, {'badQuestion': False, 'e': 218, 'noAnswer': False, 's': 195}, {'badQuestion': False, 'e': 151, 'noAnswer': False, 's': 129}, {'badQuestion': False, 'e': 218, 'noAnswer': False, 's': 195}, {'badQuestion': False, 'e': 297, 'noAnswer': False, 's': 294}, {'badQuestion': False, 'e': 297, 'noAnswer': False, 's': 294}], 'isAnswerAbsent': [0, 0, 0, 0, 0, 0, 0, 0, 0], 'isQuestionBad': [0, 0, 0, 0, 0, 0, 0, 0, 0], 'q': ['What was the amount of children murdered?', 'When was Pandher sentenced to death?', 'The court aquitted Moninder Singh Pandher of what crime?', 'who was acquitted', 'who was sentenced', 'What was Moninder Singh Pandher acquitted for?', 'Who was sentenced to death in February?', 'how many people died', 'How many children and young women were murdered?'], 'validated_answers': [{'sourcerAnswers': [{'count': [0], 'e': [297], 'noAnswer': [False], 's': [294]}, {'count': [0], 'e': [0], 'noAnswer': [True], 's': [0]}, {'count': [0], 'e': [0], 'noAnswer': [True], 's': [0]}]}, {'sourcerAnswers': [{'count': [0], 'e': [271], 'noAnswer': [False], 's': [261]}, {'count': [0], 'e': [271], 'noAnswer': [False], 's': [258]}, {'count': [0], 'e': [271], 'noAnswer': [False], 's': [261]}]}, {'sourcerAnswers': [{'count': [0], 'e': [33], 'noAnswer': [False], 's': [26]}, {'count': [0], 'e': [0], 'noAnswer': [True], 's': [0]}, {'count': [0], 'e': [640], 'noAnswer': [False], 's': [624]}]}, {'sourcerAnswers': [{'count': [0], 'e': [218], 'noAnswer': [False], 's': [195]}, {'count': [0], 'e': [218], 'noAnswer': [False], 's': [195]}]}, {'sourcerAnswers': [{'count': [0], 'e': [0], 'noAnswer': [True], 's': [0]}, {'count': [0, 0], 'e': [218, 271], 'noAnswer': [False, False], 's': [195, 232]}, {'count': [0], 'e': [0], 'noAnswer': [True], 's': [0]}]}, {'sourcerAnswers': [{'count': [0], 'e': [192], 'noAnswer': [False], 's': [129]}, {'count': [0], 'e': [151], 'noAnswer': [False], 's': [129]}, {'count': [0], 'e': [151], 'noAnswer': [False], 's': [133]}]}, {'sourcerAnswers': [{'count': [0], 'e': [218], 'noAnswer': [False], 's': [195]}, {'count': [0], 'e': [218], 'noAnswer': [False], 's': [195]}]}, {'sourcerAnswers': [{'count': [0], 'e': [297], 'noAnswer': [False], 's': [294]}, {'count': [0], 'e': [297], 'noAnswer': [False], 's': [294]}]}, {'sourcerAnswers': [{'count': [0], 'e': [297], 'noAnswer': [False], 's': [294]}, {'count': [0], 'e': [297], 'noAnswer': [False], 's': [294]}]}]}, 'storyId': './cnn/stories/42d01e187213e86f5fe617fe32e716ff7fa3afc4.story', 'text': 'NEW DELHI, India (CNN) -- A high court in northern India on Friday acquitted a wealthy businessman facing the death sentence for the killing of a teen in a case dubbed "the house of horrors."\n\n\n\nMoninder Singh Pandher was sentenced to death by a lower court in February.\n\n\n\nThe teen was one of 19 victims -- children and young women -- in one of the most gruesome serial killings in India in recent years.\n\n\n\nThe Allahabad high court has acquitted Moninder Singh Pandher, his lawyer Sikandar B. Kochar told CNN.\n\n\n\nPandher and his domestic employee Surinder Koli were sentenced to death in February by a lower court for the rape and murder of the 14-year-old.\n\n\n\nThe high court upheld Koli\'s death sentence, Kochar said.\n\n\n\nThe two were arrested two years ago after body parts packed in plastic bags were found near their home in Noida, a New Delhi suburb. Their home was later dubbed a "house of horrors" by the Indian media.\n\n\n\nPandher was not named a main suspect by investigators initially, but was summoned as co-accused during the trial, Kochar said.\n\n\n\nKochar said his client was in Australia when the teen was raped and killed.\n\n\n\nPandher faces trial in the remaining 18 killings and could remain in custody, the attorney said.', 'type': 'train'}
```

### Data Fields


Configuration: combined-csv
 - 'story_id': An identifier of the story
- 'story_text': text of the story
- 'question': A question about the story.
- 'answer_char_ranges': The raw data collected for character based indices to answers in story_text. E.g. 196:228|196:202,217:228|None. Answers from different crowdsourcers are separated by |, within those, multiple selections from the same crowdsourcer are separated by ,. None means the crowdsourcer thought there was no answer to the question in the story. The start is inclusive and the end is exclusive. The end may point to whitespace after a token.

Configuration: combined-csv
- 'storyId': An identifier of the story.
- 'text': Text of the story
- 'type': Split type - train, validation or test
- 'questions': A list containing the following. 
  - 'q': A question
  - 'isAnswerAbsent': Proportion of crowdsourcers that said there was no answer to the question in the story.
  - 'isQuestionBad': Proportion of crowdsourcers that said the question does not make sense.
  - 'consensus': The consensus answer. Use this field to pick the best continuous answer span from the text. If you want to know about a question having multiple answers in the text then you can use the more detailed "answers" and "validatedAnswers". The object can have start and end positions like in the example above or can be {"badQuestion": true} or {"noAnswer": true}. Note that there is only one consensus answer since it's based on the majority agreement of the crowdsourcers.
  - 's': start of the answer
  - 'e': end of the answer
  - 'badQuestion': The validator said that the question did not make sense.
  - 'noAnswer': The crowdsourcer said that there was no answer to the question in the text.
  - 'answers': The answers from various crowdsourcers.
    - 'sourcerAnswers': The answer provided from one crowdsourcer.
      - 's': start
      - 'e': end
      - 'noAnswer': The crowdsourcer said that there was no answer to the question in the text.
  - 'validated_answers': The answers from the validators.
    - 'sourcerAnswers': The answer provided from one crowdsourcer.
      - 's': start
      - 'e': end
      - 'noAnswer': The crowdsourcer said that there was no answer to the question in the text.
      - 'count': The number of validators that agreed with this answer.

Configuration: split
 - 'story_id': An identifier of the story
- 'story_text': text of the story
- 'question': A question about the story.
- 'answer_token_ranges': Word based indices to answers in story_text. E.g. 196:202,217:228. Multiple selections from the same answer are separated by ,. The start is inclusive and the end is exclusive. The end may point to whitespace after a token.

### Data Splits

split: Train, Validation and Test.
combined-csv and combined-json: train (whole dataset)

## Dataset Creation

### Curation Rationale

[More Information Needed]

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

### Contributions

Thanks to [@rsanjaykamath](https://github.com/rsanjaykamath) for adding this dataset.