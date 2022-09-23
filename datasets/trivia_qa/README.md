---
annotations_creators:
- crowdsourced
language_creators:
- machine-generated
language:
- en
license:
- unknown
multilinguality:
- monolingual
paperswithcode_id: triviaqa
pretty_name: TriviaQA
size_categories:
- 10K<n<100K
- 100K<n<1M
source_datasets:
- original
task_categories:
- question-answering
- text2text-generation
task_ids:
- open-domain-qa
- open-domain-abstractive-qa
- extractive-qa
- abstractive-qa
dataset_info:
- config_name: rc
  features:
  - name: question
    dtype: string
  - name: question_id
    dtype: string
  - name: question_source
    dtype: string
  - name: entity_pages
    sequence:
    - name: doc_source
      dtype: string
    - name: filename
      dtype: string
    - name: title
      dtype: string
    - name: wiki_context
      dtype: string
  - name: search_results
    sequence:
    - name: description
      dtype: string
    - name: filename
      dtype: string
    - name: rank
      dtype: int32
    - name: title
      dtype: string
    - name: url
      dtype: string
    - name: search_context
      dtype: string
  - name: answer
    struct:
    - name: aliases
      sequence: string
    - name: normalized_aliases
      sequence: string
    - name: matched_wiki_entity_name
      dtype: string
    - name: normalized_matched_wiki_entity_name
      dtype: string
    - name: normalized_value
      dtype: string
    - name: type
      dtype: string
    - name: value
      dtype: string
  splits:
  - name: test
    num_bytes: 1577710751
    num_examples: 17210
  - name: train
    num_bytes: 12749652867
    num_examples: 138384
  - name: validation
    num_bytes: 1662321436
    num_examples: 17944
  download_size: 2665779500
  dataset_size: 15989685054
- config_name: rc.nocontext
  features:
  - name: question
    dtype: string
  - name: question_id
    dtype: string
  - name: question_source
    dtype: string
  - name: entity_pages
    sequence:
    - name: doc_source
      dtype: string
    - name: filename
      dtype: string
    - name: title
      dtype: string
    - name: wiki_context
      dtype: string
  - name: search_results
    sequence:
    - name: description
      dtype: string
    - name: filename
      dtype: string
    - name: rank
      dtype: int32
    - name: title
      dtype: string
    - name: url
      dtype: string
    - name: search_context
      dtype: string
  - name: answer
    struct:
    - name: aliases
      sequence: string
    - name: normalized_aliases
      sequence: string
    - name: matched_wiki_entity_name
      dtype: string
    - name: normalized_matched_wiki_entity_name
      dtype: string
    - name: normalized_value
      dtype: string
    - name: type
      dtype: string
    - name: value
      dtype: string
  splits:
  - name: test
    num_bytes: 3668151
    num_examples: 17210
  - name: train
    num_bytes: 106884466
    num_examples: 138384
  - name: validation
    num_bytes: 14060078
    num_examples: 17944
  download_size: 2665779500
  dataset_size: 124612695
- config_name: unfiltered
  features:
  - name: question
    dtype: string
  - name: question_id
    dtype: string
  - name: question_source
    dtype: string
  - name: entity_pages
    sequence:
    - name: doc_source
      dtype: string
    - name: filename
      dtype: string
    - name: title
      dtype: string
    - name: wiki_context
      dtype: string
  - name: search_results
    sequence:
    - name: description
      dtype: string
    - name: filename
      dtype: string
    - name: rank
      dtype: int32
    - name: title
      dtype: string
    - name: url
      dtype: string
    - name: search_context
      dtype: string
  - name: answer
    struct:
    - name: aliases
      sequence: string
    - name: normalized_aliases
      sequence: string
    - name: matched_wiki_entity_name
      dtype: string
    - name: normalized_matched_wiki_entity_name
      dtype: string
    - name: normalized_value
      dtype: string
    - name: type
      dtype: string
    - name: value
      dtype: string
  splits:
  - name: test
    num_bytes: 2906455559
    num_examples: 10832
  - name: train
    num_bytes: 25019623548
    num_examples: 87622
  - name: validation
    num_bytes: 3038803991
    num_examples: 11313
  download_size: 3298328560
  dataset_size: 30964883098
