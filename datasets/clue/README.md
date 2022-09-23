---
annotations_creators:
- other
language:
- zh
language_creators:
- other
license:
- unknown
multilinguality:
- monolingual
pretty_name: 'CLUE: Chinese Language Understanding Evaluation benchmark'
size_categories:
- 100K<n<1M
source_datasets:
- original
task_categories:
- text-classification
- multiple-choice
task_ids:
- topic-classification
- semantic-similarity-scoring
- natural-language-inference
- text-classification-other-coreference-nli
- text-classification-other-qa-nli
- multiple-choice-qa
paperswithcode_id: clue
dataset_info:
- config_name: afqmc
  features:
  - name: sentence1
    dtype: string
  - name: sentence2
    dtype: string
  - name: label
    dtype:
      class_label:
        names:
          0: '0'
          1: '1'
  - name: idx
    dtype: int32
  splits:
  - name: test
    num_bytes: 378726
    num_examples: 3861
  - name: train
    num_bytes: 3396535
    num_examples: 34334
  - name: validation
    num_bytes: 426293
    num_examples: 4316
  download_size: 1195044
  dataset_size: 4201554
- config_name: tnews
  features:
  - name: sentence
    dtype: string
  - name: label
    dtype:
      class_label:
        names:
          0: '100'
          1: '101'
          2: '102'
          3: '103'
          4: '104'
          5: '106'
          6: '107'
          7: '108'
          8: '109'
          9: '110'
          10: '112'
          11: '113'
          12: '114'
          13: '115'
          14: '116'
  - name: idx
    dtype: int32
  splits:
  - name: test
    num_bytes: 810974
    num_examples: 10000
  - name: train
    num_bytes: 4245701
    num_examples: 53360
  - name: validation
    num_bytes: 797926
    num_examples: 10000
  download_size: 5123575
  dataset_size: 5854601
- config_name: iflytek
  features:
  - name: sentence
    dtype: string
  - name: label
    dtype:
      class_label:
        names:
          0: '0'
          1: '1'
          2: '2'
          3: '3'
          4: '4'
          5: '5'
          6: '6'
          7: '7'
          8: '8'
          9: '9'
          10: '10'
          11: '11'
          12: '12'
          13: '13'
          14: '14'
          15: '15'
          16: '16'
          17: '17'
          18: '18'
          19: '19'
          20: '20'
          21: '21'
          22: '22'
          23: '23'
          24: '24'
          25: '25'
          26: '26'
          27: '27'
          28: '28'
          29: '29'
          30: '30'
          31: '31'
          32: '32'
          33: '33'
          34: '34'
          35: '35'
          36: '36'
          37: '37'
          38: '38'
          39: '39'
          40: '40'
          41: '41'
          42: '42'
          43: '43'
          44: '44'
          45: '45'
          46: '46'
          47: '47'
          48: '48'
          49: '49'
          50: '50'
          51: '51'
          52: '52'
          53: '53'
          54: '54'
          55: '55'
          56: '56'
          57: '57'
          58: '58'
          59: '59'
          60: '60'
          61: '61'
          62: '62'
          63: '63'
          64: '64'
          65: '65'
          66: '66'
          67: '67'
          68: '68'
          69: '69'
          70: '70'
          71: '71'
          72: '72'
          73: '73'
          74: '74'
          75: '75'
          76: '76'
          77: '77'
          78: '78'
          79: '79'
          80: '80'
          81: '81'
          82: '82'
          83: '83'
          84: '84'
          85: '85'
          86: '86'
          87: '87'
          88: '88'
          89: '89'
          90: '90'
          91: '91'
          92: '92'
          93: '93'
          94: '94'
          95: '95'
          96: '96'
          97: '97'
          98: '98'
          99: '99'
          100: '100'
          101: '101'
          102: '102'
          103: '103'
          104: '104'
          105: '105'
          106: '106'
          107: '107'
          108: '108'
          109: '109'
          110: '110'
          111: '111'
          112: '112'
          113: '113'
          114: '114'
          115: '115'
          116: '116'
          117: '117'
          118: '118'
  - name: idx
    dtype: int32
  splits:
  - name: test
    num_bytes: 2105688
    num_examples: 2600
  - name: train
    num_bytes: 10028613
    num_examples: 12133
  - name: validation
    num_bytes: 2157123
    num_examples: 2599
  download_size: 6505938
  dataset_size: 14291424
