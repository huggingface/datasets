---
annotations_creators:
- no-annotation
language_creators:
- expert-generated
languages:
- es
licenses:
- cc-by-sa-4.0
multilinguality:
- monolingual
size_categories:
- 10M<n<100M
source_datasets:
- original
task_categories:
- other
- sequence-modeling
task_ids:
- language-modeling
- other-other-pretraining-language-models
paperswithcode_id: sbwce
---

# Dataset Card for Spanish Billion Words

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

- **Homepage:** [Spanish Billion Words homepage](https://crscardellino.github.io/SBWCE/)
- **Point of Contact:** [Cristian Cardellino](mailto:ccardellino@unc.edu.ar) (Corpus Creator), [María Grandury](mailto:mariagrandury@gmail.com) (Corpus Submitter)

### Dataset Summary

The Spanish Billion Words Corpus is an unannotated Spanish corpus of nearly 1.5 billion words, compiled from different resources from the web. 
This resources include the spanish portions of SenSem, the Ancora Corpus, some OPUS Project Corpora and the Europarl,
the Tibidabo Treebank, the IULA Spanish LSP Treebank, and dumps from the Spanish Wikipedia, Wikisource and Wikibooks.

This corpus is a compilation of 100 text files. Each line of these files represents one of the 50 million sentences from the corpus.

### Supported Tasks and Leaderboards

This dataset can be used for language modelling and for pretraining language models.

### Languages

The text in this dataset is in Spanish, BCP-47 code: 'es'.

## Dataset Structure

### Data Instances

Each example in this dataset is a sentence in Spanish:
```
{'text': 'Yo me coloqué en un asiento próximo a una ventana cogí un libro de una mesa y empecé a leer'}
```

### Data Fields

- `text`: a sentence in Spanish

### Data Splits

The dataset is not split.

## Dataset Creation

### Curation Rationale

The Spanish Billion Words Corpus was created to train word embeddings using the word2vect algorithm provided by the gensim package.

### Source Data

#### Initial Data Collection and Normalization

The corpus was created compiling the following resources:

- The Spanish portion of [SenSem]().
- The Spanish portion of the [Ancora Corpus](http://clic.ub.edu/corpus/en).
- [Tibidabo Treebank and IULA Spanish LSP Treebank](http://lod.iula.upf.edu/resources/metadata_TRL_Tibidabo_LSP_treebank_ES).
- The Spanish portion of the following [OPUS Project](http://opus.nlpl.eu/index.php) Corpora:
    - The [books](http://opus.nlpl.eu/Books.php) aligned by [Andras Farkas](https://farkastranslations.com/).
    - The [JRC-Acquis](http://opus.nlpl.eu/JRC-Acquis.php) collection of legislative text of the European Union.
    - The [News Commentary](http://opus.nlpl.eu/News-Commentary.php) corpus.
    - The [United Nations](http://opus.nlpl.eu/UN.php) documents compiled by [Alexandre Rafalovitch](https://www.outerthoughts.com/) and [Robert Dale](http://web.science.mq.edu.au/~rdale/).
- The Spanish portion of the [Europarl](http://statmt.org/europarl/) (European Parliament), compiled by [Philipp Koehn](https://homepages.inf.ed.ac.uk/pkoehn/).
- Dumps from the Spanish [Wikipedia](https://es.wikipedia.org/wiki/Wikipedia:Portada), [Wikisource](https://es.wikisource.org/wiki/Portada) and [Wikibooks](https://es.wikibooks.org/wiki/Portada) on date 2015-09-01, parsed with the Wikipedia Extractor.

All the annotated corpora (like Ancora, SenSem and Tibidabo) were untagged and
the parallel corpora (most coming from the OPUS Project) was preprocessed to obtain only the Spanish portions of it.

Once the whole corpus was unannotated, all non-alphanumeric characters were replaced with whitespaces, 
all numbers with the token “DIGITO” and all the multiple whitespaces with only one whitespace.

The capitalization of the words remained unchanged.

#### Who are the source language producers?

The data was compiled and processed by Cristian Cardellino.

### Annotations

The dataset is unannotated. 

#### Annotation process

[N/A]

#### Who are the annotators?

[N/A]

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

The data was collected and processed by Cristian Cardellino.

### Licensing Information

The dataset is licensed under a Creative Commons Attribution-ShareAlike 4.0 International license 
[(CC BY-SA 4.0)](https://creativecommons.org/licenses/by-sa/4.0/)

### Citation Information
```
@misc{cardellinoSBWCE,
     author = {Cardellino, Cristian},
     title = {Spanish {B}illion {W}ords {C}orpus and {E}mbeddings},
     url = {https://crscardellino.github.io/SBWCE/},
     month = {August},
     year = {2019}
}
```
### Contributions

Thanks to [@mariagrandury](https://github.com/mariagrandury) for adding this dataset.