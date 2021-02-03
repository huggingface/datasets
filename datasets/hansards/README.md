---
---

# Dataset Card for "hansards"

## Table of Contents
- [Dataset Description](#dataset-description)
  - [Dataset Summary](#dataset-summary)
  - [Supported Tasks](#supported-tasks)
  - [Languages](#languages)
- [Dataset Structure](#dataset-structure)
  - [Data Instances](#data-instances)
  - [Data Fields](#data-fields)
  - [Data Splits Sample Size](#data-splits-sample-size)
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

## [Dataset Description](#dataset-description)

- **Homepage:** [https://www.isi.edu/natural-language/download/hansard/](https://www.isi.edu/natural-language/download/hansard/)
- **Repository:** [More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)
- **Paper:** [More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)
- **Point of Contact:** [More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)
- **Size of downloaded dataset files:** 78.99 MB
- **Size of the generated dataset:** 248.34 MB
- **Total amount of disk used:** 327.33 MB

### [Dataset Summary](#dataset-summary)

This release contains 1.3 million pairs of aligned text chunks (sentences or smaller fragments)
from the official records (Hansards) of the 36th Canadian Parliament.

The complete Hansards of the debates in the House and Senate of the 36th Canadian Parliament,
as far as available, were aligned. The corpus was then split into 5 sets of sentence pairs:
training (80% of the sentence pairs), two sets of sentence pairs for testing (5% each), and
two sets of sentence pairs for final evaluation (5% each). The current release consists of the
training and testing sets. The evaluation sets are reserved for future MT evaluation purposes
and currently not available.

Caveats
1. This release contains only sentence pairs. Even though the order of the sentences is the same
as in the original, there may be gaps resulting from many-to-one, many-to-many, or one-to-many
alignments that were filtered out. Therefore, this release may not be suitable for
discourse-related research.
2. Neither the sentence splitting nor the alignments are perfect. In particular, watch out for
pairs that differ considerably in length. You may want to filter these out before you do
any statistical training.

The alignment of the Hansards was performed as part of the ReWrite project under funding
from the DARPA TIDES program.

### [Supported Tasks](#supported-tasks)

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

### [Languages](#languages)

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

## [Dataset Structure](#dataset-structure)

We show detailed information for up to 5 configurations of the dataset.

### [Data Instances](#data-instances)

#### house

- **Size of downloaded dataset files:** 64.45 MB
- **Size of the generated dataset:** 204.44 MB
- **Total amount of disk used:** 268.89 MB

An example of 'train' looks as follows.
```
{
    "en": "Mr. Walt Lastewka (Parliamentary Secretary to Minister of Industry, Lib.):",
    "fr": "M. Walt Lastewka (secrétaire parlementaire du ministre de l'Industrie, Lib.):"
}
```

#### senate

- **Size of downloaded dataset files:** 14.54 MB
- **Size of the generated dataset:** 43.90 MB
- **Total amount of disk used:** 58.44 MB

An example of 'train' looks as follows.
```
{
    "en": "Mr. Walt Lastewka (Parliamentary Secretary to Minister of Industry, Lib.):",
    "fr": "M. Walt Lastewka (secrétaire parlementaire du ministre de l'Industrie, Lib.):"
}
```

### [Data Fields](#data-fields)

The data fields are the same among all splits.

#### house
- `fr`: a `string` feature.
- `en`: a `string` feature.

#### senate
- `fr`: a `string` feature.
- `en`: a `string` feature.

### [Data Splits Sample Size](#data-splits-sample-size)

| name |train | test |
|------|-----:|-----:|
|house |947969|122290|
|senate|182135| 25553|

## [Dataset Creation](#dataset-creation)

### [Curation Rationale](#curation-rationale)

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

### [Source Data](#source-data)

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

### [Annotations](#annotations)

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

### [Personal and Sensitive Information](#personal-and-sensitive-information)

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

## [Considerations for Using the Data](#considerations-for-using-the-data)

### [Social Impact of Dataset](#social-impact-of-dataset)

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

### [Discussion of Biases](#discussion-of-biases)

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

### [Other Known Limitations](#other-known-limitations)

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

## [Additional Information](#additional-information)

### [Dataset Curators](#dataset-curators)

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

### [Licensing Information](#licensing-information)

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

### [Citation Information](#citation-information)

```

```


### Contributions

Thanks to [@patrickvonplaten](https://github.com/patrickvonplaten), [@thomwolf](https://github.com/thomwolf), [@albertvillanova](https://github.com/albertvillanova) for adding this dataset.