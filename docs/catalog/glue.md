<div itemscope itemtype="http://schema.org/Dataset">
  <div itemscope itemprop="includedInDataCatalog" itemtype="http://schema.org/DataCatalog">
    <meta itemprop="name" content="TensorFlow Datasets" />
  </div>
  <meta itemprop="name" content="glue" />
  <meta itemprop="description" content="GLUE, the General Language Understanding Evaluation benchmark&#10;(https://gluebenchmark.com/) is a collection of resources for training,&#10;evaluating, and analyzing natural language understanding systems.&#10;&#10;&#10;&#10;To use this dataset:&#10;&#10;```python&#10;import tensorflow_datasets as tfds&#10;&#10;ds = tfds.load(&#x27;glue&#x27;, split=&#x27;train&#x27;)&#10;for ex in ds.take(4):&#10;  print(ex)&#10;```&#10;&#10;See [the guide](https://www.tensorflow.org/datasets/overview) for more&#10;informations on [tensorflow_datasets](https://www.tensorflow.org/datasets).&#10;&#10;" />
  <meta itemprop="url" content="https://www.tensorflow.org/datasets/catalog/glue" />
  <meta itemprop="sameAs" content="https://nyu-mll.github.io/CoLA/" />
  <meta itemprop="citation" content="@article{warstadt2018neural,&#10;  title={Neural Network Acceptability Judgments},&#10;  author={Warstadt, Alex and Singh, Amanpreet and Bowman, Samuel R},&#10;  journal={arXiv preprint arXiv:1805.12471},&#10;  year={2018}&#10;}&#10;@inproceedings{wang2019glue,&#10;  title={{GLUE}: A Multi-Task Benchmark and Analysis Platform for Natural Language Understanding},&#10;  author={Wang, Alex and Singh, Amanpreet and Michael, Julian and Hill, Felix and Levy, Omer and Bowman, Samuel R.},&#10;  note={In the Proceedings of ICLR.},&#10;  year={2019}&#10;}&#10;&#10;Note that each GLUE dataset has its own citation. Please see the source to see&#10;the correct citation for each contained dataset." />
</div>
# `glue`

*   **Description**:

