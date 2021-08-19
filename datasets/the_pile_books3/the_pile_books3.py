# coding=utf-8
# Copyright 2021 The TensorFlow Datasets Authors and the HuggingFace Datasets Authors.
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
"""The BookCorpus dataset based on Shawn Presser's work https://github.com/soskek/bookcorpus/issues/27 """


from pathlib import Path

import datasets


_DESCRIPTION = """\
This dataset is Shawn Presser's work and is part of EleutherAi/The Pile dataset. \
This dataset contains all of bibliotik in plain .txt form, aka 197,000 books processed in exactly \
the same way as did for bookcorpusopen (a.k.a. books1). seems to be similar to OpenAI's mysterious \
"books2" dataset referenced in their papers. Unfortunately OpenAI will not give details, so we know \
very little about any differences. People suspect it's "all of libgen", but it's purely conjecture.
"""

_CITATION = """\
@article{pile,
    title={The {P}ile: An 800GB Dataset of Diverse Text for Language Modeling},
    author={Gao, Leo and Biderman, Stella and Black, Sid and Golding, Laurence and Hoppe, Travis and Foster, Charles and Phang, Jason and He, Horace and Thite, Anish and Nabeshima, Noa and Presser, Shawn and Leahy, Connor},
    journal={arXiv preprint arXiv:2101.00027},
    year={2020}
}
"""
_PROJECT_URL = "https://github.com/soskek/bookcorpus/issues/27#issuecomment-716104208"
_DOWNLOAD_URL = "https://the-eye.eu/public/AI/pile_preliminary_components/books3.tar.gz"


class Books3Config(datasets.BuilderConfig):
    """BuilderConfig for ThePileBooks3."""

    def __init__(self, **kwargs):
        """BuilderConfig for ThePileBooks3.
        Args:
        **kwargs: keyword arguments forwarded to super.
        """
        super(Books3Config, self).__init__(version=datasets.Version("1.0.0", ""), **kwargs)


class ThePileBooks3(datasets.GeneratorBasedBuilder):
    """Books3 dataset."""

    BUILDER_CONFIGS = [
        Books3Config(
            name="plain_text",
            description="Plain text",
        )
    ]
    # Every example is a whole book thus big, adjust writer_batch_size to avoid OOM at the cost of writing speed
    DEFAULT_WRITER_BATCH_SIZE = 500

    def _info(self):
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=datasets.Features(
                {
                    "title": datasets.Value("string"),
                    "text": datasets.Value("string"),
                }
            ),
            supervised_keys=None,
            homepage=_PROJECT_URL,
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        extracted_dir = dl_manager.download_and_extract(_DOWNLOAD_URL)
        leaf_dirs = Path(extracted_dir).glob("**/Bibliotik/*")
        leaf_dirs = sorted(leaf_dirs)

        return [
            datasets.SplitGenerator(name=datasets.Split.TRAIN, gen_kwargs={"leaf_dirs": leaf_dirs}),
        ]

    def _generate_examples(self, leaf_dirs):
        _id = 0
        for leaf_dir in leaf_dirs:
            for path in sorted(leaf_dir.glob("**/*.epub.txt")):
                with path.open(mode="r", encoding="utf-8") as f:
                    entry = {"title": path.name, "text": f.read()}
                yield _id, entry
                _id += 1
