"""TODO(squad_v1_pt): Add a description here."""

from __future__ import absolute_import, division, print_function

import json
import os

import nlp


# TODO(squad_v1_pt): BibTeX citation
_CITATION = """\
@article{2016arXiv160605250R,
       author = {{Rajpurkar}, Pranav and {Zhang}, Jian and {Lopyrev},
                 Konstantin and {Liang}, Percy},
        title = "{SQuAD: 100,000+ Questions for Machine Comprehension of Text}",
      journal = {arXiv e-prints},
         year = 2016,
          eid = {arXiv:1606.05250},
        pages = {arXiv:1606.05250},
archivePrefix = {arXiv},
       eprint = {1606.05250},
}
"""

# TODO(squad_v1_pt):
_DESCRIPTION = """\
Portuguese translation of the SQuAD dataset. The translation was performed automatically using the Google Cloud API.
"""
_URL = "https://github.com/nunorc/squad-v1.1-pt/raw/master"
_TRAIN_FILE = "train-v1.1-pt.json"
_DEV_FILE = "dev-v1.1-pt.json"


class SquadV1Pt(nlp.GeneratorBasedBuilder):
    """TODO(squad_v1_pt): Short description of my dataset."""

    # TODO(squad_v1_pt): Set up version.
    VERSION = nlp.Version("1.1.0")

    def _info(self):
        # TODO(squad_v1_pt): Specifies the nlp.DatasetInfo object
        return nlp.DatasetInfo(
            # This is the description that will appear on the datasets page.
            description=_DESCRIPTION,
            # nlp.features.FeatureConnectors
            features=nlp.Features(
                {
                    "id": nlp.Value("string"),
                    "title": nlp.Value("string"),
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
            homepage="https://github.com/nunorc/squad-v1.1-pt",
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        """Returns SplitGenerators."""
        # TODO(squad_v1_pt): Downloads the data and defines the splits
        # dl_manager is a nlp.download.DownloadManager that can be used to
        # download and extract URLs
        urls_to_download = {"train": os.path.join(_URL, _TRAIN_FILE), "dev": os.path.join(_URL, _DEV_FILE)}
        downloaded_files = dl_manager.download_and_extract(urls_to_download)

        return [
            nlp.SplitGenerator(name=nlp.Split.TRAIN, gen_kwargs={"filepath": downloaded_files["train"]}),
            nlp.SplitGenerator(name=nlp.Split.VALIDATION, gen_kwargs={"filepath": downloaded_files["dev"]}),
        ]

    def _generate_examples(self, filepath):
        """Yields examples."""
        # TODO(squad_v1_pt): Yields (key, example) tuples from the dataset
        with open(filepath) as f:
            data = json.load(f)
            for example in data["data"]:
                title = example.get("title", "").strip()
                for paragraph in example["paragraphs"]:
                    context = paragraph["context"].strip()
                    for qa in paragraph["qas"]:
                        question = qa["question"].strip()
                        id_ = qa["id"]

                        answer_starts = [answer["answer_start"] for answer in qa["answers"]]
                        answers = [answer["text"].strip() for answer in qa["answers"]]

                        yield id_, {
                            "title": title,
                            "context": context,
                            "question": question,
                            "id": id_,
                            "answers": {"answer_start": answer_starts, "text": answers,},
                        }
