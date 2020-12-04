---
annotations_creators:
- expert-generated
language_creators:
- found
languages:
- en
licenses:
- cc-by-sa-3.0
multilinguality:
- monolingual
size_categories:
- 100K<n<1M
source_datasets:
- original
task_categories:
- conditional-text-generation
task_ids:
- table-to-text
---

# Dataset Card Creation Guide

## Table of Contents
- [Dataset Description](#dataset-description)
  - [Dataset Summary](#dataset-summary)
  - [Supported Tasks](#supported-tasks-and-leaderboards)
  - [Languages](#languages)
- [Dataset Structure](#dataset-structure)
  - [Data Instances](#data-instances)
  - [Data Fields](#data-instances)
  - [Data Splits](#data-instances)
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

## Dataset Description

- **Homepage:** None
- **Repository:** https://github.com/google-research-datasets/ToTTo
- **Paper:** https://arxiv.org/abs/2004.14373
- **Leaderboard:** https://github.com/google-research-datasets/ToTTo#leaderboard
- **Point of Contact:** totto@google.com

### Dataset Summary

[More Information Needed]

### Supported Tasks and Leaderboards

[More Information Needed]

### Languages

[More Information Needed]

## Dataset Structure

### Data Instances

```
DatasetDict({
    train: Dataset({
        features: ['id', 'table_page_title', 'table_webpage_url', 'table_section_title', 'table_section_text', 'table', 'highlighted_cells', 'example_id', 'sentence_annotations', 'overlap_subset'],
        num_rows: 120761
    })
    validation: Dataset({
        features: ['id', 'table_page_title', 'table_webpage_url', 'table_section_title', 'table_section_text', 'table', 'highlighted_cells', 'example_id', 'sentence_annotations', 'overlap_subset'],
        num_rows: 7700
    })
    test: Dataset({
        features: ['id', 'table_page_title', 'table_webpage_url', 'table_section_title', 'table_section_text', 'table', 'highlighted_cells', 'example_id', 'sentence_annotations', 'overlap_subset'],
        num_rows: 7700
    })
})
```

### Data Fields

A sample training set is provided below

```
{'example_id': '1762238357686640028',
 'highlighted_cells': [[13, 2]],
 'id': 0,
 'overlap_subset': 'none',
 'sentence_annotations': {'final_sentence': ['A Favorita is the telenovela aired in the 9 pm timeslot.'],
  'original_sentence': ['It is also the first telenovela by the writer to air in the 9 pm timeslot.'],
  'sentence_after_ambiguity': ['A Favorita is the telenovela aired in the 9 pm timeslot.'],
  'sentence_after_deletion': ['It is the telenovela air in the 9 pm timeslot.']},
 'table': [[{'column_span': 1, 'is_header': True, 'row_span': 1, 'value': '#'},
   {'column_span': 1, 'is_header': True, 'row_span': 1, 'value': 'Run'},
   {'column_span': 1, 'is_header': True, 'row_span': 1, 'value': 'Title'},
   {'column_span': 1, 'is_header': True, 'row_span': 1, 'value': 'Chapters'},
   {'column_span': 1, 'is_header': True, 'row_span': 1, 'value': 'Author'},
   {'column_span': 1, 'is_header': True, 'row_span': 1, 'value': 'Director'},
   {'column_span': 1,
    'is_header': True,
    'row_span': 1,
    'value': 'Ibope Rating'}],
  [{'column_span': 1, 'is_header': False, 'row_span': 1, 'value': '59'},
   {'column_span': 1,
    'is_header': False,
    'row_span': 1,
    'value': 'June 5, 2000— February 2, 2001'},
   {'column_span': 1,
    'is_header': False,
    'row_span': 1,
    'value': 'Laços de Família'},
   {'column_span': 1, 'is_header': False, 'row_span': 1, 'value': '209'},
   {'column_span': 1,
    'is_header': False,
    'row_span': 1,
    'value': 'Manoel Carlos'},
   {'column_span': 1,
    'is_header': False,
    'row_span': 1,
    'value': 'Ricardo Waddington'},
   {'column_span': 1, 'is_header': False, 'row_span': 1, 'value': '44.9'}],
  [{'column_span': 1, 'is_header': False, 'row_span': 1, 'value': '60'},
   {'column_span': 1,
    'is_header': False,
    'row_span': 1,
    'value': 'February 5, 2001— September 28, 2001'},
   {'column_span': 1,
    'is_header': False,
    'row_span': 1,
    'value': 'Porto dos Milagres'},
   {'column_span': 1, 'is_header': False, 'row_span': 1, 'value': '203'},
   {'column_span': 1,
    'is_header': False,
    'row_span': 1,
    'value': 'Aguinaldo Silva Ricardo Linhares'},
   {'column_span': 1,
    'is_header': False,
    'row_span': 1,
    'value': 'Marcos Paulo Simões'},
   {'column_span': 1, 'is_header': False, 'row_span': 1, 'value': '44.6'}],
  [{'column_span': 1, 'is_header': False, 'row_span': 1, 'value': '61'},
   {'column_span': 1,
    'is_header': False,
    'row_span': 1,
    'value': 'October 1, 2001— June 14, 2002'},
   {'column_span': 1, 'is_header': False, 'row_span': 1, 'value': 'O Clone'},
   {'column_span': 1, 'is_header': False, 'row_span': 1, 'value': '221'},
   {'column_span': 1,
    'is_header': False,
    'row_span': 1,
    'value': 'Glória Perez'},
   {'column_span': 1,
    'is_header': False,
    'row_span': 1,
    'value': 'Jayme Monjardim'},
   {'column_span': 1, 'is_header': False, 'row_span': 1, 'value': '47.0'}],
  [{'column_span': 1, 'is_header': False, 'row_span': 1, 'value': '62'},
   {'column_span': 1,
    'is_header': False,
    'row_span': 1,
    'value': 'June 17, 2002— February 14, 2003'},
   {'column_span': 1, 'is_header': False, 'row_span': 1, 'value': 'Esperança'},
   {'column_span': 1, 'is_header': False, 'row_span': 1, 'value': '209'},
   {'column_span': 1,
    'is_header': False,
    'row_span': 1,
    'value': 'Benedito Ruy Barbosa'},
   {'column_span': 1,
    'is_header': False,
    'row_span': 1,
    'value': 'Luiz Fernando'},
   {'column_span': 1, 'is_header': False, 'row_span': 1, 'value': '37.7'}],
  [{'column_span': 1, 'is_header': False, 'row_span': 1, 'value': '63'},
   {'column_span': 1,
    'is_header': False,
    'row_span': 1,
    'value': 'February 17, 2003— October 10, 2003'},
   {'column_span': 1,
    'is_header': False,
    'row_span': 1,
    'value': 'Mulheres Apaixonadas'},
   {'column_span': 1, 'is_header': False, 'row_span': 1, 'value': '203'},
   {'column_span': 1,
    'is_header': False,
    'row_span': 1,
    'value': 'Manoel Carlos'},
   {'column_span': 1,
    'is_header': False,
    'row_span': 1,
    'value': 'Ricardo Waddington'},
   {'column_span': 1, 'is_header': False, 'row_span': 1, 'value': '46.6'}],
  [{'column_span': 1, 'is_header': False, 'row_span': 1, 'value': '64'},
   {'column_span': 1,
    'is_header': False,
    'row_span': 1,
    'value': 'October 13, 2003— June 25, 2004'},
   {'column_span': 1,
    'is_header': False,
    'row_span': 1,
    'value': 'Celebridade'},
   {'column_span': 1, 'is_header': False, 'row_span': 1, 'value': '221'},
   {'column_span': 1,
    'is_header': False,
    'row_span': 1,
    'value': 'Gilberto Braga'},
   {'column_span': 1,
    'is_header': False,
    'row_span': 1,
    'value': 'Dennis Carvalho'},
   {'column_span': 1, 'is_header': False, 'row_span': 1, 'value': '46.0'}],
  [{'column_span': 1, 'is_header': False, 'row_span': 1, 'value': '65'},
   {'column_span': 1,
    'is_header': False,
    'row_span': 1,
    'value': 'June 28, 2004— March 11, 2005'},
   {'column_span': 1,
    'is_header': False,
    'row_span': 1,
    'value': 'Senhora do Destino'},
   {'column_span': 1, 'is_header': False, 'row_span': 1, 'value': '221'},
   {'column_span': 1,
    'is_header': False,
    'row_span': 1,
    'value': 'Aguinaldo Silva'},
   {'column_span': 1, 'is_header': False, 'row_span': 1, 'value': 'Wolf Maya'},
   {'column_span': 1, 'is_header': False, 'row_span': 1, 'value': '50.4'}],
  [{'column_span': 1, 'is_header': False, 'row_span': 1, 'value': '66'},
   {'column_span': 1,
    'is_header': False,
    'row_span': 1,
    'value': 'March 14, 2005— November 4, 2005'},
   {'column_span': 1, 'is_header': False, 'row_span': 1, 'value': 'América'},
   {'column_span': 1, 'is_header': False, 'row_span': 1, 'value': '203'},
   {'column_span': 1,
    'is_header': False,
    'row_span': 1,
    'value': 'Glória Perez'},
   {'column_span': 1,
    'is_header': False,
    'row_span': 1,
    'value': 'Jayme Monjardim Marcos Schechtman'},
   {'column_span': 1, 'is_header': False, 'row_span': 1, 'value': '49.4'}],
  [{'column_span': 1, 'is_header': False, 'row_span': 1, 'value': '67'},
   {'column_span': 1,
    'is_header': False,
    'row_span': 1,
    'value': 'November 7, 2005— July 7, 2006'},
   {'column_span': 1, 'is_header': False, 'row_span': 1, 'value': 'Belíssima'},
   {'column_span': 1, 'is_header': False, 'row_span': 1, 'value': '209'},
   {'column_span': 1,
    'is_header': False,
    'row_span': 1,
    'value': 'Sílvio de Abreu'},
   {'column_span': 1,
    'is_header': False,
    'row_span': 1,
    'value': 'Denise Saraceni'},
   {'column_span': 1, 'is_header': False, 'row_span': 1, 'value': '48.5'}],
  [{'column_span': 1, 'is_header': False, 'row_span': 1, 'value': '68'},
   {'column_span': 1,
    'is_header': False,
    'row_span': 1,
    'value': 'July 10, 2006— March 2, 2007'},
   {'column_span': 1,
    'is_header': False,
    'row_span': 1,
    'value': 'Páginas da Vida'},
   {'column_span': 1, 'is_header': False, 'row_span': 1, 'value': '203'},
   {'column_span': 1,
    'is_header': False,
    'row_span': 1,
    'value': 'Manoel Carlos'},
   {'column_span': 1,
    'is_header': False,
    'row_span': 1,
    'value': 'Jayme Monjardim'},
   {'column_span': 1, 'is_header': False, 'row_span': 1, 'value': '46.8'}],
  [{'column_span': 1, 'is_header': False, 'row_span': 1, 'value': '69'},
   {'column_span': 1,
    'is_header': False,
    'row_span': 1,
    'value': 'March 5, 2007— September 28, 2007'},
   {'column_span': 1,
    'is_header': False,
    'row_span': 1,
    'value': 'Paraíso Tropical'},
   {'column_span': 1, 'is_header': False, 'row_span': 1, 'value': '179'},
   {'column_span': 1,
    'is_header': False,
    'row_span': 1,
    'value': 'Gilberto Braga Ricardo Linhares'},
   {'column_span': 1,
    'is_header': False,
    'row_span': 1,
    'value': 'Dennis Carvalho'},
   {'column_span': 1, 'is_header': False, 'row_span': 1, 'value': '42.8'}],
  [{'column_span': 1, 'is_header': False, 'row_span': 1, 'value': '70'},
   {'column_span': 1,
    'is_header': False,
    'row_span': 1,
    'value': 'October 1, 2007— May 31, 2008'},
   {'column_span': 1,
    'is_header': False,
    'row_span': 1,
    'value': 'Duas Caras'},
   {'column_span': 1, 'is_header': False, 'row_span': 1, 'value': '210'},
   {'column_span': 1,
    'is_header': False,
    'row_span': 1,
    'value': 'Aguinaldo Silva'},
   {'column_span': 1, 'is_header': False, 'row_span': 1, 'value': 'Wolf Maya'},
   {'column_span': 1, 'is_header': False, 'row_span': 1, 'value': '41.1'}],
  [{'column_span': 1, 'is_header': False, 'row_span': 1, 'value': '71'},
   {'column_span': 1,
    'is_header': False,
    'row_span': 1,
    'value': 'June 2, 2008— January 16, 2009'},
   {'column_span': 1,
    'is_header': False,
    'row_span': 1,
    'value': 'A Favorita'},
   {'column_span': 1, 'is_header': False, 'row_span': 1, 'value': '197'},
   {'column_span': 1,
    'is_header': False,
    'row_span': 1,
    'value': 'João Emanuel Carneiro'},
   {'column_span': 1,
    'is_header': False,
    'row_span': 1,
    'value': 'Ricardo Waddington'},
   {'column_span': 1, 'is_header': False, 'row_span': 1, 'value': '39.5'}],
  [{'column_span': 1, 'is_header': False, 'row_span': 1, 'value': '72'},
   {'column_span': 1,
    'is_header': False,
    'row_span': 1,
    'value': 'January 19, 2009— September 11, 2009'},
   {'column_span': 1,
    'is_header': False,
    'row_span': 1,
    'value': 'Caminho das Índias'},
   {'column_span': 1, 'is_header': False, 'row_span': 1, 'value': '203'},
   {'column_span': 1,
    'is_header': False,
    'row_span': 1,
    'value': 'Glória Perez'},
   {'column_span': 1,
    'is_header': False,
    'row_span': 1,
    'value': 'Marcos Schechtman'},
   {'column_span': 1, 'is_header': False, 'row_span': 1, 'value': '38.8'}],
  [{'column_span': 1, 'is_header': False, 'row_span': 1, 'value': '73'},
   {'column_span': 1,
    'is_header': False,
    'row_span': 1,
    'value': 'September 14, 2009— May 14, 2010'},
   {'column_span': 1,
    'is_header': False,
    'row_span': 1,
    'value': 'Viver a Vida'},
   {'column_span': 1, 'is_header': False, 'row_span': 1, 'value': '209'},
   {'column_span': 1,
    'is_header': False,
    'row_span': 1,
    'value': 'Manoel Carlos'},
   {'column_span': 1,
    'is_header': False,
    'row_span': 1,
    'value': 'Jayme Monjardim'},
   {'column_span': 1, 'is_header': False, 'row_span': 1, 'value': '35.6'}]],
 'table_page_title': 'List of 8/9 PM telenovelas of Rede Globo',
 'table_section_text': '',
 'table_section_title': '2000s',
 'table_webpage_url': 'http://en.wikipedia.org/wiki/List_of_8/9_PM_telenovelas_of_Rede_Globo'}
```

Please note that in test set sentence annotations are not available and thus values inside `sentence_annotations` can be safely ignored.

### Data Splits

[More Information Needed]
## Dataset Creation

### Curation Rationale

[More Information Needed]

### Source Data

[More Information Needed]

#### Initial Data Collection and Normalization

[More Information Needed]

#### Who are the source language producers?

[More Information Needed]

### Annotations

[More Information Needed]

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

[More Information Needed]

### Citation Information

[More Information Needed]
