"""TODO(squad_es): Add a description here."""

from __future__ import absolute_import, division, print_function

import json

import datasets


# TODO(squad_es): BibTeX citation
_CITATION = """\
@article{2016arXiv160605250R,
       author = {Casimiro Pio , Carrino and  Marta R. , Costa-jussa and  Jose A. R. , Fonollosa},
        title = "{Automatic Spanish Translation of the SQuAD Dataset for Multilingual
Question Answering}",
      journal = {arXiv e-prints},
         year = 2019,
          eid = {arXiv:1912.05200v1},
        pages = {arXiv:1912.05200v1},
archivePrefix = {arXiv},
       eprint = {1912.05200v2},
}
"""

# TODO(squad_es_v1):
_DESCRIPTION = """\
automatic translation of the Stanford Question Answering Dataset (SQuAD) v2 into Spanish
"""

_URL = "https://raw.githubusercontent.com/ccasimiro88/TranslateAlignRetrieve/master/"
_URLS_V1 = {
    "train": _URL + "SQuAD-es-v1.1/train-v1.1-es.json",
    "dev": _URL + "SQuAD-es-v1.1/dev-v1.1-es.json",
}
_URLS_V2 = {
    "train": _URL + "SQuAD-es-v2.0/train-v2.0-es.json",
    "dev": _URL + "SQuAD-es-v2.0/dev-v2.0-es.json",
}


class SquadEsConfig(datasets.BuilderConfig):
    """BuilderConfig for SQUADEsV2."""

    def __init__(self, **kwargs):
        """BuilderConfig for SQUADEsV2.

        Args:
          **kwargs: keyword arguments forwarded to super.
        """
        super(SquadEsConfig, self).__init__(**kwargs)


class SquadEs(datasets.GeneratorBasedBuilder):
    """TODO(squad_es): Short description of my dataset."""

    # TODO(squad_es): Set up version.
    VERSION = datasets.Version("0.1.0")

    BUILDER_CONFIGS = [
        SquadEsConfig(
            name="v1.1.0",
            version=datasets.Version("1.1.0", ""),
            description="Plain text Spanish squad version 1",
        ),
        SquadEsConfig(
            name="v2.0.0",
            version=datasets.Version("2.0.0", ""),
            description="Plain text Spanish squad version 2",
        ),
    ]

    def _info(self):
        # TODO(squad_es): Specifies the datasets.DatasetInfo object
        return datasets.DatasetInfo(
            # This is the description that will appear on the datasets page.
            description=_DESCRIPTION,
            # datasets.features.FeatureConnectors
            features=datasets.Features(
                {
                    # These are the features of your dataset like images, labels ...
                    "id": datasets.Value("string"),
                    "title": datasets.Value("string"),
                    "context": datasets.Value("string"),
                    "question": datasets.Value("string"),
                    "answers": datasets.features.Sequence(
                        {
                            "text": datasets.Value("string"),
                            "answer_start": datasets.Value("int32"),
                        }
                    ),
                }
            ),
            # If there's a common (input, target) tuple from the features,
            # specify them here. They'll be used if as_supervised=True in
            # builder.as_dataset.
            supervised_keys=None,
            # Homepage of the dataset for documentation
            homepage="https://github.com/ccasimiro88/TranslateAlignRetrieve",
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        """Returns SplitGenerators."""
        # TODO(squad_es): Downloads the data and defines the splits
        # dl_manager is a datasets.download.DownloadManager that can be used to

        # download and extract URLs
        if self.config.name == "v1.1.0":
            dl_dir = dl_manager.download_and_extract(_URLS_V1)
        elif self.config.name == "v2.0.0":
            dl_dir = dl_manager.download_and_extract(_URLS_V2)
        else:
            raise Exception("version does not match any existing one")
        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={"filepath": dl_dir["train"]},
            ),
            datasets.SplitGenerator(
                name=datasets.Split.VALIDATION,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={"filepath": dl_dir["dev"]},
            ),
        ]

    def _generate_examples(self, filepath):
        """Yields examples."""
        # TODO(squad_es): Yields (key, example) tuples from the dataset
        with open(filepath, encoding="utf-8") as f:
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
                            "answers": {
                                "answer_start": answer_starts,
                                "text": answers,
                            },
                        }
