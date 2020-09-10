"""TODO(wiqa): Add a description here."""

from __future__ import absolute_import, division, print_function

import json
import os

import datasets


# TODO(wiqa): BibTeX citation
_CITATION = """\
@article{wiqa,
      author    = {Niket Tandon and Bhavana Dalvi Mishra and Keisuke Sakaguchi and Antoine Bosselut and Peter Clark}
      title     = {WIQA: A dataset for "What if..." reasoning over procedural text},
      journal   = {arXiv:1909.04739v1},
      year      = {2019},
}
"""

# TODO(wiqa):
_DESCRIPTION = """\
The WIQA dataset V1 has 39705 questions containing a perturbation and a possible effect in the context of a paragraph.
The dataset is split into 29808 train questions, 6894 dev questions and 3003 test questions.
"""
_URL = "https://public-aristo-processes.s3-us-west-2.amazonaws.com/wiqa_dataset_no_explanation_v2/wiqa-dataset-v2-october-2019.zip"
URl = "s3://ai2-s2-research-public/open-corpus/2020-04-10/"


class Wiqa(datasets.GeneratorBasedBuilder):
    """TODO(wiqa): Short description of my dataset."""

    # TODO(wiqa): Set up version.
    VERSION = datasets.Version("0.1.0")

    def _info(self):
        # TODO(wiqa): Specifies the datasets.DatasetInfo object
        return datasets.DatasetInfo(
            # This is the description that will appear on the datasets page.
            description=_DESCRIPTION,
            # datasets.features.FeatureConnectors
            features=datasets.Features(
                {
                    # These are the features of your dataset like images, labels ...
                    "question_stem": datasets.Value("string"),
                    "question_para_step": datasets.features.Sequence(datasets.Value("string")),
                    "answer_label": datasets.Value("string"),
                    "answer_label_as_choice": datasets.Value("string"),
                    "choices": datasets.features.Sequence(
                        {"text": datasets.Value("string"), "label": datasets.Value("string")}
                    ),
                    "metadata_question_id": datasets.Value("string"),
                    "metadata_graph_id": datasets.Value("string"),
                    "metadata_para_id": datasets.Value("string"),
                    "metadata_question_type": datasets.Value("string"),
                    "metadata_path_len": datasets.Value("int32"),
                }
            ),
            # If there's a common (input, target) tuple from the features,
            # specify them here. They'll be used if as_supervised=True in
            # builder.as_dataset.
            supervised_keys=None,
            # Homepage of the dataset for documentation
            homepage="https://allenai.org/data/wiqa",
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        """Returns SplitGenerators."""
        # TODO(wiqa): Downloads the data and defines the splits
        # dl_manager is a datasets.download.DownloadManager that can be used to
        # download and extract URLs
        dl_dir = dl_manager.download_and_extract(_URL)

        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={"filepath": os.path.join(dl_dir, "train.jsonl")},
            ),
            datasets.SplitGenerator(
                name=datasets.Split.TEST,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={"filepath": os.path.join(dl_dir, "test.jsonl")},
            ),
            datasets.SplitGenerator(
                name=datasets.Split.VALIDATION,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={"filepath": os.path.join(dl_dir, "dev.jsonl")},
            ),
        ]

    def _generate_examples(self, filepath):
        """Yields examples."""
        # TODO(wiqa): Yields (key, example) tuples from the dataset
        with open(filepath, encoding="utf-8") as f:
            for id_, row in enumerate(f):
                data = json.loads(row)

                yield id_, {
                    "question_stem": data["question"]["stem"],
                    "question_para_step": data["question"]["para_steps"],
                    "answer_label": data["question"]["answer_label"],
                    "answer_label_as_choice": data["question"]["answer_label_as_choice"],
                    "choices": {
                        "text": [choice["text"] for choice in data["question"]["choices"]],
                        "label": [choice["label"] for choice in data["question"]["choices"]],
                    },
                    "metadata_question_id": data["metadata"]["ques_id"],
                    "metadata_graph_id": data["metadata"]["graph_id"],
                    "metadata_para_id": data["metadata"]["para_id"],
                    "metadata_question_type": data["metadata"]["question_type"],
                    "metadata_path_len": data["metadata"]["path_len"],
                }
