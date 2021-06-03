---
annotations_creators:
- found
language_creators:
- found
languages:
- tr
licenses:
- unknown
multilinguality:
- monolingual
size_categories:
- 10K<n<100K
source_datasets:
- original
task_categories:
- text-classification
task_ids:
- sentiment-classification
- sentiment-scoring
paperswithcode_id: null
---

# Dataset Card for TurkishMovieSentiment: This dataset contains turkish movie reviews.

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

- **Homepage:** [https://www.kaggle.com/mustfkeskin/turkish-movie-sentiment-analysis-dataset/tasks](https://www.kaggle.com/mustfkeskin/turkish-movie-sentiment-analysis-dataset/tasks)
- **Point of Contact:** [Mustafa Keskin](https://www.linkedin.com/in/mustfkeskin/)

### Dataset Summary

This data set is a dataset from kaggle consisting of Turkish movie reviews and scored between 0-5.

### Languages

The dataset is based on Turkish.

## Dataset Structure

### Data Instances

**Example 1:**

**Comment:** Jean Reno denince zaten leon filmi gelir akla izlemeyen kalmamıştır ama kaldıysada ee ne duruyorsun hemen izle :),

**Film_name:** Sevginin Gücü,

**Point:** 5,0

**Example 2:**

**Comment:** Bence güzel bi film olmush.İzlenmeli.İnsana şükretmek gerektini hatırlatıyor.Ama cok da poh pohlanacak bi sey yapmamıslar,

**Film_name:** Cinderella Man,

**Point:** 2,5

### Data Fields

- **comment**(string) : Contatins turkish movie review
- **film_name**(string) : Film name in Turkish.
- **point**(float) : [0-5] floating point

### Data Splits

It is not divided into Train set and Test set.

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

The dataset does not contain any additional annotations.

#### Annotation process

[More Information Needed]

#### Who are the annotators?

[More Information Needed]

### Personal and Sensitive Information

[More Information Needed]

## Considerations for Using the Data

### Discussion of Social Impact and Biases

[More Information Needed]

### Other Known Limitations

[More Information Needed]

## Additional Information

### Dataset Curators

The dataset was created by [Mustafa Keskin](https://www.linkedin.com/in/mustfkeskin/).  

### Licensing Information

The data is under the [CC0: Public Domain](https://creativecommons.org/publicdomain/zero/1.0/)

### Citation Information

[More Information Needed]

### Contributions

Thanks to [@yavuzKomecoglu](https://github.com/yavuzKomecoglu) for adding this dataset.