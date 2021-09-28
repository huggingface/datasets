---
annotations_creators:
- expert-generated
language_creators:
- expert-generated
languages:
- en-US
licenses:
- mit
multilinguality:
- monolingual
pretty_name: competition_math
size_categories:
- unknown
source_datasets:
- original
task_categories:
- conditional-text-generation
task_ids:
- explanation-generation
---

# Dataset Card for Mathematics Aptitude Test of Heuristics (MATH) dataset

## Table of Contents
- [Table of Contents](#table-of-contents)
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

- **Homepage:** https://github.com/hendrycks/math
- **Repository:** https://github.com/hendrycks/math
- **Paper:** https://arxiv.org/pdf/2103.03874.pdf
- **Leaderboard:** N/A
- **Point of Contact:** Dan Hendrycks

### Dataset Summary

The Mathematics Aptitude Test of Heuristics (MATH) dataset consists of problems
from mathematics competitions, including the AMC 10, AMC 12, AIME, and more. 
Each problem in MATH has a full step-by-step solution, which can be used to teach
models to generate answer derivations and explanations.

### Supported Tasks and Leaderboards

[More Information Needed]

### Languages

[More Information Needed]

## Dataset Structure

### Data Instances

A data instance consists of a competition math problem and its step-by-step solution written in LaTeX and natural language. The step-by-step solution contains the final answer enclosed in LaTeX's `\boxed` tag.

### Data Fields

* `problem`: The competition math problem.
* `solution`: The step-by-step solution.
* `level`: The problem's difficulty level from 'Level 1' to 'Level 5', where a subject's easiest problems for humans are assigned to 'Level 1' and a subject's hardest problems are assigned to 'Level 5'.
* `type`: The subject of the problem: Algebra, Counting & Probability, Geometry, Intermediate Algebra, Number Theory, Prealgebra and Precalculus.

### Data Splits

* train: 7,500 examples
* test: 5,000 examples

## Dataset Creation

### Curation Rationale

[More Information Needed]

### Source Data

#### Initial Data Collection and Normalization

[More Information Needed]

#### Who are the source language producers?

[More Information Needed]

### Annotations

#### Annotation process

[More Information Needed]

#### Who are the annotators?

[More Information Needed]

### Personal and Sensitive Information

[More Information Needed]

## Considerations for Using the Data

### Social Impact of Dataset

[More Information Needed]

### Discussion of Biases

[More Information Needed]

### Other Known Limitations

[More Information Needed]

## Additional Information

### Dataset Curators

[More Information Needed]

### Licensing Information

https://github.com/hendrycks/math/blob/main/LICENSE

### Citation Information

    @article{hendrycksmath2021,
      title={Measuring Mathematical Problem Solving With the MATH Dataset},
      author={Dan Hendrycks
        and Collin Burns
        and Saurav Kadavath
        and Akul Arora
        and Steven Basart
        and Eric Tang
        and Dawn Song
        and Jacob Steinhardt},
      journal={arXiv preprint arXiv:2103.03874},
      year={2021}
    }

### Contributions

Thanks to [@hacobe](https://github.com/hacobe) for adding this dataset.
