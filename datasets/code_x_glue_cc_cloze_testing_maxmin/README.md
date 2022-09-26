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
pretty_name: CodeXGlueCcClozeTestingMaxmin
configs:
- go
- java
- javascript
- php
- python
- ruby
---
# Dataset Card for "code_x_glue_cc_cloze_testing_maxmin"

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

- **Homepage:** https://github.com/microsoft/CodeXGLUE/tree/main/Code-Code/ClozeTesting-maxmin

### Dataset Summary

CodeXGLUE ClozeTesting-maxmin dataset, available at https://github.com/microsoft/CodeXGLUE/tree/main/Code-Code/ClozeTesting-maxmin

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
    "idx": "maxmin-1", 
    "nl_tokens": ["SetMaxStructPoolSize", "sets", "the", "struct", "pools", "max", "size", ".", "this", "may", "be", "usefull", "for", "fine", "grained", "performance", "tuning", "towards", "your", "application", "however", "the", "default", "should", "be", "fine", "for", "nearly", "all", "cases", ".", "only", "increase", "if", "you", "have", "a", "deeply", "nested", "struct", "structure", ".", "NOTE", ":", "this", "method", "is", "not", "thread", "-", "safe", "NOTE", ":", "this", "is", "only", "here", "to", "keep", "compatibility", "with", "v5", "in", "v6", "the", "method", "will", "be", "removed"], 
    "pl_tokens": ["func", "(", "v", "*", "Validate", ")", "SetMaxStructPoolSize", "(", "<mask>", "int", ")", "{", "structPool", "=", "&", "sync", ".", "Pool", "{", "New", ":", "newStructErrors", "}", "\n", "}"]
}
```

#### java

An example of 'train' looks as follows.
```
{
    "id": 0, 
    "idx": "maxmin-1", 
    "nl_tokens": ["Test", "whether", "find", "can", "be", "found", "at", "position", "startPos", "in", "the", "string", "src", "."], 
    "pl_tokens": ["public", "static", "boolean", "startsWith", "(", "char", "[", "]", "src", ",", "char", "[", "]", "find", ",", "int", "startAt", ")", "{", "int", "startPos", "=", "startAt", ";", "boolean", "result", "=", "true", ";", "// Check ranges", "if", "(", "src", ".", "length", "<", "startPos", "+", "find", ".", "length", ")", "{", "result", "=", "false", ";", "}", "else", "{", "final", "int", "<mask>", "=", "find", ".", "length", ";", "for", "(", "int", "a", "=", "0", ";", "a", "<", "max", "&&", "result", ";", "a", "++", ")", "{", "if", "(", "src", "[", "startPos", "]", "!=", "find", "[", "a", "]", ")", "{", "result", "=", "false", ";", "}", "startPos", "++", ";", "}", "}", "return", "result", ";", "}"]
}
```

#### javascript

An example of 'train' looks as follows.
```
{
    "id": 0, 
    "idx": "maxmin-1", 
    "nl_tokens": ["string", ".", "max", "Maximum", "length", "of", "the", "string"], 
    "pl_tokens": ["function", "(", "string", ")", "{", "// string.check check sting type and size", "return", "(", "(", "typeof", "string", "===", "'string'", "||", "string", "instanceof", "String", ")", "&&", "string", ".", "length", ">=", "this", ".", "<mask>", "&&", "string", ".", "length", "<=", "this", ".", "max", "&&", "(", "!", "this", ".", "match", "||", "string", ".", "match", "(", "this", ".", "match", ")", ")", ")", ";", "}"]
}
```

#### php

An example of 'train' looks as follows.
```
{
    "id": 0, 
    "idx": "maxmin-1", 
    "nl_tokens": ["Read", "the", "next", "character", "from", "the", "supplied", "string", ".", "Return", "null", "when", "we", "have", "run", "out", "of", "characters", "."], 
    "pl_tokens": ["public", "function", "readOne", "(", ")", "{", "if", "(", "$", "this", "->", "pos", "<=", "$", "this", "->", "<mask>", ")", "{", "$", "value", "=", "$", "this", "->", "string", "[", "$", "this", "->", "pos", "]", ";", "$", "this", "->", "pos", "+=", "1", ";", "}", "else", "{", "$", "value", "=", "null", ";", "}", "return", "$", "value", ";", "}"]
}
```

#### python

An example of 'train' looks as follows.
```
{
    "id": 0, 
    "idx": "maxmin-1", 
    "nl_tokens": ["Returns", "intermediary", "colors", "for", "given", "list", "of", "colors", "."], 
    "pl_tokens": ["def", "_interpolate", "(", "self", ",", "colors", ",", "n", "=", "100", ")", ":", "gradient", "=", "[", "]", "for", "i", "in", "_range", "(", "n", ")", ":", "l", "=", "len", "(", "colors", ")", "-", "1", "x", "=", "int", "(", "1.0", "*", "i", "/", "n", "*", "l", ")", "x", "=", "<mask>", "(", "x", "+", "0", ",", "l", ")", "y", "=", "min", "(", "x", "+", "1", ",", "l", ")", "base", "=", "1.0", "*", "n", "/", "l", "*", "x", "d", "=", "(", "i", "-", "base", ")", "/", "(", "1.0", "*", "n", "/", "l", ")", "r", "=", "colors", "[", "x", "]", ".", "r", "*", "(", "1", "-", "d", ")", "+", "colors", "[", "y", "]", ".", "r", "*", "d", "g", "=", "colors", "[", "x", "]", ".", "g", "*", "(", "1", "-", "d", ")", "+", "colors", "[", "y", "]", ".", "g", "*", "d", "b", "=", "colors", "[", "x", "]", ".", "b", "*", "(", "1", "-", "d", ")", "+", "colors", "[", "y", "]", ".", "b", "*", "d", "a", "=", "colors", "[", "x", "]", ".", "a", "*", "(", "1", "-", "d", ")", "+", "colors", "[", "y", "]", ".", "a", "*", "d", "gradient", ".", "append", "(", "color", "(", "r", ",", "g", ",", "b", ",", "a", ",", "mode", "=", "\"rgb\"", ")", ")", "gradient", ".", "append", "(", "colors", "[", "-", "1", "]", ")", "return", "gradient"]
}
```

#### ruby

An example of 'train' looks as follows.
```
{
    "id": 0, 
    "idx": "maxmin-1", 
    "nl_tokens": ["Delete", "all", "copies", "that", "are", "older", "than", "the", "max", "age", "provided", "in", "seconds", "."], 
    "pl_tokens": ["def", "clean", "(", "<mask>", ":", "24", "*", "60", "*", "60", ")", "Futex", ".", "new", "(", "file", ",", "log", ":", "@log", ")", ".", "open", "do", "list", "=", "load", "list", ".", "reject!", "do", "|", "s", "|", "if", "s", "[", ":time", "]", ">=", "Time", ".", "now", "-", "max", "false", "else", "@log", ".", "debug", "(", "\"Copy ##{s[:name]}/#{s[:host]}:#{s[:port]} is too old, over #{Age.new(s[:time])}\"", ")", "true", "end", "end", "save", "(", "list", ")", "deleted", "=", "0", "files", ".", "each", "do", "|", "f", "|", "next", "unless", "list", ".", "find", "{", "|", "s", "|", "s", "[", ":name", "]", "==", "File", ".", "basename", "(", "f", ",", "Copies", "::", "EXT", ")", "}", ".", "nil?", "file", "=", "File", ".", "join", "(", "@dir", ",", "f", ")", "size", "=", "File", ".", "size", "(", "file", ")", "File", ".", "delete", "(", "file", ")", "@log", ".", "debug", "(", "\"Copy at #{f} deleted: #{Size.new(size)}\"", ")", "deleted", "+=", "1", "end", "list", ".", "select!", "do", "|", "s", "|", "cp", "=", "File", ".", "join", "(", "@dir", ",", "\"#{s[:name]}#{Copies::EXT}\"", ")", "wallet", "=", "Wallet", ".", "new", "(", "cp", ")", "begin", "wallet", ".", "refurbish", "raise", "\"Invalid protocol #{wallet.protocol} in #{cp}\"", "unless", "wallet", ".", "protocol", "==", "Zold", "::", "PROTOCOL", "true", "rescue", "StandardError", "=>", "e", "FileUtils", ".", "rm_rf", "(", "cp", ")", "@log", ".", "debug", "(", "\"Copy at #{cp} deleted: #{Backtrace.new(e)}\"", ")", "deleted", "+=", "1", "false", "end", "end", "save", "(", "list", ")", "deleted", "end", "end"]
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
|go        |  152|
|java      |  482|
|javascript|  272|
|php       |  407|
|python    | 1264|
|ruby      |   38|

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
