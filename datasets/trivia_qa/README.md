---
---

# Dataset Card for "trivia_qa"

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

- **Homepage:** [http://nlp.cs.washington.edu/triviaqa/](http://nlp.cs.washington.edu/triviaqa/)
- **Repository:** [More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)
- **Paper:** [More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)
- **Point of Contact:** [More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)
- **Size of downloaded dataset files:** 8833.35 MB
- **Size of the generated dataset:** 43351.32 MB
- **Total amount of disk used:** 52184.66 MB

### [Dataset Summary](#dataset-summary)

TriviaqQA is a reading comprehension dataset containing over 650K
question-answer-evidence triples. TriviaqQA includes 95K question-answer
pairs authored by trivia enthusiasts and independently gathered evidence
documents, six per question on average, that provide high quality distant
supervision for answering the questions.

### [Supported Tasks](#supported-tasks)

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

### [Languages](#languages)

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

## [Dataset Structure](#dataset-structure)

We show detailed information for up to 5 configurations of the dataset.

### [Data Instances](#data-instances)

#### rc

- **Size of downloaded dataset files:** 2542.29 MB
- **Size of the generated dataset:** 15275.31 MB
- **Total amount of disk used:** 17817.60 MB

An example of 'train' looks as follows.
```

```

#### rc.nocontext

- **Size of downloaded dataset files:** 2542.29 MB
- **Size of the generated dataset:** 120.42 MB
- **Total amount of disk used:** 2662.71 MB

An example of 'train' looks as follows.
```

```

#### unfiltered

- **Size of downloaded dataset files:** 3145.53 MB
- **Size of the generated dataset:** 27884.47 MB
- **Total amount of disk used:** 31030.00 MB

An example of 'validation' looks as follows.
```

```

#### unfiltered.nocontext

- **Size of downloaded dataset files:** 603.25 MB
- **Size of the generated dataset:** 71.11 MB
- **Total amount of disk used:** 674.35 MB

An example of 'train' looks as follows.
```

```

### [Data Fields](#data-fields)

The data fields are the same among all splits.

#### rc
- `question`: a `string` feature.
- `question_id`: a `string` feature.
- `question_source`: a `string` feature.
- `entity_pages`: a dictionary feature containing:
  - `doc_source`: a `string` feature.
  - `filename`: a `string` feature.
  - `title`: a `string` feature.
  - `wiki_context`: a `string` feature.
- `search_results`: a dictionary feature containing:
  - `description`: a `string` feature.
  - `filename`: a `string` feature.
  - `rank`: a `int32` feature.
  - `title`: a `string` feature.
  - `url`: a `string` feature.
  - `search_context`: a `string` feature.
- `aliases`: a `list` of `string` features.
- `normalized_aliases`: a `list` of `string` features.
- `matched_wiki_entity_name`: a `string` feature.
- `normalized_matched_wiki_entity_name`: a `string` feature.
- `normalized_value`: a `string` feature.
- `type`: a `string` feature.
- `value`: a `string` feature.

#### rc.nocontext
- `question`: a `string` feature.
- `question_id`: a `string` feature.
- `question_source`: a `string` feature.
- `entity_pages`: a dictionary feature containing:
  - `doc_source`: a `string` feature.
  - `filename`: a `string` feature.
  - `title`: a `string` feature.
  - `wiki_context`: a `string` feature.
- `search_results`: a dictionary feature containing:
  - `description`: a `string` feature.
  - `filename`: a `string` feature.
  - `rank`: a `int32` feature.
  - `title`: a `string` feature.
  - `url`: a `string` feature.
  - `search_context`: a `string` feature.
- `aliases`: a `list` of `string` features.
- `normalized_aliases`: a `list` of `string` features.
- `matched_wiki_entity_name`: a `string` feature.
- `normalized_matched_wiki_entity_name`: a `string` feature.
- `normalized_value`: a `string` feature.
- `type`: a `string` feature.
- `value`: a `string` feature.

#### unfiltered
- `question`: a `string` feature.
- `question_id`: a `string` feature.
- `question_source`: a `string` feature.
- `entity_pages`: a dictionary feature containing:
  - `doc_source`: a `string` feature.
  - `filename`: a `string` feature.
  - `title`: a `string` feature.
  - `wiki_context`: a `string` feature.
- `search_results`: a dictionary feature containing:
  - `description`: a `string` feature.
  - `filename`: a `string` feature.
  - `rank`: a `int32` feature.
  - `title`: a `string` feature.
  - `url`: a `string` feature.
  - `search_context`: a `string` feature.
- `aliases`: a `list` of `string` features.
- `normalized_aliases`: a `list` of `string` features.
- `matched_wiki_entity_name`: a `string` feature.
- `normalized_matched_wiki_entity_name`: a `string` feature.
- `normalized_value`: a `string` feature.
- `type`: a `string` feature.
- `value`: a `string` feature.

#### unfiltered.nocontext
- `question`: a `string` feature.
- `question_id`: a `string` feature.
- `question_source`: a `string` feature.
- `entity_pages`: a dictionary feature containing:
  - `doc_source`: a `string` feature.
  - `filename`: a `string` feature.
  - `title`: a `string` feature.
  - `wiki_context`: a `string` feature.
- `search_results`: a dictionary feature containing:
  - `description`: a `string` feature.
  - `filename`: a `string` feature.
  - `rank`: a `int32` feature.
  - `title`: a `string` feature.
  - `url`: a `string` feature.
  - `search_context`: a `string` feature.
- `aliases`: a `list` of `string` features.
- `normalized_aliases`: a `list` of `string` features.
- `matched_wiki_entity_name`: a `string` feature.
- `normalized_matched_wiki_entity_name`: a `string` feature.
- `normalized_value`: a `string` feature.
- `type`: a `string` feature.
- `value`: a `string` feature.

### [Data Splits Sample Size](#data-splits-sample-size)

|        name        |train |validation|test |
|--------------------|-----:|---------:|----:|
|rc                  |138384|     18669|17210|
|rc.nocontext        |138384|     18669|17210|
|unfiltered          | 87622|     11313|10832|
|unfiltered.nocontext| 87622|     11313|10832|

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

@article{2017arXivtriviaqa,
       author = {{Joshi}, Mandar and {Choi}, Eunsol and {Weld},
                 Daniel and {Zettlemoyer}, Luke},
        title = "{triviaqa: A Large Scale Distantly Supervised Challenge Dataset for Reading Comprehension}",
      journal = {arXiv e-prints},
         year = 2017,
          eid = {arXiv:1705.03551},
        pages = {arXiv:1705.03551},
archivePrefix = {arXiv},
       eprint = {1705.03551},
}

```


### Contributions

Thanks to [@thomwolf](https://github.com/thomwolf), [@patrickvonplaten](https://github.com/patrickvonplaten), [@lewtun](https://github.com/lewtun) for adding this dataset.