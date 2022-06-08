---
pretty_name: SEDE (Stack Exchange Data Explorer)
annotations_creators:
- no-annotation
language_creators:
- found
languages:
- en
licenses:
- apache-2.0
multilinguality:
- monolingual
paperswithcode_id: sede
size_categories:
- 10K<n<100K
source_datasets:
- original
task_categories:
- token-classification
task_ids:
- parsing
---

# Dataset Card for SEDE

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

- **Repository:** https://github.com/hirupert/sede
- **Paper:** https://arxiv.org/abs/2106.05006
- **Leaderboard:** https://paperswithcode.com/sota/text-to-sql-on-sede
- **Point of Contact:** [email](moshe@hirupert.com)

### Dataset Summary

SEDE (Stack Exchange Data Explorer) is a dataset for Text-to-SQL tasks with more than 12,000 SQL queries and their natural language description. It's based on a real usage of users from the Stack Exchange Data Explorer platform, which brings complexities and challenges never seen before in any other semantic parsing dataset like including complex nesting, dates manipulation, numeric and text manipulation, parameters, and most importantly: under-specification and hidden-assumptions.

### Supported Tasks and Leaderboards

- `parsing`: The dataset can be used to train a model for Text-to-SQL task. A Seq2Seq model (e.g. T5) can be used to solve the task. A model with more inductive-bias (e.g. a model with a grammar-based decoder) or an interactive settings for Text-to-SQL (https://arxiv.org/abs/2005.02539) can improve the results further. The model performance is measured by how high its [PCM-F1](https://arxiv.org/abs/2106.05006) score is. A [t5-large](https://huggingface.co/t5-large) achieves a [PCM-F1 of 50.6](https://arxiv.org/abs/2106.05006).

### Languages

The text in the dataset is in English. The associated BCP-47 code is `en`.

## Dataset Structure

### Data Instances

A typical data point comprises a question title, (optionally) a description and its underlying SQL query. In addition, each sample has a unique ID (from the Stack Exchange Data Explorer), its creation date and a boolean flag named `validated` if this sample was validated to be in gold quality by humans, see the paper for full details regarding the `validated` flag.

An instance for example:

```
{
   'QuerySetId':1233,
   'Title':'Top 500 Askers on the site',
   'Description':'A list of the top 500 askers of questions ordered by average answer score excluding community wiki closed posts.',
   'QueryBody':'SELECT  * FROM (\nSELECT \n    TOP 500\n    OwnerUserId as [User Link],\n    Count(Posts.Id) AS Questions,\n    CAST(AVG(CAST(Score AS float)) as numeric(6,2)) AS [Average Question Score]\nFROM\n    Posts\nWHERE \n    PostTypeId = 1 and CommunityOwnedDate is null and ClosedDate is null\nGROUP BY\n    OwnerUserId\nORDER BY\n    Count(Posts.Id) DESC\n)ORDER BY\n    [Average Question Score] DESC',
   'CreationDate':'2010-05-27 20:08:16',
   'validated':true
}
```

### Data Fields

- QuerySetId: a unique ID coming from the Stack Exchange Data Explorer.
- Title: utterance title.
- Description: utterance description (might be empty).
- QueryBody: the underlying SQL query.
- CreationDate: when this sample was created.
- validated: `true` if this sample was validated to be in gold quality by humans.

### Data Splits

The data is split into a training, validation and test set. The validation and test set contain only samples that were validated by humans to be in gold quality.

Train Valid Test
10309 857 857

## Dataset Creation

### Curation Rationale

Most available semantic parsing datasets, comprising of pairs of natural utterances and logical forms, were collected solely for the purpose of training and evaluation of natural language understanding systems. As a result, they do not contain any of the richness and variety of natural-occurring utterances, where humans ask about data they need or are curious about. SEDE contains a variety of real-world challenges which were rarely reflected so far in any other semantic parsing dataset. There is a large gap between the performance on SEDE compared to other common datasets, which leaves a room for future research for generalisation of Text-to-SQL models.

### Source Data

#### Initial Data Collection and Normalization

To introduce a realistic Text-to-SQL benchmark, we gather SQL queries together with their titles and descriptions from a naturally occurring dataset: the Stack Exchange Data Explorer. Stack Exchange is an online question & answers community, with over 3 million questions asked. However in its raw form many of the rows are duplicated or contain unusable queries or titles. The reason for this large difference between the original data size and the cleaned version is that any time that the author of the query executes it, an entry is saved to the log. To alleviate these issues, we write rule-based filters that remove bad queries/descriptions pairs with high precision. For example, we filter out examples with numbers in the description, if these numbers do not appear in the query (refer to the preprocessing script in the repository for the complete list of filters and the number of examples each of them filter). Whenever a query has multiple versions due to multiple executions, we take the last executed query which passed all filters. After this filtering step, we are left with 12,309 examples. Using these filters cleans most of the noise, but not all of it. To complete the cleaning process, we manually go over the examples in the validation and test sets, and either filter-out wrong examples or perform minimal changes to either the utterances or the queries (for example, fix a wrong textual value) to ensure that models are evaluated with correct data. The final number of all training, validation and test examples is 12,023.

#### Who are the source language producers?

The language producers are Stack Exchange Data Explorer (https://data.stackexchange.com/) users.

### Annotations

#### Annotation process

[N/A]

#### Who are the annotators?

[N/A]

### Personal and Sensitive Information

All the data in the dataset is for public use.

## Considerations for Using the Data

### Social Impact of Dataset

We hope that the release of this challenging dataset will encourage research on improving generalisation for real-world SQL prediction that will help non technical business users acquire the data they need from their company's database.

### Discussion of Biases

[N/A]

### Other Known Limitations

[Needs More Information]

## Additional Information

### Dataset Curators

The dataset was initially created by Moshe Hazoom, Vibhor Malik and Ben Bogin, during work done at Ruper.

### Licensing Information

Apache-2.0 License

### Citation Information

```
@misc{hazoom2021texttosql,
      title={Text-to-SQL in the Wild: A Naturally-Occurring Dataset Based on Stack Exchange Data},
      author={Moshe Hazoom and Vibhor Malik and Ben Bogin},
      year={2021},
      eprint={2106.05006},
      archivePrefix={arXiv},
      primaryClass={cs.CL}
}
```

### Contributions
Thanks to [@Hazoom](https://github.com/Hazoom) for adding this dataset.