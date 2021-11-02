# coding=utf-8
# Copyright 2021 The HuggingFace Datasets Authors and the current dataset script contributor.
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
"""The Stack Exchange Corpus"""

import os
from pathlib import Path

import datasets


_CITATION = """\
@article{pile,
    title={The {P}ile: An 800GB Dataset of Diverse Text for Language Modeling},
    author={Gao, Leo and Biderman, Stella and Black, Sid and Golding, Laurence and Hoppe, Travis and Foster, Charles and Phang, Jason and He, Horace and Thite, Anish and Nabeshima, Noa and Presser, Shawn and Leahy, Connor},
    journal={arXiv preprint arXiv:2101.00027},
    year={2020}
}
"""

_DESCRIPTION = """\
This dataset is part of EleutherAI/The Pile dataset and is a dataset for Language Models from processing stackexchange data dump, \
which is an anonymized dump of all user-contributed content on the Stack Exchange network.
"""

_URL = "https://the-eye.eu/public/AI/pile_preliminary_components/stackexchange_dataset.tar"


class ThePileStackExchange(datasets.GeneratorBasedBuilder):
    """The StackExchange dataset."""

    BUILDER_CONFIGS = [
        datasets.BuilderConfig(
            name="plain_text",
            description="Plain text",
            version=datasets.Version("1.0.0"),
        )
    ]

    def _info(self):
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=datasets.Features({"domain": datasets.Value("string"), "text": datasets.Value("string")}),
            homepage="https://github.com/EleutherAI/stackexchange-dataset",
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        dl_dir = dl_manager.download_and_extract(_URL)
        zips = [str(f) for f in (Path(dl_dir) / "out").iterdir()]
        extracted = dl_manager.extract(zips, num_proc=os.cpu_count())
        # non-dir extracteds are zero-size unknown things
        dirs = [path for path in extracted if os.path.isdir(path)]
        return [
            datasets.SplitGenerator(name=datasets.Split.TRAIN, gen_kwargs={"dirs": dirs}),
        ]

    def _generate_examples(self, dirs):
        """Yields examples."""
        _id = 0
        for dir in sorted(dirs):
            txt_files = sorted(Path(dir).glob("**/*.txt"))
            for txt_file in txt_files:
                # PosiPath(/home/user/.cache/huggingface/datasets/downloads/extracted/3923d60abeeb876021dc55a897ac2f260b181556f8ca56a7c61e3b8b80afec77/academia.stackexchange_0000000001.txt)
                domain = txt_file.name.split(".")[0]
                with txt_file.open(mode="r", encoding="utf-8") as f:
                    document = f.read()
                yield _id, {"domain": domain, "text": document}
                _id += 1
