---
annotations_creators:
- found
language_creators:
- found
languages:
- C++
licenses:
- other-C-UDA
multilinguality:
- monolingual
size_categories:
- n>1M
source_datasets: []
task_categories:
- text-classification
task_ids:
- semantic-similarity-classification
---
# Dataset Card for "code_x_glue_cc_clone_detection_big_clone_bench"

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

 
- **Homepage:** https://github.com/microsoft/CodeXGLUE/tree/main/Code-Code/Clone-detection-BigCloneBench

 

### [Dataset Summary](#dataset-summary)


CodeXGLUE Clone-detection-BigCloneBench dataset, available at https://github.com/microsoft/CodeXGLUE/tree/main/Code-Code/Clone-detection-BigCloneBench

Given two codes as the input, the task is to do binary classification (0/1), where 1 stands for semantic equivalence and 0 for others. Models are evaluated by F1 score.
The dataset we use is BigCloneBench and filtered following the paper Detecting Code Clones with Graph Neural Network and Flow-Augmented Abstract Syntax Tree.


## [Dataset Structure](#dataset-structure)
 

### [Data Instances](#data-instances)

 

 

An example of 'train' looks as follows.
```
{
    "func1": "    private void setNodekeyInJsonResponse(String service) throws Exception {\n        String filename = this.baseDirectory + service + \".json\";\n        Scanner s = new Scanner(new File(filename));\n        PrintWriter fw = new PrintWriter(new File(filename + \".new\"));\n        while (s.hasNextLine()) {\n            fw.println(s.nextLine().replaceAll(\"NODEKEY\", this.key));\n        }\n        s.close();\n        fw.close();\n        (new File(filename + \".new\")).renameTo(new File(filename));\n    }\n", 
    "func2": "    public void transform(String style, String spec, OutputStream out) throws IOException {\n        URL url = new URL(rootURL, spec);\n        InputStream in = new PatchXMLSymbolsStream(new StripDoctypeStream(url.openStream()));\n        transform(style, in, out);\n        in.close();\n    }\n", 
    "id": 0, 
    "id1": 13988825, 
    "id2": 8660836, 
    "label": false
}
```
 



### [Data Fields](#data-fields)

 
In the following each data field in go is explained for each config. The data fields are the same among all splits.

#### default

|field name|         type         |                    description                    |
|----------|----------------------|---------------------------------------------------|
|id        |int32                 | Index of the sample                               |
|id1       |int32                 | The first function id                             |
|id2       |int32                 | The second function id                            |
|func1     |string                | The full text of the first function               |
|func2     |string                | The full text of the second function              |
|label     |datasets.Value("bool"]| 1 is the functions are not equivalent, 0 otherwise|






### [Data Splits](#data-splits)

 


| name  |train |validation| test |
|-------|-----:|---------:|-----:|
|default|901028|    415416|415416|







## [Additional Information](#additional-information)
 

### [Dataset Curators](#dataset-curators)


https://github.com/microsoft, https://github.com/madlag


### [Licensing Information](#licensing-information)


Computational Use of Data Agreement (C-UDA) License.


### [Citation Information](#citation-information)


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




