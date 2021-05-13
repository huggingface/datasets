"""TODO(xcopa): Add a description here."""


import json
import os

import datasets


# TODO(xcopa): BibTeX citation
_CITATION = """\
  @article{ponti2020xcopa,
  title={{XCOPA: A} Multilingual Dataset for Causal Commonsense Reasoning},
  author={Edoardo M. Ponti, Goran Glava\v{s}, Olga Majewska, Qianchu Liu, Ivan Vuli\'{c} and Anna Korhonen},
  journal={arXiv preprint},
  year={2020},
  url={https://ducdauge.github.io/files/xcopa.pdf}
}

@inproceedings{roemmele2011choice,
  title={Choice of plausible alternatives: An evaluation of commonsense causal reasoning},
  author={Roemmele, Melissa and Bejan, Cosmin Adrian and Gordon, Andrew S},
  booktitle={2011 AAAI Spring Symposium Series},
  year={2011},
  url={https://people.ict.usc.edu/~gordon/publications/AAAI-SPRING11A.PDF},
}
"""

# TODO(xcopa):
_DESCRIPTION = """\
  XCOPA: A Multilingual Dataset for Causal Commonsense Reasoning
The Cross-lingual Choice of Plausible Alternatives dataset is a benchmark to evaluate the ability of machine learning models to transfer commonsense reasoning across
languages. The dataset is the translation and reannotation of the English COPA (Roemmele et al. 2011) and covers 11 languages from 11 families and several areas around
the globe. The dataset is challenging as it requires both the command of world knowledge and the ability to generalise to new languages. All the details about the
creation of XCOPA and the implementation of the baselines are available in the paper.\n
"""

_LANG = ["et", "ht", "it", "id", "qu", "sw", "zh", "ta", "th", "tr", "vi"]

_URL = "https://github.com/cambridgeltl/xcopa/archive/master.zip"


class XcopaConfig(datasets.BuilderConfig):
    """BuilderConfig for Break"""

    def __init__(self, **kwargs):
        """

        Args:
            data_dir: directory for the given language dataset
            **kwargs: keyword arguments forwarded to super.
        """
        super(XcopaConfig, self).__init__(version=datasets.Version("1.0.0", ""), **kwargs)


class Xcopa(datasets.GeneratorBasedBuilder):
    """TODO(xcopa): Short description of my dataset."""

    # TODO(xcopa): Set up version.
    VERSION = datasets.Version("0.1.0")
    BUILDER_CONFIGS = [
        XcopaConfig(
            name=lang,
            description="Xcopa language {}".format(lang),
        )
        for lang in _LANG
    ]

    def _info(self):
        # TODO(xcopa): Specifies the datasets.DatasetInfo object
        return datasets.DatasetInfo(
            # This is the description that will appear on the datasets page.
            description=_DESCRIPTION + self.config.description,
            # datasets.features.FeatureConnectors
            features=datasets.Features(
                {
                    # These are the features of your dataset like images, labels ...
                    "premise": datasets.Value("string"),
                    "choice1": datasets.Value("string"),
                    "choice2": datasets.Value("string"),
                    "question": datasets.Value("string"),
                    "label": datasets.Value("int32"),
                    "idx": datasets.Value("int32"),
                    "changed": datasets.Value("bool"),
                }
            ),
            # If there's a common (input, target) tuple from the features,
            # specify them here. They'll be used if as_supervised=True in
            # builder.as_dataset.
            supervised_keys=None,
            # Homepage of the dataset for documentation
            homepage="https://github.com/cambridgeltl/xcopa",
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        """Returns SplitGenerators."""
        # TODO(xcopa): Downloads the data and defines the splits
        # dl_manager is a datasets.download.DownloadManager that can be used to
        # download and extract URLs
        dl_dir = dl_manager.download_and_extract(_URL)

        data_dir = os.path.join(dl_dir, "xcopa-master", "data", self.config.name)
        return [
            datasets.SplitGenerator(
                name=datasets.Split.TEST,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={"filepath": os.path.join(data_dir, "test." + self.config.name + ".jsonl")},
            ),
            datasets.SplitGenerator(
                name=datasets.Split.VALIDATION,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={"filepath": os.path.join(data_dir, "val." + self.config.name + ".jsonl")},
            ),
        ]

    def _generate_examples(self, filepath):
        """Yields examples."""
        # TODO(xcopa): Yields (key, example) tuples from the dataset
        with open(filepath, encoding="utf-8") as f:
            for row in f:
                data = json.loads(row)
                idx = data["idx"]
                yield idx, data
