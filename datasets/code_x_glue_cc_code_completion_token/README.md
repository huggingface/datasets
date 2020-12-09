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

An example of 'test' looks as follows.
```
{
    "code": ["<s>", "package", "org", ".", "vaadin", ".", "teemu", ".", "clara", ".", "demo", ";", "import", "java", ".", "io", ".", "BufferedReader", ";", "import", "java", ".", "io", ".", "ByteArrayInputStream", ";", "import", "java", ".", "io", ".", "IOException", ";", "import", "java", ".", "io", ".", "InputStreamReader", ";", "import", "org", ".", "vaadin", ".", "teemu", ".", "clara", ".", "Clara", ";", "import", "org", ".", "vaadin", ".", "teemu", ".", "clara", ".", "inflater", ".", "LayoutInflaterException", ";", "import", "com", ".", "vaadin", ".", "Application", ";", "import", "com", ".", "vaadin", ".", "terminal", ".", "ThemeResource", ";", "import", "com", ".", "vaadin", ".", "ui", ".", "Button", ";", "import", "com", ".", "vaadin", ".", "ui", ".", "Button", ".", "ClickEvent", ";", "import", "com", ".", "vaadin", ".", "ui", ".", "Component", ";", "import", "com", ".", "vaadin", ".", "ui", ".", "Embedded", ";", "import", "com", ".", "vaadin", ".", "ui", ".", "HorizontalLayout", ";", "import", "com", ".", "vaadin", ".", "ui", ".", "HorizontalSplitPanel", ";", "import", "com", ".", "vaadin", ".", "ui", ".", "TextArea", ";", "import", "com", ".", "vaadin", ".", "ui", ".", "VerticalLayout", ";", "import", "com", ".", "vaadin", ".", "ui", ".", "Window", ";", "import", "com", ".", "vaadin", ".", "ui", ".", "Window", ".", "Notification", ";", "@", "SuppressWarnings", "(", "\"serial\"", ")", "public", "class", "DemoApplication", "extends", "Application", "{", "private", "DemoController", "controller", ";", "private", "TextArea", "xmlArea", ";", "private", "HorizontalSplitPanel", "split", "=", "new", "HorizontalSplitPanel", "(", ")", ";", "private", "Window", "mainWindow", ";", "@", "Override", "public", "void", "init", "(", ")", "{", "setTheme", "(", "\"clara\"", ")", ";", "setMainWindow", "(", "mainWindow", "=", "new", "Window", "(", ")", ")", ";", "controller", "=", "new", "DemoController", "(", "mainWindow", ")", ";", "mainWindow", ".", "setContent", "(", "split", ")", ";", "VerticalLayout", "editor", "=", "new", "VerticalLayout", "(", ")", ";", "editor", ".", "setSpacing", "(", "true", ")", ";", "editor", ".", "setMargin", "(", "false", ",", "false", ",", "false", ",", "true", ")", ";", "editor", ".", "setHeight", "(", "\"100%\"", ")", ";", "editor", ".", "addComponent", "(", "xmlArea", "=", "createXmlArea", "(", ")", ")", ";", "editor", ".", "setExpandRatio", "(", "xmlArea", ",", "1.0f", ")", ";", "editor", ".", "addComponent", "(", "createUpdateButton", "(", ")", ")", ";", "HorizontalLayout", "wrapper", "=", "new", "HorizontalLayout", "(", ")", ";", "wrapper", ".", "setMargin", "(", "true", ")", ";", "wrapper", ".", "setSizeFull", "(", ")", ";", "wrapper", ".", "addComponent", "(", "createLogo", "(", ")", ")", ";", "wrapper", ".", "addComponent", "(", "editor", ")", ";", "wrapper", ".", "setExpandRatio", "(", "editor", ",", "1.0f", ")", ";", "split", ".", "setFirstComponent", "(", "wrapper", ")", ";", "updateLayout", "(", ")", ";", "}", "private", "Component", "createLogo", "(", ")", "{", "Embedded", "logo", "=", "new", "Embedded", "(", "null", ",", "new", "ThemeResource", "(", "\"\"", ")", ")", ";", "logo", ".", "setHeight", "(", "\"90px\"", ")", ";", "logo", ".", "setWidth", "(", "\"90px\"", ")", ";", "return", "logo", ";", "}", "private", "TextArea", "createXmlArea", "(", ")", "{", "TextArea", "area", "=", "new", "TextArea", "(", ")", ";", "area", ".", "setStyleName", "(", "\"xml-area\"", ")", ";", "area", ".", "setSizeFull", "(", ")", ";", "area", ".", "setValue", "(", "readStartingPoint", "(", ")", ")", ";", "return", "area", ";", "}", "private", "Button", "createUpdateButton", "(", ")", "{", "return", "new", "Button", "(", "\"Update\"", ",", "new", "Button", ".", "ClickListener", "(", ")", "{", "public", "void", "buttonClick", "(", "ClickEvent", "event", ")", "{", "updateLayout", "(", ")", ";", "}", "}", ")", ";", "}", "private", "String", "readStartingPoint", "(", ")", "{", "BufferedReader", "reader", "=", "null", ";", "try", "{", "reader", "=", "new", "BufferedReader", "(", "new", "InputStreamReader", "(", "getClass", "(", ")", ".", "getClassLoader", "(", ")", ".", "getResourceAsStream", "(", "\"\"", ")", ")", ")", ";", "StringBuilder", "xml", "=", "new", "StringBuilder", "(", ")", ";", "String", "line", ";", "while", "(", "(", "line", "=", "reader", ".", "readLine", "(", ")", ")", "!=", "null", ")", "{", "xml", ".", "append", "(", "line", ")", ";", "xml", ".", "append", "(", "\"n\"", ")", ";", "}", "return", "xml", ".", "toString", "(", ")", ";", "}", "catch", "(", "IOException", "e", ")", "{", "e", ".", "printStackTrace", "(", ")", ";", "}", "finally", "{", "if", "(", "reader", "!=", "null", ")", "{", "try", "{", "reader", ".", "close", "(", ")", ";", "}", "catch", "(", "IOException", "e", ")", "{", "e", ".", "printStackTrace", "(", ")", ";", "}", "}", "}", "return", "null", ";", "}", "private", "void", "updateLayout", "(", ")", "{", "try", "{", "Component", "c", "=", "Clara", ".", "create", "(", "new", "ByteArrayInputStream", "(", "xmlArea", ".", "getValue", "(", ")", ".", "toString", "(", ")", ".", "getBytes", "(", ")", ")", ",", "controller", ")", ";", "split", ".", "replaceComponent", "(", "split", ".", "getSecondComponent", "(", ")", ",", "c", ")", ";", "}", "catch", "(", "LayoutInflaterException", "e", ")", "{", "mainWindow", ".", "showNotification", "(", "e", ".", "getMessage", "(", ")", ",", "Notification", ".", "TYPE_ERROR_MESSAGE", ")", ";", "}", "}", "}", "</s>"], 
    "id": 0
}
```
 

