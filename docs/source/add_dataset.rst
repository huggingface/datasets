Writing a dataset loading script
=============================================

There are two main reasons you may want to write your own dataset loading script:

- you want to use local/private data files and the generic dataloader for CSV/JSON/text files (see :ref:`loading-from-local-files`) are not enough for your use-case,
- you would like to share a new dataset with the community, for instance in the `HuggingFace Hub <https://huggingface.co/datasets>`__.

In these cases you will need to understand how datasets are loaded and how you can write from scratch or adapt a dataset loading script.

This is the purpose of this chapter.

.. note::

	You can start from the `template for a dataset loading script <https://github.com/huggingface/nlp/blob/master/templates/new_dataset_script.py>`__ when writing a new dataset loading script. You can find this template in the ``templates`` folder on the github repository.

Here a quick general overview of the classes  and method involved when generating a dataset:

.. image:: /imgs/nlp_doc.jpg

On the left is the general organization inside the library to create a :class:`nlp.Dataset` instance and on the right, the elements which are specific to each dataset loading script.

To create a new dataset loading script one mostly need to specify three methods in a :class:`nlp.DatasetBuilder` class:

- :func:`nlp.DatasetBuilder._info` which is in charge of specifying the dataset metadata as a :obj:`nlp.DatasetInfo` dataclass and in particular the :class:`nlp.Features` which defined the names and types of each column in the dataset,
- :func:`nlp.DatasetBuilder._split_generator` which is in charge of downloading or retrieving the data files, organizing them by splits and defining specific arguments for the generation process if needed,
- :func:`nlp.DatasetBuilder._generate_examples` which is in charge of loading the files for a split and yielding examples with the format specified in the ``features``.

Optionally, the dataset loading script can define a configuration to be used by the :class:`nlp.DatasetBuilder` by inheriting from :class:`nlp.BuilderConfig`. Such a class allows to customize the building process, for instance by allowing to select specific subsets of the data or specific ways to process the data when loading the dataset.

.. note::

	Note on naming: the dataset class should be camel case, while the dataset name is its snake case equivalent (ex: :obj:`class BookCorpus(nlp.GeneratorBasedBuilder)` for the dataset ``book_corpus``).


Adding dataset metadata
----------------------------------

The :func:`nlp.DatasetBuilder._info` method is in charge of specifying the dataset metadata as a :obj:`nlp.DatasetInfo` dataclass and in particular the :class:`nlp.Features` which defined the names and types of each column in the dataset,

:class:`nlp.DatasetInfo` has a predefined set of attributes and cannot be extended. The full list of attributes can be found in the package reference.

The most important attributes to specify are:

- :attr:`nlp.DatasetInfo.features`: a :class:`nlp.Features` instance defining the name and the type of each column in the dataset and the general organization of the examples,
- :attr:`nlp.DatasetInfo.description`: a :obj:`str` describing the dataset,
- :attr:`nlp.DatasetInfo.citation`: a :obj:`str` containing the citation for the dataset in a BibTex format for inclusion in communications citing the dataset,
- :attr:`nlp.DatasetInfo.homepage`: a :obj:`str` containing an URL to an original homepage of the dataset.

Here is for instance the :func:`nlp.Dataset._info` for the SQuAD dataset for instance, which is taken from the `squad dataset loading script <https://github.com/huggingface/nlp/tree/master/datasets/squad/squad.py>`__ 

.. code-block::

    def _info(self):
        return nlp.DatasetInfo(
            description=_DESCRIPTION,
            features=nlp.Features(
                {
                    "id": nlp.Value("string"),
                    "title": nlp.Value("string"),
                    "context": nlp.Value("string"),
                    "question": nlp.Value("string"),
                    "answers": nlp.features.Sequence(
                        {"text": nlp.Value("string"), "answer_start": nlp.Value("int32"),}
                    ),
                }
            ),
            # No default supervised_keys (as we have to pass both question
            # and context as input).
            supervised_keys=None,
            homepage="https://rajpurkar.github.io/SQuAD-explorer/",
            citation=_CITATION,
        )


