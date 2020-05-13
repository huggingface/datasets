"""TODO(sciTail): Add a description here."""

from __future__ import absolute_import, division, print_function

import csv
import json
import os
import textwrap

import nlp


# TODO(sciTail): BibTeX citation
_CITATION = """\
inproceedings{scitail,
     Author = {Tushar Khot and Ashish Sabharwal and Peter Clark},
     Booktitle = {AAAI},
     Title = {{SciTail}: A Textual Entailment Dataset from Science Question Answering},
     Year = {2018}
}
"""

# TODO(sciTail):
_DESCRIPTION = """\
The SciTail dataset is an entailment dataset created from multiple-choice science exams and web sentences. Each question 
and the correct answer choice are converted into an assertive statement to form the hypothesis. We use information 
retrieval to obtain relevant text from a large text corpus of web sentences, and use these sentences as a premise P. We 
crowdsource the annotation of such premise-hypothesis pair as supports (entails) or not (neutral), in order to create 
the SciTail dataset. The dataset contains 27,026 examples with 10,101 examples with entails label and 16,925 examples 
with neutral label
"""

_URL = "http://data.allenai.org.s3.amazonaws.com/downloads/SciTailV1.1.zip"


class ScitailConfig(nlp.BuilderConfig):

    """ BuilderConfig for Xquad"""

    def __init__(self, **kwargs):
        """

        Args:
            **kwargs: keyword arguments forwarded to super.
        """
        super(ScitailConfig, self).__init__(
            version=nlp.Version("1.1.0", "New split API (https://tensorflow.org/datasets/splits)"), **kwargs
        )


