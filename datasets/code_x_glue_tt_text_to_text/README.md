---
annotations_creators:
- found
language_creators:
- found
languages:
- da
- no
- lv
- zh
- en
licenses:
- other-C-UDA
multilinguality:
- multilingual
size_categories:
- 10K<n<100K
source_datasets:
- original
task_categories:
- conditional-text-generation
task_ids:
- machine-translation
---
# Dataset Card for "code_x_glue_tt_text_to_text"

## Table of Contents
- [Dataset Description](#dataset-description)
  - [Dataset Summary](#dataset-summary)
  - [Supported Tasks](#supported-tasks)
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

## [Dataset Description](#dataset-description)

- **Homepage:** https://github.com/microsoft/CodeXGLUE/tree/main/Text-Text/text-to-text

### [Dataset Summary](#dataset-summary)

CodeXGLUE text-to-text dataset, available at https://github.com/microsoft/CodeXGLUE/tree/main/Text-Text/text-to-text

The dataset we use is crawled and filtered from Microsoft Documentation, whose document located at https://github.com/MicrosoftDocs/.

### [Supported Tasks](#supported-tasks)

[More Information Needed]

### [Languages](#languages)

da_en, lv_en, no_en, zh_en

## [Dataset Structure](#dataset-structure)

### [Data Instances](#data-instances)

#### da_en

An example of 'validation' looks as follows.
```
{
    "id": 0,
    "source": "2 . \u00c5bn den serviceartikel , som du vil definere komponenter for ud fra en stykliste .\n",
    "target": "2 . Open the service item for which you want to set up components from a BOM .\n"
}
```

#### lv_en

An example of 'validation' looks as follows.
```
{
    "id": 0,
    "source": "# # &lt; a name = &quot; chart-of-accounts-and-financial-dimension-components &quot; &gt; &lt; / a &gt; Kontu pl\u0101ns un finan\u0161u dimensiju komponenti\n",
    "target": "# # Chart of accounts and financial dimension components\n"
}
```

#### no_en

An example of 'test' looks as follows.
```
{
    "id": 0,
    "source": "&#91; Analysere kontantstr\u00f8mmen i firmaet &#93; ( finance-analyze-cash-flow.md )\n",
    "target": "&#91; Analyzing Cash Flow in Your Company &#93; ( finance-analyze-cash-flow.md )\n"
}
```

#### zh_en

An example of 'train' looks as follows.
```
{
    "id": 0,
    "source": "\u4ee5\u4e0b \u547d\u540d \u7a7a\u95f4 \u5305\u542b \u53ef \u8ba9 Android \u5e94\u7528 \u5b9e\u73b0 \u57fa\u4e8e Windows \u7684 \u5c31\u8fd1 \u5171 \u4eab \u529f\u80fd \u7684 API \u3002\n",
    "target": "The following namespaces contain APIs that allow an Android app to implement the Windows-based Nearby sharing feature .\n"
}
```

### [Data Fields](#data-fields)

In the following each data field in go is explained for each config. The data fields are the same among all splits.

#### da_en, lv_en, no_en, zh_en

|field name| type |              description               |
|----------|------|----------------------------------------|
|id        |int32 | The index of the sample                |
|source    |string| The source language version of the text|
|target    |string| The target language version of the text|

### [Data Splits](#data-splits)

|name |train|validation|test|
|-----|----:|---------:|---:|
|da_en|42701|      1000|1000|
|lv_en|18749|      1000|1000|
|no_en|44322|      1000|1000|
|zh_en|50154|      1000|1000|

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
@article{CodeXGLUE,
         title={CodeXGLUE: A Benchmark Dataset and Open Challenge for Code Intelligence},
         year={2020},}
```

