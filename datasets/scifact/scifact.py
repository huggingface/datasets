"""TODO(scifact): Add a description here."""

from __future__ import absolute_import, division, print_function

import json
import os

import datasets


# TODO(scifact): BibTeX citation
_CITATION = """\
@inproceedings{scifact2020
  title={ Fact or Fiction: Verifying Scientific Claims},
  author={David,  Wadden and Kyle, Lo and Lucy Lu, Wang and Shanchuan, Lin and Madeleine van, Zuylen and Arman, Cohan and  Hannaneh, Hajishirzi},
  booktitle={2011 AAAI Spring Symposium Series},
  year={2020},
}
"""

# TODO(scifact):
_DESCRIPTION = """\
SciFact, a dataset of 1.4K expert-written scientific claims paired with evidence-containing abstracts, and annotated with labels and rationales
"""

_URL = "https://ai2-s2-scifact.s3-us-west-2.amazonaws.com/release/2020-05-01/data.tar.gz"


class ScifactConfig(datasets.BuilderConfig):
    """BuilderConfig for Scifact"""

    def __init__(self, **kwargs):
        """

        Args:
            **kwargs: keyword arguments forwarded to super.
        """
        super(ScifactConfig, self).__init__(version=datasets.Version("1.0.0", ""), **kwargs)


class Scifact(datasets.GeneratorBasedBuilder):
    """TODO(scifact): Short description of my dataset."""

    # TODO(scifact): Set up version.
    VERSION = datasets.Version("0.1.0")
    BUILDER_CONFIGS = [
        ScifactConfig(name="corpus", description=" The corpus of evidence documents"),
        ScifactConfig(name="claims", description=" The claims are split into train, test, dev"),
    ]

    def _info(self):
        # TODO(scifact): Specifies the datasets.DatasetInfo object
        if self.config.name == "corpus":
            features = {
                "doc_id": datasets.Value("int32"),  # The document's S2ORC ID.
                "title": datasets.Value("string"),  # The title.
                "abstract": datasets.features.Sequence(
                    datasets.Value("string")
                ),  # The abstract, written as a list of sentences.
                "structured": datasets.Value("bool"),  # Indicator for whether this is a structured abstract.
            }
        else:
            features = {
                "id": datasets.Value("int32"),  # An integer claim ID.
                "claim": datasets.Value("string"),  # The text of the claim.
                "evidence_doc_id": datasets.Value("string"),
                "evidence_label": datasets.Value("string"),  # Label for the rationale.
                "evidence_sentences": datasets.features.Sequence(datasets.Value("int32")),  # Rationale sentences.
                "cited_doc_ids": datasets.features.Sequence(datasets.Value("int32")),  # The claim's "cited documents".
            }

        return datasets.DatasetInfo(
            # This is the description that will appear on the datasets page.
            description=_DESCRIPTION,
            # datasets.features.FeatureConnectors
            features=datasets.Features(
                features
                # These are the features of your dataset like images, labels ...
            ),
            # If there's a common (input, target) tuple from the features,
            # specify them here. They'll be used if as_supervised=True in
            # builder.as_dataset.
            supervised_keys=None,
            # Homepage of the dataset for documentation
            homepage="https://scifact.apps.allenai.org/",
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        """Returns SplitGenerators."""
        # TODO(scifact): Downloads the data and defines the splits
        # dl_manager is a datasets.download.DownloadManager that can be used to
        # download and extract URLs
        dl_dir = dl_manager.download_and_extract(_URL)

        if self.config.name == "corpus":
            return [
                datasets.SplitGenerator(
                    name=datasets.Split.TRAIN,
                    # These kwargs will be passed to _generate_examples
                    gen_kwargs={"filepath": os.path.join(dl_dir, "data", "corpus.jsonl"), "split": "train"},
                ),
            ]
        else:
            return [
                datasets.SplitGenerator(
                    name=datasets.Split.TRAIN,
                    # These kwargs will be passed to _generate_examples
                    gen_kwargs={"filepath": os.path.join(dl_dir, "data", "claims_train.jsonl"), "split": "train"},
                ),
                datasets.SplitGenerator(
                    name=datasets.Split.TEST,
                    # These kwargs will be passed to _generate_examples
                    gen_kwargs={"filepath": os.path.join(dl_dir, "data", "claims_test.jsonl"), "split": "test"},
                ),
                datasets.SplitGenerator(
                    name=datasets.Split.VALIDATION,
                    # These kwargs will be passed to _generate_examples
                    gen_kwargs={"filepath": os.path.join(dl_dir, "data", "claims_dev.jsonl"), "split": "dev"},
                ),
            ]

    def _generate_examples(self, filepath, split):
        """Yields examples."""
        # TODO(scifact): Yields (key, example) tuples from the dataset
        with open(filepath, encoding="utf-8") as f:
            for id_, row in enumerate(f):
                data = json.loads(row)
                if self.config.name == "corpus":
                    yield id_, {
                        "doc_id": int(data["doc_id"]),
                        "title": data["title"],
                        "abstract": data["abstract"],
                        "structured": data["structured"],
                    }
                else:
                    if split == "test":
                        yield id_, {
                            "id": data["id"],
                            "claim": data["claim"],
                            "evidence_doc_id": "",
                            "evidence_label": "",
                            "evidence_sentences": [],
                            "cited_doc_ids": [],
                        }
                    else:
                        evidences = data["evidence"]
                        if evidences:
                            for id1, doc_id in enumerate(evidences):
                                for id2, evidence in enumerate(evidences[doc_id]):
                                    yield str(id_) + "_" + str(id1) + "_" + str(id2), {
                                        "id": data["id"],
                                        "claim": data["claim"],
                                        "evidence_doc_id": doc_id,
                                        "evidence_label": evidence["label"],
                                        "evidence_sentences": evidence["sentences"],
                                        "cited_doc_ids": data.get("cited_doc_ids", []),
                                    }
                        else:
                            yield id_, {
                                "id": data["id"],
                                "claim": data["claim"],
                                "evidence_doc_id": "",
                                "evidence_label": "",
                                "evidence_sentences": [],
                                "cited_doc_ids": data.get("cited_doc_ids", []),
                            }
