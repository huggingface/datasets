---
annotations_creators:
- crowdsourced
language_creators:
- crowdsourced
- found
- machine-generated
language:
- de
- en
- es
- fr
- it
- nl
- pl
- pt
- ru
- zh
license:
- other
multilinguality:
- multilingual
size_categories:
- 10K<n<100K
source_datasets:
- extended|other-sts-b
task_categories:
- text-classification
task_ids:
- text-scoring
- semantic-similarity-scoring
paperswithcode_id: null
pretty_name: STSb Multi MT
dataset_info:
- config_name: en
  features:
  - name: sentence1
    dtype: string
  - name: sentence2
    dtype: string
  - name: similarity_score
    dtype: float32
  splits:
  - name: dev
    num_bytes: 210072
    num_examples: 1500
  - name: test
    num_bytes: 164466
    num_examples: 1379
  - name: train
    num_bytes: 731803
    num_examples: 5749
  download_size: 1072429
  dataset_size: 1106341
- config_name: de
  features:
  - name: sentence1
    dtype: string
  - name: sentence2
    dtype: string
  - name: similarity_score
    dtype: float32
  splits:
  - name: dev
    num_bytes: 247077
    num_examples: 1500
  - name: test
    num_bytes: 193333
    num_examples: 1379
  - name: train
    num_bytes: 867473
    num_examples: 5749
  download_size: 1279173
  dataset_size: 1307883
- config_name: es
  features:
  - name: sentence1
    dtype: string
  - name: sentence2
    dtype: string
  - name: similarity_score
    dtype: float32
  splits:
  - name: dev
    num_bytes: 245250
    num_examples: 1500
  - name: test
    num_bytes: 194616
    num_examples: 1379
  - name: train
    num_bytes: 887101
    num_examples: 5749
  download_size: 1294160
  dataset_size: 1326967
- config_name: fr
  features:
  - name: sentence1
    dtype: string
  - name: sentence2
    dtype: string
  - name: similarity_score
    dtype: float32
  splits:
  - name: dev
    num_bytes: 254083
    num_examples: 1500
  - name: test
    num_bytes: 200446
    num_examples: 1379
  - name: train
    num_bytes: 910195
    num_examples: 5749
  download_size: 1332515
  dataset_size: 1364724
- config_name: it
  features:
  - name: sentence1
    dtype: string
  - name: sentence2
    dtype: string
  - name: similarity_score
    dtype: float32
  splits:
  - name: dev
    num_bytes: 243144
    num_examples: 1500
  - name: test
    num_bytes: 191647
    num_examples: 1379
  - name: train
    num_bytes: 871526
    num_examples: 5749
  download_size: 1273630
  dataset_size: 1306317
- config_name: nl
  features:
  - name: sentence1
    dtype: string
  - name: sentence2
    dtype: string
  - name: similarity_score
    dtype: float32
  splits:
  - name: dev
    num_bytes: 234887
    num_examples: 1500
  - name: test
    num_bytes: 182904
    num_examples: 1379
  - name: train
    num_bytes: 833667
    num_examples: 5749
  download_size: 1217753
  dataset_size: 1251458
- config_name: pl
  features:
  - name: sentence1
    dtype: string
  - name: sentence2
    dtype: string
  - name: similarity_score
    dtype: float32
  splits:
  - name: dev
    num_bytes: 231758
    num_examples: 1500
  - name: test
    num_bytes: 181266
    num_examples: 1379
  - name: train
    num_bytes: 828433
    num_examples: 5749
  download_size: 1212336
  dataset_size: 1241457
- config_name: pt
  features:
  - name: sentence1
    dtype: string
  - name: sentence2
    dtype: string
  - name: similarity_score
    dtype: float32
  splits:
  - name: dev
    num_bytes: 240559
    num_examples: 1500
  - name: test
    num_bytes: 189163
    num_examples: 1379
  - name: train
    num_bytes: 854356
    num_examples: 5749
  download_size: 1251508
  dataset_size: 1284078
- config_name: ru
  features:
  - name: sentence1
    dtype: string
  - name: sentence2
    dtype: string
  - name: similarity_score
    dtype: float32
  splits:
  - name: dev
    num_bytes: 386268
    num_examples: 1500
  - name: test
    num_bytes: 300007
    num_examples: 1379
  - name: train
    num_bytes: 1391674
    num_examples: 5749
  download_size: 2051645
  dataset_size: 2077949
