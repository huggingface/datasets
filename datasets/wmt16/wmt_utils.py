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
"""WMT: Translate dataset."""


import codecs
import functools
import glob
import gzip
import itertools
import os
import re
import xml.etree.cElementTree as ElementTree
from abc import ABC, abstractmethod

import datasets


logger = datasets.logging.get_logger(__name__)


_DESCRIPTION = """\
Translate dataset based on the data from statmt.org.

Versions exists for the different years using a combination of multiple data
sources. The base `wmt_translate` allows you to create your own config to choose
your own data/language pair by creating a custom `datasets.translate.wmt.WmtConfig`.

```
config = datasets.wmt.WmtConfig(
    version="0.0.1",
    language_pair=("fr", "de"),
    subsets={
        datasets.Split.TRAIN: ["commoncrawl_frde"],
        datasets.Split.VALIDATION: ["euelections_dev2019"],
    },
)
builder = datasets.builder("wmt_translate", config=config)
```

"""


CWMT_SUBSET_NAMES = ["casia2015", "casict2011", "casict2015", "datum2015", "datum2017", "neu2017"]


class SubDataset:
    """Class to keep track of information on a sub-dataset of WMT."""

    def __init__(self, name, target, sources, url, path, manual_dl_files=None):
        """Sub-dataset of WMT.

        Args:
          name: `string`, a unique dataset identifier.
          target: `string`, the target language code.
          sources: `set<string>`, the set of source language codes.
          url: `string` or `(string, string)`, URL(s) or URL template(s) specifying
            where to download the raw data from. If two strings are provided, the
            first is used for the source language and the second for the target.
            Template strings can either contain '{src}' placeholders that will be
            filled in with the source language code, '{0}' and '{1}' placeholders
            that will be filled in with the source and target language codes in
            alphabetical order, or all 3.
          path: `string` or `(string, string)`, path(s) or path template(s)
            specifing the path to the raw data relative to the root of the
            downloaded archive. If two strings are provided, the dataset is assumed
            to be made up of parallel text files, the first being the source and the
            second the target. If one string is provided, both languages are assumed
            to be stored within the same file and the extension is used to determine
            how to parse it. Template strings should be formatted the same as in
            `url`.
          manual_dl_files: `<list>(string)` (optional), the list of files that must
            be manually downloaded to the data directory.
        """
        self._paths = (path,) if isinstance(path, str) else path
        self._urls = (url,) if isinstance(url, str) else url
        self._manual_dl_files = manual_dl_files if manual_dl_files else []
        self.name = name
        self.target = target
        self.sources = set(sources)

    def _inject_language(self, src, strings):
        """Injects languages into (potentially) template strings."""
        if src not in self.sources:
            raise ValueError(f"Invalid source for '{self.name}': {src}")

        def _format_string(s):
            if "{0}" in s and "{1}" and "{src}" in s:
                return s.format(*sorted([src, self.target]), src=src)
            elif "{0}" in s and "{1}" in s:
                return s.format(*sorted([src, self.target]))
            elif "{src}" in s:
                return s.format(src=src)
            else:
                return s

        return [_format_string(s) for s in strings]

    def get_url(self, src):
        return self._inject_language(src, self._urls)

    def get_manual_dl_files(self, src):
        return self._inject_language(src, self._manual_dl_files)

    def get_path(self, src):
        return self._inject_language(src, self._paths)


