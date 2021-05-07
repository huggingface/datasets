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

An example of 'test' looks as follows.
```
{
    "id": 0, 
    "source": "4 . K\u00f8r modellen , og udgiv den som en webtjeneste .\n", 
    "target": "4 . Run the model , and publish it as a web service .\n"
}
```
 

#### lv_en

An example of 'train' looks as follows.
```
{
    "id": 0, 
    "source": "title : Pakalpojumu objektu izveide\n", 
    "target": "title : Create service objects\n"
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

An example of 'validation' looks as follows.
```
{
    "id": 0, 
    "source": "& # 124 ; MCDUserNotificationReadStateFilterAny & # 124 ; 0 & # 124 ; \u5305\u62ec \u901a\u77e5 , \u800c \u4e0d \u8003\u8651 \u8bfb\u53d6 \u72b6\u6001 \u3002 & # 124 ;\n", 
    "target": "&#124; MCDUserNotificationReadStateFilterAny &#124; 0 &#124; Include notifications regardless of read state . &#124;\n"
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




