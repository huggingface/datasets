"""TODO(com_qa): Add a description here."""

from __future__ import absolute_import, division, print_function

import json

import datasets


# TODO(com_qa): BibTeX citation
_CITATION = """\
@inproceedings{abujabal-etal-2019-comqa,
    title = "{ComQA: A Community-sourced Dataset for Complex Factoid Question Answering with Paraphrase Clusters",
    author = {Abujabal, Abdalghani  and
      Saha Roy, Rishiraj  and
      Yahya, Mohamed  and
      Weikum, Gerhard},
    booktitle = {Proceedings of the 2019 Conference of the North {A}merican Chapter of the Association for Computational Linguistics: Human Language Technologies, Volume 1 (Long and Short Papers)},
    month = {jun},
    year = {2019},
    address = {Minneapolis, Minnesota},
    publisher = {Association for Computational Linguistics},
    url = {https://www.aclweb.org/anthology/N19-1027},
    doi = {10.18653/v1/N19-1027{,
    pages = {307--317},
    }
"""

# TODO(com_qa):
_DESCRIPTION = """\
ComQA is a dataset of 11,214 questions, which were collected from WikiAnswers, a community question answering website.
By collecting questions from such a site we ensure that the information needs are ones of interest to actual users.
Moreover, questions posed there are often cannot be answered by commercial search engines or QA technology, making them
more interesting for driving future research compared to those collected from an engine's query log. The dataset contains
questions with various challenging phenomena such as the need for temporal reasoning, comparison (e.g., comparatives,
superlatives, ordinals), compositionality (multiple, possibly nested, subquestions with multiple entities), and
unanswerable questions (e.g., Who was the first human being on Mars?). Through a large crowdsourcing effort, questions
in ComQA are grouped into 4,834 paraphrase clusters that express the same information need. Each cluster is annotated
with its answer(s). ComQA answers come in the form of Wikipedia entities wherever possible. Wherever the answers are
temporal or measurable quantities, TIMEX3 and the International System of Units (SI) are used for normalization.
"""

_URL = "https://qa.mpi-inf.mpg.de/comqa/"
_URLS = {
    "train": _URL + "comqa_train.json",
    "dev": _URL + "comqa_dev.json",
    "test": _URL + "comqa_test.json",
}


class ComQa(datasets.GeneratorBasedBuilder):
    """TODO(com_qa): Short description of my dataset."""

    # TODO(com_qa): Set up version.
    VERSION = datasets.Version("0.1.0")

    def _info(self):
        # TODO(com_qa): Specifies the datasets.DatasetInfo object
        return datasets.DatasetInfo(
            # This is the description that will appear on the datasets page.
            description=_DESCRIPTION,
            # datasets.features.FeatureConnectors
            features=datasets.Features(
                {
                    "cluster_id": datasets.Value("string"),
                    "questions": datasets.features.Sequence(datasets.Value("string")),
                    "answers": datasets.features.Sequence(datasets.Value("string")),
                    # These are the features of your dataset like images, labels ...
                }
            ),
            # If there's a common (input, target) tuple from the features,
            # specify them here. They'll be used if as_supervised=True in
            # builder.as_dataset.
            supervised_keys=None,
            # Homepage of the dataset for documentation
            homepage="http://qa.mpi-inf.mpg.de/comqa/",
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        """Returns SplitGenerators."""
        # TODO(com_qa): Downloads the data and defines the splits
        # dl_manager is a datasets.download.DownloadManager that can be used to
        # download and extract URLs
        urls_to_download = _URLS
        dl_dir = dl_manager.download_and_extract(urls_to_download)
        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={"filepath": dl_dir["train"], "split": "train"},
            ),
            datasets.SplitGenerator(
                name=datasets.Split.TEST,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={"filepath": dl_dir["test"], "split": "test"},
            ),
            datasets.SplitGenerator(
                name=datasets.Split.VALIDATION,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={"filepath": dl_dir["dev"], "split": "dev"},
            ),
        ]

    def _generate_examples(self, filepath, split):
        """Yields examples."""
        # TODO(com_qa): Yields (key, example) tuples from the dataset
        with open(filepath, encoding="utf-8") as f:
            data = json.load(f)
            for id_, example in enumerate(data):
                questions = []
                if split == "test":
                    cluster_id = str(example["id"])
                    questions.append(example["question"])
                else:
                    cluster_id = example["cluster_id"]
                    questions = example["questions"]
                answers = example["answers"]
                yield id_, {
                    "cluster_id": cluster_id,
                    "questions": questions,
                    "answers": answers,
                }