# Subsets used in the training sets for various years of WMT.
_TRAIN_SUBSETS = [
    # pylint:disable=line-too-long
    SubDataset(
        name="commoncrawl",
        target="en",  # fr-de pair in commoncrawl_frde
        sources={"cs", "de", "es", "fr", "ru"},
        url="https://huggingface.co/datasets/wmt/wmt13/resolve/main-zip/training-parallel-commoncrawl.zip",
        path=("commoncrawl.{src}-en.{src}", "commoncrawl.{src}-en.en"),
    ),
    SubDataset(
        name="commoncrawl_frde",
        target="de",
        sources={"fr"},
        url=(
            "https://huggingface.co/datasets/wmt/wmt19/resolve/main/translation-task/fr-de/bitexts/commoncrawl.fr.gz",
            "https://huggingface.co/datasets/wmt/wmt19/resolve/main/translation-task/fr-de/bitexts/commoncrawl.de.gz",
        ),
        path=("", ""),
    ),
    SubDataset(
        name="czeng_10",
        target="en",
        sources={"cs"},
        url="http://ufal.mff.cuni.cz/czeng/czeng10",
        manual_dl_files=["data-plaintext-format.%d.tar" % i for i in range(10)],
        # Each tar contains multiple files, which we process specially in
        # _parse_czeng.
        path=("data.plaintext-format/??train.gz",) * 10,
    ),
    SubDataset(
        name="czeng_16pre",
        target="en",
        sources={"cs"},
        url="http://ufal.mff.cuni.cz/czeng/czeng16pre",
        manual_dl_files=["czeng16pre.deduped-ignoring-sections.txt.gz"],
        path="",
    ),
    SubDataset(
        name="czeng_16",
        target="en",
        sources={"cs"},
        url="http://ufal.mff.cuni.cz/czeng",
        manual_dl_files=["data-plaintext-format.%d.tar" % i for i in range(10)],
        # Each tar contains multiple files, which we process specially in
        # _parse_czeng.
        path=("data.plaintext-format/??train.gz",) * 10,
    ),
    SubDataset(
        # This dataset differs from the above in the filtering that is applied
        # during parsing.
        name="czeng_17",
        target="en",
        sources={"cs"},
        url="http://ufal.mff.cuni.cz/czeng",
        manual_dl_files=["data-plaintext-format.%d.tar" % i for i in range(10)],
        # Each tar contains multiple files, which we process specially in
        # _parse_czeng.
        path=("data.plaintext-format/??train.gz",) * 10,
    ),
    SubDataset(
        name="dcep_v1",
        target="en",
        sources={"lv"},
        url="https://huggingface.co/datasets/wmt/wmt17/resolve/main-zip/translation-task/dcep.lv-en.v1.zip",
        path=("dcep.en-lv/dcep.lv", "dcep.en-lv/dcep.en"),
    ),
    SubDataset(
        name="europarl_v7",
        target="en",
        sources={"cs", "de", "es", "fr"},
        url="https://huggingface.co/datasets/wmt/wmt13/resolve/main-zip/training-parallel-europarl-v7.zip",
        path=("training/europarl-v7.{src}-en.{src}", "training/europarl-v7.{src}-en.en"),
    ),
    SubDataset(
        name="europarl_v7_frde",
        target="de",
        sources={"fr"},
        url=(
            "https://huggingface.co/datasets/wmt/wmt19/resolve/main/translation-task/fr-de/bitexts/europarl-v7.fr.gz",
            "https://huggingface.co/datasets/wmt/wmt19/resolve/main/translation-task/fr-de/bitexts/europarl-v7.de.gz",
        ),
        path=("", ""),
    ),
    SubDataset(
        name="europarl_v8_18",
        target="en",
        sources={"et", "fi"},
        url="https://huggingface.co/datasets/wmt/wmt18/resolve/main-zip/translation-task/training-parallel-ep-v8.zip",
        path=("training/europarl-v8.{src}-en.{src}", "training/europarl-v8.{src}-en.en"),
    ),
    SubDataset(
        name="europarl_v8_16",
        target="en",
        sources={"fi", "ro"},
        url="https://huggingface.co/datasets/wmt/wmt16/resolve/main-zip/translation-task/training-parallel-ep-v8.zip",
        path=("training-parallel-ep-v8/europarl-v8.{src}-en.{src}", "training-parallel-ep-v8/europarl-v8.{src}-en.en"),
    ),
    SubDataset(
        name="europarl_v9",
        target="en",
        sources={"cs", "de", "fi", "lt"},
        url="https://huggingface.co/datasets/wmt/europarl/resolve/main/v9/training/europarl-v9.{src}-en.tsv.gz",
        path="",
    ),
    SubDataset(
        name="gigafren",
        target="en",
        sources={"fr"},
        url="https://huggingface.co/datasets/wmt/wmt10/resolve/main-zip/training-giga-fren.zip",
        path=("giga-fren.release2.fixed.fr.gz", "giga-fren.release2.fixed.en.gz"),
    ),
    SubDataset(
        name="hindencorp_01",
        target="en",
        sources={"hi"},
        url="http://ufallab.ms.mff.cuni.cz/~bojar/hindencorp",
        manual_dl_files=["hindencorp0.1.gz"],
        path="",
    ),
    SubDataset(
        name="leta_v1",
        target="en",
        sources={"lv"},
        url="https://huggingface.co/datasets/wmt/wmt17/resolve/main-zip/translation-task/leta.v1.zip",
        path=("LETA-lv-en/leta.lv", "LETA-lv-en/leta.en"),
    ),
    SubDataset(
        name="multiun",
        target="en",
        sources={"es", "fr"},
        url="https://huggingface.co/datasets/wmt/wmt13/resolve/main-zip/training-parallel-un.zip",
        path=("un/undoc.2000.{src}-en.{src}", "un/undoc.2000.{src}-en.en"),
    ),
    SubDataset(
        name="newscommentary_v9",
        target="en",
        sources={"cs", "de", "fr", "ru"},
        url="https://huggingface.co/datasets/wmt/wmt14/resolve/main-zip/training-parallel-nc-v9.zip",
        path=("training/news-commentary-v9.{src}-en.{src}", "training/news-commentary-v9.{src}-en.en"),
    ),
    SubDataset(
        name="newscommentary_v10",
        target="en",
        sources={"cs", "de", "fr", "ru"},
        url="https://huggingface.co/datasets/wmt/wmt15/resolve/main-zip/training-parallel-nc-v10.zip",
        path=("news-commentary-v10.{src}-en.{src}", "news-commentary-v10.{src}-en.en"),
    ),
    SubDataset(
        name="newscommentary_v11",
        target="en",
        sources={"cs", "de", "ru"},
        url="https://huggingface.co/datasets/wmt/wmt16/resolve/main-zip/translation-task/training-parallel-nc-v11.zip",
        path=(
            "training-parallel-nc-v11/news-commentary-v11.{src}-en.{src}",
            "training-parallel-nc-v11/news-commentary-v11.{src}-en.en",
        ),
    ),
    SubDataset(
        name="newscommentary_v12",
        target="en",
        sources={"cs", "de", "ru", "zh"},
        url="https://huggingface.co/datasets/wmt/wmt17/resolve/main-zip/translation-task/training-parallel-nc-v12.zip",
        path=("training/news-commentary-v12.{src}-en.{src}", "training/news-commentary-v12.{src}-en.en"),
    ),
    SubDataset(
        name="newscommentary_v13",
        target="en",
        sources={"cs", "de", "ru", "zh"},
        url="https://huggingface.co/datasets/wmt/wmt18/resolve/main-zip/translation-task/training-parallel-nc-v13.zip",
        path=(
            "training-parallel-nc-v13/news-commentary-v13.{src}-en.{src}",
            "training-parallel-nc-v13/news-commentary-v13.{src}-en.en",
        ),
    ),
    SubDataset(
        name="newscommentary_v14",
        target="en",  # fr-de pair in newscommentary_v14_frde
        sources={"cs", "de", "kk", "ru", "zh"},
        url="http://data.statmt.org/news-commentary/v14/training/news-commentary-v14.{0}-{1}.tsv.gz",
        path="",
    ),
    SubDataset(
        name="newscommentary_v14_frde",
        target="de",
        sources={"fr"},
        url="http://data.statmt.org/news-commentary/v14/training/news-commentary-v14.de-fr.tsv.gz",
        path="",
    ),
    SubDataset(
        name="onlinebooks_v1",
        target="en",
        sources={"lv"},
        url="https://huggingface.co/datasets/wmt/wmt17/resolve/main-zip/translation-task/books.lv-en.v1.zip",
        path=("farewell/farewell.lv", "farewell/farewell.en"),
    ),
    SubDataset(
        name="paracrawl_v1",
        target="en",
        sources={"cs", "de", "et", "fi", "ru"},
        url="https://s3.amazonaws.com/web-language-models/paracrawl/release1/paracrawl-release1.en-{src}.zipporah0-dedup-clean.tgz",  # TODO(QL): use zip for streaming
        path=(
            "paracrawl-release1.en-{src}.zipporah0-dedup-clean.{src}",
            "paracrawl-release1.en-{src}.zipporah0-dedup-clean.en",
        ),
    ),
    SubDataset(
        name="paracrawl_v1_ru",
        target="en",
        sources={"ru"},
        url="https://s3.amazonaws.com/web-language-models/paracrawl/release1/paracrawl-release1.en-ru.zipporah0-dedup-clean.tgz",  # TODO(QL): use zip for streaming
        path=(
            "paracrawl-release1.en-ru.zipporah0-dedup-clean.ru",
            "paracrawl-release1.en-ru.zipporah0-dedup-clean.en",
        ),
    ),
    SubDataset(
        name="paracrawl_v3",
        target="en",  # fr-de pair in paracrawl_v3_frde
        sources={"cs", "de", "fi", "lt"},
        url="https://s3.amazonaws.com/web-language-models/paracrawl/release3/en-{src}.bicleaner07.tmx.gz",
        path="",
    ),
    SubDataset(
        name="paracrawl_v3_frde",
        target="de",
        sources={"fr"},
        url=(
            "https://huggingface.co/datasets/wmt/wmt19/resolve/main/translation-task/fr-de/bitexts/de-fr.bicleaner07.de.gz",
            "https://huggingface.co/datasets/wmt/wmt19/resolve/main/translation-task/fr-de/bitexts/de-fr.bicleaner07.fr.gz",
        ),
        path=("", ""),
    ),
    SubDataset(
        name="rapid_2016",
        target="en",
        sources={"de", "et", "fi"},
        url="https://huggingface.co/datasets/wmt/wmt18/resolve/main-zip/translation-task/rapid2016.zip",
        path=("rapid2016.{0}-{1}.{src}", "rapid2016.{0}-{1}.en"),
    ),
    SubDataset(
        name="rapid_2016_ltfi",
        target="en",
        sources={"fi", "lt"},
        url="https://tilde-model.s3-eu-west-1.amazonaws.com/rapid2016.en-{src}.tmx.zip",
        path="rapid2016.en-{src}.tmx",
    ),
    SubDataset(
        name="rapid_2019",
        target="en",
        sources={"de"},
        url="https://s3-eu-west-1.amazonaws.com/tilde-model/rapid2019.de-en.zip",
        path=("rapid2019.de-en.de", "rapid2019.de-en.en"),
    ),
    SubDataset(
        name="setimes_2",
        target="en",
        sources={"ro", "tr"},
        url="https://opus.nlpl.eu/download.php?f=SETIMES/v2/tmx/en-{src}.tmx.gz",
        path="",
    ),
    SubDataset(
        name="uncorpus_v1",
        target="en",
        sources={"ru", "zh"},
        url="https://huggingface.co/datasets/wmt/uncorpus/resolve/main-zip/UNv1.0.en-{src}.zip",
        path=("en-{src}/UNv1.0.en-{src}.{src}", "en-{src}/UNv1.0.en-{src}.en"),
    ),
    SubDataset(
        name="wikiheadlines_fi",
        target="en",
        sources={"fi"},
        url="https://huggingface.co/datasets/wmt/wmt15/resolve/main-zip/wiki-titles.zip",
        path="wiki/fi-en/titles.fi-en",
    ),
    SubDataset(
        name="wikiheadlines_hi",
        target="en",
        sources={"hi"},
        url="https://huggingface.co/datasets/wmt/wmt14/resolve/main-zip/wiki-titles.zip",
        path="wiki/hi-en/wiki-titles.hi-en",
    ),
    SubDataset(
        # Verified that wmt14 and wmt15 files are identical.
        name="wikiheadlines_ru",
        target="en",
        sources={"ru"},
        url="https://huggingface.co/datasets/wmt/wmt15/resolve/main-zip/wiki-titles.zip",
        path="wiki/ru-en/wiki.ru-en",
    ),
    SubDataset(
        name="wikititles_v1",
        target="en",
        sources={"cs", "de", "fi", "gu", "kk", "lt", "ru", "zh"},
        url="https://huggingface.co/datasets/wmt/wikititles/resolve/main/v1/wikititles-v1.{src}-en.tsv.gz",
        path="",
    ),
    SubDataset(
        name="yandexcorpus",
        target="en",
        sources={"ru"},
        url="https://translate.yandex.ru/corpus?lang=en",
        manual_dl_files=["1mcorpus.zip"],
        path=("corpus.en_ru.1m.ru", "corpus.en_ru.1m.en"),
    ),
    # pylint:enable=line-too-long
] + [
    SubDataset(  # pylint:disable=g-complex-comprehension
        name=ss,
        target="en",
        sources={"zh"},
        url="https://huggingface.co/datasets/wmt/wmt18/resolve/main/cwmt-wmt/%s.zip" % ss,
        path=("%s/*_c[hn].txt" % ss, "%s/*_en.txt" % ss),
    )
    for ss in CWMT_SUBSET_NAMES
]