- config_name: unfiltered.nocontext
  features:
  - name: question
    dtype: string
  - name: question_id
    dtype: string
  - name: question_source
    dtype: string
  - name: entity_pages
    sequence:
    - name: doc_source
      dtype: string
    - name: filename
      dtype: string
    - name: title
      dtype: string
    - name: wiki_context
      dtype: string
  - name: search_results
    sequence:
    - name: description
      dtype: string
    - name: filename
      dtype: string
    - name: rank
      dtype: int32
    - name: title
      dtype: string
    - name: url
      dtype: string
    - name: search_context
      dtype: string
  - name: answer
    struct:
    - name: aliases
      sequence: string
    - name: normalized_aliases
      sequence: string
    - name: matched_wiki_entity_name
      dtype: string
    - name: normalized_matched_wiki_entity_name
      dtype: string
    - name: normalized_value
      dtype: string
    - name: type
      dtype: string
    - name: value
      dtype: string
  splits:
  - name: test
    num_bytes: 2320908
    num_examples: 10832
  - name: train
    num_bytes: 63301342
    num_examples: 87622
  - name: validation
    num_bytes: 8297118
    num_examples: 11313
  download_size: 632549060
  dataset_size: 73919368
- config_name: rc.web
  features:
  - name: question
    dtype: string
  - name: question_id
    dtype: string
  - name: question_source
    dtype: string
  - name: entity_pages
    sequence:
    - name: doc_source
      dtype: string
    - name: filename
      dtype: string
    - name: title
      dtype: string
    - name: wiki_context
      dtype: string
  - name: search_results
    sequence:
    - name: description
      dtype: string
    - name: filename
      dtype: string
    - name: rank
      dtype: int32
    - name: title
      dtype: string
    - name: url
      dtype: string
    - name: search_context
      dtype: string
  - name: answer
    struct:
    - name: aliases
      sequence: string
    - name: normalized_aliases
      sequence: string
    - name: matched_wiki_entity_name
      dtype: string
    - name: normalized_matched_wiki_entity_name
      dtype: string
    - name: normalized_value
      dtype: string
    - name: type
      dtype: string
    - name: value
      dtype: string
  splits:
  - name: test
    num_bytes: 1171664123
    num_examples: 9509
  - name: train
    num_bytes: 9408852131
    num_examples: 76496
  - name: validation
    num_bytes: 1232155262
    num_examples: 9951
  download_size: 2665779500
  dataset_size: 11812671516
- config_name: rc.web.nocontext
  features:
  - name: question
    dtype: string
  - name: question_id
    dtype: string
  - name: question_source
    dtype: string
  - name: entity_pages
    sequence:
    - name: doc_source
      dtype: string
    - name: filename
      dtype: string
    - name: title
      dtype: string
    - name: wiki_context
      dtype: string
  - name: search_results
    sequence:
    - name: description
      dtype: string
    - name: filename
      dtype: string
    - name: rank
      dtype: int32
    - name: title
      dtype: string
    - name: url
      dtype: string
    - name: search_context
      dtype: string
  - name: answer
    struct:
    - name: aliases
      sequence: string
    - name: normalized_aliases
      sequence: string
    - name: matched_wiki_entity_name
      dtype: string
    - name: normalized_matched_wiki_entity_name
      dtype: string
    - name: normalized_value
      dtype: string
    - name: type
      dtype: string
    - name: value
      dtype: string
  splits:
  - name: test
    num_bytes: 2024871
    num_examples: 9509
  - name: train
    num_bytes: 58524077
    num_examples: 76496
  - name: validation
    num_bytes: 7694681
    num_examples: 9951
  download_size: 2665779500
  dataset_size: 68243629
