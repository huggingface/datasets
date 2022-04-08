# Metric Card for FrugalScore


## Metric Description
FrugalScore is a reference-based metric for Natural Language Generation (NLG) model evaluation. It is based on a distillation approach that allows to learn a fixed, low cost version of any expensive NLG metric, while retaining most of its original performance.

The FrugalScore models are obtained by continuing the pretraining of small models on a synthetic dataset constructed using summarization, backtranslation and denoising models. During the training, the small models learn the internal mapping of the expensive metric, including any similarity function.

## How to use 

When loading FrugalScore, you can indicate the model you wish to use to compute the score. The default model is `moussaKam/frugalscore_tiny_bert-base_bert-score`, and a full list of models can be found in the [Limitations and bias](#Limitations-and-bias) section.

```python
>>> from datasets import load_metric
>>> frugalscore = load_metric("frugalscore", "moussaKam/frugalscore_medium_bert-base_mover-score")
```

FrugalScore calculates how good are the predictions given some references, based on a set of scores.

The inputs it takes are:

`predictions`: a list of strings representing the predictions to score. 

`references`: a list of string representing the references for each prediction. 

Its optional arguments are:

`batch_size`: the batch size for predictions (default value is `32`).

`max_length`: the maximum sequence length (default value is `128`).

`device`: either "gpu" or "cpu" (default value is `None`). 

```python
>>> results = frugalscore.compute(predictions=['hello there', 'huggingface'], references=['hello world', 'hugging face'], batch_size=16, max_length=64, device="gpu")
```

## Output values

The output of FrugalScore is a dictionary with the list of scores for each prediction-reference pair:
```python
{'scores': [0.6307541, 0.6449357]}
```

### Values from popular papers
The [original FrugalScore paper](https://arxiv.org/abs/2110.08559) reported that FrugalScore-Tiny retains 97.7/94.7% of the original performance compared to [BertScore](https://huggingface.co/metrics/bertscore) while running 54 times faster and having 84 times less parameters.

## Examples 

Maximal values (exact match between `references` and `predictions`): 

```python
>>> from datasets import load_metric
>>> frugalscore = load_metric("frugalscore")
>>> results = frugalscore.compute(predictions=['hello world'], references=['hello world'])
>>> print(results)
{'scores': [0.9891098]}
```

Partial values: 

```python
>>> from datasets import load_metric
>>> frugalscore = load_metric("frugalscore")
>>> results = frugalscore.compute(predictions=['hello world'], references=['hugging face'])
>>> print(results)
{'scores': [0.42482382]}
```

## Limitations and bias

FrugalScore is based on [BertScore](https://huggingface.co/metrics/bertscore) and [MoverScore](https://arxiv.org/abs/1909.02622), and the models used are based on the original models used for these scores.

The full list of available models for FrugalScore is:

| FrugalScore                                        | Student     | Teacher        | Method     |
|----------------------------------------------------|-------------|----------------|------------|
| [moussaKam/frugalscore_tiny_bert-base_bert-score](https://huggingface.co/moussaKam/frugalscore_tiny_bert-base_bert-score)    | BERT-tiny   | BERT-Base      | BERTScore  |
| [moussaKam/frugalscore_small_bert-base_bert-score](https://huggingface.co/moussaKam/frugalscore_small_bert-base_bert-score)   | BERT-small  | BERT-Base      | BERTScore  |
| [moussaKam/frugalscore_medium_bert-base_bert-score](https://huggingface.co/moussaKam/frugalscore_medium_bert-base_bert-score) | BERT-medium | BERT-Base      | BERTScore  |
| [moussaKam/frugalscore_tiny_roberta_bert-score](https://huggingface.co/moussaKam/frugalscore_tiny_roberta_bert-score)     | BERT-tiny   | RoBERTa-Large  | BERTScore  |
| [moussaKam/frugalscore_small_roberta_bert-score](https://huggingface.co/moussaKam/frugalscore_small_roberta_bert-score)     | BERT-small  | RoBERTa-Large  | BERTScore  |
| [moussaKam/frugalscore_medium_roberta_bert-score](https://huggingface.co/moussaKam/frugalscore_medium_roberta_bert-score)    | BERT-medium | RoBERTa-Large  | BERTScore  |
| [moussaKam/frugalscore_tiny_deberta_bert-score](https://huggingface.co/moussaKam/frugalscore_tiny_deberta_bert-score)      | BERT-tiny   | DeBERTa-XLarge | BERTScore  |
| [moussaKam/frugalscore_small_deberta_bert-score](https://huggingface.co/moussaKam/frugalscore_small_deberta_bert-score)     | BERT-small  | DeBERTa-XLarge | BERTScore  |
| [moussaKam/frugalscore_medium_deberta_bert-score](https://huggingface.co/moussaKam/frugalscore_medium_deberta_bert-score)    | BERT-medium | DeBERTa-XLarge | BERTScore  |
| [moussaKam/frugalscore_tiny_bert-base_mover-score](https://huggingface.co/moussaKam/frugalscore_tiny_bert-base_mover-score)   | BERT-tiny   | BERT-Base      | MoverScore |
| [moussaKam/frugalscore_small_bert-base_mover-score](https://huggingface.co/moussaKam/frugalscore_small_bert-base_mover-score)  | BERT-small  | BERT-Base      | MoverScore |
| [moussaKam/frugalscore_medium_bert-base_mover-score](https://huggingface.co/moussaKam/frugalscore_medium_bert-base_mover-score) | BERT-medium | BERT-Base      | MoverScore |

Depending on the size of the model picked, the loading time will vary: the `tiny` models will load very quickly, whereas the `medium` ones can take several minutes, depending on your Internet connection. 

## Citation
```bibtex
@article{eddine2021frugalscore,
  title={FrugalScore: Learning Cheaper, Lighter and Faster Evaluation Metrics for Automatic Text Generation},
  author={Eddine, Moussa Kamal and Shang, Guokan and Tixier, Antoine J-P and Vazirgiannis, Michalis},
  journal={arXiv preprint arXiv:2110.08559},
  year={2021}
}
```

## Further References
- [Original FrugalScore code](https://github.com/moussaKam/FrugalScore)
- [FrugalScore paper](https://arxiv.org/abs/2110.08559) 
