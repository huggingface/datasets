---
annotations_creators:
- expert-generated
language_creators:
- found
language:
- en
license:
- unknown
multilinguality:
- monolingual
size_categories:
- 10K<n<100K
source_datasets:
- extended|conll2003
task_categories:
- token-classification
task_ids:
- named-entity-recognition
paperswithcode_id: conll
pretty_name: CoNLL++
train-eval-index:
- config: conllpp
  task: token-classification
  task_id: entity_extraction
  splits:
    train_split: train
    eval_split: test
  col_mapping:
    tokens: tokens
    ner_tags: tags
  metrics:
  - type: seqeval
    name: seqeval
dataset_info:
  features:
  - name: id
    dtype: string
  - name: tokens
    sequence: string
  - name: pos_tags
    sequence:
      class_label:
        names:
          0: '"'
          1: ''''''
          2: '#'
          3: $
          4: (
          5: )
          6: ','
          7: .
          8: ':'
          9: '``'
          10: CC
          11: CD
          12: DT
          13: EX
          14: FW
          15: IN
          16: JJ
          17: JJR
          18: JJS
          19: LS
          20: MD
          21: NN
          22: NNP
          23: NNPS
          24: NNS
          25: NN|SYM
          26: PDT
          27: POS
          28: PRP
          29: PRP$
          30: RB
          31: RBR
          32: RBS
          33: RP
          34: SYM
          35: TO
          36: UH
          37: VB
          38: VBD
          39: VBG
          40: VBN
          41: VBP
          42: VBZ
          43: WDT
          44: WP
          45: WP$
          46: WRB
  - name: chunk_tags
    sequence:
      class_label:
        names:
          0: O
          1: B-ADJP
          2: I-ADJP
          3: B-ADVP
          4: I-ADVP
          5: B-CONJP
          6: I-CONJP
          7: B-INTJ
          8: I-INTJ
          9: B-LST
          10: I-LST
          11: B-NP
          12: I-NP
          13: B-PP
          14: I-PP
          15: B-PRT
          16: I-PRT
          17: B-SBAR
          18: I-SBAR
          19: B-UCP
          20: I-UCP
          21: B-VP
          22: I-VP
  - name: ner_tags
    sequence:
      class_label:
        names:
          0: O
          1: B-PER
          2: I-PER
          3: B-ORG
          4: I-ORG
          5: B-LOC
          6: I-LOC
          7: B-MISC
          8: I-MISC
  config_name: conllpp
  splits:
  - name: test
    num_bytes: 1582078
    num_examples: 3453
  - name: train
    num_bytes: 6931393
    num_examples: 14041
  - name: validation
    num_bytes: 1739247
    num_examples: 3250
  download_size: 4859600
  dataset_size: 10252718
---

# Dataset Card for "conllpp"

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

- **Homepage:** [Github](https://github.com/ZihanWangKi/CrossWeigh)
- **Repository:** [Github](https://github.com/ZihanWangKi/CrossWeigh)
- **Paper:** [Aclweb](https://www.aclweb.org/anthology/D19-1519)
- **Leaderboard:**
- **Point of Contact:**

### Dataset Summary

CoNLLpp is a corrected version of the CoNLL2003 NER dataset where labels of 5.38% of the sentences in the test set
have been manually corrected. The training set and development set from CoNLL2003 is included for completeness. One 
correction on the test set for example, is:

```
{
    "tokens": ["SOCCER", "-", "JAPAN", "GET", "LUCKY", "WIN", ",", "CHINA", "IN", "SURPRISE", "DEFEAT", "."],
    "original_ner_tags_in_conll2003": ["O", "O", "B-LOC", "O", "O", "O", "O", "B-PER", "O", "O", "O", "O"],
    "corrected_ner_tags_in_conllpp": ["O", "O", "B-LOC", "O", "O", "O", "O", "B-LOC", "O", "O", "O", "O"],
}
```

### Supported Tasks and Leaderboards

[More Information Needed]

### Languages

[More Information Needed]

## Dataset Structure

### Data Instances

#### conllpp

- **Size of downloaded dataset files:** 4.63 MB
- **Size of the generated dataset:** 9.78 MB
- **Total amount of disk used:** 14.41 MB

An example of 'train' looks as follows.
```
This example was too long and was cropped:

{
    "chunk_tags": [11, 12, 12, 21, 13, 11, 11, 21, 13, 11, 12, 13, 11, 21, 22, 11, 12, 17, 11, 21, 17, 11, 12, 12, 21, 22, 22, 13, 11, 0],
    "id": "0",
    "ner_tags": [0, 3, 4, 0, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    "pos_tags": [12, 22, 22, 38, 15, 22, 28, 38, 15, 16, 21, 35, 24, 35, 37, 16, 21, 15, 24, 41, 15, 16, 21, 21, 20, 37, 40, 35, 21, 7],
    "tokens": ["The", "European", "Commission", "said", "on", "Thursday", "it", "disagreed", "with", "German", "advice", "to", "consumers", "to", "shun", "British", "lamb", "until", "scientists", "determine", "whether", "mad", "cow", "disease", "can", "be", "transmitted", "to", "sheep", "."]
}
```

### Data Fields

The data fields are the same among all splits.

#### conllpp
- `id`: a `string` feature.
- `tokens`: a `list` of `string` features.
- `pos_tags`: a `list` of classification labels, with possible values including `"` (0), `''` (1), `#` (2), `$` (3), `(` (4).
- `chunk_tags`: a `list` of classification labels, with possible values including `O` (0), `B-ADJP` (1), `I-ADJP` (2), `B-ADVP` (3), `I-ADVP` (4).
- `ner_tags`: a `list` of classification labels, with possible values including `O` (0), `B-PER` (1), `I-PER` (2), `B-ORG` (3), `I-ORG` (4).

### Data Splits

|  name   |train|validation|test|
|---------|----:|---------:|---:|
|conll2003|14041|      3250|3453|

## Dataset Creation

### Curation Rationale

[More Information Needed]

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

[More Information Needed]

### Licensing Information

[More Information Needed]

### Citation Information

```
@inproceedings{wang2019crossweigh,
  title={CrossWeigh: Training Named Entity Tagger from Imperfect Annotations},
  author={Wang, Zihan and Shang, Jingbo and Liu, Liyuan and Lu, Lihao and Liu, Jiacheng and Han, Jiawei},
  booktitle={Proceedings of the 2019 Conference on Empirical Methods in Natural Language Processing and the 9th International Joint Conference on Natural Language Processing (EMNLP-IJCNLP)},
  pages={5157--5166},
  year={2019}
}
```

### Contributions

Thanks to [@ZihanWangKi](https://github.com/ZihanWangKi) for adding this dataset.