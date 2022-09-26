---
annotations_creators:
- crowdsourced
language_creators:
- crowdsourced
language:
- en
license:
- cc-by-nc-sa-3.0
multilinguality:
- monolingual
size_categories:
- 1K<n<10K
source_datasets:
- extended|image-flickr-8k
- extended|semeval2012-sts-msr-video
task_categories:
- text-classification
task_ids:
- natural-language-inference
paperswithcode_id: sick
pretty_name: Sentences Involving Compositional Knowledge
---

# Dataset Card for sick

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

- **Homepage:** http://marcobaroni.org/composes/sick.html
- **Repository:** [Needs More Information]
- **Paper:** https://www.aclweb.org/anthology/L14-1314/
- **Leaderboard:** [Needs More Information]
- **Point of Contact:** [Needs More Information]

### Dataset Summary

Shared and internationally recognized benchmarks are fundamental for the development of any computational system. We aim to help the research community working on compositional distributional semantic models (CDSMs) by providing SICK (Sentences Involving Compositional Knowldedge), a large size English benchmark tailored for them. SICK consists of about 10,000 English sentence pairs that include many examples of the lexical, syntactic and semantic phenomena that CDSMs are expected to account for, but do not require dealing with other aspects of existing sentential data sets (idiomatic multiword expressions, named entities, telegraphic language) that are not within the scope of CDSMs. By means of crowdsourcing techniques, each pair was annotated for two crucial semantic tasks: relatedness in meaning (with a 5-point rating scale as gold score) and entailment relation between the two elements (with three possible gold labels: entailment, contradiction, and neutral). The SICK data set was used in SemEval-2014 Task 1, and it freely available for research purposes.


### Supported Tasks and Leaderboards

[Needs More Information]

### Languages

The dataset is in English.

## Dataset Structure

### Data Instances

Example instance:
```
{
    "entailment_AB": "A_neutral_B",
    "entailment_BA": "B_neutral_A",
    "label": 1,
    "id": "1",
    "relatedness_score": 4.5,
    "sentence_A": "A group of kids is playing in a yard and an old man is standing in the background",
    "sentence_A_dataset": "FLICKR",
    "sentence_A_original": "A group of children playing in a yard, a man in the background.",
    "sentence_B": "A group of boys in a yard is playing and a man is standing in the background",
    "sentence_B_dataset": "FLICKR",
    "sentence_B_original": "A group of children playing in a yard, a man in the background."
}
```

### Data Fields

- pair_ID: sentence pair ID
- sentence_A: sentence A
- sentence_B: sentence B
- label: textual entailment gold label: entailment (0), neutral (1) or contradiction (2)
- relatedness_score: semantic relatedness gold score (on a 1-5 continuous scale)
- entailment_AB: entailment for the A-B order (A_neutral_B, A_entails_B, or A_contradicts_B)
- entailment_BA: entailment for the B-A order (B_neutral_A, B_entails_A, or B_contradicts_A)
- sentence_A_original: original sentence from which sentence A is derived
- sentence_B_original: original sentence from which sentence B is derived
- sentence_A_dataset: dataset from which the original sentence A was extracted (FLICKR vs. SEMEVAL)
- sentence_B_dataset: dataset from which the original sentence B was extracted (FLICKR vs. SEMEVAL)

### Data Splits

Train Trial Test
4439 495 4906

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

[Needs More Information]

### Licensing Information

[Needs More Information]

### Citation Information

```
@inproceedings{marelli-etal-2014-sick,
    title = "A {SICK} cure for the evaluation of compositional distributional semantic models",
    author = "Marelli, Marco  and
      Menini, Stefano  and
      Baroni, Marco  and
      Bentivogli, Luisa  and
      Bernardi, Raffaella  and
      Zamparelli, Roberto",
    booktitle = "Proceedings of the Ninth International Conference on Language Resources and Evaluation ({LREC}'14)",
    month = may,
    year = "2014",
    address = "Reykjavik, Iceland",
    publisher = "European Language Resources Association (ELRA)",
    url = "http://www.lrec-conf.org/proceedings/lrec2014/pdf/363_Paper.pdf",
    pages = "216--223",
}
```

### Contributions

Thanks to [@calpt](https://github.com/calpt) for adding this dataset.
