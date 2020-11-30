"""TODO(squad_it): Add a description here."""

from __future__ import absolute_import, division, print_function

import json

import datasets


# TODO(squad_it): BibTeX citation
_CITATION = """\
@InProceedings{10.1007/978-3-030-03840-3_29,
    author={Croce, Danilo and Zelenanska, Alexandra and Basili, Roberto},
    editor={Ghidini, Chiara and Magnini, Bernardo and Passerini, Andrea and Traverso, Paolo",
    title={Neural Learning for Question Answering in Italian},
    booktitle={AI*IA 2018 -- Advances in Artificial Intelligence},
    year={2018},
    publisher={Springer International Publishing},
    address={Cham},
    pages={389--402},
    isbn={978-3-030-03840-3}
}
"""

# TODO(squad_it):
_DESCRIPTION = """\
SQuAD-it is derived from the SQuAD dataset and it is obtained through semi-automatic translation of the SQuAD dataset
into Italian. It represents a large-scale dataset for open question answering processes on factoid questions in Italian.
 The dataset contains more than 60,000 question/answer pairs derived from the original English dataset. The dataset is
 split into training and test sets to support the replicability of the benchmarking of QA systems:
"""

_URL = "https://github.com/crux82/squad-it/raw/master/"
_URLS = {
    "train": _URL + "SQuAD_it-train.json.gz",
    "test": _URL + "SQuAD_it-test.json.gz",
}


class SquadIt(datasets.GeneratorBasedBuilder):
    """TODO(squad_it): Short description of my dataset."""

    # TODO(squad_it): Set up version.
    VERSION = datasets.Version("0.1.0")

    def _info(self):
        # TODO(squad_it): Specifies the datasets.DatasetInfo object
        return datasets.DatasetInfo(
            # This is the description that will appear on the datasets page.
            description=_DESCRIPTION,
            # datasets.features.FeatureConnectors
            features=datasets.Features(
                {
                    "id": datasets.Value("string"),
                    "context": datasets.Value("string"),
                    "question": datasets.Value("string"),
                    "answers": datasets.features.Sequence(
                        {
                            "text": datasets.Value("string"),
                            "answer_start": datasets.Value("int32"),
                        }
                    ),
                    # These are the features of your dataset like images, labels ...
                }
            ),
            # If there's a common (input, target) tuple from the features,
            # specify them here. They'll be used if as_supervised=True in
            # builder.as_dataset.
            supervised_keys=None,
            # Homepage of the dataset for documentation
            homepage="https://github.com/crux82/squad-it",
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        """Returns SplitGenerators."""
        # TODO(squad_it): Downloads the data and defines the splits
        # dl_manager is a datasets.download.DownloadManager that can be used to
        # download and extract URLs
        urls_to_download = _URLS
        downloaded_files = dl_manager.download_and_extract(urls_to_download)

        return [
            datasets.SplitGenerator(name=datasets.Split.TRAIN, gen_kwargs={"filepath": downloaded_files["train"]}),
            datasets.SplitGenerator(name=datasets.Split.TEST, gen_kwargs={"filepath": downloaded_files["test"]}),
        ]

    def _generate_examples(self, filepath):
        """Yields examples."""
        # TODO(squad_it): Yields (key, example) tuples from the dataset
        with open(filepath, encoding="utf-8") as f:
            data = json.load(f)
            for example in data["data"]:
                for paragraph in example["paragraphs"]:
                    context = paragraph["context"].strip()
                    for qa in paragraph["qas"]:
                        question = qa["question"].strip()
                        id_ = qa["id"]

                        answer_starts = [answer["answer_start"] for answer in qa["answers"]]
                        answers = [answer["text"].strip() for answer in qa["answers"]]

                        yield id_, {
                            "context": context,
                            "question": question,
                            "id": id_,
                            "answers": {
                                "answer_start": answer_starts,
                                "text": answers,
                            },
                        }
