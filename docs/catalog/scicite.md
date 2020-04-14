<div itemscope itemtype="http://schema.org/Dataset">
  <div itemscope itemprop="includedInDataCatalog" itemtype="http://schema.org/DataCatalog">
    <meta itemprop="name" content="TensorFlow Datasets" />
  </div>
  <meta itemprop="name" content="scicite" />
  <meta itemprop="description" content="&#10;This is a dataset for classifying citation intents in academic papers.&#10;The main citation intent label for each Json object is specified with the label&#10;key while the citation context is specified in with a context key. Example:&#10;{&#10; &#x27;string&#x27;: &#x27;In chacma baboons, male-infant relationships can be linked to both&#10;    formation of friendships and paternity success [30,31].&#x27;&#10; &#x27;sectionName&#x27;: &#x27;Introduction&#x27;,&#10; &#x27;label&#x27;: &#x27;background&#x27;,&#10; &#x27;citingPaperId&#x27;: &#x27;7a6b2d4b405439&#x27;,&#10; &#x27;citedPaperId&#x27;: &#x27;9d1abadc55b5e0&#x27;,&#10; ...&#10; }&#10;You may obtain the full information about the paper using the provided paper ids&#10;with the Semantic Scholar API (https://api.semanticscholar.org/).&#10;The labels are:&#10;Method, Background, Result&#10;&#10;&#10;To use this dataset:&#10;&#10;```python&#10;import tensorflow_datasets as tfds&#10;&#10;ds = tfds.load(&#x27;scicite&#x27;, split=&#x27;train&#x27;)&#10;for ex in ds.take(4):&#10;  print(ex)&#10;```&#10;&#10;See [the guide](https://www.tensorflow.org/datasets/overview) for more&#10;informations on [tensorflow_datasets](https://www.tensorflow.org/datasets).&#10;&#10;" />
  <meta itemprop="url" content="https://www.tensorflow.org/datasets/catalog/scicite" />
  <meta itemprop="sameAs" content="https://github.com/allenai/scicite" />
  <meta itemprop="citation" content="&#10;@InProceedings{Cohan2019Structural,&#10;  author={Arman Cohan and Waleed Ammar and Madeleine Van Zuylen and Field Cady},&#10;  title={Structural Scaffolds for Citation Intent Classification in Scientific Publications},&#10;  booktitle=&quot;NAACL&quot;,&#10;  year=&quot;2019&quot;&#10;}&#10;" />
</div>
# `scicite`

*   **Description**:

This is a dataset for classifying citation intents in academic papers. The main
citation intent label for each Json object is specified with the label key while
the citation context is specified in with a context key. Example: { 'string':
'In chacma baboons, male-infant relationships can be linked to both formation of
friendships and paternity success [30,31].' 'sectionName': 'Introduction',
'label': 'background', 'citingPaperId': '7a6b2d4b405439', 'citedPaperId':
'9d1abadc55b5e0', ... } You may obtain the full information about the paper
using the provided paper ids with the Semantic Scholar API
(https://api.semanticscholar.org/). The labels are: Method, Background, Result

*   **Homepage**:
    [https://github.com/allenai/scicite](https://github.com/allenai/scicite)
*   **Source code**:
    [`tfds.text.scicite.Scicite`](https://github.com/tensorflow/datasets/tree/master/tensorflow_datasets/text/scicite.py)
*   **Versions**:
    *   **`1.0.0`** (default): No release notes.
*   **Download size**: `22.12 MiB`
*   **Dataset size**: `Unknown size`
*   **Auto-cached**
    ([documentation](https://www.tensorflow.org/datasets/performances#auto-caching)):
    No
*   **Splits**:

Split        | Examples
:----------- | -------:
'test'       | 1,859
'train'      | 8,194
'validation' | 916

*   **Features**:

```python
FeaturesDict({
    'citeEnd': tf.int64,
    'citeStart': tf.int64,
    'citedPaperId': Text(shape=(), dtype=tf.string),
    'citingPaperId': Text(shape=(), dtype=tf.string),
    'excerpt_index': tf.int32,
    'id': Text(shape=(), dtype=tf.string),
    'isKeyCitation': tf.bool,
    'label': ClassLabel(shape=(), dtype=tf.int64, num_classes=3),
    'label2': ClassLabel(shape=(), dtype=tf.int64, num_classes=4),
    'label2_confidence': tf.float32,
    'label_confidence': tf.float32,
    'sectionName': Text(shape=(), dtype=tf.string),
    'source': ClassLabel(shape=(), dtype=tf.int64, num_classes=7),
    'string': Text(shape=(), dtype=tf.string),
})
```
*   **Supervised keys** (See
    [`as_supervised` doc](https://www.tensorflow.org/datasets/api_docs/python/tfds/load#args)):
    `('string', 'label')`
*   **Citation**:

```
@InProceedings{Cohan2019Structural,
  author={Arman Cohan and Waleed Ammar and Madeleine Van Zuylen and Field Cady},
  title={Structural Scaffolds for Citation Intent Classification in Scientific Publications},
  booktitle="NAACL",
  year="2019"
}
```
