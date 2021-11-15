---
annotations_creators:
- expert-generated
language_creators:
- other
languages:
- en
licenses:
- cc-by-sa-3.0
multilinguality:
- monolingual
pretty_name: NQ-Open
size_categories:
- 10K<n<100K
source_datasets:
- extended|natural_questions
task_categories:
- question-answering
task_ids:
- open-domain-qa
paperswithcode_id: null
---

# Dataset Card for nq_open

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

- **Homepage:** https://efficientqa.github.io/
- **Repository:** https://github.com/google-research-datasets/natural-questions/tree/master/nq_open
- **Paper:** https://www.aclweb.org/anthology/P19-1612.pdf
- **Leaderboard:** https://ai.google.com/research/NaturalQuestions/efficientqa
- **Point of Contact:** [Mailing List](efficientqa@googlegroups.com)

### Dataset Summary

The NQ-Open task, introduced by Lee et.al. 2019,
is an open domain question answering benchmark that is derived from Natural Questions.
The goal is to predict an English answer string for an input English question.
All questions can be answered using the contents of English Wikipedia.

### Supported Tasks and Leaderboards

Open Domain Question-Answering, 
EfficientQA Leaderboard: https://ai.google.com/research/NaturalQuestions/efficientqa

### Languages

English (`en`)

## Dataset Structure

### Data Instances

```
{
    "question": "names of the metropolitan municipalities in south africa",
    "answer": [
        "Mangaung Metropolitan Municipality",
        "Nelson Mandela Bay Metropolitan Municipality",
        "eThekwini Metropolitan Municipality",
        "City of Tshwane Metropolitan Municipality",
        "City of Johannesburg Metropolitan Municipality",
        "Buffalo City Metropolitan Municipality",
        "City of Ekurhuleni Metropolitan Municipality"
    ]
}
```

### Data Fields

- `question` - Input open domain question.
- `answer` - List of possible answers to the question

### Data Splits

- Train : 87925
- validation : 1800

## Dataset Creation

### Curation Rationale

[Needs More Information]

### Source Data

#### Initial Data Collection and Normalization

Natural Questions contains question from aggregated queries to Google Search (Kwiatkowski et al., 2019). To gather an open version of this dataset, we only keep questions with short answers and discard the given evidence document. Answers with many tokens often resemble extractive snippets rather than canonical answers, so we discard answers with more than 5 tokens.

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

Evaluating on this diverse set of question-answer pairs is crucial, because all existing datasets have inherent biases that are problematic for open domain QA systems with learned retrieval. 
In the Natural Questions dataset the question askers do not already know the answer. This accurately reflects a distribution of genuine information-seeking questions.
However, annotators must separately find correct answers, which requires assistance from automatic tools and can introduce a moderate bias towards results from the tool.

### Other Known Limitations

[Needs More Information]

## Additional Information

### Dataset Curators

[Needs More Information]

### Licensing Information

All of the Natural Questions data is released under the
[CC BY-SA 3.0](https://creativecommons.org/licenses/by-sa/3.0/) license.

### Citation Information

```
@article{doi:10.1162/tacl\_a\_00276,
    author = {Kwiatkowski, Tom and Palomaki, Jennimaria and Redfield, Olivia and Collins, Michael and Parikh, Ankur and Alberti, Chris and Epstein, Danielle and Polosukhin, Illia and Devlin, Jacob and Lee, Kenton and Toutanova, Kristina and Jones, Llion and Kelcey, Matthew and Chang, Ming-Wei and Dai, Andrew                         M. and Uszkoreit, Jakob and Le, Quoc and Petrov, Slav},
    title = {Natural Questions: A Benchmark for Question Answering Research},
    journal = {Transactions of the Association for Computational Linguistics},
    volume = {7},
    number = {},
    pages = {453-466},
    year = {2019},
    doi = {10.1162/tacl\_a\_00276},
    URL = { 
            https://doi.org/10.1162/tacl_a_00276
        },
    eprint = { 
            https://doi.org/10.1162/tacl_a_00276
        
        },
    abstract = { We present the Natural Questions corpus, a question answering data set. Questions consist of real anonymized, aggregated queries issued to the Google search engine. An annotator is presented with a question along with a Wikipedia page from the top 5 search results, and annotates a long answer (typically a paragraph) and a short answer (one or more entities) if present on the page, or marks null if no long/short answer is present. The public release consists of 307,373 training examples with single annotations; 7,830 examples with 5-way annotations for development data; and a further 7,842 examples with 5-way annotated sequestered as test data. We present experiments validating quality of the data. We also describe analysis of 25-way annotations on 302 examples, giving insights into human variability on the annotation task. We introduce robust metrics for the purposes of evaluating question answering systems; demonstrate high human upper bounds on these metrics; and establish baseline results using competitive methods drawn from related literature. }
}

@inproceedings{lee-etal-2019-latent,
    title = "Latent Retrieval for Weakly Supervised Open Domain Question Answering",
    author = "Lee, Kenton  and
      Chang, Ming-Wei  and
      Toutanova, Kristina",
    booktitle = "Proceedings of the 57th Annual Meeting of the Association for Computational Linguistics",
    month = jul,
    year = "2019",
    address = "Florence, Italy",
    publisher = "Association for Computational Linguistics",
    url = "https://www.aclweb.org/anthology/P19-1612",
    doi = "10.18653/v1/P19-1612",
    pages = "6086--6096",
    abstract = "Recent work on open domain question answering (QA) assumes strong supervision of the supporting evidence and/or assumes a blackbox information retrieval (IR) system to retrieve evidence candidates. We argue that both are suboptimal, since gold evidence is not always available, and QA is fundamentally different from IR. We show for the first time that it is possible to jointly learn the retriever and reader from question-answer string pairs and without any IR system. In this setting, evidence retrieval from all of Wikipedia is treated as a latent variable. Since this is impractical to learn from scratch, we pre-train the retriever with an Inverse Cloze Task. We evaluate on open versions of five QA datasets. On datasets where the questioner already knows the answer, a traditional IR system such as BM25 is sufficient. On datasets where a user is genuinely seeking an answer, we show that learned retrieval is crucial, outperforming BM25 by up to 19 points in exact match.",
}
```

### Contributions

Thanks to [@Nilanshrajput](https://github.com/Nilanshrajput) for adding this dataset.
