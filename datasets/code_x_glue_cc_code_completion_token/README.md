---
annotations_creators:
- found
language_creators:
- found
languages:
- python
- java
licenses:
- other-C-UDA
multilinguality:
- monolingual
size_categories:
- 10K<n<100K
source_datasets: []
task_categories:
- sequence-modeling
task_ids:
- language-modeling
---
# Dataset Card for "code_x_glue_cc_code_completion_token"

## Table of Contents
- [Dataset Description](#dataset-description)
  - [Dataset Summary](#dataset-summary)
  - [Languages](#languages)
- [Dataset Structure](#dataset-structure)
  - [Data Instances](#data-instances)
  - [Data Fields](#data-fields)
  - [Data Splits](#data-splits)
- [Additional Information](#additional-information)
  - [Dataset Curators](#dataset-curators)
  - [Licensing Information](#licensing-information)
  - [Citation Information](#citation-information)



## [Dataset Description](#dataset-description)

 
- **Homepage:** https://github.com/microsoft/CodeXGLUE/tree/main/Code-Code/CodeCompletion-token

 

### [Dataset Summary](#dataset-summary)


CodeXGLUE CodeCompletion-token dataset, available at https://github.com/microsoft/CodeXGLUE/tree/main/Code-Code/CodeCompletion-token

Predict next code token given context of previous tokens. Models are evaluated by token level accuracy.
    Code completion is a one of the most widely used features in software development through IDEs. An effective code completion tool could improve software developers' productivity. We provide code completion evaluation tasks in two granularities -- token level and line level. Here we introduce token level code completion. Token level task is analogous to language modeling. Models should have be able to predict the next token in arbitary types.
    


### [Languages](#languages)


java, python


## [Dataset Structure](#dataset-structure)
 

### [Data Instances](#data-instances)

 

 

#### java

An example of 'validation' looks as follows.
```
{
    "code": ["<s>", "package", "ch", ".", "hsr", ".", "geohash", ";", "import", "java", ".", "util", ".", "Random", ";", "import", "ch", ".", "mollusca", ".", "benchmarking", ".", "Before", ";", "import", "ch", ".", "mollusca", ".", "benchmarking", ".", "Benchmark", ";", "public", "class", "GeoHashEncodingBenchmark", "{", "private", "static", "final", "int", "NUMBER_OF_HASHES", "=", "1000000", ";", "private", "GeoHash", "[", "]", "hashes", ";", "private", "double", "[", "]", "latitudes", ";", "private", "double", "[", "]", "longitudes", ";", "@", "Before", "public", "void", "setupBenchmark", "(", ")", "{", "hashes", "=", "new", "GeoHash", "[", "NUMBER_OF_HASHES", "]", ";", "latitudes", "=", "new", "double", "[", "NUMBER_OF_HASHES", "]", ";", "longitudes", "=", "new", "double", "[", "NUMBER_OF_HASHES", "]", ";", "Random", "rand", "=", "new", "Random", "(", ")", ";", "for", "(", "int", "i", "=", "0", ";", "i", "<", "NUMBER_OF_HASHES", ";", "i", "++", ")", "{", "latitudes", "[", "i", "]", "=", "rand", ".", "nextDouble", "(", ")", "*", "180", "-", "90", ";", "longitudes", "[", "i", "]", "=", "rand", ".", "nextDouble", "(", ")", "*", "360", "-", "180", ";", "}", "}", "@", "Benchmark", "(", "times", "=", "10", ")", "public", "void", "benchmarkGeoHashEncoding", "(", ")", "{", "for", "(", "int", "i", "=", "0", ";", "i", "<", "NUMBER_OF_HASHES", ";", "i", "++", ")", "{", "hashes", "[", "i", "]", "=", "GeoHash", ".", "withBitPrecision", "(", "latitudes", "[", "i", "]", ",", "longitudes", "[", "i", "]", ",", "60", ")", ";", "}", "}", "}", "</s>"], 
    "id": 0
}
```
 

#### python

An example of 'test' looks as follows.
```
{
    "code": ["<s>", "from", "django", ".", "utils", ".", "translation", "import", "ugettext_lazy", "as", "_", "<EOL>", "from", "horizon", "import", "tabs", "<EOL>", "class", "NetworkProfileTab", "(", "tabs", ".", "Tab", ")", ":", "<EOL>", "name", "=", "_", "(", "\"\"", ")", "<EOL>", "slug", "=", "\"\"", "<EOL>", "template_name", "=", "''", "<EOL>", "def", "get_context_data", "(", "self", ",", "request", ")", ":", "<EOL>", "return", "None", "<EOL>", "class", "PolicyProfileTab", "(", "tabs", ".", "Tab", ")", ":", "<EOL>", "name", "=", "_", "(", "\"Policy Profile\"", ")", "<EOL>", "slug", "=", "\"policy_profile\"", "<EOL>", "template_name", "=", "''", "<EOL>", "preload", "=", "False", "<EOL>", "class", "IndexTabs", "(", "tabs", ".", "TabGroup", ")", ":", "<EOL>", "slug", "=", "\"indextabs\"", "<EOL>", "tabs", "=", "(", "NetworkProfileTab", ",", "PolicyProfileTab", ")", "</s>"], 
    "id": 0, 
    "path": "Havate/havate-openstack/proto-build/gui/horizon/Horizon_GUI/openstack_dashboard/dashboards/router/nexus1000v/tabs.py\n"
}
```
 



### [Data Fields](#data-fields)

 
In the following each data field in go is explained for each config. The data fields are the same among all splits.

#### java

|field name|      type      |    description     |
|----------|----------------|--------------------|
|id        |int32           | Index of the sample|
|code      |Sequence[string]| Code Tokens        |


#### python

|field name|      type      |         description         |
|----------|----------------|-----------------------------|
|id        |int32           | Index of the sample         |
|path      |string          | Original path in the dataset|
|code      |Sequence[string]| Code Tokens                 |






### [Data Splits](#data-splits)

 



#### java

|    |train|validation|test|
|----|----:|---------:|---:|
|java|12934|      7189|8268|




#### python

|      |train |test |
|------|-----:|----:|
|python|100000|50000|








## [Additional Information](#additional-information)
 

### [Dataset Curators](#dataset-curators)


https://github.com/microsoft, https://github.com/madlag


### [Licensing Information](#licensing-information)


Computational Use of Data Agreement (C-UDA) License.


### [Citation Information](#citation-information)


```
@article{raychev2016probabilistic,
      title={Probabilistic Model for Code with Decision Trees},
      author={Raychev, Veselin and Bielik, Pavol and Vechev, Martin},
      journal={ACM SIGPLAN Notices},
      pages={731--747},
      year={2016},
      publisher={ACM New York, NY, USA}
    }
    @inproceedings{allamanis2013mining,
      title={Mining Source Code Repositories at Massive Scale using Language Modeling},
      author={Allamanis, Miltiadis and Sutton, Charles},
      booktitle={2013 10th Working Conference on Mining Software Repositories (MSR)},
      pages={207--216},
      year={2013},
      organization={IEEE}
    }
```




