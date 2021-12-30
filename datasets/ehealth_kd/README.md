---
annotations_creators:
- expert-generated
language_creators:
- expert-generated
languages:
- es
licenses:
- cc-by-nc-sa-4.0
multilinguality:
- monolingual
size_categories:
- 1K<n<10K
source_datasets:
- original
task_categories:
- structure-prediction
task_ids:
- named-entity-recognition
- structure-prediction-other-relation-prediction
paperswithcode_id: null
---

# Dataset Card for eHealth-KD

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

- **Homepage:** [eHealth-KD homepage](https://knowledge-learning.github.io/ehealthkd-2020/)
- **Repository:** [eHealth-KD repository](https://github.com/knowledge-learning/ehealthkd-2020)
- **Paper:** [eHealth-KD overview paper](http://ceur-ws.org/Vol-2664/eHealth-KD_overview.pdf)
- **Leaderboard:** [eHealth-KD Challenge 2020 official results](https://knowledge-learning.github.io/ehealthkd-2020/results)
- **Point of Contact:** [Yoan Gutiérrez Vázquez](mailto:ygutierrez@dlsi.ua.es) (Organization Committee), [María Grandury](mailto:yacine@huggingface.co) (Dataset Submitter)

### Dataset Summary

Dataset of the eHealth-KD Challenge at IberLEF 2020. It is designed for the identification of semantic 
entities and relations in Spanish health documents.

### Supported Tasks and Leaderboards

The eHealth-KD challenge proposes two computational subtasks:

- `named-entity-recognition`: Given a sentence of an eHealth document written in Spanish, the goal of this subtask is to 
identify all the entities and their types.

- `relation-prediction`: The purpose of this subtask is to recognise all relevant semantic relationships between the entities recognised.

For an analysis of the most successful approaches of this challenge, read the [eHealth-KD overview paper](http://ceur-ws.org/Vol-2664/eHealth-KD_overview.pdf).

### Languages

The text in the dataset is in Spanish (BCP-47 code: `es`).

## Dataset Structure

### Data Instances

The first example of the eHeatlh-KD Corpus train set looks as follows:
```
{
'sentence': 'En la leucemia linfocítica crónica, hay demasiados linfocitos, un tipo de glóbulos blancos.',
'entities': {
    [
        'ent_id: 'T1',
        'ent_text': 'leucemia linfocítica crónica',
        'ent_label': 0,
        'start_character': 6,
        'end_character': 34
    ],
    [
        'ent_id: 'T2',
        'ent_text': 'linfocitos',
        'ent_label': 0,
        'start_character': 51,
        'end_character': 61
    ],
    [
        'ent_id: 'T3',
        'ent_text': 'glóbulos blancos',
        'ent_label': 0,
        'start_character': 74,
        'end_character': 90
    ]
},
relations: {
    [
        'rel_id: 'R0'
        'rel_label': 0,
        'arg1': T2
        'arg2': T3
    ],
    [
        'rel_id': 'R1'
        'rel_label': 5,
        'arg1': T1,
        'arg2': T2
    ]
}
}
```

### Data Fields

- `sentence`: sentence of an eHealth document written in Spanish
- `entities`: list of entities identified in the sentence
    - `ent_id`: entity identifier (`T`+ a number)
    - `ent_text`: entity, can consist of one or more complete words (i.e., not a prefix or a suffix of a word), and will
     never include any surrounding punctuation symbols, parenthesis, etc.
    - `ent_label`: type of entity (`Concept`, `Action`, `Predicate` or `Reference`)
    - `start_character`: position of the first character of the entity
    - `end_character`: position of the last character of the entity
- `relations`: list of semantic relationships between the entities recognised
    - `rel_id`: relation identifier (`R` + a number)
    - `rel_label`: type of relation, can be a general relation (`is-a`, `same-as`, `has-property`, `part-of`, `causes`, `entails`),
    a contextual relation (`in-time`, `in-place`, `in-context`) an action role (`subject`, `target`) or a predicate role (`domain`, `arg`). 
    - `arg1`: ID of the first entity of the relation
    - `arg2`: ID of the second entity of the relation

For more information about the types of entities and relations, click [here](https://knowledge-learning.github.io/ehealthkd-2020/tasks).

### Data Splits

The data is split into a training, validation and test set. The split sizes are as follow:

|                 | Train  | Val   | Test |
| -----           | ------ | ----- | ---- |
| eHealth-KD 2020 | 800    | 199   | 100  |

In the challenge there are 4 different scenarios for testing. The test data of this dataset corresponds to the third scenario.
More information about the testing data [here](https://github.com/knowledge-learning/ehealthkd-2020/tree/master/data/testing).

## Dataset Creation

### Curation Rationale

The vast amount of clinical text available online has motivated the development of automatic
knowledge discovery systems that can analyse this data and discover relevant facts.

The eHealth Knowledge Discovery (eHealth-KD) challenge, in its third edition, leverages
a semantic model of human language that encodes the most common expressions of factual
knowledge, via a set of four general-purpose entity types and thirteen semantic relations among
them. The challenge proposes the design of systems that can automatically annotate entities and
relations in clinical text in the Spanish language.

### Source Data

#### Initial Data Collection and Normalization

As in the previous edition, the corpus for eHealth-KD 2020 has been extracted from MedlinePlus sources. This platform 
freely provides large health textual data from which we have made a selection for constituting the eHealth-KD corpus. 
The selection has been made by sampling specific XML files from the collection available in the [Medline website](https://medlineplus.gov/xml.html).

```
“MedlinePlus is the National Institutes of Health’s Website for patients and their families and
friends. Produced by the National Library of Medicine, the world’s largest medical library, it 
brings you information about diseases, conditions, and wellness issues in language you can 
understand. MedlinePlus offers reliable, up-to-date health information, anytime, anywhere, for free.”
```

These files contain several entries related to health and medicine topics and have been processed to remove all 
XML markup to extract the textual content. Only Spanish language items were considered. Once cleaned, each individual 
item was converted to a plain text document, and some further post-processing is applied to remove unwanted sentences, 
such as headers, footers and similar elements, and to flatten HTML lists into plain sentences. 

#### Who are the source language producers?

As in the previous edition, the corpus for eHealth-KD 2020 was extracted from [MedlinePlus](https://medlineplus.gov/xml.html) sources.

### Annotations

#### Annotation process

Once the MedlinePlus files were cleaned, they were manually tagged using [BRAT](http://brat.nlplab.org/) by a group of 
annotators. After tagging, a post-processing was applied to BRAT’s output files (ANN format) to obtain the output files 
in the formats needed for the challenge.

#### Who are the annotators?

The data was manually tagged.

### Personal and Sensitive Information

[More Information Needed]

## Considerations for Using the Data

### Social Impact of Dataset

"The eHealth-KD 2020 proposes –as the previous editions– modeling the human language in a scenario in which Spanish 
electronic health documents could be machine-readable from a semantic point of view. 
 
 With this task, we expect to encourage the development of software technologies to automatically extract a large variety 
 of knowledge from eHealth documents written in the Spanish Language."

### Discussion of Biases

[More Information Needed]

### Other Known Limitations

[More Information Needed]

## Additional Information

### Dataset Curators

#### Organization Committee

|                   Name                  |         Email         |          Institution          |
|:---------------------------------------:|:---------------------:|:-----------------------------:|
| Yoan Gutiérrez Vázquez (contact person) | ygutierrez@dlsi.ua.es | University of Alicante, Spain |
| Suilan Estévez Velarde                  | sestevez@matcom.uh.cu | University of Havana, Cuba    |
| Alejandro Piad Morffis                  | apiad@matcom.uh.cu    | University of Havana, Cuba    |
| Yudivián Almeida Cruz                   | yudy@matcom.uh.cu     | University of Havana, Cuba    |
| Andrés Montoyo Guijarro                 | montoyo@dlsi.ua.es    | University of Alicante, Spain |
| Rafael Muñoz Guillena                   | rafael@dlsi.ua.es     | University of Alicante, Spain |

#### Funding

This research has been supported by a Carolina Foundation grant in agreement with University of Alicante and University 
of Havana. Moreover, it has also been partially funded by both aforementioned universities, IUII, Generalitat Valenciana,
Spanish Government, Ministerio de Educación, Cultura y Deporte through the projects SIIA (PROMETEU/2018/089) and 
LIVINGLANG (RTI2018-094653-B-C22).

### Licensing Information

This dataset is under the Attribution-NonCommercial-ShareAlike 4.0 International 
[(CC BY-NC-SA 4.0)](https://creativecommons.org/licenses/by-nc-sa/4.0/).

To accept the distribution terms, please fill in the following [form](https://forms.gle/pUJutSDq2FYLwNWQA).

### Citation Information

In the following link you can find the 
[preliminar bibtexts of the systems’ working-notes](https://knowledge-learning.github.io/ehealthkd-2020/shared/eHealth-KD_2020_bibtexts.zip).
In addition, to cite the eHealth-KD challenge you can use the following preliminar bibtext:

```
@inproceedings{overview_ehealthkd2020,
  author    = {Piad{-}Morffis, Alejandro and
               Guti{\'{e}}rrez, Yoan and
               Ca{\~{n}}izares-Diaz, Hian and
               Estevez{-}Velarde, Suilan and 
               Almeida{-}Cruz, Yudivi{\'{a}}n and
               Mu{\~{n}}oz, Rafael and
               Montoyo, Andr{\'{e}}s},
  title     = {Overview of the eHealth Knowledge Discovery Challenge at IberLEF 2020},
  booktitle = ,
  year      = {2020},
}
```
### Contributions

Thanks to [@mariagrandury](https://github.com/mariagrandury) for adding this dataset.