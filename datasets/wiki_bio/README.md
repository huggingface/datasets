---
annotations_creators:
- found
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
- explanation-generation
- table-to-text
paperswithcode_id: wikibio
---

# Dataset Card for [Dataset Name]

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

- **Repository:** https://github.com/DavidGrangier/wikipedia-biography-dataset
- **Paper:** https://arxiv.org/pdf/1603.07771.pdf
- **GoogleDrive:** https://drive.google.com/uc?export=download&id=1L7aoUXzHPzyzQ0ns4ApBbYepsjFOtXil

### Dataset Summary

This Dataset contains 728321 biographies extracted from Wikipedia containing the first paragraph of the biography and the tabular infobox.
### Supported Tasks and Leaderboards

The main purpose of this dataset is developing text generation models.

### Languages

English.

## Dataset Structure

### Data Instances

[More Information Needed]

### Data Fields

The structure of a single sample is the following:
```json
{
   "input_text":{
      "context":"pope michael iii of alexandria\n",
      "table":{
         "column_header":[
            "type",
            "ended",
            "death_date",
            "title",
            "enthroned",
            "name",
            "buried",
            "religion",
            "predecessor",
            "nationality",
            "article_title",
            "feast_day",
            "birth_place",
            "residence",
            "successor"
         ],
         "content":[
            "pope",
            "16 march 907",
            "16 march 907",
            "56th of st. mark pope of alexandria & patriarch of the see",
            "25 april 880",
            "michael iii of alexandria",
            "monastery of saint macarius the great",
            "coptic orthodox christian",
            "shenouda i",
            "egyptian",
            "pope michael iii of alexandria\n",
            "16 -rrb- march -lrb- 20 baramhat in the coptic calendar",
            "egypt",
            "saint mark 's church",
            "gabriel i"
         ],
         "row_number":[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
      }
   },
   "target_text":"pope michael iii of alexandria -lrb- also known as khail iii -rrb- was the coptic pope of alexandria and patriarch of the see of st. mark -lrb- 880 -- 907 -rrb- .\nin 882 , the governor of egypt , ahmad ibn tulun , forced khail to pay heavy contributions , forcing him to sell a church and some attached properties to the local jewish community .\nthis building was at one time believed to have later become the site of the cairo geniza .\n"
}
```
where, in the `"table"` field, all the information of the Wikpedia infobox is stored (the header of the infobox is stored in `"column_header"` and the information in the `"content"` field).
### Data Splits

- Train: 582659 samples.
- Test: 72831 samples.
- Validation: 72831 samples.
## Dataset Creation

### Curation Rationale

[More Information Needed]

### Source Data
This dataset was announced in the paper <em>Neural Text Generation from Structured Data with Application to the Biography Domain</em> [(arxiv link)](https://arxiv.org/pdf/1603.07771.pdf) and is stored both in [this](https://github.com/DavidGrangier/wikipedia-biography-dataset) repo (owned by DavidGrangier) and in [Google Drive](https://drive.google.com/uc?export=download&id=1L7aoUXzHPzyzQ0ns4ApBbYepsjFOtXil) (zipped and mantained by the TensorFlow team).
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

This dataset is ditributed under Creative Comons CC BY-SA 3.0 License.
### Citation Information

For refering the original paper in BibTex format:

```
@article{DBLP:journals/corr/LebretGA16,
  author    = {R{\'{e}}mi Lebret and
               David Grangier and
               Michael Auli},
  title     = {Generating Text from Structured Data with Application to the Biography
               Domain},
  journal   = {CoRR},
  volume    = {abs/1603.07771},
  year      = {2016},
  url       = {http://arxiv.org/abs/1603.07771},
  archivePrefix = {arXiv},
  eprint    = {1603.07771},
  timestamp = {Mon, 13 Aug 2018 16:48:30 +0200},
  biburl    = {https://dblp.org/rec/journals/corr/LebretGA16.bib},
  bibsource = {dblp computer science bibliography, https://dblp.org}
}
```

### Contributions

Thanks to [@alejandrocros](https://github.com/alejandrocros) for adding this dataset.