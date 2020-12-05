---
- YAML tags: copy-paste the tags obtained with the tagging app: http://34.68.228.168:8501/ or https://github.com/huggingface/datasets-tagging for local tagging
---

# Dataset Card Creation Guide

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

- **Homepage:** [Add homepage URL here if available (unless it's a GitHub repository)]()
- **Repository:** [If the dataset is hosted on github or has a github homepage, add URL here]()
- **Paper:** [If the dataset was introduced by a paper or there was a paper written describing the dataset, add URL here (landing page for Arxiv paper preferred)]()
- **Leaderboard:** [If the dataset supports an active leaderboard, add link here]()
- **Point of Contact:** [If known, name and email of at least one person the reader can contact for questions about the dataset.]()

### Dataset Summary

Briefly summarize the dataset, its intended use and the supported tasks. Give an overview of how and why the dataset was created. The summary should explicitly mention the languages present in the dataset (possibly in broad terms, e.g. *translations between several pairs of European languages*), and describe the domain, topic, or genre covered.

### Supported Tasks and Leaderboards

For each of the tasks tagged for this dataset, give a brief description of the tag, metrics, and suggested models (with a link to their HuggingFace implementation if available). Give a similar description of tasks that were not covered by the structured tag set (repace the `task-category-tag` with an appropriate `other:other-task-name`).

- `task-category-tag`: The dataset can be used to train a model for [TASK NAME], which consists in [TASK DESCRIPTION]. Success on this task is typically measured by achieving a *high/low* [metric name](https://huggingface.co/metrics/metric_name). The ([model name](https://huggingface.co/model_name) or [model class](https://huggingface.co/transformers/model_doc/model_class.html)) model currently achieves the following score. *[IF A LEADERBOARD IS AVAILABLE]:* This task has an active leaderboard which can be found at [leaderboard url]() and ranks models based on [metric name](https://huggingface.co/metrics/metric_name) while also reporting [other metric name](https://huggingface.co/metrics/other_metric_name).

### Languages

Provide a brief overview of the languages represented in the dataset. Describe relevant details about specifics of the language such as whether it is social media text, African American English,...

When relevant, please provide [BCP-47 codes](https://tools.ietf.org/html/bcp47), which consist of a [primary language subtag](https://tools.ietf.org/html/bcp47#section-2.2.1), with a [script subtag](https://tools.ietf.org/html/bcp47#section-2.2.3) and/or [region subtag](https://tools.ietf.org/html/bcp47#section-2.2.4) if available.

## Dataset Structure

### Data Instances

Provide an JSON-formatted example and brief description of a typical instance in the dataset. If available, provide a link to further examples.

```
{
  'example_field': ...,
  ...
}
```

Provide any additional information that is not covered in the other sections about the data here. In particular describe any relationships between data points and if these relationships are made explicit.

### Data Fields

List and describe the fields present in the dataset. Mention their data type, and whether they are used as input or output in any of the tasks the dataset currently supports. If the data has span indices, describe their attributes, such as whether they are at the character level or word level, whether they are contiguous or not, etc. If the datasets contains example IDs, state whether they have an inherent meaning, such as a mapping to other datasets or pointing to relationships between data points.

- `example_field`: description of `example_field`

### Data Splits

Describe and name the splits in the dataset if there are more than one.

Describe any criteria for splitting the data, if used. If their are differences between the splits (e.g. if the training annotations are machine-generated and the dev and test ones are created by humans, or if different numbers of annotators contributed to each example), describe them here.

Provide the sizes of each split. As appropriate, provide any descriptive statistics for the features, such as average length.  For example:

|                            | Tain   | Valid | Test |
| -----                      | ------ | ----- | ---- |
| Input Sentences            |        |       |      |
| Average Sentence Length    |        |       |      |

## Dataset Creation

### Curation Rationale

What need motivated the creation of this dataset? What are some of the reasons underlying the major choices involved in putting it together?

### Source Data

This section describes the source data (e.g. news text and headlines, social media posts, translated sentences,...)

#### Initial Data Collection and Normalization

Describe the data collection process. Describe any criteria for data selection or filtering. List any key words or search terms used. If possible, include runtime information for the collection process.

If data was collected from other pre-existing datasets, link to source here and to their [Hugging Face version](https://huggingface.co/datasets/dataset_name).

If the data was modified or normalized after being collected (e.g. if the data is word-tokenized), describe the process and the tools used.

#### Who are the source language producers?

State whether the data was produced by humans or machine generated. Describe the people or systems who originally created the data.

If available, include self-reported demographic or identity information for the source data creators, but avoid inferring this information. Instead state that this information is unknown. See [Larson 2017](https://www.aclweb.org/anthology/W17-1601.pdf) for using identity categories as a variables, particularly gender.

Describe the conditions under which the data was created (for example, if the producers were crowdworkers, state what platform was used, or if the data was found, what website the data was found on). If compensation was provided, include that information here.

Describe other people represented or mentioned in the data. Where possible, link to references for the information.

### Annotations

If the dataset contains annotations which are not part of the initial data collection, describe them in the following paragraphs.

#### Annotation process

If applicable, describe the annotation process and any tools used, or state otherwise. Describe the amount of data annotated, if not all. Describe or reference annotation guidelines provided to the annotators. If available, provide interannotator statistics. Describe any annotation validation processes.

#### Who are the annotators?

If annotations were collected for the source data (such as class labels or syntactic parses), state whether the annotations were produced by humans or machine generated.

Describe the people or systems who originally created the annotations and their selection criteria if applicable.

If available, include self-reported demographic or identity information for the annotators, but avoid inferring this information. Instead state that this information is unknown. See [Larson 2017](https://www.aclweb.org/anthology/W17-1601.pdf) for using identity categories as a variables, particularly gender.

Describe the conditions under which the data was annotated (for example, if the annotators were crowdworkers, state what platform was used, or if the data was found, what website the data was found on). If compensation was provided, include that information here.

### Personal and Sensitive Information

State whether the dataset uses identity categories and, if so, how the information is used. Describe where this information comes from (i.e. self-reporting, collecting from profiles, inferring, etc.). See [Larson 2017](https://www.aclweb.org/anthology/W17-1601.pdf) for using identity categories as a variables, particularly gender. State whether the data is linked to individuals and whether those individuals can be identified in the dataset, either directly or indirectly (i.e., in combination with other data).

State whether the dataset contains other data that might be considered sensitive (e.g., data that reveals racial or ethnic origins, sexual orientations, religious beliefs, political opinions or union memberships, or locations; financial or health data; biometric or genetic data; forms of government identification, such as social security numbers; criminal history).  

If efforts were made to anonymize the data, describe the anonymization process.

## Considerations for Using the Data

### Social Impact of Dataset

Please discuss some of the ways you believe the use of this dataset will impact society.

The statement should include both positive outlooks, such as outlining how technologies developed through its use may improve people's lives, and discuss the accompanying risks. These risks may range from making important decisions more opaque to people who are affected by the technology, to reinforcing existing harmful biases (whose specifics should be discussed in the next section), among other considerations.

Please also mention in this section if the proposed dataset contains a *low-resource* or under-represented language.

### Discussion of Biases

Provide descriptions of specific biases that are likely to be reflected in the data, and state whether any steps were taken to reduce their impact.

For Wikipedia text, see for example [Dinan et al 2020 on biases in Wikipedia (esp. Table 1)](https://arxiv.org/abs/2005.00614), or [Blodgett et al 2020](https://www.aclweb.org/anthology/2020.acl-main.485/) for a more general discussion of the topic.

If analyses have been run quantifying these biases, please add brief summaries and links to the studies here.

### Other Known Limitations

If studies of the datasets have outlined other limitations of the dataset, such as annotation artifacts, please outline and cite them here.

## Additional Information

### Dataset Curators

List the people involved in collecting the dataset and their affiliation(s). If funding information is known, include it here.

### Licensing Information

Provide the license and link to the license webpage if available.

### Citation Information

Provide the [BibTex](http://www.bibtex.org/)-formatted reference for the dataset. For example:
```
@article{article_id,
  author    = {Author List},
  title     = {Dataset Paper Title},
  journal   = {Publication Venue},
  year      = {2525}
}
```

If the dataset has a [DOI](https://www.doi.org/), please provide it here.
