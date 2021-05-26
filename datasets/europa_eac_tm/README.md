---
annotations_creators:
- expert-generated
language_creators:
- expert-generated
languages:
- bg
- cs
- da
- de
- el
- en
- es
- et
- fi
- fr
- hr
- hu
- is
- it
- lt
- lv
- mt
- nl
- 'no'
- pl
- pt
- ro
- sk
- sl
- sv
- tr
licenses:
- cc-by-4.0
multilinguality:
- translation
size_categories:
- 1K<n<10K
source_datasets:
- original
task_categories:
- conditional-text-generation
task_ids:
- machine-translation
paperswithcode_id: null
---

# Dataset Card for Europa Education and Culture Translation Memory (EAC-TM)

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

- **Homepage:** [https://ec.europa.eu/jrc/en/language-technologies/eac-translation-memory](https://ec.europa.eu/jrc/en/language-technologies/eac-translation-memory)
- **Paper:** [https://link.springer.com/article/10.1007/s10579-014-9277-0](https://link.springer.com/article/10.1007/s10579-014-9277-0)
- **Point of Contact:** [ralf.steinberg@jrc.ec.europa.eu](mailto:ralf.steinberg@jrc.ec.europa.eu)

### Dataset Summary

This dataset is a corpus of manually produced translations from english to up to 25 languages, released in 2012 by the European Union's Directorate General for Education and Culture (EAC).

To load a language pair that is not part of the config, just specify the language code as language pair. For example, if you want to translate Czech to Greek:

`dataset = load_dataset("europa_eac_tm", language_pair=("cs", "el"))`

### Supported Tasks and Leaderboards

- `conditional-text-generation`: the dataset can be used to train a model for `machine-translation`. Machine translation models are usually evaluated using metrics such as [BLEU](https://huggingface.co/metrics/bleu), [ROUGE](https://huggingface.co/metrics/rouge) or [SacreBLEU](https://huggingface.co/metrics/sacrebleu). You can use the [mBART](https://huggingface.co/facebook/mbart-large-cc25) model for this task. This task has active leaderboards which can be found at [https://paperswithcode.com/task/machine-translation](https://paperswithcode.com/task/machine-translation), which usually rank models based on [BLEU score](https://huggingface.co/metrics/bleu).

### Languages

The sentences in this dataset were originally written in English (source language is English) and then translated into the other languages. The sentences are extracted from electroniv forms: application and report forms for decentralised actions of EAC's Life-long Learning Programme (LLP) and the Youth in Action Programme. The contents in the electronic forms are technically split into two types: (a) the labels and contents of drop-down menus (referred to as 'Forms' Data) and (b) checkboxes (referred to as 'Reference Data').

The dataset contains traduction of English sentences or parts of sentences to Bulgarian, Czech, Danish, Dutch, Estonian, German, Greek, Finnish, French, Croatian, Hungarian, Icelandic, Italian, Latvian, Lithuanian, Maltese, Norwegian, Polish, Portuguese, Romanian, Slovak, Slovenian, Spanish, Swedish and Turkish.

Language codes:
- `bg`
- `cs`
- `da`
- `de`
- `el`
- `en`
- `es`
- `et`
- `fi`
- `fr`
- `hr`
- `hu`
- `is`
- `it`
- `lt`
- `lv`
- `mt`
- `nl`
- `no`
- `pl`
- `pt`
- `ro`
- `sk`
- `sl`
- `sv`
- `tr`

## Dataset Structure

### Data Instances

```
{
  "translation": {
    "en":"Sentence to translate",
    "<target_language>": "Phrase à traduire",
  },
  "sentence_type": 0
}
```

### Data Fields

- `translation`: Mapping of sentences to translate (in English) and translated sentences.

- `sentence_type`: Integer value, 0 if the sentence is a 'form data' (extracted from the labels and contents of drop-down menus of the source electronic forms) or 1 if the sentence is a 'reference data' (extracted from the electronic forms checkboxes).

### Data Splits

The data is not splitted (only the `train` split is available).

## Dataset Creation

### Curation Rationale

The EAC-TM is relatively small compared to the JRC-Acquis and to DGT-TM, but it has the advantage that it focuses on a very different domain, namely that of education and culture. Also, it includes translation units for the languages Croatian (HR), Icelandic (IS), Norwegian (Bokmål, NB or Norwegian, NO) and Turkish (TR).

### Source Data

#### Initial Data Collection and Normalization

EAC-TM was built in the context of translating electronic forms: application and report forms for decentralised actions of EAC's Life-long Learning Programme (LLP) and the Youth in Action Programme. All documents and sentences were originally written in English (source language is English) and then translated into the other languages.

The contents in the electronic forms are technically split into two types: (a) the labels and contents of drop-down menus (referred to as 'Forms' Data) and (b) checkboxes (referred to as 'Reference Data'). Due to the different types of data, the two collections are kept separate. For example, labels can be 'Country', 'Please specify your home country' etc., while examples for reference data are 'Germany', 'Basic/general programmes', 'Education and Culture' etc.

The data consists of translations carried out between the end of the year 2008 and July 2012.

#### Who are the source language producers?

The texts were translated by staff of the National Agencies of the Lifelong Learning and Youth in Action programmes. They are typically professionals in the field of education/youth and EU programmes. They are thus not professional translators, but they are normally native speakers of the target language.

### Annotations

#### Annotation process

Sentences were manually translated by humans.
#### Who are the annotators?

The texts were translated by staff of the National Agencies of the Lifelong Learning and Youth in Action programmes. They are typically professionals in the field of education/youth and EU programmes. They are thus not professional translators, but they are normally native speakers of the target language.

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

© European Union, 1995-2020

The Commission's reuse policy is implemented by the [Commission Decision of 12 December 2011 on the reuse of Commission documents](https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32011D0833).

Unless otherwise indicated (e.g. in individual copyright notices), content owned by the EU on this website is licensed under the [Creative Commons Attribution 4.0 International (CC BY 4.0) licence](http://creativecommons.org/licenses/by/4.0/). This means that reuse is allowed, provided appropriate credit is given and changes are indicated.

You may be required to clear additional rights if a specific content depicts identifiable private individuals or includes third-party works. To use or reproduce content that is not owned by the EU, you may need to seek permission directly from the rightholders. Software or documents covered by industrial property rights, such as patents, trade marks, registered designs, logos and names, are excluded from the Commission's reuse policy and are not licensed to you.

### Citation Information

```
@Article{Steinberger2014,
        author={Steinberger, Ralf
                and Ebrahim, Mohamed
                and Poulis, Alexandros
                and Carrasco-Benitez, Manuel
                and Schl{\"u}ter, Patrick
                and Przybyszewski, Marek
                and Gilbro, Signe},
        title={An overview of the European Union's highly multilingual parallel corpora},
        journal={Language Resources and Evaluation},
        year={2014},
        month={Dec},
        day={01},
        volume={48},
        number={4},
        pages={679-707},
        issn={1574-0218},
        doi={10.1007/s10579-014-9277-0},
        url={https://doi.org/10.1007/s10579-014-9277-0}
}
```

### Contributions

Thanks to [@SBrandeis](https://github.com/SBrandeis) for adding this dataset.