_DEV_SUBSETS = [
    SubDataset(
        name="euelections_dev2019",
        target="de",
        sources={"fr"},
        url="https://huggingface.co/datasets/wmt/wmt19/resolve/main-zip/translation-task/dev.zip",
        path=("dev/euelections_dev2019.fr-de.src.fr", "dev/euelections_dev2019.fr-de.tgt.de"),
    ),
    SubDataset(
        name="newsdev2014",
        target="en",
        sources={"hi"},
        url="https://huggingface.co/datasets/wmt/wmt19/resolve/main-zip/translation-task/dev.zip",
        path=("dev/newsdev2014.hi", "dev/newsdev2014.en"),
    ),
    SubDataset(
        name="newsdev2015",
        target="en",
        sources={"fi"},
        url="https://huggingface.co/datasets/wmt/wmt19/resolve/main-zip/translation-task/dev.zip",
        path=("dev/newsdev2015-fien-src.{src}.sgm", "dev/newsdev2015-fien-ref.en.sgm"),
    ),
    SubDataset(
        name="newsdiscussdev2015",
        target="en",
        sources={"ro", "tr"},
        url="https://huggingface.co/datasets/wmt/wmt19/resolve/main-zip/translation-task/dev.zip",
        path=("dev/newsdiscussdev2015-{src}en-src.{src}.sgm", "dev/newsdiscussdev2015-{src}en-ref.en.sgm"),
    ),
    SubDataset(
        name="newsdev2016",
        target="en",
        sources={"ro", "tr"},
        url="https://huggingface.co/datasets/wmt/wmt19/resolve/main-zip/translation-task/dev.zip",
        path=("dev/newsdev2016-{src}en-src.{src}.sgm", "dev/newsdev2016-{src}en-ref.en.sgm"),
    ),
    SubDataset(
        name="newsdev2017",
        target="en",
        sources={"lv", "zh"},
        url="https://huggingface.co/datasets/wmt/wmt19/resolve/main-zip/translation-task/dev.zip",
        path=("dev/newsdev2017-{src}en-src.{src}.sgm", "dev/newsdev2017-{src}en-ref.en.sgm"),
    ),
    SubDataset(
        name="newsdev2018",
        target="en",
        sources={"et"},
        url="https://huggingface.co/datasets/wmt/wmt19/resolve/main-zip/translation-task/dev.zip",
        path=("dev/newsdev2018-{src}en-src.{src}.sgm", "dev/newsdev2018-{src}en-ref.en.sgm"),
    ),
    SubDataset(
        name="newsdev2019",
        target="en",
        sources={"gu", "kk", "lt"},
        url="https://huggingface.co/datasets/wmt/wmt19/resolve/main-zip/translation-task/dev.zip",
        path=("dev/newsdev2019-{src}en-src.{src}.sgm", "dev/newsdev2019-{src}en-ref.en.sgm"),
    ),
    SubDataset(
        name="newsdiscussdev2015",
        target="en",
        sources={"fr"},
        url="https://huggingface.co/datasets/wmt/wmt19/resolve/main-zip/translation-task/dev.zip",
        path=("dev/newsdiscussdev2015-{src}en-src.{src}.sgm", "dev/newsdiscussdev2015-{src}en-ref.en.sgm"),
    ),
    SubDataset(
        name="newsdiscusstest2015",
        target="en",
        sources={"fr"},
        url="https://huggingface.co/datasets/wmt/wmt19/resolve/main-zip/translation-task/dev.zip",
        path=("dev/newsdiscusstest2015-{src}en-src.{src}.sgm", "dev/newsdiscusstest2015-{src}en-ref.en.sgm"),
    ),
    SubDataset(
        name="newssyscomb2009",
        target="en",
        sources={"cs", "de", "es", "fr"},
        url="https://huggingface.co/datasets/wmt/wmt19/resolve/main-zip/translation-task/dev.zip",
        path=("dev/newssyscomb2009.{src}", "dev/newssyscomb2009.en"),
    ),
    SubDataset(
        name="newstest2008",
        target="en",
        sources={"cs", "de", "es", "fr", "hu"},
        url="https://huggingface.co/datasets/wmt/wmt19/resolve/main-zip/translation-task/dev.zip",
        path=("dev/news-test2008.{src}", "dev/news-test2008.en"),
    ),
    SubDataset(
        name="newstest2009",
        target="en",
        sources={"cs", "de", "es", "fr"},
        url="https://huggingface.co/datasets/wmt/wmt19/resolve/main-zip/translation-task/dev.zip",
        path=("dev/newstest2009.{src}", "dev/newstest2009.en"),
    ),
    SubDataset(
        name="newstest2010",
        target="en",
        sources={"cs", "de", "es", "fr"},
        url="https://huggingface.co/datasets/wmt/wmt19/resolve/main-zip/translation-task/dev.zip",
        path=("dev/newstest2010.{src}", "dev/newstest2010.en"),
    ),
    SubDataset(
        name="newstest2011",
        target="en",
        sources={"cs", "de", "es", "fr"},
        url="https://huggingface.co/datasets/wmt/wmt19/resolve/main-zip/translation-task/dev.zip",
        path=("dev/newstest2011.{src}", "dev/newstest2011.en"),
    ),
    SubDataset(
        name="newstest2012",
        target="en",
        sources={"cs", "de", "es", "fr", "ru"},
        url="https://huggingface.co/datasets/wmt/wmt19/resolve/main-zip/translation-task/dev.zip",
        path=("dev/newstest2012.{src}", "dev/newstest2012.en"),
    ),
    SubDataset(
        name="newstest2013",
        target="en",
        sources={"cs", "de", "es", "fr", "ru"},
        url="https://huggingface.co/datasets/wmt/wmt19/resolve/main-zip/translation-task/dev.zip",
        path=("dev/newstest2013.{src}", "dev/newstest2013.en"),
    ),
    SubDataset(
        name="newstest2014",
        target="en",
        sources={"cs", "de", "es", "fr", "hi", "ru"},
        url="https://huggingface.co/datasets/wmt/wmt19/resolve/main-zip/translation-task/dev.zip",
        path=("dev/newstest2014-{src}en-src.{src}.sgm", "dev/newstest2014-{src}en-ref.en.sgm"),
    ),
    SubDataset(
        name="newstest2015",
        target="en",
        sources={"cs", "de", "fi", "ru"},
        url="https://huggingface.co/datasets/wmt/wmt19/resolve/main-zip/translation-task/dev.zip",
        path=("dev/newstest2015-{src}en-src.{src}.sgm", "dev/newstest2015-{src}en-ref.en.sgm"),
    ),
    SubDataset(
        name="newsdiscusstest2015",
        target="en",
        sources={"fr"},
        url="https://huggingface.co/datasets/wmt/wmt19/resolve/main-zip/translation-task/dev.zip",
        path=("dev/newsdiscusstest2015-{src}en-src.{src}.sgm", "dev/newsdiscusstest2015-{src}en-ref.en.sgm"),
    ),
    SubDataset(
        name="newstest2016",
        target="en",
        sources={"cs", "de", "fi", "ro", "ru", "tr"},
        url="https://huggingface.co/datasets/wmt/wmt19/resolve/main-zip/translation-task/dev.zip",
        path=("dev/newstest2016-{src}en-src.{src}.sgm", "dev/newstest2016-{src}en-ref.en.sgm"),
    ),
    SubDataset(
        name="newstestB2016",
        target="en",
        sources={"fi"},
        url="https://huggingface.co/datasets/wmt/wmt19/resolve/main-zip/translation-task/dev.zip",
        path=("dev/newstestB2016-enfi-ref.{src}.sgm", "dev/newstestB2016-enfi-src.en.sgm"),
    ),
    SubDataset(
        name="newstest2017",
        target="en",
        sources={"cs", "de", "fi", "lv", "ru", "tr", "zh"},
        url="https://huggingface.co/datasets/wmt/wmt19/resolve/main-zip/translation-task/dev.zip",
        path=("dev/newstest2017-{src}en-src.{src}.sgm", "dev/newstest2017-{src}en-ref.en.sgm"),
    ),
    SubDataset(
        name="newstestB2017",
        target="en",
        sources={"fi"},
        url="https://huggingface.co/datasets/wmt/wmt19/resolve/main-zip/translation-task/dev.zip",
        path=("dev/newstestB2017-fien-src.fi.sgm", "dev/newstestB2017-fien-ref.en.sgm"),
    ),
    SubDataset(
        name="newstest2018",
        target="en",
        sources={"cs", "de", "et", "fi", "ru", "tr", "zh"},
        url="https://huggingface.co/datasets/wmt/wmt19/resolve/main-zip/translation-task/dev.zip",
        path=("dev/newstest2018-{src}en-src.{src}.sgm", "dev/newstest2018-{src}en-ref.en.sgm"),
    ),
]

