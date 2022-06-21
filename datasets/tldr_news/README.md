# Dataset Card for `tldr_news`

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

- **Homepage:** https://tldr.tech/newsletter

### Dataset Summary

The `tldr_news` dataset was constructed by collecting a daily tech newsletter (
available [here](https://tldr.tech/newsletter)). Then for every piece of news, the "headline" and its corresponding "
content" were collected.
Such a dataset can be used to train a model to generate a headline from a input piece of text.

### Supported Tasks and Leaderboards

There is no official supported tasks nor leaderboard for this dataset.

### Languages

en

## Dataset Structure

### Data Instances

A data point comprises a "headline" and its corresponding "content".
An example is as follows:

```
{
    "headline": "World-first 'impossible' rotating detonation engine fires up",
    "content": "A team in Florida working with the US Air Force has built an experimental model of a rotating detonation rocket engine. It uses spinning explosions inside a ring channel to create a super-efficient thrust. Most engines use combustion, which is a relatively slow and controlled process compared to detonation. Detonation releases significantly more energy than combustion with significantly less fuel, but detonation engines have proven to be incredibly difficult to build and sustain. A 20-second slow-motion video of the rocket firing is available."
}
```

### Data Fields

- `headline (str)`: the piece of news' headline
- `content (str)`: the piece of news

### Data Splits

[Needs More Information]

## Dataset Creation

### Curation Rationale

This dataset was obtained by scrapping the collecting all the existing newsletter
available [here](https://tldr.tech/newsletter). Every single newsletter was then processed to extract all the different
pieces of news. Then for every collected piece of news the headline and the content were extracted.

### Source Data

#### Initial Data Collection and Normalization

The dataset was has been collected from https://tldr.tech/newsletter. The headline and content have not been
post-processed nor normalized.

#### Who are the source language producers?

The people (or person) behind the https://tldr.tech/ newsletter.

### Annotations

#### Annotation process

[Needs More Information]

#### Who are the annotators?

Disclaimers: The dataset was created from a newsletter. The author had no intention to for those newsletters to be
collected to form a dataset.

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

The dataset was obtained by scrapping this website: https://tldr.tech/newsletter

### Licensing Information

[Needs More Information]

### Citation Information

[Needs More Information]