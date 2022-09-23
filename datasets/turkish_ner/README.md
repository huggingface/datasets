---
annotations_creators:
- machine-generated
language_creators:
- expert-generated
language:
- tr
license:
- cc-by-4.0
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
paperswithcode_id: null
pretty_name: TurkishNer
dataset_info:
  features:
  - name: id
    dtype: string
  - name: tokens
    sequence: string
  - name: domain
    dtype:
      class_label:
        names:
          0: architecture
          1: basketball
          2: book
          3: business
          4: education
          5: fictional_universe
          6: film
          7: food
          8: geography
          9: government
          10: law
          11: location
          12: military
          13: music
          14: opera
          15: organization
          16: people
          17: religion
          18: royalty
          19: soccer
          20: sports
          21: theater
          22: time
          23: travel
          24: tv
  - name: ner_tags
    sequence:
      class_label:
        names:
          0: O
          1: B-PERSON
          2: I-PERSON
          3: B-ORGANIZATION
          4: I-ORGANIZATION
          5: B-LOCATION
          6: I-LOCATION
          7: B-MISC
          8: I-MISC
  splits:
  - name: train
    num_bytes: 177658278
    num_examples: 532629
  download_size: 204393976
  dataset_size: 177658278
---


# Dataset Card for turkish_ner

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

- **Homepage:** http://arxiv.org/abs/1702.02363
- **Repository:** [Needs More Information]
- **Paper:** http://arxiv.org/abs/1702.02363
- **Leaderboard:** [Needs More Information]
- **Point of Contact:** erayyildiz@ktu.edu.tr

### Dataset Summary

Automatically annotated Turkish corpus for named entity recognition and text categorization using large-scale gazetteers. The constructed gazetteers contains approximately 300K entities with thousands of fine-grained entity types under 25 different domains.

### Supported Tasks and Leaderboards

[Needs More Information]

### Languages

Turkish

## Dataset Structure

### Data Instances

[More Information Needed]

### Data Fields

[More Information Needed]

### Data Splits

There's only the training set.

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

H. Bahadir Sahin, Caglar Tirkaz, Eray Yildiz, Mustafa Tolga Eren and Omer Ozan Sonmez

### Licensing Information

Creative Commons Attribution 4.0 International

### Citation Information

@InProceedings@article{DBLP:journals/corr/SahinTYES17,
  author    = {H. Bahadir Sahin and
               Caglar Tirkaz and
               Eray Yildiz and
               Mustafa Tolga Eren and
               Omer Ozan Sonmez},
  title     = {Automatically Annotated Turkish Corpus for Named Entity Recognition
               and Text Categorization using Large-Scale Gazetteers},
  journal   = {CoRR},
  volume    = {abs/1702.02363},
  year      = {2017},
  url       = {http://arxiv.org/abs/1702.02363},
  archivePrefix = {arXiv},
  eprint    = {1702.02363},
  timestamp = {Mon, 13 Aug 2018 16:46:36 +0200},
  biburl    = {https://dblp.org/rec/journals/corr/SahinTYES17.bib},
  bibsource = {dblp computer science bibliography, https://dblp.org}
}

### Contributions

Thanks to [@merveenoyan](https://github.com/merveenoyan) for adding this dataset.