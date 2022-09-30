# Metric Card for COVAL

## Metric description

CoVal is a coreference evaluation tool for the [CoNLL](https://huggingface.co/datasets/conll2003) and [ARRAU](https://catalog.ldc.upenn.edu/LDC2013T22) datasets which implements of the common evaluation metrics including MUC [Vilain et al, 1995](https://aclanthology.org/M95-1005.pdf), B-cubed [Bagga and Baldwin, 1998](https://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.34.2578&rep=rep1&type=pdf), CEAFe [Luo et al., 2005](https://aclanthology.org/H05-1004.pdf), LEA [Moosavi and Strube, 2016](https://aclanthology.org/P16-1060.pdf) and the averaged CoNLL score (the average of the F1 values of MUC, B-cubed and CEAFe). 

CoVal code was written by [`@ns-moosavi`](https://github.com/ns-moosavi), with some parts borrowed from [Deep Coref](https://github.com/clarkkev/deep-coref/blob/master/evaluation.py). The test suite is taken from the [official CoNLL code](https://github.com/conll/reference-coreference-scorers/), with additions by [`@andreasvc`](https://github.com/andreasvc) and file parsing developed by Leo Born.

## How to use 

The metric takes two lists of sentences as input: one representing `predictions` and `references`, with the sentences consisting of words in the CoNLL format (see the [Limitations and bias](#Limitations-and-bias) section below for more details on the CoNLL format). 

```python
from datasets import load_metric
coval = load_metric('coval')
words = ['bc/cctv/00/cctv_0005   0   0       Thank   VBP  (TOP(S(VP*    thank  01   1    Xu_li  *           (V*)        *       -',
... 'bc/cctv/00/cctv_0005   0   1         you   PRP        (NP*)      -    -   -    Xu_li  *        (ARG1*)   (ARG0*)   (116)',
... 'bc/cctv/00/cctv_0005   0   2    everyone    NN        (NP*)      -    -   -    Xu_li  *    (ARGM-DIS*)        *    (116)',
... 'bc/cctv/00/cctv_0005   0   3         for    IN        (PP*       -    -   -    Xu_li  *        (ARG2*         *       -',
... 'bc/cctv/00/cctv_0005   0   4    watching   VBG   (S(VP*))))   watch  01   1    Xu_li  *             *)      (V*)      -',
... 'bc/cctv/00/cctv_0005   0   5           .     .          *))      -    -   -    Xu_li  *             *         *       -']
references = [words]
predictions = [words]
results = coval.compute(predictions=predictions, references=references)
```
It also has several optional arguments:

`keep_singletons`: After extracting all mentions of key or system file mentions whose corresponding coreference chain is of size one are considered as singletons. The default evaluation mode will include singletons in evaluations if they are included in the key or the system files. By setting `keep_singletons=False`, all singletons in the key and system files will be excluded from the evaluation.

`NP_only`: Most of the recent coreference resolvers only resolve NP mentions and leave out the resolution of VPs. By setting the `NP_only` option, the scorer will only evaluate the resolution of NPs.

`min_span`: By setting `min_span`, the scorer reports the results based on automatically detected minimum spans. Minimum spans are determined using the [MINA algorithm](https://arxiv.org/pdf/1906.06703.pdf).
        

## Output values

The metric outputs a dictionary with the following key-value pairs:

`mentions`: number of mentions, ranges from 0-1

`muc`: MUC metric, which expresses performance in terms of recall and precision, ranging from 0-1.

`bcub`: B-cubed metric, which is the averaged precision of all items in the distribution, ranging from 0-1.

`ceafe`: CEAFe (Constrained Entity Alignment F-Measure) is computed by aligning reference and system entities with the constraint that a reference entity is aligned with at most one reference entity. It ranges from 0-1

`lea`: LEA is a Link-Based Entity-Aware metric which, for each entity, considers how important the entity is and how well it is resolved. It ranges from 0-1.

`conll_score`: averaged CoNLL score (the average of the F1 values of `muc`, `bcub` and `ceafe`), ranging from 0 to 100. 
   

### Values from popular papers

Given that many of the metrics returned by COVAL come from different sources, is it hard to cite reference values for all of them.

The CoNLL score is used to track progress on different datasets such as the [ARRAU corpus](https://paperswithcode.com/sota/coreference-resolution-on-the-arrau-corpus) and [CoNLL 2012](https://paperswithcode.com/sota/coreference-resolution-on-conll-2012).

## Examples 

Maximal values

```python
from datasets import load_metric
coval = load_metric('coval')
words = ['bc/cctv/00/cctv_0005   0   0       Thank   VBP  (TOP(S(VP*    thank  01   1    Xu_li  *           (V*)        *       -',
... 'bc/cctv/00/cctv_0005   0   1         you   PRP        (NP*)      -    -   -    Xu_li  *        (ARG1*)   (ARG0*)   (116)',
... 'bc/cctv/00/cctv_0005   0   2    everyone    NN        (NP*)      -    -   -    Xu_li  *    (ARGM-DIS*)        *    (116)',
... 'bc/cctv/00/cctv_0005   0   3         for    IN        (PP*       -    -   -    Xu_li  *        (ARG2*         *       -',
... 'bc/cctv/00/cctv_0005   0   4    watching   VBG   (S(VP*))))   watch  01   1    Xu_li  *             *)      (V*)      -',
... 'bc/cctv/00/cctv_0005   0   5           .     .          *))      -    -   -    Xu_li  *             *         *       -']
references = [words]
predictions = [words]
results = coval.compute(predictions=predictions, references=references)
print(results)
{'mentions/recall': 1.0, 'mentions/precision': 1.0, 'mentions/f1': 1.0, 'muc/recall': 1.0, 'muc/precision': 1.0, 'muc/f1': 1.0, 'bcub/recall': 1.0, 'bcub/precision': 1.0, 'bcub/f1': 1.0, 'ceafe/recall': 1.0, 'ceafe/precision': 1.0, 'ceafe/f1': 1.0, 'lea/recall': 1.0, 'lea/precision': 1.0, 'lea/f1': 1.0, 'conll_score': 100.0}
```

## Limitations and bias

This wrapper of CoVal currently only works with [CoNLL line format](https://huggingface.co/datasets/conll2003), which has one word per line with all the annotation for this word in column separated by spaces:

| Column | Type                  | Description                                                                                                                                                                                                                                                                                             |
|:-------|:----------------------|:--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 1      | Document ID           | This is a variation on the document filename                                                                                                                                                                                                                                                            |
| 2      | Part number           | Some files are divided into multiple parts numbered as 000, 001, 002, ... etc.                                                                                                                                                                                                                          |
| 3      | Word number           |                                                                                                                                                                                                                                                                                                         |
| 4      | Word                  | This is the token as segmented/tokenized in the Treebank. Initially the *_skel file contain the placeholder [WORD] which gets replaced by the actual token from the Treebank which is part of the OntoNotes release.                                                                                    |
| 5      | Part-of-Speech        |                                                                                                                                                                                                                                                                                                         |
| 6      | Parse bit             | This is the bracketed structure broken before the first open parenthesis in the parse, and the word/part-of-speech leaf replaced with a *. The full parse can be created by substituting the asterix with the "([pos] [word])" string (or leaf) and concatenating the items in the rows of that column. |
| 7      | Predicate lemma       | The predicate lemma is mentioned for the rows for which we have semantic role information. All other rows are marked with a "-".                                                                                                                                                                        |
| 8      | Predicate Frameset ID | This is the PropBank frameset ID of the predicate in Column 7.                                                                                                                                                                                                                                          |                                                                                                                                                                                                                                          
| 9      | Word sense            | This is the word sense of the word in Column 3.                                                                                                                                                                                                                                                         |                                                                                                                                                                                                                                                        
| 10     | Speaker/Author        | This is the speaker or author name where available. Mostly in Broadcast Conversation and Web Log data.                                                                                                                                                                                                  |                                                                                                                                                                                                 
| 11     | Named Entities        | These columns identifies the spans representing various named entities.                                                                                                                                                                                                                                 |                                                                                                                                                                                                                                
| 12:N   | Predicate Arguments   | There is one column each of predicate argument structure information for the predicate mentioned in Column 7.                                                                                                                                                                                           |
| N      | Coreference           | Coreference chain information encoded in a parenthesis structure.                                                                                                                                                                                                                                       |                                                                                                                                                                                                                                     

## Citations

```bibtex
@InProceedings{moosavi2019minimum,
  author = { Nafise Sadat Moosavi, Leo Born, Massimo Poesio and Michael Strube},
  title = {Using Automatically Extracted Minimum Spans to Disentangle Coreference Evaluation from Boundary Detection},
  year = {2019},
  booktitle = {Proceedings of the 57th Annual Meeting of
      the Association for Computational Linguistics (Volume 1: Long Papers)},
  publisher = {Association for Computational Linguistics},
  address = {Florence, Italy},
}
```
```bibtex
@inproceedings{10.3115/1072399.1072405,
  author = {Vilain, Marc and Burger, John and Aberdeen, John and Connolly, Dennis and Hirschman, Lynette},
  title = {A Model-Theoretic Coreference Scoring Scheme},
  year = {1995},
  isbn = {1558604022},
  publisher = {Association for Computational Linguistics},
  address = {USA},
  url = {https://doi.org/10.3115/1072399.1072405},
  doi = {10.3115/1072399.1072405},
  booktitle = {Proceedings of the 6th Conference on Message Understanding},
  pages = {45–52},
  numpages = {8},
  location = {Columbia, Maryland},
  series = {MUC6 ’95}
}
```

```bibtex
@INPROCEEDINGS{Bagga98algorithmsfor,
    author = {Amit Bagga and Breck Baldwin},
    title = {Algorithms for Scoring Coreference Chains},
    booktitle = {In The First International Conference on Language Resources and Evaluation Workshop on Linguistics Coreference},
    year = {1998},
    pages = {563--566}
}
```
```bibtex
@INPROCEEDINGS{Luo05oncoreference,
    author = {Xiaoqiang Luo},
    title = {On coreference resolution performance metrics},
    booktitle = {In Proc. of HLT/EMNLP},
    year = {2005},
    pages = {25--32},
    publisher = {URL}
}
```

```bibtex
@inproceedings{moosavi-strube-2016-coreference,
    title = "Which Coreference Evaluation Metric Do You Trust? A Proposal for a Link-based Entity Aware Metric",
    author = "Moosavi, Nafise Sadat  and
      Strube, Michael",
    booktitle = "Proceedings of the 54th Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers)",
    month = aug,
    year = "2016",
    address = "Berlin, Germany",
    publisher = "Association for Computational Linguistics",
    url = "https://www.aclweb.org/anthology/P16-1060",
    doi = "10.18653/v1/P16-1060",
    pages = "632--642",
}
```
    
## Further References 

- [CoNLL 2012 Task Description](http://www.conll.cemantix.org/2012/data.html): for information on the format (section "*_conll File Format")
- [CoNLL Evaluation details](https://github.com/ns-moosavi/coval/blob/master/conll/README.md)
- [Hugging Face - Neural Coreference Resolution (Neuralcoref)](https://huggingface.co/coref/)