#### python

An example of 'train' looks as follows.
```
{
    "code": ["<s>", "from", "bootstrap", "import", "Bootstrap", "<EOL>", "from", "fund", "import", "InstantPaymentNotificationHandler", "<EOL>", "from", "fund", "import", "ThankYouHandler", "<EOL>", "from", "view", "import", "*", "<EOL>", "mapping", "=", "[", "(", "<EOL>", "r'/'", ",", "<EOL>", "Index", "<EOL>", ")", ",", "(", "<EOL>", "r'/ipn'", ",", "<EOL>", "InstantPaymentNotificationHandler", "<EOL>", ")", ",", "(", "<EOL>", "r'/thank-you'", ",", "<EOL>", "ThankYouHandler", "<EOL>", ")", ",", "(", "<EOL>", "r'/about\\/?'", ",", "<EOL>", "About", "<EOL>", ")", ",", "(", "<EOL>", "r'/guide\\/?'", ",", "<EOL>", "Guide", "<EOL>", ")", ",", "(", "<EOL>", "r''", ",", "<EOL>", "Download", "<EOL>", ")", ",", "(", "<EOL>", "r''", ",", "<EOL>", "Standards", "<EOL>", ")", ",", "(", "<EOL>", "r'/community\\/?'", ",", "<EOL>", "Community", "<EOL>", ")", ",", "(", "<EOL>", "r'/news\\/?'", ",", "<EOL>", "News", "<EOL>", ")", ",", "(", "<EOL>", "r'/support\\/?'", ",", "<EOL>", "Support", "<EOL>", ")", ",", "(", "<EOL>", "r'/contact\\/?'", ",", "<EOL>", "Contact", "<EOL>", ")", ",", "(", "<EOL>", "r'/press\\/?'", ",", "<EOL>", "Press", "<EOL>", ")", ",", "(", "<EOL>", "r'/legal/terms'", ",", "<EOL>", "Terms", "<EOL>", ")", ",", "(", "<EOL>", "r'/library\\/?'", ",", "<EOL>", "Library", "<EOL>", ")", ",", "(", "<EOL>", "r''", ",", "<EOL>", "Library", "<EOL>", ")", ",", "(", "<EOL>", "r''", ",", "<EOL>", "Library", "<EOL>", ")", ",", "(", "<EOL>", "r''", ",", "<EOL>", "Users", "<EOL>", ")", ",", "(", "<EOL>", "r''", ",", "<EOL>", "User", "<EOL>", ")", ",", "(", "<EOL>", "r''", ",", "<EOL>", "Design", "<EOL>", ")", ",", "(", "<EOL>", "r''", ",", "<EOL>", "Design", "<EOL>", ")", ",", "(", "<EOL>", "r''", ",", "<EOL>", "Design", "<EOL>", ")", ",", "(", "<EOL>", "r''", ",", "<EOL>", "Design", "<EOL>", ")", ",", "(", "<EOL>", "r''", ",", "<EOL>", "Design", "<EOL>", ")", ",", "(", "<EOL>", "r''", ",", "<EOL>", "RedirectSuccess", "<EOL>", ")", ",", "(", "<EOL>", "r''", ",", "<EOL>", "RedirectError", "<EOL>", ")", ",", "(", "<EOL>", "r''", ",", "<EOL>", "RedirectAfterDelete", "<EOL>", ")", ",", "(", "<EOL>", "r''", ",", "<EOL>", "Moderate", "<EOL>", ")", ",", "(", "<EOL>", "r''", ",", "<EOL>", "Bootstrap", "<EOL>", ")", ",", "(", "<EOL>", "r'/activity'", ",", "<EOL>", "ActivityScreen", "<EOL>", ")", ",", "(", "<EOL>", "r'/txns'", ",", "<EOL>", "TxnList", "<EOL>", ")", ",", "(", "<EOL>", "r''", ",", "<EOL>", "Base64Blob", "<EOL>", ")", ",", "(", "<EOL>", "r''", ",", "<EOL>", "Base64Blob", "<EOL>", ")", ",", "(", "<EOL>", "r''", ",", "<EOL>", "MessageStrings", "<EOL>", ")", ",", "(", "<EOL>", "r'/.*'", ",", "<EOL>", "NotFound", "<EOL>", ")", "<EOL>", "]", "</s>"], 
    "id": 0, 
    "path": "00/wikihouse/urls.py\n"
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




