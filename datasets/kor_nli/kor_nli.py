"""TODO(kor_nli): Add a description here."""

from __future__ import absolute_import, division, print_function

import csv
import os

import nlp


# TODO(kor_nli): BibTeX citation
_CITATION = """\
@article{ham2020kornli,
  title={KorNLI and KorSTS: New Benchmark Datasets for Korean Natural Language Understanding},
  author={Ham, Jiyeon and Choe, Yo Joong and Park, Kyubyong and Choi, Ilji and Soh, Hyungjoon},
  journal={arXiv preprint arXiv:2004.03289},
  year={2020}
}
"""

# TODO(kor_nli):
_DESCRIPTION = """ Korean Natural  Language Inference datasets
"""
_URL = "https://github.com/kakaobrain/KorNLUDatasets/archive/master.zip"


class KorNLIConfig(nlp.BuilderConfig):
    """BuilderConfig for KorNLI."""

    def __init__(self, **kwargs):
        """BuilderConfig for KorNLI.

    Args:

      **kwargs: keyword arguments forwarded to super.
    """
        # Version 1.1.0 remove empty document and summary strings.
        super(KorNLIConfig, self).__init__(version=nlp.Version("1.0.0"), **kwargs)


class KorNli(nlp.GeneratorBasedBuilder):
    """TODO(kor_nli): Short description of my dataset."""

    # TODO(kor_nli): Set up version.
    VERSION = nlp.Version("1.0.0")
    BUILDER_CONFIGS = [
        KorNLIConfig(name="multi_nli", description="Korean multi NLI datasets"),
        KorNLIConfig(name="snli", description="Korean SNLI dataset"),
        KorNLIConfig(name="xnli", description="Korean XNLI dataset"),
    ]

    def _info(self):
        # TODO(kor_nli): Specifies the nlp.DatasetInfo object
        return nlp.DatasetInfo(
            # This is the description that will appear on the datasets page.
            description=_DESCRIPTION,
            # nlp.features.FeatureConnectors
            features=nlp.Features(
                {
                    # These are the features of your dataset like images, labels ...
                    "sentence1": nlp.Value("string"),
                    "sentence2": nlp.Value("string"),
                    "gold_label": nlp.Value("string"),
                }
            ),
            # If there's a common (input, target) tuple from the features,
            # specify them here. They'll be used if as_supervised=True in
            # builder.as_dataset.
            supervised_keys=None,
            # Homepage of the dataset for documentation
            homepage="https://github.com/kakaobrain/KorNLUDatasets",
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        """Returns SplitGenerators."""
        # TODO(kor_nli): Downloads the data and defines the splits
        # dl_manager is a nlp.download.DownloadManager that can be used to
        # download and extract URLs
        dl_dir = dl_manager.download_and_extract(_URL)
        dl_dir = os.path.join(dl_dir, "KorNLUDatasets-master", "KorNLI")
        if self.config.name == "multi_nli":
            return [
                nlp.SplitGenerator(
                    name=nlp.Split.TRAIN,
                    # These kwargs will be passed to _generate_examples
                    gen_kwargs={"filepath": os.path.join(dl_dir, "multinli.train.ko.tsv")},
                ),
            ]
        elif self.config.name == "snli":
            return [
                nlp.SplitGenerator(
                    name=nlp.Split.TRAIN,
                    # These kwargs will be passed to _generate_examples
                    gen_kwargs={"filepath": os.path.join(dl_dir, "snli_1.0_train.ko.tsv")},
                ),
            ]
        else:
            return [
                nlp.SplitGenerator(
                    name=nlp.Split.VALIDATION,
                    # These kwargs will be passed to _generate_examples
                    gen_kwargs={"filepath": os.path.join(dl_dir, "xnli.dev.ko.tsv")},
                ),
                nlp.SplitGenerator(
                    name=nlp.Split.TEST,
                    # These kwargs will be passed to _generate_examples
                    gen_kwargs={"filepath": os.path.join(dl_dir, "xnli.test.ko.tsv")},
                ),
            ]

    def _generate_examples(self, filepath):
        """Yields examples."""
        # TODO(kor_nli): Yields (key, example) tuples from the dataset
        with open(filepath) as f:
            data = csv.DictReader(f, dialect="excel-tab")
            for id_, row in enumerate(data):

                if len(row) != 3:
                    continue
                yield id_, row
