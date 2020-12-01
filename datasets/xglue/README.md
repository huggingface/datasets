---
annotations_creators:
  mlqa:
  - crowdsourced
  nc:
  - machine-generated
  ner:
  - expert-generated
  - found
  ntg:
  - machine-generated
  paws-x:
  - expert-generated
  pos:
  - expert-generated
  - found
  qadsm:
  - machine-generated
  qam:
  - machine-generated
  qg:
  - machine-generated
  wpr:
  - machine-generated
  xnli:
  - machine-generated
language_creators:
  mlqa:
  - found
  nc:
  - found
  ner:
  - crowdsourced
  - expert-generated
  ntg:
  - machine-generated
  paws-x:
  - expert-generated
  pos:
  - crowdsourced
  - expert-generated
  qadsm:
  - found
  qam:
  - found
  qg:
  - machine-generated
  wpr:
  - found
  xnli:
  - crowdsourced
  - expert-generated
languages:
  mlqa:
  - ar
  - de
  - en
  - es
  - hi
  - vi
  - zh
  nc:
	- en
	- de
	- es
	- fr
	- ru
  ner:
  - de
  - en
  - es
  - nl
  ntg:
	- en
	- de
	- es
	- fr
	- ru
  paws-x:
	- en
	- de
	- es
	- fr
  pos:
  - ar
  - bg
  - de
  - el
  - en
  - es
  - fr
  - hi
  - it
  - nl
  - pl
  - ru
  - th
  - tr
  - ur
  - vi
  - zh
  qadsm:
	- en
	- de
	- fr
  qam:
	- en
	- de
	- fr
  qg:
	- en
	- de
	- fr
	- pt
	- it
	- zh
  wpr:
	- en
	- de
	- fr
	- es
	- it
	- pt
	- zh
  xnli:
  - ar
  - bg
  - de
  - el
  - en
  - es
  - fr
  - hi
  - ru
  - sw
  - th
  - tr
  - ur
  - vi
  - zh
licenses:
  mlqa:
  - cc-by-sa-4.0
  nc:
  - unknown
  ner:
  - unknown
  ntg:
  - unknown
  paws-x:
  - unknown
  pos:
  - other-Licence Universal Dependencies v2.5
  qadsm:
  - unknown
  qam:
  - unknown
  qg:
  - unknown
  wpr:
  - unknown
  xnli:
  - cc-by-nc-4.0
multilinguality:
  mlqa:
  - multilingual
  nc:
  - multilingual
  ner:
  - multilingual
  ntg:
  - multilingual
  paws-x:
  - multilingual
  pos:
  - multilingual
  qadsm:
  - multilingual
  qam:
  - multilingual
  qg:
  - multilingual
  wpr:
  - multilingual
  xnli:
  - multilingual
  - translation
size_categories:
  mlqa:
  - 100K<n<1M
  nc:
  - 100K<n<1M
  ner:
  - 10K<n<100K
  ntg:
  - 100K<n<1M
  paws-x:
  - 10K<n<100K
  pos:
  - 10K<n<100K
  qadsm:
  - 100K<n<1M
  qam:
  - 100K<n<1M
  qg:
  - 100K<n<1M
  wpr:
  - 100K<n<1M
  xnli:
  - 100K<n<1M
source_datasets:
  mlqa:
  - extended|squad
  nc:
  - original
  ner:
  - extended|conll2003
  ntg:
  - original
  paws-x:
  - original
  pos: 
  - original
  qadsm:
  - original
  qam:
  - original
  qg:
  - original
  wpr:
  - original
  xnli:
  - extended|xnli
task_categories:
  mlqa:
  - question-answering
  nc:
  - text-classification
  ner:
  - structure-prediction
  ntg:
  - conditional-text-generation
  paws-x:
  - text-classification
  pos:
  - structure-prediction
  qadsm:
  - text-classification
  qam:
  - text-classification
  qg:
  - conditional-text-generation
  wpr:
  - text-classification
  xnli:
  - text-classification
task_ids:
  mlqa:
  - extractive-qa
  - open-domain-qa
  nc:
  - topic-classification
  ner:
  - named-entity-recognition
  ntg:
  - summarization
  paws-x:
  - text-classification-other-paraphrase identification
  pos:
  - parsing
  qadsm:
  - acceptability-classification
  qam:
  - acceptability-classification
  qg:
  - conditional-text-generation-other-question-answering
  wpr:
  - acceptability-classification
  xnli:
  - natural-language-inference
---

# Dataset Card for XGLUE

## Table of Contents
- [Dataset Description](#dataset-description)
  - [Dataset Summary](#dataset-summary)
  - [Leaderboards](#leaderboards)
- [Additional Information](#additional-information)
  - [Dataset Curators](#dataset-curators)
  - [Licensing Information](#licensing-information)
  - [Citation Information](#citation-information)

## Dataset Description

- **Homepage:** [XGLUE homepage](https://microsoft.github.io/XGLUE/)
- **Paper:** [XGLUE: A New Benchmark Dataset for Cross-lingual Pre-training, Understanding and Generation](https://arxiv.org/abs/1907.09190)

### Dataset Summary

XGLUE is a new benchmark dataset to evaluate the performance of cross-lingual pre-trained models with respect to cross-lingual natural language understanding and generation. 

The training data of each task is in English while the validation and test data is present in multiple different languages.
The following table shows which languages are present as validation and test data for each config.

![Available Languages for Test and Validation Data](https://raw.githubusercontent.com/patrickvonplaten/scientific_images/master/xglue_langs.png)

Therefore, for each config, a cross-lingual pre-trained model should be fine-tuned on the English training data, and evaluated on for all languages.

### Leaderboards

The XGLUE leaderboard can be found on the [homepage](https://microsoft.github.io/XGLUE/) and 
consits of a XGLUE-Understanding Score (the average of the tasks `ner`, `pos`, `mlqa`, `nc`, `xnli`, `paws-x`, `qadsm`, `wpr`, `qam`) and a XGLUE-Generation Score (the average of the tasks `qg`, `ntg`).

## Additional Information

### Dataset Curators

The dataset is maintained mainly by Yaobo Liang, Yeyun Gong, Nan Duan, Ming Gong, Linjun Shou, and Daniel Campos from Microsoft Research.

### Licensing Information

The licensing status of the dataset hinges on the legal status of [XGLUE](https://microsoft.github.io/XGLUE/) hich is unclear.

### Citation Information

```
@article{Liang2020XGLUEAN,
  title={XGLUE: A New Benchmark Dataset for Cross-lingual Pre-training, Understanding and Generation},
  author={Yaobo Liang and Nan Duan and Yeyun Gong and Ning Wu and Fenfei Guo and Weizhen Qi and Ming Gong and Linjun Shou and Daxin Jiang and Guihong Cao and Xiaodong Fan and Ruofei Zhang and Rahul Agrawal and Edward Cui and Sining Wei and Taroon Bharti and Ying Qiao and Jiun-Hung Chen and Winnie Wu and Shuguang Liu and Fan Yang and Daniel Campos and Rangan Majumder and Ming Zhou},
  journal={arXiv},
  year={2020},
  volume={abs/2004.01401}
}
```
