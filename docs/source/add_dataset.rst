Writing your own dataset loading script
=============================================

There are two main reasons you may want to write your own dataset loading script: either you want to use local/private data files and the generic dataloader for CSV/JSON are not suitable for your usage (cf. :ref:`_loading-from-local-files`), or you would like to share a new dataset with the community, for instance with the `HuggingFace Hub <https://huggingface.co/datasets>`__.

In these cases you will need to understand how datasets are loaded and how you can write or adapt a dataset loading script. This is the purpose of this chapter.

Here a quick general overview of the classes, attributes and method involved:

.. image:: /imgs/nlp_doc.jpg

On the left is the general organization inside the library to create a :class:`nlp.Dataset` instance and on the right, the elements which are specific to each dataset loading script.

To create a new dataset loading script one mostly need to specify three methods in a :class:`nlp.DatasetBuilder` class:

- :func:`nlp.DatasetBuilder._info` which is in charge of specifying the dataset metadata as a :obj:`nlp.DatasetInfo` dataclass and in particular the :class:`nlp.Features` which defined the names and types of each column in the dataset,
- :func:`nlp.DatasetBuilder._split_generator` which is in charge of downloading or retrieving the data files, organizing them by splits and defining specific arguments for the generation process if needed,
- :func:`nlp.DatasetBuilder._generate_examples` which is in charge of loading the files for a split and yielding examples with the format specified in the ``features``.

Optionally, the dataset loading script can define a configuration to be used by the :class:`nlp.DatasetBuilder` by inheriting from :class:`nlp.BuilderConfig`. Such a class allows to customize the building process, for instance by allowing to select specific subsets of the data or specific ways to process the data when loading the dataset.

.. note::

	Note on naming: the dataset class should be camel case, while the dataset name is its snake case equivalent (ex: :obj:`class BookCorpus(nlp.GeneratorBasedBuilder)` for the dataset ``book_corpus``).


Populating the Dataset metadata
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

Let's spend some time diving in the ``features``.

The dataset features
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

:class:`nlp.Features` define the internal structure and typings for each example in the dataset. Features are used to specify the underlying serailization format but also contain high-level informations regarding the fields, e.g. conversion methods from names to integer values for a class label field.

Here is a brief presentation of the various types of features which can be used to define the dataset fields (aka columns):

- :class:`nlp.Features` is the base class and should be only called once and instantiated with a dictionnary of field names and field sub-features as detailed in the rest of this list,
- a python :obj:`dict` specifies that the field is a nested field containing a mapping of sub-fields to sub-fields features. It's possible to have nested fields of nested fields in an arbitrary manner.
- a python :obj:`list` or a :class:`nlp.Sequence` specifies that the field contains a list of objects. The python :obj:`list` or :class:`nlp.Sequence` should be provided with a single sub-feature as an example of the feature type hosted in this list. Python :obj:`list` are simplest to define and write while :class:`nlp.Sequence` provide a few more specific behaviors like the possibility to specify a fixed length for the list (slightly more efficient).

.. note::

	A :class:`nlp.Sequence` with a internal dictionnary feature will be automatically converted in a dictionnary of lists. This behavior is implemented to have a compatilbity layer with the TensorFlow Datasets library but may be un-wanted in some cases. If you don't want this behavior, you can use a python :obj:`list` instead of the :class:`nlp.Sequence`.

- a :class:`nlp.ClassLabel` feature specifies a field with a predefined set of classes which can have labels associated to them and will be stored as integers in the dataset. This field will be stored and retrieved as an integer value and two conversion methodes, :func:`nlp.ClassLabel.str2int` and :func:`nlp.ClassLabel.int2str` can be used to convert from the label names to the associate integer value and vice-versa.

- a :class:`nlp.Value` feature specifies a single typed value, e.g. ``int64`` or ``string``. The types supported are all the `non-nested types of Apache Arrow <https://arrow.apache.org/docs/python/api/datatypes.html#factory-functions>`__ among which the most commonly used ones are ``int64``, ``float32`` and ``string``.
- :class:`nlp.Tensor` is mostly supported to have a compatibility layer with the TensorFlow Datasets library and can host a 0D or 1D array. A 0D array is equivalent to a :class:`nlp.Value` of the same dtype while a 1D array is equivalent to a :class:`nlp.Sequence` of the same dtype and fixed length.
- eventually, two features are specific to Machine Translation: :class:`nlp.Translation` and :class:`nlp.TranslationVariableLanguages`. We refere to the package reference for more details on these features.

