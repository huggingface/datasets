## Metric description
This metric wraps the official scoring script for version 1 of the [Stanford Question Answering Dataset (SQuAD)](https://huggingface.co/datasets/squad). 

SQuAD is a reading comprehension dataset, consisting of questions posed by crowdworkers on a set of Wikipedia articles, where the answer to every question is a segment of text, or span, from the corresponding reading passage, or the question might be unanswerable.


## Intended uses & limitations
This metric works only with the [SQuAD v.1 dataset](https://huggingface.co/datasets/squad) -- it will not work with any other dataset formats.

## How to use 

The metric takes two files or two lists of question-answers dictionaries as inputs : one with the predictions of the model and the other with the references to be compared to:

    from datasets import load_metric
    squad_metric = load_metric("squad")
    results = squad_metric.compute(predictions=predictions, references=references)
  
It outputs a dictionary with two values: the average exact match score and the average [F1 score](https://huggingface.co/metrics/f1).

    {'exact_match': 100.0, 'f1': 100.0}

## Range
The range of `exact_match` is 0-100, where 0.0 means no answers were matched and 100.0 means all answers were matched. 

The range of `f1` is 0-1 -- its lowest possible value is 0, if either the precision or the recall is 0, and its highest possible value is 1.0, which means perfect precision and recall.

## Values from popular papers
The [original SQuAD paper](https://nlp.stanford.edu/pubs/rajpurkar2016squad.pdf) reported an F1 score of 51.0% and an Exact Match score of 40.0%. They also report that human performance on the dataset represents an F1 score of 90.5% and an Exact Match score of 80.3%.

For more recent model performance, see the [dataset leaderboard](https://paperswithcode.com/dataset/squad).


## Limitations and bias
The SQuAD dataset does contain a certain amount of noise, such as duplicate questions as well as missing answers, but these represent a minority of the 100,000 question-answer pairs. Also, neither exact match nor F1 score reflect whether models do better on certain types of questions (e.g. who questions) or those that cover a certain gender or geographical area -- carrying out more in-depth error analysis can complement these numbers. 


## Citation

    @inproceedings{Rajpurkar2016SQuAD10,
    title={SQuAD: 100, 000+ Questions for Machine Comprehension of Text},
    author={Pranav Rajpurkar and Jian Zhang and Konstantin Lopyrev and Percy Liang},
    booktitle={EMNLP},
    year={2016}
    }