- config_name: cmnli
  features:
  - name: sentence1
    dtype: string
  - name: sentence2
    dtype: string
  - name: label
    dtype:
      class_label:
        names:
          0: neutral
          1: entailment
          2: contradiction
  - name: idx
    dtype: int32
  splits:
  - name: test
    num_bytes: 2386837
    num_examples: 13880
  - name: train
    num_bytes: 67685309
    num_examples: 391783
  - name: validation
    num_bytes: 2051845
    num_examples: 12241
  download_size: 31404066
  dataset_size: 72123991
- config_name: cluewsc2020
  features:
  - name: idx
    dtype: int32
  - name: text
    dtype: string
  - name: label
    dtype:
      class_label:
        names:
          0: 'true'
          1: 'false'
  - name: target
    struct:
    - name: span1_text
      dtype: string
    - name: span2_text
      dtype: string
    - name: span1_index
      dtype: int32
    - name: span2_index
      dtype: int32
  splits:
  - name: test
    num_bytes: 645649
    num_examples: 2574
  - name: train
    num_bytes: 288828
    num_examples: 1244
  - name: validation
    num_bytes: 72682
    num_examples: 304
  download_size: 281384
  dataset_size: 1007159
- config_name: csl
  features:
  - name: idx
    dtype: int32
  - name: corpus_id
    dtype: int32
  - name: abst
    dtype: string
  - name: label
    dtype:
      class_label:
        names:
          0: '0'
          1: '1'
  - name: keyword
    sequence: string
  splits:
  - name: test
    num_bytes: 2463740
    num_examples: 3000
  - name: train
    num_bytes: 16478914
    num_examples: 20000
  - name: validation
    num_bytes: 2464575
    num_examples: 3000
  download_size: 3234594
  dataset_size: 21407229
- config_name: cmrc2018
  features:
  - name: id
    dtype: string
  - name: context
    dtype: string
  - name: question
    dtype: string
  - name: answers
    sequence:
    - name: text
      dtype: string
    - name: answer_start
      dtype: int32
  splits:
  - name: test
    num_bytes: 3112066
    num_examples: 2000
  - name: train
    num_bytes: 15508110
    num_examples: 10142
  - name: trial
    num_bytes: 1606931
    num_examples: 1002
  - name: validation
    num_bytes: 5183809
    num_examples: 3219
  download_size: 3405146
  dataset_size: 25410916
- config_name: drcd
  features:
  - name: id
    dtype: string
  - name: context
    dtype: string
  - name: question
    dtype: string
  - name: answers
    sequence:
    - name: text
      dtype: string
    - name: answer_start
      dtype: int32
  splits:
  - name: test
    num_bytes: 4982402
    num_examples: 3493
  - name: train
    num_bytes: 37443458
    num_examples: 26936
  - name: validation
    num_bytes: 5222753
    num_examples: 3524
  download_size: 7264200
  dataset_size: 47648613
- config_name: chid
  features:
  - name: idx
    dtype: int32
  - name: candidates
    sequence: string
  - name: content
    sequence: string
  - name: answers
    sequence:
    - name: text
      dtype: string
    - name: candidate_id
      dtype: int32
  splits:
  - name: test
    num_bytes: 11480463
    num_examples: 3447
  - name: train
    num_bytes: 252478178
    num_examples: 84709
  - name: validation
    num_bytes: 10117789
    num_examples: 3218
  download_size: 139199202
  dataset_size: 274076430
- config_name: c3
  features:
  - name: id
    dtype: int32
  - name: context
    sequence: string
  - name: question
    dtype: string
  - name: choice
    sequence: string
  - name: answer
    dtype: string
  splits:
  - name: test
    num_bytes: 1600166
    num_examples: 1625
  - name: train
    num_bytes: 9672787
    num_examples: 11869
  - name: validation
    num_bytes: 2990967
    num_examples: 3816
  download_size: 3495930
  dataset_size: 14263920
- config_name: ocnli
  features:
  - name: sentence1
    dtype: string
  - name: sentence2
    dtype: string
  - name: label
    dtype:
      class_label:
        names:
          0: neutral
          1: entailment
          2: contradiction
  - name: idx
    dtype: int32
  splits:
  - name: test
    num_bytes: 376066
    num_examples: 3000
  - name: train
    num_bytes: 6187190
    num_examples: 50437
  - name: validation
    num_bytes: 366235
    num_examples: 2950
  download_size: 4359754
  dataset_size: 6929491
