---
pretty_name: Wikicorpus
annotations_creators:
  raw_ca:
  - no-annotation
  raw_en:
  - no-annotation
  raw_es:
  - no-annotation
  tagged_ca:
  - machine-generated
  tagged_en:
  - machine-generated
  tagged_es:
  - machine-generated
language_creators:
- found
languages:
  raw_ca:
  - ca
  raw_en:
  - en
  raw_es:
  - es
  tagged_ca:
  - ca
  tagged_en:
  - en
  tagged_es:
  - es
licenses:
- gfdl-1.1
multilinguality:
- monolingual
size_categories:
  raw_ca:
  - 100K<n<1M
  raw_en:
  - 1M<n<10M
  raw_es:
  - 100K<n<1M
  tagged_ca:
  - 1M<n<10M
  tagged_en:
  - 10M<n<100M
  tagged_es:
  - 1M<n<10M
source_datasets:
- original
task_categories:
  raw_ca:
  - sequence-modeling
  raw_en:
  - sequence-modeling
  raw_es:
  - sequence-modeling
  tagged_ca:
  - structure-prediction
  - text-classification
  tagged_en:
  - structure-prediction
  - text-classification
  tagged_es:
  - structure-prediction
  - text-classification
task_ids:
  raw_ca:
  - language-modeling
  raw_en:
  - language-modeling
  raw_es:
  - language-modeling
  tagged_ca:
  - structure-prediction-other-lemmatization
  - part-of-speech-tagging
  - text-classification-other-word-sense-disambiguation
  tagged_en:
  - structure-prediction-other-lemmatization
  - part-of-speech-tagging
  - text-classification-other-word-sense-disambiguation
  tagged_es:
  - structure-prediction-other-lemmatization
  - part-of-speech-tagging
  - text-classification-other-word-sense-disambiguation
paperswithcode_id: null
---

# Dataset Card for Wikicorpus

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

- **Homepage:** https://www.cs.upc.edu/~nlp/wikicorpus/
- **Repository:**
- **Paper:** https://www.cs.upc.edu/~nlp/papers/reese10.pdf
- **Leaderboard:**
- **Point of Contact:**

### Dataset Summary

The Wikicorpus is a trilingual corpus (Catalan, Spanish, English) that contains large portions of the Wikipedia (based on a 2006 dump) and has been automatically enriched with linguistic information. In its present version, it contains over 750 million words.

The corpora have been annotated with lemma and part of speech information using the open source library FreeLing. Also, they have been sense annotated with the state of the art Word Sense Disambiguation algorithm UKB. As UKB assigns WordNet senses, and WordNet has been aligned across languages via the InterLingual Index, this sort of annotation opens the way to massive explorations in lexical semantics that were not possible before.

### Supported Tasks and Leaderboards

[More Information Needed]

### Languages

Each sub-dataset is monolingual in the languages:
- ca: Catalan
- en: English
- es: Spanish

## Dataset Structure

### Data Instances

[More Information Needed]

### Data Fields

[More Information Needed]

### Data Splits

[More Information Needed]

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

The WikiCorpus is licensed under the same license as Wikipedia, that is, the [GNU Free Documentation License](http://www.fsf.org/licensing/licenses/fdl.html)

### Citation Information

```
@inproceedings{reese-etal-2010-wikicorpus,
    title = "{W}ikicorpus: A Word-Sense Disambiguated Multilingual {W}ikipedia Corpus",
    author = "Reese, Samuel  and
      Boleda, Gemma  and
      Cuadros, Montse  and
      Padr{\'o}, Llu{\'i}s  and
      Rigau, German",
    booktitle = "Proceedings of the Seventh International Conference on Language Resources and Evaluation ({LREC}'10)",
    month = may,
    year = "2010",
    address = "Valletta, Malta",
    publisher = "European Language Resources Association (ELRA)",
    url = "http://www.lrec-conf.org/proceedings/lrec2010/pdf/222_Paper.pdf",
    abstract = "This article presents a new freely available trilingual corpus (Catalan, Spanish, English) that contains large portions of the Wikipedia and has been automatically enriched with linguistic information. To our knowledge, this is the largest such corpus that is freely available to the community: In its present version, it contains over 750 million words. The corpora have been annotated with lemma and part of speech information using the open source library FreeLing. Also, they have been sense annotated with the state of the art Word Sense Disambiguation algorithm UKB. As UKB assigns WordNet senses, and WordNet has been aligned across languages via the InterLingual Index, this sort of annotation opens the way to massive explorations in lexical semantics that were not possible before. We present a first attempt at creating a trilingual lexical resource from the sense-tagged Wikipedia corpora, namely, WikiNet. Moreover, we present two by-products of the project that are of use for the NLP community: An open source Java-based parser for Wikipedia pages developed for the construction of the corpus, and the integration of the WSD algorithm UKB in FreeLing.",
}
```

### Contributions

Thanks to [@albertvillanova](https://github.com/albertvillanova) for adding this dataset.