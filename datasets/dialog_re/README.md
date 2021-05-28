---
annotations_creators:
- expert-generated
language_creators:
- expert-generated
languages:
- en
licenses: []
multilinguality:
- monolingual
size_categories:
- 1K<n<10K
source_datasets:
- original
task_categories:
- other
- sequence-modeling
task_ids:
- other-other-relation-extraction
- dialogue-modeling
paperswithcode_id: dialogre
---

# Dataset Card for [DialogRE]

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

- **Homepage:** [DialogRE Homepage](https://dataset.org/dialogre/)
- **Repository:** [DialogRE Repository](https://github.com/nlpdata/dialogre)
- **Paper:** [Arxiv](https://arxiv.org/abs/2004.08056v1)
- **Point of Contact:** [dialogre@dataset.org](mailto:dialogre@dataset.org)

### Dataset Summary

The DialogRE dataset is the first human-annotated dialogue-based relation extraction (RE) dataset, aiming to support the prediction of relation(s) between two arguments that appear in a dialogue. DialogRE can also act as a platform for studying cross-sentence RE as most facts span multiple sentences.  Specifically,  the dataset annotate all occurrences of 36 possible relation types that exist between pairs of arguments in the 1,788 dialogues originating from the complete transcripts of Friends (in English).

### Supported Tasks and Leaderboards

* `other-other-relation-extraction`:  The dataset can be used to train a model for Relation Extraction, which consists of the prediction of relation between two arguments that appear in a dialogue. Success on this task is typically measured by achieving a *high* [F1 Score](https://huggingface.co/metrics/f1). 

### Languages

The dialogues in the dataset is in English originating from the transcripts of Friends. The associated BCP-47 code is `en`.

## Dataset Structure

### Data Instances

A typical data point consists of a dialogue between speakers as a list of sentences. This is followed by the annotations of the relations between the entities in the dialog. 

An example from the DialogRE train set looks as follows:

```
{'dialog': ["Speaker 1: It's been an hour and not one of my classmates has shown up! I tell you, when I actually die some people are gonna get seriously haunted!",
  'Speaker 2: There you go! Someone came!',
  "Speaker 1: Ok, ok! I'm gonna go hide! Oh, this is so exciting, my first mourner!",
  'Speaker 3: Hi, glad you could come.',
  'Speaker 2: Please, come in.',
  "Speaker 4: Hi, you're Chandler Bing, right? I'm Tom Gordon, I was in your class.",
  'Speaker 2: Oh yes, yes... let me... take your coat.',
  "Speaker 4: Thanks... uh... I'm so sorry about Ross, it's...",
  'Speaker 2: At least he died doing what he loved... watching blimps.',
  'Speaker 1: Who is he?',
  'Speaker 2: Some guy, Tom Gordon.',
  "Speaker 1: I don't remember him, but then again I touched so many lives.",
  'Speaker 3: So, did you know Ross well?',
  "Speaker 4: Oh, actually I barely knew him. Yeah, I came because I heard Chandler's news. D'you know if he's seeing anyone?",
  'Speaker 3: Yes, he is. Me.',
  'Speaker 4: What? You... You... Oh! Can I ask you a personal question? Ho-how do you shave your beard so close?',
  "Speaker 2: Ok Tommy, that's enough mourning for you! Here we go, bye bye!!",
  'Speaker 4: Hey, listen. Call me.',
  'Speaker 2: Ok!'],
 'relation_data': {'r': [['per:alternate_names'],
   ['per:alumni'],
   ['per:alternate_names'],
   ['per:alumni', 'per:positive_impression'],
   ['per:alternate_names'],
   ['unanswerable']],
  'rid': [[30], [4], [30], [4, 1], [30], [37]],
  't': [[''], [''], [''], ['', 'call me'], [''], ['']],
  'x': ['Speaker 2',
   'Speaker 2',
   'Speaker 4',
   'Speaker 4',
   'Speaker 4',
   'Speaker 1'],
  'x_type': ['PER', 'PER', 'PER', 'PER', 'PER', 'PER'],
  'y': ['Chandler Bing',
   'Speaker 4',
   'Tom Gordon',
   'Speaker 2',
   'Tommy',
   'Tommy'],
  'y_type': ['PER', 'PER', 'PER', 'PER', 'PER', 'PER']}}
```



### Data Fields

* `dialog`

  * List of dialog spoken between the speakers

* List of annotations per dialog per argument

  * `x` : First entity

  * `y` : Second entity

  * `x_type` : Type of the first entity
  * `y_type`: Type of the second entity
  * `r` : List of relations
  * `rid`: List of relation IDs
  * `t`: List of relation Trigger words

### Data Splits

The data is split into a training, validation and test set as per the original dataset split. 

|                       | Tain | Valid | Test |
| --------------------- | ---- | ----- | ---- |
| Input dialog examples | 1073 | 358   | 357  |

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

DialogRE dataset is intended for non-commercial research purpose only

### Citation Information

```
@inproceedings{yu2020dialogue,
  title={Dialogue-Based Relation Extraction},
  author={Yu, Dian and Sun, Kai and Cardie, Claire and Yu, Dong},
  booktitle={Proceedings of the 58th Annual Meeting of the Association for Computational Linguistics},
  year={2020},
  url={https://arxiv.org/abs/2004.08056v1}
}
```


### Contributions

Thanks to [@vineeths96](https://github.com/vineeths96) for adding this dataset.