# Metric Card for *Current Metric*

## Metric Description

## Intended Uses
*What type of task can this metric be used for? What dataset(s)?*

## How to Use

### Inputs
- **input 1** *(type): definition of input 1, with explanation, if necessary.*
- **input 2** *(type): definition of input 2, with explanation, if necessary.*

### Output Values
*Explain what this metric outputs*

```
# Give an example of what the metric output looks like (e.g. the perplexity example below)
{'perplexity': 117.9}
```

*State the possible values that the metric's output can take, as well as what is considered a good score.*

#### Values from Popular Papers
*Give examples, preferrably with links, to papers that have reported this metric, along with the values they have reported.*

### Examples
*Give examples of the metric being used. Try to include examples that clear up any potential ambiguity *

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