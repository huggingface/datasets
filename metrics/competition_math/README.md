# Metric Card for Competition MATH

## Metric description

This metric is used to assess performance on the [Mathematics Aptitude Test of Heuristics (MATH) dataset](https://huggingface.co/datasets/competition_math). 

It first canonicalizes the inputs (e.g., converting `1/2` to `\\frac{1}{2}`) and then computes accuracy.

## How to use 

This metric takes two arguments:

`predictions`: a list of predictions to score. Each prediction is a string that contains natural language and LaTeX.

`references`: list of reference for each prediction. Each reference is a string that contains natural language and LaTeX.


```python
>>> from datasets import load_metric
>>> math = load_metric("competition_math")
>>> references = ["\\frac{1}{2}"]
>>> predictions = ["1/2"]
>>> results = math.compute(references=references, predictions=predictions)
```

N.B. To be able to use Competition MATH, you need to install the `math_equivalence` dependency using `pip install git+https://github.com/hendrycks/math.git`. 


## Output values

This metric returns a dictionary that contains the [accuracy](https://huggingface.co/metrics/accuracy) after canonicalizing inputs, on a scale between 0.0 and 1.0.

### Values from popular papers
The [original MATH dataset paper](https://arxiv.org/abs/2103.03874) reported accuracies ranging from 3.0% to 6.9% by different large language models. 

More recent progress on the dataset can be found on the [dataset leaderboard](https://paperswithcode.com/sota/math-word-problem-solving-on-math).

## Examples 

Maximal values (full match):

```python
>>> from datasets import load_metric
>>> math = load_metric("competition_math")
>>> references = ["\\frac{1}{2}"]
>>> predictions = ["1/2"]
>>> results = math.compute(references=references, predictions=predictions)
>>> print(results)
{'accuracy': 1.0}
```

Minimal values (no match):

```python
>>> from datasets import load_metric
>>> math = load_metric("competition_math")
>>> references = ["\\frac{1}{2}"]
>>> predictions = ["3/4"]
>>> results = math.compute(references=references, predictions=predictions)
>>> print(results)
{'accuracy': 0.0}
```

Partial match:

```python
>>> from datasets import load_metric
>>> math = load_metric("competition_math")
>>> references = ["\\frac{1}{2}","\\frac{3}{4}"]
>>> predictions = ["1/5", "3/4"]
>>> results = math.compute(references=references, predictions=predictions)
>>> print(results)
{'accuracy': 0.5}
```

## Limitations and bias

This metric is limited to datasets with the same format as the [Mathematics Aptitude Test of Heuristics (MATH) dataset](https://huggingface.co/datasets/competition_math), and is meant to evaluate the performance of large language models at solving mathematical problems.

N.B. The MATH dataset also assigns levels of difficulty to different problems, so disagregating model performance by difficulty level (similarly to what was done in the [original paper](https://arxiv.org/abs/2103.03874) can give a better indication of how a given model does on a given difficulty of math problem, compared to overall accuracy. 

## Citation

```bibtex
@article{hendrycksmath2021,
  title={Measuring Mathematical Problem Solving With the MATH Dataset},
  author={Dan Hendrycks
    and Collin Burns
    and Saurav Kadavath
    and Akul Arora
    and Steven Basart
    and Eric Tang
    and Dawn Song
    and Jacob Steinhardt},
  journal={arXiv preprint arXiv:2103.03874},
  year={2021}
}
```
    
## Further References 
- [MATH dataset](https://huggingface.co/datasets/competition_math)
- [MATH leaderboard](https://paperswithcode.com/sota/math-word-problem-solving-on-math)
- [MATH paper](https://arxiv.org/abs/2103.03874)