DATASET_MAP = {dataset.name: dataset for dataset in _TRAIN_SUBSETS + _DEV_SUBSETS}

_CZENG17_FILTER = SubDataset(
    name="czeng17_filter",
    target="en",
    sources={"cs"},
    url="http://ufal.mff.cuni.cz/czeng/download.php?f=convert_czeng16_to_17.pl.zip",
    path="convert_czeng16_to_17.pl",
)


class WmtConfig(datasets.BuilderConfig):
    """BuilderConfig for WMT."""

    def __init__(self, url=None, citation=None, description=None, language_pair=(None, None), subsets=None, **kwargs):
        """BuilderConfig for WMT.

        Args:
          url: The reference URL for the dataset.
          citation: The paper citation for the dataset.
          description: The description of the dataset.
          language_pair: pair of languages that will be used for translation. Should
                     contain 2 letter coded strings. For example: ("en", "de").
            configuration for the `datasets.features.text.TextEncoder` used for the
            `datasets.features.text.Translation` features.
          subsets: Dict[split, list[str]]. List of the subset to use for each of the
            split. Note that WMT subclasses overwrite this parameter.
          **kwargs: keyword arguments forwarded to super.
        """
        name = "%s-%s" % (language_pair[0], language_pair[1])
        if "name" in kwargs:  # Add name suffix for custom configs
            name += "." + kwargs.pop("name")

        super(WmtConfig, self).__init__(name=name, description=description, **kwargs)

        self.url = url or "http://www.statmt.org"
        self.citation = citation
        self.language_pair = language_pair
        self.subsets = subsets

        # TODO(PVP): remove when manual dir works
        # +++++++++++++++++++++
        if language_pair[1] in ["cs", "hi", "ru"]:
            assert NotImplementedError(f"The dataset for {language_pair[1]}-en is currently not fully supported.")
        # +++++++++++++++++++++


