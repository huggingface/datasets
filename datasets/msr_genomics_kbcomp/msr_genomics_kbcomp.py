# coding=utf-8
# Copyright 2020 The HuggingFace Datasets Authors and the current dataset script contributor.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


import csv
import os

import datasets


# Find for instance the citation on arxiv or on the dataset repo/website
_CITATION = """\
@inproceedings{toutanova-etal-2016-compositional,
    title = "Compositional Learning of Embeddings for Relation Paths in Knowledge Base and Text",
    author = "Toutanova, Kristina  and
      Lin, Victoria  and
      Yih, Wen-tau  and
      Poon, Hoifung  and
      Quirk, Chris",
    booktitle = "Proceedings of the 54th Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers)",
    month = aug,
    year = "2016",
    address = "Berlin, Germany",
    publisher = "Association for Computational Linguistics",
    url = "https://www.aclweb.org/anthology/P16-1136",
    doi = "10.18653/v1/P16-1136",
    pages = "1434--1444",
}
"""

_DESCRIPTION = """\
The database is derived from the NCI PID Pathway Interaction Database, and the textual mentions are extracted from cooccurring pairs of genes in PubMed abstracts, processed and annotated by Literome (Poon et al. 2014). This dataset was used in the paper “Compositional Learning of Embeddings for Relation Paths in Knowledge Bases and Text” (Toutanova, Lin, Yih, Poon, and Quirk, 2016).
"""

_HOMEPAGE = "https://msropendata.com/datasets/80b4f6e8-5d7c-4abc-9c79-2e51dfedd791"


class MsrGenomicsKbcomp(datasets.GeneratorBasedBuilder):

    VERSION = datasets.Version("1.1.0")

    @property
    def manual_download_instructions(self):
        return """\
  To use msr_genomics_kbcomp you need to download it manually. Please go to its homepage (https://msropendata.com/datasets/80b4f6e8-5d7c-4abc-9c79-2e51dfedd791)and login. Extract all files in one folder and use the path folder in datasets.load_dataset('msr_genomics_kbcomp', data_dir='path/to/folder/folder_name')
  """

    def _info(self):
        return datasets.DatasetInfo(
            # This is the description that will appear on the datasets page.
            description=_DESCRIPTION,
            # datasets.features.FeatureConnectors
            features=datasets.Features(
                {
                    # These are the features of your dataset like images, labels ...
                    "GENE1": datasets.Value("string"),
                    "relation": datasets.features.ClassLabel(
                        names=["Positive_regulation", "Negative_regulation", "Family"]
                    ),
                    "GENE2": datasets.Value("string"),
                }
            ),
            # If there's a common (input, target) tuple from the features,
            # specify them here. They'll be used if as_supervised=True in
            # builder.as_dataset.
            supervised_keys=None,
            # Homepage of the dataset for documentation
            homepage="_HOMEPAGE",
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        """Returns SplitGenerators."""
        # dl_manager is a datasets.download.DownloadManager that can be used to
        # download and extract URLs
        data_dir = os.path.abspath(os.path.expanduser(dl_manager.manual_dir))

        if not os.path.exists(data_dir):
            raise FileNotFoundError(
                f"{data_dir} does not exist. Make sure you insert a manual dir via `datasets.load_dataset('msr_genomics_kbcomp', data_dir=...)` that includes files unzipped from the reclor zip. Manual download instructions: {self.manual_download_instructions}"
            )
        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={"filepath": os.path.join(data_dir, "train.txt")},
            ),
            datasets.SplitGenerator(
                name=datasets.Split.TEST,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={"filepath": os.path.join(data_dir, "test.txt")},
            ),
            datasets.SplitGenerator(
                name=datasets.Split.VALIDATION,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={"filepath": os.path.join(data_dir, "valid.txt")},
            ),
        ]

    def _generate_examples(self, filepath):
        """Yields examples."""
        with open(filepath, encoding="utf-8") as f:
            data = csv.DictReader(f, delimiter="\t", quoting=csv.QUOTE_NONE)
            for id_, row in enumerate(data):
                yield id_, {
                    "GENE1": row["GENE1"],
                    "relation": row["relation"],
                    "GENE2": row["GENE2"],
                }
