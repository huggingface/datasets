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

 
- **Homepage:** https://github.com/microsoft/CodeXGLUE/tree/main/Text-Text/text-to-text

 

### [Dataset Summary](#dataset-summary)


CodeXGLUE text-to-text dataset, available at https://github.com/microsoft/CodeXGLUE/tree/main/Text-Text/text-to-text

The dataset we use is crawled and filtered from Microsoft Documentation, whose document located at https://github.com/MicrosoftDocs/.


### [Languages](#languages)


da_en, lv_en, no_en, zh_en


## [Dataset Structure](#dataset-structure)
 

### [Data Instances](#data-instances)

 

 

#### da_en

An example of 'train' looks as follows.
```
{
    "id": 0, 
    "source": "title : &quot; Oversigt over ops\u00e6tninger for serviceartikler og serviceartikelkomponenter &quot;\n", 
    "target": "title : Overview of Setups for Service Items and Service Item Components\n"
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

An example of 'validation' looks as follows.
```
{
    "id": 0, 
    "source": "2 . \u00c5pne servicevaren du vil definere komponenter fra en stykkliste for .\n", 
    "target": "2 . Open the service item for which you want to set up components from a BOM .\n"
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




