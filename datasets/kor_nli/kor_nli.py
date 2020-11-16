"""TODO(kor_nli): Add a description here."""

from __future__ import absolute_import, division, print_function

import os

import datasets


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


class KorNLIConfig(datasets.BuilderConfig):
    """BuilderConfig for KorNLI."""

    def __init__(self, **kwargs):
        """BuilderConfig for KorNLI.

        Args:

          **kwargs: keyword arguments forwarded to super.
        """
        # Version 1.1.0 remove empty document and summary strings.
        super(KorNLIConfig, self).__init__(version=datasets.Version("1.0.0"), **kwargs)


class KorNli(datasets.GeneratorBasedBuilder):
    """TODO(kor_nli): Short description of my dataset."""

    # TODO(kor_nli): Set up version.
    VERSION = datasets.Version("1.0.0")
    BUILDER_CONFIGS = [
        KorNLIConfig(name="multi_nli", description="Korean multi NLI datasets"),
        KorNLIConfig(name="snli", description="Korean SNLI dataset"),
        KorNLIConfig(name="xnli", description="Korean XNLI dataset"),
    ]

    def _info(self):
        # TODO(kor_nli): Specifies the datasets.DatasetInfo object
        return datasets.DatasetInfo(
            # This is the description that will appear on the datasets page.
            description=_DESCRIPTION,
            # datasets.features.FeatureConnectors
            features=datasets.Features(
                {
                    # These are the features of your dataset like images, labels ...
                    "premise": datasets.Value("string"),
                    "hypothesis": datasets.Value("string"),
                    "label": datasets.ClassLabel(names=["entailment", "neutral", "contradiction"]),
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
        # dl_manager is a datasets.download.DownloadManager that can be used to
        # download and extract URLs
        dl_dir = dl_manager.download_and_extract(_URL)
        dl_dir = os.path.join(dl_dir, "KorNLUDatasets-master", "KorNLI")
        if self.config.name == "multi_nli":
            return [
                datasets.SplitGenerator(
                    name=datasets.Split.TRAIN,
                    # These kwargs will be passed to _generate_examples
                    gen_kwargs={"filepath": os.path.join(dl_dir, "multinli.train.ko.tsv")},
                ),
            ]
        elif self.config.name == "snli":
            return [
                datasets.SplitGenerator(
                    name=datasets.Split.TRAIN,
                    # These kwargs will be passed to _generate_examples
                    gen_kwargs={"filepath": os.path.join(dl_dir, "snli_1.0_train.ko.tsv")},
                ),
            ]
        else:
            return [
                datasets.SplitGenerator(
                    name=datasets.Split.VALIDATION,
                    # These kwargs will be passed to _generate_examples
                    gen_kwargs={"filepath": os.path.join(dl_dir, "xnli.dev.ko.tsv")},
                ),
                datasets.SplitGenerator(
                    name=datasets.Split.TEST,
                    # These kwargs will be passed to _generate_examples
                    gen_kwargs={"filepath": os.path.join(dl_dir, "xnli.test.ko.tsv")},
                ),
            ]

    def _generate_examples(self, filepath):
        """Yields examples."""
        # TODO(kor_nli): Yields (key, example) tuples from the dataset
        with open(filepath, encoding="utf-8") as f:
            next(f)  # skip headers
            columns = ("premise", "hypothesis", "label")
            for id_, row in enumerate(f):
                row = row.strip().split("\t")
                if len(row) != 3:
                    continue
                row = dict(zip(columns, row))
                yield id_, row
