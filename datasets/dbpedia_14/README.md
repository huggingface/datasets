---
annotations_creators:
- machine-generated
language_creators:
- crowdsourced
languages:
- en
licenses:
- cc-by-sa-3.0
multilinguality:
- monolingual
size_categories:
- 100K<n<1M
source_datasets:
- original
task_categories:
- text-classification
task_ids:
- topic-classification
paperswithcode_id: dbpedia
---

# Dataset Card for DBpedia14

## Table of Contents
- [Dataset Description](#dataset-description)
  - [Dataset Summary](#dataset-summary)
  - [Supported Tasks and Leaderboards](#supported-tasks-and-leaderboards)
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
  - [Contributions](#contributions)

## Dataset Description

- **Homepage:** [DBpedia14 homepage](https://wiki.dbpedia.org/develop/datasets)
- **Repository:** [DBpedia14 repository](https://github.com/dbpedia/extraction-framework)
- **Paper:** [DBpedia--a large-scale, multilingual knowledge base extracted from Wikipedia](https://content.iospress.com/articles/semantic-web/sw134)
- **Point of Contact:** [Xiang Zhang](mailto:xiang.zhang@nyu.edu)

### Dataset Summary

The DBpedia ontology classification dataset is constructed by picking 14 non-overlapping classes
from DBpedia 2014. They are listed in classes.txt. From each of thse 14 ontology classes, we
randomly choose 40,000 training samples and 5,000 testing samples. Therefore, the total size
of the training dataset is 560,000 and testing dataset 70,000.
There are 3 columns in the dataset (same for train and test splits), corresponding to class index
(1 to 14), title and content. The title and content are escaped using double quotes ("), and any
internal double quote is escaped by 2 double quotes (""). There are no new lines in title or content.

### Supported Tasks and Leaderboards

- `text-classification`, `topic-classification`: The dataset is mainly used for text classification: given the content
and the title, predict the correct topic. 

### Languages

Although DBpedia is a multilingual knowledge base, the DBpedia14 extract contains English data mainly, other languages may appear
(e.g. a film whose title is origanlly not English).  

## Dataset Structure

### Data Instances

A typical data point, comprises of a title, a content and the corresponding label. 

An example from the DBpedia test set looks as follows:
```
{
    'title':'',
    'content':" TY KU /taɪkuː/ is an American alcoholic beverage company that specializes in sake and other spirits. The privately-held company was founded in 2004 and is headquartered in New York City New York. While based in New York TY KU's beverages are made in Japan through a joint venture with two sake breweries. Since 2011 TY KU's growth has extended its products into all 50 states.",
    'label':0
}
```

### Data Fields

- 'title': a string containing the title of the document - escaped using double quotes (") and any internal double quote is escaped by 2 double quotes ("").
- 'content': a string containing the body of the document - escaped using double quotes (") and any internal double quote is escaped by 2 double quotes ("").
- 'label': one of the 14 possible topics.

### Data Splits

The data is split into a training and test set.
For each of the 14 classes we have 40,000 training samples and 5,000 testing samples.
Therefore, the total size of the training dataset is 560,000 and testing dataset 70,000.

## Dataset Creation

### Curation Rationale

The DBPedia ontology classification dataset is constructed by Xiang Zhang (xiang.zhang@nyu.edu), licensed under the terms of the Creative Commons Attribution-ShareAlike License and the GNU Free Documentation License. It is used as a text classification benchmark in the following paper: Xiang Zhang, Junbo Zhao, Yann LeCun. Character-level Convolutional Networks for Text Classification. Advances in Neural Information Processing Systems 28 (NIPS 2015).

### Source Data

#### Initial Data Collection and Normalization

[More Information Needed]

#### Who are the source language producers?

[More Information Needed]

### Annotations

#### Annotation process

[More Information Needed]

#### Who are the annotators?

[More Information Needed]

### Personal and Sensitive Information

[More Information Needed]

## Considerations for Using the Data

### Social Impact of Dataset

[More Information Needed]

### Discussion of Biases

[More Information Needed]

### Other Known Limitations

[More Information Needed]

## Additional Information

### Dataset Curators

The DBPedia ontology classification dataset is constructed by Xiang Zhang (xiang.zhang@nyu.edu), licensed under the terms of the Creative Commons Attribution-ShareAlike License and the GNU Free Documentation License. It is used as a text classification benchmark in the following paper: Xiang Zhang, Junbo Zhao, Yann LeCun. Character-level Convolutional Networks for Text Classification. Advances in Neural Information Processing Systems 28 (NIPS 2015).

### Licensing Information

The DBPedia ontology classification dataset is licensed under the terms of the Creative Commons Attribution-ShareAlike License and the GNU Free Documentation License.

### Citation Information

Xiang Zhang, Junbo Zhao, Yann LeCun. Character-level Convolutional Networks for Text Classification. Advances in Neural Information Processing Systems 28 (NIPS 2015).

Lehmann, Jens, Robert Isele, Max Jakob, Anja Jentzsch, Dimitris Kontokostas, Pablo N. Mendes, Sebastian Hellmann et al. "DBpedia–a large-scale, multilingual knowledge base extracted from Wikipedia." Semantic web 6, no. 2 (2015): 167-195.
### Contributions

Thanks to [@hfawaz](https://github.com/hfawaz) for adding this dataset.