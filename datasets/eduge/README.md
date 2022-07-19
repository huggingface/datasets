---
pretty_name: Eduge
annotations_creators:
- expert-generated
language_creators:
- expert-generated
language:
- mn
license:
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
- multi-class-classification
---


# Dataset Card for Eduge

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

- **Homepage:** http://eduge.mn/
- **Repository:** https://github.com/tugstugi/mongolian-nlp
- **Paper:** [Needs More Information]
- **Leaderboard:** [Needs More Information]
- **Point of Contact:** [Needs More Information]

### Dataset Summary

Eduge news classification dataset provided by Bolorsoft LLC. Used to train the Eduge.mn production news classifier
75K news articles in 9 categories: урлаг соёл, эдийн засаг, эрүүл мэнд, хууль, улс төр, спорт, технологи, боловсрол and байгал орчин

### Supported Tasks and Leaderboards

- `text-classification`: We can transform the above into a 9-class classification task.

### Languages

The text in the dataset is in Mongolian

## Dataset Structure

### Data Instances

For the `default` configuration:
```
{
 'label': 0, #  'урлаг соёл'
 'news': 'Шударга өрсөлдөөн, хэрэглэгчийн төлөө газар 2013 оны дөрөвдүгээр сараас эхлэн Монгол киноны ашиг орлогын мэдээллийг олон нийтэд хүргэж байгаа. Ингэснээр Монголын кино үйлдвэрлэгчид улсад ашиг орлогоо шударгаар төлөх, мөн  чанартай уран бүтээлийн тоо өсөх боломж бүрдэж байгаа юм.',
}
```

### Data Fields

- `news`: a complete news article on a specific topic as a string
- `label`: the single class of the topic, among these values: "урлаг соёл" (0), "эдийн засаг" (1), "эрүүл мэнд" (2), "хууль" (3), "улс төр" (4), "спорт" (5), "технологи" (6), "боловсрол" (7), "байгал орчин" (8).

### Data Splits

The set of complete articles is split into a training and test set. 

## Dataset Creation

### Curation Rationale

[Needs More Information]

### Source Data

#### Initial Data Collection and Normalization

[Needs More Information]

#### Who are the source language producers?

Eduge.mn which is a combination from shuud.mn, ikon.mn, olloo.mn, news.gogo.mn, montsame.mn, zaluu.com, sonin.mn, medee.mn, bloombergtv.mn.

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

[Needs More Information]

### Licensing Information

[Needs More Information]

### Citation Information

No citation available for this dataset.

### Contributions

Thanks to [@enod](https://github.com/enod) for adding this dataset.
