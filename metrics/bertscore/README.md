# Metric Card for BERT Score

## Metric description

BERTScore is an automatic evaluation metric for text generation that computes a similarity score for each token in the candidate sentence with each token in the reference sentence. It leverages the pre-trained contextual embeddings from [BERT](https://huggingface.co/bert-base-uncased) models and matches words in candidate and reference sentences by cosine similarity. 

Moreover, BERTScore computes precision, recall, and F1 measure, which can be useful for evaluating different language generation tasks. 

## How to use 

BERTScore takes 3 mandatory arguments : `predictions` (a list of string of candidate sentences), `references` (a list of strings or list of list of strings of reference sentences) and either `lang` (a string of two letters indicating the language of the sentences, in [ISO 639-1 format](https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes)) or `model_type` (a string specififying which model to use, according to the BERT specification). The default behavior of the metric is to use the suggested model for the target language when one is specified, otherwise to use the `model_type` indicated.

```python
from datasets import load_metric
bertscore = load_metric("bertscore")
predictions = ["hello there", "general kenobi"]
references = ["hello there", "general kenobi"]
results = bertscore.compute(predictions=predictions, references=references, lang="en")
```

BERTScore also accepts multiple optional arguments: 


`num_layers` (int): The layer of representation to use. The default is the number of layers tuned on WMT16 correlation data, which depends on the `model_type` used.

`verbose` (bool): Turn on intermediate status update. The default value is `False`. 

`idf` (bool or dict): Use idf weighting; can also be a precomputed idf_dict. 

`device` (str): On which the contextual embedding model will be allocated on. If this argument is `None`, the model lives on `cuda:0` if cuda is available.

`nthreads` (int): Number of threads used for computation. The default value is `4`. 

`rescale_with_baseline` (bool): Rescale BERTScore with the  pre-computed baseline. The default value is `False`. 

`batch_size` (int): BERTScore processing batch size, at least one of `model_type` or `lang`. `lang` needs to be specified when `rescale_with_baseline` is `True`.

`baseline_path` (str): Customized baseline file.

`use_fast_tokenizer` (bool): `use_fast` parameter passed to HF tokenizer. The default value is `False`. 


## Output values

BERTScore outputs a dictionary with the following values:

`precision`: The [precision](https://huggingface.co/metrics/precision) for each sentence from the `predictions` + `references` lists, which ranges from 0.0 to 1.0. 

`recall`: The [recall](https://huggingface.co/metrics/recall) for each sentence from the `predictions` + `references` lists, which ranges from 0.0 to 1.0.

`f1`: The [F1 score](https://huggingface.co/metrics/f1) for each sentence from the `predictions` + `references` lists, which ranges from 0.0 to 1.0.
 
`hashcode:` The hashcode of the library.


### Values from popular papers
The [original BERTScore paper](https://openreview.net/pdf?id=SkeHuCVFDr) reported average model selection accuracies (Hits@1) on WMT18 hybrid systems for different language pairs, which ranged from 0.004 for `en<->tr` to 0.824 for `en<->de`.

For more recent model performance, see the [metric leaderboard](https://paperswithcode.com/paper/bertscore-evaluating-text-generation-with).

## Examples 

Maximal values with the `distilbert-base-uncased` model:

```python
from datasets import load_metric
bertscore = load_metric("bertscore")
predictions = ["hello world", "general kenobi"]
references = ["hello world", "general kenobi"]
results = bertscore.compute(predictions=predictions, references=references, model_type="distilbert-base-uncased")
print(results)
{'precision': [1.0, 1.0], 'recall': [1.0, 1.0], 'f1': [1.0, 1.0], 'hashcode': 'distilbert-base-uncased_L5_no-idf_version=0.3.10(hug_trans=4.10.3)'}
```

Partial match with the `bert-base-uncased` model:

```python
from datasets import load_metric
bertscore = load_metric("bertscore")
predictions = ["hello world", "general kenobi"]
references = ["goodnight moon", "the sun is shining"]
results = bertscore.compute(predictions=predictions, references=references, model_type="distilbert-base-uncased")
print(results)
{'precision': [0.7380737066268921, 0.5584042072296143], 'recall': [0.7380737066268921, 0.5889028906822205], 'f1': [0.7380737066268921, 0.5732481479644775], 'hashcode': 'bert-base-uncased_L5_no-idf_version=0.3.10(hug_trans=4.10.3)'}
```

## Limitations and bias

The [original BERTScore paper](https://openreview.net/pdf?id=SkeHuCVFDr) showed that BERTScore correlates well with human judgment on sentence-level and system-level evaluation, but this depends on the model and language pair selected.

Furthermore, not all languages are supported by the metric -- see the [BERTScore supported language list](https://github.com/google-research/bert/blob/master/multilingual.md#list-of-languages) for more information.

Finally, calculating the BERTScore metric involves downloading the BERT model that is used to compute the score-- the default model for `en`, `roberta-large`, takes over 1.4GB of storage space and downloading it can take a significant amount of time depending on the speed of your internet connection. If this is an issue, choose a smaller model; for instance `distilbert-base-uncased` is 268MB. A full list of compatible models can be found [here](https://docs.google.com/spreadsheets/d/1RKOVpselB98Nnh_EOC4A2BYn8_201tmPODpNWu4w7xI/edit#gid=0).  


## Citation

```bibtex
@inproceedings{bert-score,
  title={BERTScore: Evaluating Text Generation with BERT},
  author={Tianyi Zhang* and Varsha Kishore* and Felix Wu* and Kilian Q. Weinberger and Yoav Artzi},
  booktitle={International Conference on Learning Representations},
  year={2020},
  url={https://openreview.net/forum?id=SkeHuCVFDr}
}
```
    
## Further References 

- [BERTScore Project README](https://github.com/Tiiiger/bert_score#readme)
- [BERTScore ICLR 2020 Poster Presentation](https://iclr.cc/virtual_2020/poster_SkeHuCVFDr.html)