class Wmt(ABC, datasets.GeneratorBasedBuilder):
    """WMT translation dataset."""

    def __init__(self, *args, **kwargs):
        if type(self) == Wmt and "config" not in kwargs:  # pylint: disable=unidiomatic-typecheck
            raise ValueError(
                "The raw `wmt_translate` can only be instantiated with the config "
                "kwargs. You may want to use one of the `wmtYY_translate` "
                "implementation instead to get the WMT dataset for a specific year."
            )
        super(Wmt, self).__init__(*args, **kwargs)

    @property
    @abstractmethod
    def _subsets(self):
        """Subsets that make up each split of the dataset."""
        raise NotImplementedError("This is a abstract method")

    @property
    def subsets(self):
        """Subsets that make up each split of the dataset for the language pair."""
        source, target = self.config.language_pair
        filtered_subsets = {}
        for split, ss_names in self._subsets.items():
            filtered_subsets[split] = []
            for ss_name in ss_names:
                dataset = DATASET_MAP[ss_name]
                if dataset.target != target or source not in dataset.sources:
                    logger.info("Skipping sub-dataset that does not include language pair: %s", ss_name)
                else:
                    filtered_subsets[split].append(ss_name)
        logger.info("Using sub-datasets: %s", filtered_subsets)
        return filtered_subsets

    def _info(self):
        src, target = self.config.language_pair
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=datasets.Features(
                {"translation": datasets.features.Translation(languages=self.config.language_pair)}
            ),
            supervised_keys=(src, target),
            homepage=self.config.url,
            citation=self.config.citation,
        )

    def _vocab_text_gen(self, split_subsets, extraction_map, language):
        for _, ex in self._generate_examples(split_subsets, extraction_map, with_translation=False):
            yield ex[language]

    def _split_generators(self, dl_manager):
        source, _ = self.config.language_pair
        manual_paths_dict = {}
        urls_to_download = {}
        for ss_name in itertools.chain.from_iterable(self.subsets.values()):
            if ss_name == "czeng_17":
                # CzEng1.7 is CzEng1.6 with some blocks filtered out. We must download
                # the filtering script so we can parse out which blocks need to be
                # removed.
                urls_to_download[_CZENG17_FILTER.name] = _CZENG17_FILTER.get_url(source)

            # get dataset
            dataset = DATASET_MAP[ss_name]
            if dataset.get_manual_dl_files(source):
                # TODO(PVP): following two lines skip configs that are incomplete for now
                # +++++++++++++++++++++
                logger.info("Skipping {dataset.name} for now. Incomplete dataset for {self.config.name}")
                continue
                # +++++++++++++++++++++

                manual_dl_files = dataset.get_manual_dl_files(source)
                manual_paths = [
                    os.path.join(os.path.abspath(os.path.expanduser(dl_manager.manual_dir)), fname)
                    for fname in manual_dl_files
                ]
                assert all(
                    os.path.exists(path) for path in manual_paths
                ), f"For {dataset.name}, you must manually download the following file(s) from {dataset.get_url(source)} and place them in {dl_manager.manual_dir}: {', '.join(manual_dl_files)}"

                # set manual path for correct subset
                manual_paths_dict[ss_name] = manual_paths
            else:
                urls_to_download[ss_name] = dataset.get_url(source)

        # Download and extract files from URLs.
        downloaded_files = dl_manager.download_and_extract(urls_to_download)
        # Extract manually downloaded files.
        manual_files = dl_manager.extract(manual_paths_dict)
        extraction_map = dict(downloaded_files, **manual_files)

        for language in self.config.language_pair:
            self._vocab_text_gen(self.subsets[datasets.Split.TRAIN], extraction_map, language)

        return [
            datasets.SplitGenerator(  # pylint:disable=g-complex-comprehension
                name=split, gen_kwargs={"split_subsets": split_subsets, "extraction_map": extraction_map}
            )
            for split, split_subsets in self.subsets.items()
        ]

    def _generate_examples(self, split_subsets, extraction_map, with_translation=True):
        """Returns the examples in the raw (text) form."""
        source, _ = self.config.language_pair

        def _get_local_paths(dataset, extract_dirs):
            rel_paths = dataset.get_path(source)
            if len(extract_dirs) == 1:
                extract_dirs = extract_dirs * len(rel_paths)
            return [
                os.path.join(ex_dir, rel_path) if rel_path else ex_dir
                for ex_dir, rel_path in zip(extract_dirs, rel_paths)
            ]

        def _get_filenames(dataset):
            rel_paths = dataset.get_path(source)
            urls = dataset.get_url(source)
            if len(urls) == 1:
                urls = urls * len(rel_paths)
            return [rel_path if rel_path else os.path.basename(url) for url, rel_path in zip(urls, rel_paths)]

        for ss_name in split_subsets:
            # TODO(PVP) remove following five lines when manual data works
            # +++++++++++++++++++++
            dataset = DATASET_MAP[ss_name]
            source, _ = self.config.language_pair
            if dataset.get_manual_dl_files(source):
                logger.info(f"Skipping {dataset.name} for now. Incomplete dataset for {self.config.name}")
                continue
            # +++++++++++++++++++++

            logger.info("Generating examples from: %s", ss_name)
            print("Generating examples from: %s", ss_name)
            dataset = DATASET_MAP[ss_name]
            extract_dirs = extraction_map[ss_name]
            files = _get_local_paths(dataset, extract_dirs)
            filenames = _get_filenames(dataset)

            sub_generator_args = tuple(files)

            if ss_name.startswith("czeng"):
                if ss_name.endswith("16pre"):
                    sub_generator = functools.partial(_parse_tsv, language_pair=("en", "cs"))
                    sub_generator_args += tuple(filenames)
                elif ss_name.endswith("17"):
                    filter_path = _get_local_paths(_CZENG17_FILTER, extraction_map[_CZENG17_FILTER.name])[0]
                    sub_generator = functools.partial(_parse_czeng, filter_path=filter_path)
                else:
                    sub_generator = _parse_czeng
            elif ss_name == "hindencorp_01":
                sub_generator = _parse_hindencorp
            elif len(files) == 2:
                if ss_name.endswith("_frde"):
                    sub_generator = _parse_frde_bitext
                else:
                    sub_generator = _parse_parallel_sentences
                    sub_generator_args += tuple(filenames)
            elif len(files) == 1:
                fname = filenames[0]
                # Note: Due to formatting used by `download_manager`, the file
                # extension may not be at the end of the file path.
                if ".tsv" in fname:
                    sub_generator = _parse_tsv
                    sub_generator_args += tuple(filenames)
                elif (
                    ss_name.startswith("newscommentary_v14")
                    or ss_name.startswith("europarl_v9")
                    or ss_name.startswith("wikititles_v1")
                ):
                    sub_generator = functools.partial(_parse_tsv, language_pair=self.config.language_pair)
                    sub_generator_args += tuple(filenames)
                elif "tmx" in fname or ss_name.startswith("paracrawl_v3"):
                    sub_generator = _parse_tmx
                elif ss_name.startswith("wikiheadlines"):
                    sub_generator = _parse_wikiheadlines
                else:
                    raise ValueError("Unsupported file format: %s" % fname)
            else:
                raise ValueError("Invalid number of files: %d" % len(files))

            for sub_key, ex in sub_generator(*sub_generator_args):
                if not all(ex.values()):
                    continue
                # TODO(adarob): Add subset feature.
                # ex["subset"] = subset
                key = f"{ss_name}/{sub_key}"
                if with_translation is True:
                    ex = {"translation": ex}
                yield key, ex


