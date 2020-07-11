# coding=utf-8
# Copyright 2020 The TensorFlow Datasets Authors and the HuggingFace NLP Authors.
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
from __future__ import absolute_import, division, print_function

import hashlib
import logging
import os

import nlp


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
    # pylint: disable=line-too-long
    "cnn_stories": "https://drive.google.com/uc?export=download&id=0BwmD_VLjROrfTHk4NFg2SndKcjQ",
    "dm_stories": "https://drive.google.com/uc?export=download&id=0BwmD_VLjROrfM1BxdkxVaTY2bWs",
    "test_urls": "https://raw.githubusercontent.com/abisee/cnn-dailymail/master/url_lists/all_test.txt",
    "train_urls": "https://raw.githubusercontent.com/abisee/cnn-dailymail/master/url_lists/all_train.txt",
    "val_urls": "https://raw.githubusercontent.com/abisee/cnn-dailymail/master/url_lists/all_val.txt",
    # pylint: enable=line-too-long
}

_HIGHLIGHTS = "highlights"
_ARTICLE = "article"

_SUPPORTED_VERSIONS = [
    # Using cased version.
    nlp.Version("3.0.0", "Using cased version."),
    # Same data as 0.0.2
    nlp.Version("1.0.0", "New split API (https://tensorflow.org/datasets/splits)"),
    # Having the model predict newline separators makes it easier to evaluate
    # using summary-level ROUGE.
    nlp.Version("2.0.0", "Separate target sentences with newline."),
]


_DEFAULT_VERSION = nlp.Version("3.0.0", "Using cased version.")


class CnnDailymailConfig(nlp.BuilderConfig):
    """BuilderConfig for CnnDailymail."""

    def __init__(self, **kwargs):
        """BuilderConfig for CnnDailymail.

    Args:

      **kwargs: keyword arguments forwarded to super.
    """
        super(CnnDailymailConfig, self).__init__(**kwargs)


def _get_url_hashes(path):
    """Get hashes of urls in file."""
    urls = _read_text_file(path)

    def url_hash(u):
        h = hashlib.sha1()
        try:
            u = u.encode("utf-8")
        except UnicodeDecodeError:
            logging.error("Cannot hash url: %s", u)
        h.update(u)
        return h.hexdigest()

    return {url_hash(u): True for u in urls}


def _get_hash_from_path(p):
    """Extract hash from path."""
    basename = os.path.basename(p)
    return basename[0 : basename.find(".story")]


def _find_files(dl_paths, publisher, url_dict):
    """Find files corresponding to urls."""
    if publisher == "cnn":
        top_dir = os.path.join(dl_paths["cnn_stories"], "cnn", "stories")
    elif publisher == "dm":
        top_dir = os.path.join(dl_paths["dm_stories"], "dailymail", "stories")
    else:
        logging.fatal("Unsupported publisher: %s", publisher)
    files = sorted(os.listdir(top_dir))

    ret_files = []
    for p in files:
        if _get_hash_from_path(p) in url_dict:
            ret_files.append(os.path.join(top_dir, p))
    return ret_files


def _subset_filenames(dl_paths, split):
    """Get filenames for a particular split."""
    assert isinstance(dl_paths, dict), dl_paths
    # Get filenames for a split.
    if split == nlp.Split.TRAIN:
        urls = _get_url_hashes(dl_paths["train_urls"])
    elif split == nlp.Split.VALIDATION:
        urls = _get_url_hashes(dl_paths["val_urls"])
    elif split == nlp.Split.TEST:
        urls = _get_url_hashes(dl_paths["test_urls"])
    else:
        logging.fatal("Unsupported split: %s", split)
    cnn = _find_files(dl_paths, "cnn", urls)
    dm = _find_files(dl_paths, "dm", urls)
    return cnn + dm


DM_SINGLE_CLOSE_QUOTE = "\u2019"  # unicode
DM_DOUBLE_CLOSE_QUOTE = "\u201d"
# acceptable ways to end a sentence
END_TOKENS = [".", "!", "?", "...", "'", "`", '"', DM_SINGLE_CLOSE_QUOTE, DM_DOUBLE_CLOSE_QUOTE, ")"]


def _read_text_file(text_file):
    lines = []
    with open(text_file, "r") as f:
        for line in f:
            lines.append(line.strip())
    return lines


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


class CnnDailymail(nlp.GeneratorBasedBuilder):
    """CNN/DailyMail non-anonymized summarization dataset."""

    BUILDER_CONFIGS = [
        CnnDailymailConfig(name=str(version), description="Plain text", version=version)
        for version in _SUPPORTED_VERSIONS
    ]

    def _info(self):
        # Should return a nlp.DatasetInfo object
        return nlp.DatasetInfo(
            description=_DESCRIPTION,
            features=nlp.Features(
                {_ARTICLE: nlp.Value("string"), _HIGHLIGHTS: nlp.Value("string"), "id": nlp.Value("string"),}
            ),
            supervised_keys=None,
            homepage="https://github.com/abisee/cnn-dailymail",
            citation=_CITATION,
        )

    def _vocab_text_gen(self, paths):
        for _, ex in self._generate_examples(paths):
            yield " ".join([ex[_ARTICLE], ex[_HIGHLIGHTS]])

    def _split_generators(self, dl_manager):
        dl_paths = dl_manager.download_and_extract(_DL_URLS)
        train_files = _subset_filenames(dl_paths, nlp.Split.TRAIN)
        # Generate shared vocabulary

        return [
            nlp.SplitGenerator(name=nlp.Split.TRAIN, gen_kwargs={"files": train_files}),
            nlp.SplitGenerator(
                name=nlp.Split.VALIDATION, gen_kwargs={"files": _subset_filenames(dl_paths, nlp.Split.VALIDATION)}
            ),
            nlp.SplitGenerator(name=nlp.Split.TEST, gen_kwargs={"files": _subset_filenames(dl_paths, nlp.Split.TEST)}),
        ]

    def _generate_examples(self, files):
        for p in files:
            article, highlights = _get_art_abs(p, self.config.version)
            if not article or not highlights:
                continue
            fname = os.path.basename(p)
            yield fname, {
                _ARTICLE: article,
                _HIGHLIGHTS: highlights,
                "id": _get_hash_from_path(fname),
            }
