---
annotations_creators:
- expert-generated
language_creators:
- expert-generated
languages:
- id
licenses:
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
- fact-checking
paperswithcode_id: null
---

# Dataset Card for Indonesian Clickbait Headlines

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

- **Homepage:** [CLICK-ID: A Novel Dataset for Indonesian Clickbait Headlines](https://www.sciencedirect.com/science/article/pii/S2352340920311252#!)
- **Repository:** [CLICK-ID: A Novel Dataset for Indonesian Clickbait Headlines](http://dx.doi.org/10.17632/k42j7x2kpn.1)
- **Paper:** [CLICK-ID: A Novel Dataset for Indonesian Clickbait Headlines](https://www.sciencedirect.com/science/article/pii/S2352340920311252#!)
- **Leaderboard:**
- **Point of Contact:** [Andika William](mailto:andika.william@mail.ugm.ac.id), [Yunita Sari](mailto:yunita.sari@ugm.ac.id)

### Dataset Summary

The CLICK-ID dataset is a collection of Indonesian news headlines that was collected from 12 local online news 
publishers; detikNews, Fimela, Kapanlagi, Kompas, Liputan6, Okezone, Posmetro-Medan, Republika, Sindonews, Tempo,
Tribunnews, and Wowkeren. This dataset is comprised of mainly two parts; (i) 46,119 raw article data, and (ii)
15,000 clickbait annotated sample headlines. Annotation was conducted with 3 annotator examining each headline.
Judgment were based only on the headline. The majority then is considered as the ground truth. In the annotated
sample, our annotation shows 6,290 clickbait and 8,710 non-clickbait.

### Supported Tasks and Leaderboards

[More Information Needed]

### Languages
Indonesian

## Dataset Structure
### Data Instances
An example of the annotated article:
```
{
  'id': '100',
  'label': 1,
  'title': "SAH! Ini Daftar Nama Menteri Kabinet Jokowi - Ma'ruf Amin"
}
>
``` 

### Data Fields

#### Annotated
- `id`: id of the sample
- `title`: the title of the news article
- `label`: the label of the article, either non-clickbait or clickbait

#### Raw
- `id`: id of the sample
- `title`: the title of the news article
- `source`: the name of the publisher/newspaper
- `date`: date
- `category`: the category of the article
- `sub-category`: the sub category of the article
- `content`: the content of the article
- `url`: the url of the article

### Data Splits

The dataset contains train set.

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

Creative Commons Attribution 4.0 International license

### Citation Information
```
@article{WILLIAM2020106231,
title = "CLICK-ID: A novel dataset for Indonesian clickbait headlines",
journal = "Data in Brief",
volume = "32",
pages = "106231",
year = "2020",
issn = "2352-3409",
doi = "https://doi.org/10.1016/j.dib.2020.106231",
url = "http://www.sciencedirect.com/science/article/pii/S2352340920311252",
author = "Andika William and Yunita Sari",
keywords = "Indonesian, Natural Language Processing, News articles, Clickbait, Text-classification",
abstract = "News analysis is a popular task in Natural Language Processing (NLP). In particular, the problem of clickbait in news analysis has gained attention in recent years [1, 2]. However, the majority of the tasks has been focused on English news, in which there is already a rich representative resource. For other languages, such as Indonesian, there is still a lack of resource for clickbait tasks. Therefore, we introduce the CLICK-ID dataset of Indonesian news headlines extracted from 12 Indonesian online news publishers. It is comprised of 15,000 annotated headlines with clickbait and non-clickbait labels. Using the CLICK-ID dataset, we then developed an Indonesian clickbait classification model achieving favourable performance. We believe that this corpus will be useful for replicable experiments in clickbait detection or other experiments in NLP areas."
}
```

### Contributions

Thanks to [@cahya-wirawan](https://github.com/cahya-wirawan) for adding this dataset.