The :class:`nlp.Features` define the structure for each examples and can define arbitrary nested objects with fields of various types.

More details on the available ``features`` can be found in the guide on features :doc:`features` and in the package reference on :class:`nlp.Features`.

Many examples of features can also be found in the various `dataset scripts provided on the GitHub repository <https://github.com/huggingface/nlp/tree/master/datasets>`__ and even directly inspected on the `🤗nlp viewer <https://huggingface.co/nlp/viewer>`__.

Here are the features of the SQuAD dataset for instance, which is taken from the `squad dataset loading script <https://github.com/huggingface/nlp/tree/master/datasets/squad/squad.py>`__:

.. code-block::

	nlp.Features(
                {
					"id": nlp.Value("string"),
					"title": nlp.Value("string"),
					"context": nlp.Value("string"),
					"question": nlp.Value("string"),
					"answers": nlp.Sequence(
						{"text": nlp.Value("string"),
						"answer_start": nlp.Value("int32"),
						}
					),
                }
            )

These features should be mostly self-explanatory given the above introduction. One specific behavior here is the fact that the ``Sequence`` field in ``"answers"`` is given a dictionary of sub-fields. As mentioned in the above note, in this case, this feature is actually **converted in a dictionary of lists** (instead of the list of dictionary that we read in the feature here).

We can see a confirmation of that in the structure of the examples yield by the generation method at the very end of the `squad dataset loading script <https://github.com/huggingface/nlp/tree/master/datasets/squad/squad.py>`__:

.. code-block::

	answer_starts = [answer["answer_start"] for answer in qa["answers"]]
	answers = [answer["text"].strip() for answer in qa["answers"]]

	yield id_, {
		"title": title,
		"context": context,
		"question": question,
		"id": id_,
		"answers": {"answer_start": answer_starts, "text": answers,},
	}

Here the ``"answers"`` is accordingly provided with a dictionary of lists and not a list of dictionary.

Let's take another example of features from the `large-scale reading comprehension dataset Race <https://huggingface.co/datasets/race>`__:

.. code-block::

	features=nlp.Features(
		{
			"article": nlp.Value("string"),
			"answer": nlp.Value("string"),
			"question": nlp.Value("string"),
			"options": nlp.features.Sequence({"option": nlp.Value("string")})
		}
	)

Here is the corresponding first examples in the dataset:

.. code-block::

	>>> from nlp import load_dataset
	>>> dataset = load_dataset('race', split='train')
	>>> dataset[0]
	{'article': 'My husband is a born shopper. He loves to look at things and to touch them. He likes to compare prices between the same items in different shops. He would never think of buying anything without looking around in several
	 ...
	 sadder. When he saw me he said, "I\'m sorry, Mum. I have forgotten to buy oranges and the meat. I only remembered to buy six eggs, but I\'ve dropped three of them."', 
	 'answer': 'C',
	 'question': 'The husband likes shopping because   _  .',
	 'options': {
		'option':['he has much money.',
				  'he likes the shops.',
				  'he likes to compare the prices between the same items.',
				  'he has nothing to do but shopping.'
				]
		}
	}


Downloading data files and organizing splits
-------------------------------------------------

The :func:`nlp.DatasetBuilder._split_generator` method is in charge of downloading (or retrieving locally the data files), organizing them according to the splits and defining specific arguments for the generation process if needed.

This method **takes as input** a :class:`nlp.DownloadManager` which is a utility which can be used to download files (or to retreive them from the local filesystem if they are local files or are already in the cache) and return a list of :class:`nlp.SplitGenerator`. A :class:`nlp.SplitGenerator` is a simple dataclass containing the name of the split and keywords arguments to be provided to the :func:`nlp.DatasetBuilder._generate_examples` method that we detail in the next section. These arguments can be specific to each splits and typically comprise at least the local path to the data files to load for each split.

