"""TODO(boolq): Add a description here."""

from __future__ import absolute_import, division, print_function

import json
import os

import tensorflow as tf

import nlp


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

_URL = "gs://boolq"
_TRAIN_FILE_NAME = "train.jsonl"
_DEV_FILE_NAME = "dev.jsonl"


class Boolq(nlp.GeneratorBasedBuilder):
    """TODO(boolq): Short description of my dataset."""

    # TODO(boolq): Set up version.
    VERSION = nlp.Version("0.1.0")

    def _info(self):
        # TODO(boolq): Specifies the nlp.DatasetInfo object
        return nlp.DatasetInfo(
            # This is the description that will appear on the datasets page.
            description=_DESCRIPTION,
            # nlp.features.FeatureConnectors
            features=nlp.Features(
                {
                    "question": nlp.Value("string"),
                    "answer": nlp.Value("bool"),
                    "passage": nlp.Value("string")
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
        # dl_manager is a nlp.download.DownloadManager that can be used to
        # download and extract URLs
        urls_to_download = {
            "train": os.path.join(_URL, _TRAIN_FILE_NAME),
            "dev": os.path.join(_URL, _DEV_FILE_NAME),
        }
        downloaded_files = dl_manager.download_custom(urls_to_download, tf.io.gfile.copy)

        return [
            nlp.SplitGenerator(name=nlp.Split.TRAIN, gen_kwargs={"filepath": downloaded_files["train"]}),
            nlp.SplitGenerator(name=nlp.Split.VALIDATION, gen_kwargs={"filepath": downloaded_files["dev"]},),
        ]

    def _generate_examples(self, filepath):
        """Yields examples."""
        # TODO(boolq): Yields (key, example) tuples from the dataset
        with open(filepath) as f:
            for id_, row in enumerate(f):
                data = json.loads(row)
                question = data["question"]
                answer = data["answer"]
                passage = data["passage"]
                yield id_, {"question": question, "answer": answer, "passage": passage}
