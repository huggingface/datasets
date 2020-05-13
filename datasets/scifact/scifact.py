"""TODO(scifact): Add a description here."""

from __future__ import absolute_import, division, print_function

import json
import os

import nlp


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


class ScifactConfig(nlp.BuilderConfig):
    """BuilderConfig for Scifact"""

    def __init__(self, **kwargs):
        """

        Args:
            **kwargs: keyword arguments forwarded to super.
        """
        super(ScifactConfig, self).__init__(
            version=nlp.Version("1.0.0", "New split API (https://tensorflow.org/datasets/splits)"), **kwargs
        )


class Scifact(nlp.GeneratorBasedBuilder):
    """TODO(scifact): Short description of my dataset."""

    # TODO(scifact): Set up version.
    VERSION = nlp.Version("0.1.0")
    BUILDER_CONFIGS = [
        ScifactConfig(name="corpus", description=" The corpus of evidence documents"),
        ScifactConfig(name="claims", description=" The claims are split into train, test, dev"),
    ]

    def _info(self):
        # TODO(scifact): Specifies the nlp.DatasetInfo object
        if self.config.name == "corpus":
            features = {
                "doc_id": nlp.Value("int32"),  # The document's S2ORC ID.
                "title": nlp.Value("string"),  # The title.
                "abstract": nlp.features.Sequence(
                    {"sentence": nlp.Value("string")}
                ),  # The abstract, written as a list of sentences.
                "structured": nlp.Value("bool"),  # Indicator for whether this is a structured abstract.
            }
        else:
            features = {
                "id": nlp.Value("int32"),  # An integer claim ID.
                "claim": nlp.Value("string"),  # The text of the claim.
                "evidence_doc_id": nlp.Value("string"),
                "evidence_label": nlp.Value("string"),  # Label for the rationale.
                "evidence_sentences": nlp.features.Sequence({"sentence": nlp.Value("int32")}),  # Rationale sentences.
                "cited_doc_ids": nlp.features.Sequence(
                    {"doc_id": nlp.Value("int32")}
                ),  # The claim's "cited documents".
            }

        return nlp.DatasetInfo(
            # This is the description that will appear on the datasets page.
            description=_DESCRIPTION,
            # nlp.features.FeatureConnectors
            features=nlp.Features(
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
        # dl_manager is a nlp.download.DownloadManager that can be used to
        # download and extract URLs
        dl_dir = dl_manager.download_and_extract(_URL)

        if self.config.name == "corpus":
            return [
                nlp.SplitGenerator(
                    name=nlp.Split.TRAIN,
                    # These kwargs will be passed to _generate_examples
                    gen_kwargs={"filepath": os.path.join(dl_dir, "data", "corpus.jsonl"), "split": "train"},
                ),
            ]
        else:
            return [
                nlp.SplitGenerator(
                    name=nlp.Split.TRAIN,
                    # These kwargs will be passed to _generate_examples
                    gen_kwargs={"filepath": os.path.join(dl_dir, "data", "claims_train.jsonl"), "split": "train"},
                ),
                nlp.SplitGenerator(
                    name=nlp.Split.TEST,
                    # These kwargs will be passed to _generate_examples
                    gen_kwargs={"filepath": os.path.join(dl_dir, "data", "claims_test.jsonl"), "split": "test"},
                ),
                nlp.SplitGenerator(
                    name=nlp.Split.VALIDATION,
                    # These kwargs will be passed to _generate_examples
                    gen_kwargs={"filepath": os.path.join(dl_dir, "data", "claims_dev.jsonl"), "split": "dev"},
                ),
            ]

    def _generate_examples(self, filepath, split):
        """Yields examples."""
        # TODO(scifact): Yields (key, example) tuples from the dataset
        with open(filepath) as f:
            for id_, row in enumerate(f):
                data = json.loads(row)
                if self.config.name == "corpus":
                    yield id_, {
                        "doc_id": int(data["doc_id"]),
                        "title": data["title"],
                        "abstract": {"sentence": data["abstract"]},
                        "structured": data["structured"],
                    }
                else:
                    if split == "test":
                        yield id_, {
                            "id": data["id"],
                            "claim": data["claim"],
                            "evidence_doc_id": "",
                            "evidence_label": "",
                            "evidence_sentences": {"sentence": []},
                            "cited_doc_ids": {"doc_id": []},
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
                                        "evidence_sentences": {"sentence": evidence["sentences"]},
                                        "cited_doc_ids": {"doc_id": data.get("cited_doc_ids", [])},
                                    }
                        else:
                            yield id_, {
                                "id": data["id"],
                                "claim": data["claim"],
                                "evidence_doc_id": "",
                                "evidence_label": "",
                                "evidence_sentences": {"sentence": []},
                                "cited_doc_ids": {"doc_id": data.get("cited_doc_ids", [])},
                            }
