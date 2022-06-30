---
annotations_creators:
- found
language_creators:
- found
language:
- ro
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
- sentiment-classification
paperswithcode_id: null
pretty_name: RoSent
---

# Dataset Card for RoSent

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

- **Homepage:** [GitHub](https://github.com/dumitrescustefan/Romanian-Transformers/tree/examples/examples/sentiment_analysis)
- **Repository:** [GitHub](https://github.com/dumitrescustefan/Romanian-Transformers/tree/examples/examples/sentiment_analysis)
- **Paper:** [arXiv preprint](https://arxiv.org/pdf/2009.08712.pdf)
- **Leaderboard:**
- **Point of Contact:**

### Dataset Summary

This dataset is a Romanian Sentiment Analysis dataset. It is present in a processed form, as used by the authors of [`Romanian Transformers`](https://github.com/dumitrescustefan/Romanian-Transformers) in their examples and based on the original data present in at [this GitHub repository](https://github.com/katakonst/sentiment-analysis-tensorflow). The original data contains product and movie reviews in Romanian.

### Supported Tasks and Leaderboards

[More Information Needed]

### Languages

This dataset is present in Romanian language.

## Dataset Structure

### Data Instances

An instance from the `train` split:
```
{'id': '0', 'label': 1, 'original_id': '0', 'sentence': 'acest document mi-a deschis cu adevarat ochii la ceea ce oamenii din afara statelor unite s-au gandit la atacurile din 11 septembrie. acest film a fost construit in mod expert si prezinta acest dezastru ca fiind mai mult decat un atac asupra pamantului american. urmarile acestui dezastru sunt previzionate din multe tari si perspective diferite. cred ca acest film ar trebui sa fie mai bine distribuit pentru acest punct. de asemenea, el ajuta in procesul de vindecare sa vada in cele din urma altceva decat stirile despre atacurile teroriste. si unele dintre piese sunt de fapt amuzante, dar nu abuziv asa. acest film a fost extrem de recomandat pentru mine, si am trecut pe acelasi sentiment.'}
```

### Data Fields

- `original_id`: a `string` feature containing the original id from the file.
- `id`: a `string` feature .
- `sentence`: a `string` feature.
- `label`: a classification label, with possible values including `negative` (0), `positive` (1).

### Data Splits

This dataset has two splits: `train` with 17941 examples, and `test` with 11005 examples.

## Dataset Creation

### Curation Rationale

[More Information Needed]

### Source Data

#### Initial Data Collection and Normalization

The source dataset is present at the [this GitHub repository](https://github.com/katakonst/sentiment-analysis-tensorflow) and is based on product and movie reviews. The original source is unknown.

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

Stefan Daniel Dumitrescu, Andrei-Marious Avram, Sampo Pyysalo, [@katakonst](https://github.com/katakonst)

### Licensing Information

[More Information Needed]

### Citation Information

```
@article{dumitrescu2020birth,
  title={The birth of Romanian BERT},
  author={Dumitrescu, Stefan Daniel and Avram, Andrei-Marius and Pyysalo, Sampo},
  journal={arXiv preprint arXiv:2009.08712},
  year={2020}
}
```

### Contributions

Thanks to [@gchhablani](https://github.com/gchhablani) and [@iliemihai](https://github.com/iliemihai) for adding this dataset.
