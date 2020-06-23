"""TODO(discofuse): Add a description here."""

from __future__ import absolute_import, division, print_function

import csv
import os

import tensorflow as tf

import nlp


# TODO(discofuse): BibTeX citation

_URL_ = "https://storage.googleapis.com/discofuse_dataset_v1/"
_CITATION = """\
@InProceedings{GevaEtAl2019,
  title = {DiscoFuse: A Large-Scale Dataset for Discourse-Based Sentence Fusion},
  author = {Geva, Mor and Malmi, Eric and Szpektor, Idan and Berant, Jonathan},
  booktitle = {Proceedings of the 2019 Annual Conference of the North American Chapter of the Association for Computational Linguistics},
  note = {arXiv preprint arXiv:1902.10526},
  year = {2019}
}

"""

# TODO(discofuse):
_DESCRIPTION = """\
 DISCOFUSE is a large scale dataset for discourse-based sentence fusion. 
"""


class DiscofuseConfig(nlp.BuilderConfig):

    """ BuilderConfig for Discofuse"""

    def __init__(self, data_url, balanced=False, **kwargs):
        """

        Args:
            balanced: to specify if we want to load the balanced file or the full file
            **kwargs: keyword arguments forwarded to super.
        """
        super(DiscofuseConfig, self).__init__(
            version=nlp.Version("1.0.0", "New split API (https://tensorflow.org/datasets/splits)"), **kwargs
        )
        self.balanced = balanced
        self.data_url = data_url