- config_name: diagnostics
  features:
  - name: sentence1
    dtype: string
  - name: sentence2
    dtype: string
  - name: label
    dtype:
      class_label:
        names:
          0: neutral
          1: entailment
          2: contradiction
  - name: idx
    dtype: int32
  splits:
  - name: test
    num_bytes: 42400
    num_examples: 514
  download_size: 12062
  dataset_size: 42400
---

# Dataset Card for "clue"

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

- **Homepage:** https://www.cluebenchmarks.com
- **Repository:** https://github.com/CLUEbenchmark/CLUE
- **Paper:** [CLUE: A Chinese Language Understanding Evaluation Benchmark](https://aclanthology.org/2020.coling-main.419/)
- **Point of Contact:** [Zhenzhong Lan](mailto:lanzhenzhong@westlake.edu.cn)
- **Size of downloaded dataset files:** 189.48 MB
- **Size of the generated dataset:** 463.81 MB
- **Total amount of disk used:** 653.29 MB

### Dataset Summary

CLUE, A Chinese Language Understanding Evaluation Benchmark
(https://www.cluebenchmarks.com/) is a collection of resources for training,
evaluating, and analyzing Chinese language understanding systems.

### Supported Tasks and Leaderboards

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

### Languages

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

## Dataset Structure

### Data Instances

#### afqmc

- **Size of downloaded dataset files:** 1.14 MB
- **Size of the generated dataset:** 4.01 MB
- **Total amount of disk used:** 5.15 MB

An example of 'validation' looks as follows.
```
{
    "idx": 0,
    "label": 0,
    "sentence1": "双十一花呗提额在哪",
    "sentence2": "里可以提花呗额度"
}
```

#### c3

- **Size of downloaded dataset files:** 3.05 MB
- **Size of the generated dataset:** 14.96 MB
- **Total amount of disk used:** 18.02 MB

An example of 'train' looks as follows.
```
This example was too long and was cropped:

{
    "answer": "比人的灵敏",
    "choice": ["没有人的灵敏", "和人的差不多", "和人的一样好", "比人的灵敏"],
    "context": "[\"许多动物的某些器官感觉特别灵敏，它们能比人类提前知道一些灾害事件的发生，例如，海洋中的水母能预报风暴，老鼠能事先躲避矿井崩塌或有害气体，等等。地震往往能使一些动物的某些感觉器官受到刺激而发生异常反应。如一个地区的重力发生变异，某些动物可能通过它们的平衡...",
    "id": 1,
    "question": "动物的器官感觉与人的相比有什么不同?"
}
```

#### chid

- **Size of downloaded dataset files:** 132.75 MB
- **Size of the generated dataset:** 261.38 MB
- **Total amount of disk used:** 394.13 MB

An example of 'train' looks as follows.
```
This example was too long and was cropped:

{
    "answers": {
        "candidate_id": [3, 5, 6, 1, 7, 4, 0],
        "text": ["碌碌无为", "无所作为", "苦口婆心", "得过且过", "未雨绸缪", "软硬兼施", "传宗接代"]
    },
    "candidates": "[\"传宗接代\", \"得过且过\", \"咄咄逼人\", \"碌碌无为\", \"软硬兼施\", \"无所作为\", \"苦口婆心\", \"未雨绸缪\", \"和衷共济\", \"人老珠黄\"]...",
    "content": "[\"谈到巴萨目前的成就，瓜迪奥拉用了“坚持”两个字来形容。自从上世纪90年代克鲁伊夫带队以来，巴萨就坚持每年都有拉玛西亚球员进入一队的传统。即便是范加尔时代，巴萨强力推出的“巴萨五鹰”德拉·佩纳、哈维、莫雷罗、罗杰·加西亚和贝拉乌桑几乎#idiom0000...",
    "idx": 0
}
```

#### cluewsc2020

- **Size of downloaded dataset files:** 0.27 MB
- **Size of the generated dataset:** 0.98 MB
- **Total amount of disk used:** 1.23 MB

An example of 'train' looks as follows.
```
{
    "idx": 0,
    "label": 1,
    "target": {
        "span1_index": 3,
        "span1_text": "伤口",
        "span2_index": 27,
        "span2_text": "它们"
    },
    "text": "裂开的伤口涂满尘土，里面有碎石子和木头刺，我小心翼翼把它们剔除出去。"
}
```

#### cmnli

- **Size of downloaded dataset files:** 29.95 MB
- **Size of the generated dataset:** 68.78 MB
- **Total amount of disk used:** 98.73 MB

An example of 'train' looks as follows.
```
{
    "idx": 0,
    "label": 0,
    "sentence1": "从概念上讲，奶油略读有两个基本维度-产品和地理。",
    "sentence2": "产品和地理位置是使奶油撇油起作用的原因。"
}
```

### Data Fields

The data fields are the same among all splits.

#### afqmc
- `sentence1`: a `string` feature.
- `sentence2`: a `string` feature.
- `label`: a classification label, with possible values including `0` (0), `1` (1).
- `idx`: a `int32` feature.

#### c3
- `id`: a `int32` feature.
- `context`: a `list` of `string` features.
- `question`: a `string` feature.
- `choice`: a `list` of `string` features.
- `answer`: a `string` feature.

#### chid
- `idx`: a `int32` feature.
- `candidates`: a `list` of `string` features.
- `content`: a `list` of `string` features.
- `answers`: a dictionary feature containing:
  - `text`: a `string` feature.
  - `candidate_id`: a `int32` feature.

#### cluewsc2020
- `idx`: a `int32` feature.
- `text`: a `string` feature.
- `label`: a classification label, with possible values including `true` (0), `false` (1).
- `span1_text`: a `string` feature.
- `span2_text`: a `string` feature.
- `span1_index`: a `int32` feature.
- `span2_index`: a `int32` feature.

#### cmnli
- `sentence1`: a `string` feature.
- `sentence2`: a `string` feature.
- `label`: a classification label, with possible values including `neutral` (0), `entailment` (1), `contradiction` (2).
- `idx`: a `int32` feature.

### Data Splits

|   name    |train |validation|test |
|-----------|-----:|---------:|----:|
|afqmc      | 34334|      4316| 3861|
|c3         | 11869|      3816| 3892|
|chid       | 84709|      3218| 3231|
|cluewsc2020|  1244|       304|  290|
|cmnli      |391783|     12241|13880|

## Dataset Creation

### Curation Rationale

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

### Source Data

#### Initial Data Collection and Normalization

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

#### Who are the source language producers?

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

### Annotations

#### Annotation process

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

#### Who are the annotators?

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

### Personal and Sensitive Information

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

## Considerations for Using the Data

### Social Impact of Dataset

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

### Discussion of Biases

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

### Other Known Limitations

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

## Additional Information

### Dataset Curators

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

### Licensing Information

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

### Citation Information

```
@inproceedings{xu-etal-2020-clue,
    title = "{CLUE}: A {C}hinese Language Understanding Evaluation Benchmark",
    author = "Xu, Liang  and
      Hu, Hai  and
      Zhang, Xuanwei  and
      Li, Lu  and
      Cao, Chenjie  and
      Li, Yudong  and
      Xu, Yechen  and
      Sun, Kai  and
      Yu, Dian  and
      Yu, Cong  and
      Tian, Yin  and
      Dong, Qianqian  and
      Liu, Weitang  and
      Shi, Bo  and
      Cui, Yiming  and
      Li, Junyi  and
      Zeng, Jun  and
      Wang, Rongzhao  and
      Xie, Weijian  and
      Li, Yanting  and
      Patterson, Yina  and
      Tian, Zuoyu  and
      Zhang, Yiwen  and
      Zhou, He  and
      Liu, Shaoweihua  and
      Zhao, Zhe  and
      Zhao, Qipeng  and
      Yue, Cong  and
      Zhang, Xinrui  and
      Yang, Zhengliang  and
      Richardson, Kyle  and
      Lan, Zhenzhong",
    booktitle = "Proceedings of the 28th International Conference on Computational Linguistics",
    month = dec,
    year = "2020",
    address = "Barcelona, Spain (Online)",
    publisher = "International Committee on Computational Linguistics",
    url = "https://aclanthology.org/2020.coling-main.419",
    doi = "10.18653/v1/2020.coling-main.419",
    pages = "4762--4772",
}
```


### Contributions

Thanks to [@thomwolf](https://github.com/thomwolf), [@JetRunner](https://github.com/JetRunner) for adding this dataset.