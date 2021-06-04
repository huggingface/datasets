---
annotations_creators:
- found
language_creators:
- found
languages:
- code
licenses:
- other-C-UDA
multilinguality:
- monolingual
size_categories:
- n>1M
source_datasets:
- original
task_categories:
- text-classification
task_ids:
- semantic-similarity-classification
---
# Dataset Card for "code_x_glue_cc_clone_detection_big_clone_bench"

## Table of Contents
- [Dataset Description](#dataset-description)
  - [Dataset Summary](#dataset-summary)
  - [Supported Tasks](#supported-tasks)
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

## [Dataset Description](#dataset-description)

- **Homepage:** https://github.com/microsoft/CodeXGLUE/tree/main/Code-Code/Clone-detection-BigCloneBench

### [Dataset Summary](#dataset-summary)

CodeXGLUE Clone-detection-BigCloneBench dataset, available at https://github.com/microsoft/CodeXGLUE/tree/main/Code-Code/Clone-detection-BigCloneBench

Given two codes as the input, the task is to do binary classification (0/1), where 1 stands for semantic equivalence and 0 for others. Models are evaluated by F1 score.
The dataset we use is BigCloneBench and filtered following the paper Detecting Code Clones with Graph Neural Network and Flow-Augmented Abstract Syntax Tree.

### [Supported Tasks](#supported-tasks)

[More Information Needed]

## [Dataset Structure](#dataset-structure)

### [Data Instances](#data-instances)

An example of 'validation' looks as follows.
```
{
    "func1": "    public ViewInitListener() throws IOException {\n        URL url = this.getClass().getResource(VIEW_INIT_CONFIG);\n        log.debug(\"Loading configuration from: \" + url);\n        config = new Properties();\n        InputStream in = url.openStream();\n        config.load(in);\n        in.close();\n    }\n",
    "func2": "    public void run() {\n        String s, s2;\n        s = \"\";\n        s2 = \"\";\n        try {\n            URL url = new URL(\"http://www.m-w.com/dictionary/\" + Word);\n            BufferedReader in = new BufferedReader(new InputStreamReader(url.openStream()));\n            String str;\n            while (((str = in.readLine()) != null) && (!stopped)) {\n                s = s + str;\n            }\n            in.close();\n        } catch (MalformedURLException e) {\n        } catch (IOException e) {\n        }\n        Pattern pattern = Pattern.compile(\"popWin\\\\('/cgi-bin/(.+?)'\", Pattern.CASE_INSENSITIVE | Pattern.DOTALL);\n        Matcher matcher = pattern.matcher(s);\n        if ((!stopped) && (matcher.find())) {\n            String newurl = \"http://m-w.com/cgi-bin/\" + matcher.group(1);\n            try {\n                URL url2 = new URL(newurl);\n                BufferedReader in2 = new BufferedReader(new InputStreamReader(url2.openStream()));\n                String str;\n                while (((str = in2.readLine()) != null) && (!stopped)) {\n                    s2 = s2 + str;\n                }\n                in2.close();\n            } catch (MalformedURLException e) {\n            } catch (IOException e) {\n            }\n            Pattern pattern2 = Pattern.compile(\"<A HREF=\\\"http://(.+?)\\\">Click here to listen with your default audio player\", Pattern.CASE_INSENSITIVE | Pattern.DOTALL);\n            Matcher matcher2 = pattern2.matcher(s2);\n            if ((!stopped) && (matcher2.find())) {\n                if (getWave(\"http://\" + matcher2.group(1))) label.setEnabled(true);\n            }\n        }\n        button.setEnabled(true);\n    }\n",
    "id": 0,
    "id1": 13653451,
    "id2": 21955002,
    "label": false
}
```

### [Data Fields](#data-fields)

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

### [Data Splits](#data-splits)

| name  |train |validation| test |
|-------|-----:|---------:|-----:|
|default|901028|    415416|415416|

## [Dataset Creation](#dataset-creation)

### [Curation Rationale](#curation-rationale)

[More Information Needed]

### [Source Data](#source-data)

[More Information Needed]

### [Annotations](#annotations)

[More Information Needed]

### [Personal and Sensitive Information](#personal-and-sensitive-information)

[More Information Needed]

## [Considerations for Using the Data](#considerations-for-using-the-data)

### [Social Impact of Dataset](#social-impact-of-dataset)

[More Information Needed]

### [Discussion of Biases](#discussion-of-biases)

[More Information Needed]

### [Other Known Limitations](#other-known-limitations)

[More Information Needed]

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

