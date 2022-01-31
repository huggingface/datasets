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
"""The Pile dataset."""

import json

import datasets


_CITATION = """\
@misc{gao2020pile,
      title={The Pile: An 800GB Dataset of Diverse Text for Language Modeling},
      author={Leo Gao and Stella Biderman and Sid Black and Laurence Golding and Travis Hoppe and Charles Foster and Jason Phang and Horace He and Anish Thite and Noa Nabeshima and Shawn Presser and Connor Leahy},
      year={2020},
      eprint={2101.00027},
      archivePrefix={arXiv},
      primaryClass={cs.CL}
}
"""

_DESCRIPTION = """\
The Pile is a 825 GiB diverse, open source language modelling data set that consists of 22 smaller, high-quality
datasets combined together.
"""

_HOMEPAGE = "https://pile.eleuther.ai/"

_LICENSES = {
    "all": "Multiple: see each subset license",
    "enron_emails": "Unknown",
    "europarl": "Unknown",
    "free_law": "Unknown",
    "hacker_news": "Unknown",
    "nih_exporter": "Unknown",
    "pubmed": "Unknown",
    "pubmed_central": "Unknown",
    "ubuntu_irc": "Unknown",
    "uspto": "Unknown",
}

_DATA_URLS = {
    "all": {
        "train": [f"https://the-eye.eu/public/AI/pile/train/{i:0>2}.jsonl.zst" for i in range(30)],
        "validation": ["https://the-eye.eu/public/AI/pile/val.jsonl.zst"],
        "test": ["https://the-eye.eu/public/AI/pile/test.jsonl.zst"],
    },
    "enron_emails": "http://eaidata.bmk.sh/data/enron_emails.jsonl.zst",
    "europarl": "https://the-eye.eu/public/AI/pile_preliminary_components/EuroParliamentProceedings_1996_2011.jsonl.zst",
    "free_law": "https://the-eye.eu/public/AI/pile_preliminary_components/FreeLaw_Opinions.jsonl.zst",
    "hacker_news": "https://the-eye.eu/public/AI/pile_preliminary_components/hn.tar.gz",
    "nih_exporter": "https://the-eye.eu/public/AI/pile_preliminary_components/NIH_ExPORTER_awarded_grant_text.jsonl.zst",
    "pubmed": "https://the-eye.eu/public/AI/pile_preliminary_components/PUBMED_title_abstracts_2019_baseline.jsonl.zst",
    "pubmed_central": "https://the-eye.eu/public/AI/pile_preliminary_components/PMC_extracts.tar.gz",
    "ubuntu_irc": "https://the-eye.eu/public/AI/pile_preliminary_components/ubuntu_irc_until_2020_9_1.jsonl.zst",
    "uspto": "https://the-eye.eu/public/AI/pile_preliminary_components/pile_uspto.tar",
}

_FEATURES = {
    "all": datasets.Features(
        {
            "text": datasets.Value("string"),
            "meta": {"pile_set_name": datasets.Value("string")},
        }
    ),
    "enron_emails": datasets.Features(
        {
            "text": datasets.Value("string"),
            "meta": datasets.Value("string"),
        }
    ),
    "europarl": datasets.Features(
        {
            "text": datasets.Value("string"),
            "meta": datasets.Value("string"),
        }
    ),
    "free_law": datasets.Features(
        {
            "text": datasets.Value("string"),
            "meta": datasets.Value("string"),
        }
    ),
    "hacker_news": datasets.Features(
        {
            "text": datasets.Value("string"),
            "meta": datasets.Value("string"),
        }
    ),
    "nih_exporter": datasets.Features(
        {
            "text": datasets.Value("string"),
            "meta": datasets.Value("string"),
        }
    ),
    "pubmed": datasets.Features(
        {
            "text": datasets.Value("string"),
            "meta": datasets.Value("string"),
        }
    ),
    "pubmed_central": datasets.Features(
        {
            "text": datasets.Value("string"),
            "meta": datasets.Value("string"),
        }
    ),
    "ubuntu_irc": datasets.Features(
        {
            "text": datasets.Value("string"),
            "meta": datasets.Value("string"),
        }
    ),
    "uspto": datasets.Features(
        {
            "text": datasets.Value("string"),
            "meta": datasets.Value("string"),
        }
    ),
}


