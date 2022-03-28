# Metric Card for Code Eval

## Metric description

The CodeEval metric estimates the pass@k metric for code synthesis. 

It implements the evaluation harness for the HumanEval problem solving dataset described in the paper ["Evaluating Large Language Models Trained on Code"](https://arxiv.org/abs/2107.03374).


## How to use 

The Code Eval metric calculates how good are predictions given a set of references. Its arguments are:

`predictions`: a list of candidates to evaluate. Each candidate should be a list of strings with several code candidates to solve the problem.

`references`: a list with a test for each prediction. Each test should evaluate the correctness of a code candidate.

`k`: number of code candidates to consider in the evaluation. The default value is `[1, 10, 100]`.

`num_workers`: the number of workers used to evaluate the candidate programs (The default value is `4`).

`timeout`: The maximum time taken to produce a prediction before it is considered a "timeout". The default value is `3.0` (i.e. 3 seconds).

```python
from datasets import load_metric
code_eval = load_metric("code_eval")
test_cases = ["assert add(2,3)==5"]
candidates = [["def add(a,b): return a*b", "def add(a, b): return a+b"]]
pass_at_k, results = code_eval.compute(references=test_cases, predictions=candidates, k=[1, 2])
```

N.B.
Before running this metric, you will need to run the following commands:
```python
import os
os.environ["HF_ALLOW_CODE_EVAL"] = "1"` 
```

## Output values

The Code Eval metric outputs two things:

`pass_at_k`: a dictionary with the pass rates for each k value defined in the arguments.

`results`: a dictionary with granular results of each unit test.

### Values from popular papers
The [original CODEX paper](https://arxiv.org/pdf/2107.03374.pdf) reported that the CODEX-12B model had a pass@k score of 28.8% at `k=1`, 46.8% at `k=10` and 72.3% at `k=100`. However, since the CODEX model is not open source, it is hard to verify these numbers. 



## Examples 

Full match at `k=1`:

```python
from datasets import load_metric
code_eval = load_metric("code_eval")
test_cases = ["assert add(2,3)==5"]
candidates = [["def add(a, b): return a+b"]]
pass_at_k, results = code_eval.compute(references=test_cases, predictions=candidates, k=[1])
print(pass_at_k)
{'pass@1': 1.0}
```

No match for k = 1:

```python
from datasets import load_metric
code_eval = load_metric("code_eval")
test_cases = ["assert add(2,3)==5"]
candidates = [["def add(a,b): return a*b"]]
pass_at_k, results = code_eval.compute(references=test_cases, predictions=candidates, k=[1])
print(pass_at_k)
{'pass@1': 0.0}
```

Partial match at k=1, full match at k=2:

```python
from datasets import load_metric
code_eval = load_metric("code_eval")
test_cases = ["assert add(2,3)==5"]
candidates = [["def add(a, b): return a+b", "def add(a,b): return a*b"]]
pass_at_k, results = code_eval.compute(references=test_cases, predictions=candidates, k=[1, 2])
print(pass_at_k)
{'pass@1': 0.5, 'pass@2': 1.0}
```

## Limitations and bias

As per the warning included in the metric code itself:
"This program exists to run untrusted model-generated code. Users are strongly encouraged not to do so outside of a robust security sandbox. The execution call in execution.py is deliberately commented out to ensure users read this disclaimer before running code in a potentially unsafe manner. See the comment in execution.py for more information and instructions."

More information about the limitations of the code can be found on the [Human Eval Github repository](https://github.com/openai/human-eval).

## Citation

```bibtex
@misc{chen2021evaluating,
      title={Evaluating Large Language Models Trained on Code},
      author={Mark Chen and Jerry Tworek and Heewoo Jun and Qiming Yuan \
and Henrique Ponde de Oliveira Pinto and Jared Kaplan and Harri Edwards \
and Yuri Burda and Nicholas Joseph and Greg Brockman and Alex Ray \
and Raul Puri and Gretchen Krueger and Michael Petrov and Heidy Khlaaf \
and Girish Sastry and Pamela Mishkin and Brooke Chan and Scott Gray \
and Nick Ryder and Mikhail Pavlov and Alethea Power and Lukasz Kaiser \
and Mohammad Bavarian and Clemens Winter and Philippe Tillet \
and Felipe Petroski Such and Dave Cummings and Matthias Plappert \
and Fotios Chantzis and Elizabeth Barnes and Ariel Herbert-Voss \
and William Hebgen Guss and Alex Nichol and Alex Paino and Nikolas Tezak \
and Jie Tang and Igor Babuschkin and Suchir Balaji and Shantanu Jain \
and William Saunders and Christopher Hesse and Andrew N. Carr \
and Jan Leike and Josh Achiam and Vedant Misra and Evan Morikawa \
and Alec Radford and Matthew Knight and Miles Brundage and Mira Murati \
and Katie Mayer and Peter Welinder and Bob McGrew and Dario Amodei \
and Sam McCandlish and Ilya Sutskever and Wojciech Zaremba},
      year={2021},
      eprint={2107.03374},
      archivePrefix={arXiv},
      primaryClass={cs.LG}
}
```
    
## Further References 

- [Human Eval Github repository](https://github.com/openai/human-eval)
- [OpenAI Codex website](https://openai.com/blog/openai-codex/)
