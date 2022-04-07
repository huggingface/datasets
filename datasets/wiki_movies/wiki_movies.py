# coding=utf-8
# Copyright 2020 The HuggingFace Datasets Authors and the current dataset script contributor.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""WikiMovies: A Question-Answering dataset that contains raw text alongside a preprocessed knowledge base, in the domain of movies from the Open Movie Database. It is the QA part of the Movie Dialog dataset.
It was built with the following goals in mind: (i) machine learning techniques should have ample training examples for learning; and (ii) one can analyze easily the performance of different representations of knowledge and break down the results by question type. The dataset can be downloaded fromhttp://fb.ai/babi
"""


import datasets


_CITATION = """\
@misc{miller2016keyvalue,
      title={Key-Value Memory Networks for Directly Reading Documents},
      author={Alexander Miller and Adam Fisch and Jesse Dodge and Amir-Hossein Karimi and Antoine Bordes and Jason Weston},
      year={2016},
      eprint={1606.03126},
      archivePrefix={arXiv},
      primaryClass={cs.CL}
}"""

_DESCRIPTION = """\
The WikiMovies dataset consists of roughly 100k (templated) questions over 75k entities based on questions with answers in the open movie database (OMDb).
"""

_HOMEPAGE = "https://research.fb.com/downloads/babi/"

_LICENSE = "Creative Commons Public License (CCPL)"

# TODO: Add link to the official dataset URLs here
# The HuggingFace dataset library don't host the datasets but only point to the original files
# This can be an arbitrary nested dict/list of URLs (see below in `_split_generators` method)
_URLs = {"default": "https://thespermwhale.com/jaseweston/babi/movieqa.tar.gz"}


class WikiMovies(datasets.GeneratorBasedBuilder):
    """The WikiMovies dataset consists of roughly 100k (templated) questions over 75k entities based on questions with answers in the open movie database (OMDb)."""

    VERSION = datasets.Version("1.1.0")

    def _info(self):
        features = datasets.Features(
            {
                "question": datasets.Value("string"),
                "answer": datasets.Value("string"),
                # These are the features of your dataset like images, labels ...
            }
        )
        return datasets.DatasetInfo(
            # This is the description that will appear on the datasets page.
            description=_DESCRIPTION,
            # This defines the different columns of the dataset and their types
            features=features,  # Here we define them above because they are different between the two configurations
            # If there's a common (input, target) tuple from the features,
            # specify them here. They'll be used if as_supervised=True in
            # builder.as_dataset.
            supervised_keys=None,
            # Homepage of the dataset for documentation
            homepage=_HOMEPAGE,
            # License for the dataset if available
            license=_LICENSE,
            # Citation for the dataset
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        """Returns SplitGenerators."""
        # TODO: This method is tasked with downloading/extracting the data and defining the splits depending on the configuration
        # If several configurations are possible (listed in BUILDER_CONFIGS), the configuration selected by the user is in self.config.name

        # dl_manager is a datasets.download.DownloadManager that can be used to download and extract URLs
        # It can accept any type or nested list/dict and will give back the same structure with the url replaced with path to local files.
        # By default the archives will be extracted and a path to a cached folder where they are extracted is returned instead of the archive
        my_urls = _URLs[self.config.name]
        archive = dl_manager.download(my_urls)
        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={
                    "filepath": "/".join(["movieqa", "questions", "wiki_entities", "wiki-entities_qa_train.txt"]),
                    "files": dl_manager.iter_archive(archive),
                },
            ),
            datasets.SplitGenerator(
                name=datasets.Split.TEST,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={
                    "filepath": "/".join(["movieqa", "questions", "wiki_entities", "wiki-entities_qa_test.txt"]),
                    "files": dl_manager.iter_archive(archive),
                },
            ),
            datasets.SplitGenerator(
                name=datasets.Split.VALIDATION,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={
                    "filepath": "/".join(["movieqa", "questions", "wiki_entities", "wiki-entities_qa_dev.txt"]),
                    "files": dl_manager.iter_archive(archive),
                },
            ),
        ]

    def _generate_examples(self, filepath, files):
        # It is in charge of opening the given file and yielding (key, example) tuples from the dataset
        # The key is not important, it's more here for legacy reason (legacy from tfds)

        for path, f in files:
            if path == filepath:
                for id_, row in enumerate(f):
                    tmp_data = row.decode("utf-8").split("\t")
                    tmp_question = tmp_data[0][1:]
                    yield id_, {
                        "question": tmp_question,
                        "answer": tmp_data[1],
                    }
                break