class Scitail(nlp.GeneratorBasedBuilder):
    """TODO(sciTail): Short description of my dataset."""

    # TODO(sciTail): Set up version.
    VERSION = nlp.Version("1.1.0")
    BUILDER_CONFIGS = [
        ScitailConfig(
            name="snli_format",
            description="JSONL format used by SNLI with a JSON object corresponding to each entailment example in each line.",
        ),
        ScitailConfig(
            name="tsv_format", description="Tab-separated format with three columns: premise hypothesis label"
        ),
        ScitailConfig(
            name="dgem_format",
            description="Tab-separated format used by the DGEM model: premise hypothesis label hypothesis graph structure",
        ),
        ScitailConfig(
            name="predictor_format",
            description=textwrap.dedent(
                """\
          AllenNLP predictors work only with JSONL format. This folder contains the SciTail train/dev/test in JSONL format
        so that it can be loaded into the predictors. Each line is a JSON object with the following keys:
        gold_label : the example label from {entails, neutral}
        sentence1: the premise
        sentence2: the hypothesis
        sentence2_structure: structure from the hypothesis """
            ),
        ),
    ]

    def _info(self):
        # TODO(sciTail): Specifies the nlp.DatasetInfo object
        if self.config.name == "snli_format":
            return nlp.DatasetInfo(
                # This is the description that will appear on the datasets page.
                description=_DESCRIPTION,
                # nlp.features.FeatureConnectors
                features=nlp.Features(
                    {
                        "sentence1_binary_parse": nlp.Value("string"),
                        "sentence1_parse": nlp.Value("string"),
                        "sentence1": nlp.Value("string"),
                        "sentence2_parse": nlp.Value("string"),
                        "sentence2": nlp.Value("string"),
                        "annotator_labels": nlp.features.Sequence({"annotator_label": nlp.Value("string")}),
                        "gold_label": nlp.Value("string")
                        # These are the features of your dataset like images, labels ...
                    }
                ),
                # If there's a common (input, target) tuple from the features,
                # specify them here. They'll be used if as_supervised=True in
                # builder.as_dataset.
                supervised_keys=None,
                # Homepage of the dataset for documentation
                homepage="https://allenai.org/data/scitail",
                citation=_CITATION,
            )
        elif self.config.name == "tsv_format":
            return nlp.DatasetInfo(
                # This is the description that will appear on the datasets page.
                description=_DESCRIPTION,
                # nlp.features.FeatureConnectors
                features=nlp.Features(
                    {
                        "premise": nlp.Value("string"),
                        "hypothesis": nlp.Value("string"),
                        "label": nlp.Value("string")
                        # These are the features of your dataset like images, labels ...
                    }
                ),
                # If there's a common (input, target) tuple from the features,
                # specify them here. They'll be used if as_supervised=True in
                # builder.as_dataset.
                supervised_keys=None,
                # Homepage of the dataset for documentation
                homepage="https://allenai.org/data/scitail",
                citation=_CITATION,
            )
        elif self.config.name == "predictor_format":
            return nlp.DatasetInfo(
                # This is the description that will appear on the datasets page.
                description=_DESCRIPTION,
                # nlp.features.FeatureConnectors
                features=nlp.Features(
                    {
                        "answer": nlp.Value("string"),
                        "sentence2_structure": nlp.Value("string"),
                        "sentence1": nlp.Value("string"),
                        "sentence2": nlp.Value("string"),
                        "gold_label": nlp.Value("string"),
                        "question": nlp.Value("string")
                        # These are the features of your dataset like images, labels ...
                    }
                ),
                # If there's a common (input, target) tuple from the features,
                # specify them here. They'll be used if as_supervised=True in
                # builder.as_dataset.
                supervised_keys=None,
                # Homepage of the dataset for documentation
                homepage="https://allenai.org/data/scitail",
                citation=_CITATION,
            )
        elif self.config.name == "dgem_format":
            return nlp.DatasetInfo(
                # This is the description that will appear on the datasets page.
                description=_DESCRIPTION,
                # nlp.features.FeatureConnectors
                features=nlp.Features(
                    {
                        "premise": nlp.Value("string"),
                        "hypothesis": nlp.Value("string"),
                        "label": nlp.Value("string"),
                        "hypothesis_graph_structure": nlp.Value("string")
                        # These are the features of your dataset like images, labels ...
                    }
                ),
                # If there's a common (input, target) tuple from the features,
                # specify them here. They'll be used if as_supervised=True in
                # builder.as_dataset.
                supervised_keys=None,
                # Homepage of the dataset for documentation
                homepage="https://allenai.org/data/scitail",
                citation=_CITATION,
            )

    def _split_generators(self, dl_manager):
        """Returns SplitGenerators."""
        # TODO(sciTail): Downloads the data and defines the splits
        # dl_manager is a nlp.download.DownloadManager that can be used to
        # download and extract URLs
        dl_dir = dl_manager.download_and_extract(_URL)
        data_dir = os.path.join(dl_dir, "SciTailV1.1")
        snli = os.path.join(data_dir, "snli_format")
        dgem = os.path.join(data_dir, "dgem_format")
        tsv = os.path.join(data_dir, "tsv_format")
        predictor = os.path.join(data_dir, "predictor_format")
        if self.config.name == "snli_format":
            return [
                nlp.SplitGenerator(
                    name=nlp.Split.TRAIN,
                    # These kwargs will be passed to _generate_examples
                    gen_kwargs={"filepath": os.path.join(snli, "scitail_1.0_train.txt")},
                ),
                nlp.SplitGenerator(
                    name=nlp.Split.TEST,
                    # These kwargs will be passed to _generate_examples
                    gen_kwargs={"filepath": os.path.join(snli, "scitail_1.0_test.txt")},
                ),
                nlp.SplitGenerator(
                    name=nlp.Split.VALIDATION,
                    # These kwargs will be passed to _generate_examples
                    gen_kwargs={"filepath": os.path.join(snli, "scitail_1.0_dev.txt")},
                ),
            ]
        elif self.config.name == "tsv_format":
            return [
                nlp.SplitGenerator(
                    name=nlp.Split.TRAIN,
                    # These kwargs will be passed to _generate_examples
                    gen_kwargs={"filepath": os.path.join(tsv, "scitail_1.0_train.tsv")},
                ),
                nlp.SplitGenerator(
                    name=nlp.Split.TEST,
                    # These kwargs will be passed to _generate_examples
                    gen_kwargs={"filepath": os.path.join(tsv, "scitail_1.0_test.tsv")},
                ),
                nlp.SplitGenerator(
                    name=nlp.Split.VALIDATION,
                    # These kwargs will be passed to _generate_examples
                    gen_kwargs={"filepath": os.path.join(tsv, "scitail_1.0_dev.tsv")},
                ),
            ]
        elif self.config.name == "predictor_format":
            return [
                nlp.SplitGenerator(
                    name=nlp.Split.TRAIN,
                    # These kwargs will be passed to _generate_examples
                    gen_kwargs={"filepath": os.path.join(predictor, "scitail_1.0_structure_train.jsonl")},
                ),
                nlp.SplitGenerator(
                    name=nlp.Split.TEST,
                    # These kwargs will be passed to _generate_examples
                    gen_kwargs={"filepath": os.path.join(predictor, "scitail_1.0_structure_test.jsonl")},
                ),
                nlp.SplitGenerator(
                    name=nlp.Split.VALIDATION,
                    # These kwargs will be passed to _generate_examples
                    gen_kwargs={"filepath": os.path.join(predictor, "scitail_1.0_structure_dev.jsonl")},
                ),
            ]
        elif self.config.name == "dgem_format":
            return [
                nlp.SplitGenerator(
                    name=nlp.Split.TRAIN,
                    # These kwargs will be passed to _generate_examples
                    gen_kwargs={"filepath": os.path.join(dgem, "scitail_1.0_structure_train.tsv")},
                ),
                nlp.SplitGenerator(
                    name=nlp.Split.TEST,
                    # These kwargs will be passed to _generate_examples
                    gen_kwargs={"filepath": os.path.join(dgem, "scitail_1.0_structure_test.tsv")},
                ),
                nlp.SplitGenerator(
                    name=nlp.Split.VALIDATION,
                    # These kwargs will be passed to _generate_examples
                    gen_kwargs={"filepath": os.path.join(dgem, "scitail_1.0_structure_dev.tsv")},
                ),
            ]

    def _generate_examples(self, filepath):
        """Yields examples."""
        # TODO(sciTail): Yields (key, example) tuples from the dataset
        with open(filepath) as f:
            if self.config.name == "snli_format":
                for id_, row in enumerate(f):
                    data = json.loads(row)

                    yield id_, {
                        "sentence1_binary_parse": data["sentence1_binary_parse"],
                        "sentence1_parse": data["sentence1_parse"],
                        "sentence1": data["sentence1"],
                        "sentence2_parse": data["sentence2_parse"],
                        "sentence2": data["sentence2"],
                        "annotator_labels": {"annotator_label": data["annotator_labels"]},
                        "gold_label": data["gold_label"],
                    }
            elif self.config.name == "tsv_format":
                data = csv.reader(f, delimiter="\t")
                for id_, row in enumerate(data):
                    yield id_, {"premise": row[0], "hypothesis": row[1], "label": row[2]}
            elif self.config.name == "dgem_format":
                data = csv.reader(f, delimiter="\t")
                for id_, row in enumerate(data):
                    yield id_, {
                        "premise": row[0],
                        "hypothesis": row[1],
                        "label": row[2],
                        "hypothesis_graph_structure": row[3],
                    }
            elif self.config.name == "predictor_format":
                for id_, row in enumerate(f):
                    data = json.loads(row)
                    yield id_, {
                        "answer": data["answer"],
                        "sentence2_structure": data["sentence2_structure"],
                        "sentence1": data["sentence1"],
                        "sentence2": data["sentence2"],
                        "gold_label": data["gold_label"],
                        "question": data["question"],
                    }