def _parse_parallel_sentences(f1, f2, filename1, filename2):
    """Returns examples from parallel SGML or text files, which may be gzipped."""

    def _parse_text(path, original_filename):
        """Returns the sentences from a single text file, which may be gzipped."""
        split_path = original_filename.split(".")

        if split_path[-1] == "gz":
            lang = split_path[-2]

            def gen():
                with open(path, "rb") as f, gzip.GzipFile(fileobj=f) as g:
                    for line in g:
                        yield line.decode("utf-8").rstrip()

            return gen(), lang

        if split_path[-1] == "txt":
            # CWMT
            lang = split_path[-2].split("_")[-1]
            lang = "zh" if lang in ("ch", "cn") else lang
        else:
            lang = split_path[-1]

        def gen():
            with open(path, "rb") as f:
                for line in f:
                    yield line.decode("utf-8").rstrip()

        return gen(), lang

    def _parse_sgm(path, original_filename):
        """Returns sentences from a single SGML file."""
        lang = original_filename.split(".")[-2]
        # Note: We can't use the XML parser since some of the files are badly
        # formatted.
        seg_re = re.compile(r"<seg id=\"\d+\">(.*)</seg>")

        def gen():
            with open(path, encoding="utf-8") as f:
                for line in f:
                    seg_match = re.match(seg_re, line)
                    if seg_match:
                        assert len(seg_match.groups()) == 1
                        yield seg_match.groups()[0]

        return gen(), lang

    parse_file = _parse_sgm if os.path.basename(f1).endswith(".sgm") else _parse_text

    # Some datasets (e.g., CWMT) contain multiple parallel files specified with
    # a wildcard. We sort both sets to align them and parse them one by one.
    f1_files = sorted(glob.glob(f1))
    f2_files = sorted(glob.glob(f2))

    assert f1_files and f2_files, "No matching files found: %s, %s." % (f1, f2)
    assert len(f1_files) == len(f2_files), "Number of files do not match: %d vs %d for %s vs %s." % (
        len(f1_files),
        len(f2_files),
        f1,
        f2,
    )

    for f_id, (f1_i, f2_i) in enumerate(zip(sorted(f1_files), sorted(f2_files))):
        l1_sentences, l1 = parse_file(f1_i, filename1)
        l2_sentences, l2 = parse_file(f2_i, filename2)

        for line_id, (s1, s2) in enumerate(zip(l1_sentences, l2_sentences)):
            key = f"{f_id}/{line_id}"
            yield key, {l1: s1, l2: s2}


