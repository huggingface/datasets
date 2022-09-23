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
- extended|other-turkish_ner
task_categories:
- token-classification
task_ids:
- named-entity-recognition
paperswithcode_id: null
pretty_name: TurkishShrinkedNer
dataset_info:
  features:
  - name: id
    dtype: string
  - name: tokens
    sequence: string
  - name: ner_tags
    sequence:
      class_label:
        names:
          0: O
          1: B-academic
          2: I-academic
          3: B-academic_person
          4: I-academic_person
          5: B-aircraft
          6: I-aircraft
          7: B-album_person
          8: I-album_person
          9: B-anatomy
          10: I-anatomy
          11: B-animal
          12: I-animal
          13: B-architect_person
          14: I-architect_person
          15: B-capital
          16: I-capital
          17: B-chemical
          18: I-chemical
          19: B-clothes
          20: I-clothes
          21: B-country
          22: I-country
          23: B-culture
          24: I-culture
          25: B-currency
          26: I-currency
          27: B-date
          28: I-date
          29: B-food
          30: I-food
          31: B-genre
          32: I-genre
          33: B-government
          34: I-government
          35: B-government_person
          36: I-government_person
          37: B-language
          38: I-language
          39: B-location
          40: I-location
          41: B-material
          42: I-material
          43: B-measure
          44: I-measure
          45: B-medical
          46: I-medical
          47: B-military
          48: I-military
          49: B-military_person
          50: I-military_person
          51: B-nation
          52: I-nation
          53: B-newspaper
          54: I-newspaper
          55: B-organization
          56: I-organization
          57: B-organization_person
          58: I-organization_person
          59: B-person
          60: I-person
          61: B-production_art_music
          62: I-production_art_music
          63: B-production_art_music_person
          64: I-production_art_music_person
          65: B-quantity
          66: I-quantity
          67: B-religion
          68: I-religion
          69: B-science
          70: I-science
          71: B-shape
          72: I-shape
          73: B-ship
          74: I-ship
          75: B-software
          76: I-software
          77: B-space
          78: I-space
          79: B-space_person
          80: I-space_person
          81: B-sport
          82: I-sport
          83: B-sport_name
          84: I-sport_name
          85: B-sport_person
          86: I-sport_person
          87: B-structure
          88: I-structure
          89: B-subject
          90: I-subject
          91: B-tech
          92: I-tech
          93: B-train
          94: I-train
          95: B-vehicle
          96: I-vehicle
  splits:
  - name: train
    num_bytes: 200728389
    num_examples: 614515
  download_size: 0
  dataset_size: 200728389
---

# Dataset Card for turkish_shrinked_ner

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

- **Homepage:** https://www.kaggle.com/behcetsenturk/shrinked-twnertc-turkish-ner-data-by-kuzgunlar
- **Repository:** [Needs More Information]
- **Paper:** [Needs More Information]
- **Leaderboard:** [Needs More Information]
- **Point of Contact:** https://www.kaggle.com/behcetsenturk

### Dataset Summary

Shrinked processed version (48 entity type) of the turkish_ner.

Original turkish_ner dataset: Automatically annotated Turkish corpus for named entity recognition and text categorization using large-scale gazetteers. The constructed gazetteers contains approximately 300K entities with thousands of fine-grained entity types under 25 different domains.

Shrinked entity types are: academic, academic_person, aircraft, album_person, anatomy, animal, architect_person, capital, chemical, clothes, country, culture, currency, date, food, genre, government, government_person, language, location, material, measure, medical, military, military_person, nation, newspaper, organization, organization_person, person, production_art_music, production_art_music_person, quantity, religion, science, shape, ship, software, space, space_person, sport, sport_name, sport_person, structure, subject, tech, train, vehicle

### Supported Tasks and Leaderboards

[Needs More Information]

### Languages

Turkish

## Dataset Structure

### Data Instances

[Needs More Information]

### Data Fields

[Needs More Information]

### Data Splits

There's only the training set.

## Dataset Creation

### Curation Rationale

[Needs More Information]

### Source Data

#### Initial Data Collection and Normalization

[Needs More Information]

#### Who are the source language producers?

[Needs More Information]

### Annotations

#### Annotation process

[Needs More Information]

#### Who are the annotators?

[Needs More Information]

### Personal and Sensitive Information

[Needs More Information]

## Considerations for Using the Data

### Social Impact of Dataset

[Needs More Information]

### Discussion of Biases

[Needs More Information]

### Other Known Limitations

[Needs More Information]

## Additional Information

### Dataset Curators

Behcet Senturk

### Licensing Information

Creative Commons Attribution 4.0 International

### Citation Information

[Needs More Information]

### Contributions

Thanks to [@bhctsntrk](https://github.com/bhctsntrk) for adding this dataset.