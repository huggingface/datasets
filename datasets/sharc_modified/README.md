---
annotations_creators:
- crowdsourced
language_creators:
- crowdsourced
- expert-generated
languages:
- en
licenses:
- unknown
multilinguality:
- monolingual
size_categories:
- 10K<n<100K
source_datasets:
- extended|sharc
task_categories:
- question-answering
task_ids:
- extractive-qa
- question-answering-other-conversational-qa
paperswithcode_id: null
---

# Dataset Card Creation Guide

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

- **Homepage:** [More info needed]
- **Repository:** [github](https://github.com/nikhilweee/neural-conv-qa)
- **Paper:** [Neural Conversational QA: Learning to Reason v.s. Exploiting Patterns](https://arxiv.org/abs/1909.03759)
- **Leaderboard:** [More info needed]
- **Point of Contact:** [More info needed]

### Dataset Summary

[More Information Needed]

### Supported Tasks and Leaderboards

[More Information Needed]

### Languages

The dataset is in english (en).

## Dataset Structure

### Data Instances

Example of one instance:
```
{
    "annotation": {
        "answer": [
            {
                "paragraph_reference": {
                    "end": 64,
                    "start": 35,
                    "string": "syndactyly affecting the feet"
                },
                "sentence_reference": {
                    "bridge": false,
                    "end": 64,
                    "start": 35,
                    "string": "syndactyly affecting the feet"
                }
            }
        ],
        "explanation_type": "single_sentence",
        "referential_equalities": [
            {
                "question_reference": {
                    "end": 40,
                    "start": 29,
                    "string": "webbed toes"
                },
                "sentence_reference": {
                    "bridge": false,
                    "end": 11,
                    "start": 0,
                    "string": "Webbed toes"
                }
            }
        ],
        "selected_sentence": {
            "end": 67,
            "start": 0,
            "string": "Webbed toes is the common name for syndactyly affecting the feet . "
        }
    },
    "example_id": 9174646170831578919,
    "original_nq_answers": [
        {
            "end": 45,
            "start": 35,
            "string": "syndactyly"
        }
    ],
    "paragraph_text": "Webbed toes is the common name for syndactyly affecting the feet . It is characterised by the fusion of two or more digits of the feet . This is normal in many birds , such as ducks ; amphibians , such as frogs ; and mammals , such as kangaroos . In humans it is considered unusual , occurring in approximately one in 2,000 to 2,500 live births .",
    "question": "what is the medical term for webbed toes",
    "sentence_starts": [
        0,
        67,
        137,
        247
    ],
    "title_text": "Webbed toes",
    "url": "https: //en.wikipedia.org//w/index.php?title=Webbed_toes&amp;oldid=801229780"
}
```

### Data Fields

- `example_id`: a unique integer identifier that matches up with NQ
- `title_text`: the title of the wikipedia page containing the paragraph
- `url`: the url of the wikipedia page containing the paragraph
- `question`: a natural language question string from NQ
- `paragraph_text`: a paragraph string from a wikipedia page containing the answer to question
- `sentence_starts`: a list of integer character offsets indicating the start of sentences in the paragraph
- `original_nq_answers`: the original short answer spans from NQ
- `annotation`: the QED annotation, a dictionary with the following items and further elaborated upon below:
  - `referential_equalities`: a list of dictionaries, one for each referential equality link annotated
  - `answer`: a list of dictionaries, one for each short answer span
  - `selected_sentence`: a dictionary representing the annotated sentence in the passage
  - `explanation_type`: one of "single_sentence", "multi_sentence", or "none"


### Data Splits

The dataset is split into training and validation splits.
|                            | Tain   | Valid |
| -----                      | ------ | ----- |
| N. Instances               | 7638   | 1355  |

## Dataset Creation

### Curation Rationale

[More Information Needed]

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

[More Information Needed]

### Citation Information

```
@misc{lamm2020qed,
    title={QED: A Framework and Dataset for Explanations in Question Answering},
    author={Matthew Lamm and Jennimaria Palomaki and Chris Alberti and Daniel Andor and Eunsol Choi and Livio Baldini Soares and Michael Collins},
    year={2020},
    eprint={2009.06354},
    archivePrefix={arXiv},
    primaryClass={cs.CL}
}
```
### Contributions

Thanks to [@patil-suraj](https://github.com/patil-suraj) for adding this dataset.