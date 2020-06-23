"""TODO(pg19): Add a description here."""

from __future__ import absolute_import, division, print_function

import csv
import json
import os

import tensorflow as tf

import nlp


# TODO(pg19): BibTeX citation
_CITATION = """\
@article{raecompressive2019,
  author = {Rae, Jack W and Potapenko, Anna and Jayakumar, Siddhant M and
            Hillier, Chloe and Lillicrap, Timothy P},
  title = {Compressive Transformers for Long-Range Sequence Modelling},
  journal = {arXiv preprint},
  url = {https://arxiv.org/abs/1911.05507},
  year = {2019},
}

"""

# TODO(pg19):
_DESCRIPTION = """\
This repository contains the PG-19 language modeling benchmark.
It includes a set of books extracted from the Project Gutenberg books library, that were published before 1919.
It also contains metadata of book titles and publication dates.
"""

_ROOT_URL = "gs://deepmind-gutenberg/"
_METADATA_URL = os.path.join(_ROOT_URL, "metadata.csv")


class Pg19(nlp.GeneratorBasedBuilder):
    """TODO(pg19): Short description of my dataset."""

    # TODO(pg19): Set up version.
    VERSION = nlp.Version("0.1.0")

    def _info(self):
        # TODO(pg19): Specifies the nlp.DatasetInfo object
        return nlp.DatasetInfo(
            # This is the description that will appear on the datasets page.
            description=_DESCRIPTION,
            # nlp.features.FeatureConnectors
            features=nlp.Features(
                {
                    "short_book_title": nlp.Value("string"),
                    "publication_date": nlp.Value("int32"),
                    "url": nlp.Value("string"),
                    "text": nlp.Value("string"),
                    # These are the features of your dataset like images, labels ...
                }
            ),
            # If there's a common (input, target) tuple from the features,
            # specify them here. They'll be used if as_supervised=True in
            # builder.as_dataset.
            supervised_keys=None,
            # Homepage of the dataset for documentation
            homepage="https://github.com/deepmind/pg19",
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        """Returns SplitGenerators."""
        # TODO(pg19): Downloads the data and defines the splits
        # dl_manager is a nlp.download.DownloadManager that can be used to
        # download and extract URLs

        def get_filename(path):
            return os.path.splitext(os.path.basename(path))[0]

        def download_listdir(url, local_filepath):
            results = tf.io.gfile.listdir(url)
            with open(local_filepath, "w") as f:
                f.write(json.dumps(results))
            return local_filepath

        def filepath_to_json(path):
            with open(path, "r") as f:
                return json.load(f)

        split_paths = ["train", "validation", "test"]
        full_urls = list(map(lambda url: os.path.join(_ROOT_URL, url), split_paths))
        split_paths = dl_manager.download_custom(dict(zip(split_paths, full_urls)), download_listdir)
        file_urls = list(map(filepath_to_json, split_paths.values()))
        complete_file_urls = [
            list(map(lambda url: os.path.join(_ROOT_URL, split_path, url), urls))
            for (split_path, urls) in zip(split_paths, file_urls)
        ]
        urls_to_download = {(get_filename(url)): url for urls in complete_file_urls for url in urls}

        metadata = dl_manager.download_custom({"metadata": _METADATA_URL}, tf.io.gfile.copy)
        downloaded_files = dl_manager.download_custom(urls_to_download, tf.io.gfile.copy, show_progress=True)

        ids_in_split = list(map(lambda urls: list(map(get_filename, urls)), file_urls))
        split_ids_index = dict(zip(split_paths, ids_in_split))

        return [
            nlp.SplitGenerator(
                name=nlp.Split.TRAIN,
                gen_kwargs={
                    "ids": split_ids_index["train"],
                    "metadata_filepath": metadata["metadata"],
                    "filepaths": downloaded_files,
                },
            ),
            nlp.SplitGenerator(
                name=nlp.Split.VALIDATION,
                gen_kwargs={
                    "ids": split_ids_index["validation"],
                    "metadata_filepath": metadata["metadata"],
                    "filepaths": downloaded_files,
                },
            ),
            nlp.SplitGenerator(
                name=nlp.Split.TEST,
                gen_kwargs={
                    "ids": split_ids_index["test"],
                    "metadata_filepath": metadata["metadata"],
                    "filepaths": downloaded_files,
                },
            ),
        ]

    def _generate_examples(self, ids, metadata_filepath, filepaths):
        """Yields examples."""
        # TODO(pg19): Yields (key, example) tuples from the dataset

        with open(metadata_filepath) as f:
            metadata_dict = csv.DictReader(f, fieldnames=["_id", "short_book_title", "publication_date", "url"])
            indexed_metadata = {row["_id"]: row for row in metadata_dict}

        for _id in ids:
            data = indexed_metadata[_id]
            filepath = filepaths[_id]

            with open(filepath) as f:
                text = f.read()

            _id = data["_id"]
            short_book_title = data["short_book_title"]
            publication_date = int(data["publication_date"])
            url = data["url"]

            yield _id, {
                "short_book_title": short_book_title,
                "publication_date": publication_date,
                "url": url,
                "text": text,
            }
