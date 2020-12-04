---
annotations_creators:
- crowdsourced
language_creators:
- crowdsourced
- found
languages:
- en
licenses:
- mit
multilinguality:
- monolingual
size_categories:
- 10K<n<100K
source_datasets:
- extended|wikipedia
task_categories:
- question-answering
- sequence-modeling
task_ids:
- dialogue-modeling
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

- **Homepage:** [Add homepage URL here if available (unless it's a GitHub repository)]()
- **Repository:** [If the dataset is hosted on github or has a github homepage, add URL here]()
- **Paper:** [If the dataset was introduced by a paper or there was a paper written describing the dataset, add URL here (landing page for Arxiv paper preferred)]()
- **Leaderboard:** [If the dataset supports an active leaderboard, add link here]()
- **Point of Contact:** [If known, name and email of at least one person the reader can contact for questions about the dataset.]()

### Dataset Summary

Question Answering in Context is a dataset for modeling, understanding, and participating in information seeking dialog. Data instances consist of an interactive dialog between two crowd workers: (1) a student who poses a sequence of freeform questions to learn as much as possible about a hidden Wikipedia text, and (2) a teacher who answers the questions by providing short excerpts (spans) from the text. QuAC introduces challenges not found in existing machine comprehension datasets: its questions are often more open-ended, unanswerable, or only meaningful within the dialog context.

### Supported Tasks and Leaderboards

The core problem involves predicting a text span to answer a question about a Wikipedia section (extractive question answering). Since QuAC questions include a dialog component, each instance includes a “dialog history” of questions and answers asked in the dialog prior to the given question, along with some additional metadata.

Authors provided [an official evaluation script](https://s3.amazonaws.com/my89public/quac/scorer.py) for evaluation.

### Languages

The text in the dataset is in English. The associated BCP-47 code is `en`.

## Dataset Structure

### Data Instances

A validation examples looks like this (one entry per dialogue):

```
{
  'dialogue_id': 'C_6abd2040a75d47168a9e4cca9ca3fed5_0',

  'wikipedia_page_title': 'Satchel Paige',

  'background': 'Leroy Robert "Satchel" Paige (July 7, 1906 - June 8, 1982) was an American Negro league baseball and Major League Baseball (MLB) pitcher who became a legend in his own lifetime by being known as perhaps the best pitcher in baseball history, by his longevity in the game, and by attracting record crowds wherever he pitched. Paige was a right-handed pitcher, and at age 42 in 1948, he was the oldest major league rookie while playing for the Cleveland Indians. He played with the St. Louis Browns until age 47, and represented them in the All-Star Game in 1952 and 1953.',

  'section_title': 'Chattanooga and Birmingham: 1926-29',

  'context': 'A former friend from the Mobile slums, Alex Herman, was the player/manager for the Chattanooga White Sox of the minor Negro Southern League. In 1926 he discovered Paige and offered to pay him $250 per month, of which Paige would collect $50 with the rest going to his mother. He also agreed to pay Lula Paige a $200 advance, and she agreed to the contract. The local newspapers--the Chattanooga News and Chattanooga Times--recognized from the beginning that Paige was special. In April 1926, shortly after his arrival, he recorded nine strikeouts over six innings against the Atlanta Black Crackers. Part way through the 1927 season, Paige\'s contract was sold to the Birmingham Black Barons of the major Negro National League (NNL). According to Paige\'s first memoir, his contract was for $450 per month, but in his second he said it was for $275. Pitching for the Black Barons, Paige threw hard but was wild and awkward. In his first big game in late June 1927, against the St. Louis Stars, Paige incited a brawl when his fastball hit the hand of St. Louis catcher Mitchell Murray. Murray then charged the mound and Paige raced for the dugout, but Murray flung his bat and struck Paige above the hip. The police were summoned, and the headline of the Birmingham Reporter proclaimed a "Near Riot." Paige improved and matured as a pitcher with help from his teammates, Sam Streeter and Harry Salmon, and his manager, Bill Gatewood. He finished the 1927 season 7-1 with 69 strikeouts and 26 walks in 89 1/3 innings. Over the next two seasons, Paige went 12-5 and 10-9 while recording 176 strikeouts in 1929. (Several sources credit his 1929 strikeout total as the all-time single-season record for the Negro leagues, though there is variation among the sources about the exact number of strikeouts.) On April 29 of that season he recorded 17 strikeouts in a game against the Cuban Stars, which exceeded what was then the major league record of 16 held by Noodles Hahn and Rube Waddell. Six days later he struck out 18 Nashville Elite Giants, a number that was tied in the white majors by Bob Feller in 1938. Due to his increased earning potential, Barons owner R. T. Jackson would "rent" Paige out to other ball clubs for a game or two to draw a decent crowd, with both Jackson and Paige taking a cut. CANNOTANSWER',

  'turn_ids': ['C_6abd2040a75d47168a9e4cca9ca3fed5_0_q#0', 'C_6abd2040a75d47168a9e4cca9ca3fed5_0_q#1', 'C_6abd2040a75d47168a9e4cca9ca3fed5_0_q#2', 'C_6abd2040a75d47168a9e4cca9ca3fed5_0_q#3', 'C_6abd2040a75d47168a9e4cca9ca3fed5_0_q#4', 'C_6abd2040a75d47168a9e4cca9ca3fed5_0_q#5', 'C_6abd2040a75d47168a9e4cca9ca3fed5_0_q#6', 'C_6abd2040a75d47168a9e4cca9ca3fed5_0_q#7'],

  'questions': ['what did he do in Chattanooga', 'how did he discover him', 'what position did he play', 'how did they help him', 'when did he go to Birmingham', 'how did he feel about this', 'how did he do with this team', 'What made him leave the team'],

  'followups': [0, 2, 0, 1, 0, 1, 0, 1],

  'yesnos': [2, 2, 2, 2, 2, 2, 2, 2]

  'answers': {
    'answer_starts': [
      [480, 39, 0, 67, 39],
      [2300, 2300, 2300],
      [848, 1023, 848, 848, 1298],
      [2300, 2300, 2300, 2300, 2300],
      [600, 600, 600, 634, 600],
      [2300, 2300, 2300],
      [939, 1431, 848, 848, 1514],
      [2106, 2106, 2165]
    ],
    'texts': [
      ['April 1926, shortly after his arrival, he recorded nine strikeouts over six innings against the Atlanta Black Crackers.', 'Alex Herman, was the player/manager for the Chattanooga White Sox of the minor Negro Southern League. In 1926 he discovered Paige', 'A former friend from the Mobile slums, Alex Herman, was the player/manager for the Chattanooga White Sox of the minor Negro Southern League.', 'manager for the Chattanooga White Sox of the minor Negro Southern League. In 1926 he discovered Paige and offered to pay him $250 per month,', 'Alex Herman, was the player/manager for the Chattanooga White Sox of the minor Negro Southern League. In 1926 he discovered Paige and offered to pay him $250 per month,'],
      ['CANNOTANSWER', 'CANNOTANSWER', 'CANNOTANSWER'],
      ['Pitching for the Black Barons,', 'fastball', 'Pitching for', 'Pitching', 'Paige improved and matured as a pitcher with help from his teammates,'], ['CANNOTANSWER', 'CANNOTANSWER', 'CANNOTANSWER', 'CANNOTANSWER', 'CANNOTANSWER'],
      ["Part way through the 1927 season, Paige's contract was sold to the Birmingham Black Barons", "Part way through the 1927 season, Paige's contract was sold to the Birmingham Black Barons", "Part way through the 1927 season, Paige's contract was sold to the Birmingham Black Barons", "Paige's contract was sold to the Birmingham Black Barons of the major Negro National League (NNL", "Part way through the 1927 season, Paige's contract was sold to the Birmingham Black Barons"], ['CANNOTANSWER', 'CANNOTANSWER', 'CANNOTANSWER'],
      ['game in late June 1927, against the St. Louis Stars, Paige incited a brawl when his fastball hit the hand of St. Louis catcher Mitchell Murray.', 'He finished the 1927 season 7-1 with 69 strikeouts and 26 walks in 89 1/3 innings.', 'Pitching for the Black Barons, Paige threw hard but was wild and awkward.', 'Pitching for the Black Barons, Paige threw hard but was wild and awkward.', 'Over the next two seasons, Paige went 12-5 and 10-9 while recording 176 strikeouts in 1929. ('],
      ['Due to his increased earning potential, Barons owner R. T. Jackson would "rent" Paige out to other ball clubs', 'Due to his increased earning potential, Barons owner R. T. Jackson would "rent" Paige out to other ball clubs for a game or two to draw a decent crowd,', 'Jackson would "rent" Paige out to other ball clubs for a game or two to draw a decent crowd, with both Jackson and Paige taking a cut.']
    ]
  },

  'orig_answers': {
    'answer_starts': [39, 2300, 1298, 2300, 600, 2300, 1514, 2165],
    'texts': ['Alex Herman, was the player/manager for the Chattanooga White Sox of the minor Negro Southern League. In 1926 he discovered Paige and offered to pay him $250 per month,', 'CANNOTANSWER', 'Paige improved and matured as a pitcher with help from his teammates,', 'CANNOTANSWER', "Part way through the 1927 season, Paige's contract was sold to the Birmingham Black Barons", 'CANNOTANSWER', 'Over the next two seasons, Paige went 12-5 and 10-9 while recording 176 strikeouts in 1929. (', 'Jackson would "rent" Paige out to other ball clubs for a game or two to draw a decent crowd, with both Jackson and Paige taking a cut.']
  },
}
```

### Data Fields

- `dialogue_id`: ID of the dialogue.
- `wikipedia_page_title`: title of the Wikipedia page.
- `background`: first paragraph of the main Wikipedia article.
- `section_tile`: Wikipedia section title.
- `context`: Wikipedia section text.
- `turn_ids`: list of identification of dialogue turns. One list of ids per dialogue.
- `questions`: list of questions in the dialogue. One list of questions per dialogue.
- `followups`: list of followup actions in the dialogue. One list of followups per dialogue. `y`: follow, `m`: maybe follow yp, `n`: don't follow up.
- `yesnos`: list of yes/no in the dialogue. One list of yes/nos per dialogue. `y`: yes, `n`: no, `x`: neither.
- `answers`: dictionary of answers to the questions (validation step of data collection)
  - `answer_starts`: list of list of starting offsets. For training, list of single element lists (one answer per question).
  - `texts`: list of list of span texts answering questions. For training, list of single element lists (one answer per question).
- `orig_answers`: dictionary of original answers (the ones provided by the teacher in the dialogue)
  - `answer_starts`: list of starting offsets
  - `texts`: list of span texts answering questions.

### Data Splits

QuAC contains 98,407 QA pairs from 13,594 dialogs. The dialogs were conducted on 8,854 unique sections from 3,611 unique Wikipedia articles, and every dialog contains between four and twelve questions.

The dataset comes with a train/dev split such that there is no overlap in sections across splits. Furthermore, the dev and test sets only include one
dialog per section, in contrast to the training set which can have multiple dialogs per section. Dev and test instances come with five reference answers instead of just one as in the training set; we obtain the extra references to improve the reliability of our evaluations, as questions can have multiple valid answer spans. The test set is not publicly available; instead, researchers must submit their models to the [leaderboard](http://quac.ai), which will run the model on our hidden test set.

The training set contains 83,568 questions (11,567 dialogues), while 7,354 (1,000) and 7,353 (1,002) separate questions are reserved for the dev and test set respectively.

## Dataset Creation

### Curation Rationale

Please refer to the [Datasheet](https://quac.ai/datasheet.pdf) from the authors of the dataset.

### Source Data

Please refer to the [Datasheet](https://quac.ai/datasheet.pdf) from the authors of the dataset.

#### Initial Data Collection and Normalization

Please refer to the [Datasheet](https://quac.ai/datasheet.pdf) from the authors of the dataset.

#### Who are the source language producers?

Please refer to the [Datasheet](https://quac.ai/datasheet.pdf) from the authors of the dataset.

### Annotations

Please refer to the [Datasheet](https://quac.ai/datasheet.pdf) from the authors of the dataset.

#### Annotation process

Please refer to the [Datasheet](https://quac.ai/datasheet.pdf) from the authors of the dataset.

#### Who are the annotators?

Please refer to the [Datasheet](https://quac.ai/datasheet.pdf) from the authors of the dataset.
### Personal and Sensitive Information

Please refer to the [Datasheet](https://quac.ai/datasheet.pdf) from the authors of the dataset.

## Considerations for Using the Data

### Social Impact of Dataset

Please refer to the [Datasheet](https://quac.ai/datasheet.pdf) from the authors of the dataset.

### Discussion of Biases

Please refer to the [Datasheet](https://quac.ai/datasheet.pdf) from the authors of the dataset.

### Other Known Limitations

Please refer to the [Datasheet](https://quac.ai/datasheet.pdf) from the authors of the dataset.

## Additional Information

### Dataset Curators

Please refer to the [Datasheet](https://quac.ai/datasheet.pdf) from the authors of the dataset.

### Licensing Information

The dataset is distributed under the MIT license.

### Citation Information

Provide the [BibTex](http://www.bibtex.org/)-formatted reference for the dataset. For example:
```
@inproceedings{choi-etal-2018-quac,
    title = "{Q}u{AC}: Question Answering in Context",
    author = "Choi, Eunsol  and
      He, He  and
      Iyyer, Mohit  and
      Yatskar, Mark  and
      Yih, Wen-tau  and
      Choi, Yejin  and
      Liang, Percy  and
      Zettlemoyer, Luke",
    booktitle = "Proceedings of the 2018 Conference on Empirical Methods in Natural Language Processing",
    month = oct # "-" # nov,
    year = "2018",
    address = "Brussels, Belgium",
    publisher = "Association for Computational Linguistics",
    url = "https://www.aclweb.org/anthology/D18-1241",
    doi = "10.18653/v1/D18-1241",
    pages = "2174--2184",
    abstract = "We present QuAC, a dataset for Question Answering in Context that contains 14K information-seeking QA dialogs (100K questions in total). The dialogs involve two crowd workers: (1) a student who poses a sequence of freeform questions to learn as much as possible about a hidden Wikipedia text, and (2) a teacher who answers the questions by providing short excerpts from the text. QuAC introduces challenges not found in existing machine comprehension datasets: its questions are often more open-ended, unanswerable, or only meaningful within the dialog context, as we show in a detailed qualitative evaluation. We also report results for a number of reference models, including a recently state-of-the-art reading comprehension architecture extended to model dialog context. Our best model underperforms humans by 20 F1, suggesting that there is significant room for future work on this data. Dataset, baseline, and leaderboard available at \url{http://quac.ai}.",
}
```
