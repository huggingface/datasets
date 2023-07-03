# Metric Card for KLUE-MRC

Please note that as KLUE-MRC has the same task format as SQuAD 2.0, this evaluation script follows almost the same format as the official evaluation script for SQuAD 2.0.

## Metric description

This metric wrap the unofficial scoring script for [Machine Machine Reading Comprehension task of
Korean Language Understanding Evaluation (KLUE-MRC)](https://huggingface.co/datasets/klue/viewer/mrc/train).

KLUE-MRC is a Korean reading comprehension dataset consisting of questions where the answer to every question is a segment of text, or span, from the corresponding reading passage, or the question might be unanswerable.

As KLUE-MRC has the same task format as SQuAD 2.0, this evaluation script uses the same metrics of SQuAD 2.0 (F1 and EM).

KLUE-MRC consists of 12,286 question paraphrasing, 7,931 multi-sentence reasoning, and 9,269 unanswerable questions. Totally, 29,313 examples are made with 22,343 documents and 23,717 passages.

## How to use 

The metric takes two files or two lists - one representing model predictions and the other the references to compare them to. 

*Predictions* : List of triple for question-answers to score with the following key-value pairs:
* `'id'`:  the question-answer identification field of the question and answer pair 
* `'prediction_text'` : the text of the answer
* `'no_answer_probability'` : the probability that the question has no answer

*References*: List of question-answers dictionaries with the following key-value pairs:
* `'id'`: id of the question-answer pair (see above),
* `'answers'`: a list of Dict {'text': text of the answer as a string}
*  `'unanswerable'`: the boolean value indicating whether the question is answerable or not.

```python
from datasets import load_metric
klue_mrc_metric = load_metric("klue_mrc")
results = klue_mrc_metric.compute(predictions=predictions, references=references)
```

## Output values

This metric outputs a dictionary with 13 values: 
* `'exact'`: Exact match (the normalized answer exactly match the gold answer) (see the `exact_match` metric (forthcoming))
* `'f1'`: The average F1-score of predicted tokens versus the gold answer (see the [F1 score](https://huggingface.co/metrics/f1) metric)
* `'total'`: Number of scores considered
* `'HasAns_exact'`: Exact match (the normalized answer exactly match the gold answer)
* `'HasAns_f1'`:  The F-score of predicted tokens versus the gold answer
* `'HasAns_total'`: How many of the questions have answers
* `'NoAns_exact'`: Exact match (the normalized answer exactly match the gold answer)
* `'NoAns_f1'`: The F-score of predicted tokens versus the gold answer
* `'NoAns_total'`: How many of the questions have no answers
* `'best_exact'` : Best exact match (with varying threshold)
* `'best_exact_thresh'`: No-answer probability threshold associated to the best exact match
* `'best_f1'`: Best F1 score (with varying threshold)
* `'best_f1_thresh'`: No-answer probability threshold associated to the best F1


The range of `exact_match` is 0-100, where 0.0 means no answers were matched and 100.0 means all answers were matched. 

The range of `f1` is 0-1 -- its lowest possible value is 0, if either the precision or the recall is 0, and its highest possible value is 1.0, which means perfect precision and recall.

The range of `total` depends on the length of predictions/references: its minimal value is 0, and maximal value is the total number of questions in the predictions and references.

## Example 

```python
from datasets import load_metric
klue_mrc_metric = load_metric("klue_mrc")
predictions = [{'prediction_text': '2020', 'id': 'klue-mrc-v1_train_12311', 'no_answer_probability': 0.}]
references = [{'answers': {'answer_start': [ 38 ], 'text': [ '2020' ]}, 'id': 'klue-mrc-v1_train_12311'}]
results = klue_mrc_metric.compute(predictions=predictions, references=references)
results
{'exact': 100.0, 'f1': 100.0, 'total': 1, 'HasAns_exact': 100.0, 'HasAns_f1': 100.0, 'HasAns_total': 1, 'best_exact': 100.0, 'best_exact_thresh': 0.0, 'best_f1': 100.0, 'best_f1_thresh': 0.0}
```

## Limitations
This metric works only with the datasets in the same format as the [KLUE-MRC](https://huggingface.co/datasets/klue/viewer/mrc/train). 


## Citation

```bibtex
@inproceedings{NEURIPS DATASETS AND BENCHMARKS2021_98dce83d,
 author = {Park, Sungjoon and Moon, Jihyung and Kim, Sungdong and Cho, Won Ik and Han, Ji Yoon and Park, Jangwon and Song, Chisung and Kim, Junseong and Song, Youngsook and Oh, Taehwan and Lee, Joohong and Oh, Juhyun and Lyu, Sungwon and Jeong, Younghoon and Lee, Inkwon and Seo, Sangwoo and Lee, Dongjun and Kim, Hyunwoo and Lee, Myeonghwa and Jang, Seongbo and Do, Seungwon and Kim, Sunkyoung and Lim, Kyungtae and Lee, Jongwon and Park, Kyumin and Shin, Jamin and Kim, Seonghyun and Park, Lucy and Park, Lucy and Oh, Alice and Ha (NAVER AI Lab), Jung-Woo and Cho, Kyunghyun and Cho, Kyunghyun},
 booktitle = {Proceedings of the Neural Information Processing Systems Track on Datasets and Benchmarks},
 editor = {J. Vanschoren and S. Yeung},
 pages = {},
 publisher = {Curran},
 title = {KLUE: Korean Language Understanding Evaluation},
 url = {https://datasets-benchmarks-proceedings.neurips.cc/paper_files/paper/2021/file/98dce83da57b0395e163467c9dae521b-Paper-round2.pdf},
 volume = {1},
 year = {2021}
}
```
    
## Further References 

- [LM Eval Harness](https://github.com/EleutherAI/lm-evaluation-harness) leverages this scoring script for the evaluation of [KLUE-MRC](https://huggingface.co/datasets/klue/viewer/mrc/train).
- [The Stanford Question Answering Dataset: Background, Challenges, Progress (blog post)](https://rajpurkar.github.io/mlx/qa-and-squad/)
- [Hugging Face Course -- Question Answering](https://huggingface.co/course/chapter7/7)