def _parse_frde_bitext(fr_path, de_path):
    with open(fr_path, encoding="utf-8") as fr_f:
        with open(de_path, encoding="utf-8") as de_f:
            for line_id, (s1, s2) in enumerate(zip(fr_f, de_f)):
                yield line_id, {"fr": s1.rstrip(), "de": s2.rstrip()}


def _parse_tmx(path):
    """Generates examples from TMX file."""

    def _get_tuv_lang(tuv):
        for k, v in tuv.items():
            if k.endswith("}lang"):
                return v
        raise AssertionError("Language not found in `tuv` attributes.")

    def _get_tuv_seg(tuv):
        segs = tuv.findall("seg")
        assert len(segs) == 1, "Invalid number of segments: %d" % len(segs)
        return segs[0].text

    with open(path, "rb") as f:
        # Workaround due to: https://github.com/tensorflow/tensorflow/issues/33563
        utf_f = codecs.getreader("utf-8")(f)
        for line_id, (_, elem) in enumerate(ElementTree.iterparse(utf_f)):
            if elem.tag == "tu":
                yield line_id, {_get_tuv_lang(tuv): _get_tuv_seg(tuv) for tuv in elem.iterfind("tuv")}
                elem.clear()


def _parse_tsv(path, filename, language_pair=None):
    """Generates examples from TSV file."""
    if language_pair is None:
        lang_match = re.match(r".*\.([a-z][a-z])-([a-z][a-z])\.tsv", filename)
        assert lang_match is not None, "Invalid TSV filename: %s" % filename
        l1, l2 = lang_match.groups()
    else:
        l1, l2 = language_pair
    with open(path, encoding="utf-8") as f:
        for j, line in enumerate(f):
            cols = line.split("\t")
            if len(cols) != 2:
                logger.warning("Skipping line %d in TSV (%s) with %d != 2 columns.", j, path, len(cols))
                continue
            s1, s2 = cols
            yield j, {l1: s1.strip(), l2: s2.strip()}