- config_name: unfiltered.web
  features:
  - name: question
    dtype: string
  - name: question_id
    dtype: string
  - name: question_source
    dtype: string
  - name: entity_pages
    sequence:
    - name: doc_source
      dtype: string
    - name: filename
      dtype: string
    - name: title
      dtype: string
    - name: wiki_context
      dtype: string
  - name: search_results
    sequence:
    - name: description
      dtype: string
    - name: filename
      dtype: string
    - name: rank
      dtype: int32
    - name: title
      dtype: string
    - name: url
      dtype: string
    - name: search_context
      dtype: string
  - name: answer
    struct:
    - name: aliases
      sequence: string
    - name: normalized_aliases
      sequence: string
    - name: matched_wiki_entity_name
      dtype: string
    - name: normalized_matched_wiki_entity_name
      dtype: string
    - name: normalized_value
      dtype: string
    - name: type
      dtype: string
    - name: value
      dtype: string
  splits:
  - name: test
  - name: train
  - name: validation
  download_size: 3298328560
  dataset_size: 0
- config_name: unfiltered.web.nocontext
  features:
  - name: question
    dtype: string
  - name: question_id
    dtype: string
  - name: question_source
    dtype: string
  - name: entity_pages
    sequence:
    - name: doc_source
      dtype: string
    - name: filename
      dtype: string
    - name: title
      dtype: string
    - name: wiki_context
      dtype: string
  - name: search_results
    sequence:
    - name: description
      dtype: string
    - name: filename
      dtype: string
    - name: rank
      dtype: int32
    - name: title
      dtype: string
    - name: url
      dtype: string
    - name: search_context
      dtype: string
  - name: answer
    struct:
    - name: aliases
      sequence: string
    - name: normalized_aliases
      sequence: string
    - name: matched_wiki_entity_name
      dtype: string
    - name: normalized_matched_wiki_entity_name
      dtype: string
    - name: normalized_value
      dtype: string
    - name: type
      dtype: string
    - name: value
      dtype: string
  splits:
  - name: test
  - name: train
  - name: validation
  download_size: 632549060
  dataset_size: 0
- config_name: rc.wikipedia
  features:
  - name: question
    dtype: string
  - name: question_id
    dtype: string
  - name: question_source
    dtype: string
  - name: entity_pages
    sequence:
    - name: doc_source
      dtype: string
    - name: filename
      dtype: string
    - name: title
      dtype: string
    - name: wiki_context
      dtype: string
  - name: search_results
    sequence:
    - name: description
      dtype: string
    - name: filename
      dtype: string
    - name: rank
      dtype: int32
    - name: title
      dtype: string
    - name: url
      dtype: string
    - name: search_context
      dtype: string
  - name: answer
    struct:
    - name: aliases
      sequence: string
    - name: normalized_aliases
      sequence: string
    - name: matched_wiki_entity_name
      dtype: string
    - name: normalized_matched_wiki_entity_name
      dtype: string
    - name: normalized_value
      dtype: string
    - name: type
      dtype: string
    - name: value
      dtype: string
  splits:
  - name: test
    num_bytes: 406046628
    num_examples: 7701
  - name: train
    num_bytes: 3340800860
    num_examples: 61888
  - name: validation
    num_bytes: 430166174
    num_examples: 7993
  download_size: 2665779500
  dataset_size: 4177013662
- config_name: rc.wikipedia.nocontext
  features:
  - name: question
    dtype: string
  - name: question_id
    dtype: string
  - name: question_source
    dtype: string
  - name: entity_pages
    sequence:
    - name: doc_source
      dtype: string
    - name: filename
      dtype: string
    - name: title
      dtype: string
    - name: wiki_context
      dtype: string
  - name: search_results
    sequence:
    - name: description
      dtype: string
    - name: filename
      dtype: string
    - name: rank
      dtype: int32
    - name: title
      dtype: string
    - name: url
      dtype: string
    - name: search_context
      dtype: string
  - name: answer
    struct:
    - name: aliases
      sequence: string
    - name: normalized_aliases
      sequence: string
    - name: matched_wiki_entity_name
      dtype: string
    - name: normalized_matched_wiki_entity_name
      dtype: string
    - name: normalized_value
      dtype: string
    - name: type
      dtype: string
    - name: value
      dtype: string
  splits:
  - name: test
    num_bytes: 1643280
    num_examples: 7701
  - name: train
    num_bytes: 48360513
    num_examples: 61888
  - name: validation
    num_bytes: 6365397
    num_examples: 7993
  download_size: 2665779500
  dataset_size: 56369190
