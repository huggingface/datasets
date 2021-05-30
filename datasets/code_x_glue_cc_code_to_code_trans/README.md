---
annotations_creators:
- expert-generated
language_creators:
- found
languages:
- code
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
  - [Supported Tasks](#supported-tasks)
  - [Languages](#languages)
- [Dataset Structure](#dataset-structure)
  - [Data Instances](#data-instances)
  - [Data Fields](#data-fields)
  - [Data Splits Sample Size](#data-splits-sample-size)
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

## [Dataset Description](#dataset-description)

- **Homepage:** https://github.com/microsoft/CodeXGLUE/tree/main/Code-Code/code-to-code-trans

### [Dataset Summary](#dataset-summary)

CodeXGLUE code-to-code-trans dataset, available at https://github.com/microsoft/CodeXGLUE/tree/main/Code-Code/code-to-code-trans

The dataset is collected from several public repos, including Lucene(http://lucene.apache.org/), POI(http://poi.apache.org/), JGit(https://github.com/eclipse/jgit/) and Antlr(https://github.com/antlr/).
        We collect both the Java and C# versions of the codes and find the parallel functions. After removing duplicates and functions with the empty body, we split the whole dataset into training, validation and test sets.

### [Supported Tasks](#supported-tasks)

- `machine-translation`: The dataset can be used to train a model for translating code in Java to C# and vice versa.

### [Languages](#languages)

- Java **programming** language
- C# **programming** language

## [Dataset Structure](#dataset-structure)

### [Data Instances](#data-instances)

An example of 'validation' looks as follows.
```
{
    "cs": "public DVRecord(RecordInputStream in1){_option_flags = in1.ReadInt();_promptTitle = ReadUnicodeString(in1);_errorTitle = ReadUnicodeString(in1);_promptText = ReadUnicodeString(in1);_errorText = ReadUnicodeString(in1);int field_size_first_formula = in1.ReadUShort();_not_used_1 = in1.ReadShort();_formula1 = NPOI.SS.Formula.Formula.Read(field_size_first_formula, in1);int field_size_sec_formula = in1.ReadUShort();_not_used_2 = in1.ReadShort();_formula2 = NPOI.SS.Formula.Formula.Read(field_size_sec_formula, in1);_regions = new CellRangeAddressList(in1);}\n", 
    "id": 0, 
    "java": "public DVRecord(RecordInputStream in) {_option_flags = in.readInt();_promptTitle = readUnicodeString(in);_errorTitle = readUnicodeString(in);_promptText = readUnicodeString(in);_errorText = readUnicodeString(in);int field_size_first_formula = in.readUShort();_not_used_1 = in.readShort();_formula1 = Formula.read(field_size_first_formula, in);int field_size_sec_formula = in.readUShort();_not_used_2 = in.readShort();_formula2 = Formula.read(field_size_sec_formula, in);_regions = new CellRangeAddressList(in);}\n"
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

### [Data Splits Sample Size](#data-splits-sample-size)

| name  |train|validation|test|
|-------|----:|---------:|---:|
|default|10300|       500|1000|

## Dataset Creation(#dataset-creation)

### Curation Rationale(#curation-rationale)

[More Information Needed]

### Source Data(#source-data)

[More Information Needed]

### Annotations(#annotations)

[More Information Needed]

### Personal and Sensitive Information(#personal-and-sensitive-information)

[More Information Needed]

## Considerations for Using the Data(#considerations-for-using-the-data)

### Social Impact of Dataset(#social-impact-of-dataset)

[More Information Needed]

### Discussion of Biases(#discussion-of-biases)

[More Information Needed]

### Other Known Limitations(#other-known-limitations)

[More Information Needed]

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

### Contributions
Thanks to @madlag (and partly also @ncoop57) for adding this dataset.