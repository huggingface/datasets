---
annotations_creators:
- expert-generated
language_creators:
- expert-generated
languages:
- en
licenses:
- cc-by-4.0
multilinguality:
- monolingual
size_categories:
- n<1K
source_datasets:
- original
task_categories:
- structure-prediction
task_ids:
- coreference-resolution
paperswithcode_id: wsc
---

# Dataset Card for The Winograd Schema Challenge

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

- **Homepage:** https://cs.nyu.edu/faculty/davise/papers/WinogradSchemas/WS.html
- **Repository:** 
- **Paper:** https://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.729.9814&rep=rep1&type=pdf
- **Leaderboard:**
- **Point of Contact:**

### Dataset Summary

A Winograd schema is a pair of sentences that differ in only one or two words and that contain an ambiguity that is
resolved in opposite ways in the two sentences and requires the use of world knowledge and reasoning for its
resolution. The schema takes its name from a well-known example by Terry Winograd:

> The city councilmen refused the demonstrators a permit because they [feared/advocated] violence.

If the word is ``feared'', then ``they'' presumably refers to the city council; if it is ``advocated'' then ``they''
presumably refers to the demonstrators.

### Supported Tasks and Leaderboards

From the official webpage:

> A contest, entitled the Winograd Schema Challenge was run once, in 2016. At that time, there was a cash prize
offered for achieving human-level performance in the contest. Since then, the sponsor has withdrawn; therefore NO
CASH PRIZES CAN BE OFFERED OR WILL BE AWARDED FOR ANY KIND OF PERFORMANCE OR ACHIEVEMENT ON THIS CHALLENGE.

### Languages

The dataset is in English.

[Translation of 12 WSs into Chinese ](https://cs.nyu.edu/faculty/davise/papers/WinogradSchemas/WSChinese.html)(translated by Wei Xu).

Translations into Japanese, by Soichiro Tanaka, Rafal Rzepka, and Shiho Katajima\
**Translation changing English names to Japanese **[PDF ](https://cs.nyu.edu/faculty/davise/papers/WinogradSchemas/collection_ja.pdf)    [HTML](http://arakilab.media.eng.hokudai.ac.jp/~kabura/collection_ja.html)\
**Translation preserving English names** [PDF ](https://cs.nyu.edu/faculty/davise/papers/WinogradSchemas/collection_katakana.pdf)    [HTML](http://arakilab.media.eng.hokudai.ac.jp/~kabura/collection_katakana.html)

[Translation into French, ](http://www.llf.cnrs.fr/winograd-fr)by Pascal Amsili and Olga Seminck

[Winograd Schemas in Portuguese](https://sol.sbc.org.br/index.php/eniac/article/view/9334) by Gabriela Melo, Vinicius Imaizumi, and Fábio Cozman.

[Mandarinograd: A Chinese Collection of Winograd Schemas](https://www.aclweb.org/anthology/2020.lrec-1.3) by Timothée Bernard and Ting Han, LREC-2020.

## Dataset Structure

### Data Instances

Each instance contains a text passage with a designated pronoun and two possible answers indicating which entity in
the passage the pronoun represents. An example instance looks like the following:

```python
{
  'label': 0,
  'options': ['The city councilmen', 'The demonstrators'],
  'pronoun': 'they',
  'pronoun_loc': 63,
  'quote': 'they feared violence',
  'quote_loc': 63,
  'source': '(Winograd 1972)',
  'text': 'The city councilmen refused the demonstrators a permit because they feared violence.'
}
 ```

### Data Fields

- `text` (str): The text sequence
- `options` (list[str]): The two entity options that the pronoun may be referring to
- `label` (int): The index of the correct option in the `options` field
- `pronoun` (str): The pronoun in the sequence to be resolved
- `pronoun_loc` (int): The starting position of the pronoun in the sequence
- `quote` (str): The substr with the key action or context surrounding the pronoun
- `quote_loc` (int): The starting position of the quote in the sequence
- `source` (str): A description of the source who contributed the example

### Data Splits

Only a test split is included.

## Dataset Creation

### Curation Rationale

The Winograd Schema Challenge was proposed as an automated evaluation of an AI system's commonsense linguistic
understanding. From the webpage:

> The strengths of the challenge are that it is clear-cut, in that the answer to each schema is a binary choice;
vivid, in that it is obvious to non-experts that a program that fails to get the right answers clearly has serious
gaps in its understanding; and difficult, in that it is far beyond the current state of the art.

### Source Data

#### Initial Data Collection and Normalization

This data was manually written by experts such that the schemas are:

- easily disambiguated by the human reader (ideally, so easily that the reader does not even notice that there is an ambiguity);

- not solvable by simple techniques such as selectional restrictions;

- Google-proof; that is, there is no obvious statistical test over text corpora that will reliably disambiguate these correctly.

#### Who are the source language producers?

This dataset has grown over time, and so was produced by a variety of lingustic and AI researchers. See the `source`
field for the source of each instance.

### Annotations

#### Annotation process

Annotations are produced by the experts who construct the examples.

#### Who are the annotators?

See above.

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

This dataset has grown over time, and so was produced by a variety of lingustic and AI researchers. See the `source`
field for the source of each instance.

### Licensing Information

This work is licensed under a [Creative Commons Attribution 4.0 International
License](https://creativecommons.org/licenses/by/4.0/).

### Citation Information

The Winograd Schema Challenge including many of the examples here was proposed by
[Levesque et al 2012](https://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.729.9814&rep=rep1&type=pdf):

```
@inproceedings{levesque2012winograd,
  title={The winograd schema challenge},
  author={Levesque, Hector and Davis, Ernest and Morgenstern, Leora},
  booktitle={Thirteenth International Conference on the Principles of Knowledge Representation and Reasoning},
  year={2012},
  organization={Citeseer}
}
```
### Contributions

Thanks to [@joeddav](https://github.com/joeddav) for adding this dataset.