- config_name: unfiltered.wikipedia
  features:
  - name: question
    dtype: string
  - name: question_id
    dtype: string
  - name: question_source
    dtype: string
  - name: entity_pages
    sequence:
    - name: doc_source
      dtype: string
    - name: filename
      dtype: string
    - name: title
      dtype: string
    - name: wiki_context
      dtype: string
  - name: search_results
    sequence:
    - name: description
      dtype: string
    - name: filename
      dtype: string
    - name: rank
      dtype: int32
    - name: title
      dtype: string
    - name: url
      dtype: string
    - name: search_context
      dtype: string
  - name: answer
    struct:
    - name: aliases
      sequence: string
    - name: normalized_aliases
      sequence: string
    - name: matched_wiki_entity_name
      dtype: string
    - name: normalized_matched_wiki_entity_name
      dtype: string
    - name: normalized_value
      dtype: string
    - name: type
      dtype: string
    - name: value
      dtype: string
  splits:
  - name: test
  - name: train
  - name: validation
  download_size: 3298328560
  dataset_size: 0
- config_name: unfiltered.wikipedia.nocontext
  features:
  - name: question
    dtype: string
  - name: question_id
    dtype: string
  - name: question_source
    dtype: string
  - name: entity_pages
    sequence:
    - name: doc_source
      dtype: string
    - name: filename
      dtype: string
    - name: title
      dtype: string
    - name: wiki_context
      dtype: string
  - name: search_results
    sequence:
    - name: description
      dtype: string
    - name: filename
      dtype: string
    - name: rank
      dtype: int32
    - name: title
      dtype: string
    - name: url
      dtype: string
    - name: search_context
      dtype: string
  - name: answer
    struct:
    - name: aliases
      sequence: string
    - name: normalized_aliases
      sequence: string
    - name: matched_wiki_entity_name
      dtype: string
    - name: normalized_matched_wiki_entity_name
      dtype: string
    - name: normalized_value
      dtype: string
    - name: type
      dtype: string
    - name: value
      dtype: string
  splits:
  - name: test
  - name: train
  - name: validation
  download_size: 632549060
  dataset_size: 0
---

# Dataset Card for "trivia_qa"

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

- **Homepage:** [http://nlp.cs.washington.edu/triviaqa/](http://nlp.cs.washington.edu/triviaqa/)
- **Repository:** [https://github.com/mandarjoshi90/triviaqa](https://github.com/mandarjoshi90/triviaqa)
- **Paper:** [TriviaQA: A Large Scale Distantly Supervised Challenge Dataset for Reading Comprehension](https://arxiv.org/abs/1705.03551)
- **Leaderboard:** [CodaLab Leaderboard](https://competitions.codalab.org/competitions/17208#results)
- **Point of Contact:** [More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)
- **Size of downloaded dataset files:** 8833.35 MB
- **Size of the generated dataset:** 43351.32 MB
- **Total amount of disk used:** 52184.66 MB

### Dataset Summary

TriviaqQA is a reading comprehension dataset containing over 650K
question-answer-evidence triples. TriviaqQA includes 95K question-answer
pairs authored by trivia enthusiasts and independently gathered evidence
documents, six per question on average, that provide high quality distant
supervision for answering the questions.

### Supported Tasks and Leaderboards

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

### Languages

English.

## Dataset Structure

### Data Instances

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

### Data Fields

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

### Data Splits

|        name        |train |validation|test |
|--------------------|-----:|---------:|----:|
|rc                  |138384|     18669|17210|
|rc.nocontext        |138384|     18669|17210|
|unfiltered          | 87622|     11313|10832|
|unfiltered.nocontext| 87622|     11313|10832|

## Dataset Creation

### Curation Rationale

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

### Source Data

#### Initial Data Collection and Normalization

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

#### Who are the source language producers?

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

### Annotations

#### Annotation process

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

#### Who are the annotators?

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

### Personal and Sensitive Information

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

## Considerations for Using the Data

### Social Impact of Dataset

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

### Discussion of Biases

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

### Other Known Limitations

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

## Additional Information

### Dataset Curators

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

### Licensing Information

The University of Washington does not own the copyright of the questions and documents included in TriviaQA.

### Citation Information

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