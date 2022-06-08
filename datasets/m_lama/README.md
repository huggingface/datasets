---
annotations_creators:
- crowdsourced
- expert-generated
- machine-generated
language_creators:
- crowdsourced
- expert-generated
- machine-generated
languages:
- af
- ar
- az
- be
- bg
- bn
- ca
- ceb
- cs
- cy
- da
- de
- el
- en
- es
- et
- eu
- fa
- fi
- fr
- ga
- gl
- he
- hi
- hr
- hu
- hy
- id
- it
- ja
- ka
- ko
- la
- lt
- lv
- ms
- nl
- pl
- pt
- ro
- ru
- sk
- sl
- sq
- sr
- sv
- ta
- th
- tr
- uk
- ur
- vi
- zh
licenses:
- cc-by-nc-sa-4.0
multilinguality:
- translation
size_categories:
- 100K<n<1M
source_datasets:
- extended|lama
task_categories:
- question-answering
- text-classification
task_ids:
- open-domain-qa
- text-scoring
- text-classification-other-probing
paperswithcode_id: null
pretty_name: MLama
---

# Dataset Card for [Dataset Name]

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

- **Homepage:** [Multilingual LAMA](http://cistern.cis.lmu.de/mlama/)
- **Repository:** [Github](https://github.com/norakassner/mlama)
- **Paper:** [Arxiv](https://arxiv.org/abs/2102.00894)
- **Point of Contact:** [Contact section](http://cistern.cis.lmu.de/mlama/)



### Dataset Summary

This dataset provides the data for mLAMA, a multilingual version of LAMA. 
Regarding LAMA see https://github.com/facebookresearch/LAMA. For mLAMA
the TREx and GoogleRE part of LAMA was considered and machine translated using 
Google Translate, and the Wikidata and Google Knowledge Graph API. The machine
translated templates were checked for validity, i.e., whether they contain 
exactly one '[X]' and one '[Y]'.

This data can be used for creating fill-in-the-blank queries like 
"Paris is the capital of [MASK]" across 53 languages. For more details see
the website http://cistern.cis.lmu.de/mlama/ or the github repo https://github.com/norakassner/mlama.

### Supported Tasks and Leaderboards

Language model knowledge probing.

### Languages

This dataset contains data in 53 languages: 
af,ar,az,be,bg,bn,ca,ceb,cs,cy,da,de,el,en,es,et,eu,fa,fi,fr,ga,gl,he,hi,hr,hu,hy,id,it,ja,ka,ko,la,lt,lv,ms,nl,pl,pt,ro,ru,sk,sl,sq,sr,sv,ta,th,tr,uk,ur,vi,zh

## Dataset Structure
For each of the 53 languages and each of the 43 relations/predicates there is a set of triples.

### Data Instances
For each language and relation there are triples, that consists of an object, a predicate and a subject. For each predicate there is a template available. An example for `dataset["test"][0]` is given here:
```python
{
'language': 'af',
'lineid': 0, 
'obj_label': 'Frankryk', 
'obj_uri': 'Q142', 
'predicate_id': 'P1001', 
'sub_label': 'President van Frankryk', 
'sub_uri': 'Q191954', 
'template': "[X] is 'n wettige term in [Y].", 
'uuid': '3fe3d4da-9df9-45ba-8109-784ce5fba38a'
}
```


### Data Fields

Each instance has the following fields
* "uuid": a unique identifier
* "lineid": a identifier unique to mlama
* "obj_id": knowledge graph id of the object
* "obj_label": surface form of the object
* "sub_id": knowledge graph id of the subject
* "sub_label": surface form of the subject
* "template": template
* "language": language code
* "predicate_id": relation id


### Data Splits

There is only one partition that is labelled as 'test data'.

## Dataset Creation

### Curation Rationale

The dataset was translated into 53 languages to investigate knowledge in pretrained language models
multilingually.

### Source Data

#### Initial Data Collection and Normalization

The data has several sources: 

LAMA (https://github.com/facebookresearch/LAMA) licensed under Attribution-NonCommercial 4.0 International (CC BY-NC 4.0)
T-REx (https://hadyelsahar.github.io/t-rex/) licensed under Creative Commons Attribution-ShareAlike 4.0 International License
Google-RE (https://github.com/google-research-datasets/relation-extraction-corpus)
Wikidata (https://www.wikidata.org/) licensed under Creative Commons CC0 License and Creative Commons Attribution-ShareAlike License

#### Who are the source language producers?

See links above. 

### Annotations

#### Annotation process

Crowdsourced (wikidata) and machine translated.

#### Who are the annotators?

Unknown. 

### Personal and Sensitive Information

Names of (most likely) famous people who have entries in Google Knowledge Graph or Wikidata.

## Considerations for Using the Data

Data was created through machine translation and automatic processes.

### Social Impact of Dataset

[More Information Needed]

### Discussion of Biases

[More Information Needed]

### Other Known Limitations

Not all triples are available in all languages.


## Additional Information

### Dataset Curators

The authors of the mLAMA paper and the authors of the original datasets.

### Licensing Information

The Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International (CC BY-NC-SA 4.0). https://creativecommons.org/licenses/by-nc-sa/4.0/

### Citation Information

```
@article{kassner2021multilingual,
  author    = {Nora Kassner and
               Philipp Dufter and
               Hinrich Sch{\"{u}}tze},
  title     = {Multilingual {LAMA:} Investigating Knowledge in Multilingual Pretrained
               Language Models},
  journal   = {CoRR},
  volume    = {abs/2102.00894},
  year      = {2021},
  url       = {https://arxiv.org/abs/2102.00894},
  archivePrefix = {arXiv},
  eprint    = {2102.00894},
  timestamp = {Tue, 09 Feb 2021 13:35:56 +0100},
  biburl    = {https://dblp.org/rec/journals/corr/abs-2102-00894.bib},
  bibsource = {dblp computer science bibliography, https://dblp.org},
  note      = {to appear in EACL2021}
}
```

### Contributions

Thanks to [@pdufter](https://github.com/pdufter) for adding this dataset.
