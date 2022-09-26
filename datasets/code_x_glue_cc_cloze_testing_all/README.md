---
annotations_creators:
- found
language_creators:
- found
language:
- code
license:
- c-uda
multilinguality:
- monolingual
size_categories:
- 10K<n<100K
- 1K<n<10K
source_datasets:
- original
task_categories:
- text-generation
- fill-mask
task_ids:
- slot-filling
pretty_name: CodeXGlueCcClozeTestingAll
configs:
- go
- java
- javascript
- php
- python
- ruby
---
# Dataset Card for "code_x_glue_cc_cloze_testing_all"

## Table of Contents
- [Dataset Description](#dataset-description)
  - [Dataset Summary](#dataset-summary)
  - [Supported Tasks and Leaderboards](#supported-tasks)
  - [Languages](#languages)
- [Dataset Structure](#dataset-structure)
  - [Data Instances](#data-instances)
  - [Data Fields](#data-fields)
  - [Data Splits](#data-splits-sample-size)
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

- **Homepage:** https://github.com/microsoft/CodeXGLUE/tree/main/Code-Code/ClozeTesting-all

### Dataset Summary

CodeXGLUE ClozeTesting-all dataset, available at https://github.com/microsoft/CodeXGLUE/tree/main/Code-Code/ClozeTesting-all

Cloze tests are widely adopted in Natural Languages Processing to evaluate the performance of the trained language models. The task is aimed to predict the answers for the blank with the context of the blank, which can be formulated as a multi-choice classification problem.
Here we present the two cloze testing datasets in code domain with six different programming languages: ClozeTest-maxmin and ClozeTest-all. Each instance in the dataset contains a masked code function, its docstring and the target word.
The only difference between ClozeTest-maxmin and ClozeTest-all is their selected words sets, where ClozeTest-maxmin only contains two words while ClozeTest-all contains 930 words.

### Supported Tasks and Leaderboards

- `slot-filling`: The dataset can be used to train a model for predicting the missing token from a piece of code, similar to the Cloze test.

### Languages

- Go **programming** language
- Java **programming** language
- Javascript **programming** language
- PHP **programming** language
- Python **programming** language
- Ruby **programming** language

## Dataset Structure

### Data Instances

#### go

An example of 'train' looks as follows.
```
{
    "id": 0, 
    "idx": "all-1", 
    "nl_tokens": ["MarshalJSON", "supports", "json", ".", "Marshaler", "interface"], 
    "pl_tokens": ["func", "(", "v", "ContextRealtimeData", ")", "MarshalJSON", "(", ")", "(", "[", "]", "byte", ",", "error", ")", "{", "w", ":=", "jwriter", ".", "<mask>", "{", "}", "\n", "easyjsonC5a4559bEncodeGithubComChromedpCdprotoWebaudio7", "(", "&", "w", ",", "v", ")", "\n", "return", "w", ".", "Buffer", ".", "BuildBytes", "(", ")", ",", "w", ".", "Error", "\n", "}"]
}
```

#### java

An example of 'train' looks as follows.
```
{
    "id": 0, 
    "idx": "all-1", 
    "nl_tokens": ["/", "*", "(", "non", "-", "Javadoc", ")"], 
    "pl_tokens": ["@", "Override", "public", "int", "peekBit", "(", ")", "throws", "AACException", "{", "int", "ret", ";", "if", "(", "bitsCached", ">", "0", ")", "{", "ret", "=", "(", "cache", ">>", "(", "bitsCached", "-", "1", ")", ")", "&", "1", ";", "}", "else", "{", "final", "int", "word", "=", "readCache", "(", "true", ")", ";", "ret", "=", "(", "<mask>", ">>", "WORD_BITS", "-", "1", ")", "&", "1", ";", "}", "return", "ret", ";", "}"]
}
```

#### javascript

An example of 'train' looks as follows.
```
{
    "id": 0, 
    "idx": "all-1", 
    "nl_tokens": ["Cast", "query", "params", "according", "to", "type"], 
    "pl_tokens": ["function", "castQueryParams", "(", "relId", ",", "data", ",", "{", "relationships", "}", ")", "{", "const", "relationship", "=", "relationships", "[", "relId", "]", "if", "(", "!", "relationship", ".", "query", ")", "{", "return", "{", "}", "}", "return", "Object", ".", "keys", "(", "relationship", ".", "query", ")", ".", "reduce", "(", "(", "params", ",", "<mask>", ")", "=>", "{", "const", "value", "=", "getField", "(", "data", ",", "relationship", ".", "query", "[", "key", "]", ")", "if", "(", "value", "===", "undefined", ")", "{", "throw", "new", "TypeError", "(", "'Missing value for query param'", ")", "}", "return", "{", "...", "params", ",", "[", "key", "]", ":", "value", "}", "}", ",", "{", "}", ")", "}"]
}
```

#### php

An example of 'train' looks as follows.
```
{
    "id": 0, 
    "idx": "all-1", 
    "nl_tokens": ["Get", "choices", "."], 
    "pl_tokens": ["protected", "<mask>", "getChoices", "(", "FormFieldTranslation", "$", "translation", ")", "{", "$", "choices", "=", "preg_split", "(", "'/\\r\\n|\\r|\\n/'", ",", "$", "translation", "->", "getOption", "(", "'choices'", ")", ",", "-", "1", ",", "PREG_SPLIT_NO_EMPTY", ")", ";", "return", "array_combine", "(", "$", "choices", ",", "$", "choices", ")", ";", "}"]
}
```

#### python

An example of 'train' looks as follows.
```
{
    "id": 0, 
    "idx": "all-1", 
    "nl_tokens": ["Post", "a", "review"], 
    "pl_tokens": ["def", "post_review", "(", "session", ",", "review", ")", ":", "# POST /api/projects/0.1/reviews/", "<mask>", "=", "make_post_request", "(", "session", ",", "'reviews'", ",", "json_data", "=", "review", ")", "json_data", "=", "response", ".", "json", "(", ")", "if", "response", ".", "status_code", "==", "200", ":", "return", "json_data", "[", "'status'", "]", "else", ":", "raise", "ReviewNotPostedException", "(", "message", "=", "json_data", "[", "'message'", "]", ",", "error_code", "=", "json_data", "[", "'error_code'", "]", ",", "request_id", "=", "json_data", "[", "'request_id'", "]", ")"]
}
```

#### ruby

An example of 'train' looks as follows.
```
{
    "id": 0, 
    "idx": "all-1", 
    "nl_tokens": ["By", "default", "taskers", "don", "t", "see", "the", "flor", "variables", "in", "the", "execution", ".", "If", "include_vars", "or", "exclude_vars", "is", "present", "in", "the", "configuration", "of", "the", "tasker", "some", "or", "all", "of", "the", "variables", "are", "passed", "."], 
    "pl_tokens": ["def", "gather_vars", "(", "executor", ",", "tconf", ",", "message", ")", "# try to return before a potentially costly call to executor.vars(nid)", "return", "nil", "if", "(", "tconf", ".", "keys", "&", "%w[", "include_vars", "exclude_vars", "]", ")", ".", "empty?", "# default behaviour, don't pass variables to taskers", "iv", "=", "expand_filter", "(", "tconf", "[", "'include_vars'", "]", ")", "return", "nil", "if", "iv", "==", "false", "ev", "=", "expand_filter", "(", "tconf", "[", "'exclude_vars'", "]", ")", "return", "{", "}", "if", "ev", "==", "true", "vars", "=", "executor", ".", "vars", "(", "message", "[", "'nid'", "]", ")", "return", "vars", "if", "iv", "==", "true", "vars", "=", "vars", ".", "select", "{", "|", "k", ",", "v", "|", "var_match", "(", "k", ",", "iv", ")", "}", "if", "<mask>", "vars", "=", "vars", ".", "reject", "{", "|", "k", ",", "v", "|", "var_match", "(", "k", ",", "ev", ")", "}", "if", "ev", "vars", "end"]
}
```

### Data Fields

In the following each data field in go is explained for each config. The data fields are the same among all splits.

#### go, java, javascript, php, python, ruby

|field name|      type      |         description          |
|----------|----------------|------------------------------|
|id        |int32           | Index of the sample          |
|idx       |string          | Original index in the dataset|
|nl_tokens |Sequence[string]| Natural language tokens      |
|pl_tokens |Sequence[string]| Programming language tokens  |

### Data Splits

|   name   |train|
|----------|----:|
|go        |25282|
|java      |40492|
|javascript|13837|
|php       |51930|
|python    |40137|
|ruby      | 4437|

## Dataset Creation

### Curation Rationale

[More Information Needed]

### Source Data

#### Initial Data Collection and Normalization

Data from CodeSearchNet Challenge dataset.
[More Information Needed]

#### Who are the source language producers?

Software Engineering developers.

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

https://github.com/microsoft, https://github.com/madlag

### Licensing Information

Computational Use of Data Agreement (C-UDA) License.

### Citation Information

```
@article{CodeXGLUE,
  title={CodeXGLUE: An Open Challenge for Code Intelligence},
  journal={arXiv},
  year={2020},
}
@article{feng2020codebert,
  title={CodeBERT: A Pre-Trained Model for Programming and Natural Languages},
  author={Feng, Zhangyin and Guo, Daya and Tang, Duyu and Duan, Nan and Feng, Xiaocheng and Gong, Ming and Shou, Linjun and Qin, Bing and Liu, Ting and Jiang, Daxin and others},
  journal={arXiv preprint arXiv:2002.08155},
  year={2020}
}
@article{husain2019codesearchnet,
  title={CodeSearchNet Challenge: Evaluating the State of Semantic Code Search},
  author={Husain, Hamel and Wu, Ho-Hsiang and Gazit, Tiferet and Allamanis, Miltiadis and Brockschmidt, Marc},
  journal={arXiv preprint arXiv:1909.09436},
  year={2019}
}
```

### Contributions

Thanks to @madlag (and partly also @ncoop57) for adding this dataset.
