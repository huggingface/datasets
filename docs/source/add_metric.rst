Writing a metric loading script
=============================================

If you want to use your own metric, or if you would like to share a new metric with the community, for instance in the `HuggingFace Hub <https://huggingface.co/metrics>`__, then you can define a new metric loading script.

This chapter will explain how metrics are loaded and how you can write from scratch or adapt a metric loading script.

.. note::

	You can start from the `template for a metric loading script <https://github.com/huggingface/datasets/blob/master/templates/new_metric_script.py>`__ when writing a new metric loading script. You can find this template in the ``templates`` folder on the github repository.


To create a new metric loading script one mostly needs to specify three methods in a :class:`datasets.Metric` class:

- :func:`datasets.Metric._info` which is in charge of specifying the metric metadata as a :obj:`datasets.MetricInfo` dataclass and in particular the :class:`datasets.Features` which defined the types of the predictions and the references,
- :func:`datasets.Metric._compute` which is in charge of computing the actual score(s), given some predictions and references.

.. note::

	Note on naming: the metric class should be camel case, while the metric name is its snake case equivalent (ex: :obj:`class Rouge(datasets.Metric)` for the metric ``rouge``).


Adding metric metadata
----------------------------------

The :func:`datasets.Metric._info` method is in charge of specifying the metric metadata as a :obj:`datasets.MetricInfo` dataclass and in particular the :class:`datasets.Features` which defined the types of the predictions and the references. :class:`datasets.MetricInfo` has a predefined set of attributes and cannot be extended. The full list of attributes can be found in the package reference.

The most important attributes to specify are:

- :attr:`datasets.MetricInfo.features`: a :class:`datasets.Features` instance defining the name and the type the predictions and references,
- :attr:`datasets.MetricInfo.description`: a :obj:`str` describing the metric,
- :attr:`datasets.MetricInfo.citation`: a :obj:`str` containing the citation for the metric in a BibTex format for inclusion in communications citing the metric,
- :attr:`datasets.MetricInfo.homepage`: a :obj:`str` containing an URL to an original homepage of the metric.
- :attr:`datasets.MetricInfo.format`: an optional :obj:`str` to tell what is the format of the predictions and the references passed to _compute. It can be set to "numpy", "torch", "tensorflow" or "pandas".

Here is for instance the :func:`datasets.Metric._info` for the Sacrebleu metric for instance, which is taken from the `sacrebleu metric loading script <https://github.com/huggingface/datasets/tree/master/metrics/sacrebleu/sacrebleu.py>`__

.. code-block::

    def _info(self):
        return datasets.MetricInfo(
            description=_DESCRIPTION,
            citation=_CITATION,
            homepage="https://github.com/mjpost/sacreBLEU",
            inputs_description=_KWARGS_DESCRIPTION,
            features=datasets.Features({
                'predictions': datasets.Value('string'),
                'references': datasets.Sequence(datasets.Value('string')),
            }),
            codebase_urls=["https://github.com/mjpost/sacreBLEU"],
            reference_urls=["https://github.com/mjpost/sacreBLEU",
                            "https://en.wikipedia.org/wiki/BLEU",
                            "https://towardsdatascience.com/evaluating-text-output-in-nlp-bleu-at-your-own-risk-e8609665a213"]
        )


The :class:`datasets.Features` define the type of the predictions and the references and can define arbitrary nested objects with fields of various types. More details on the available ``features`` can be found in the guide on features :doc:`features` and in the package reference on :class:`datasets.Features`. Many examples of features can also be found in the various `metric scripts provided on the GitHub repository <https://github.com/huggingface/datasets/tree/master/metrics>`__ and even in `dataset scripts provided on the GitHub repository <https://github.com/huggingface/datasets/tree/master/datasets>`__ or directly inspected on the `datasets viewer <https://huggingface.co/nlp/viewer>`__.

Here are the features of the SQuAD metric for instance, which is taken from the `squad metric loading script <https://github.com/huggingface/datasets/tree/master/metrics/squad/squad.py>`__:

.. code-block::

    datasets.Features({
        'predictions': datasets.Value('string'),
        'references': datasets.Sequence(datasets.Value('string')),
    }),

We can see that each prediction is a string, and each reference is a sequence of strings.
Indeed we can use the metric the following way:

.. code-block::

    >>> import datasets

    >>> metric = datasets.load_metric('./metrics/sacrebleu')
    >>> reference_batch = [['The dog bit the man.', 'The dog had bit the man.'],
    ...                    ['It was not unexpected.', 'No one was surprised.'],
    ...                    ['The man bit him first.', 'The man had bitten the dog.']]
    >>> sys_batch = ['The dog bit the man.', "It wasn't surprising.", 'The man had just bitten him.']
    >>> score = metric.add_batch(predictions=sys_batch, references=reference_batch)
    >>> print(metric)


Downloading data files
-------------------------------------------------

The :func:`datasets.Metric._download_and_prepare` method is in charge of downloading (or retrieving locally the data files) if needed.

