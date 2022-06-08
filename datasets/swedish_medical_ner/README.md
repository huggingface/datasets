---
annotations_creators:
- machine-generated
- expert-generated
language_creators:
- found
languages:
- sv-SE
licenses:
- cc-by-sa-4.0
multilinguality:
- monolingual
size_categories:
- 100K<n<1M
source_datasets:
- original
task_categories:
- token-classification
task_ids:
- named-entity-recognition
pretty_name: SwedMedNER
---

# Dataset Card for swedish_medical_ner

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

- **Repository:** https://github.com/olofmogren/biomedical-ner-data-swedish
- **Paper:** [Named Entity Recognition in Swedish Health Records with Character-Based Deep Bidirectional LSTMs](https://aclanthology.org/W16-5104.pdf)
- **Point of Contact:** [Olof Mogren](olof@mogren.one)

### Dataset Summary

SwedMedNER is Named Entity Recognition dataset on medical text in Swedish. It consists three subsets which are in turn derived from three different sources respectively: the Swedish Wikipedia (a.k.a. wiki), Läkartidningen (a.k.a. lt), and 1177 Vårdguiden (a.k.a. 1177). While the Swedish Wikipedia and Läkartidningen subsets in total contains over 790000 sequences with 60 characters each, the 1177 Vårdguiden subset is manually annotated and contains 927 sentences, 2740 annotations, out of which 1574 are _disorder and findings_, 546 are _pharmaceutical drug_, and 620 are _body structure_.

Texts from both Swedish Wikipedia and Läkartidningen were automatically annotated using a list of medical seed terms. Sentences from 1177 Vårdguiden were manuually annotated.


### Supported Tasks and Leaderboards

Medical NER.

### Languages

Swedish (SV).

## Dataset Structure

### Data Instances

Annotated example sentences are shown below:

```
( Förstoppning ) är ett vanligt problem hos äldre.
[ Cox-hämmare ] finns även som gel och sprej.
[ Medicinen ] kan också göra att man blöder lättare eftersom den påverkar { blodets } förmåga att levra sig.
```

Tags are as follows:
- Prenthesis, (): Disorder and Finding
- Brackets, []: Pharmaceutical Drug
- Curly brackets, {}: Body Structure

Data example:

```
In: data = load_dataset('./datasets/swedish_medical_ner', "wiki")
In: data['train']:
Out: 
Dataset({
    features: ['sid', 'sentence', 'entities'],
    num_rows: 48720
})

In: data['train'][0]['sentence']
Out: '{kropp} beskrivs i till exempel människokroppen, anatomi och f'
In: data['train'][0]['entities']
Out: {'start': [0], 'end': [7], 'text': ['kropp'], 'type': [2]}
```

### Data Fields

- `sentence`
- `entities`
    - `start`: the start index
    - `end`: the end index
    - `text`: the text of the entity
    - `type`: entity type: Disorder and Finding (0), Pharmaceutical Drug (1) or Body Structure (2)

### Data Splits

In the original paper, its authors used the text from Läkartidningen for model training, Swedish Wikipedia for validation, and 1177.se for the final model evaluation. 

## Dataset Creation

### Curation Rationale

### Source Data

- Swedish Wikipedia;
- Läkartidningen - contains articles from the Swedish journal for medical professionals;
- 1177.se - a web site provided by the Swedish public health care authorities, containing information, counselling, and other health-care services.

#### Initial Data Collection and Normalization

[More Information Needed]

#### Who are the source language producers?

[More Information Needed]

### Annotations

#### Annotation process

- A list of seed terms was extracted using SweMeSH and SNOMED CT;
   - The following predefined categories was used for the extraction: disorder & finding (sjukdom & symtom), pharmaceutical drug (läkemedel) and body structure (kroppsdel)
- For _Swedish Wikipedia_, an initial list of medical domain articles were selected manually. These source articles as well as their linked articles were downloaded and automatically annotated by finding the aforementioned seed terms with a context window of 60 characters;
- Articles from the _Läkartidningen_ corpus were downloaded and automatically annotated by finding the aforementioned seed terms with a context window of 60 characters;
- 15 documents from _1177.se_ were downloaded in May 2016 and then manually annotated with the seed terms as support, resulting 2740 annotations.

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

- Simon Almgren, simonwalmgren@gmail.com
- Sean Pavlov, sean.pavlov@gmail.com
- Olof Mogren, olof@mogren.one
Chalmers University of Technology

### Licensing Information

This dataset is released under the [Creative Commons Attribution-ShareAlike 4.0 International Public License (CC BY-SA 4.0)](http://creativecommons.org/licenses/by-sa/4.0/).

### Citation Information

```bibtex
@inproceedings{almgrenpavlovmogren2016bioner,
  title={Named Entity Recognition in Swedish Medical Journals with Deep Bidirectional Character-Based LSTMs},
  author={Simon Almgren, Sean Pavlov, Olof Mogren},
  booktitle={Proceedings of the Fifth Workshop on Building and Evaluating Resources for Biomedical Text Mining (BioTxtM 2016)},
  pages={1},
  year={2016}
}
```

### Contributions

Thanks to [@bwang482](https://github.com/bwang482) for adding this dataset.