---
annotations_creators:
- crowdsourced
language_creators:
- found
languages:
- en
licenses:
- ms-pl
multilinguality:
- monolingual
size_categories:
- 10K<n<100K
source_datasets:
- original
task_categories:
- question-answering
task_ids:
- extractive-qa
paperswithcode_id: null
pretty_name: Microsoft Research Sequential Question Answering
---

# Dataset Card for Microsoft Research Sequential Question Answering

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

- **Homepage:** [Microsoft Research Sequential Question Answering (SQA) Dataset](https://msropendata.com/datasets/b25190ed-0f59-47b1-9211-5962858142c2)
- **Repository:**
- **Paper:** [https://www.microsoft.com/en-us/research/wp-content/uploads/2017/05/acl17-dynsp.pdf](https://www.microsoft.com/en-us/research/wp-content/uploads/2017/05/acl17-dynsp.pdf)
- **Leaderboard:**
- **Point of Contact:**
  - Scott Wen-tau Yih        scottyih@microsoft.com
  - Mohit Iyyer              m.iyyer@gmail.com
  - Ming-Wei Chang           minchang@microsoft.com

### Dataset Summary

Recent work in semantic parsing for question answering has focused on long and complicated questions, many of which would seem unnatural if asked in a normal conversation between two humans. In an effort to explore a conversational QA setting, we present a more realistic task: answering sequences of simple but inter-related questions.

We created SQA by asking crowdsourced workers to decompose 2,022 questions from WikiTableQuestions (WTQ)*, which contains highly-compositional questions about tables from Wikipedia. We had three workers decompose each WTQ question, resulting in a dataset of 6,066 sequences that contain 17,553 questions in total. Each question is also associated with answers in the form of cell locations in the tables.

- Panupong Pasupat, Percy Liang. "Compositional Semantic Parsing on Semi-Structured Tables" ACL-2015.
  [http://www-nlp.stanford.edu/software/sempre/wikitable/](http://www-nlp.stanford.edu/software/sempre/wikitable/)

### Supported Tasks and Leaderboards

[More Information Needed]

### Languages

English (`en`).

## Dataset Structure

### Data Instances

```
{'id': 'nt-639',
 'annotator': 0,
 'position': 0,
 'question': 'where are the players from?',
 'table_file': 'table_csv/203_149.csv',
 'table_header': ['Pick', 'Player', 'Team', 'Position', 'School'],
 'table_data': [['1',
   'Ben McDonald',
   'Baltimore Orioles',
   'RHP',
   'Louisiana State University'],
  ['2',
   'Tyler Houston',
   'Atlanta Braves',
   'C',
   '"Valley HS (Las Vegas',
   ' NV)"'],
  ['3', 'Roger Salkeld', 'Seattle Mariners', 'RHP', 'Saugus (CA) HS'],
  ['4',
   'Jeff Jackson',
   'Philadelphia Phillies',
   'OF',
   '"Simeon HS (Chicago',
   ' IL)"'],
  ['5', 'Donald Harris', 'Texas Rangers', 'OF', 'Texas Tech University'],
  ['6', 'Paul Coleman', 'Saint Louis Cardinals', 'OF', 'Frankston (TX) HS'],
  ['7', 'Frank Thomas', 'Chicago White Sox', '1B', 'Auburn University'],
  ['8', 'Earl Cunningham', 'Chicago Cubs', 'OF', 'Lancaster (SC) HS'],
  ['9',
   'Kyle Abbott',
   'California Angels',
   'LHP',
   'Long Beach State University'],
  ['10',
   'Charles Johnson',
   'Montreal Expos',
   'C',
   '"Westwood HS (Fort Pierce',
   ' FL)"'],
  ['11',
   'Calvin Murray',
   'Cleveland Indians',
   '3B',
   '"W.T. White High School (Dallas',
   ' TX)"'],
  ['12', 'Jeff Juden', 'Houston Astros', 'RHP', 'Salem (MA) HS'],
  ['13', 'Brent Mayne', 'Kansas City Royals', 'C', 'Cal State Fullerton'],
  ['14',
   'Steve Hosey',
   'San Francisco Giants',
   'OF',
   'Fresno State University'],
  ['15',
   'Kiki Jones',
   'Los Angeles Dodgers',
   'RHP',
   '"Hillsborough HS (Tampa',
   ' FL)"'],
  ['16', 'Greg Blosser', 'Boston Red Sox', 'OF', 'Sarasota (FL) HS'],
  ['17', 'Cal Eldred', 'Milwaukee Brewers', 'RHP', 'University of Iowa'],
  ['18',
   'Willie Greene',
   'Pittsburgh Pirates',
   'SS',
   '"Jones County HS (Gray',
   ' GA)"'],
  ['19', 'Eddie Zosky', 'Toronto Blue Jays', 'SS', 'Fresno State University'],
  ['20', 'Scott Bryant', 'Cincinnati Reds', 'OF', 'University of Texas'],
  ['21', 'Greg Gohr', 'Detroit Tigers', 'RHP', 'Santa Clara University'],
  ['22',
   'Tom Goodwin',
   'Los Angeles Dodgers',
   'OF',
   'Fresno State University'],
  ['23', 'Mo Vaughn', 'Boston Red Sox', '1B', 'Seton Hall University'],
  ['24', 'Alan Zinter', 'New York Mets', 'C', 'University of Arizona'],
  ['25', 'Chuck Knoblauch', 'Minnesota Twins', '2B', 'Texas A&M University'],
  ['26', 'Scott Burrell', 'Seattle Mariners', 'RHP', 'Hamden (CT) HS']],
 'answer_coordinates': {'row_index': [0,
   1,
   2,
   3,
   4,
   5,
   6,
   7,
   8,
   9,
   10,
   11,
   12,
   13,
   14,
   15,
   16,
   17,
   18,
   19,
   20,
   21,
   22,
   23,
   24,
   25],
  'column_index': [4,
   4,
   4,
   4,
   4,
   4,
   4,
   4,
   4,
   4,
   4,
   4,
   4,
   4,
   4,
   4,
   4,
   4,
   4,
   4,
   4,
   4,
   4,
   4,
   4,
   4]},
 'answer_text': ['Louisiana State University',
  'Valley HS (Las Vegas, NV)',
  'Saugus (CA) HS',
  'Simeon HS (Chicago, IL)',
  'Texas Tech University',
  'Frankston (TX) HS',
  'Auburn University',
  'Lancaster (SC) HS',
  'Long Beach State University',
  'Westwood HS (Fort Pierce, FL)',
  'W.T. White High School (Dallas, TX)',
  'Salem (MA) HS',
  'Cal State Fullerton',
  'Fresno State University',
  'Hillsborough HS (Tampa, FL)',
  'Sarasota (FL) HS',
  'University of Iowa',
  'Jones County HS (Gray, GA)',
  'Fresno State University',
  'University of Texas',
  'Santa Clara University',
  'Fresno State University',
  'Seton Hall University',
  'University of Arizona',
  'Texas A&M University',
  'Hamden (CT) HS']}
```

### Data Fields

- `id` (`str`): question sequence id (the id is consistent with those in WTQ)
- `annotator` (`int`): `0`, `1`, `2` (the 3 annotators who annotated the question intent)
- `position` (`int`): the position of the question in the sequence
- `question` (`str`): the question given by the annotator
- `table_file` (`str`): the associated table
- `table_header` (`List[str]`): a list of headers in the table
- `table_data` (`List[List[str]]`): 2d array of data in the table
- `answer_coordinates` (`List[Dict]`): the table cell coordinates of the answers (0-based, where 0 is the first row after the table header)
  - `row_index`
  - `column_index`
- `answer_text` (`List[str]`): the content of the answer cells

Note that some text fields may contain Tab or LF characters and thus start with quotes.
It is recommended to use a CSV parser like the Python CSV package to process the data.

### Data Splits


|             | train | test |
|-------------|------:|-----:|
| N. examples | 14541 | 3012 |


## Dataset Creation

### Curation Rationale

[More Information Needed]

### Source Data

#### Initial Data Collection and Normalization

[More Information Needed]

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

[Microsoft Research Data License Agreement](https://msropendata-web-api.azurewebsites.net/licenses/2f933be3-284d-500b-7ea3-2aa2fd0f1bb2/view).

### Citation Information

```
@inproceedings{iyyer-etal-2017-search,
    title = "Search-based Neural Structured Learning for Sequential Question Answering",
    author = "Iyyer, Mohit  and
      Yih, Wen-tau  and
      Chang, Ming-Wei",
    booktitle = "Proceedings of the 55th Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers)",
    month = jul,
    year = "2017",
    address = "Vancouver, Canada",
    publisher = "Association for Computational Linguistics",
    url = "https://aclanthology.org/P17-1167",
    doi = "10.18653/v1/P17-1167",
    pages = "1821--1831",
}

```

### Contributions

Thanks to [@mattbui](https://github.com/mattbui) for adding this dataset.