This method **takes as input** a :class:`datasets.DownloadManager` which is a utility which can be used to download files (or to retrieve them from the local filesystem if they are local files or are already in the cache).

Let's have a look at a simple example of a :func:`datasets.Metric._download_and_prepare` method. We'll take the example of the `bleurt metric loading script <https://github.com/huggingface/datasets/tree/master/metrics/bleurt/bleurt.py>`__:

.. code-block::

    def _download_and_prepare(self, dl_manager):

        # check that config name specifies a valid BLEURT model
        if self.config_name not in CHECKPOINT_URLS.keys():
            raise KeyError(f"{self.config_name} model not found. You should supply the name of a model checkpoint for bleurt in {CHECKPOINT_URLS.keys()}")

        # download the model checkpoint specified by self.config_name and set up the scorer
        model_path = dl_manager.download_and_extract(CHECKPOINT_URLS[self.config_name])
        self.scorer = score.BleurtScorer(os.path.join(model_path, self.config_name))  

As you can see this method downloads a model checkpoint depending of the configuration name of the metric. The checkpoint url is then provided to the :func:`datasets.DownloadManager.download_and_extract` method which will take care of downloading or retrieving the file from the local file system and returning a object of the same type and organization (here a just one path, but it could be a list or a dict of paths) with the path to the local version of the requested files. :func:`datasets.DownloadManager.download_and_extract` can take as input a single URL/path or a list or dictionary of URLs/paths and will return an object of the same structure (single URL/path, list or dictionary of URLs/paths) with the path to the local files. This method also takes care of extracting compressed tar, gzip and zip archives.

:func:`datasets.DownloadManager.download_and_extract` can download files from a large set of origins but if your data files are hosted on a special access server, it's also possible to provide a callable which will take care of the downloading process to the ``DownloadManager`` using :func:`datasets.DownloadManager.download_custom`.

.. note::

	In addition to :func:`datasets.DownloadManager.download_and_extract` and :func:`datasets.DownloadManager.download_custom`, the :class:`datasets.DownloadManager` class also provide more fine-grained control on the download and extraction process through several methods including: :func:`datasets.DownloadManager.download`, :func:`datasets.DownloadManager.extract` and :func:`datasets.DownloadManager.iter_archive`. Please refer to the package reference on :class:`datasets.DownloadManager` for details on these methods.


Computing the scores
-------------------------------------------------

The :func:`datasets.DatasetBuilder._compute` is in charge of computing the metric scores given predictions and references that are in the format specified in the ``features`` set in :func:`datasets.DatasetBuilder._info`.

Here again, let's take the simple example of the `xnli metric loading script <https://github.com/huggingface/datasets/tree/master/metrics/squad/squad.py>`__:

.. code-block::

    def simple_accuracy(preds, labels):
        return (preds == labels).mean()

    class Xnli(datasets.Metric):
        def _info(self):
            return datasets.MetricInfo(
                description=_DESCRIPTION,
                citation=_CITATION,
                inputs_description=_KWARGS_DESCRIPTION,
                features=datasets.Features({
                    'predictions': datasets.Value('int64' if self.config_name != 'sts-b' else 'float32'),
                    'references': datasets.Value('int64' if self.config_name != 'sts-b' else 'float32'),
                }),
                codebase_urls=[],
                reference_urls=[],
                format='numpy'
            )

        def _compute(self, predictions, references):
            return {"accuracy": simple_accuracy(predictions, references)}

Here to compute the accuracy it uses the simple_accuracy function, that uses numpy to compute the accuracy using .mean()

The predictions and references objects passes to _compute are sequences of integers or floats, and the sequences are formated as numpy arrays since the format specified in the :obj:`datasets.MetricInfo` object is set to "numpy".

Specifying several metric configurations
-------------------------------------------------

Sometimes you want to provide several ways of computing the scores.

It is possible to gave different configurations for a metric. The configuration name is stored in :obj:`datasets.Metric.config_name` attribute. The configuration name can be specified by the user when instantiating a metric:

.. code-block::

	>>> from datasets import load_metric
	>>> metric = load_metric('bleurt', name='bleurt-base-128')
	>>> metric = load_metric('bleurt', name='bleurt-base-512')

Here depending on the configuration name, a different checkpoint will be downloaded and used to compute the BLEURT score.

You can access :obj:`datasets.Metric.config_name` from inside :func:`datasets.Metric._info`, :func:`datasets.Metric._download_and_prepare` and :func:`datasets.Metric._compute`

Testing the metric loading script
-------------------------------------------------

Once you're finished with creating or adapting a metric loading script, you can try it locally by giving the path to the metric loading script:

.. code-block::

	>>> from datasets import load_metric
	>>> metric = load_metric('PATH/TO/MY/SCRIPT.py')

If your metric has several configurations you can use the arguments of :func:`datasets.load_metric` accordingly:

.. code-block::

	>>> from datasets import load_metric
	>>> metric = load_metric('PATH/TO/MY/SCRIPT.py', 'my_configuration')


