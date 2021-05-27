---
annotations_creators:
- crowdsourced
language_creators:
- found
languages:
- en
licenses:
- apache-2.0
multilinguality:
- monolingual
size_categories:
- 1K<n<10K
source_datasets:
- original
task_categories:
- question-answering
task_ids:
- open-domain-qa
paperswithcode_id: selqa
---

# Dataset Card for SelQA

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

- **Homepage:** https://github.com/emorynlp/selqa
- **Repository:** https://github.com/emorynlp/selqa
- **Paper:** https://arxiv.org/abs/1606.00851
- **Leaderboard:** [Needs More Information]
- **Point of Contact:** Tomasz Jurczyk <http://tomaszjurczyk.com/>, Jinho D. Choi <http://www.mathcs.emory.edu/~choi/home.html>

### Dataset Summary

SelQA: A New Benchmark for Selection-Based Question Answering


### Supported Tasks and Leaderboards

Question Answering

### Languages

English

## Dataset Structure

### Data Instances

An example from the `answer selection` set:
```
{
        "section": "Museums",
        "question": "Where are Rockefeller Museum and LA Mayer Institute for Islamic Art?",
        "article": "Israel",
        "is_paraphrase": true,
        "topic": "COUNTRY",
        "answers": [
            5
        ],
        "candidates": [
            "The Israel Museum in Jerusalem is one of Israel's most important cultural institutions and houses the Dead Sea scrolls, along with an extensive collection of Judaica and European art.",
            "Israel's national Holocaust museum, Yad Vashem, is the world central archive of Holocaust-related information.",
            "Beth Hatefutsoth (the Diaspora Museum), on the campus of Tel Aviv University, is an interactive museum devoted to the history of Jewish communities around the world.",
            "Apart from the major museums in large cities, there are high-quality artspaces in many towns and \"kibbutzim\".",
            "\"Mishkan Le'Omanut\" on Kibbutz Ein Harod Meuhad is the largest art museum in the north of the country.",
            "Several Israeli museums are devoted to Islamic culture, including the Rockefeller Museum and the L. A. Mayer Institute for Islamic Art, both in Jerusalem.",
            "The Rockefeller specializes in archaeological remains from the Ottoman and other periods of Middle East history.",
            "It is also the home of the first hominid fossil skull found in Western Asia called Galilee Man.",
            "A cast of the skull is on display at the Israel Museum."
        ],
        "q_types": [
            "where"
        ]
    }
```

