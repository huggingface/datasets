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
"""Dataset of disentangled IRC"""


import glob
import os
from pathlib import Path

import datasets


_CITATION = """\
@inproceedings{kummerfeld-etal-2019-large,
    title = "A Large-Scale Corpus for Conversation Disentanglement",
    author = "Kummerfeld, Jonathan K.  and
      Gouravajhala, Sai R.  and
      Peper, Joseph J.  and
      Athreya, Vignesh  and
      Gunasekara, Chulaka  and
      Ganhotra, Jatin  and
      Patel, Siva Sankalp  and
      Polymenakos, Lazaros C  and
      Lasecki, Walter",
    booktitle = "Proceedings of the 57th Annual Meeting of the Association for Computational Linguistics",
    month = jul,
    year = "2019",
    address = "Florence, Italy",
    publisher = "Association for Computational Linguistics",
    url = "https://aclanthology.org/P19-1374",
    doi = "10.18653/v1/P19-1374",
    pages = "3846--3856",
    arxiv = "https://arxiv.org/abs/1810.11118",
    software = "https://jkk.name/irc-disentanglement",
    data = "https://jkk.name/irc-disentanglement",
    abstract = "Disentangling conversations mixed together in a single stream of messages is a difficult task, made harder by the lack of large manually annotated datasets. We created a new dataset of 77,563 messages manually annotated with reply-structure graphs that both disentangle conversations and define internal conversation structure. Our data is 16 times larger than all previously released datasets combined, the first to include adjudication of annotation disagreements, and the first to include context. We use our data to re-examine prior work, in particular, finding that 89% of conversations in a widely used dialogue corpus are either missing messages or contain extra messages. Our manually-annotated data presents an opportunity to develop robust data-driven methods for conversation disentanglement, which will help advance dialogue research.",
}
"""

_DESCRIPTION = """\
Disentangling conversations mixed together in a single stream of messages is
a difficult task, made harder by the lack of large manually annotated
datasets. This new dataset of 77,563 messages manually annotated with
reply-structure graphs that both disentangle conversations and define
internal conversation structure. The dataset is 16 times larger than all
previously released datasets combined, the first to include adjudication of
annotation disagreements, and the first to include context.
"""

_HOMEPAGE = "https://jkk.name/irc-disentanglement/"

_LICENSE = "Creative Commons Attribution 4.0 International Public License"

_URL = "https://github.com/jkkummerfeld/irc-disentanglement/tarball/master"


