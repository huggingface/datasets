---
annotations_creators:
- expert-generated
language_creators:
- found
languages:
- java
- C#
licenses:
- other-C-UDA
multilinguality:
- other-programming-languages
size_categories:
- 10K<n<100K
source_datasets:
- original
task_categories:
- conditional-text-generation
task_ids:
- machine-translation
---
# Dataset Card for "code_x_glue_cc_code_to_code_trans"

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

 
- **Homepage:** https://github.com/microsoft/CodeXGLUE/tree/main/Code-Code/code-to-code-trans

 

### [Dataset Summary](#dataset-summary)


CodeXGLUE code-to-code-trans dataset, available at https://github.com/microsoft/CodeXGLUE/tree/main/Code-Code/code-to-code-trans

The dataset is collected from several public repos, including Lucene(http://lucene.apache.org/), POI(http://poi.apache.org/), JGit(https://github.com/eclipse/jgit/) and Antlr(https://github.com/antlr/).
        We collect both the Java and C# versions of the codes and find the parallel functions. After removing duplicates and functions with the empty body, we split the whole dataset into training, validation and test sets.


## [Dataset Structure](#dataset-structure)
 

### [Data Instances](#data-instances)

 

 

An example of 'train' looks as follows.
```
{
    "cs": "public virtual ListSpeechSynthesisTasksResponse ListSpeechSynthesisTasks(ListSpeechSynthesisTasksRequest request){var options = new InvokeOptions();options.RequestMarshaller = ListSpeechSynthesisTasksRequestMarshaller.Instance;options.ResponseUnmarshaller = ListSpeechSynthesisTasksResponseUnmarshaller.Instance;return Invoke<ListSpeechSynthesisTasksResponse>(request, options);}\n", 
    "id": 0, 
    "java": "public ListSpeechSynthesisTasksResult listSpeechSynthesisTasks(ListSpeechSynthesisTasksRequest request) {request = beforeClientExecution(request);return executeListSpeechSynthesisTasks(request);}\n"
}
```
 



### [Data Fields](#data-fields)

 
In the following each data field in go is explained for each config. The data fields are the same among all splits.

#### default

|field name| type |         description         |
|----------|------|-----------------------------|
|id        |int32 | Index of the sample         |
|java      |string| The java version of the code|
|cs        |string| The C# version of the code  |






### [Data Splits](#data-splits)

 


| name  |train|validation|test|
|-------|----:|---------:|---:|
|default|10300|       500|1000|







## [Additional Information](#additional-information)
 

### [Dataset Curators](#dataset-curators)


https://github.com/microsoft, https://github.com/madlag


### [Licensing Information](#licensing-information)


Computational Use of Data Agreement (C-UDA) License.


### [Citation Information](#citation-information)


```
@article{CodeXGLUE,
         title={CodeXGLUE: A Benchmark Dataset and Open Challenge for Code Intelligence},
         year={2020},}
```




