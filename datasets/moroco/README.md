---
annotations_creators:
- found
language_creators:
- found
language:
- ro
language_bcp47:
- ro-MD
license:
- cc-by-4.0
multilinguality:
- monolingual
size_categories:
- 10K<n<100K
source_datasets:
- original
task_categories:
- text-classification
task_ids:
- topic-classification
paperswithcode_id: moroco
pretty_name: "MOROCO: The Moldavian and Romanian Dialectal Corpus"
---

# Dataset Card for MOROCO

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

- **Homepage:** [Github](https://github.com/butnaruandrei/MOROCO)
- **Repository:** [Github](https://github.com/butnaruandrei/MOROCO)
- **Paper:** [Arxiv](https://arxiv.org/abs/1901.06543)
- **Leaderboard:** [Needs More Information]
- **Point of Contact:** [email](raducu.ionescu@gmail.com)

### Dataset Summary

Introducing MOROCO - The **Mo**ldavian and **Ro**manian Dialectal **Co**rpus. The MOROCO data set contains Moldavian and Romanian samples of text collected from the news domain. The samples belong to one of the following six topics: (0) culture, (1) finance, (2) politics, (3) science, (4) sports, (5) tech. The corpus features a total of 33,564 samples labelled with one of the fore mentioned six categories. We are also including a train/validation/test split with 21,719/5,921/5,924 samples in each subset.

### Supported Tasks and Leaderboards

[LiRo Benchmark and Leaderboard](https://eemlcommunity.github.io/ro_benchmark_leaderboard/site/)

### Languages

The text dataset is in Romanian (`ro`)

## Dataset Structure

### Data Instances

Below we have an example of sample from MOROCO:

```
{'id': , '48482',
 'category': 2, 
 'sample': '“$NE$ cum am spus, nu este un sfârşit de drum . Vom continua lupta cu toate instrumentele şi cu toate mijloacele legale, parlamentare şi civice pe care le avem la dispoziţie . Evident că vom contesta la $NE$ această lege, au anunţat şi colegii de la $NE$ o astfel de contestaţie . Practic trebuie utilizat orice instrument pe care îl identificăm pentru a bloca intrarea în vigoare a acestei legi . Bineînţeles, şi preşedintele are punctul său de vedere . ( . . . ) $NE$ legi sunt împănate de motive de neconstituţionalitate . Colegii mei de la departamentul juridic lucrează în prezent pentru a definitiva textul contestaţiei”, a declarat $NE$ $NE$ citat de news . ro . Senatul a adoptat, marţi, în calitate de for decizional, $NE$ privind statutul judecătorilor şi procurorilor, cu 80 de voturi ”pentru” şi niciun vot ”împotrivă”, în condiţiile în care niciun partid din opoziţie nu a fost prezent în sală .',
}
```

where 48482 is the sample ID, followed by the category ground truth label, and then the text representing the actual content to be classified by topic.

Note: The category label has integer values ranging from 0 to 5.


### Data Fields

- `id`: string, the unique indentifier of a sample
- `category_label`: integer in the range [0, 5]; the category assigned to a sample.
- `sample`: a string, news report to be classified / used in classification.

### Data Splits

The train/validation/test split contains 21,719/5,921/5,924 samples tagged with the category assigned to each sample in the dataset.

## Dataset Creation

### Curation Rationale

The samples are preprocessed in order to eliminate named entities. This is required to prevent classifiers from taking the decision based on features that are not related to the topics. 
For example, named entities that refer to politicians or football players names can provide clues about the topic. For more details, please read the [paper](https://arxiv.org/abs/1901.06543).

### Source Data


#### Data Collection and Normalization

For the data collection, five of the most popular news websites in Romania and the Republic of Moldova were targetted. Given that the data set was obtained through a web scraping technique, all the HTML tags needed to be removed, as well as replace consecutive white spaces with a single space. 

As part of the pre-processing, we remove named entities, such as country names, cities, public figures, etc. The named entities have been replaced with $NE$. The necessity to remove them, comes also from the scope of this dataset: categorization by topic. Thus, the authors decided to remove named entities in order to prevent classifiers from taking the decision based on features that are not truly indicative of the topics. 

#### Who are the source language producers?

The original text comes from news websites from Romania and the Republic of Moldova.

### Annotations

#### Annotation process

As mentioned above, MOROCO is composed of text samples from the top five most popular news websites in Romania and the Republic of Moldova, respectively. Since there are topic tags in the news websites targetd, the text samples can be automatically labeled with the corresponding category.

#### Who are the annotators?

N/A

### Personal and Sensitive Information

The textual data collected for MOROCO consists in news reports freely available on the Internet and of public interest. 
To the best of authors' knowledge, there is no personal or sensitive information that needed to be considered in the said textual inputs collected.

## Considerations for Using the Data

### Social Impact of Dataset

This dataset is part of an effort to encourage text classification research in languages other than English. Such work increases the accessibility of natural language technology to more regions and cultures. 
In the past three years there was a growing interest for studying Romanian from a Computational Linguistics perspective. However, we are far from having enough datasets and resources in this particular language.

### Discussion of Biases

The data included in MOROCO spans a well defined time frame of a few years. Part of the topics that were of interest then in the news landscape, might not show up nowadays or a few years from now in news websites.

### Other Known Limitations

[Needs More Information]

## Additional Information

### Dataset Curators

Published and managed by Radu Tudor Ionescu and Andrei Butnaru.

### Licensing Information

CC BY-SA 4.0 License

### Citation Information

```
@inproceedings{ Butnaru-ACL-2019,
    author = {Andrei M. Butnaru and Radu Tudor Ionescu},
    title = "{MOROCO: The Moldavian and Romanian Dialectal Corpus}",
    booktitle = {Proceedings of ACL},
    year = {2019},
    pages={688--698},
}
```

### Contributions

Thanks to [@MihaelaGaman](https://github.com/MihaelaGaman) for adding this dataset.

