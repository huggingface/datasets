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
"""The OpenWebText2 Corpus"""


import glob
import io
import json
import os

import zstandard

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
OpenWebText2 is part of EleutherAi/The Pile dataset and is an enhanced version of the original OpenWebTextCorpus \
covering all Reddit submissions from 2005 up until April 2020, \
with further months becoming available after the corresponding PushShift dump files are released.
"""

_URL = "https://the-eye.eu/public/AI/pile_preliminary_components/openwebtext2.jsonl.zst.tar"


class Openwebtext2(datasets.GeneratorBasedBuilder):
    """The OpenWebText2 dataset."""

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
            features=datasets.Features(
                {
                    "title": datasets.Value("string"),
                    "text": datasets.Value("string"),
                    "reddit_scores": datasets.Sequence(datasets.Value("int8")),
                }
            ),
            homepage="https://openwebtext2.readthedocs.io/en/latest/",
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        dl_dir = dl_manager.download_and_extract(_URL)
        files = glob.glob(os.path.join(dl_dir, "*jsonl.zst"))
        return [
            datasets.SplitGenerator(name=datasets.Split.TRAIN, gen_kwargs={"files": files}),
        ]

    def _generate_examples(self, files):
        """Yields examples."""
        _id = 0
        for file_path in files:
            reader = Reader()
            for document, metadata in reader.read_jsonl(file_path, get_meta=True):
                yield _id, {
                    "title": metadata["title"],
                    "text": document,
                    "reddit_scores": metadata["reddit_scores"],
                }
                _id += 1


# Modified version of lm_dataformat Reader with self.fh set, allowing peeking for tqdm.
class Reader:
    def __init__(self):
        pass

    def read_jsonl(self, file, get_meta=False, autojoin_paragraphs=True, para_joiner="\n\n"):
        with open(file, "rb") as fh:
            self.fh = fh
            cctx = zstandard.ZstdDecompressor()
            reader = io.BufferedReader(cctx.stream_reader(fh))
            for line in reader:
                ob = json.loads(line)
                # naive jsonl where each object is just the string itself, with no meta. For legacy compatibility.
                if isinstance(ob, str):
                    assert not get_meta
                    yield ob
                    continue

                text = ob["text"]

                if autojoin_paragraphs and isinstance(text, list):
                    text = para_joiner.join(text)

                if get_meta:
                    yield text, (ob["meta"] if "meta" in ob else {})
                else:
                    yield text