Many examples of features can be found in the various `dataset scripts provided on the GitHub repository <https://github.com/huggingface/nlp/tree/master/datasets>`__ and even directly inspected on the `🤗nlp viewer <https://huggingface.co/nlp/viewer>`__.

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

These features should be mostly self-explanatory given the above introduction. One specific behavior here is the fact that the ``Sequence`` field in ``"answers"`` is given a dictionnary of sub-fields. As mentioned in the above note, in this case, this feature is actually **converted in a dictionnary of lists** (instead of the list of dictionnary that we read in the feature here).

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

Here the ``"answers"`` is accordingly provided with a dictionnary of lists and not a list of dictionnary.

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


Downloading the files and organizing splits
-------------------------------------------------

The :func:`nlp.DatasetBuilder._split_generator` method is in charge of downloading (or retrieving locally the data files), organizing them according to the splits and defining specific arguments for the generation process if needed.

This method will typically:
1. first download all the files depending on the builder configuration in ``self.config`` if the configuration is used to select sub-sets of the dataset, and
2. instantiate a list of splits defined by :class:`nlp.SplitGenerator` objects.

A simple example can be found in the `squad dataset loading script <https://github.com/huggingface/nlp/tree/master/datasets/squad/squad.py>`__: 

.. code-block::

    def _split_generators(self, dl_manager):
        urls_to_download = {
            "train": os.path.join(self._URL, self._TRAINING_FILE),
            "dev": os.path.join(self._URL, self._DEV_FILE),
        }
        downloaded_files = dl_manager.download_and_extract(urls_to_download)

        return [
            nlp.SplitGenerator(name=nlp.Split.TRAIN, gen_kwargs={"filepath": downloaded_files["train"]}),
            nlp.SplitGenerator(name=nlp.Split.VALIDATION, gen_kwargs={"filepath": downloaded_files["dev"]}),
        ]


The ``dl_manager`` is an instance of :class:`nlp.DownloadManager`




Adding dummy test data
----------------------------

3. **Make sure you run all of the following commands from the root of your `nlp` git clone.**. To check that your dataset works correctly and to create its `dataset_infos.json` file run the command:

::

	python nlp-cli test datasets/<your-dataset-folder> --save_infos --all_configs

4. If the command was succesful, you should now create some dummy data. Use the following command to get in-detail instructions on how to create the dummy data:

::

	python nlp-cli dummy_data datasets/<your-dataset-folder> 


5. Now test that both the real data and the dummy data work correctly using the following commands:

*For the real data*:
::

	RUN_SLOW=1 pytest tests/test_dataset_common.py::LocalDatasetTest::test_load_real_dataset_<your-dataset-name>

	and 

*For the dummy data*:
::

	RUN_SLOW=1 pytest tests/test_dataset_common.py::LocalDatasetTest::test_load_dataset_all_configs_<your-dataset-name>


6. If all tests pass, your dataset works correctly. Awesome! You can now follow steps 6, 7 and 8 of the section *How to contribute to nlp?*. If you experience problems with the dummy data tests, you might want to take a look at the section *Help for dummy data tests* below.


Follow these steps in case the dummy data test keeps failing:

- Verify that all filenames are spelled correctly. Rerun the command 
	::

		python nlp-cli dummy_data datasets/<your-dataset-folder> 

	and make sure you follow the exact instructions provided by the command of step 5). 

- Your datascript might require a difficult dummy data structure. In this case make sure you fully understand the data folder logit created by the function `_split_generations(...)` and expected by the function `_generate_examples(...)` of your dataset script. Also take a look at `tests/README.md` which lists different possible cases of how the dummy data should be created.

- If the dummy data tests still fail, open a PR in the repo anyways and make a remark in the description that you need help creating the dummy data.

