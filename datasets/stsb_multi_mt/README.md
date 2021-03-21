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

It can be used to train [sentence embeddings](https://github.com/UKPLab/sentence-transformers) like [T-Systems-onsite/cross-en-de-roberta-sentence-transformer](https://huggingface.co/T-Systems-onsite/cross-en-de-roberta-sentence-transformer).