class IRCDisentangle(datasets.GeneratorBasedBuilder):
    """IRCDisentangle dataset"""

    VERSION = datasets.Version("1.0.0")

    BUILDER_CONFIGS = [
        datasets.BuilderConfig(
            name="ubuntu",
            version=VERSION,
            description="This part of the dataset is the annotated conversations from the Ubuntu channel",
        ),
        datasets.BuilderConfig(
            name="channel_two",
            version=VERSION,
            description="This part of the dataset is the annotated conversations from the Channel Two",
        ),
    ]

    DEFAULT_CONFIG_NAME = "ubuntu"

    def _info(self):
        if self.config.name == "ubuntu":
            features = datasets.Features(
                {
                    "id": datasets.Value("int32"),
                    "raw": datasets.Value("string"),
                    "ascii": datasets.Value("string"),
                    "tokenized": datasets.Value("string"),
                    "date": datasets.Value("string"),
                    "connections": datasets.features.Sequence(datasets.Value("int32")),
                }
            )
        elif self.config.name == "channel_two":
            features = datasets.Features(
                {
                    "id": datasets.Value("int32"),
                    "raw": datasets.Value("string"),
                    "ascii": datasets.Value("string"),
                    "tokenized": datasets.Value("string"),
                    "connections": datasets.features.Sequence(datasets.Value("int32")),
                }
            )
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=features,
            supervised_keys=None,
            homepage=_HOMEPAGE,
            license=_LICENSE,
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        """Returns SplitGenerators."""
        my_urls = _URL
        dl_dir = dl_manager.download_and_extract(my_urls)

        files = dict()
        if self.config.name == "ubuntu":
            for split in ["train", "dev", "test"]:
                files[split] = os.path.join(dl_dir, "jkkummerfeld-irc-disentanglement-fd379e9", "data", split)

            return [
                datasets.SplitGenerator(
                    name=datasets.Split.TRAIN,
                    gen_kwargs={
                        "filepath": files["train"],
                        "split": "train",
                    },
                ),
                datasets.SplitGenerator(
                    name=datasets.Split.TEST,
                    gen_kwargs={
                        "filepath": files["test"],
                        "split": "test",
                    },
                ),
                datasets.SplitGenerator(
                    name=datasets.Split.VALIDATION,
                    gen_kwargs={
                        "filepath": files["dev"],
                        "split": "dev",
                    },
                ),
            ]

        elif self.config.name == "channel_two":
            filepath = os.path.join(dl_dir, "jkkummerfeld-irc-disentanglement-fd379e9", "data", "channel-two")
            return [
                datasets.SplitGenerator(
                    name="dev",
                    gen_kwargs={
                        "filepath": filepath,
                        "split": "dev",
                    },
                ),
                datasets.SplitGenerator(
                    name="pilot",
                    gen_kwargs={
                        "filepath": filepath,
                        "split": "pilot",
                    },
                ),
                datasets.SplitGenerator(
                    name="test",
                    gen_kwargs={
                        "filepath": filepath,
                        "split": "test",
                    },
                ),
                datasets.SplitGenerator(
                    name="pilot_dev",
                    gen_kwargs={
                        "filepath": filepath,
                        "split": "pilot-dev",
                    },
                ),
                datasets.SplitGenerator(
                    name="all_",
                    gen_kwargs={
                        "filepath": filepath,
                        "split": "all",
                    },
                ),
            ]

    def _generate_examples(self, filepath, split):
        """Yields examples."""

        if self.config.name == "ubuntu":
            # run loop for each date
            all_files = sorted(glob.glob(os.path.join(filepath, "*.annotation.txt")))
            all_dates = [Path(filename).name[:10] for filename in all_files]
            all_info = [Path(filename).name[10:-15] for filename in all_files]

        elif self.config.name == "channel_two":
            # run loop once (there are no dates for this config)
            all_dates = ["_"]
            all_info = ["_"]

        last_id = 0
        id_ = 0

        for date, info in zip(all_dates, all_info):

            if self.config.name == "ubuntu":
                # load file of given date and additional info for each split
                raw_path = os.path.join(filepath, f"{date}{info}.raw.txt")
                ascii_path = os.path.join(filepath, f"{date}{info}.ascii.txt")
                tok_path = os.path.join(filepath, f"{date}{info}.tok.txt")
                annot_path = os.path.join(filepath, f"{date}{info}.annotation.txt")

            elif self.config.name == "channel_two":
                # load files of different splits
                raw_path = os.path.join(filepath, f"channel-two.{split}.raw.txt")
                ascii_path = os.path.join(filepath, f"channel-two.{split}.ascii.txt")
                tok_path = os.path.join(filepath, f"channel-two.{split}.tok.txt")
                annot_path = os.path.join(filepath, f"channel-two.{split}.annotation.txt")

            with open(raw_path, encoding="utf-8") as f_raw, open(ascii_path, encoding="utf-8") as f_ascii, open(
                tok_path, encoding="utf-8"
            ) as f_tok, open(annot_path, encoding="utf-8") as f_annot:

                # tokenize txt file
                raw_sentences = f_raw.read().split("\n")
                ascii_sentences = f_ascii.read().split("\n")
                tok_sentences = f_tok.read().split("\n")
                annot_lines = f_annot.read().split("\n")

            assert (
                len(raw_sentences) == len(ascii_sentences) == len(tok_sentences)
            ), "Sizes do not match: %d vs %d vs %d for Raw Sentences vs Ascii Sentences vs Tokenized Sentences." % (
                len(raw_sentences),
                len(ascii_sentences),
                len(tok_sentences),
            )

            annotation_pairs = []

            # for annotation lines, make annotation pairs
            for annot in annot_lines:
                line = annot.split(" ")
                if len(line) > 1:
                    annotation_pairs.append((int(line[0]), int(line[1])))

            annotations = dict()
            for row in range(last_id, last_id + len(raw_sentences)):
                annotations[row] = set()

            for (a, b) in annotation_pairs:
                # required for dummy data creation
                if last_id + a not in annotations:
                    annotations[last_id + a] = set()
                if last_id + b not in annotations:
                    annotations[last_id + b] = set()

                # add annotation 'b' to a's annotation set, and vice versa
                annotations[last_id + a].add(last_id + b)
                annotations[last_id + b].add(last_id + a)

            for i in range(len(raw_sentences)):
                # return all 3 kinds of chat messages, the date (if applicable), and the annotation set for that sentece
                if self.config.name == "ubuntu":
                    yield id_, {
                        "id": id_,
                        "raw": raw_sentences[i],
                        "ascii": ascii_sentences[i],
                        "tokenized": tok_sentences[i],
                        "date": date,
                        "connections": sorted(annotations[id_]),
                    }
                elif self.config.name == "channel_two":
                    yield id_, {
                        "id": id_,
                        "raw": raw_sentences[i],
                        "ascii": ascii_sentences[i],
                        "tokenized": tok_sentences[i],
                        "connections": sorted(annotations[i]),
                    }
                id_ += 1

            # continue counting from position last left off
            last_id = id_
