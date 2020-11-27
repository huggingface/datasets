"""TODO(wiki_split): Add a description here."""

from __future__ import absolute_import, division, print_function

import csv
import os

import datasets


# TODO(wiki_split): BibTeX citation
_CITATION = """\
@InProceedings{BothaEtAl2018,
  title = {{Learning To Split and Rephrase From Wikipedia Edit History}},
  author = {Botha, Jan A and Faruqui, Manaal and Alex, John and Baldridge, Jason and Das, Dipanjan},
  booktitle = {Proceedings of the 2018 Conference on Empirical Methods in Natural Language Processing},
  pages = {to appear},
  note = {arXiv preprint arXiv:1808.09468},
  year = {2018}
}
"""

# TODO(wiki_split):
_DESCRIPTION = """\
One million English sentences, each split into two sentences that together preserve the original meaning, extracted from Wikipedia
Google's WikiSplit dataset was constructed automatically from the publicly available Wikipedia revision history. Although
the dataset contains some inherent noise, it can serve as valuable training data for models that split or merge sentences.
"""

_URL = "https://github.com/google-research-datasets/wiki-split/raw/master/"
_URLS = {
    "train": _URL + "train.tsv.zip",
    "test": _URL + "test.tsv",
    "dev": _URL + "validation.tsv",
}


class WikiSplit(datasets.GeneratorBasedBuilder):
    """TODO(wiki_split): Short description of my dataset."""

    # TODO(wiki_split): Set up version.
    VERSION = datasets.Version("0.1.0")

    def _info(self):
        # TODO(wiki_split): Specifies the datasets.DatasetInfo object
        return datasets.DatasetInfo(
            # This is the description that will appear on the datasets page.
            description=_DESCRIPTION,
            # datasets.features.FeatureConnectors
            features=datasets.Features(
                {
                    "complex_sentence": datasets.Value("string"),
                    "simple_sentence_1": datasets.Value("string"),
                    "simple_sentence_2": datasets.Value("string"),
                    # These are the features of your dataset like images, labels ...
                }
            ),
            # If there's a common (input, target) tuple from the features,
            # specify them here. They'll be used if as_supervised=True in
            # builder.as_dataset.
            supervised_keys=None,
            # Homepage of the dataset for documentation
            homepage="https://dataset-homepage/",
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        """Returns SplitGenerators."""
        # TODO(wiki_split): Downloads the data and defines the splits
        # dl_manager is a datasets.download.DownloadManager that can be used to
        # download and extract URLs
        urls_to_download = _URLS
        dl_dir = dl_manager.download_and_extract(urls_to_download)
        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={"filepath": os.path.join(dl_dir["train"], "train.tsv")},
            ),
            datasets.SplitGenerator(
                name=datasets.Split.TEST,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={"filepath": dl_dir["test"]},
            ),
            datasets.SplitGenerator(
                name=datasets.Split.VALIDATION,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={"filepath": dl_dir["dev"]},
            ),
        ]

    def _generate_examples(self, filepath):
        """Yields examples."""
        # TODO(wiki_split): Yields (key, example) tuples from the dataset
        with open(filepath, encoding="utf-8") as f:
            data = csv.reader(f, delimiter="\t")
            # data = csv.reader(f, delimiter='\t')

            for id_, row in enumerate(data):
                yield id_, {
                    "complex_sentence": row[0],
                    "simple_sentence_1": row[1].split("<::::>")[0],
                    "simple_sentence_2": row[1].split("<::::>")[1],
                }