.. note::

	**Using local data files** Two attributes of :class:`nlp.BuilderConfig` are specifically provided to store paths to local data files if your dataset is not online but constituted by local data files. These two attributes are :obj:`data_dir` and :obj:`data_files` and can be freely used to provide a directory path or file paths. These two attributes can be set when calling :func:`nlp.load_dataset` using the associated keyword arguments, e.g. ``dataset = nlp.load_dataset('my_script', data_files='my_local_data_file.csv')`` and the values can be used in :func:`nlp.DatasetBuilder._split_generator` by accessing ``self.config.data_dir`` and ``self.config.data_files``. See the `text file loading script <https://github.com/huggingface/nlp/blob/master/datasets/text/text.py>`__ for a simple example using :attr:`nlp.BuilderConfig.data_files`.

Let's have a look at a simple example of a :func:`nlp.DatasetBuilder._split_generator` method. We'll take the example of the `squad dataset loading script <https://github.com/huggingface/nlp/tree/master/datasets/squad/squad.py>`__:

.. code-block::

	class Squad(nlp.GeneratorBasedBuilder):
		"""SQUAD: The Stanford Question Answering Dataset. Version 1.1."""

		_URL = "https://rajpurkar.github.io/SQuAD-explorer/dataset/"
		_DEV_FILE = "dev-v1.1.json"
		_TRAINING_FILE = "train-v1.1.json"

		def _split_generators(self, dl_manager: nlp.DownloadManager) -> List[nlp.SplitGenerator]:
			urls_to_download = {
				"train": os.path.join(self._URL, self._TRAINING_FILE),
				"dev": os.path.join(self._URL, self._DEV_FILE),
			}
			downloaded_files = dl_manager.download_and_extract(urls_to_download)

			return [
				nlp.SplitGenerator(name=nlp.Split.TRAIN, gen_kwargs={"filepath": downloaded_files["train"]}),
				nlp.SplitGenerator(name=nlp.Split.VALIDATION, gen_kwargs={"filepath": downloaded_files["dev"]}),
			]

As you can see this method first prepare a dict of URL to the original data files for SQuAD. This dict is then provided to the :func:`nlp.DownloadManager.download_and_extract` method which will take care of downloading or retriving from the local file system these files and returning a object of the same type and organization (here a dictionary) with the path to the local version of the requetsed files. :func:`nlp.DownloadManager.download_and_extract` can take as input a single URL/path or a list or dictionary of URLs/paths and will return an object of the same structure (single URL/path, list or dictionary of URLs/paths) with the path to the local files.

This method also takes care of extracting compressed tar, gzip and zip archives.

:func:`nlp.DownloadManager.download_and_extract` can download files from a large set of origins but if your data files are hosted on a special access server, it's also possible to provide a callable which will take care of the downloading process to the ``DownloadManager`` using :func:`nlp.DownloadManager.download_custom`.

.. note::

	In addition to :func:`nlp.DownloadManager.download_and_extract` and :func:`nlp.DownloadManager.download_custom`, the :class:`nlp.DownloadManager` class also provide more fine-grained control on the download and extraction process through several methods including: :func:`nlp.DownloadManager.download`, :func:`nlp.DownloadManager.extract` and :func:`nlp.DownloadManager.iter_archive`. Please refere to the package reference on :class:`nlp.DownloadManager` for details on these methods.

Once the data files are downloaded, the next mission for the :func:`nlp.DatasetBuilder._split_generator` method is to prepare the :class:`nlp.SplitGenerator` for each split which will be used to call the :func:`nlp.DatasetBuilder._generate_examples` method that we detail in the next session.

A :class:`nlp.SplitGenerator` is a simple dataclass containing:

