---
annotations_creators:
- no-annotation
language_creators:
- found
languages:
- en
licenses:
- other-
multilinguality:
- monolingual
pretty_name: The Pile
size_categories:
- unknown
source_datasets:
- original
task_categories:
- sequence-modeling
task_ids:
- language-modeling
---

# Dataset Card for The Pile

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

- **Homepage:** https://pile.eleuther.ai/
- **Repository:** https://github.com/EleutherAI/the-pile
- **Paper:** [The Pile: An 800GB Dataset of Diverse Text for Language Modeling](https://arxiv.org/abs/2101.00027)
- **Leaderboard:**
- **Point of Contact:** [EleutherAI](mailto:contact@eleuther.ai)

### Dataset Summary

The Pile is a 825 GiB diverse, open source language modelling data set that consists of 22 smaller, high-quality
datasets combined together.


### Supported Tasks and Leaderboards

[More Information Needed]

### Languages

This dataset is in English (`EN`).

## Dataset Structure

### Data Instances

#### all
```
{
  'meta': {'pile_set_name': 'Pile-CC'},
  'text': 'It is done, and submitted. You can play “Survival of the Tastiest” on Android, and on the web. Playing on...'
}
```

#### free_law
```
{
  'meta':  "{'case_jurisdiction': 'scotus.tar.gz', 'case_ID': '110921.json','date_created': '2010-04-28T17:12:49Z'}",
  'text': '\n461 U.S. 238 (1983)\nOLIM ET AL.\nv.\nWAKINEKONA\nNo. 81-1581.\nSupreme Court of United States.\nArgued...'
}
```

#### pubmed_central
```
{
  'meta': "{id': 'PMC5595690'}",
  'text': 'Introduction {#acel12642-sec-0001}\n============\n\nAlzheimer\\\'s disease (AD), the most common cause of...'
}
```

#### uspto
```
{
  'text': "1. Field of the Invention\nIn an extensive plant breeding program, Grant Merrill, originator and now deceased, originated a large number of new and distinct varieties of fruit trees, and which included the herein-claimed variety of peach tree. Such plant breeding program was undertaken in originator's experimental orchard located near Exeter, Tulare County, Calif.\n2. Prior Varieties\nAmong the existent varieties of peach trees which were known to originator, particular reference is made to Gemfree (U.S. Plant Pat. No. 1,409) and June Lady (U.S. Plant Pat. No. 3,022) hereinafter mentioned for the purpose of comparison.",
  'meta': "{'bibliographic_information': {'Patent Number': 'PP0049700', 'Series Code': '6', 'Application Number': '2845415', 'Application Type': '6', 'Art unit': '337', 'Application Filing Date': '19810720', 'Title of Invention': 'Peach tree (A3-10)', 'Issue Date': '19830104', 'Number of Claims': '1', 'Exemplary Claim Number(s)': '1', 'Primary Examiner': 'Bagwill; Robert E.', 'Number of Drawing Sheets': '1', 'Number of figures': '1'}, 'source_file': 'https://bulkdata.uspto.gov/data/patent/grant/redbook/fulltext/1983/pftaps19830104_wk01.zip', 'abstract': 'A peach tree which is large, vigorous, and spreading; foliated with large, lanceolate leaves having a finely serrate margin, a petiole of medium length and thickness, and medium size, reniform glands; blooms from medium size, conic, plump, pubescent buds; the flowers, medium in blooming period compared with other varieties, being of medium size, and pink; and is a regular and very productive bearer of medium but variable size, round truncate, clingstone fruit having yellow skin substantially overspread with red, yellow flesh mottled with red adjacent the skin, and an amber stone.', 'classifications': [{'OCL': ['Plt', '43'], 'EDF': ['3'], 'ICL': ['A01H', '503'], 'FSC': ['Plt'], 'FSS': ['43']}], 'inventors': [{'inventor name': 'Merrill, deceased; Grant', 'Street': '325 Breese Ave.', 'City': 'late of Red Bluff', 'State': 'CA'}, {'inventor name': 'Merrill, executrix; by Lucile B.', 'Street': '325 Breese Ave.', 'City': 'Red Bluff', 'State': 'CA', 'Zip code': '96080'}]}"
}
```

### Data Fields

#### all

- `text` (str): Text.
- `meta` (dict): Metadata of the data instance, with keys:
  - pile_set_name: Name of the subset.

#### free_law

- `text` (str): Text.
- `meta` (str): Metadata of the data instance, with: case_ID, case_jurisdiction, date_created.

#### pubmed_central

- `text` (str): Text.
- `meta` (str): Metadata of the data instance, with: ID of the data instance.

#### uspto

- `text` (str): Text.
- `meta` (str): Metadata of the data instance, with: bibliographic_information, source_file, abstract, classifications, 
  inventors.

### Data Splits

The "all" configuration is composed of 3 splits: train, validation and test.

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

Please refer to the specific license depending on the subset you use:
- PubMed Central: [MIT License](https://github.com/EleutherAI/pile-pubmedcentral/blob/master/LICENSE)

### Citation Information

```
@misc{gao2020pile,
      title={The Pile: An 800GB Dataset of Diverse Text for Language Modeling},
      author={Leo Gao and Stella Biderman and Sid Black and Laurence Golding and Travis Hoppe and Charles Foster and Jason Phang and Horace He and Anish Thite and Noa Nabeshima and Shawn Presser and Connor Leahy},
      year={2020},
      eprint={2101.00027},
      archivePrefix={arXiv},
      primaryClass={cs.CL}
}
```

### Contributions

Thanks to [@github-username](https://github.com/<github-username>) for adding this dataset.
