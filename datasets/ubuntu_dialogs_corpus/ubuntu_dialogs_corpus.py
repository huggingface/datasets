"""TODO(ubuntu_dialogs_corpus): Add a description here."""

from __future__ import absolute_import, division, print_function

import csv
import os

import nlp


# TODO(ubuntu_dialogs_corpus): BibTeX citation
_CITATION = """\
@article{DBLP:journals/corr/LowePSP15,
  author    = {Ryan Lowe and
               Nissan Pow and
               Iulian Serban and
               Joelle Pineau},
  title     = {The Ubuntu Dialogue Corpus: {A} Large Dataset for Research in Unstructured
               Multi-Turn Dialogue Systems},
  journal   = {CoRR},
  volume    = {abs/1506.08909},
  year      = {2015},
  url       = {http://arxiv.org/abs/1506.08909},
  archivePrefix = {arXiv},
  eprint    = {1506.08909},
  timestamp = {Mon, 13 Aug 2018 16:48:23 +0200},
  biburl    = {https://dblp.org/rec/journals/corr/LowePSP15.bib},
  bibsource = {dblp computer science bibliography, https://dblp.org}
}
"""

# TODO(ubuntu_dialogs_corpus):
_DESCRIPTION = """\
Ubuntu Dialogue Corpus, a dataset containing almost 1 million multi-turn dialogues, with a total of over 7 million utterances and 100 million words. This provides a unique resource for research into building dialogue managers based on neural language models that can make use of large amounts of unlabeled data. The dataset has both the multi-turn property of conversations in the Dialog State Tracking Challenge datasets, and the unstructured nature of interactions from microblog services such as Twitter.
"""


class UbuntuDialogsCorpusConfig(nlp.BuilderConfig):
    """BuilderConfig for UbuntuDialogsCorpus."""

    def __init__(self, features, **kwargs):
        """BuilderConfig for UbuntuDialogsCorpus.

    Args:

      **kwargs: keyword arguments forwarded to super.
    """

        super(UbuntuDialogsCorpusConfig, self).__init__(version=nlp.Version("2.0.0"), **kwargs)
        self.features = features


class UbuntuDialogsCorpus(nlp.GeneratorBasedBuilder):
    """TODO(ubuntu_dialogs_corpus): Short description of my dataset."""

    # TODO(ubuntu_dialogs_corpus): Set up version.
    VERSION = nlp.Version("2.0.0")
    BUILDER_CONFIGS = [
        UbuntuDialogsCorpusConfig(
            name="train", features=["Context", "Utterance", "Label"], description="training features"
        ),
        UbuntuDialogsCorpusConfig(
            name="dev_test",
            features=["Context", "Ground Truth Utterance"] + ["Distractor_" + str(i) for i in range(9)],
            description="test and dev features",
        ),
    ]

    @property
    def manual_download_instructions(self):
        return """\
  Please download the Ubuntu Dialog Corpus from https://github.com/rkadlec/ubuntu-ranking-dataset-creator. Run ./generate.sh -t -s -l to download the
   data. Others arguments are left to their default values here. Please save train.csv, test.csv and valid.csv in the same path"""

    def _info(self):
        # TODO(ubuntu_dialogs_corpus): Specifies the nlp.DatasetInfo object
        features = {feature: nlp.Value("string") for feature in self.config.features}
        if self.config.name == "train":
            features["Label"] = nlp.Value("int32")
        return nlp.DatasetInfo(
            # This is the description that will appear on the datasets page.
            description=_DESCRIPTION,
            # nlp.features.FeatureConnectors
            features=nlp.Features(
                # These are the features of your dataset like images, labels ...
                features
            ),
            # If there's a common (input, target) tuple from the features,
            # specify them here. They'll be used if as_supervised=True in
            # builder.as_dataset.
            supervised_keys=None,
            # Homepage of the dataset for documentation
            homepage="https://github.com/rkadlec/ubuntu-ranking-dataset-creator",
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        """Returns SplitGenerators."""
        # TODO(ubuntu_dialogs_corpus): Downloads the data and defines the splits
        # dl_manager is a nlp.download.DownloadManager that can be used to
        # download and extract URLs
        manual_dir = os.path.abspath(os.path.expanduser(dl_manager.manual_dir))

        if self.config.name == "train":
            return [
                nlp.SplitGenerator(
                    name=nlp.Split.TRAIN,
                    # These kwargs will be passed to _generate_examples
                    gen_kwargs={"filepath": os.path.join(manual_dir, "train.csv")},
                ),
            ]
        else:
            return [
                nlp.SplitGenerator(
                    name=nlp.Split.TEST,
                    # These kwargs will be passed to _generate_examples
                    gen_kwargs={"filepath": os.path.join(manual_dir, "test.csv")},
                ),
                nlp.SplitGenerator(
                    name=nlp.Split.VALIDATION,
                    # These kwargs will be passed to _generate_examples
                    gen_kwargs={"filepath": os.path.join(manual_dir, "valid.csv")},
                ),
            ]

    def _generate_examples(self, filepath):
        """Yields examples."""
        # TODO(ubuntu_dialogs_corpus): Yields (key, example) tuples from the dataset
        with open(filepath) as f:
            data = csv.DictReader(f)
            for id_, row in enumerate(data):
                yield id_, row