An example from the `answer triggering` set:
```
{
        "section": "Museums",
        "question": "Where are Rockefeller Museum and LA Mayer Institute for Islamic Art?",
        "article": "Israel",
        "is_paraphrase": true,
        "topic": "COUNTRY",
        "candidate_list": [
            {
                "article": "List of places in Jerusalem",
                "section": "List_of_places_in_Jerusalem-Museums",
                "answers": [],
                "candidates": [
                    " Israel Museum *Shrine of the Book *Rockefeller Museum of Archeology Bible Lands Museum Jerusalem Yad Vashem Holocaust Museum L.A. Mayer Institute for Islamic Art Bloomfield Science Museum Natural History Museum Museum of Italian Jewish Art Ticho House Tower of David Jerusalem Tax Museum Herzl Museum Siebenberg House Museums.",
                    "Museum on the Seam "
                ]
            },
            {
                "article": "Israel",
                "section": "Israel-Museums",
                "answers": [
                    5
                ],
                "candidates": [
                    "The Israel Museum in Jerusalem is one of Israel's most important cultural institutions and houses the Dead Sea scrolls, along with an extensive collection of Judaica and European art.",
                    "Israel's national Holocaust museum, Yad Vashem, is the world central archive of Holocaust-related information.",
                    "Beth Hatefutsoth (the Diaspora Museum), on the campus of Tel Aviv University, is an interactive museum devoted to the history of Jewish communities around the world.",
                    "Apart from the major museums in large cities, there are high-quality artspaces in many towns and \"kibbutzim\".",
                    "\"Mishkan Le'Omanut\" on Kibbutz Ein Harod Meuhad is the largest art museum in the north of the country.",
                    "Several Israeli museums are devoted to Islamic culture, including the Rockefeller Museum and the L. A. Mayer Institute for Islamic Art, both in Jerusalem.",
                    "The Rockefeller specializes in archaeological remains from the Ottoman and other periods of Middle East history.",
                    "It is also the home of the first hominid fossil skull found in Western Asia called Galilee Man.",
                    "A cast of the skull is on display at the Israel Museum."
                ]
            },
            {
                "article": "L. A. Mayer Institute for Islamic Art",
                "section": "L._A._Mayer_Institute_for_Islamic_Art-Abstract",
                "answers": [],
                "candidates": [
                    "The L.A. Mayer Institute for Islamic Art (Hebrew: \u05de\u05d5\u05d6\u05d9\u05d0\u05d5\u05df \u05dc.",
                    "\u05d0.",
                    "\u05de\u05d0\u05d9\u05e8 \u05dc\u05d0\u05de\u05e0\u05d5\u05ea \u05d4\u05d0\u05e1\u05dc\u05d0\u05dd) is a museum in Jerusalem, Israel, established in 1974.",
                    "It is located in Katamon, down the road from the Jerusalem Theater.",
                    "The museum houses Islamic pottery, textiles, jewelry, ceremonial objects and other Islamic cultural artifacts.",
                    "It is not to be confused with the Islamic Museum, Jerusalem. "
                ]
            },
            {
                "article": "Islamic Museum, Jerusalem",
                "section": "Islamic_Museum,_Jerusalem-Abstract",
                "answers": [],
                "candidates": [
                    "The Islamic Museum is a museum on the Temple Mount in the Old City section of Jerusalem.",
                    "On display are exhibits from ten periods of Islamic history encompassing several Muslim regions.",
                    "The museum is located adjacent to al-Aqsa Mosque.",
                    "It is not to be confused with the L. A. Mayer Institute for Islamic Art, also a museum in Jerusalem. "
                ]
            },
            {
                "article": "L. A. Mayer Institute for Islamic Art",
                "section": "L._A._Mayer_Institute_for_Islamic_Art-Contemporary_Arab_art",
                "answers": [],
                "candidates": [
                    "In 2008, a group exhibit of contemporary Arab art opened at L.A. Mayer Institute, the first show of local Arab art in an Israeli museum and the first to be mounted by an Arab curator.",
                    "Thirteen Arab artists participated in the show. "
                ]
            }
        ],
        "q_types": [
            "where"
        ]
    }
```

An example from any of the `experiments` data:
```
Where are Rockefeller Museum and LA Mayer Institute for Islamic Art ?	The Israel Museum in Jerusalem is one of Israel 's most important cultural institutions and houses the Dead Sea scrolls , along with an extensive collection of Judaica and European art .	0
Where are Rockefeller Museum and LA Mayer Institute for Islamic Art ?	Israel 's national Holocaust museum , Yad Vashem , is the world central archive of Holocaust - related information .	0
Where are Rockefeller Museum and LA Mayer Institute for Islamic Art ?	Beth Hatefutsoth ( the Diaspora Museum ) , on the campus of Tel Aviv University , is an interactive museum devoted to the history of Jewish communities around the world .	0
Where are Rockefeller Museum and LA Mayer Institute for Islamic Art ?	Apart from the major museums in large cities , there are high - quality artspaces in many towns and " kibbutzim " .	0
Where are Rockefeller Museum and LA Mayer Institute for Islamic Art ?	" Mishkan Le'Omanut " on Kibbutz Ein Harod Meuhad is the largest art museum in the north of the country .	0
Where are Rockefeller Museum and LA Mayer Institute for Islamic Art ?	Several Israeli museums are devoted to Islamic culture , including the Rockefeller Museum and the L. A. Mayer Institute for Islamic Art , both in Jerusalem .	1
Where are Rockefeller Museum and LA Mayer Institute for Islamic Art ?	The Rockefeller specializes in archaeological remains from the Ottoman and other periods of Middle East history .	0
Where are Rockefeller Museum and LA Mayer Institute for Islamic Art ?	It is also the home of the first hominid fossil skull found in Western Asia called Galilee Man .	0
Where are Rockefeller Museum and LA Mayer Institute for Islamic Art ?	A cast of the skull is on display at the Israel Museum .	0
```

