# Metric Card for Perplexity

## Metric Description
Given a model and an input text sequence, perplexity measures how likely the model is to generate the input text sequence. 

## Intended Uses
Any language generation task.

## How to Use

### Inputs
- **model_id** (str): model used for calculating Perplexity. NOTE: Perplexity can only be calculated for causal language models.
    - This includes models such as gpt2, causal variations of bert, causal versions of t5, and more (the full list can be found in the AutoModelForCausalLM documentation here: https://huggingface.co/docs/transformers/master/en/model_doc/auto#transformers.AutoModelForCausalLM )
- **input_texts** (list of str): input text, each separate text snippet is one list entry. Perplexity returned will be an average of the perplexity for each list entry.
- **stride** (int): stride size, defaults to 512
- **device** (str): device to run on, defaults to 'cuda' when available

### Output Values
This metric outputs a dictionary with one value: the average perplexity score for the text input in the list.

```
{'perplexity': 117.9}
```

This metric's range is 0 and up. A lower score is better.

#### Values from Popular Papers


### Examples
Calculating perplexity on input_texts defined here:
```python
perplexity = datasets.load_metric("perplexity")
input_texts = ["lorem ipsum", "Happy Birthday!", "Bienvenue"]
results = perplexity.compute(model_id='gpt2',
                              input_texts=input_texts,
                              stride=1)
round(results["perplexity"], 1)
>>> 78.2
```
Calculating perplexity on input_texts loaded in from a dataset:
```python
perplexity = datasets.load_metric("perplexity")
input_texts = datasets.load_dataset("wikitext",
                                     "wikitext-2-raw-v1",
                                     split="test")["text"][:10]

results = perplexity.compute(model_id='gpt2',
                              input_texts=input_texts,
                              stride=256)
round(results["perplexity"], 1)
>>> 117.9
```

## Limitations and Bias
Note that the output value is based heavily on what text the model was trained on. This means that perplexity scores are not comparable between models or datasets. 


## Citation

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

## Further References
- [Hugging Face Perplexity Blog Post](https://huggingface.co/docs/transformers/perplexity)
