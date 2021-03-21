---
annotations_creators:
- crowdsourced
language_creators:
- crowdsourced
- found
- machine-generated
languages:
- en
- de
- es
- fr
- it
- nl
- pl
- pt
- ru
- zh
licenses:
- custom
multilinguality:
- multilingual
size_categories:
- 10K<n<100K
source_datasets:
- extended|other-sts-b
task_categories:
- text-scoring
task_ids:
- semantic-similarity-scoring
---

# STSb Multi MT
Machine translated multilingual STS benchmark dataset.

These are different multilingual translations and the English original of the [STSbenchmark dataset](https://ixa2.si.ehu.es/stswiki/index.php/STSbenchmark). Translation has been done with [deepl.com](https://www.deepl.com/).

- Available languages are: de, en, es, fr, it, nl, pl, pt, ru, zh
- Dataset splits are called: train, dev, test

It can be used to train [sentence embeddings](https://github.com/UKPLab/sentence-transformers) like [T-Systems-onsite/cross-en-de-roberta-sentence-transformer](https://huggingface.co/T-Systems-onsite/cross-en-de-roberta-sentence-transformer).

The dataset with translations is hosted here: <https://github.com/PhilipMay/stsb-multi-mt>
Please [open an issue](https://github.com/PhilipMay/stsb-multi-mt/issues/new) if you have questions or want to report problems.

## Examples of Use

### Load German dev Dataset
```python
from datasets import load_dataset
dataset = load_dataset('stsb_multi_mt', name="de", split='dev')
```

### Load English train Dataset
```python
from datasets import load_dataset
dataset = load_dataset('stsb_multi_mt', name="en", split='train')
```
