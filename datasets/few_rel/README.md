---
annotations_creators:
- crowdsourced
- machine-generated
language_creators:
- found
language:
- en
license:
- mit
multilinguality:
- monolingual
size_categories:
- 10K<n<100K
- n<1K
source_datasets:
- original
task_categories:
- other
task_ids:
- other-other-relation-extraction
paperswithcode_id: fewrel
pretty_name: Few-Shot Relation Classification Dataset
configs:
- default
- pid2name
---

# Dataset Card for few_rel

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

- **Homepage:** [GitHub Page](https://thunlp.github.io/)
- **Repository:** [GitHub](https://github.com/thunlp/FewRel)
- **Paper:** [FewRel](https://www.aclweb.org/anthology/D18-1514.pdf), [FewRel 2.0](https://www.aclweb.org/anthology/D19-1649.pdf)
- **Leaderboard:** [GitHub Leaderboard](https://thunlp.github.io/fewrel.html)
- **Point of Contact:** [Needs More Information]

### Dataset Summary

FewRel is a large-scale few-shot relation extraction dataset, which contains more than one hundred relations and tens of thousands of annotated instances cross different domains.

### Supported Tasks and Leaderboards

[Needs More Information]

### Languages

The dataset contaings English text, as used by writers on Wikipedia, and crowdsourced English annotations.

## Dataset Structure


### Data Instances

An instance from `train_wiki` split:

```
{'head': {'indices': [[16]], 'text': 'tjq', 'type': 'Q1331049'}, 'names': ['place served by transport hub', 'territorial entity or entities served by this transport hub (airport, train station, etc.)'], 'relation': 'P931', 'tail': {'indices': [[13, 14]], 'text': 'tanjung pandan', 'type': 'Q3056359'}, 'tokens': ['Merpati', 'flight', '106', 'departed', 'Jakarta', '(', 'CGK', ')', 'on', 'a', 'domestic', 'flight', 'to', 'Tanjung', 'Pandan', '(', 'TJQ', ')', '.']}
```

### Data Fields

For `default`:

- `relation`: a `string` feature containing PID of the relation.
- `tokens`: a `list` of `string` features containing tokens for the text.
- `head`: a dictionary containing:
  - `text`: a `string` feature representing the head entity.
  - `type`: a `string` feature representing the type of the head entity.
  - `indices`: a `list` containing `list` of token indices.

- `tail`: a dictionary containing:
  - `text`: a `string` feature representing the tail entity.
  - `type`: a `string` feature representing the type of the tail entity.
  - `indices`: a `list` containing `list` of token indices.
- `names`: a `list` of `string` features containing relation names. For `pubmed_unsupervised` split, this is set to a `list` with an empty `string`. For `val_semeval` and `val_pubmed` split, this is set to a `list` with the `string` from the `relation` field.

### Data Splits

`train_wiki`: 44800
`val_nyt`: 2500
`val_pubmed`: 1000
`val_semeval`: 8851
`val_wiki`: 11200
`pubmed_unsupervised`: 2500

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

For FewRel:

Han, Xu and Zhu, Hao and Yu, Pengfei and Wang, Ziyun and Yao, Yuan and Liu, Zhiyuan and Sun, Maosong

For  FewRel 2.0:

Gao, Tianyu and Han, Xu and Zhu, Hao and Liu, Zhiyuan and Li, Peng and Sun, Maosong and Zhou, Jie

### Licensing Information

```
MIT License

Copyright (c) 2018 THUNLP

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

### Citation Information

```
@inproceedings{han-etal-2018-fewrel,
    title = "{F}ew{R}el: A Large-Scale Supervised Few-Shot Relation Classification Dataset with State-of-the-Art Evaluation",
    author = "Han, Xu and Zhu, Hao and Yu, Pengfei and Wang, Ziyun and Yao, Yuan and Liu, Zhiyuan and Sun, Maosong",
    booktitle = "Proceedings of the 2018 Conference on Empirical Methods in Natural Language Processing",
    month = oct # "-" # nov,
    year = "2018",
    address = "Brussels, Belgium",
    publisher = "Association for Computational Linguistics",
    url = "https://www.aclweb.org/anthology/D18-1514",
    doi = "10.18653/v1/D18-1514",
    pages = "4803--4809"
}
```
```

@inproceedings{gao-etal-2019-fewrel,
    title = "{F}ew{R}el 2.0: Towards More Challenging Few-Shot Relation Classification",
    author = "Gao, Tianyu and Han, Xu and Zhu, Hao and Liu, Zhiyuan and Li, Peng and Sun, Maosong and Zhou, Jie",
    booktitle = "Proceedings of the 2019 Conference on Empirical Methods in Natural Language Processing and the 9th International Joint Conference on Natural Language Processing (EMNLP-IJCNLP)",
    month = nov,
    year = "2019",
    address = "Hong Kong, China",
    publisher = "Association for Computational Linguistics",
    url = "https://www.aclweb.org/anthology/D19-1649",
    doi = "10.18653/v1/D19-1649",
    pages = "6251--6256"
}
```

### Contributions

Thanks to [@gchhablani](https://github.com/gchhablani) for adding this dataset.
