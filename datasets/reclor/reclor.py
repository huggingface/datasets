"""TODO(reclor): Add a description here."""

from __future__ import absolute_import, division, print_function

import json
import os

import datasets


# TODO(reclor): BibTeX citation
_CITATION = """\
@inproceedings{yu2020reclor,
        author = {Yu, Weihao and Jiang, Zihang and Dong, Yanfei and Feng, Jiashi},
        title = {ReClor: A Reading Comprehension Dataset Requiring Logical Reasoning},
        booktitle = {International Conference on Learning Representations (ICLR)},
        month = {April},
        year = {2020}
    }

"""

# TODO(reclor):
_DESCRIPTION = """\
Logical reasoning is an important ability to examine, analyze, and critically evaluate arguments as they occur in ordinary
language as the definition from LSAC. ReClor is a dataset extracted from logical reasoning questions of standardized graduate
admission examinations. Empirical results show that the state-of-the-art models struggle on ReClor with poor performance
indicating more research is needed to essentially enhance the logical reasoning ability of current models. We hope this
dataset could help push Machine Reading Comprehension (MRC) towards more complicated reasonin
"""


class Reclor(datasets.GeneratorBasedBuilder):
    """TODO(reclor): Short description of my dataset."""

    # TODO(reclor): Set up version.
    VERSION = datasets.Version("0.1.0")

    @property
    def manual_download_instructions(self):
        return """\
  to use ReClor you need to download it manually. Please go to its homepage (http://whyu.me/reclor/) fill the google
  form and you will receive a download link and a password to extract it.Please extract all files in one folder and use the path folder in datasets.load_dataset('reclor', data_dir='path/to/folder/folder_name')
  """

    def _info(self):
        # TODO(reclor): Specifies the datasets.DatasetInfo object
        return datasets.DatasetInfo(
            # This is the description that will appear on the datasets page.
            description=_DESCRIPTION,
            # datasets.features.FeatureConnectors
            features=datasets.Features(
                {
                    # These are the features of your dataset like images, labels ...
                    "context": datasets.Value("string"),
                    "question": datasets.Value("string"),
                    "answers": datasets.features.Sequence(datasets.Value("string")),
                    "label": datasets.Value("string"),
                    "id_string": datasets.Value("string"),
                }
            ),
            # If there's a common (input, target) tuple from the features,
            # specify them here. They'll be used if as_supervised=True in
            # builder.as_dataset.
            supervised_keys=None,
            # Homepage of the dataset for documentation
            homepage="http://whyu.me/reclor/",
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        """Returns SplitGenerators."""
        # TODO(reclor): Downloads the data and defines the splits
        # dl_manager is a datasets.download.DownloadManager that can be used to
        # download and extract URLs
        data_dir = os.path.abspath(os.path.expanduser(dl_manager.manual_dir))

        if not os.path.exists(data_dir):
            raise FileNotFoundError(
                "{} does not exist. Make sure you insert a manual dir via `datasets.load_dataset('wikihow', data_dir=...)` that includes files unzipped from the reclor zip. Manual download instructions: {}".format(
                    data_dir, self.manual_download_instructions
                )
            )
        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={"filepath": os.path.join(data_dir, "train.json")},
            ),
            datasets.SplitGenerator(
                name=datasets.Split.TEST,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={"filepath": os.path.join(data_dir, "test.json")},
            ),
            datasets.SplitGenerator(
                name=datasets.Split.VALIDATION,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={"filepath": os.path.join(data_dir, "val.json")},
            ),
        ]

    def _generate_examples(self, filepath):
        """Yields examples."""
        # TODO(reclor): Yields (key, example) tuples from the dataset
        with open(filepath, encoding="utf-8") as f:
            data = json.load(f)
            for id_, row in enumerate(data):
                yield id_, {
                    "context": row["context"],
                    "question": row["question"],
                    "answers": row["answers"],
                    "label": str(row.get("label", "")),
                    "id_string": row["id_string"],
                }