### Data Fields

#### Answer Selection
##### Data for Analysis

for analysis, the columns are: 

* `question`: the question.
* `article`: the Wikipedia article related to this question.
* `section`: the section in the Wikipedia article related to this question.
* `topic`: the topic of this question, where the topics are *MUSIC*, *TV*, *TRAVEL*, *ART*, *SPORT*, *COUNTRY*, *MOVIES*, *HISTORICAL EVENTS*, *SCIENCE*, *FOOD*.
* `q_types`: the list of question types, where the types are *what*, *why*, *when*, *who*, *where*, and *how*.  If empty, none of the those types are recognized in this question.
* `is_paraphrase`: *True* if this question is a paragraph of some other question in this dataset; otherwise, *False*.
* `candidates`: the list of sentences in the related section.
* `answers`: the list of candidate indices containing the answer context of this question.

##### Data for Experiments

for experiments, each column gives:

* `0`: a question where all tokens are separated.
* `1`: a candidate of the question where all tokens are separated.
* `2`: the label where `0` implies no answer to the question is found in this candidate and `1` implies the answer is found.

#### Answer Triggering
##### Data for Analysis

for analysis, the columns are: 

* `question`: the question.
* `article`: the Wikipedia article related to this question.
* `section`: the section in the Wikipedia article related to this question.
* `topic`: the topic of this question, where the topics are *MUSIC*, *TV*, *TRAVEL*, *ART*, *SPORT*, *COUNTRY*, *MOVIES*, *HISTORICAL EVENTS*, *SCIENCE*, *FOOD*.
* `q_types`: the list of question types, where the types are *what*, *why*, *when*, *who*, *where*, and *how*.  If empty, none of the those types are recognized in this question.
* `is_paraphrase`: *True* if this question is a paragraph of some other question in this dataset; otherwise, *False*.
* `candidate_list`: the list of 5 candidate sections:
  * `article`: the title of the candidate article.
  * `section`: the section in the candidate article.
  * `candidates`: the list of sentences in this candidate section.
  * `answers`: the list of candidate indices containing the answer context of this question (can be empty).

##### Data for Experiments

for experiments, each column gives:

* `0`: a question where all tokens are separated.
* `1`: a candidate of the question where all tokens are separated.
* `2`: the label where `0` implies no answer to the question is found in this candidate and `1` implies the answer is found. 

### Data Splits

|      |Train| Valid| Test|
| ---  | --- | ---  | --- |
| Answer Selection |  5529 | 785 | 1590 |
| Answer Triggering |  27645 | 3925 | 7950 |

## Dataset Creation

### Curation Rationale

To encourage research and provide an initial benchmark for selection based question answering and answer triggering tasks

### Source Data

#### Initial Data Collection and Normalization

[Needs More Information]

#### Who are the source language producers?

[Needs More Information]

### Annotations

#### Annotation process

Crowdsourced

#### Who are the annotators?

[Needs More Information]

### Personal and Sensitive Information

[Needs More Information]

## Considerations for Using the Data

### Social Impact of Dataset

The purpose of this dataset is to help develop better selection-based question answering systems.

### Discussion of Biases

[Needs More Information]

### Other Known Limitations

[Needs More Information]

## Additional Information

### Dataset Curators

[Needs More Information]

### Licensing Information

Apache License 2.0

### Citation Information
@InProceedings{7814688,
  author={T. {Jurczyk} and M. {Zhai} and J. D. {Choi}},
  booktitle={2016 IEEE 28th International Conference on Tools with Artificial Intelligence (ICTAI)}, 
  title={SelQA: A New Benchmark for Selection-Based Question Answering}, 
  year={2016},
  volume={},
  number={},
  pages={820-827},
  doi={10.1109/ICTAI.2016.0128}
}

### Contributions

Thanks to [@Bharat123rox](https://github.com/Bharat123rox) for adding this dataset.