class Discofuse(nlp.GeneratorBasedBuilder):
    """TODO(discofuse): Short description of my dataset."""

    # TODO(discofuse): Set up version.
    VERSION = nlp.Version("1.0.0")
    BUILDER_CONFIGS = [
        DiscofuseConfig(
            name="discofuse-sport", description="sentence fusion", data_url=_URL_ + "discofuse_v1_sports.tar.gz"
        ),
        DiscofuseConfig(
            name="discofuse-wikipedia", description="sentence fusion", data_url=_URL_ + "discofuse_v1_wikipedia.tar.gz"
        ),
    ]

    def _info(self):
        # TODO(discofuse): Specifies the nlp.DatasetInfo object
        return nlp.DatasetInfo(
            # This is the description that will appear on the datasets page.
            description=_DESCRIPTION,
            # nlp.features.FeatureConnectors
            features=nlp.Features(
                {
                    "connective_string": nlp.Value("string"),
                    "discourse_type": nlp.Value("string"),
                    "coherent_second_sentence": nlp.Value("string"),
                    "has_coref_type_pronoun": nlp.Value("float32"),
                    "incoherent_first_sentence": nlp.Value("string"),
                    "incoherent_second_sentence": nlp.Value("string"),
                    "has_coref_type_nominal": nlp.Value("float32"),
                    "coherent_first_sentence": nlp.Value("string"),
                    # These are the features of your dataset like images, labels ...
                }
            ),
            # If there's a common (input, target) tuple from the features,
            # specify them here. They'll be used if as_supervised=True in
            # builder.as_dataset.
            supervised_keys=None,
            # Homepage of the dataset for documentation
            homepage="https://github.com/google-research-datasets/discofuse",
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        """Returns SplitGenerators."""
        # TODO(discofuse): Downloads the data and defines the splits
        # dl_manager is a nlp.download.DownloadManager that can be used to
        # download and extract URLs
        if self.config.name == "discofuse-sport":
            dl_dir = dl_manager.download_and_extract(self.config.data_url)
            data_dir = os.path.join(dl_dir, "discofuse_v1/sports")
            if self.config.balanced:
                return [
                    nlp.SplitGenerator(
                        name=nlp.Split.TRAIN,
                        # These kwargs will be passed to _generate_examples
                        gen_kwargs={"filepath": os.path.join(data_dir, "train_balanced.tsv")},
                    ),
                    nlp.SplitGenerator(
                        name=nlp.Split.TEST,
                        # These kwargs will be passed to _generate_examples
                        gen_kwargs={"filepath": os.path.join(data_dir, "test_balanced.tsv")},
                    ),
                    nlp.SplitGenerator(
                        name=nlp.Split.VALIDATION,
                        # These kwargs will be passed to _generate_examples
                        gen_kwargs={"filepath": os.path.join(data_dir, "dev_balanced.tsv")},
                    ),
                ]
            else:
                return [
                    nlp.SplitGenerator(
                        name=nlp.Split.TRAIN,
                        # These kwargs will be passed to _generate_examples
                        gen_kwargs={"filepath": os.path.join(data_dir, "train.tsv")},
                    ),
                    nlp.SplitGenerator(
                        name=nlp.Split.TEST,
                        # These kwargs will be passed to _generate_examples
                        gen_kwargs={"filepath": os.path.join(data_dir, "test.tsv")},
                    ),
                    nlp.SplitGenerator(
                        name=nlp.Split.VALIDATION,
                        # These kwargs will be passed to _generate_examples
                        gen_kwargs={"filepath": os.path.join(data_dir, "dev.tsv")},
                    ),
                ]
        else:
            if self.config.name == "discofuse-wikipedia":
                dl_dir = dl_manager.download_and_extract(self.config.data_url)
                data_dir = os.path.join(dl_dir, "discofuse_v1/wikipedia")
                if self.config.balanced:
                    return [
                        nlp.SplitGenerator(
                            name=nlp.Split.TRAIN,
                            # These kwargs will be passed to _generate_examples
                            gen_kwargs={"filepath": os.path.join(data_dir, "train_balanced.tsv")},
                        ),
                        nlp.SplitGenerator(
                            name=nlp.Split.TEST,
                            # These kwargs will be passed to _generate_examples
                            gen_kwargs={"filepath": os.path.join(data_dir, "test_balanced.tsv")},
                        ),
                        nlp.SplitGenerator(
                            name=nlp.Split.VALIDATION,
                            # These kwargs will be passed to _generate_examples
                            gen_kwargs={"filepath": os.path.join(data_dir, "dev_balanced.tsv")},
                        ),
                    ]
                else:
                    return [
                        nlp.SplitGenerator(
                            name=nlp.Split.TRAIN,
                            # These kwargs will be passed to _generate_examples
                            gen_kwargs={"filepath": os.path.join(data_dir, "train.tsv")},
                        ),
                        nlp.SplitGenerator(
                            name=nlp.Split.TEST,
                            # These kwargs will be passed to _generate_examples
                            gen_kwargs={"filepath": os.path.join(data_dir, "test.tsv")},
                        ),
                        nlp.SplitGenerator(
                            name=nlp.Split.VALIDATION,
                            # These kwargs will be passed to _generate_examples
                            gen_kwargs={"filepath": os.path.join(data_dir, "dev.tsv")},
                        ),
                    ]

    def _generate_examples(self, filepath):
        """Yields examples."""
        # TODO(discofuse): Yields (key, example) tuples from the dataset
        with open(filepath) as f:
            data = csv.DictReader(f, delimiter="\t")
            for id_, row in enumerate(data):
                co_first_sent = row["coherent_first_sentence"]
                co_second_sent = row["coherent_second_sentence"]
                connect_str = row["connective_string"]
                discourse_type = row["discourse_type"]
                has_coref_pronoun = row["has_coref_type_pronoun"]
                has_coref_nominal = row["has_coref_type_nominal"]
                inco_first_sent = row["incoherent_first_sentence"]
                inco_second_sent = row["incoherent_second_sentence"]
                yield id_, {
                    "connective_string": connect_str,
                    "discourse_type": discourse_type,
                    "coherent_second_sentence": co_second_sent,
                    "has_coref_type_pronoun": has_coref_pronoun,
                    "incoherent_first_sentence": inco_first_sent,
                    "incoherent_second_sentence": inco_second_sent,
                    "has_coref_type_nominal": has_coref_nominal,
                    "coherent_first_sentence": co_first_sent,
                }
