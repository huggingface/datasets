---
annotations_creators:
- found
language_creators:
- found
languages:
- es
licenses:
- unknown
multilinguality:
- monolingual
size_categories:
- 1K<n<10K
source_datasets:
- original
task_categories:
- text-classification
task_ids:
- sentiment-classification
paperswithcode_id: null
pretty_name: Muchocine
---

# Dataset Card for Muchocine

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

- **Homepage:** http://www.lsi.us.es/~fermin/index.php/Datasets

### Dataset Summary

The Muchocine reviews dataset contains 3,872 longform movie reviews in Spanish language,
each with a shorter summary review, and a rating on a 1-5 scale.

### Supported Tasks and Leaderboards

- `text-classification`: This dataset can be used for Text Classification, more precisely Sentiment Classification where the task is to predict the `star_rating` for a `reveiw_body` or a `review summaray`.

### Languages

Spanish.

## Dataset Structure

### Data Instances

An example from the train split:

```
{
  'review_body': 'Zoom nos cuenta la historia de Jack Shepard, anteriormente conocido como el Capitán Zoom, Superhéroe que perdió sus poderes y que actualmente vive en el olvido. La llegada de una amenaza para la Tierra hará que la agencia del gobierno que se ocupa de estos temas acuda a él para que entrene a un grupo de jóvenes con poderes para combatir esta amenaza.Zoom es una comedia familiar, con todo lo que eso implica, es decir, guión flojo y previsible, bromas no salidas de tono, historia amorosa de por medio y un desenlace tópico. La gracia está en que los protagonistas son jóvenes con superpoderes, una producción cargada de efectos especiales y unos cuantos guiños frikis. La película además se pasa volando ya que dura poco mas de ochenta minutos y cabe destacar su prologo en forma de dibujos de comics explicando la historia de la cual partimos en la película.Tim Allen protagoniza la cinta al lado de un envejecido Chevy Chase, que hace de doctor encargado del proyecto, un papel bastante gracioso y ridículo, pero sin duda el mejor papel es el de Courteney Cox, en la piel de una científica amante de los comics y de lo más friki. Del grupito de los cuatro niños sin duda la mas graciosa es la niña pequeña con súper fuerza y la que provocara la mayor parte de los gags debido a su poder.Una comedia entretenida y poca cosa más para ver una tarde de domingo. ',
  'review_summary': 'Una comedia entretenida y poca cosa más para ver una tarde de domingo ', 'star_rating': 2
}
```

### Data Fields

- `review_body` - longform review
- `review_summary` - shorter-form review
- `star_rating` - an integer star rating (1-5)

The original source also includes part-of-speech tagging for body and summary fields.

### Data Splits

One split (train) with 3,872 reviews.

## Dataset Creation

### Curation Rationale

[More Information Needed]

### Source Data

#### Initial Data Collection and Normalization

Data was collected from www.muchocine.net and uploaded by Dr. Fermín L. Cruz Mata
of La Universidad de Sevilla.

#### Who are the source language producers?

[More Information Needed]

### Annotations

#### Annotation process

The text reviews and star ratings came directly from users, so no additional annotation was needed.

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

Dr. Fermín L. Cruz Mata.

### Licensing Information

[More Information Needed]

### Citation Information

See http://www.lsi.us.es/~fermin/index.php/Datasets

### Contributions

Thanks to [@mapmeld](https://github.com/mapmeld) for adding this dataset.
