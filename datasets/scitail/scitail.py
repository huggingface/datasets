"""TODO(sciTail): Add a description here."""


import csv
import json
import os
import textwrap

import datasets


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


class ScitailConfig(datasets.BuilderConfig):

    """BuilderConfig for Xquad"""

    def __init__(self, **kwargs):
        """

        Args:
            **kwargs: keyword arguments forwarded to super.
        """
        super(ScitailConfig, self).__init__(version=datasets.Version("1.1.0", ""), **kwargs)


class Scitail(datasets.GeneratorBasedBuilder):
    """TODO(sciTail): Short description of my dataset."""

    # TODO(sciTail): Set up version.
    VERSION = datasets.Version("1.1.0")
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
        # TODO(sciTail): Specifies the datasets.DatasetInfo object
        if self.config.name == "snli_format":
            return datasets.DatasetInfo(
                # This is the description that will appear on the datasets page.
                description=_DESCRIPTION,
                # datasets.features.FeatureConnectors
                features=datasets.Features(
                    {
                        "sentence1_binary_parse": datasets.Value("string"),
                        "sentence1_parse": datasets.Value("string"),
                        "sentence1": datasets.Value("string"),
                        "sentence2_parse": datasets.Value("string"),
                        "sentence2": datasets.Value("string"),
                        "annotator_labels": datasets.features.Sequence(datasets.Value("string")),
                        "gold_label": datasets.Value("string")
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
            return datasets.DatasetInfo(
                # This is the description that will appear on the datasets page.
                description=_DESCRIPTION,
                # datasets.features.FeatureConnectors
                features=datasets.Features(
                    {
                        "premise": datasets.Value("string"),
                        "hypothesis": datasets.Value("string"),
                        "label": datasets.Value("string")
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
            return datasets.DatasetInfo(
                # This is the description that will appear on the datasets page.
                description=_DESCRIPTION,
                # datasets.features.FeatureConnectors
                features=datasets.Features(
                    {
                        "answer": datasets.Value("string"),
                        "sentence2_structure": datasets.Value("string"),
                        "sentence1": datasets.Value("string"),
                        "sentence2": datasets.Value("string"),
                        "gold_label": datasets.Value("string"),
                        "question": datasets.Value("string")
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
            return datasets.DatasetInfo(
                # This is the description that will appear on the datasets page.
                description=_DESCRIPTION,
                # datasets.features.FeatureConnectors
                features=datasets.Features(
                    {
                        "premise": datasets.Value("string"),
                        "hypothesis": datasets.Value("string"),
                        "label": datasets.Value("string"),
                        "hypothesis_graph_structure": datasets.Value("string")
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
        # dl_manager is a datasets.download.DownloadManager that can be used to
        # download and extract URLs
        dl_dir = dl_manager.download_and_extract(_URL)
        data_dir = os.path.join(dl_dir, "SciTailV1.1")
        snli = os.path.join(data_dir, "snli_format")
        dgem = os.path.join(data_dir, "dgem_format")
        tsv = os.path.join(data_dir, "tsv_format")
        predictor = os.path.join(data_dir, "predictor_format")
        if self.config.name == "snli_format":
            return [
                datasets.SplitGenerator(
                    name=datasets.Split.TRAIN,
                    # These kwargs will be passed to _generate_examples
                    gen_kwargs={"filepath": os.path.join(snli, "scitail_1.0_train.txt")},
                ),
                datasets.SplitGenerator(
                    name=datasets.Split.TEST,
                    # These kwargs will be passed to _generate_examples
                    gen_kwargs={"filepath": os.path.join(snli, "scitail_1.0_test.txt")},
                ),
                datasets.SplitGenerator(
                    name=datasets.Split.VALIDATION,
                    # These kwargs will be passed to _generate_examples
                    gen_kwargs={"filepath": os.path.join(snli, "scitail_1.0_dev.txt")},
                ),
            ]
        elif self.config.name == "tsv_format":
            return [
                datasets.SplitGenerator(
                    name=datasets.Split.TRAIN,
                    # These kwargs will be passed to _generate_examples
                    gen_kwargs={"filepath": os.path.join(tsv, "scitail_1.0_train.tsv")},
                ),
                datasets.SplitGenerator(
                    name=datasets.Split.TEST,
                    # These kwargs will be passed to _generate_examples
                    gen_kwargs={"filepath": os.path.join(tsv, "scitail_1.0_test.tsv")},
                ),
                datasets.SplitGenerator(
                    name=datasets.Split.VALIDATION,
                    # These kwargs will be passed to _generate_examples
                    gen_kwargs={"filepath": os.path.join(tsv, "scitail_1.0_dev.tsv")},
                ),
            ]
        elif self.config.name == "predictor_format":
            return [
                datasets.SplitGenerator(
                    name=datasets.Split.TRAIN,
                    # These kwargs will be passed to _generate_examples
                    gen_kwargs={"filepath": os.path.join(predictor, "scitail_1.0_structure_train.jsonl")},
                ),
                datasets.SplitGenerator(
                    name=datasets.Split.TEST,
                    # These kwargs will be passed to _generate_examples
                    gen_kwargs={"filepath": os.path.join(predictor, "scitail_1.0_structure_test.jsonl")},
                ),
                datasets.SplitGenerator(
                    name=datasets.Split.VALIDATION,
                    # These kwargs will be passed to _generate_examples
                    gen_kwargs={"filepath": os.path.join(predictor, "scitail_1.0_structure_dev.jsonl")},
                ),
            ]
        elif self.config.name == "dgem_format":
            return [
                datasets.SplitGenerator(
                    name=datasets.Split.TRAIN,
                    # These kwargs will be passed to _generate_examples
                    gen_kwargs={"filepath": os.path.join(dgem, "scitail_1.0_structure_train.tsv")},
                ),
                datasets.SplitGenerator(
                    name=datasets.Split.TEST,
                    # These kwargs will be passed to _generate_examples
                    gen_kwargs={"filepath": os.path.join(dgem, "scitail_1.0_structure_test.tsv")},
                ),
                datasets.SplitGenerator(
                    name=datasets.Split.VALIDATION,
                    # These kwargs will be passed to _generate_examples
                    gen_kwargs={"filepath": os.path.join(dgem, "scitail_1.0_structure_dev.tsv")},
                ),
            ]

    def _generate_examples(self, filepath):
        """Yields examples."""
        # TODO(sciTail): Yields (key, example) tuples from the dataset
        with open(filepath, encoding="utf-8") as f:
            if self.config.name == "snli_format":
                for id_, row in enumerate(f):
                    data = json.loads(row)

                    yield id_, {
                        "sentence1_binary_parse": data["sentence1_binary_parse"],
                        "sentence1_parse": data["sentence1_parse"],
                        "sentence1": data["sentence1"],
                        "sentence2_parse": data["sentence2_parse"],
                        "sentence2": data["sentence2"],
                        "annotator_labels": data["annotator_labels"],
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
