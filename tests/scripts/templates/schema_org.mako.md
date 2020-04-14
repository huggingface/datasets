<%!
"""
Builds schema.org microdata for DatasetSearch from DatasetBuilder.

Markup spec: https://developers.google.com/search/docs/data-types/dataset#dataset
Testing tool: https://search.google.com/structured-data/testing-tool
For Google Dataset Search: https://toolbox.google.com/datasetsearch

Microdata format was chosen over JSON-LD due to the fact that Markdown
rendering engines remove all \<script\> tags.
"""

import html

def escape(val):
  val = html.escape(val, quote=True)
  val = val.replace("\n", "&#10;")
  val = val.strip()
  return val
%>
<%
description = """{description}

To use this dataset:

```python
import tensorflow_datasets as tfds

ds = tfds.load('{name}', split='train')
for ex in ds.take(4):
  print(ex)
```

See [the guide](https://www.tensorflow.org/datasets/overview) for more
informations on [tensorflow_datasets](https://www.tensorflow.org/datasets).

""".format(
    description=builder.info.description,
    name=builder.info.name,
)

%>

<div itemscope itemtype="http://schema.org/Dataset">
  <div itemscope itemprop="includedInDataCatalog" itemtype="http://schema.org/DataCatalog">
    <meta itemprop="name" content="TensorFlow Datasets" />
  </div>
  <meta itemprop="name" content="${builder.info.name}" />
  <meta itemprop="description" content="${escape(description)}" />
  <meta itemprop="url" content="https://www.tensorflow.org/datasets/catalog/${builder.info.name}" />
  <meta itemprop="sameAs" content="${escape(builder.info.homepage)}" />
  <meta itemprop="citation" content="${escape(builder.info.citation)}" />
</div>
