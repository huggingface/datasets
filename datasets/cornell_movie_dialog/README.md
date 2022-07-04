---
language:
- en
paperswithcode_id: cornell-movie-dialogs-corpus
pretty_name: Cornell Movie-Dialogs Corpus
---

# Dataset Card for "cornell_movie_dialog"

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

- **Homepage:** [http://www.cs.cornell.edu/~cristian/Cornell_Movie-Dialogs_Corpus.html](http://www.cs.cornell.edu/~cristian/Cornell_Movie-Dialogs_Corpus.html)
- **Repository:** [More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)
- **Paper:** [More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)
- **Point of Contact:** [More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)
- **Size of downloaded dataset files:** 9.46 MB
- **Size of the generated dataset:** 18.64 MB
- **Total amount of disk used:** 28.10 MB

### Dataset Summary

This corpus contains a large metadata-rich collection of fictional conversations extracted from raw movie scripts:
- 220,579 conversational exchanges between 10,292 pairs of movie characters
- involves 9,035 characters from 617 movies
- in total 304,713 utterances
- movie metadata included:
    - genres
    - release year
    - IMDB rating
    - number of IMDB votes
    - IMDB rating
- character metadata included:
    - gender (for 3,774 characters)
    - position on movie credits (3,321 characters)

### Supported Tasks and Leaderboards

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

### Languages

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

## Dataset Structure

### Data Instances

#### default

- **Size of downloaded dataset files:** 9.46 MB
- **Size of the generated dataset:** 18.64 MB
- **Total amount of disk used:** 28.10 MB

An example of 'train' looks as follows.
```
{
    "characterID1": "u0 ",
    "characterID2": " u2 ",
    "characterName1": " m0 ",
    "characterName2": " m0 ",
    "movieGenres": ["comedy", "romance"],
    "movieID": " m0 ",
    "movieIMDBRating": " 6.90 ",
    "movieNoIMDBVotes": " 62847 ",
    "movieTitle": " f ",
    "movieYear": " 1999 ",
    "utterance": {
        "LineID": ["L1"],
        "text": ["L1 "]
    }
}
```

### Data Fields

The data fields are the same among all splits.

#### default
- `movieID`: a `string` feature.
- `movieTitle`: a `string` feature.
- `movieYear`: a `string` feature.
- `movieIMDBRating`: a `string` feature.
- `movieNoIMDBVotes`: a `string` feature.
- `movieGenres`: a `list` of `string` features.
- `characterID1`: a `string` feature.
- `characterID2`: a `string` feature.
- `characterName1`: a `string` feature.
- `characterName2`: a `string` feature.
- `utterance`: a dictionary feature containing:
  - `text`: a `string` feature.
  - `LineID`: a `string` feature.

### Data Splits

| name  |train|
|-------|----:|
|default|83097|

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

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

### Citation Information

```
  @InProceedings{Danescu-Niculescu-Mizil+Lee:11a,

  author={Cristian Danescu-Niculescu-Mizil and Lillian Lee},

  title={Chameleons in imagined conversations:
  A new approach to understanding coordination of linguistic style in dialogs.},

  booktitle={Proceedings of the

        Workshop on Cognitive Modeling and Computational Linguistics, ACL 2011},

  year={2011}

}

```


### Contributions

Thanks to [@mariamabarham](https://github.com/mariamabarham), [@patrickvonplaten](https://github.com/patrickvonplaten), [@thomwolf](https://github.com/thomwolf) for adding this dataset.
