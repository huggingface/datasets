---
annotations_creators:
- no-annotation
language_creators:
- expert-generated
languages:
  en:
  - en
  es:
  - es
licenses:
- mit
multilinguality:
- monolingual
size_categories:
- 1K<n<10K
source_datasets:
- original
task_categories:
- question-answering
task_ids:
- multiple-choice-qa
paperswithcode_id: headqa
---

# Dataset Card for HEAD-QA

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

- **Homepage:** [HEAD-QA homepage](https://aghie.github.io/head-qa/)
- **Repository:** [HEAD-QA repository](https://github.com/aghie/head-qa)
- **Paper:** [HEAD-QA: A Healthcare Dataset for Complex Reasoning](https://www.aclweb.org/anthology/P19-1092/)
- **Leaderboard:** [HEAD-QA leaderboard](https://aghie.github.io/head-qa/#leaderboard-general)
- **Point of Contact:** [María Grandury](mailto:mariagrandury@gmail.com) (Dataset Submitter)

### Dataset Summary

HEAD-QA is a multi-choice HEAlthcare Dataset. The questions come from exams to access a specialized position in the 
Spanish healthcare system, and are challenging even for highly specialized humans. They are designed by the 
[Ministerio de Sanidad, Consumo y Bienestar Social](https://www.mscbs.gob.es/), who also provides direct 
[access](https://fse.mscbs.gob.es/fseweb/view/public/datosanteriores/cuadernosExamen/busquedaConvocatoria.xhtml)
to the exams of the last 5 years (in Spanish).

```
Date of the last update of the documents object of the reuse: January, 14th, 2019.
```

HEAD-QA tries to make these questions accesible for the Natural Language Processing community. We hope it is an useful resource towards achieving better QA systems. The dataset contains questions about the following topics:
- Medicine
- Nursing
- Psychology
- Chemistry
- Pharmacology
- Biology

### Supported Tasks and Leaderboards

- `multiple-choice-qa`: HEAD-QA is a multi-choice question answering testbed to encourage research on complex reasoning.

### Languages

The questions and answers are available in both Spanish (BCP-47 code: 'es-ES') and English (BCP-47 code: 'en').

The language by default is Spanish:
```
from datasets import load_dataset

data_es = load_dataset('head_qa')

data_en = load_dataset('head_qa', 'en')
```

## Dataset Structure

### Data Instances

A typical data point comprises a question `qtext`, multiple possible answers `atext` and the right answer `ra`.

An example from the HEAD-QA dataset looks as follows:
```
{
'qid': '1', 
'category': 'biology', 
'qtext': 'Los potenciales postsinápticos excitadores:',
'answers': [
	{
		'aid': 1, 
		'atext': 'Son de tipo todo o nada.'
	}, 
	{
		'aid': 2, 
		'atext': 'Son hiperpolarizantes.'
	},
	{
		'aid': 3, 
		'atext': 'Se pueden sumar.'
	},
	{
		'aid': 4, 
		'atext': 'Se propagan a largas distancias.'
	},
	{
		'aid': 5, 
		'atext': 'Presentan un periodo refractario.'
	}],
'ra': '3',
'image': <PIL.PngImagePlugin.PngImageFile image mode=RGB size=675x538 at 0x1B42B6A1668>,
'name': 'Cuaderno_2013_1_B',
'year': '2013'
}
```

### Data Fields

- `qid`: question identifier (int)
- `category`: category of the question: "medicine", "nursing", "psychology", "chemistry", "pharmacology", "biology"
- `qtext`: question text
- `answers`: list of possible answers. Each element of the list is a dictionary with 2 keys:
    - `aid`: answer identifier (int)
    - `atext`: answer text
- `ra`: `aid` of the right answer (int)
- `image`: (optional) a `PIL.Image.Image` object containing the image. Note that when accessing the image column: `dataset[0]["image"]` the image file is automatically decoded. Decoding of a large number of image files might take a significant amount of time. Thus it is important to first query the sample index before the `"image"` column, *i.e.* `dataset[0]["image"]` should **always** be preferred over `dataset["image"][0]`
- `name`: name of the exam from which the question was extracted
- `year`: year in which the exam took place

### Data Splits

The data is split into train, validation and test set for each of the two languages. The split sizes are as follow:

|         | Train  | Val   | Test |
| -----   | ------ | ----- | ---- |
| Spanish | 2657   | 1366  | 2742 |
| English | 2657   | 1366  | 2742 |

## Dataset Creation

### Curation Rationale

As motivation for the creation of this dataset, here is the abstract of the paper:

"We present HEAD-QA, a multi-choice question answering testbed to encourage research on complex reasoning. The questions
come from exams to access a specialized position in the Spanish healthcare system, and are challenging even for highly 
specialized humans. We then consider monolingual (Spanish) and cross-lingual (to English) experiments with information 
retrieval and neural techniques. We show that: (i) HEAD-QA challenges current methods, and (ii) the results lag well 
behind human performance, demonstrating its usefulness as a benchmark for future work."

### Source Data

#### Initial Data Collection and Normalization

The questions come from exams to access a specialized position in the Spanish healthcare system, and are designed by the
[Ministerio de Sanidad, Consumo y Bienestar Social](https://www.mscbs.gob.es/), who also provides direct 
[access](https://fse.mscbs.gob.es/fseweb/view/public/datosanteriores/cuadernosExamen/busquedaConvocatoria.xhtml)
to the exams of the last 5 years (in Spanish).

#### Who are the source language producers?

The dataset was created by David Vilares and Carlos Gómez-Rodríguez.

### Annotations

The dataset does not contain any additional annotations.

#### Annotation process

[N/A]

#### Who are the annotators?

[N/A]

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

The dataset was created by David Vilares and Carlos Gómez-Rodríguez.

### Licensing Information

According to the [HEAD-QA homepage](https://aghie.github.io/head-qa/#legal-requirements):

The Ministerio de Sanidad, Consumo y Biniestar Social allows the redistribution of the exams and their content under [certain conditions:](https://www.mscbs.gob.es/avisoLegal/home.htm)

- The denaturalization of the content of the information is prohibited in any circumstance.
- The user is obliged to cite the source of the documents subject to reuse.
- The user is obliged to indicate the date of the last update of the documents object of the reuse.

According to the [HEAD-QA repository](https://github.com/aghie/head-qa/blob/master/LICENSE):

The dataset is licensed under the [MIT License](https://mit-license.org/).

### Citation Information

```
@inproceedings{vilares-gomez-rodriguez-2019-head,
    title = "{HEAD}-{QA}: A Healthcare Dataset for Complex Reasoning",
    author = "Vilares, David  and
      G{\'o}mez-Rodr{\'i}guez, Carlos",
    booktitle = "Proceedings of the 57th Annual Meeting of the Association for Computational Linguistics",
    month = jul,
    year = "2019",
    address = "Florence, Italy",
    publisher = "Association for Computational Linguistics",
    url = "https://www.aclweb.org/anthology/P19-1092",
    doi = "10.18653/v1/P19-1092",
    pages = "960--966",
    abstract = "We present HEAD-QA, a multi-choice question answering testbed to encourage research on complex reasoning. The questions come from exams to access a specialized position in the Spanish healthcare system, and are challenging even for highly specialized humans. We then consider monolingual (Spanish) and cross-lingual (to English) experiments with information retrieval and neural techniques. We show that: (i) HEAD-QA challenges current methods, and (ii) the results lag well behind human performance, demonstrating its usefulness as a benchmark for future work.",
}
```
### Contributions

Thanks to [@mariagrandury](https://github.com/mariagrandury) for adding this dataset.