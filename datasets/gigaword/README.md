---
annotations_creators:
- found
language_creators:
- found
language:
- en
license:
- mit
multilinguality:
- monolingual
size_categories:
- 100K<n<1M
source_datasets:
- extended|gigaword_2003
task_categories:
- summarization
task_ids:
- summarization--other-headline-generation
paperswithcode_id: null
pretty_name: Gigaword
train-eval-index:
- config: default
  task: summarization
  task_id: summarization
  splits:
    train_split: train
    eval_split: test
  col_mapping:
    document: text
    summary: target
  metrics:
    - type: rouge
      name: Rouge
---

# Dataset Card for Gigaword

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

- **Repository:** [Gigaword repository](https://github.com/harvardnlp/sent-summary)
- **Leaderboard:** [Gigaword leaderboard](https://paperswithcode.com/sota/text-summarization-on-gigaword)
- **Paper:** [A Neural Attention Model for Abstractive Sentence Summarization](https://arxiv.org/abs/1509.00685)
- **Point of Contact:** [Alexander Rush](mailto:arush@cornell.edu)
- **Size of downloaded dataset files:** 551.61 MB
- **Size of the generated dataset:** 918.35 MB
- **Total amount of disk used:** 1469.96 MB

### Dataset Summary

Headline-generation on a corpus of article pairs from Gigaword consisting of
around 4 million articles. Use the 'org_data' provided by
https://github.com/microsoft/unilm/ which is identical to
https://github.com/harvardnlp/sent-summary but with better format.

### Supported Tasks and Leaderboards

- `summarization`: This dataset can be used for Summarization, where given a dicument, the goal is to predict its summery. The model performance is evaluated using the [ROUGE](https://huggingface.co/metrics/rouge) metric. The leaderboard for this task is available [here](https://paperswithcode.com/sota/text-summarization-on-gigaword).

### Languages

English.

## Dataset Structure

### Data Instances

An example of 'train' looks as follows.
```
{
  'document': "australia 's current account deficit shrunk by a record #.## billion dollars -lrb- #.## billion us -rrb- in the june quarter due to soaring commodity prices , figures released monday showed .", 
  'summary': 'australian current account deficit narrows sharply'
}
```

### Data Fields

The data fields are the same among all splits.

- `document`: a `string` feature.
- `summary`: a `string` feature.

### Data Splits

| name  | train |validation|test|
|-------|------:|---------:|---:|
|default|3803957|    189651|1951|

## Dataset Creation

### Curation Rationale

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

### Source Data

#### Initial Data Collection and Normalization

From the paper:
> For our training set, we pair the headline of each article with its first sentence to create an inputsummary pair. While the model could in theory be trained on any pair, Gigaword contains many spurious headline-article pairs. We therefore prune training based on the following heuristic filters: (1) Are there no non-stop-words in common? (2) Does the title contain a byline or other extraneous editing marks? (3) Does the title have a question mark or colon? After applying these filters, the training set consists of roughly J = 4 million title-article pairs. We apply a minimal preprocessing step using PTB tokenization, lower-casing, replacing all digit characters with #, and replacing of word types seen less than 5 times with UNK. We also remove all articles from the time-period of the DUC evaluation. release. 
The complete input training vocabulary consists of 119 million word tokens and 110K unique word types with an average sentence size of 31.3 words. The headline vocabulary consists of 31 million tokens and 69K word types with the average title of length 8.3 words (note that this is significantly shorter than the DUC summaries). On average there are 4.6 overlapping word types between the headline and the input; although only 2.6 in the
first 75-characters of the input.

#### Who are the source language producers?

From the paper:
> For training data for both tasks, we utilize the annotated Gigaword data set (Graff et al., 2003; Napoles et al., 2012), which consists of standard Gigaword, preprocessed with Stanford CoreNLP tools (Manning et al., 2014).

### Annotations

#### Annotation process

Annotations are inherited from the annotatated Gigaword data set.

Additional information from the paper:
> Our model only uses annotations for tokenization and sentence separation, although several of the baselines use parsing and tagging as well.

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

```bibtex
@article{graff2003english,
  title={English gigaword},
  author={Graff, David and Kong, Junbo and Chen, Ke and Maeda, Kazuaki},
  journal={Linguistic Data Consortium, Philadelphia},
  volume={4},
  number={1},
  pages={34},
  year={2003}
}

@article{Rush_2015,
   title={A Neural Attention Model for Abstractive Sentence Summarization},
   url={http://dx.doi.org/10.18653/v1/D15-1044},
   DOI={10.18653/v1/d15-1044},
   journal={Proceedings of the 2015 Conference on Empirical Methods in Natural Language Processing},
   publisher={Association for Computational Linguistics},
   author={Rush, Alexander M. and Chopra, Sumit and Weston, Jason},
   year={2015}
}
```


### Contributions

Thanks to [@lewtun](https://github.com/lewtun), [@lhoestq](https://github.com/lhoestq), [@thomwolf](https://github.com/thomwolf) for adding this dataset.
