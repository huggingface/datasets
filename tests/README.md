## Add Dummy data test

**Important** In order to pass the `load_dataset_<dataset_name>` test, dummy data is required for all possible config names.

First we distinguish between datasets scripts that
- A) have no config class and
- B) have a config class

For A) the dummy data folder structure, will always look as follows:
- ``dummy/<version>/dummy_data.zip``,  *e.g.* ``cosmos_qa/dummy/0.1.0/dummy_data.zip``.
For B) the dummy data folder structure, will always look as follows:
- ``dummy/<config_name>/<version>/dummy_data.zip``, *e.g.* ``squad/dummy/plain-text/1.0.0/dummy_data.zip``.


Now the difficult part is to create the correct `dummy_data.zip` file.

**Important** When checking the dummy folder structure of already added datasets, always unzip ``dummy_data.zip``. If a folder ``dummy_data`` is found next to ``dummy_data.zip``, it is probably an old version and should be deleted. The tests only take the ``dummy_data.zip`` file into account.

Here we have to pay close attention to the ``_split_generators(self, dl_manager)`` function of the dataset script in question.
There are three general possibilties:

1) The ``dl_manager.download_and_extract()`` is given a **single path variable** of type `str` as its argument. In this case the file `dummy_data.zip` should unzip to the following structure:
``os.path.join("dummy_data", <additional-paths-as-defined-in-split-generations>)`` *e.g.* for ``sentiment140``, the unzipped ``dummy_data.zip`` has the following dir structure ``dummy_data/testdata.manual.2009.06.14.csv`` and ``dummy_data/training.1600000.processed.noemoticon.csv``.

**Note** if there are no ``<additional-paths-as-defined-in-split-generations>``, then ``dummy_data`` should be the name of the single file. An example for this is the ``crime-and-punishment`` dataset script.

2) The ``dl_manager.download_and_extract()`` is given a **dictionary of paths** of type `str` as its argument. In this case the file `dummy_data.zip` should unzip to the following structure:
``os.path.join("dummy_data", <value_of_dict>.split('/')[-1], <additional-paths-as-defined-in-split-generations>)`` *e.g.* for ``squad``, the unzipped ``dummy_data.zip`` has the following dir structure ``dummy_data/dev-v1.1.json``, etc...

**Note** if ``<value_of_dict>`` is a zipped file then the dummy data folder structure should contain the exact name of the zipped file and the following extracted folder structure. The file `dummy_data.zip` should **never** itself contain a zipped file since the dummy data is not unzipped by the ``MockDownloadManager`` during testing. *E.g.* check the dummy folder structure of ``hansards`` where the folders have to be named ``*.tar`` or the structure of ``wiki_split`` where the folders have to be named ``*.zip``.

3) The ``dl_manager.download_and_extract()`` is given a **dictionary of lists of paths** of type `str` as its argument. This is a very special case and has been seen only for the dataset ``ensli``. In this case the values are simply flattened and the dummy folder structure is the same as in 2).
