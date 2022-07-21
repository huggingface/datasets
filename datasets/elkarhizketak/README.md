---
annotations_creators:
- no-annotation
language_creators:
- crowdsourced
language:
- eu
license:
- cc-by-sa-4.0
multilinguality:
- monolingual
size_categories:
- 1K<n<10K
source_datasets:
- original
task_categories:
- question-answering
task_ids:
- extractive-qa
- question-ansering-other-dialogue-qa
pretty_name: ElkarHizketak
---

# Dataset Card for ElkarHizketak

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
    - [Initial Data Collection and Normalization](#initial-data-collection-and-normalization)
    - [Who are the source language producers?](#who-are-the-source-language-producers)
  - [Annotations](#annotations)
    - [Annotation process](#annotation-process)
    - [Who are the annotators?](#who-are-the-annotators)
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

- **Homepage:** [ElkarHizketak homepage](http://ixa.si.ehu.es/node/12934)
- **Paper:** [Conversational Question Answering in Low Resource Scenarios: A Dataset and Case Study for Basque](https://aclanthology.org/2020.lrec-1.55/)
- **Point of Contact:** [Arantxa Otegi](mailto:arantza.otegi@ehu.eus)

### Dataset Summary

ElkarHizketak is a low resource conversational Question Answering (QA) dataset in Basque created by Basque speaker volunteers. The dataset contains close to 400 dialogues and more than 1600 question and answers, and its small size presents a realistic low-resource scenario for conversational QA systems. The dataset is built on top of Wikipedia sections about popular people and organizations. The dialogues involve two crowd workers: (1) a student ask questions after reading a small introduction about the person, but without seeing the section text; and (2) a teacher answers the questions selecting a span of text of the section.

### Supported Tasks and Leaderboards

- `extractive-qa`: The dataset can be used to train a model for Conversational Question Answering.

### Languages

The text in the dataset is in Basque.

## Dataset Structure

### Data Instances

An example from the train split:
```
{'dialogue_id': 'C_50be3f56f0d04c99a82f1f950baf0c2d',
 'wikipedia_page_title': 'Howard Becker',
 'background': 'Howard Saul Becker (Chicago,Illinois, 1928ko apirilaren 18an) Estatu Batuetako soziologoa bat da. Bere ekarpen handienak desbiderakuntzaren soziologian, artearen soziologian eta musikaren soziologian egin ditu. "Outsiders" (1963) bere lanik garrantzitsuetako da eta bertan garatu zuen bere etiketatze-teoria. Nahiz eta elkarrekintza sinbolikoaren edo gizarte-konstruktibismoaren korronteen barruan sartu izan, berak ez du bere burua inongo paradigman kokatzen. Chicagoko Unibertsitatean graduatua, Becker Chicagoko Soziologia Eskolako bigarren belaunaldiaren barruan kokatu ohi da, Erving Goffman eta Anselm Strauss-ekin batera.',
 'section_title': 'Hastapenak eta hezkuntza.',
 'context': 'Howard Saul Becker Chicagon jaio zen 1928ko apirilaren 18an. Oso gazte zelarik piano jotzen asi zen eta 15 urte zituenean dagoeneko tabernetan aritzen zen pianoa jotzen. Beranduago Northwestern Unibertsitateko banda batean jo zuen. Beckerren arabera, erdi-profesional gisa aritu ahal izan zen Bigarren Mundu Gerra tokatu eta musikari gehienak soldadugai zeudelako. Musikari bezala egin zuen lan horretan egin zuen lehen aldiz drogaren kulturaren ezagutza, aurrerago ikerketa-gai hartuko zuena. 1946an bere graduazpiko soziologia titulua lortu zuen Chicagoko Unibertsitatean. Ikasten ari zen bitartean, pianoa jotzen jarraitu zuen modu erdi-profesionalean. Hala ere, soziologiako masterra eta doktoretza eskuratu zituen Chicagoko Unibertsitatean. Unibertsitate horretan Chicagoko Soziologia Eskolaren jatorrizko tradizioaren barruan hezia izan zen. Chicagoko Soziologia Eskolak garrantzi berezia ematen zion datu kualitatiboen analisiari eta Chicagoko hiria hartzen zuen ikerketa eremu bezala. Beckerren hasierako lan askok eskola honen tradizioaren eragina dute, bereziko Everett C. Hughes-en eragina, bere tutore eta gidari izan zena. Askotan elkarrekintzaile sinboliko bezala izendatua izan da, nahiz eta Beckerek berak ez duen gogoko izendapen hori. Haren arabera, bere leinu akademikoa Georg Simmel, Robert E. Park eta Everett Hughes dira. Doktoretza lortu ostean, 23 urterekin, Beckerrek marihuanaren erabilpena ikertu zuen "Institut for Juvenil Reseac"h-en. Ondoren Illinoisko Unibertsitatean eta Standfor Unibertsitateko ikerketa institutu batean aritu zen bere irakasle karrera hasi aurretik. CANNOTANSWER',
 'turn_id': 'C_50be3f56f0d04c99a82f1f950baf0c2d_q#0',
 'question': 'Zer da desbiderakuntzaren soziologia?',
 'yesno': 2,
 'answers': {'text': ['CANNOTANSWER'],
  'answer_start': [1601],
  'input_text': ['CANNOTANSWER']},
 'orig_answer': {'text': 'CANNOTANSWER', 'answer_start': 1601}}
 ```

### Data Fields

The different fields are:

- `dialogue_id`: string,
- `wikipedia_page_title`: title of the wikipedia page as a string,
- `background`: string,
- `section_title`: title os the section as a string,
- `context`: context of the question as a string string,
- `turn_id`: string,
- `question`: question as a string,
- `yesno`: Class label that represents if the question is a yes/no question. Possible values are "y" (0), "n" (1), "x" (2),
- `answers`: a dictionary with three fields:
  - `text`: list of texts of the answer as a string,
  - `answer_start`: list of positions of the answers in the context as an int32,
  - `input_text`: list of strings,
    }
),
- `orig_answer`: {
  - `text`: original answer text as a string,
  - `answer_start`: original position of the answer as an int32,
},

### Data Splits

The data is split into a training, development and test set. The split sizes are as follow:

- train: 1,306 questions / 301 dialogues
- development:  161 questions / 38 dialogues
- test: 167 questions / 38 dialogues

## Dataset Creation

### Curation Rationale

This is the first non-English conversational QA dataset and the first conversational dataset for Basque. Its small size presents a realistic low-resource scenario for conversational QA systems.

### Source Data

#### Initial Data Collection and Normalization

First we selected sections of Wikipedia articles about people, as less specialized knowledge is required to converse about people than other categories. In order to retrieve articles we selected the following categories in Basque Wikipedia: Biografia (Biography is the equivalent category in English Wikipedia), Biografiak (People) and Gizabanako biziak (Living people). We applied this category filter and downloaded the articles using a querying tool provided by the Wikimedia foundation. Once we retrieved the articles, we selected sections from them that contained between 175 and 300 words. These filters and threshold were set after some pilot studies where we check the adequacy of the people involved in the selected articles and the length of the passages in order to have enough but not to much information to hold a conversation.

Then, dialogues were collected during some online sessions that we arranged with Basque speaking volunteers. The dialogues involve two crowd workers: (1) a student ask questions after reading a small introduction about the person, but without seeing the section text; and (2) a teacher answers the questions selecting a span of text of the section.

#### Who are the source language producers?

The language producers are Basque speaking volunteers which hold a conversation using a text-based chat interface developed for those purposes.

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

The dataset was created by Arantxa Otegi, Jon Ander Campos, Aitor Soroa and Eneko Agirre from the [HiTZ Basque Center for Language Technologies](https://www.hitz.eus/) and [Ixa NLP Group](https://www.ixa.eus/) at the University of the Basque Country (UPV/EHU).

### Licensing Information

Copyright (C) by Ixa Taldea, University of the Basque Country UPV/EHU.

This dataset is licensed under the Creative Commons Attribution-ShareAlike 4.0 International Public License (CC BY-SA 4.0).
To view a copy of this license, visit [https://creativecommons.org/licenses/by-sa/4.0/legalcode](https://creativecommons.org/licenses/by-sa/4.0/legalcode).

### Citation Information

If you are using this dataset in your work, please cite this publication:

```bibtex
@inproceedings{otegi-etal-2020-conversational,
    title = "{Conversational Question Answering in Low Resource Scenarios: A Dataset and Case Study for Basque}",
    author = "Otegi, Arantxa  and
      Agirre, Aitor  and
      Campos, Jon Ander  and
      Soroa, Aitor  and
      Agirre, Eneko",
    booktitle = "Proceedings of the 12th Language Resources and Evaluation Conference",
    year = "2020",
    address = "Marseille, France",
    publisher = "European Language Resources Association",
    url = "https://aclanthology.org/2020.lrec-1.55",
    pages = "436--442"
}
```

### Contributions

Thanks to [@antxa](https://github.com/antxa) for adding this dataset.