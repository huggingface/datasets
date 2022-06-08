# Metric Card for Perplexity

## Metric Description
Given a model and an input text sequence, perplexity measures how likely the model is to generate the input text sequence. This can be used in two main ways:
1. to evaluate how well the model has learned the distribution of the text it was trained on
    - In this case, the model input should be the trained model to be evaluated, and the input texts should be the text that the model was trained on.
2. to evaluate how well a selection of text matches the distribution of text that the input model was trained on
    - In this case, the model input should be a trained model, and the input texts should be the text to be evaluated.

## Intended Uses
Any language generation task.

## How to Use

The metric takes a list of text as input, as well as the name of the model used to compute the metric:

```python
from datasets import load_metric
perplexity = load_metric("perplexity")
results = perplexity.compute(input_texts=input_texts, model_id='gpt2')
```

### Inputs
- **model_id** (str): model used for calculating Perplexity. NOTE: Perplexity can only be calculated for causal language models.
    - This includes models such as gpt2, causal variations of bert, causal versions of t5, and more (the full list can be found in the AutoModelForCausalLM documentation here: https://huggingface.co/docs/transformers/master/en/model_doc/auto#transformers.AutoModelForCausalLM )
- **input_texts** (list of str): input text, each separate text snippet is one list entry.
- **batch_size** (int): the batch size to run texts through the model. Defaults to 16.
- **add_start_token** (bool): whether to add the start token to the texts, so the perplexity can include the probability of the first word. Defaults to True.
- **device** (str): device to run on, defaults to 'cuda' when available

### Output Values
This metric outputs a dictionary with the perplexity scores for the text input in the list, and the average perplexity.
If one of the input texts is longer than the max input length of the model, then it is truncated to the max length for the perplexity computation.

```
{'perplexities': [8.182524681091309, 33.42122268676758, 27.012239456176758], 'mean_perplexity': 22.871995608011883}
```

This metric's range is 0 and up. A lower score is better.

#### Values from Popular Papers


### Examples
Calculating perplexity on input_texts defined here:
```python
perplexity = datasets.load_metric("perplexity")
input_texts = ["lorem ipsum", "Happy Birthday!", "Bienvenue"]
results = perplexity.compute(model_id='gpt2',
                             add_start_token=False,
                             input_texts=input_texts)
print(list(results.keys()))
>>>['perplexities', 'mean_perplexity']
print(round(results["mean_perplexity"], 2))
>>>78.22
print(round(results["perplexities"][0], 2))
>>>11.11
```
Calculating perplexity on input_texts loaded in from a dataset:
```python
perplexity = datasets.load_metric("perplexity")
input_texts = datasets.load_dataset("wikitext",
                                    "wikitext-2-raw-v1",
                                    split="test")["text"][:50]
input_texts = [s for s in input_texts if s!='']
results = perplexity.compute(model_id='gpt2',
                             input_texts=input_texts)
print(list(results.keys()))
>>>['perplexities', 'mean_perplexity']
print(round(results["mean_perplexity"], 2))
>>>60.35
print(round(results["perplexities"][0], 2))
>>>81.12
```

## Limitations and Bias
Note that the output value is based heavily on what text the model was trained on. This means that perplexity scores are not comparable between models or datasets.


## Citation

```bibtex
@article{jelinek1977perplexity,
title={Perplexity—a measure of the difficulty of speech recognition tasks},
author={Jelinek, Fred and Mercer, Robert L and Bahl, Lalit R and Baker, James K},
journal={The Journal of the Acoustical Society of America},
volume={62},
number={S1},
pages={S63--S63},
year={1977},
publisher={Acoustical Society of America}
}
```

## Further References
- [Hugging Face Perplexity Blog Post](https://huggingface.co/docs/transformers/perplexity)
