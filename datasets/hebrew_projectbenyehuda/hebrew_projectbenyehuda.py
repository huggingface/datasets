"""Public domain texts from Project Ben-Yehuda- a set of books extracted from the Project BenYehuda library"""


import csv

import datasets


_CITATION = """\
@article{,
  author = {},
  title = {Public domain texts from Project Ben-Yehuda},
  journal = {},
  url = {https://github.com/projectbenyehuda/public_domain_dump},
  year = {2020},
}

"""

_DESCRIPTION = """\
This repository contains a dump of thousands of public domain works in Hebrew, from Project Ben-Yehuda, in plaintext UTF-8 files, with and without diacritics (nikkud). The metadata (pseudocatalogue.csv) file is a list of titles, authors, genres, and file paths, to help you process the dump.
All these works are in the public domain, so you are free to make any use of them, and do not need to ask for permission.
There are 10078 files, 3181136 lines
"""

_ASSET_ROOT_URL = "https://raw.githubusercontent.com/projectbenyehuda/public_domain_dump/master/"
_STORAGE_API_ROOT_URL = "https://raw.githubusercontent.com/projectbenyehuda/public_domain_dump/master/txt/"

# download one by one file from github is too slow

_METADATA_URL = _ASSET_ROOT_URL + "pseudocatalogue.csv"


class HebrewProjectbenyehuda(datasets.GeneratorBasedBuilder):
    """Project Ben Yehuda dataset - books as plain text extracted from the Project Project Ben Yehuda library"""

    VERSION = datasets.Version("0.1.0")

    def _info(self):
        return datasets.DatasetInfo(
            # This is the description that will appear on the datasets page.
            description=_DESCRIPTION,
            # datasets.features.FeatureConnectors
            features=datasets.Features(
                {
                    "id": datasets.Value("int32"),
                    "url": datasets.Value("string"),
                    "title": datasets.Value("string"),
                    "authors": datasets.Value("string"),
                    "translators": datasets.Value("string"),
                    "original_language": datasets.Value("string"),
                    "genre": datasets.Value("string"),
                    "source_edition": datasets.Value("string"),
                    "text": datasets.Value("string"),
                    # These are the features of your dataset like images, labels ...
                }
            ),
            # If there's a common (input, target) tuple from the features,
            # specify them here. They'll be used if as_supervised=True in
            # builder.as_dataset.
            supervised_keys=None,
            # Homepage of the dataset for documentation
            homepage="https://github.com/projectbenyehuda/public_domain_dump",
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        """Returns SplitGenerators."""

        # dl_manager is a datasets.download.DownloadManager that can be used to
        # download and extract URLs

        metadata = dl_manager.download({"metadata": _METADATA_URL})

        urls_to_download = dict()
        ids = list()
        with open(metadata["metadata"], encoding="utf-8") as csv_file:
            for row in csv.DictReader(csv_file):
                ids.append(row["ID"])
                urls_to_download[row["ID"]] = _STORAGE_API_ROOT_URL + row["path"].strip("/") + ".txt"

        downloaded_files = dl_manager.download(urls_to_download)
        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                gen_kwargs={
                    "ids": ids,
                    "metadata_filepath": metadata["metadata"],
                    "filepaths": downloaded_files,
                },
            )
        ]

    def _generate_examples(self, ids, metadata_filepath, filepaths):
        """Yields examples."""

        with open(metadata_filepath, encoding="utf-8") as f:
            metadata_dict = csv.DictReader(
                f,
                fieldnames=[
                    "_id",
                    "path",
                    "title",
                    "authors",
                    "translators",
                    "original_language",
                    "genre",
                    "source_edition",
                ],
            )
            indexed_metadata = {str(row["_id"]): row for row in metadata_dict}

        for _id in ids:
            data = indexed_metadata[_id]
            filepath = filepaths[_id]

            with open(filepath, encoding="utf-8") as f:
                text = f.read()

            _id = data["_id"]
            title = data["title"]
            url = data["path"].strip("/")
            url = _STORAGE_API_ROOT_URL + url + ".txt"
            authors = data["authors"]
            translators = data["translators"]
            original_language = data["original_language"]
            genre = data["genre"]
            source_edition = data["source_edition"]

            yield _id, {
                "id": _id,
                "title": title,
                "url": url,
                "authors": authors,
                "translators": translators,
                "original_language": original_language,
                "genre": genre,
                "source_edition": source_edition,
                "text": text,
            }
