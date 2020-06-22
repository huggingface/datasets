"""TODO(cmrc2018): Add a description here."""

from __future__ import absolute_import, division, print_function

import json
import os

import nlp


# TODO(cmrc2018): BibTeX citation
_CITATION = """\
@inproceedings{cui-emnlp2019-cmrc2018,
    title = {A Span-Extraction Dataset for {C}hinese Machine Reading Comprehension},
    author = {Cui, Yiming  and
      Liu, Ting  and
      Che, Wanxiang  and
      Xiao, Li  and
      Chen, Zhipeng  and
      Ma, Wentao  and
      Wang, Shijin  and
      Hu, Guoping},
    booktitle = {Proceedings of the 2019 Conference on Empirical Methods in Natural Language Processing and the 9th International Joint Conference on Natural Language Processing (EMNLP-IJCNLP)},
    month = {nov},
    year = {2019},
    address = {Hong Kong, China},
    publisher = {Association for Computational Linguistics},
    url = {https://www.aclweb.org/anthology/D19-1600},
    doi = {10.18653/v1/D19-1600},
    pages = {5886--5891}}
"""

# TODO(cmrc2018):
_DESCRIPTION = """\
A Span-Extraction dataset for Chinese machine reading comprehension to add language
diversities in this area. The dataset is composed by near 20,000 real questions annotated
on Wikipedia paragraphs by human experts. We also annotated a challenge set which
contains the questions that need comprehensive understanding and multi-sentence
inference throughout the context.
"""
_URL = "https://github.com/ymcui/cmrc2018"
_TRAIN_FILE = "https://worksheets.codalab.org/rest/bundles/0x15022f0c4d3944a599ab27256686b9ac/contents/blob/"
_DEV_FILE = "https://worksheets.codalab.org/rest/bundles/0x72252619f67b4346a85e122049c3eabd/contents/blob/"
_TEST_FILE = "https://worksheets.codalab.org/rest/bundles/0x182c2e71fac94fc2a45cc1a3376879f7/contents/blob/"


class Cmrc2018(nlp.GeneratorBasedBuilder):
    """TODO(cmrc2018): Short description of my dataset."""

    # TODO(cmrc2018): Set up version.
    VERSION = nlp.Version("0.1.0")

    def _info(self):
        # TODO(cmrc2018): Specifies the nlp.DatasetInfo object
        return nlp.DatasetInfo(
            # This is the description that will appear on the datasets page.
            description=_DESCRIPTION,
            # nlp.features.FeatureConnectors
            features=nlp.Features(
                {
                    "id": nlp.Value("string"),
                    "context": nlp.Value("string"),
                    "question": nlp.Value("string"),
                    "answers": nlp.features.Sequence(
                        {"text": nlp.Value("string"), "answer_start": nlp.Value("int32"),}
                    ),
                    # These are the features of your dataset like images, labels ...
                }
            ),
            # If there's a common (input, target) tuple from the features,
            # specify them here. They'll be used if as_supervised=True in
            # builder.as_dataset.
            supervised_keys=None,
            # Homepage of the dataset for documentation
            homepage=_URL,
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        """Returns SplitGenerators."""
        # TODO(cmrc2018): Downloads the data and defines the splits
        # dl_manager is a nlp.download.DownloadManager that can be used to
        # download and extract URLs
        urls_to_download = {"train": _TRAIN_FILE, "dev": _DEV_FILE, "test": _TEST_FILE}
        downloaded_files = dl_manager.download_and_extract(urls_to_download)

        return [
            nlp.SplitGenerator(name=nlp.Split.TRAIN, gen_kwargs={"filepath": downloaded_files["train"]}),
            nlp.SplitGenerator(name=nlp.Split.VALIDATION, gen_kwargs={"filepath": downloaded_files["dev"]}),
            nlp.SplitGenerator(name=nlp.Split.TEST, gen_kwargs={"filepath": downloaded_files["test"]}),
        ]

    def _generate_examples(self, filepath):
        """Yields examples."""
        # TODO(cmrc2018): Yields (key, example) tuples from the dataset
        with open(filepath) as f:
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
                            "answers": {"answer_start": answer_starts, "text": answers,},
                        }
