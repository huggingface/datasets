---
annotations_creators:
- machine-generated
language_creators:
- crowdsourced
languages:
- af
- ar
- az
- be
- ber
- bg
- bn
- br
- ca
- cbk
- cmn
- cs
- da
- de
- el
- en
- eo
- es
- et
- eu
- fi
- fr
- gl
- gos
- he
- hi
- hr
- hu
- hy
- ia
- id
- ie
- io
- is
- it
- ja
- jbo
- kab
- ko
- kw
- la
- lfn
- lt
- mk
- mr
- nb
- nds
- nl
- orv
- ota
- pes
- pl
- pt
- rn
- ro
- ru
- sl
- sr
- sv
- tk
- tl
- tlh
- toki
- tr
- tt
- ug
- uk
- ur
- vi
- vo
- war
- wuu
- yue
licenses:
- cc-by-2.0
multilinguality:
- multilingual
size_categories:
- 100K<n<1M
- 10K<n<100K
- 1K<n<10K
- 1M<n<10M
- n<1K
source_datasets:
- extended|other-tatoeba
task_categories:
- text2text-generation
- translation
- text-classification
task_ids:
- text2text-generation-other-paraphrase-generation
- semantic-similarity-classification
paperswithcode_id: tapaco
pretty_name: TaPaCo Corpus
configs:
- af
- all_languages
- ar
- az
- be
- ber
- bg
- bn
- br
- ca
- cbk
- cmn
- cs
- da
- de
- el
- en
- eo
- es
- et
- eu
- fi
- fr
- gl
- gos
- he
- hi
- hr
- hu
- hy
- ia
- id
- ie
- io
- is
- it
- ja
- jbo
- kab
- ko
- kw
- la
- lfn
- lt
- mk
- mr
- nb
- nds
- nl
- orv
- ota
- pes
- pl
- pt
- rn
- ro
- ru
- sl
- sr
- sv
- tk
- tl
- tlh
- toki
- tr
- tt
- ug
- uk
- ur
- vi
- vo
- war
- wuu
- yue
---

# Dataset Card for TaPaCo Corpus

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

- **Homepage:** [TaPaCo: A Corpus of Sentential Paraphrases for 73 Languages](https://zenodo.org/record/3707949#.X9Dh0cYza3I)
- **Paper:** [TaPaCo: A Corpus of Sentential Paraphrases for 73 Languages](https://www.aclweb.org/anthology/2020.lrec-1.848.pdf)
- **Point of Contact:** [Yves Scherrer](https://blogs.helsinki.fi/yvesscherrer/)

### Dataset Summary
A freely available paraphrase corpus for 73 languages extracted from the Tatoeba database. 
Tatoeba is a crowdsourcing project mainly geared towards language learners. Its aim is to provide example sentences 
and translations for particular linguistic constructions and words. The paraphrase corpus is created by populating a 
graph with Tatoeba sentences and equivalence links between sentences “meaning the same thing”. This graph is then 
traversed to extract sets of paraphrases. Several language-independent filters and pruning steps are applied to 
remove uninteresting sentences. A manual evaluation performed on three languages shows that between half and three 
quarters of inferred paraphrases are correct and that most remaining ones are either correct but trivial, 
or near-paraphrases that neutralize a morphological distinction. The corpus contains a total of 1.9 million 
sentences, with 200 – 250 000 sentences per language. It covers a range of languages for which, to our knowledge,
no other paraphrase dataset exists.

### Supported Tasks and Leaderboards
Paraphrase detection and generation have become popular tasks in NLP
and are increasingly integrated into a wide variety of common downstream tasks such as machine translation
, information retrieval, question answering, and semantic parsing. Most of the existing datasets
 cover only a single language – in most cases English – or a small number of languages. Furthermore, some paraphrase
  datasets focus on lexical and phrasal rather than sentential paraphrases, while others are created (semi
  -)automatically using machine translation.

The number of sentences per language ranges from 200 to 250 000, which makes the dataset
more suitable for fine-tuning and evaluation purposes than
for training. It is well-suited for multi-reference evaluation
of paraphrase generation models, as there is generally not a
single correct way of paraphrasing a given input sentence.

### Languages

The dataset contains paraphrases in Afrikaans, Arabic, Azerbaijani, Belarusian, Berber languages, Bulgarian, Bengali
, Breton, Catalan; Valencian, Chavacano, Mandarin, Czech, Danish, German, Greek, Modern (1453-), English, Esperanto
, Spanish; Castilian, Estonian, Basque, Finnish, French, Galician, Gronings, Hebrew, Hindi, Croatian, Hungarian
, Armenian, Interlingua (International Auxiliary Language Association), Indonesian, Interlingue; Occidental, Ido
, Icelandic, Italian, Japanese, Lojban, Kabyle, Korean, Cornish, Latin, Lingua Franca Nova\t, Lithuanian, Macedonian
, Marathi, Bokmål, Norwegian; Norwegian Bokmål, Low German; Low Saxon; German, Low; Saxon, Low, Dutch; Flemish, ]Old
 Russian, Turkish, Ottoman (1500-1928), Iranian Persian, Polish, Portuguese, Rundi, Romanian; Moldavian; Moldovan, 
 Russian, Slovenian, Serbian, Swedish, Turkmen, Tagalog, Klingon; tlhIngan-Hol, Toki Pona, Turkish, Tatar, 
 Uighur; Uyghur, Ukrainian, Urdu, Vietnamese, Volapük, Waray, Wu Chinese and Yue Chinese

## Dataset Structure

### Data Instances
Each data instance corresponds to a paraphrase, e.g.:
```
{ 
    'paraphrase_set_id': '1483',  
    'sentence_id': '5778896',
    'paraphrase': 'Ɣremt adlis-a.', 
    'lists': ['7546'], 
    'tags': [''],
    'language': 'ber'
}
```

### Data Fields
Each dialogue instance has the following fields:
- `paraphrase_set_id`:  a running number that groups together all sentences that are considered paraphrases of each
 other
- `sentence_id`: OPUS sentence id
- `paraphrase`: Sentential paraphrase in a given language for a given paraphrase_set_id
- `lists`: Contributors can add sentences to list in order to specify the original source of the data
- `tags`: Indicates morphological or phonological properties of the sentence when available
- `language`: Language identifier, one of the 73 languages that belong to this dataset.

### Data Splits

The dataset is having a single `train` split, contains a total of 1.9 million sentences, with 200 – 250 000
 sentences per language

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

Creative Commons Attribution 2.0 Generic

### Citation Information

```
@dataset{scherrer_yves_2020_3707949,
  author       = {Scherrer, Yves},
  title        = {{TaPaCo: A Corpus of Sentential Paraphrases for 73 Languages}},
  month        = mar,
  year         = 2020,
  publisher    = {Zenodo},
  version      = {1.0},
  doi          = {10.5281/zenodo.3707949},
  url          = {https://doi.org/10.5281/zenodo.3707949}
}
```

### Contributions

Thanks to [@pacman100](https://github.com/pacman100) for adding this dataset.
