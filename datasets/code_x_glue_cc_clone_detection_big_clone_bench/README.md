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
- 1M<n<10M
source_datasets:
- original
task_categories:
- text-classification
task_ids:
- semantic-similarity-classification
pretty_name: CodeXGlueCcCloneDetectionBigCloneBench
---
# Dataset Card for "code_x_glue_cc_clone_detection_big_clone_bench"

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

- **Homepage:** https://github.com/microsoft/CodeXGLUE/tree/main/Code-Code/Clone-detection-BigCloneBench

### Dataset Summary

CodeXGLUE Clone-detection-BigCloneBench dataset, available at https://github.com/microsoft/CodeXGLUE/tree/main/Code-Code/Clone-detection-BigCloneBench

Given two codes as the input, the task is to do binary classification (0/1), where 1 stands for semantic equivalence and 0 for others. Models are evaluated by F1 score.
The dataset we use is BigCloneBench and filtered following the paper Detecting Code Clones with Graph Neural Network and Flow-Augmented Abstract Syntax Tree.

### Supported Tasks and Leaderboards

- `semantic-similarity-classification`: The dataset can be used to train a model for classifying if two given java methods are cloens of each other.

### Languages

- Java **programming** language

## Dataset Structure

### Data Instances

An example of 'test' looks as follows.
```
{
    "func1": "    @Test(expected = GadgetException.class)\n    public void malformedGadgetSpecIsCachedAndThrows() throws Exception {\n        HttpRequest request = createCacheableRequest();\n        expect(pipeline.execute(request)).andReturn(new HttpResponse(\"malformed junk\")).once();\n        replay(pipeline);\n        try {\n            specFactory.getGadgetSpec(createContext(SPEC_URL, false));\n            fail(\"No exception thrown on bad parse\");\n        } catch (GadgetException e) {\n        }\n        specFactory.getGadgetSpec(createContext(SPEC_URL, false));\n    }\n", 
    "func2": "    public InputStream getInputStream() throws TGBrowserException {\n        try {\n            if (!this.isFolder()) {\n                URL url = new URL(this.url);\n                InputStream stream = url.openStream();\n                return stream;\n            }\n        } catch (Throwable throwable) {\n            throw new TGBrowserException(throwable);\n        }\n        return null;\n    }\n", 
    "id": 0, 
    "id1": 2381663, 
    "id2": 4458076, 
    "label": false
}
```

### Data Fields

In the following each data field in go is explained for each config. The data fields are the same among all splits.

#### default

|field name| type |                    description                    |
|----------|------|---------------------------------------------------|
|id        |int32 | Index of the sample                               |
|id1       |int32 | The first function id                             |
|id2       |int32 | The second function id                            |
|func1     |string| The full text of the first function               |
|func2     |string| The full text of the second function              |
|label     |bool  | 1 is the functions are not equivalent, 0 otherwise|

### Data Splits

| name  |train |validation| test |
|-------|-----:|---------:|-----:|
|default|901028|    415416|415416|

## Dataset Creation

### Curation Rationale

[More Information Needed]

### Source Data

#### Initial Data Collection and Normalization

Data was mined from the IJaDataset 2.0 dataset.
[More Information Needed]

#### Who are the source language producers?

[More Information Needed]

### Annotations

#### Annotation process

Data was manually labeled by three judges by automatically identifying potential clones using search heuristics.
[More Information Needed]

#### Who are the annotators?

[More Information Needed]

### Personal and Sensitive Information

[More Information Needed]

## Considerations for Using the Data

### Social Impact of Dataset

[More Information Needed]

### Discussion of Biases

Most of the clones are type 1 and 2 with type 3 and especially type 4 being rare.

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
@inproceedings{svajlenko2014towards,
  title={Towards a big data curated benchmark of inter-project code clones},
  author={Svajlenko, Jeffrey and Islam, Judith F and Keivanloo, Iman and Roy, Chanchal K and Mia, Mohammad Mamun},
  booktitle={2014 IEEE International Conference on Software Maintenance and Evolution},
  pages={476--480},
  year={2014},
  organization={IEEE}
}

@inproceedings{wang2020detecting,
  title={Detecting Code Clones with Graph Neural Network and Flow-Augmented Abstract Syntax Tree},
  author={Wang, Wenhan and Li, Ge and Ma, Bo and Xia, Xin and Jin, Zhi},
  booktitle={2020 IEEE 27th International Conference on Software Analysis, Evolution and Reengineering (SANER)},
  pages={261--271},
  year={2020},
  organization={IEEE}
}
```

### Contributions

Thanks to @madlag (and partly also @ncoop57) for adding this dataset.
