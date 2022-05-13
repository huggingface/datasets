# Metric Card for CTC_Consistency


## Metric Description

We adopt the prevailing definition of consistency (Cao et al., 2018; Kryscinski et al., 2019), which dictates that the summary y should only contain information from x (instead of other sources or hallucinations). The aspect is also referred to as “factual correctness” or “faithfulness” in previous work2. For y to be fully consistent, all tokens in y should align with x. Therefore, we can straightforwardly devise the consistency metric based on the information alignment defined above:
    CONSISTENCY(y, x) = mean (align(y → x)), which is the average alignment scores of tokens in y w.r.t. x. 
Our metric offers a simpler solution than the recent QA-based metrics (Scialom et al., 2019; Durmus et al., 2020; Wang et al., 2020) that compare the answers extracted from y and x by a Question-Answering system, and is more interpretable than the black-box consistency classification models (Falke et al., 2019; Krys ́cin ́ski et al., 2019; Maynez et al., 2020).


## Installation
The most easy way to try our new framework is by Colab [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/12Dm5uzaVLmGWS273RXElawiW7GxuWvLs?usp=sharing)

If you want to install it on your machine, just follow these steps:

* Python version >= 3.6

Install with pip from PYPI by
```
pip install ctc_score
```

Or install with pip from the repository by
```
git clone https://github.com/tanyuqian/ctc-gen-eval.git
cd ctc-gen-eval/
pip install -e .
```
please also download
```
import nltk
nltk.download('stopwords')
```


## How to Use

At minimum, this metric requires sources and hypothesis as inputs.

```python
>>> ctc_consistency = datasets.load_metric("CTC_Consistency")
>>> results = ctc_consistency.compute(sources=sources, hypothesis=hypothesis)
>>> print(results["scores"])
{'accuracy': 1.0}
```


### Inputs
- **sources** (`list` of `string`): Predicted labels.
- **hypothesis** (`list` of `string`): Ground truth labels.


### Output Values
- **scores**(`float` or `int`): Accuracy score. Minimum possible value is 0. Maximum possible value is 1.0, or the number of examples input, if `normalize` is set to `True`.. A higher score means higher accuracy.

Output Example(s):
```python
{'scores': 0.9349850675401589}
```


## Citation(s)
```bibtex
@article{deng2021compression,
  title={Compression, Transduction, and Creation: A Unified Framework for Evaluating Natural Language Generation},
  author={Deng, Mingkai and Tan, Bowen and Liu, Zhengzhong and Xing, Eric P and Hu, Zhiting},
  journal={arXiv preprint arXiv:2109.06379},
  year={2021}
}
```