class ThePileConfig(datasets.BuilderConfig):
    """BuilderConfig for The Pile."""

    def __init__(self, *args, subsets, **kwargs):
        """BuilderConfig for The Pile.

        Args:
            subsets (:obj:`List[str]`): List of subsets to load.
            **kwargs: keyword arguments forwarded to super.
        """
        super().__init__(
            *args,
            name="+".join(subsets),
            **kwargs,
        )
        self.subsets = subsets


class ThePile(datasets.GeneratorBasedBuilder):
    """The Pile dataset."""

    VERSION = datasets.Version("1.1.0")

    BUILDER_CONFIG_CLASS = ThePileConfig
    BUILDER_CONFIGS = [ThePileConfig(subsets=[subset]) for subset in _DATA_URLS]
    DEFAULT_CONFIG_NAME = "all"

    def _info(self):
        """Give information and typings for the dataset."""
        return datasets.DatasetInfo(
            # This is the description that will appear on the datasets page.
            description=_DESCRIPTION,
            # This defines the different columns of the dataset and their types
            features=_FEATURES.get(self.config.name),
            # If there's a common (input, target) tuple from the features,
            # specify them here. They'll be used if as_supervised=True in
            # builder.as_dataset.
            supervised_keys=None,
            # Homepage of the dataset for documentation
            homepage=_HOMEPAGE,
            # License for the dataset if available
            license=_LICENSES.get(self.config.name, "Multiple: see each subset license"),
            # Citation for the dataset
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        """Return SplitGenerators."""
        if self.config.name == "all":
            data_dir = dl_manager.download(_DATA_URLS[self.config.name])
            return [
                datasets.SplitGenerator(
                    name=split,
                    gen_kwargs={
                        "files": data_dir[split],
                    },
                )
                for split in [datasets.Split.TRAIN, datasets.Split.VALIDATION, datasets.Split.TEST]
            ]
        else:
            data_urls = {subset: _DATA_URLS[subset] for subset in self.config.subsets}
            archive = dl_manager.download(data_urls)
            return [
                datasets.SplitGenerator(
                    name=datasets.Split.TRAIN,
                    gen_kwargs={
                        "files": {
                            subset: dl_manager.iter_archive(archive[subset])
                            if ".tar" in data_urls[subset]
                            else archive[subset]
                            for subset in self.config.subsets
                        },
                    },
                ),
            ]

    def _generate_examples(self, files):
        """Yield examples as (key, example) tuples."""
        key = 0
        if isinstance(files, list):
            import zstandard as zstd

            for path in files:
                with zstd.open(open(path, "rb"), "rt", encoding="utf-8") as f:
                    for row in f:
                        data = json.loads(row)
                        yield key, data
                        key += 1
        else:
            for subset in files:
                if subset in {"enron_emails", "europarl", "free_law", "nih_exporter", "pubmed", "ubuntu_irc"}:
                    import zstandard as zstd

                    with zstd.open(open(files[subset], "rb"), "rt", encoding="utf-8") as f:
                        for row in f:
                            data = json.loads(row)
                            yield key, data
                            key += 1
                elif subset in {"hacker_news", "pubmed_central"}:
                    for path, file in files[subset]:
                        id_ = path.split("/")[-1].split(".")[0]
                        meta = {"id": id_}
                        text = file.read().decode("utf-8")
                        yield key, {
                            "text": text,
                            "meta": meta,
                        }
                        key += 1
                elif subset == "uspto":
                    import zstandard as zstd

                    for path, file in files[subset]:
                        with zstd.open(file, "rt", encoding="utf-8") as f:
                            for row in f:
                                data = json.loads(row)
                                yield key, data
                                key += 1
