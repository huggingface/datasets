---
annotations_creators:
- no-annotation
language_creators:
- crowdsourced
- expert-generated
languages:
- ang
- ar
- as
- az
- ban
- be
- bg
- bn
- br
- bs
- ca
- cs
- cy
- da
- de
- el
- en
- eo
- es
- et
- eu
- fa
- fi
- fo
- fr
- gl
- gu
- he
- hi
- hr
- ht
- hu
- hy
- id
- is
- it
- ja
- jv
- kn
- ko
- la
- li
- lij
- lt
- mk
- ml
- mr
- nap
- nl
- "no"
- or
- pa
- pl
- pms
- pt
- ro
- ru
- sa
- sah
- sk
- sl
- sr
- sv
- ta
- te
- th
- tr
- uk
- vec
- vi
- wa
- yi
- zh
licenses:
- cc-by-sa-3.0
- gfdl-1.3-or-later
multilinguality:
- multilingual
pretty_name: Wikisource
paperswithcode_id: null
size_categories:
- unknown
source_datasets:
- original
task_categories:
- sequence-modeling
task_ids:
- language-modeling
---

# Dataset Card for Wikisource

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

- **Homepage:** https://dumps.wikimedia.org
- **Repository:**
- **Paper:**
- **Leaderboard:**
- **Point of Contact:**

### Dataset Summary

Wikisource dataset contains cleaned primary source texts in any language.

The dataset is built from the Wikipedia dump
(https://dumps.wikimedia.org/) with one split per language. Each example
contains the content of one full Wikisource article with cleaning to strip
markdown and unwanted sections (references, etc.).

The articles are parsed using the ``mwparserfromhell`` tool.

To load this dataset you need to install Apache Beam and ``mwparserfromhell`` first:

```
pip install apache_beam mwparserfromhell
```

Then can load any subset of Wikisource per language and per date this way:

```python
from datasets import load_dataset

load_dataset("wikisource", language="sw", date="20220120")
```

You can find the full list of languages and dates [here](https://dumps.wikimedia.org/backup-index-bydb.html).

### Supported Tasks and Leaderboards

The dataset is generally used for Language Modeling.

### Languages

You can find the list of languages [here](https://meta.wikimedia.org/wiki/Wikisource#List_of_Wikisources).

## Dataset Structure

### Data Instances

```
{
  "title": "Tirant lo Blanch (1873-1905)",
  "text": "A honor lahor e gloria de nostre senyor deu Jesu christ e de la gloriosa sacratissima uerge Maria mare sua senyora nostra comença la letra del present libre apellat Tirant lo blanch, dirigida per mossen Joanot martorell caualler al serenissimo princep don Ferrando de portogal...",
}
```

### Data Fields

- `title`: Title of the source text.
- `text`: Text content of the source text.

### Data Splits

The datasets contains a single "train" split.

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

https://dumps.wikimedia.org/legal.html

Except as discussed below, all original textual content is licensed under the
[GNU Free Documentation License](https://www.gnu.org/licenses/fdl-1.3.html) (GFDL) and
the [Creative Commons Attribution-Share-Alike 3.0 License](https://creativecommons.org/licenses/by-sa/3.0/).
Some text may be available only under the Creative Commons license; see our Terms of Use for details. Text written by
some authors may be released under additional licenses or into the public domain.

### Citation Information

```
@ONLINE {wikidump,
    author = "Wikimedia Foundation",
    title  = "Wikimedia Downloads",
    url    = "https://dumps.wikimedia.org"
}
```

### Contributions

Thanks to [@albertvillanova](https://github.com/albertvillanova) for adding this dataset.
