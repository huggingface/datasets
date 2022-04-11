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
# Lint as: python3


import json

import datasets


_CITATION = """\
@article{nadeem2020Stereoset,
  title={Stereoset: Measuring stereotypical bias in pretrained language models},
  author={Nadeem, Moin and Bethke, Anna and Reddy, Siva},
  journal={arXiv preprint arXiv:2004.09456},
  year={2020}
}
"""

_DESCRIPTION = """\
Stereoset is a dataset that measures stereotype bias in language models. Stereoset consists of 17,000 sentences that
measures model preferences across gender, race, religion, and profession.
"""

_LICENSE = "CC BY-SA 4.0"


class StereosetConfig(datasets.BuilderConfig):
    """BuilderConfig"""

    def __init__(self, **kwargs):
        """BuilderConfig

        Args:
          **kwargs: keyword arguments forwarded to super.
        """
        super(StereosetConfig, self).__init__(**kwargs)


class Stereoset(datasets.GeneratorBasedBuilder):

    _DOWNLOAD_URL = "https://github.com/moinnadeem/Stereoset/raw/master/data/dev.json"

    BUILDER_CONFIGS = [
        StereosetConfig(
            name="intersentence", version=datasets.Version("1.0.0"), description="intersentence task for Stereoset"
        ),
        StereosetConfig(
            name="intrasentence", version=datasets.Version("1.0.0"), description="intrasentence task for Stereoset"
        ),
    ]

    def _info(self):
        return datasets.DatasetInfo(
            # This is the description that will appear on the datasets page.
            description=_DESCRIPTION,
            # datasets.features.FeatureConnectors
            features=datasets.Features(
                {
                    "id": datasets.Value("string"),
                    "target": datasets.Value("string"),
                    "bias_type": datasets.Value("string"),
                    "context": datasets.Value("string"),
                    "sentences": datasets.features.Sequence(
                        {
                            "sentence": datasets.Value("string"),
                            "id": datasets.Value("string"),
                            "labels": datasets.features.Sequence(
                                {
                                    "label": datasets.ClassLabel(
                                        names=["anti-stereotype", "stereotype", "unrelated", "related"]
                                    ),
                                    "human_id": datasets.Value("string"),
                                }
                            ),
                            "gold_label": datasets.ClassLabel(names=["anti-stereotype", "stereotype", "unrelated"]),
                        }
                    ),
                    # These are the features of your dataset like images, labels ...
                }
            ),
            # If there's a common (input, target) tuple from the features,
            # specify them here. They'll be used if as_supervised=True in
            # builder.as_dataset.
            supervised_keys=None,
            # Homepage of the dataset for documentation
            homepage="https://Stereoset.mit.edu/",
            citation=_CITATION,
            license=_LICENSE,
        )

    def _split_generators(self, dl_manager):
        """Returns SplitGenerators."""
        # dl_manager is a datasets.download.DownloadManager that can be used to
        # download and extract URLs
        data_path = dl_manager.download_and_extract(self._DOWNLOAD_URL)

        return [
            datasets.SplitGenerator(name=datasets.Split.VALIDATION, gen_kwargs={"filepath": data_path}),
        ]

    def _generate_examples(self, filepath):
        """Yields examples."""
        with open(filepath, encoding="utf-8") as f:
            data = json.load(f)["data"][self.config.name]
            for e in data:
                sentences = []
                for s in e["sentences"]:
                    labels = []
                    for label in s["labels"]:
                        labels.append({"label": label["label"], "human_id": label["human_id"]})
                    sentences.append(
                        {"sentence": s["sentence"], "id": s["id"], "labels": labels, "gold_label": s["gold_label"]}
                    )
                yield e["id"], {
                    "id": e["id"],
                    "target": e["target"],
                    "bias_type": e["bias_type"],
                    "context": e["context"],
                    "sentences": sentences,
                }
