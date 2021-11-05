---
pretty_name: PyAst
annotations_creators:
- machine-generated
language_creators:
- found
languages:
- code
licenses:
- 0bsd
- mit
multilinguality:
- monolingual
size_categories:
- 100K<n<1M
source_datasets:
- original
task_categories:
- sequence-modeling
task_ids:
- sequence-modeling-code-modeling
paperswithcode_id: null
---
# Dataset Card for [py_ast]

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

- **homepage**: [py150](https://www.sri.inf.ethz.ch/py150) 
- **Paper**: [Probabilistic Model for Code with Decision Trees](https://dl.acm.org/doi/10.1145/3022671.2984041)
- **Leaderboard:**
- **Point of Contact:**

### Dataset Summary

The dataset consists of parsed Parsed ASTs that were used to train and evaluate the DeepSyn tool. 
The Python programs are collected from GitHub repositories
by removing duplicate files, removing project forks (copy of another existing repository)
,keeping only programs that parse and have at most 30'000 nodes in the AST and 
we aim to remove obfuscated files

### Supported Tasks and Leaderboards

Code Representation, Unsupervised Learning
### Languages

Python
## Dataset Structure  

### Data Instances
A typical datapoint contains an AST of a python program, parsed.   
The main key is `ast` wherein every program's AST is stored.  
 Each children would have,  
`type` which will formulate the type of the node.   
 `children` which enumerates if a given node has children(non-empty list). 
 `value`, if the given node has any hardcoded value(else "N/A").
 An example would be,     
'''
[ {"type":"Module","children":[1,4]},{"type":"Assign","children":[2,3]},{"type":"NameStore","value":"x"},{"type":"Num","value":"7"},    {"type":"Print","children":[5]},      {"type":"BinOpAdd","children":[6,7]},        {"type":"NameLoad","value":"x"},        {"type":"Num","value":"1"} ]
'''
### Data Fields
- `ast`: a list of dictionaries, wherein every dictionary is a node in the Abstract Syntax Tree.
- `type`: explains the type of the node.
- `children`: list of nodes which are children under the given
- `value`: hardcoded value, if the node holds an hardcoded value.

### Data Splits

The data is split into a training and test set.   
The final split sizes are as follow:

|                             | Tain   | Valid |
| -----                       | ------ | ----- |
| py_ast examples| 100000 |  50000 |
## Dataset Creation
[More Information Needed]
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
Raychev, V., Bielik, P., and Vechev, M
### Licensing Information
MIT, BSD and Apache
### Citation Information
@InProceedings{OOPSLA ’16, ACM,
title = {Probabilistic Model for Code with Decision Trees.},
authors={Raychev, V., Bielik, P., and Vechev, M.},
year={2016}
}

### Contributions

Thanks to [@reshinthadithyan](https://github.com/reshinthadithyan) for adding this dataset.