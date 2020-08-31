Loading a Metric
==============================================================

The `nlp` library also provides a selection of metrics focusing in particular on:
- providing a common API accross a range of NLP metrics
- providing metrics associated to some benchmark datasets provided by the libray such as GLUE or SQuAD
- providing access to recent and more complex metrics such as BLEURT or BERTScore
- allowing a simple use of metrics in distributed and large-scale setups

Metrics have a lot in common with how :class:`nlp.Datasets` are loaded and provided using :func:`nlp.load_dataset`.

Metrics are also provided by means of simple scripts