GLUE, the General Language Understanding Evaluation benchmark
(https://gluebenchmark.com/) is a collection of resources for training,
evaluating, and analyzing natural language understanding systems.

*   **Source code**:
    [`tfds.text.glue.Glue`](https://github.com/tensorflow/datasets/tree/master/tensorflow_datasets/text/glue.py)
*   **Versions**:
    *   **`1.0.0`** (default): New split API
        (https://tensorflow.org/datasets/splits)
*   **Dataset size**: `Unknown size`
*   **Auto-cached**
    ([documentation](https://www.tensorflow.org/datasets/performances#auto-caching)):
    No
*   **Supervised keys** (See
    [`as_supervised` doc](https://www.tensorflow.org/datasets/api_docs/python/tfds/load#args)):
    `None`

## glue/cola (default config)

*   **Config description**: The Corpus of Linguistic Acceptability consists of
    English acceptability judgments drawn from books and journal articles on
    linguistic theory. Each example is a sequence of words annotated with
    whether it is a grammatical English sentence.
*   **Homepage**:
    [https://nyu-mll.github.io/CoLA/](https://nyu-mll.github.io/CoLA/)
*   **Download size**: `368.14 KiB`
*   **Splits**:

Split        | Examples
:----------- | -------:
'test'       | 1,063
'train'      | 8,551
'validation' | 1,043

*   **Features**:

```python
FeaturesDict({
    'idx': tf.int32,
    'label': ClassLabel(shape=(), dtype=tf.int64, num_classes=2),
    'sentence': Text(shape=(), dtype=tf.string),
})
```
*   **Citation**:

```
@article{warstadt2018neural,
  title={Neural Network Acceptability Judgments},
  author={Warstadt, Alex and Singh, Amanpreet and Bowman, Samuel R},
  journal={arXiv preprint arXiv:1805.12471},
  year={2018}
}
@inproceedings{wang2019glue,
  title={{GLUE}: A Multi-Task Benchmark and Analysis Platform for Natural Language Understanding},
  author={Wang, Alex and Singh, Amanpreet and Michael, Julian and Hill, Felix and Levy, Omer and Bowman, Samuel R.},
  note={In the Proceedings of ICLR.},
  year={2019}
}

Note that each GLUE dataset has its own citation. Please see the source to see
the correct citation for each contained dataset.
```

## glue/sst2

*   **Config description**: The Stanford Sentiment Treebank consists of
    sentences from movie reviews and human annotations of their sentiment. The
    task is to predict the sentiment of a given sentence. We use the two-way
    (positive/negative) class split, and use only sentence-level labels.
*   **Homepage**:
    [https://nlp.stanford.edu/sentiment/index.html](https://nlp.stanford.edu/sentiment/index.html)
*   **Download size**: `7.09 MiB`
*   **Splits**:

Split        | Examples
:----------- | -------:
'test'       | 1,821
'train'      | 67,349
'validation' | 872

*   **Features**:

```python
FeaturesDict({
    'idx': tf.int32,
    'label': ClassLabel(shape=(), dtype=tf.int64, num_classes=2),
    'sentence': Text(shape=(), dtype=tf.string),
})
```
*   **Citation**:

```
@inproceedings{socher2013recursive,
  title={Recursive deep models for semantic compositionality over a sentiment treebank},
  author={Socher, Richard and Perelygin, Alex and Wu, Jean and Chuang, Jason and Manning, Christopher D and Ng, Andrew and Potts, Christopher},
  booktitle={Proceedings of the 2013 conference on empirical methods in natural language processing},
  pages={1631--1642},
  year={2013}
}
@inproceedings{wang2019glue,
  title={{GLUE}: A Multi-Task Benchmark and Analysis Platform for Natural Language Understanding},
  author={Wang, Alex and Singh, Amanpreet and Michael, Julian and Hill, Felix and Levy, Omer and Bowman, Samuel R.},
  note={In the Proceedings of ICLR.},
  year={2019}
}

Note that each GLUE dataset has its own citation. Please see the source to see
the correct citation for each contained dataset.
```

## glue/mrpc

*   **Config description**: The Microsoft Research Paraphrase Corpus (Dolan &
    Brockett, 2005) is a corpus of sentence pairs automatically extracted from
    online news sources, with human annotations for whether the sentences in the
    pair are semantically equivalent.
*   **Homepage**:
    [https://www.microsoft.com/en-us/download/details.aspx?id=52398](https://www.microsoft.com/en-us/download/details.aspx?id=52398)
*   **Download size**: `1.43 MiB`
*   **Splits**:

Split        | Examples
:----------- | -------:
'test'       | 1,725
'train'      | 3,668
'validation' | 408

*   **Features**:

```python
FeaturesDict({
    'idx': tf.int32,
    'label': ClassLabel(shape=(), dtype=tf.int64, num_classes=2),
    'sentence1': Text(shape=(), dtype=tf.string),
    'sentence2': Text(shape=(), dtype=tf.string),
})
```
*   **Citation**:

```
@inproceedings{dolan2005automatically,
  title={Automatically constructing a corpus of sentential paraphrases},
  author={Dolan, William B and Brockett, Chris},
  booktitle={Proceedings of the Third International Workshop on Paraphrasing (IWP2005)},
  year={2005}
}
@inproceedings{wang2019glue,
  title={{GLUE}: A Multi-Task Benchmark and Analysis Platform for Natural Language Understanding},
  author={Wang, Alex and Singh, Amanpreet and Michael, Julian and Hill, Felix and Levy, Omer and Bowman, Samuel R.},
  note={In the Proceedings of ICLR.},
  year={2019}
}

Note that each GLUE dataset has its own citation. Please see the source to see
the correct citation for each contained dataset.
```

## glue/qqp

*   **Config description**: The Quora Question Pairs2 dataset is a collection of
    question pairs from the community question-answering website Quora. The task
    is to determine whether a pair of questions are semantically equivalent.
*   **Homepage**:
    [https://data.quora.com/First-Quora-Dataset-Release-Question-Pairs](https://data.quora.com/First-Quora-Dataset-Release-Question-Pairs)
*   **Download size**: `57.73 MiB`
*   **Splits**:

Split        | Examples
:----------- | -------:
'test'       | 390,965
'train'      | 363,849
'validation' | 40,430

*   **Features**:

```python
FeaturesDict({
    'idx': tf.int32,
    'label': ClassLabel(shape=(), dtype=tf.int64, num_classes=2),
    'question1': Text(shape=(), dtype=tf.string),
    'question2': Text(shape=(), dtype=tf.string),
})
```
*   **Citation**:

```
@online{WinNT,
  author = {Iyer, Shankar and Dandekar, Nikhil and Csernai, Kornel},
  title = {First Quora Dataset Release: Question Pairs},
  year = 2017,
  url = {https://data.quora.com/First-Quora-Dataset-Release-Question-Pairs},
  urldate = {2019-04-03}
}
@inproceedings{wang2019glue,
  title={{GLUE}: A Multi-Task Benchmark and Analysis Platform for Natural Language Understanding},
  author={Wang, Alex and Singh, Amanpreet and Michael, Julian and Hill, Felix and Levy, Omer and Bowman, Samuel R.},
  note={In the Proceedings of ICLR.},
  year={2019}
}

Note that each GLUE dataset has its own citation. Please see the source to see
the correct citation for each contained dataset.
```

## glue/stsb

*   **Config description**: The Semantic Textual Similarity Benchmark (Cer et
    al., 2017) is a collection of sentence pairs drawn from news headlines,
    video and image captions, and natural language inference data. Each pair is
    human-annotated with a similarity score from 1 to 5.
*   **Homepage**:
    [http://ixa2.si.ehu.es/stswiki/index.php/STSbenchmark](http://ixa2.si.ehu.es/stswiki/index.php/STSbenchmark)
*   **Download size**: `784.05 KiB`
*   **Splits**:

Split        | Examples
:----------- | -------:
'test'       | 1,379
'train'      | 5,749
'validation' | 1,500

*   **Features**:

```python
FeaturesDict({
    'idx': tf.int32,
    'label': tf.float32,
    'sentence1': Text(shape=(), dtype=tf.string),
    'sentence2': Text(shape=(), dtype=tf.string),
})
```
*   **Citation**:

```
@article{cer2017semeval,
  title={Semeval-2017 task 1: Semantic textual similarity-multilingual and cross-lingual focused evaluation},
  author={Cer, Daniel and Diab, Mona and Agirre, Eneko and Lopez-Gazpio, Inigo and Specia, Lucia},
  journal={arXiv preprint arXiv:1708.00055},
  year={2017}
}
@inproceedings{wang2019glue,
  title={{GLUE}: A Multi-Task Benchmark and Analysis Platform for Natural Language Understanding},
  author={Wang, Alex and Singh, Amanpreet and Michael, Julian and Hill, Felix and Levy, Omer and Bowman, Samuel R.},
  note={In the Proceedings of ICLR.},
  year={2019}
}

Note that each GLUE dataset has its own citation. Please see the source to see
the correct citation for each contained dataset.
```

## glue/mnli

*   **Config description**: The Multi-Genre Natural Language Inference Corpusn
    is a crowdsourced collection of sentence pairs with textual entailment
    annotations. Given a premise sentence and a hypothesis sentence, the task is
    to predict whether the premise entails the hypothesis (entailment),
    contradicts the hypothesis (contradiction), or neither (neutral). The
    premise sentences are gathered from ten different sources, including
    transcribed speech, fiction, and government reports. We use the standard
    test set, for which we obtained private labels from the authors, and
    evaluate on both the matched (in-domain) and mismatched (cross-domain)
    section. We also use and recommend the SNLI corpus as 550k examples of
    auxiliary training data.
*   **Homepage**:
    [http://www.nyu.edu/projects/bowman/multinli/](http://www.nyu.edu/projects/bowman/multinli/)
*   **Download size**: `298.29 MiB`
*   **Splits**:

Split                   | Examples
:---------------------- | -------:
'test_matched'          | 9,796
'test_mismatched'       | 9,847
'train'                 | 392,702
'validation_matched'    | 9,815
'validation_mismatched' | 9,832

*   **Features**:

```python
FeaturesDict({
    'hypothesis': Text(shape=(), dtype=tf.string),
    'idx': tf.int32,
    'label': ClassLabel(shape=(), dtype=tf.int64, num_classes=3),
    'premise': Text(shape=(), dtype=tf.string),
})
```
*   **Citation**:

```
@InProceedings{N18-1101,
  author = "Williams, Adina
            and Nangia, Nikita
            and Bowman, Samuel",
  title = "A Broad-Coverage Challenge Corpus for
           Sentence Understanding through Inference",
  booktitle = "Proceedings of the 2018 Conference of
               the North American Chapter of the
               Association for Computational Linguistics:
               Human Language Technologies, Volume 1 (Long
               Papers)",
  year = "2018",
  publisher = "Association for Computational Linguistics",
  pages = "1112--1122",
  location = "New Orleans, Louisiana",
  url = "http://aclweb.org/anthology/N18-1101"
}
@article{bowman2015large,
  title={A large annotated corpus for learning natural language inference},
  author={Bowman, Samuel R and Angeli, Gabor and Potts, Christopher and Manning, Christopher D},
  journal={arXiv preprint arXiv:1508.05326},
  year={2015}
}
@inproceedings{wang2019glue,
  title={{GLUE}: A Multi-Task Benchmark and Analysis Platform for Natural Language Understanding},
  author={Wang, Alex and Singh, Amanpreet and Michael, Julian and Hill, Felix and Levy, Omer and Bowman, Samuel R.},
  note={In the Proceedings of ICLR.},
  year={2019}
}

Note that each GLUE dataset has its own citation. Please see the source to see
the correct citation for each contained dataset.
```

## glue/mnli_mismatched

*   **Config description**: The mismatched validation and test splits from MNLI.
    See the "mnli" BuilderConfig for additional information.
*   **Homepage**:
    [http://www.nyu.edu/projects/bowman/multinli/](http://www.nyu.edu/projects/bowman/multinli/)
*   **Download size**: `298.29 MiB`
*   **Splits**:

Split        | Examples
:----------- | -------:
'test'       | 9,847
'validation' | 9,832

*   **Features**:

```python
FeaturesDict({
    'hypothesis': Text(shape=(), dtype=tf.string),
    'idx': tf.int32,
    'label': ClassLabel(shape=(), dtype=tf.int64, num_classes=3),
    'premise': Text(shape=(), dtype=tf.string),
})
```
*   **Citation**:

```
@InProceedings{N18-1101,
  author = "Williams, Adina
            and Nangia, Nikita
            and Bowman, Samuel",
  title = "A Broad-Coverage Challenge Corpus for
           Sentence Understanding through Inference",
  booktitle = "Proceedings of the 2018 Conference of
               the North American Chapter of the
               Association for Computational Linguistics:
               Human Language Technologies, Volume 1 (Long
               Papers)",
  year = "2018",
  publisher = "Association for Computational Linguistics",
  pages = "1112--1122",
  location = "New Orleans, Louisiana",
  url = "http://aclweb.org/anthology/N18-1101"
}
@article{bowman2015large,
  title={A large annotated corpus for learning natural language inference},
  author={Bowman, Samuel R and Angeli, Gabor and Potts, Christopher and Manning, Christopher D},
  journal={arXiv preprint arXiv:1508.05326},
  year={2015}
}
@inproceedings{wang2019glue,
  title={{GLUE}: A Multi-Task Benchmark and Analysis Platform for Natural Language Understanding},
  author={Wang, Alex and Singh, Amanpreet and Michael, Julian and Hill, Felix and Levy, Omer and Bowman, Samuel R.},
  note={In the Proceedings of ICLR.},
  year={2019}
}

Note that each GLUE dataset has its own citation. Please see the source to see
the correct citation for each contained dataset.
```

## glue/mnli_matched

*   **Config description**: The matched validation and test splits from MNLI.
    See the "mnli" BuilderConfig for additional information.
*   **Homepage**:
    [http://www.nyu.edu/projects/bowman/multinli/](http://www.nyu.edu/projects/bowman/multinli/)
*   **Download size**: `298.29 MiB`
*   **Splits**:

Split        | Examples
:----------- | -------:
'test'       | 9,796
'validation' | 9,815

*   **Features**:

```python
FeaturesDict({
    'hypothesis': Text(shape=(), dtype=tf.string),
    'idx': tf.int32,
    'label': ClassLabel(shape=(), dtype=tf.int64, num_classes=3),
    'premise': Text(shape=(), dtype=tf.string),
})
```
*   **Citation**:

```
@InProceedings{N18-1101,
  author = "Williams, Adina
            and Nangia, Nikita
            and Bowman, Samuel",
  title = "A Broad-Coverage Challenge Corpus for
           Sentence Understanding through Inference",
  booktitle = "Proceedings of the 2018 Conference of
               the North American Chapter of the
               Association for Computational Linguistics:
               Human Language Technologies, Volume 1 (Long
               Papers)",
  year = "2018",
  publisher = "Association for Computational Linguistics",
  pages = "1112--1122",
  location = "New Orleans, Louisiana",
  url = "http://aclweb.org/anthology/N18-1101"
}
@article{bowman2015large,
  title={A large annotated corpus for learning natural language inference},
  author={Bowman, Samuel R and Angeli, Gabor and Potts, Christopher and Manning, Christopher D},
  journal={arXiv preprint arXiv:1508.05326},
  year={2015}
}
@inproceedings{wang2019glue,
  title={{GLUE}: A Multi-Task Benchmark and Analysis Platform for Natural Language Understanding},
  author={Wang, Alex and Singh, Amanpreet and Michael, Julian and Hill, Felix and Levy, Omer and Bowman, Samuel R.},
  note={In the Proceedings of ICLR.},
  year={2019}
}

Note that each GLUE dataset has its own citation. Please see the source to see
the correct citation for each contained dataset.
```

## glue/qnli

*   **Config description**: The Stanford Question Answering Dataset is a
    question-answering dataset consisting of question-paragraph pairs, where one
    of the sentences in the paragraph (drawn from Wikipedia) contains the answer
    to the corresponding question (written by an annotator). We convert the task
    into sentence pair classification by forming a pair between each question
    and each sentence in the corresponding context, and filtering out pairs with
    low lexical overlap between the question and the context sentence. The task
    is to determine whether the context sentence contains the answer to the
    question. This modified version of the original task removes the requirement
    that the model select the exact answer, but also removes the simplifying
    assumptions that the answer is always present in the input and that lexical
    overlap is a reliable cue.
*   **Homepage**:
    [https://rajpurkar.github.io/SQuAD-explorer/](https://rajpurkar.github.io/SQuAD-explorer/)
*   **Download size**: `10.14 MiB`
*   **Splits**:

Split        | Examples
:----------- | -------:
'test'       | 5,463
'train'      | 104,743
'validation' | 5,463

*   **Features**:

```python
FeaturesDict({
    'idx': tf.int32,
    'label': ClassLabel(shape=(), dtype=tf.int64, num_classes=2),
    'question': Text(shape=(), dtype=tf.string),
    'sentence': Text(shape=(), dtype=tf.string),
})
```
*   **Citation**:

```
@article{rajpurkar2016squad,
  title={Squad: 100,000+ questions for machine comprehension of text},
  author={Rajpurkar, Pranav and Zhang, Jian and Lopyrev, Konstantin and Liang, Percy},
  journal={arXiv preprint arXiv:1606.05250},
  year={2016}
}
@inproceedings{wang2019glue,
  title={{GLUE}: A Multi-Task Benchmark and Analysis Platform for Natural Language Understanding},
  author={Wang, Alex and Singh, Amanpreet and Michael, Julian and Hill, Felix and Levy, Omer and Bowman, Samuel R.},
  note={In the Proceedings of ICLR.},
  year={2019}
}

Note that each GLUE dataset has its own citation. Please see the source to see
the correct citation for each contained dataset.
```

## glue/rte

*   **Config description**: The Recognizing Textual Entailment (RTE) datasets
    come from a series of annual textual entailment challenges. We combine the
    data from RTE1 (Dagan et al., 2006), RTE2 (Bar Haim et al., 2006), RTE3
    (Giampiccolo et al., 2007), and RTE5 (Bentivogli et al., 2009).4 Examples
    are constructed based on news and Wikipedia text. We convert all datasets to
    a two-class split, where for three-class datasets we collapse neutral and
    contradiction into not entailment, for consistency.
*   **Homepage**:
    [https://aclweb.org/aclwiki/Recognizing_Textual_Entailment](https://aclweb.org/aclwiki/Recognizing_Textual_Entailment)
*   **Download size**: `680.81 KiB`
*   **Splits**:

Split        | Examples
:----------- | -------:
'test'       | 3,000
'train'      | 2,490
'validation' | 277

*   **Features**:

```python
FeaturesDict({
    'idx': tf.int32,
    'label': ClassLabel(shape=(), dtype=tf.int64, num_classes=2),
    'sentence1': Text(shape=(), dtype=tf.string),
    'sentence2': Text(shape=(), dtype=tf.string),
})
```
*   **Citation**:

```
@inproceedings{dagan2005pascal,
  title={The PASCAL recognising textual entailment challenge},
  author={Dagan, Ido and Glickman, Oren and Magnini, Bernardo},
  booktitle={Machine Learning Challenges Workshop},
  pages={177--190},
  year={2005},
  organization={Springer}
}
@inproceedings{bar2006second,
  title={The second pascal recognising textual entailment challenge},
  author={Bar-Haim, Roy and Dagan, Ido and Dolan, Bill and Ferro, Lisa and Giampiccolo, Danilo and Magnini, Bernardo and Szpektor, Idan},
  booktitle={Proceedings of the second PASCAL challenges workshop on recognising textual entailment},
  volume={6},
  number={1},
  pages={6--4},
  year={2006},
  organization={Venice}
}
@inproceedings{giampiccolo2007third,
  title={The third pascal recognizing textual entailment challenge},
  author={Giampiccolo, Danilo and Magnini, Bernardo and Dagan, Ido and Dolan, Bill},
  booktitle={Proceedings of the ACL-PASCAL workshop on textual entailment and paraphrasing},
  pages={1--9},
  year={2007},
  organization={Association for Computational Linguistics}
}
@inproceedings{bentivogli2009fifth,
  title={The Fifth PASCAL Recognizing Textual Entailment Challenge.},
  author={Bentivogli, Luisa and Clark, Peter and Dagan, Ido and Giampiccolo, Danilo},
  booktitle={TAC},
  year={2009}
}
@inproceedings{wang2019glue,
  title={{GLUE}: A Multi-Task Benchmark and Analysis Platform for Natural Language Understanding},
  author={Wang, Alex and Singh, Amanpreet and Michael, Julian and Hill, Felix and Levy, Omer and Bowman, Samuel R.},
  note={In the Proceedings of ICLR.},
  year={2019}
}

Note that each GLUE dataset has its own citation. Please see the source to see
the correct citation for each contained dataset.
```

## glue/wnli

*   **Config description**: The Winograd Schema Challenge (Levesque et al.,
    2011) is a reading comprehension task in which a system must read a sentence
    with a pronoun and select the referent of that pronoun from a list of
    choices. The examples are manually constructed to foil simple statistical
    methods: Each one is contingent on contextual information provided by a
    single word or phrase in the sentence. To convert the problem into sentence
    pair classification, we construct sentence pairs by replacing the ambiguous
    pronoun with each possible referent. The task is to predict if the sentence
    with the pronoun substituted is entailed by the original sentence. We use a
    small evaluation set consisting of new examples derived from fiction books
    that was shared privately by the authors of the original corpus. While the
    included training set is balanced between two classes, the test set is
    imbalanced between them (65% not entailment). Also, due to a data quirk, the
    development set is adversarial: hypotheses are sometimes shared between
    training and development examples, so if a model memorizes the training
    examples, they will predict the wrong label on corresponding development set
    example. As with QNLI, each example is evaluated separately, so there is not
    a systematic correspondence between a model's score on this task and its
    score on the unconverted original task. We call converted dataset WNLI
    (Winograd NLI).
*   **Homepage**:
    [https://cs.nyu.edu/faculty/davise/papers/WinogradSchemas/WS.html](https://cs.nyu.edu/faculty/davise/papers/WinogradSchemas/WS.html)
*   **Download size**: `28.32 KiB`
*   **Splits**:

Split        | Examples
:----------- | -------:
'test'       | 146
'train'      | 635
'validation' | 71

*   **Features**:

```python
FeaturesDict({
    'idx': tf.int32,
    'label': ClassLabel(shape=(), dtype=tf.int64, num_classes=2),
    'sentence1': Text(shape=(), dtype=tf.string),
    'sentence2': Text(shape=(), dtype=tf.string),
})
```
*   **Citation**:

```
@inproceedings{levesque2012winograd,
  title={The winograd schema challenge},
  author={Levesque, Hector and Davis, Ernest and Morgenstern, Leora},
  booktitle={Thirteenth International Conference on the Principles of Knowledge Representation and Reasoning},
  year={2012}
}
@inproceedings{wang2019glue,
  title={{GLUE}: A Multi-Task Benchmark and Analysis Platform for Natural Language Understanding},
  author={Wang, Alex and Singh, Amanpreet and Michael, Julian and Hill, Felix and Levy, Omer and Bowman, Samuel R.},
  note={In the Proceedings of ICLR.},
  year={2019}
}

Note that each GLUE dataset has its own citation. Please see the source to see
the correct citation for each contained dataset.
```

## glue/ax

*   **Config description**: A manually-curated evaluation dataset for
    fine-grained analysis of system performance on a broad range of linguistic
    phenomena. This dataset evaluates sentence understanding through Natural
    Language Inference (NLI) problems. Use a model trained on MulitNLI to
    produce predictions for this dataset.
*   **Homepage**:
    [https://gluebenchmark.com/diagnostics](https://gluebenchmark.com/diagnostics)
*   **Download size**: `217.05 KiB`
*   **Splits**:

Split  | Examples
:----- | -------:
'test' | 1,104

*   **Features**:

```python
FeaturesDict({
    'hypothesis': Text(shape=(), dtype=tf.string),
    'idx': tf.int32,
    'label': ClassLabel(shape=(), dtype=tf.int64, num_classes=3),
    'premise': Text(shape=(), dtype=tf.string),
})
```
*   **Citation**:

```
@inproceedings{wang2019glue,
  title={{GLUE}: A Multi-Task Benchmark and Analysis Platform for Natural Language Understanding},
  author={Wang, Alex and Singh, Amanpreet and Michael, Julian and Hill, Felix and Levy, Omer and Bowman, Samuel R.},
  note={In the Proceedings of ICLR.},
  year={2019}
}

Note that each GLUE dataset has its own citation. Please see the source to see
the correct citation for each contained dataset.
```