- :obj:`name` (``string``) : the **name** of a split, when possible, standard split names provided in :class:`nlp.Split` can be used: :obj:`nlp.Split.TRAIN`, :obj:`nlp.Split.VALIDATION` and :obj:`nlp.Split.TEST`,
- :obj:`gen_kwargs` (``dict``): **keywords arguments** to be provided to the :func:`nlp.DatasetBuilder._generate_examples` method to generate the samples in this split. These arguments can be specific to each splits and typically comprise at least the local path to the data files to load for each split as indicated in the above SQuAD example.


Generating the samples in each split
-------------------------------------------------

The :func:`nlp.DatasetBuilder._generate_examples` is in charge of reading the data files for a split and yielding examples with the format specified in the ``features`` set in :func:`nlp.DatasetBuilder._info`.

The input arguments of :func:`nlp.DatasetBuilder._generate_examples` are defined by the :obj:`gen_kwargs` dictionary returned by the :func:`nlp.DatasetBuilder._split_generator` method we detailed above.

Here again, let's take the simple example of the `squad dataset loading script <https://github.com/huggingface/nlp/tree/master/datasets/squad/squad.py>`__:

.. code-block::

    def _generate_examples(self, filepath):
        """This function returns the examples in the raw (text) form."""
        logging.info("generating examples from = %s", filepath)
        with open(filepath) as f:
            squad = json.load(f)
            for article in squad["data"]:
                title = article.get("title", "").strip()
                for paragraph in article["paragraphs"]:
                    context = paragraph["context"].strip()
                    for qa in paragraph["qas"]:
                        question = qa["question"].strip()
                        id_ = qa["id"]

                        answer_starts = [answer["answer_start"] for answer in qa["answers"]]
                        answers = [answer["text"].strip() for answer in qa["answers"]]

                        # Features currently used are "context", "question", and "answers".
                        # Others are extracted here for the ease of future expansions.
                        yield id_, {
                            "title": title,
                            "context": context,
                            "question": question,
                            "id": id_,
                            "answers": {"answer_start": answer_starts, "text": answers,},
                        }

The input argument is the ``filepath`` provided in the :obj:`gen_kwargs` of each :class:`nlp.SplitGenerator` returned by the :func:`nlp.DatasetBuilder._split_generator` method.