def _parse_wikiheadlines(path):
    """Generates examples from Wikiheadlines dataset file."""
    lang_match = re.match(r".*\.([a-z][a-z])-([a-z][a-z])$", path)
    assert lang_match is not None, "Invalid Wikiheadlines filename: %s" % path
    l1, l2 = lang_match.groups()
    with open(path, encoding="utf-8") as f:
        for line_id, line in enumerate(f):
            s1, s2 = line.split("|||")
            yield line_id, {l1: s1.strip(), l2: s2.strip()}


def _parse_czeng(*paths, **kwargs):
    """Generates examples from CzEng v1.6, with optional filtering for v1.7."""
    filter_path = kwargs.get("filter_path", None)
    if filter_path:
        re_block = re.compile(r"^[^-]+-b(\d+)-\d\d[tde]")
        with open(filter_path, encoding="utf-8") as f:
            bad_blocks = {blk for blk in re.search(r"qw{([\s\d]*)}", f.read()).groups()[0].split()}
        logger.info("Loaded %d bad blocks to filter from CzEng v1.6 to make v1.7.", len(bad_blocks))

    for path in paths:
        for gz_path in sorted(glob.glob(path)):
            with open(gz_path, "rb") as g, gzip.GzipFile(fileobj=g) as f:
                filename = os.path.basename(gz_path)
                for line_id, line in enumerate(f):
                    line = line.decode("utf-8")  # required for py3
                    if not line.strip():
                        continue
                    id_, unused_score, cs, en = line.split("\t")
                    if filter_path:
                        block_match = re.match(re_block, id_)
                        if block_match and block_match.groups()[0] in bad_blocks:
                            continue
                    sub_key = f"{filename}/{line_id}"
                    yield sub_key, {
                        "cs": cs.strip(),
                        "en": en.strip(),
                    }


def _parse_hindencorp(path):
    with open(path, encoding="utf-8") as f:
        for line_id, line in enumerate(f):
            split_line = line.split("\t")
            if len(split_line) != 5:
                logger.warning("Skipping invalid HindEnCorp line: %s", line)
                continue
            yield line_id, {"translation": {"en": split_line[3].strip(), "hi": split_line[4].strip()}}