- config_name: zh
  features:
  - name: sentence1
    dtype: string
  - name: sentence2
    dtype: string
  - name: similarity_score
    dtype: float32
  splits:
  - name: dev
    num_bytes: 195821
    num_examples: 1500
  - name: test
    num_bytes: 154834
    num_examples: 1379
  - name: train
    num_bytes: 694424
    num_examples: 5749
  download_size: 1006892
  dataset_size: 1045079
---

# Dataset Card for STSb Multi MT

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

- **Repository**: https://github.com/PhilipMay/stsb-multi-mt
- **Homepage (original dataset):** https://ixa2.si.ehu.es/stswiki/index.php/STSbenchmark
- **Paper about original dataset:** https://arxiv.org/abs/1708.00055
- **Leaderboard:** https://ixa2.si.ehu.eus/stswiki/index.php/STSbenchmark#Results
- **Point of Contact:** [Open an issue on GitHub](https://github.com/PhilipMay/stsb-multi-mt/issues/new)

### Dataset Summary

> STS Benchmark comprises a selection of the English datasets used in the STS tasks organized
> in the context of SemEval between 2012 and 2017. The selection of datasets include text from
> image captions, news headlines and user forums. ([source](https://ixa2.si.ehu.es/stswiki/index.php/STSbenchmark))

These are different multilingual translations and the English original of the [STSbenchmark dataset](https://ixa2.si.ehu.es/stswiki/index.php/STSbenchmark). Translation has been done with [deepl.com](https://www.deepl.com/). It can be used to train [sentence embeddings](https://github.com/UKPLab/sentence-transformers) like [T-Systems-onsite/cross-en-de-roberta-sentence-transformer](https://huggingface.co/T-Systems-onsite/cross-en-de-roberta-sentence-transformer).


**Examples of Use**

Load German dev Dataset:
```python
from datasets import load_dataset
dataset = load_dataset("stsb_multi_mt", name="de", split="dev")
```

Load English train Dataset:
```python
from datasets import load_dataset
dataset = load_dataset("stsb_multi_mt", name="en", split="train")
```

### Supported Tasks and Leaderboards

[More Information Needed]

### Languages

Available languages are: de, en, es, fr, it, nl, pl, pt, ru, zh

## Dataset Structure

### Data Instances

This dataset provides pairs of sentences and a score of their similarity.

score | 2 example sentences | explanation
------|---------|------------
5 | *The bird is bathing in the sink.<br/>Birdie is washing itself in the water basin.* | The two sentences are completely equivalent, as they mean the same thing.
4 | *Two boys on a couch are playing video games.<br/>Two boys are playing a video game.* | The two sentences are mostly equivalent, but some unimportant details differ.
3 | *John said he is considered a witness but not a suspect.<br/>“He is not a suspect anymore.” John said.* | The two sentences are roughly equivalent, but some important information differs/missing.
2 | *They flew out of the nest in groups.<br/>They flew into the nest together.* | The two sentences are not equivalent, but share some details.
1 | *The woman is playing the violin.<br/>The young lady enjoys listening to the guitar.* | The two sentences are not equivalent, but are on the same topic.
0 | *The black dog is running through the snow.<br/>A race car driver is driving his car through the mud.* | The two sentences are completely dissimilar.

An example:
```
{
    "sentence1": "A man is playing a large flute.",
    "sentence2": "A man is playing a flute.",
    "similarity_score": 3.8
}
```

### Data Fields

- `sentence1`: The 1st sentence as a `str`.
- `sentence2`: The 2nd sentence as a `str`.
- `similarity_score`: The similarity score as a `float` which is `<= 5.0` and `>= 0.0`.

### Data Splits

- train with 5749 samples
- dev with 1500 samples
- test with 1379 sampples

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

See [LICENSE](https://github.com/PhilipMay/stsb-multi-mt/blob/main/LICENSE) and [download at original dataset](https://ixa2.si.ehu.eus/stswiki/index.php/STSbenchmark).

### Citation Information

```
@InProceedings{huggingface:dataset:stsb_multi_mt,
title = {Machine translated multilingual STS benchmark dataset.},
author={Philip May},
year={2021},
url={https://github.com/PhilipMay/stsb-multi-mt}
}
```

### Contributions

Thanks to [@PhilipMay](https://github.com/PhilipMay) for adding this dataset.