# coding=utf-8
# Copyright 2020 The TensorFlow Datasets Authors and the HuggingFace Datasets Authors.
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
"""CNN/DailyMail Summarization dataset, non-anonymized version."""

import hashlib
import os

import datasets


logger = datasets.logging.get_logger(__name__)


_HOMEPAGE = "https://github.com/abisee/cnn-dailymail"

_DESCRIPTION = """\
CNN/DailyMail non-anonymized summarization dataset.

There are two features:
  - article: text of news article, used as the document to be summarized
  - highlights: joined text of highlights with <s> and </s> around each
    highlight, which is the target summary
"""

# The second citation introduces the source data, while the first
# introduces the specific form (non-anonymized) we use here.
_CITATION = """\
@article{DBLP:journals/corr/SeeLM17,
  author    = {Abigail See and
               Peter J. Liu and
               Christopher D. Manning},
  title     = {Get To The Point: Summarization with Pointer-Generator Networks},
  journal   = {CoRR},
  volume    = {abs/1704.04368},
  year      = {2017},
  url       = {http://arxiv.org/abs/1704.04368},
  archivePrefix = {arXiv},
  eprint    = {1704.04368},
  timestamp = {Mon, 13 Aug 2018 16:46:08 +0200},
  biburl    = {https://dblp.org/rec/bib/journals/corr/SeeLM17},
  bibsource = {dblp computer science bibliography, https://dblp.org}
}

@inproceedings{hermann2015teaching,
  title={Teaching machines to read and comprehend},
  author={Hermann, Karl Moritz and Kocisky, Tomas and Grefenstette, Edward and Espeholt, Lasse and Kay, Will and Suleyman, Mustafa and Blunsom, Phil},
  booktitle={Advances in neural information processing systems},
  pages={1693--1701},
  year={2015}
}
"""

_DL_URLS = {
    "cnn_stories": "https://huggingface.co/datasets/cnn_dailymail/resolve/11343c3752184397d56efc19a8a7cceb68089318/data/cnn_stories.tgz",
    "dm_stories": "https://huggingface.co/datasets/cnn_dailymail/resolve/11343c3752184397d56efc19a8a7cceb68089318/data/dailymail_stories.tgz",
    "train": "https://raw.githubusercontent.com/abisee/cnn-dailymail/master/url_lists/all_train.txt",
    "validation": "https://raw.githubusercontent.com/abisee/cnn-dailymail/master/url_lists/all_val.txt",
    "test": "https://raw.githubusercontent.com/abisee/cnn-dailymail/master/url_lists/all_test.txt",
}

_HIGHLIGHTS = "highlights"
_ARTICLE = "article"

_SUPPORTED_VERSIONS = [
    # Using cased version.
    datasets.Version("3.0.0", "Using cased version."),
    # Same data as 0.0.2
    datasets.Version("1.0.0", ""),
    # Having the model predict newline separators makes it easier to evaluate
    # using summary-level ROUGE.
    datasets.Version("2.0.0", "Separate target sentences with newline."),
]


_DEFAULT_VERSION = datasets.Version("3.0.0", "Using cased version.")


class CnnDailymailConfig(datasets.BuilderConfig):
    """BuilderConfig for CnnDailymail."""

    def __init__(self, **kwargs):
        """BuilderConfig for CnnDailymail.

        Args:

          **kwargs: keyword arguments forwarded to super.
        """
        super(CnnDailymailConfig, self).__init__(**kwargs)


def _get_url_hashes(path):
    """Get hashes of urls in file."""
    urls = _read_text_file_path(path)

    def url_hash(u):
        h = hashlib.sha1()
        try:
            u = u.encode("utf-8")
        except UnicodeDecodeError:
            logger.error("Cannot hash url: %s", u)
        h.update(u)
        return h.hexdigest()

    return {url_hash(u) for u in urls}


def _get_hash_from_path(p):
    """Extract hash from path."""
    return os.path.splitext(os.path.basename(p))[0]


DM_SINGLE_CLOSE_QUOTE = "\u2019"  # unicode
DM_DOUBLE_CLOSE_QUOTE = "\u201d"
# acceptable ways to end a sentence
END_TOKENS = [".", "!", "?", "...", "'", "`", '"', DM_SINGLE_CLOSE_QUOTE, DM_DOUBLE_CLOSE_QUOTE, ")"]


def _read_text_file_path(path):
    with open(path, "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f]
    return lines


def _read_text_file(file):
    return [line.decode("utf-8").strip() for line in file]


def _get_art_abs(story_file, tfds_version):
    """Get abstract (highlights) and article from a story file path."""
    # Based on https://github.com/abisee/cnn-dailymail/blob/master/
    #     make_datafiles.py

    lines = _read_text_file(story_file)

    # The github code lowercase the text and we removed it in 3.0.0.

    # Put periods on the ends of lines that are missing them
    # (this is a problem in the dataset because many image captions don't end in
    # periods; consequently they end up in the body of the article as run-on
    # sentences)
    def fix_missing_period(line):
        """Adds a period to a line that is missing a period."""
        if "@highlight" in line:
            return line
        if not line:
            return line
        if line[-1] in END_TOKENS:
            return line
        return line + " ."

    lines = [fix_missing_period(line) for line in lines]

    # Separate out article and abstract sentences
    article_lines = []
    highlights = []
    next_is_highlight = False
    for line in lines:
        if not line:
            continue  # empty line
        elif line.startswith("@highlight"):
            next_is_highlight = True
        elif next_is_highlight:
            highlights.append(line)
        else:
            article_lines.append(line)

    # Make article into a single string
    article = " ".join(article_lines)

    if tfds_version >= "2.0.0":
        abstract = "\n".join(highlights)
    else:
        abstract = " ".join(highlights)

    return article, abstract


class CnnDailymail(datasets.GeneratorBasedBuilder):
    """CNN/DailyMail non-anonymized summarization dataset."""

    BUILDER_CONFIGS = [
        CnnDailymailConfig(name=str(version), description="Plain text", version=version)
        for version in _SUPPORTED_VERSIONS
    ]

    def _info(self):
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=datasets.Features(
                {
                    _ARTICLE: datasets.Value("string"),
                    _HIGHLIGHTS: datasets.Value("string"),
                    "id": datasets.Value("string"),
                }
            ),
            supervised_keys=None,
            homepage=_HOMEPAGE,
            citation=_CITATION,
        )

    def _vocab_text_gen(self, paths):
        for _, ex in self._generate_examples(paths):
            yield " ".join([ex[_ARTICLE], ex[_HIGHLIGHTS]])

    def _split_generators(self, dl_manager):
        dl_paths = dl_manager.download(_DL_URLS)
        return [
            datasets.SplitGenerator(
                name=split,
                gen_kwargs={
                    "urls_file": dl_paths[split],
                    "files_per_archive": [
                        dl_manager.iter_archive(dl_paths["cnn_stories"]),
                        dl_manager.iter_archive(dl_paths["dm_stories"]),
                    ],
                },
            )
            for split in [datasets.Split.TRAIN, datasets.Split.VALIDATION, datasets.Split.TEST]
        ]

    def _generate_examples(self, urls_file, files_per_archive):
        urls = _get_url_hashes(urls_file)
        idx = 0
        for files in files_per_archive:
            for path, file in files:
                hash_from_path = _get_hash_from_path(path)
                if hash_from_path in urls:
                    article, highlights = _get_art_abs(file, self.config.version)
                    if not article or not highlights:
                        continue
                    yield idx, {
                        _ARTICLE: article,
                        _HIGHLIGHTS: highlights,
                        "id": hash_from_path,
                    }
                    idx += 1
