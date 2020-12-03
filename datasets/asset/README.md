---
annotations_creators:
- machine-generated
language_creators:
- found
languages:
- en
licenses:
- cc-by-sa-4.0
multilinguality:
- monolingual
size_categories:
- 1K<n<10K
source_datasets:
- original
- extented|other-turkcorpus
task_categories:
  ratings:
  - text-scoring
  simplification:
  - conditional-text-generation
task_ids:
  ratings:
  - text-scoring-other-simplification-evaluation
  simplification:
  - text-simplification
  ---

# Dataset Card for ASSET

## Table of Contents
- [Dataset Description](#dataset-description)
  - [Dataset Summary](#dataset-summary)
  - [Supported Tasks](#supported-tasks-and-leaderboards)
  - [Languages](#languages)
- [Dataset Structure](#dataset-structure)
  - [Data Instances](#data-instances)
  - [Data Fields](#data-instances)
  - [Data Splits](#data-instances)
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

## Dataset Description

- **Repository:** [ASSET Github repository](https://github.com/facebookresearch/asset)
- **Paper:** [ASSET: A Dataset for Tuning and Evaluation of Sentence Simplification Models with Multiple Rewriting Transformations](https://www.aclweb.org/anthology/2020.acl-main.424/)
- **Point of Contact:** [Louis Martin](louismartincs@gmail.com)

### Dataset Summary

[ASSET](https://github.com/facebookresearch/asset) [(Alva-Manchego et al., 2020)](https://www.aclweb.org/anthology/2020.acl-main.424.pdf) is multi-reference dataset for the evaluation of sentence simplification in English. The dataset uses the same 2,359 sentences from [TurkCorpus]( https://github.com/cocoxu/simplification/) [(Xu et al., 2016)](https://www.aclweb.org/anthology/Q16-1029.pdf) and each sentence is associated with 10 crowdsourced simplifications. Unlike previous simplification datasets, which contain a single transformation (e.g., lexical paraphrasing in TurkCorpus or sentence
splitting in [HSplit](https://www.aclweb.org/anthology/D18-1081.pdf)), the simplifications in ASSET encompass a variety of rewriting transformations.

### Supported Tasks and Leaderboards

The dataset supports the evaluation of `test-simplification` systems. Success in this tasks is typically measured using the [SARI](https://huggingface.co/metrics/sari) and [FKBLEU](https://huggingface.co/metrics/fkbleu) metrics described in the paper [Optimizing Statistical Machine Translation for Text Simplification](https://www.aclweb.org/anthology/Q16-1029.pdf).

### Languages

The text in this dataset is in English (`en`).

## Dataset Structure

### Data Instances

- `simplification` configuration: an instance consists in an original sentence and 10 possible reference simplifications.
- `ratings` configuration: a data instance consists in an original sentence, a simplification obtained by an automated system, and a judgment of quality along one of three axes by a crowd worker.

### Data Fields

- `original`: an original sentence from the source datasets
- `simplifications`: in the `simplification` config, a set of reference simplifications produced by crowd workers.
- `simplification`: in the `ratings` config, a simplification of the original obtained by an automated system
- `aspect`: in the `ratings` config, the aspect on which the simplification is evaluated, one of `meaning`, `fluency`, `simplicity`
- `rating`: a quality rating between 0 and 100

### Data Splits

ASSET does not contain a training set; many models use [WikiLarge](https://github.com/XingxingZhang/dress) (Zhang and Lapata, 2017) for training.

Each input sentence has 10 associated reference simplified sentences. The statistics of ASSET are given below.

|                            | Dev    | Test | Total |
| -----                      | ------ | ---- | ----- |
| Input Sentences            | 2000   | 359  | 2359  |
| Reference Simplifications  | 20000  | 3590 | 23590 |

The test and validation sets are the same as those of TurkCorpus. The split was random.

There are 19.04 tokens per reference on average (lower than 21.29 and 25.49 for TurkCorpus and HSplit, respectively). Most (17,245) of the referece sentences do not involve sentence splitting.

## Dataset Creation

### Curation Rationale

ASSET was created in order to improve the evaluation of sentence simplification. It uses the same input sentences as the [TurkCorpus]( https://github.com/cocoxu/simplification/) dataset from [(Xu et al., 2016)](https://www.aclweb.org/anthology/Q16-1029.pdf). The 2,359 input sentences of TurkCorpus are a sample of "standard" (not simple) sentences from the [Parallel Wikipedia Simplification (PWKP)](https://www.informatik.tu-darmstadt.de/ukp/research_6/data/sentence_simplification/simple_complex_sentence_pairs/index.en.jsp) dataset [(Zhu et al., 2010)](https://www.aclweb.org/anthology/C10-1152.pdf), which come from the August 22, 2009 version of Wikipedia. The sentences of TurkCorpus were chosen to be of similar length [(Xu et al., 2016)](https://www.aclweb.org/anthology/Q16-1029.pdf). No further information is provided on the sampling strategy.

The TurkCorpus dataset was developed in order to overcome some of the problems with sentence pairs from Standard and Simple Wikipedia: a large fraction of sentences were misaligned, or not actually simpler [(Xu et al., 2016)](https://www.aclweb.org/anthology/Q16-1029.pdf). However, TurkCorpus mainly focused on *lexical paraphrasing*, and so cannot be used to evaluate simplifications involving *compression* (deletion) or *sentence splitting*. HSplit [(Sulem et al., 2018)](https://www.aclweb.org/anthology/D18-1081.pdf), on the other hand, can only be used to evaluate sentence splitting. The reference sentences in ASSET include a wider variety of sentence rewriting strategies, combining splitting, compression and paraphrasing. Annotators were given examples of each kind of transformation individually, as well as all three transformations used at once, but were allowed to decide which transformations to use for any given sentence.

An example illustrating the differences between TurkCorpus, HSplit and ASSET is given below:

> **Original:** He settled in London, devoting himself chiefly to practical teaching.
>
> **TurkCorpus:** He rooted in London, devoting himself mainly to practical teaching.
>
> **HSplit:** He settled in London. He devoted himself chiefly to practical teaching.
>
> **ASSET:** He lived in London. He was a teacher.

### Source Data

#### Initial Data Collection and Normalization

[More Information Needed]

#### Who are the source language producers?

The input sentences are from English Wikipedia (August 22, 2009 version). No demographic information is available for the writers of these sentences. However, most Wikipedia editors are male (Lam, 2011; Graells-Garrido, 2015), which has an impact on the topics covered (see also [the Wikipedia page on Wikipedia gender bias](https://en.wikipedia.org/wiki/Gender_bias_on_Wikipedia)). In addition, Wikipedia editors are mostly white, young, and from the Northern Hemisphere [(Wikipedia: Systemic bias)](https://en.wikipedia.org/wiki/Wikipedia:Systemic_bias).

Reference sentences were written by 42 workers on Amazon Mechanical Turk (AMT). The requirements for being an annotator were:
- Passing a Qualification Test (appropriately simplifying sentences). Out of 100 workers, 42 passed the test.
- Being a resident of the United States, United Kingdom or Canada.
- Having a HIT approval rate over 95%, and over 1000 HITs approved.

No other demographic or compensation information is provided in the ASSET paper.

### Annotations

#### Annotation process

The instructions given to the annotators are available [here](https://github.com/facebookresearch/asset/blob/master/crowdsourcing/AMT_AnnotationInstructions.pdf).

#### Who are the annotators?

[More Information Needed]

### Personal and Sensitive Information

[More Information Needed]

## Considerations for Using the Data

### Social Impact of Dataset

[More Information Needed]

### Discussion of Biases

The dataset may contain some social biases, as the input sentences are based on Wikipedia. Studies have shown that the English Wikipedia contains both gender biases (Schmahl et al., 2020) and racial  biases (Adams et al., 2019).

> Adams, Julia, Hannah Brückner, and Cambria Naslund. "Who Counts as a Notable Sociologist on Wikipedia? Gender, Race, and the “Professor Test”." Socius 5 (2019): 2378023118823946.
> Schmahl, Katja Geertruida, et al. "Is Wikipedia succeeding in reducing gender bias? Assessing changes in gender bias in Wikipedia using word embeddings." Proceedings of the Fourth Workshop on Natural Language Processing and Computational Social Science. 2020.

### Other Known Limitations

[More Information Needed]

## Additional Information

### Dataset Curators

ASSET was developed by researchers at the University of Sheffield, Inria,
Facebook AI Research, and Imperial College London. The work was partly supported by Benoît Sagot's chair in the PRAIRIE institute, funded by the French National Research Agency (ANR) as part of the "Investissements d’avenir" program (reference ANR-19-P3IA-0001).

### Licensing Information

[Attribution-NonCommercial 4.0 International (CC BY-NC 4.0)](https://creativecommons.org/licenses/by-nc/4.0/)

### Citation Information

```
@inproceedings{alva-manchego-etal-2020-asset,
    title = "{ASSET}: {A} Dataset for Tuning and Evaluation of Sentence Simplification Models with Multiple Rewriting Transformations",
    author = "Alva-Manchego, Fernando  and
      Martin, Louis  and
      Bordes, Antoine  and
      Scarton, Carolina  and
      Sagot, Beno{\^\i}t  and
      Specia, Lucia",
    booktitle = "Proceedings of the 58th Annual Meeting of the Association for Computational Linguistics",
    month = jul,
    year = "2020",
    address = "Online",
    publisher = "Association for Computational Linguistics",
    url = "https://www.aclweb.org/anthology/2020.acl-main.424",
    pages = "4668--4679",
}
```

This dataset card uses material written by [Juan Diego Rodriguez](https://github.com/juand-r).