The method read and parse the inputs files and yield a tuple constituted of an ``id_`` (can be arbitrary be should be unique (for backward compatibility with TensorFlow dataset) and an example.

The example is a dictionary with the same structure and element types as the ``features`` defined in :func:`nlp.DatasetBuilder._info`.

Specifying several dataset configurations
-------------------------------------------------

Sometimes you want to provide access to several sub-sets of your dataset, for instance if your dataset comprise several languages or is constituted of various sub-sets or if you want to provide several ways to structure examples.

This is possible by defining a specific :class:`nlp.BuilderConfig` class and providing predefined instances of this class for the user to select from.

The base :class:`nlp.BuilderConfig` class is very simple and only comprises the following attributes:

- :obj:`name` (``str``) is the name of the dataset configuration, for instance the language name if the various configurations are specific to various languages
- :obj:`version` an optional version identifier
- :obj:`data_dir` (``str``) can be used to store the path to a local folder containing data files
- :obj:`data_files` (``Union[Dict, List]`` can be used to store paths to a local data files
- :obj:`description` (``str``) can be used to give a long description of the configuration

:class:`nlp.BuilderConfig` is only used as a containiner of informations which can be used in the :class:`nlp.DatasetBuilder` to build the dataset by being access in the ``self.config`` attribute of the :class:`nlp.DatasetBuilder` instance.

You can sub-class the base :class:`nlp.BuilderConfig` class to add additional attributes that you may wan to use to control the generation of a dataset. The specific configuration class that will be used by the dataset is set in the :attr:`nlp.DatasetBuilder.BUILDER_CONFIG_CLASS`.

There are two ways to populate the attributes of a :class:`nlp.BuilderConfig` class or sub-class:
- a list of predefined :class:`nlp.BuilderConfig` class or sub-class can be set in the :attr:`nlp.DatasetBuilder.BUILDER_CONFIGS` attribute of the dataset. Each specific configuration can then be selected by giving it's ``name`` as ``name`` keyword to :func:`nlp.load_dataset`,
- when calling :func:`nlp.load_dataset`, all the keyword arguments which are not specific to the :func:`nlp.load_dataset` method will be used to set the associated attributes of the :class:`nlp.BuilderConfig` class and overide the predefined attributes if a specific configuration was selected.

Let's take an example adapted from the `CSV files loading script <https://github.com/huggingface/nlp/blob/master/datasets/csv/csv.py>`__.

Let's say we would like two simple ways to load CSV files: using ``','`` as a delimiter (we will call this configuration ``'comma'``) or using ``';'`` as a delimiter (we will call this configuration ``'semi-colon'``).

We can define a custom configuration with a ``delimiter`` attributes:

.. code-block::

	@dataclass
	class CsvConfig(nlp.BuilderConfig):
		"""BuilderConfig for CSV."""
		delimiter: str = None

And then define several predefined configurations in the DatasetBuilder:

.. code-block::

	class Csv(nlp.ArrowBasedBuilder):
		BUILDER_CONFIG_CLASS = CsvConfig
		BUILDER_CONFIGS = [CsvConfig(name='comma',
									 description="Load CSV using ',' as a delimiter",
									 delimiter=','),
						   CsvConfig(name='semi-colon',
									 description="Load CSV using a semi-colon as a delimiter",
									 delimiter=';')]
		
		...

		def self._generate_examples(file):
			with open(file) as csvfile:
				data = csv.reader(csvfile, delimiter = self.config.delimiter)
				for i, row in enumerate(data):
					yield i, row

Here we can see how reading the CSV file can be controled using the ``self.config.delimiter`` attribute.

The users of our dataset loading script will be able to select one or the other way to load the CSV files with the configuration names or even a totally different way by setting the ``delimiter`` attrbitute directly. For instance using commands like this:

.. code-block::

	>>> from nlp import load_dataset
	>>> dataset = load_dataset('my_csv_loading_script', name='comma', data_files='my_file.csv')
	>>> dataset = load_dataset('my_csv_loading_script', name='semi-colon', data_files='my_file.csv')
	>>> dataset = load_dataset('my_csv_loading_script', name='comma', delimiter='\t', data_files='my_file.csv')

In the last case, the delimiter set by the configuration will be overiden by the delimiter given as argument to ``load_dataset``.

While the configuration attributes are used in this case to controle the reading/parsing of the data files, the configuration attributes can be used at any stage of the processing and in particulare:

- to control the :class:`nlp.DatasetInfo` attributes set in the :func:`nlp.DatasetBuilder._info` method, for instances the ``features``,
- to control the files downloaded in the :func:`nlp.DatasetBuilder._split_generator` method, for instance to select different URLs depending on a ``language`` attribute defined by the configuration,
- etc

An example of a custom configuration class with several predefined configurations can be found in the `Super-GLUE loading script <https://github.com/huggingface/nlp/blob/master/datasets/super_glue/super_glue.py>`__ which provide control over the various sub-dataset of the SuperGLUE benchmark through the conigurations.

Another example is the `Wikipedia loading script <https://github.com/huggingface/nlp/blob/master/datasets/wikipedia/wikipedia.py>`__ which provide control over the language of the Wikipedia dataset through the conigurations.


Testing the dataset loading script
-------------------------------------------------

Once you've finished with creating or adapting a dataset loading script, you can try it locally by giving the path to the dataset loading script:

.. code-block::

	>>> from nlp import load_dataset
	>>> dataset = load_dataset('PATH/TO/MY/SCRIPT.py')

If your dataset has several configurations or requires to be given the path to local data files, you can use the arguments of :func:`nlp.load_dataset` accordingly:

.. code-block::

	>>> from nlp import load_dataset
	>>> dataset = load_dataset('PATH/TO/MY/SCRIPT.py', 'my_configuration', data_files={'train': 'my_train_file.txt', 'validation': 'my_validation_file.txt'})


