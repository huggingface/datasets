<div itemscope itemtype="http://schema.org/Dataset">
  <div itemscope itemprop="includedInDataCatalog" itemtype="http://schema.org/DataCatalog">
    <meta itemprop="name" content="TensorFlow Datasets" />
  </div>
  <meta itemprop="name" content="trivia_qa" />
  <meta itemprop="description" content="TriviaqQA is a reading comprehension dataset containing over 650K&#10;question-answer-evidence triples. TriviaqQA includes 95K question-answer&#10;pairs authored by trivia enthusiasts and independently gathered evidence&#10;documents, six per question on average, that provide high quality distant&#10;supervision for answering the questions.&#10;&#10;&#10;To use this dataset:&#10;&#10;```python&#10;import tensorflow_datasets as tfds&#10;&#10;ds = tfds.load(&#x27;trivia_qa&#x27;, split=&#x27;train&#x27;)&#10;for ex in ds.take(4):&#10;  print(ex)&#10;```&#10;&#10;See [the guide](https://www.tensorflow.org/datasets/overview) for more&#10;informations on [tensorflow_datasets](https://www.tensorflow.org/datasets).&#10;&#10;" />
  <meta itemprop="url" content="https://www.tensorflow.org/datasets/catalog/trivia_qa" />
  <meta itemprop="sameAs" content="http://nlp.cs.washington.edu/triviaqa/" />
  <meta itemprop="citation" content="&#10;@article{2017arXivtriviaqa,&#10;       author = {{Joshi}, Mandar and {Choi}, Eunsol and {Weld},&#10;                 Daniel and {Zettlemoyer}, Luke},&#10;        title = &quot;{triviaqa: A Large Scale Distantly Supervised Challenge Dataset for Reading Comprehension}&quot;,&#10;      journal = {arXiv e-prints},&#10;         year = 2017,&#10;          eid = {arXiv:1705.03551},&#10;        pages = {arXiv:1705.03551},&#10;archivePrefix = {arXiv},&#10;       eprint = {1705.03551},&#10;}&#10;" />
</div>
# `trivia_qa`

*   **Description**:

TriviaqQA is a reading comprehension dataset containing over 650K
question-answer-evidence triples. TriviaqQA includes 95K question-answer pairs
authored by trivia enthusiasts and independently gathered evidence documents,
six per question on average, that provide high quality distant supervision for
answering the questions.

*   **Homepage**:
    [http://nlp.cs.washington.edu/triviaqa/](http://nlp.cs.washington.edu/triviaqa/)
*   **Source code**:
    [`tfds.text.trivia_qa.TriviaQA`](https://github.com/tensorflow/datasets/tree/master/tensorflow_datasets/text/trivia_qa.py)
*   **Versions**:
    *   **`1.1.0`** (default): No release notes.
*   **Download size**: `Unknown size`
*   **Dataset size**: `119.78 MiB`
*   **Auto-cached**
    ([documentation](https://www.tensorflow.org/datasets/performances#auto-caching)):
    Yes
*   **Splits**:

Split        | Examples
:----------- | -------:
'test'       | 10,832
'train'      | 87,622
'validation' | 11,313

*   **Features**:

```python
FeaturesDict({
    'answer': FeaturesDict({
        'aliases': Sequence(Text(shape=(), dtype=tf.string)),
        'matched_wiki_entity_name': Text(shape=(), dtype=tf.string),
        'normalized_aliases': Sequence(Text(shape=(), dtype=tf.string)),
        'normalized_matched_wiki_entity_name': Text(shape=(), dtype=tf.string),
        'normalized_value': Text(shape=(), dtype=tf.string),
        'type': Text(shape=(), dtype=tf.string),
        'value': Text(shape=(), dtype=tf.string),
    }),
    'entity_pages': Sequence({
        'doc_source': Text(shape=(), dtype=tf.string),
        'filename': Text(shape=(), dtype=tf.string),
        'title': Text(shape=(), dtype=tf.string),
        'wiki_context': Text(shape=(), dtype=tf.string),
    }),
    'question': Text(shape=(), dtype=tf.string),
    'question_id': Text(shape=(), dtype=tf.string),
    'question_source': Text(shape=(), dtype=tf.string),
    'search_results': Sequence({
        'description': Text(shape=(), dtype=tf.string),
        'filename': Text(shape=(), dtype=tf.string),
        'rank': tf.int32,
        'search_context': Text(shape=(), dtype=tf.string),
        'title': Text(shape=(), dtype=tf.string),
        'url': Text(shape=(), dtype=tf.string),
    }),
})
```
*   **Supervised keys** (See
    [`as_supervised` doc](https://www.tensorflow.org/datasets/api_docs/python/tfds/load#args)):
    `None`
*   **Citation**:

```
@article{2017arXivtriviaqa,
       author = {{Joshi}, Mandar and {Choi}, Eunsol and {Weld},
                 Daniel and {Zettlemoyer}, Luke},
        title = "{triviaqa: A Large Scale Distantly Supervised Challenge Dataset for Reading Comprehension}",
      journal = {arXiv e-prints},
         year = 2017,
          eid = {arXiv:1705.03551},
        pages = {arXiv:1705.03551},
archivePrefix = {arXiv},
       eprint = {1705.03551},
}
```

## trivia_qa/rc (default config)

*   **Config description**: Question-answer pairs where all documents for a
    given question contain the answer string(s). Includes context from Wikipedia
    and search results.

## trivia_qa/rc.nocontext

*   **Config description**: Question-answer pairs where all documents for a
    given question contain the answer string(s).

## trivia_qa/unfiltered

*   **Config description**: 110k question-answer pairs for open domain QA where
    not all documents for a given question contain the answer string(s). This
    makes the unfiltered dataset more appropriate for IR-style QA. Includes
    context from Wikipedia and search results.

## trivia_qa/unfiltered.nocontext

*   **Config description**: 110k question-answer pairs for open domain QA where
    not all documents for a given question contain the answer string(s). This
    makes the unfiltered dataset more appropriate for IR-style QA.
