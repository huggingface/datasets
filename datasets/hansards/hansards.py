"""TODO(hansards): Add a description here."""

from __future__ import absolute_import, division, print_function

import glob
import os

import nlp


# TODO(hansards): BibTeX citation
_CITATION = """
"""

# TODO(hansards):
_DESCRIPTION = """
This release contains 1.3 million pairs of aligned text chunks (sentences or smaller fragments)
from the official records (Hansards) of the 36th Canadian Parliament.

The complete Hansards of the debates in the House and Senate of the 36th Canadian Parliament,
as far as available, were aligned. The corpus was then split into 5 sets of sentence pairs:
training (80% of the sentence pairs), two sets of sentence pairs for testing (5% each), and
two sets of sentence pairs for final evaluation (5% each). The current release consists of the
training and testing sets. The evaluation sets are reserved for future MT evaluation purposes
and currently not available.

Caveats
1. This release contains only sentence pairs. Even though the order of the sentences is the same
as in the original, there may be gaps resulting from many-to-one, many-to-many, or one-to-many
alignments that were filtered out. Therefore, this release may not be suitable for
discourse-related research.
2. Neither the sentence splitting nor the alignments are perfect. In particular, watch out for
pairs that differ considerably in length. You may want to filter these out before you do
any statistical training.

The alignment of the Hansards was performed as part of the ReWrite project under funding
from the DARPA TIDES program.
"""

_URL = "https://www.isi.edu/natural-language/download/hansard/"
_DATA_URL = "http://www.isi.edu/natural-language/download/hansard/"
_HOUSE_DEBATES_TRAIN_SET_FILE = "hansard.36.r2001-1a.house.debates.training.tar"
_HOUSE_DEBATES_TEST_SET_FILE = "hansard.36.r2001-1a.house.debates.testing.tar"
_SENATE_DEBATES_TRAIN_SET_FILE = "hansard.36.r2001-1a.senate.debates.training.tar"
_SENATE_DEBATES_TEST_SET_FILE = "hansard.36.r2001-1a.senate.debates.testing.tar"


class HansardsConfig(nlp.BuilderConfig):
    """BuilderConfig for Hansards."""

    def __init__(self, **kwargs):
        """BuilderConfig for Hansards.
        Args:
          **kwargs: keyword arguments forwarded to super.
        """
        super(HansardsConfig, self).__init__(
            version=nlp.Version("1.0.0", "New split API (https://tensorflow.org/datasets/splits)"), **kwargs
        )


class Hansards(nlp.GeneratorBasedBuilder):
    """TODO(hansards): Short description of my dataset."""

    # TODO(hansards): Set up version.
    VERSION = nlp.Version("0.1.0")
    BUILDER_CONFIGS = [
        HansardsConfig(
            name="house",
            description="""\
          Alignment of debates in the House of the 36th Canadian Parliament: 1,070K sentence pairs.
          """,
        ),
        HansardsConfig(
            name="senate",
            description="""\
          Alignment of debates in the Senate of the 36th Canadian Parliament: 208K sentence pairs.
          """,
        ),
    ]

    def _info(self):
        # TODO(hansards): Specifies the nlp.DatasetInfo object
        return nlp.DatasetInfo(
            # This is the description that will appear on the datasets page.
            description=_DESCRIPTION,
            # nlp.features.FeatureConnectors
            features=nlp.Features(
                {
                    "fr": nlp.Value("string"),
                    "en": nlp.Value("string")
                    # These are the features of your dataset like images, labels ...
                }
            ),
            # If there's a common (input, target) tuple from the features,
            # specify them here. They'll be used if as_supervised=True in
            # builder.as_dataset.
            supervised_keys=None,
            # Homepage of the dataset for documentation
            homepage=_URL,
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        """Returns SplitGenerators."""
        # TODO(hansards): Downloads the data and defines the splits
        # dl_manager is a nlp.download.DownloadManager that can be used to
        # download and extract URLs
        name = self.config.name
        if name == "house":
            urls_to_download = {
                "train": os.path.join(_DATA_URL, _HOUSE_DEBATES_TRAIN_SET_FILE),
                "test": os.path.join(_DATA_URL, _HOUSE_DEBATES_TEST_SET_FILE),
            }
        elif name == "senate":
            urls_to_download = {
                "train": os.path.join(_DATA_URL, _SENATE_DEBATES_TRAIN_SET_FILE),
                "test": os.path.join(_DATA_URL, _SENATE_DEBATES_TEST_SET_FILE),
            }
        else:
            raise ValueError("Wrong builder config name '{}', it has to be either 'house' or 'senate'.".format(name))
        downloaded_files = dl_manager.download_and_extract(urls_to_download)
        if type(downloaded_files) == str:
            downloaded_files = {k: downloaded_files for k in urls_to_download.keys()}
        fr_files = {}
        en_files = {}
        for split_name in downloaded_files.keys():
            archive_dir = "hansard.36/Release-2001.1a/sentence-pairs/{}/debates/development/{}".format(
                name, split_name + "ing"
            )
            data_dir = os.path.join(downloaded_files[split_name], archive_dir)
            split_compress_files = list(sorted(glob.glob(os.path.join(data_dir, "*.gz"))))
            split_compress_files += list(sorted(glob.glob(os.path.join(data_dir, "**/*.gz"))))
            fr_split_compress_files = sorted([f for f in split_compress_files if f.endswith(".f.gz")])
            en_split_compress_files = sorted([f for f in split_compress_files if f.endswith(".e.gz")])
            fr_files[split_name] = dl_manager.extract(fr_split_compress_files)
            en_files[split_name] = dl_manager.extract(en_split_compress_files)
        return [
            nlp.SplitGenerator(
                name=nlp.Split.TRAIN,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={"fr_files": fr_files["train"], "en_files": en_files["train"]},
            ),
            nlp.SplitGenerator(
                name=nlp.Split.TEST,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={"fr_files": fr_files["test"], "en_files": en_files["test"]},
            ),
        ]

    def _generate_examples(self, fr_files, en_files):
        """Yields examples."""
        # TODO(hansards): Yields (key, example) tuples from the dataset
        for fr_file, en_file in zip(fr_files, en_files):
            with open(fr_file, "rb") as fr:
                with open(en_file, "rb") as en:
                    for j, (fr_line, en_line) in enumerate(zip(fr, en)):
                        line_id = "{}:{}".format(fr_file, j)
                        rec = {"fr": fr_line.decode("ISO-8859-1").strip(), "en": en_line.decode("ISO-8859-1").strip()}
                        yield line_id, rec
