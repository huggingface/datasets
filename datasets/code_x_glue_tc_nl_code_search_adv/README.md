--
annotations_creators:
- found
language_creators:
- found
languages:
- python
licenses:
- other-C-UDA
multilinguality:
- other-programming-languages
size_categories:
- 100K<n<1M
source_datasets: []
task_categories:
- text-retrieval
task_ids:
- document-retrieval
---
# Dataset Card for "code_x_glue_tc_nl_code_search_adv"

## Table of Contents
- [Dataset Description](#dataset-description)
  - [Dataset Summary](#dataset-summary)
- [Dataset Structure](#dataset-structure)
  - [Data Instances](#data-instances)
  - [Data Fields](#data-fields)
  - [Data Splits](#data-splits)
- [Additional Information](#additional-information)
  - [Dataset Curators](#dataset-curators)
  - [Licensing Information](#licensing-information)
  - [Citation Information](#citation-information)



## [Dataset Description](#dataset-description)

 
- **Homepage:** https://github.com/microsoft/CodeXGLUE/tree/main/Text-Code/NL-code-search-Adv

 

### [Dataset Summary](#dataset-summary)


CodeXGLUE NL-code-search-Adv dataset, available at https://github.com/microsoft/CodeXGLUE/tree/main/Text-Code/NL-code-search-Adv

The dataset we use comes from CodeSearchNet and we filter the dataset as the following:
- Remove examples that codes cannot be parsed into an abstract syntax tree.
- Remove examples that #tokens of documents is < 3 or >256
- Remove examples that documents contain special tokens (e.g. <img ...> or https:...)
- Remove examples that documents are not English.



## [Dataset Structure](#dataset-structure)
 

### [Data Instances](#data-instances)

 

 

An example of 'train' looks as follows.
```
{
    "argument_list": "", 
    "code": "def settext(self, text, cls='current'):\n        \"\"\"Set the text for this element.\n\n        Arguments:\n            text (str): The text\n            cls (str): The class of the text, defaults to ``current`` (leave this unless you know what you are doing). There may be only one text content element of each class associated with the element.\n        \"\"\"\n        self.replace(TextContent, value=text, cls=cls)", 
    "code_tokens": ["def", "settext", "(", "self", ",", "text", ",", "cls", "=", "'current'", ")", ":", "self", ".", "replace", "(", "TextContent", ",", "value", "=", "text", ",", "cls", "=", "cls", ")"], 
    "docstring": "Set the text for this element.\n\n        Arguments:\n            text (str): The text\n            cls (str): The class of the text, defaults to ``current`` (leave this unless you know what you are doing). There may be only one text content element of each class associated with the element.", 
    "docstring_summary": "", 
    "docstring_tokens": ["Set", "the", "text", "for", "this", "element", "."], 
    "func_name": "AbstractElement.settext", 
    "id": 0, 
    "identifier": "", 
    "language": "python", 
    "nwo": "", 
    "original_string": "def settext(self, text, cls='current'):\n        \"\"\"Set the text for this element.\n\n        Arguments:\n            text (str): The text\n            cls (str): The class of the text, defaults to ``current`` (leave this unless you know what you are doing). There may be only one text content element of each class associated with the element.\n        \"\"\"\n        self.replace(TextContent, value=text, cls=cls)", 
    "parameters": "", 
    "path": "pynlpl/formats/folia.py", 
    "repo": "proycon/pynlpl", 
    "return_statement": "", 
    "score": -1.0, 
    "sha": "7707f69a91caaa6cde037f0d0379f1d42500a68b", 
    "url": "https://github.com/proycon/pynlpl/blob/7707f69a91caaa6cde037f0d0379f1d42500a68b/pynlpl/formats/folia.py#L1357-L1364"
}
```
 



### [Data Fields](#data-fields)

 
In the following each data field in go is explained for each config. The data fields are the same among all splits.

#### default

|   field name    |         type          |                                    description                                    |
|-----------------|-----------------------|-----------------------------------------------------------------------------------|
|id               |int32                  | Index of the sample                                                               |
|repo             |string                 | repo: the owner/repo                                                              |
|path             |string                 | path: the full path to the original file                                          |
|func_name        |string                 | func_name: the function or method name                                            |
|original_string  |string                 | original_string: the raw string before tokenization or parsing                    |
|language         |string                 | language: the programming language                                                |
|code             |string                 | code/function: the part of the original_string that is code                       |
|code_tokens      |Sequence[string]       | code_tokens/function_tokens: tokenized version of code                            |
|docstring        |string                 | docstring: the top-level comment or docstring, if it exists in the original string|
|docstring_tokens |Sequence[string]       | docstring_tokens: tokenized version of docstring                                  |
|sha              |string                 | sha of the file                                                                   |
|url              |string                 | url of the file                                                                   |
|docstring_summary|string                 | Summary of the docstring                                                          |
|parameters       |string                 | parameters of the function                                                        |
|return_statement |string                 | return statement                                                                  |
|argument_list    |string                 | list of arguments of the function                                                 |
|identifier       |string                 | identifier                                                                        |
|nwo              |string                 | nwo                                                                               |
|score            |datasets.Value("float"]| score for this search                                                             |






### [Data Splits](#data-splits)

 


| name  |train |validation|test |
|-------|-----:|---------:|----:|
|default|251820|      9604|19210|







## [Additional Information](#additional-information)
 

### [Dataset Curators](#dataset-curators)


https://github.com/microsoft, https://github.com/madlag


### [Licensing Information](#licensing-information)


Computational Use of Data Agreement (C-UDA) License.


### [Citation Information](#citation-information)


```
@article{husain2019codesearchnet,
  title={Codesearchnet challenge: Evaluating the state of semantic code search},
  author={Husain, Hamel and Wu, Ho-Hsiang and Gazit, Tiferet and Allamanis, Miltiadis and Brockschmidt, Marc},
  journal={arXiv preprint arXiv:1909.09436},
  year={2019}
}
```




