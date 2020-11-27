"""TODO(boolq): Add a description here."""

from __future__ import absolute_import, division, print_function

import json

import datasets


# TODO(boolq): BibTeX citation
_CITATION = """\
@inproceedings{clark2019boolq,
  title =     {BoolQ: Exploring the Surprising Difficulty of Natural Yes/No Questions},
  author =    {Clark, Christopher and Lee, Kenton and Chang, Ming-Wei, and Kwiatkowski, Tom and Collins, Michael, and Toutanova, Kristina},
  booktitle = {NAACL},
  year =      {2019},
}
"""

# TODO(boolq):
_DESCRIPTION = """\
BoolQ is a question answering dataset for yes/no questions containing 15942 examples. These questions are naturally
occurring ---they are generated in unprompted and unconstrained settings.
Each example is a triplet of (question, passage, answer), with the title of the page as optional additional context.
The text-pair classification setup is similar to existing natural language inference tasks.
"""

_URL = "https://storage.googleapis.com/boolq/"
_URLS = {
    "train": _URL + "train.jsonl",
    "dev": _URL + "dev.jsonl",
}


class Boolq(datasets.GeneratorBasedBuilder):
    """TODO(boolq): Short description of my dataset."""

    # TODO(boolq): Set up version.
    VERSION = datasets.Version("0.1.0")

    def _info(self):
        # TODO(boolq): Specifies the datasets.DatasetInfo object
        return datasets.DatasetInfo(
            # This is the description that will appear on the datasets page.
            description=_DESCRIPTION,
            # datasets.features.FeatureConnectors
            features=datasets.Features(
                {
                    "question": datasets.Value("string"),
                    "answer": datasets.Value("bool"),
                    "passage": datasets.Value("string")
                    # These are the features of your dataset like images, labels ...
                }
            ),
            # If there's a common (input, target) tuple from the features,
            # specify them here. They'll be used if as_supervised=True in
            # builder.as_dataset.
            supervised_keys=None,
            # Homepage of the dataset for documentation
            homepage="https://github.com/google-research-datasets/boolean-questions",
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        """Returns SplitGenerators."""
        # TODO(boolq): Downloads the data and defines the splits
        # dl_manager is a datasets.download.DownloadManager that can be used to
        # download and extract URLs
        urls_to_download = _URLS
        downloaded_files = dl_manager.download(urls_to_download)

        return [
            datasets.SplitGenerator(name=datasets.Split.TRAIN, gen_kwargs={"filepath": downloaded_files["train"]}),
            datasets.SplitGenerator(
                name=datasets.Split.VALIDATION,
                gen_kwargs={"filepath": downloaded_files["dev"]},
            ),
        ]

    def _generate_examples(self, filepath):
        """Yields examples."""
        # TODO(boolq): Yields (key, example) tuples from the dataset
        with open(filepath, encoding="utf-8") as f:
            for id_, row in enumerate(f):
                data = json.loads(row)
                question = data["question"]
                answer = data["answer"]
                passage = data["passage"]
                yield id_, {"question": question, "answer": answer, "passage": passage}
