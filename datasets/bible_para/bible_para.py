# coding=utf-8
# Copyright 2020 HuggingFace Datasets Authors.
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
import os

import datasets


_DESCRIPTION = """\
This is a multilingual parallel corpus created from translations of the Bible compiled by Christos Christodoulopoulos and Mark Steedman.

102 languages, 5,148 bitexts
total number of files: 107
total number of tokens: 56.43M
total number of sentence fragments: 2.84M
"""
_HOMEPAGE_URL = "http://opus.nlpl.eu/bible-uedin.php"
_CITATION = """\
OPUS and A massively parallel corpus: the Bible in 100 languages, Christos Christodoulopoulos and Mark Steedman, *Language Resources and Evaluation*, 49 (2)
"""

_VERSION = "1.0.0"
_BASE_NAME = "bible-uedin.{}.{}"

_LANGUAGE_PAIRS = {
    (
        "acu",
        "af",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/acu-af.txt.zip",
    (
        "acu",
        "agr",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/acu-agr.txt.zip",
    (
        "acu",
        "ake",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/acu-ake.txt.zip",
    (
        "acu",
        "am",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/acu-am.txt.zip",
    (
        "acu",
        "amu",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/acu-amu.txt.zip",
    (
        "acu",
        "ar",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/acu-ar.txt.zip",
    (
        "acu",
        "bg",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/acu-bg.txt.zip",
    (
        "acu",
        "bsn",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/acu-bsn.txt.zip",
    (
        "acu",
        "cak",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/acu-cak.txt.zip",
    (
        "acu",
        "ceb",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/acu-ceb.txt.zip",
    (
        "acu",
        "ch",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/acu-ch.txt.zip",
    (
        "acu",
        "chq",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/acu-chq.txt.zip",
    (
        "acu",
        "chr",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/acu-chr.txt.zip",
    (
        "acu",
        "cjp",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/acu-cjp.txt.zip",
    (
        "acu",
        "cni",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/acu-cni.txt.zip",
    (
        "acu",
        "cop",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/acu-cop.txt.zip",
    (
        "acu",
        "crp",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/acu-crp.txt.zip",
    (
        "acu",
        "cs",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/acu-cs.txt.zip",
    (
        "acu",
        "da",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/acu-da.txt.zip",
    (
        "acu",
        "de",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/acu-de.txt.zip",
    (
        "acu",
        "dik",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/acu-dik.txt.zip",
    (
        "acu",
        "dje",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/acu-dje.txt.zip",
    (
        "acu",
        "djk",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/acu-djk.txt.zip",
    (
        "acu",
        "dop",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/acu-dop.txt.zip",
    (
        "acu",
        "ee",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/acu-ee.txt.zip",
    (
        "acu",
        "el",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/acu-el.txt.zip",
    (
        "acu",
        "en",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/acu-en.txt.zip",
    (
        "acu",
        "eo",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/acu-eo.txt.zip",
    (
        "acu",
        "es",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/acu-es.txt.zip",
    (
        "acu",
        "et",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/acu-et.txt.zip",
    (
        "acu",
        "eu",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/acu-eu.txt.zip",
    (
        "acu",
        "fi",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/acu-fi.txt.zip",
    (
        "acu",
        "fr",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/acu-fr.txt.zip",
    (
        "acu",
        "gbi",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/acu-gbi.txt.zip",
    (
        "acu",
        "gd",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/acu-gd.txt.zip",
    (
        "acu",
        "gu",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/acu-gu.txt.zip",
    (
        "acu",
        "gv",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/acu-gv.txt.zip",
    (
        "acu",
        "he",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/acu-he.txt.zip",
    (
        "acu",
        "hi",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/acu-hi.txt.zip",
    (
        "acu",
        "hr",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/acu-hr.txt.zip",
    (
        "acu",
        "hu",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/acu-hu.txt.zip",
    (
        "acu",
        "hy",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/acu-hy.txt.zip",
    (
        "acu",
        "id",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/acu-id.txt.zip",
    (
        "acu",
        "is",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/acu-is.txt.zip",
    (
        "acu",
        "it",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/acu-it.txt.zip",
    (
        "acu",
        "jak",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/acu-jak.txt.zip",
    (
        "acu",
        "jap",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/acu-jap.txt.zip",
    (
        "acu",
        "jiv",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/acu-jiv.txt.zip",
    (
        "acu",
        "kab",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/acu-kab.txt.zip",
    (
        "acu",
        "kbh",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/acu-kbh.txt.zip",
    (
        "acu",
        "kek",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/acu-kek.txt.zip",
    (
        "acu",
        "kn",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/acu-kn.txt.zip",
    (
        "acu",
        "ko",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/acu-ko.txt.zip",
    (
        "acu",
        "la",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/acu-la.txt.zip",
    (
        "acu",
        "lt",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/acu-lt.txt.zip",
    (
        "acu",
        "lv",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/acu-lv.txt.zip",
    (
        "acu",
        "mam",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/acu-mam.txt.zip",
    (
        "acu",
        "mi",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/acu-mi.txt.zip",
    (
        "acu",
        "ml",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/acu-ml.txt.zip",
    (
        "acu",
        "mr",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/acu-mr.txt.zip",
    (
        "acu",
        "my",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/acu-my.txt.zip",
    (
        "acu",
        "ne",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/acu-ne.txt.zip",
    (
        "acu",
        "nhg",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/acu-nhg.txt.zip",
    (
        "acu",
        "nl",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/acu-nl.txt.zip",
    (
        "acu",
        "no",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/acu-no.txt.zip",
    (
        "acu",
        "ojb",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/acu-ojb.txt.zip",
    (
        "acu",
        "pck",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/acu-pck.txt.zip",
    (
        "acu",
        "pes",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/acu-pes.txt.zip",
    (
        "acu",
        "pl",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/acu-pl.txt.zip",
    (
        "acu",
        "plt",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/acu-plt.txt.zip",
    (
        "acu",
        "pot",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/acu-pot.txt.zip",
    (
        "acu",
        "ppk",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/acu-ppk.txt.zip",
    (
        "acu",
        "pt",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/acu-pt.txt.zip",
    (
        "acu",
        "quc",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/acu-quc.txt.zip",
    (
        "acu",
        "quw",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/acu-quw.txt.zip",
    (
        "acu",
        "ro",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/acu-ro.txt.zip",
    (
        "acu",
        "rom",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/acu-rom.txt.zip",
    (
        "acu",
        "ru",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/acu-ru.txt.zip",
    (
        "acu",
        "shi",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/acu-shi.txt.zip",
    (
        "acu",
        "sk",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/acu-sk.txt.zip",
    (
        "acu",
        "sl",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/acu-sl.txt.zip",
    (
        "acu",
        "sn",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/acu-sn.txt.zip",
    (
        "acu",
        "so",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/acu-so.txt.zip",
    (
        "acu",
        "sq",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/acu-sq.txt.zip",
    (
        "acu",
        "sr",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/acu-sr.txt.zip",
    (
        "acu",
        "ss",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/acu-ss.txt.zip",
    (
        "acu",
        "sv",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/acu-sv.txt.zip",
    (
        "acu",
        "syr",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/acu-syr.txt.zip",
    (
        "acu",
        "te",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/acu-te.txt.zip",
    (
        "acu",
        "th",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/acu-th.txt.zip",
    (
        "acu",
        "tl",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/acu-tl.txt.zip",
    (
        "acu",
        "tmh",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/acu-tmh.txt.zip",
    (
        "acu",
        "tr",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/acu-tr.txt.zip",
    (
        "acu",
        "uk",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/acu-uk.txt.zip",
    (
        "acu",
        "usp",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/acu-usp.txt.zip",
    (
        "acu",
        "vi",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/acu-vi.txt.zip",
    (
        "acu",
        "wal",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/acu-wal.txt.zip",
    (
        "acu",
        "wo",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/acu-wo.txt.zip",
    (
        "acu",
        "xh",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/acu-xh.txt.zip",
    (
        "acu",
        "zh",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/acu-zh.txt.zip",
    (
        "acu",
        "zu",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/acu-zu.txt.zip",
    (
        "af",
        "agr",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/af-agr.txt.zip",
    (
        "af",
        "ake",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/af-ake.txt.zip",
    ("af", "am"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/af-am.txt.zip",
    (
        "af",
        "amu",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/af-amu.txt.zip",
    ("af", "ar"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/af-ar.txt.zip",
    ("af", "bg"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/af-bg.txt.zip",
    (
        "af",
        "bsn",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/af-bsn.txt.zip",
    (
        "af",
        "cak",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/af-cak.txt.zip",
    (
        "af",
        "ceb",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/af-ceb.txt.zip",
    ("af", "ch"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/af-ch.txt.zip",
    (
        "af",
        "chq",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/af-chq.txt.zip",
    (
        "af",
        "chr",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/af-chr.txt.zip",
    (
        "af",
        "cjp",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/af-cjp.txt.zip",
    (
        "af",
        "cni",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/af-cni.txt.zip",
    (
        "af",
        "cop",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/af-cop.txt.zip",
    (
        "af",
        "crp",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/af-crp.txt.zip",
    ("af", "cs"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/af-cs.txt.zip",
    ("af", "da"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/af-da.txt.zip",
    ("af", "de"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/af-de.txt.zip",
    (
        "af",
        "dik",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/af-dik.txt.zip",
    (
        "af",
        "dje",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/af-dje.txt.zip",
    (
        "af",
        "djk",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/af-djk.txt.zip",
    (
        "af",
        "dop",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/af-dop.txt.zip",
    ("af", "ee"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/af-ee.txt.zip",
    ("af", "el"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/af-el.txt.zip",
    ("af", "en"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/af-en.txt.zip",
    ("af", "eo"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/af-eo.txt.zip",
    ("af", "es"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/af-es.txt.zip",
    ("af", "et"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/af-et.txt.zip",
    ("af", "eu"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/af-eu.txt.zip",
    ("af", "fi"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/af-fi.txt.zip",
    ("af", "fr"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/af-fr.txt.zip",
    (
        "af",
        "gbi",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/af-gbi.txt.zip",
    ("af", "gd"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/af-gd.txt.zip",
    ("af", "gu"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/af-gu.txt.zip",
    ("af", "gv"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/af-gv.txt.zip",
    ("af", "he"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/af-he.txt.zip",
    ("af", "hi"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/af-hi.txt.zip",
    ("af", "hr"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/af-hr.txt.zip",
    ("af", "hu"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/af-hu.txt.zip",
    ("af", "hy"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/af-hy.txt.zip",
    ("af", "id"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/af-id.txt.zip",
    ("af", "is"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/af-is.txt.zip",
    ("af", "it"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/af-it.txt.zip",
    (
        "af",
        "jak",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/af-jak.txt.zip",
    (
        "af",
        "jap",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/af-jap.txt.zip",
    (
        "af",
        "jiv",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/af-jiv.txt.zip",
    (
        "af",
        "kab",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/af-kab.txt.zip",
    (
        "af",
        "kbh",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/af-kbh.txt.zip",
    (
        "af",
        "kek",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/af-kek.txt.zip",
    ("af", "kn"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/af-kn.txt.zip",
    ("af", "ko"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/af-ko.txt.zip",
    ("af", "la"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/af-la.txt.zip",
    ("af", "lt"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/af-lt.txt.zip",
    ("af", "lv"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/af-lv.txt.zip",
    (
        "af",
        "mam",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/af-mam.txt.zip",
    ("af", "mi"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/af-mi.txt.zip",
    ("af", "ml"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/af-ml.txt.zip",
    ("af", "mr"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/af-mr.txt.zip",
    ("af", "my"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/af-my.txt.zip",
    ("af", "ne"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/af-ne.txt.zip",
    (
        "af",
        "nhg",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/af-nhg.txt.zip",
    ("af", "nl"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/af-nl.txt.zip",
    ("af", "no"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/af-no.txt.zip",
    (
        "af",
        "ojb",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/af-ojb.txt.zip",
    (
        "af",
        "pck",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/af-pck.txt.zip",
    (
        "af",
        "pes",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/af-pes.txt.zip",
    ("af", "pl"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/af-pl.txt.zip",
    (
        "af",
        "plt",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/af-plt.txt.zip",
    (
        "af",
        "pot",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/af-pot.txt.zip",
    (
        "af",
        "ppk",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/af-ppk.txt.zip",
    ("af", "pt"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/af-pt.txt.zip",
    (
        "af",
        "quc",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/af-quc.txt.zip",
    (
        "af",
        "quw",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/af-quw.txt.zip",
    ("af", "ro"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/af-ro.txt.zip",
    (
        "af",
        "rom",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/af-rom.txt.zip",
    ("af", "ru"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/af-ru.txt.zip",
    (
        "af",
        "shi",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/af-shi.txt.zip",
    ("af", "sk"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/af-sk.txt.zip",
    ("af", "sl"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/af-sl.txt.zip",
    ("af", "sn"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/af-sn.txt.zip",
    ("af", "so"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/af-so.txt.zip",
    ("af", "sq"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/af-sq.txt.zip",
    ("af", "sr"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/af-sr.txt.zip",
    ("af", "ss"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/af-ss.txt.zip",
    ("af", "sv"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/af-sv.txt.zip",
    (
        "af",
        "syr",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/af-syr.txt.zip",
    ("af", "te"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/af-te.txt.zip",
    ("af", "th"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/af-th.txt.zip",
    ("af", "tl"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/af-tl.txt.zip",
    (
        "af",
        "tmh",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/af-tmh.txt.zip",
    ("af", "tr"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/af-tr.txt.zip",
    ("af", "uk"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/af-uk.txt.zip",
    (
        "af",
        "usp",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/af-usp.txt.zip",
    ("af", "vi"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/af-vi.txt.zip",
    (
        "af",
        "wal",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/af-wal.txt.zip",
    ("af", "wo"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/af-wo.txt.zip",
    ("af", "xh"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/af-xh.txt.zip",
    ("af", "zh"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/af-zh.txt.zip",
    ("af", "zu"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/af-zu.txt.zip",
    (
        "agr",
        "ake",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/agr-ake.txt.zip",
    (
        "agr",
        "am",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/agr-am.txt.zip",
    (
        "agr",
        "amu",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/agr-amu.txt.zip",
    (
        "agr",
        "ar",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/agr-ar.txt.zip",
    (
        "agr",
        "bg",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/agr-bg.txt.zip",
    (
        "agr",
        "bsn",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/agr-bsn.txt.zip",
    (
        "agr",
        "cak",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/agr-cak.txt.zip",
    (
        "agr",
        "ceb",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/agr-ceb.txt.zip",
    (
        "agr",
        "ch",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/agr-ch.txt.zip",
    (
        "agr",
        "chq",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/agr-chq.txt.zip",
    (
        "agr",
        "chr",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/agr-chr.txt.zip",
    (
        "agr",
        "cjp",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/agr-cjp.txt.zip",
    (
        "agr",
        "cni",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/agr-cni.txt.zip",
    (
        "agr",
        "cop",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/agr-cop.txt.zip",
    (
        "agr",
        "crp",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/agr-crp.txt.zip",
    (
        "agr",
        "cs",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/agr-cs.txt.zip",
    (
        "agr",
        "da",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/agr-da.txt.zip",
    (
        "agr",
        "de",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/agr-de.txt.zip",
    (
        "agr",
        "dik",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/agr-dik.txt.zip",
    (
        "agr",
        "dje",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/agr-dje.txt.zip",
    (
        "agr",
        "djk",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/agr-djk.txt.zip",
    (
        "agr",
        "dop",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/agr-dop.txt.zip",
    (
        "agr",
        "ee",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/agr-ee.txt.zip",
    (
        "agr",
        "el",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/agr-el.txt.zip",
    (
        "agr",
        "en",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/agr-en.txt.zip",
    (
        "agr",
        "eo",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/agr-eo.txt.zip",
    (
        "agr",
        "es",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/agr-es.txt.zip",
    (
        "agr",
        "et",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/agr-et.txt.zip",
    (
        "agr",
        "eu",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/agr-eu.txt.zip",
    (
        "agr",
        "fi",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/agr-fi.txt.zip",
    (
        "agr",
        "fr",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/agr-fr.txt.zip",
    (
        "agr",
        "gbi",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/agr-gbi.txt.zip",
    (
        "agr",
        "gd",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/agr-gd.txt.zip",
    (
        "agr",
        "gu",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/agr-gu.txt.zip",
    (
        "agr",
        "gv",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/agr-gv.txt.zip",
    (
        "agr",
        "he",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/agr-he.txt.zip",
    (
        "agr",
        "hi",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/agr-hi.txt.zip",
    (
        "agr",
        "hr",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/agr-hr.txt.zip",
    (
        "agr",
        "hu",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/agr-hu.txt.zip",
    (
        "agr",
        "hy",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/agr-hy.txt.zip",
    (
        "agr",
        "id",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/agr-id.txt.zip",
    (
        "agr",
        "is",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/agr-is.txt.zip",
    (
        "agr",
        "it",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/agr-it.txt.zip",
    (
        "agr",
        "jak",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/agr-jak.txt.zip",
    (
        "agr",
        "jap",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/agr-jap.txt.zip",
    (
        "agr",
        "jiv",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/agr-jiv.txt.zip",
    (
        "agr",
        "kab",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/agr-kab.txt.zip",
    (
        "agr",
        "kbh",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/agr-kbh.txt.zip",
    (
        "agr",
        "kek",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/agr-kek.txt.zip",
    (
        "agr",
        "kn",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/agr-kn.txt.zip",
    (
        "agr",
        "ko",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/agr-ko.txt.zip",
    (
        "agr",
        "la",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/agr-la.txt.zip",
    (
        "agr",
        "lt",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/agr-lt.txt.zip",
    (
        "agr",
        "lv",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/agr-lv.txt.zip",
    (
        "agr",
        "mam",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/agr-mam.txt.zip",
    (
        "agr",
        "mi",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/agr-mi.txt.zip",
    (
        "agr",
        "ml",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/agr-ml.txt.zip",
    (
        "agr",
        "mr",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/agr-mr.txt.zip",
    (
        "agr",
        "my",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/agr-my.txt.zip",
    (
        "agr",
        "ne",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/agr-ne.txt.zip",
    (
        "agr",
        "nhg",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/agr-nhg.txt.zip",
    (
        "agr",
        "nl",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/agr-nl.txt.zip",
    (
        "agr",
        "no",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/agr-no.txt.zip",
    (
        "agr",
        "ojb",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/agr-ojb.txt.zip",
    (
        "agr",
        "pck",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/agr-pck.txt.zip",
    (
        "agr",
        "pes",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/agr-pes.txt.zip",
    (
        "agr",
        "pl",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/agr-pl.txt.zip",
    (
        "agr",
        "plt",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/agr-plt.txt.zip",
    (
        "agr",
        "pot",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/agr-pot.txt.zip",
    (
        "agr",
        "ppk",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/agr-ppk.txt.zip",
    (
        "agr",
        "pt",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/agr-pt.txt.zip",
    (
        "agr",
        "quc",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/agr-quc.txt.zip",
    (
        "agr",
        "quw",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/agr-quw.txt.zip",
    (
        "agr",
        "ro",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/agr-ro.txt.zip",
    (
        "agr",
        "rom",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/agr-rom.txt.zip",
    (
        "agr",
        "ru",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/agr-ru.txt.zip",
    (
        "agr",
        "shi",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/agr-shi.txt.zip",
    (
        "agr",
        "sk",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/agr-sk.txt.zip",
    (
        "agr",
        "sl",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/agr-sl.txt.zip",
    (
        "agr",
        "sn",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/agr-sn.txt.zip",
    (
        "agr",
        "so",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/agr-so.txt.zip",
    (
        "agr",
        "sq",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/agr-sq.txt.zip",
    (
        "agr",
        "sr",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/agr-sr.txt.zip",
    (
        "agr",
        "ss",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/agr-ss.txt.zip",
    (
        "agr",
        "sv",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/agr-sv.txt.zip",
    (
        "agr",
        "syr",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/agr-syr.txt.zip",
    (
        "agr",
        "te",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/agr-te.txt.zip",
    (
        "agr",
        "th",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/agr-th.txt.zip",
    (
        "agr",
        "tl",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/agr-tl.txt.zip",
    (
        "agr",
        "tmh",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/agr-tmh.txt.zip",
    (
        "agr",
        "tr",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/agr-tr.txt.zip",
    (
        "agr",
        "uk",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/agr-uk.txt.zip",
    (
        "agr",
        "usp",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/agr-usp.txt.zip",
    (
        "agr",
        "vi",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/agr-vi.txt.zip",
    (
        "agr",
        "wal",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/agr-wal.txt.zip",
    (
        "agr",
        "wo",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/agr-wo.txt.zip",
    (
        "agr",
        "xh",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/agr-xh.txt.zip",
    (
        "agr",
        "zh",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/agr-zh.txt.zip",
    (
        "agr",
        "zu",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/agr-zu.txt.zip",
    (
        "ake",
        "am",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ake-am.txt.zip",
    (
        "ake",
        "amu",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ake-amu.txt.zip",
    (
        "ake",
        "ar",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ake-ar.txt.zip",
    (
        "ake",
        "bg",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ake-bg.txt.zip",
    (
        "ake",
        "bsn",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ake-bsn.txt.zip",
    (
        "ake",
        "cak",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ake-cak.txt.zip",
    (
        "ake",
        "ceb",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ake-ceb.txt.zip",
    (
        "ake",
        "ch",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ake-ch.txt.zip",
    (
        "ake",
        "chq",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ake-chq.txt.zip",
    (
        "ake",
        "chr",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ake-chr.txt.zip",
    (
        "ake",
        "cjp",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ake-cjp.txt.zip",
    (
        "ake",
        "cni",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ake-cni.txt.zip",
    (
        "ake",
        "cop",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ake-cop.txt.zip",
    (
        "ake",
        "crp",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ake-crp.txt.zip",
    (
        "ake",
        "cs",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ake-cs.txt.zip",
    (
        "ake",
        "da",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ake-da.txt.zip",
    (
        "ake",
        "de",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ake-de.txt.zip",
    (
        "ake",
        "dik",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ake-dik.txt.zip",
    (
        "ake",
        "dje",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ake-dje.txt.zip",
    (
        "ake",
        "djk",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ake-djk.txt.zip",
    (
        "ake",
        "dop",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ake-dop.txt.zip",
    (
        "ake",
        "ee",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ake-ee.txt.zip",
    (
        "ake",
        "el",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ake-el.txt.zip",
    (
        "ake",
        "en",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ake-en.txt.zip",
    (
        "ake",
        "eo",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ake-eo.txt.zip",
    (
        "ake",
        "es",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ake-es.txt.zip",
    (
        "ake",
        "et",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ake-et.txt.zip",
    (
        "ake",
        "eu",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ake-eu.txt.zip",
    (
        "ake",
        "fi",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ake-fi.txt.zip",
    (
        "ake",
        "fr",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ake-fr.txt.zip",
    (
        "ake",
        "gbi",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ake-gbi.txt.zip",
    (
        "ake",
        "gd",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ake-gd.txt.zip",
    (
        "ake",
        "gu",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ake-gu.txt.zip",
    (
        "ake",
        "gv",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ake-gv.txt.zip",
    (
        "ake",
        "he",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ake-he.txt.zip",
    (
        "ake",
        "hi",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ake-hi.txt.zip",
    (
        "ake",
        "hr",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ake-hr.txt.zip",
    (
        "ake",
        "hu",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ake-hu.txt.zip",
    (
        "ake",
        "hy",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ake-hy.txt.zip",
    (
        "ake",
        "id",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ake-id.txt.zip",
    (
        "ake",
        "is",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ake-is.txt.zip",
    (
        "ake",
        "it",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ake-it.txt.zip",
    (
        "ake",
        "jak",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ake-jak.txt.zip",
    (
        "ake",
        "jap",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ake-jap.txt.zip",
    (
        "ake",
        "jiv",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ake-jiv.txt.zip",
    (
        "ake",
        "kab",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ake-kab.txt.zip",
    (
        "ake",
        "kbh",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ake-kbh.txt.zip",
    (
        "ake",
        "kek",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ake-kek.txt.zip",
    (
        "ake",
        "kn",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ake-kn.txt.zip",
    (
        "ake",
        "ko",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ake-ko.txt.zip",
    (
        "ake",
        "la",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ake-la.txt.zip",
    (
        "ake",
        "lt",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ake-lt.txt.zip",
    (
        "ake",
        "lv",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ake-lv.txt.zip",
    (
        "ake",
        "mam",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ake-mam.txt.zip",
    (
        "ake",
        "mi",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ake-mi.txt.zip",
    (
        "ake",
        "ml",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ake-ml.txt.zip",
    (
        "ake",
        "mr",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ake-mr.txt.zip",
    (
        "ake",
        "my",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ake-my.txt.zip",
    (
        "ake",
        "ne",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ake-ne.txt.zip",
    (
        "ake",
        "nhg",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ake-nhg.txt.zip",
    (
        "ake",
        "nl",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ake-nl.txt.zip",
    (
        "ake",
        "no",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ake-no.txt.zip",
    (
        "ake",
        "ojb",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ake-ojb.txt.zip",
    (
        "ake",
        "pck",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ake-pck.txt.zip",
    (
        "ake",
        "pes",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ake-pes.txt.zip",
    (
        "ake",
        "pl",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ake-pl.txt.zip",
    (
        "ake",
        "plt",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ake-plt.txt.zip",
    (
        "ake",
        "pot",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ake-pot.txt.zip",
    (
        "ake",
        "ppk",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ake-ppk.txt.zip",
    (
        "ake",
        "pt",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ake-pt.txt.zip",
    (
        "ake",
        "quc",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ake-quc.txt.zip",
    (
        "ake",
        "quw",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ake-quw.txt.zip",
    (
        "ake",
        "ro",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ake-ro.txt.zip",
    (
        "ake",
        "rom",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ake-rom.txt.zip",
    (
        "ake",
        "ru",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ake-ru.txt.zip",
    (
        "ake",
        "shi",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ake-shi.txt.zip",
    (
        "ake",
        "sk",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ake-sk.txt.zip",
    (
        "ake",
        "sl",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ake-sl.txt.zip",
    (
        "ake",
        "sn",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ake-sn.txt.zip",
    (
        "ake",
        "so",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ake-so.txt.zip",
    (
        "ake",
        "sq",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ake-sq.txt.zip",
    (
        "ake",
        "sr",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ake-sr.txt.zip",
    (
        "ake",
        "ss",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ake-ss.txt.zip",
    (
        "ake",
        "sv",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ake-sv.txt.zip",
    (
        "ake",
        "syr",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ake-syr.txt.zip",
    (
        "ake",
        "te",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ake-te.txt.zip",
    (
        "ake",
        "th",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ake-th.txt.zip",
    (
        "ake",
        "tl",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ake-tl.txt.zip",
    (
        "ake",
        "tmh",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ake-tmh.txt.zip",
    (
        "ake",
        "tr",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ake-tr.txt.zip",
    (
        "ake",
        "uk",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ake-uk.txt.zip",
    (
        "ake",
        "usp",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ake-usp.txt.zip",
    (
        "ake",
        "vi",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ake-vi.txt.zip",
    (
        "ake",
        "wal",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ake-wal.txt.zip",
    (
        "ake",
        "wo",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ake-wo.txt.zip",
    (
        "ake",
        "xh",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ake-xh.txt.zip",
    (
        "ake",
        "zh",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ake-zh.txt.zip",
    (
        "ake",
        "zu",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ake-zu.txt.zip",
    (
        "am",
        "amu",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/am-amu.txt.zip",
    ("am", "ar"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/am-ar.txt.zip",
    ("am", "bg"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/am-bg.txt.zip",
    (
        "am",
        "bsn",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/am-bsn.txt.zip",
    (
        "am",
        "cak",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/am-cak.txt.zip",
    (
        "am",
        "ceb",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/am-ceb.txt.zip",
    ("am", "ch"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/am-ch.txt.zip",
    (
        "am",
        "chq",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/am-chq.txt.zip",
    (
        "am",
        "chr",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/am-chr.txt.zip",
    (
        "am",
        "cjp",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/am-cjp.txt.zip",
    (
        "am",
        "cni",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/am-cni.txt.zip",
    (
        "am",
        "cop",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/am-cop.txt.zip",
    (
        "am",
        "crp",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/am-crp.txt.zip",
    ("am", "cs"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/am-cs.txt.zip",
    ("am", "da"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/am-da.txt.zip",
    ("am", "de"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/am-de.txt.zip",
    (
        "am",
        "dik",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/am-dik.txt.zip",
    (
        "am",
        "dje",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/am-dje.txt.zip",
    (
        "am",
        "djk",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/am-djk.txt.zip",
    (
        "am",
        "dop",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/am-dop.txt.zip",
    ("am", "ee"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/am-ee.txt.zip",
    ("am", "el"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/am-el.txt.zip",
    ("am", "en"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/am-en.txt.zip",
    ("am", "eo"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/am-eo.txt.zip",
    ("am", "es"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/am-es.txt.zip",
    ("am", "et"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/am-et.txt.zip",
    ("am", "eu"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/am-eu.txt.zip",
    ("am", "fi"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/am-fi.txt.zip",
    ("am", "fr"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/am-fr.txt.zip",
    (
        "am",
        "gbi",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/am-gbi.txt.zip",
    ("am", "gd"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/am-gd.txt.zip",
    ("am", "gu"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/am-gu.txt.zip",
    ("am", "gv"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/am-gv.txt.zip",
    ("am", "he"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/am-he.txt.zip",
    ("am", "hi"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/am-hi.txt.zip",
    ("am", "hr"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/am-hr.txt.zip",
    ("am", "hu"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/am-hu.txt.zip",
    ("am", "hy"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/am-hy.txt.zip",
    ("am", "id"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/am-id.txt.zip",
    ("am", "is"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/am-is.txt.zip",
    ("am", "it"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/am-it.txt.zip",
    (
        "am",
        "jak",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/am-jak.txt.zip",
    (
        "am",
        "jap",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/am-jap.txt.zip",
    (
        "am",
        "jiv",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/am-jiv.txt.zip",
    (
        "am",
        "kab",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/am-kab.txt.zip",
    (
        "am",
        "kbh",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/am-kbh.txt.zip",
    (
        "am",
        "kek",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/am-kek.txt.zip",
    ("am", "kn"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/am-kn.txt.zip",
    ("am", "ko"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/am-ko.txt.zip",
    ("am", "la"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/am-la.txt.zip",
    ("am", "lt"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/am-lt.txt.zip",
    ("am", "lv"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/am-lv.txt.zip",
    (
        "am",
        "mam",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/am-mam.txt.zip",
    ("am", "mi"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/am-mi.txt.zip",
    ("am", "ml"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/am-ml.txt.zip",
    ("am", "mr"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/am-mr.txt.zip",
    ("am", "my"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/am-my.txt.zip",
    ("am", "ne"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/am-ne.txt.zip",
    (
        "am",
        "nhg",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/am-nhg.txt.zip",
    ("am", "nl"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/am-nl.txt.zip",
    ("am", "no"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/am-no.txt.zip",
    (
        "am",
        "ojb",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/am-ojb.txt.zip",
    (
        "am",
        "pck",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/am-pck.txt.zip",
    (
        "am",
        "pes",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/am-pes.txt.zip",
    ("am", "pl"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/am-pl.txt.zip",
    (
        "am",
        "plt",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/am-plt.txt.zip",
    (
        "am",
        "pot",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/am-pot.txt.zip",
    (
        "am",
        "ppk",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/am-ppk.txt.zip",
    ("am", "pt"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/am-pt.txt.zip",
    (
        "am",
        "quc",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/am-quc.txt.zip",
    (
        "am",
        "quw",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/am-quw.txt.zip",
    ("am", "ro"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/am-ro.txt.zip",
    (
        "am",
        "rom",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/am-rom.txt.zip",
    ("am", "ru"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/am-ru.txt.zip",
    (
        "am",
        "shi",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/am-shi.txt.zip",
    ("am", "sk"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/am-sk.txt.zip",
    ("am", "sl"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/am-sl.txt.zip",
    ("am", "sn"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/am-sn.txt.zip",
    ("am", "so"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/am-so.txt.zip",
    ("am", "sq"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/am-sq.txt.zip",
    ("am", "sr"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/am-sr.txt.zip",
    ("am", "ss"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/am-ss.txt.zip",
    ("am", "sv"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/am-sv.txt.zip",
    (
        "am",
        "syr",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/am-syr.txt.zip",
    ("am", "te"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/am-te.txt.zip",
    ("am", "th"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/am-th.txt.zip",
    ("am", "tl"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/am-tl.txt.zip",
    (
        "am",
        "tmh",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/am-tmh.txt.zip",
    ("am", "tr"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/am-tr.txt.zip",
    ("am", "uk"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/am-uk.txt.zip",
    (
        "am",
        "usp",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/am-usp.txt.zip",
    ("am", "vi"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/am-vi.txt.zip",
    (
        "am",
        "wal",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/am-wal.txt.zip",
    ("am", "wo"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/am-wo.txt.zip",
    ("am", "xh"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/am-xh.txt.zip",
    ("am", "zh"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/am-zh.txt.zip",
    ("am", "zu"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/am-zu.txt.zip",
    (
        "amu",
        "ar",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/amu-ar.txt.zip",
    (
        "amu",
        "bg",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/amu-bg.txt.zip",
    (
        "amu",
        "bsn",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/amu-bsn.txt.zip",
    (
        "amu",
        "cak",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/amu-cak.txt.zip",
    (
        "amu",
        "ceb",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/amu-ceb.txt.zip",
    (
        "amu",
        "ch",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/amu-ch.txt.zip",
    (
        "amu",
        "chq",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/amu-chq.txt.zip",
    (
        "amu",
        "chr",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/amu-chr.txt.zip",
    (
        "amu",
        "cjp",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/amu-cjp.txt.zip",
    (
        "amu",
        "cni",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/amu-cni.txt.zip",
    (
        "amu",
        "cop",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/amu-cop.txt.zip",
    (
        "amu",
        "crp",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/amu-crp.txt.zip",
    (
        "amu",
        "cs",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/amu-cs.txt.zip",
    (
        "amu",
        "da",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/amu-da.txt.zip",
    (
        "amu",
        "de",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/amu-de.txt.zip",
    (
        "amu",
        "dik",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/amu-dik.txt.zip",
    (
        "amu",
        "dje",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/amu-dje.txt.zip",
    (
        "amu",
        "djk",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/amu-djk.txt.zip",
    (
        "amu",
        "dop",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/amu-dop.txt.zip",
    (
        "amu",
        "ee",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/amu-ee.txt.zip",
    (
        "amu",
        "el",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/amu-el.txt.zip",
    (
        "amu",
        "en",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/amu-en.txt.zip",
    (
        "amu",
        "eo",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/amu-eo.txt.zip",
    (
        "amu",
        "es",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/amu-es.txt.zip",
    (
        "amu",
        "et",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/amu-et.txt.zip",
    (
        "amu",
        "eu",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/amu-eu.txt.zip",
    (
        "amu",
        "fi",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/amu-fi.txt.zip",
    (
        "amu",
        "fr",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/amu-fr.txt.zip",
    (
        "amu",
        "gbi",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/amu-gbi.txt.zip",
    (
        "amu",
        "gd",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/amu-gd.txt.zip",
    (
        "amu",
        "gu",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/amu-gu.txt.zip",
    (
        "amu",
        "gv",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/amu-gv.txt.zip",
    (
        "amu",
        "he",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/amu-he.txt.zip",
    (
        "amu",
        "hi",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/amu-hi.txt.zip",
    (
        "amu",
        "hr",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/amu-hr.txt.zip",
    (
        "amu",
        "hu",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/amu-hu.txt.zip",
    (
        "amu",
        "hy",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/amu-hy.txt.zip",
    (
        "amu",
        "id",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/amu-id.txt.zip",
    (
        "amu",
        "is",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/amu-is.txt.zip",
    (
        "amu",
        "it",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/amu-it.txt.zip",
    (
        "amu",
        "jak",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/amu-jak.txt.zip",
    (
        "amu",
        "jap",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/amu-jap.txt.zip",
    (
        "amu",
        "jiv",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/amu-jiv.txt.zip",
    (
        "amu",
        "kab",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/amu-kab.txt.zip",
    (
        "amu",
        "kbh",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/amu-kbh.txt.zip",
    (
        "amu",
        "kek",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/amu-kek.txt.zip",
    (
        "amu",
        "kn",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/amu-kn.txt.zip",
    (
        "amu",
        "ko",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/amu-ko.txt.zip",
    (
        "amu",
        "la",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/amu-la.txt.zip",
    (
        "amu",
        "lt",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/amu-lt.txt.zip",
    (
        "amu",
        "lv",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/amu-lv.txt.zip",
    (
        "amu",
        "mam",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/amu-mam.txt.zip",
    (
        "amu",
        "mi",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/amu-mi.txt.zip",
    (
        "amu",
        "ml",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/amu-ml.txt.zip",
    (
        "amu",
        "mr",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/amu-mr.txt.zip",
    (
        "amu",
        "my",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/amu-my.txt.zip",
    (
        "amu",
        "ne",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/amu-ne.txt.zip",
    (
        "amu",
        "nhg",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/amu-nhg.txt.zip",
    (
        "amu",
        "nl",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/amu-nl.txt.zip",
    (
        "amu",
        "no",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/amu-no.txt.zip",
    (
        "amu",
        "ojb",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/amu-ojb.txt.zip",
    (
        "amu",
        "pck",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/amu-pck.txt.zip",
    (
        "amu",
        "pes",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/amu-pes.txt.zip",
    (
        "amu",
        "pl",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/amu-pl.txt.zip",
    (
        "amu",
        "plt",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/amu-plt.txt.zip",
    (
        "amu",
        "pot",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/amu-pot.txt.zip",
    (
        "amu",
        "ppk",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/amu-ppk.txt.zip",
    (
        "amu",
        "pt",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/amu-pt.txt.zip",
    (
        "amu",
        "quc",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/amu-quc.txt.zip",
    (
        "amu",
        "quw",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/amu-quw.txt.zip",
    (
        "amu",
        "ro",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/amu-ro.txt.zip",
    (
        "amu",
        "rom",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/amu-rom.txt.zip",
    (
        "amu",
        "ru",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/amu-ru.txt.zip",
    (
        "amu",
        "shi",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/amu-shi.txt.zip",
    (
        "amu",
        "sk",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/amu-sk.txt.zip",
    (
        "amu",
        "sl",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/amu-sl.txt.zip",
    (
        "amu",
        "sn",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/amu-sn.txt.zip",
    (
        "amu",
        "so",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/amu-so.txt.zip",
    (
        "amu",
        "sq",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/amu-sq.txt.zip",
    (
        "amu",
        "sr",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/amu-sr.txt.zip",
    (
        "amu",
        "ss",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/amu-ss.txt.zip",
    (
        "amu",
        "sv",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/amu-sv.txt.zip",
    (
        "amu",
        "syr",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/amu-syr.txt.zip",
    (
        "amu",
        "te",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/amu-te.txt.zip",
    (
        "amu",
        "th",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/amu-th.txt.zip",
    (
        "amu",
        "tl",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/amu-tl.txt.zip",
    (
        "amu",
        "tmh",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/amu-tmh.txt.zip",
    (
        "amu",
        "tr",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/amu-tr.txt.zip",
    (
        "amu",
        "uk",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/amu-uk.txt.zip",
    (
        "amu",
        "usp",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/amu-usp.txt.zip",
    (
        "amu",
        "vi",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/amu-vi.txt.zip",
    (
        "amu",
        "wal",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/amu-wal.txt.zip",
    (
        "amu",
        "wo",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/amu-wo.txt.zip",
    (
        "amu",
        "xh",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/amu-xh.txt.zip",
    (
        "amu",
        "zh",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/amu-zh.txt.zip",
    (
        "amu",
        "zu",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/amu-zu.txt.zip",
    ("ar", "bg"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ar-bg.txt.zip",
    (
        "ar",
        "bsn",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ar-bsn.txt.zip",
    (
        "ar",
        "cak",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ar-cak.txt.zip",
    (
        "ar",
        "ceb",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ar-ceb.txt.zip",
    ("ar", "ch"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ar-ch.txt.zip",
    (
        "ar",
        "chq",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ar-chq.txt.zip",
    (
        "ar",
        "chr",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ar-chr.txt.zip",
    (
        "ar",
        "cjp",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ar-cjp.txt.zip",
    (
        "ar",
        "cni",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ar-cni.txt.zip",
    (
        "ar",
        "cop",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ar-cop.txt.zip",
    (
        "ar",
        "crp",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ar-crp.txt.zip",
    ("ar", "cs"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ar-cs.txt.zip",
    ("ar", "da"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ar-da.txt.zip",
    ("ar", "de"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ar-de.txt.zip",
    (
        "ar",
        "dik",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ar-dik.txt.zip",
    (
        "ar",
        "dje",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ar-dje.txt.zip",
    (
        "ar",
        "djk",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ar-djk.txt.zip",
    (
        "ar",
        "dop",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ar-dop.txt.zip",
    ("ar", "ee"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ar-ee.txt.zip",
    ("ar", "el"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ar-el.txt.zip",
    ("ar", "en"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ar-en.txt.zip",
    ("ar", "eo"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ar-eo.txt.zip",
    ("ar", "es"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ar-es.txt.zip",
    ("ar", "et"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ar-et.txt.zip",
    ("ar", "eu"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ar-eu.txt.zip",
    ("ar", "fi"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ar-fi.txt.zip",
    ("ar", "fr"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ar-fr.txt.zip",
    (
        "ar",
        "gbi",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ar-gbi.txt.zip",
    ("ar", "gd"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ar-gd.txt.zip",
    ("ar", "gu"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ar-gu.txt.zip",
    ("ar", "gv"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ar-gv.txt.zip",
    ("ar", "he"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ar-he.txt.zip",
    ("ar", "hi"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ar-hi.txt.zip",
    ("ar", "hr"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ar-hr.txt.zip",
    ("ar", "hu"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ar-hu.txt.zip",
    ("ar", "hy"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ar-hy.txt.zip",
    ("ar", "id"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ar-id.txt.zip",
    ("ar", "is"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ar-is.txt.zip",
    ("ar", "it"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ar-it.txt.zip",
    (
        "ar",
        "jak",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ar-jak.txt.zip",
    (
        "ar",
        "jap",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ar-jap.txt.zip",
    (
        "ar",
        "jiv",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ar-jiv.txt.zip",
    (
        "ar",
        "kab",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ar-kab.txt.zip",
    (
        "ar",
        "kbh",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ar-kbh.txt.zip",
    (
        "ar",
        "kek",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ar-kek.txt.zip",
    ("ar", "kn"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ar-kn.txt.zip",
    ("ar", "ko"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ar-ko.txt.zip",
    ("ar", "la"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ar-la.txt.zip",
    ("ar", "lt"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ar-lt.txt.zip",
    ("ar", "lv"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ar-lv.txt.zip",
    (
        "ar",
        "mam",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ar-mam.txt.zip",
    ("ar", "mi"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ar-mi.txt.zip",
    ("ar", "ml"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ar-ml.txt.zip",
    ("ar", "mr"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ar-mr.txt.zip",
    ("ar", "my"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ar-my.txt.zip",
    ("ar", "ne"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ar-ne.txt.zip",
    (
        "ar",
        "nhg",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ar-nhg.txt.zip",
    ("ar", "nl"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ar-nl.txt.zip",
    ("ar", "no"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ar-no.txt.zip",
    (
        "ar",
        "ojb",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ar-ojb.txt.zip",
    (
        "ar",
        "pck",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ar-pck.txt.zip",
    (
        "ar",
        "pes",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ar-pes.txt.zip",
    ("ar", "pl"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ar-pl.txt.zip",
    (
        "ar",
        "plt",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ar-plt.txt.zip",
    (
        "ar",
        "pot",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ar-pot.txt.zip",
    (
        "ar",
        "ppk",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ar-ppk.txt.zip",
    ("ar", "pt"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ar-pt.txt.zip",
    (
        "ar",
        "quc",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ar-quc.txt.zip",
    (
        "ar",
        "quw",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ar-quw.txt.zip",
    ("ar", "ro"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ar-ro.txt.zip",
    (
        "ar",
        "rom",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ar-rom.txt.zip",
    ("ar", "ru"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ar-ru.txt.zip",
    (
        "ar",
        "shi",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ar-shi.txt.zip",
    ("ar", "sk"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ar-sk.txt.zip",
    ("ar", "sl"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ar-sl.txt.zip",
    ("ar", "sn"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ar-sn.txt.zip",
    ("ar", "so"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ar-so.txt.zip",
    ("ar", "sq"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ar-sq.txt.zip",
    ("ar", "sr"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ar-sr.txt.zip",
    ("ar", "ss"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ar-ss.txt.zip",
    ("ar", "sv"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ar-sv.txt.zip",
    (
        "ar",
        "syr",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ar-syr.txt.zip",
    ("ar", "te"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ar-te.txt.zip",
    ("ar", "th"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ar-th.txt.zip",
    ("ar", "tl"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ar-tl.txt.zip",
    (
        "ar",
        "tmh",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ar-tmh.txt.zip",
    ("ar", "tr"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ar-tr.txt.zip",
    ("ar", "uk"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ar-uk.txt.zip",
    (
        "ar",
        "usp",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ar-usp.txt.zip",
    ("ar", "vi"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ar-vi.txt.zip",
    (
        "ar",
        "wal",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ar-wal.txt.zip",
    ("ar", "wo"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ar-wo.txt.zip",
    ("ar", "xh"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ar-xh.txt.zip",
    ("ar", "zh"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ar-zh.txt.zip",
    ("ar", "zu"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ar-zu.txt.zip",
    (
        "bg",
        "bsn",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/bg-bsn.txt.zip",
    (
        "bg",
        "cak",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/bg-cak.txt.zip",
    (
        "bg",
        "ceb",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/bg-ceb.txt.zip",
    ("bg", "ch"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/bg-ch.txt.zip",
    (
        "bg",
        "chq",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/bg-chq.txt.zip",
    (
        "bg",
        "chr",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/bg-chr.txt.zip",
    (
        "bg",
        "cjp",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/bg-cjp.txt.zip",
    (
        "bg",
        "cni",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/bg-cni.txt.zip",
    (
        "bg",
        "cop",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/bg-cop.txt.zip",
    (
        "bg",
        "crp",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/bg-crp.txt.zip",
    ("bg", "cs"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/bg-cs.txt.zip",
    ("bg", "da"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/bg-da.txt.zip",
    ("bg", "de"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/bg-de.txt.zip",
    (
        "bg",
        "dik",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/bg-dik.txt.zip",
    (
        "bg",
        "dje",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/bg-dje.txt.zip",
    (
        "bg",
        "djk",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/bg-djk.txt.zip",
    (
        "bg",
        "dop",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/bg-dop.txt.zip",
    ("bg", "ee"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/bg-ee.txt.zip",
    ("bg", "el"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/bg-el.txt.zip",
    ("bg", "en"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/bg-en.txt.zip",
    ("bg", "eo"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/bg-eo.txt.zip",
    ("bg", "es"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/bg-es.txt.zip",
    ("bg", "et"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/bg-et.txt.zip",
    ("bg", "eu"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/bg-eu.txt.zip",
    ("bg", "fi"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/bg-fi.txt.zip",
    ("bg", "fr"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/bg-fr.txt.zip",
    (
        "bg",
        "gbi",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/bg-gbi.txt.zip",
    ("bg", "gd"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/bg-gd.txt.zip",
    ("bg", "gu"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/bg-gu.txt.zip",
    ("bg", "gv"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/bg-gv.txt.zip",
    ("bg", "he"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/bg-he.txt.zip",
    ("bg", "hi"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/bg-hi.txt.zip",
    ("bg", "hr"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/bg-hr.txt.zip",
    ("bg", "hu"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/bg-hu.txt.zip",
    ("bg", "hy"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/bg-hy.txt.zip",
    ("bg", "id"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/bg-id.txt.zip",
    ("bg", "is"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/bg-is.txt.zip",
    ("bg", "it"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/bg-it.txt.zip",
    (
        "bg",
        "jak",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/bg-jak.txt.zip",
    (
        "bg",
        "jap",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/bg-jap.txt.zip",
    (
        "bg",
        "jiv",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/bg-jiv.txt.zip",
    (
        "bg",
        "kab",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/bg-kab.txt.zip",
    (
        "bg",
        "kbh",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/bg-kbh.txt.zip",
    (
        "bg",
        "kek",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/bg-kek.txt.zip",
    ("bg", "kn"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/bg-kn.txt.zip",
    ("bg", "ko"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/bg-ko.txt.zip",
    ("bg", "la"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/bg-la.txt.zip",
    ("bg", "lt"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/bg-lt.txt.zip",
    ("bg", "lv"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/bg-lv.txt.zip",
    (
        "bg",
        "mam",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/bg-mam.txt.zip",
    ("bg", "mi"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/bg-mi.txt.zip",
    ("bg", "ml"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/bg-ml.txt.zip",
    ("bg", "mr"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/bg-mr.txt.zip",
    ("bg", "my"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/bg-my.txt.zip",
    ("bg", "ne"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/bg-ne.txt.zip",
    (
        "bg",
        "nhg",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/bg-nhg.txt.zip",
    ("bg", "nl"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/bg-nl.txt.zip",
    ("bg", "no"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/bg-no.txt.zip",
    (
        "bg",
        "ojb",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/bg-ojb.txt.zip",
    (
        "bg",
        "pck",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/bg-pck.txt.zip",
    (
        "bg",
        "pes",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/bg-pes.txt.zip",
    ("bg", "pl"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/bg-pl.txt.zip",
    (
        "bg",
        "plt",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/bg-plt.txt.zip",
    (
        "bg",
        "pot",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/bg-pot.txt.zip",
    (
        "bg",
        "ppk",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/bg-ppk.txt.zip",
    ("bg", "pt"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/bg-pt.txt.zip",
    (
        "bg",
        "quc",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/bg-quc.txt.zip",
    (
        "bg",
        "quw",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/bg-quw.txt.zip",
    ("bg", "ro"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/bg-ro.txt.zip",
    (
        "bg",
        "rom",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/bg-rom.txt.zip",
    ("bg", "ru"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/bg-ru.txt.zip",
    (
        "bg",
        "shi",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/bg-shi.txt.zip",
    ("bg", "sk"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/bg-sk.txt.zip",
    ("bg", "sl"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/bg-sl.txt.zip",
    ("bg", "sn"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/bg-sn.txt.zip",
    ("bg", "so"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/bg-so.txt.zip",
    ("bg", "sq"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/bg-sq.txt.zip",
    ("bg", "sr"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/bg-sr.txt.zip",
    ("bg", "ss"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/bg-ss.txt.zip",
    ("bg", "sv"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/bg-sv.txt.zip",
    (
        "bg",
        "syr",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/bg-syr.txt.zip",
    ("bg", "te"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/bg-te.txt.zip",
    ("bg", "th"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/bg-th.txt.zip",
    ("bg", "tl"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/bg-tl.txt.zip",
    (
        "bg",
        "tmh",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/bg-tmh.txt.zip",
    ("bg", "tr"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/bg-tr.txt.zip",
    ("bg", "uk"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/bg-uk.txt.zip",
    (
        "bg",
        "usp",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/bg-usp.txt.zip",
    ("bg", "vi"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/bg-vi.txt.zip",
    (
        "bg",
        "wal",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/bg-wal.txt.zip",
    ("bg", "wo"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/bg-wo.txt.zip",
    ("bg", "xh"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/bg-xh.txt.zip",
    ("bg", "zh"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/bg-zh.txt.zip",
    ("bg", "zu"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/bg-zu.txt.zip",
    (
        "bsn",
        "cak",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/bsn-cak.txt.zip",
    (
        "bsn",
        "ceb",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/bsn-ceb.txt.zip",
    (
        "bsn",
        "ch",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/bsn-ch.txt.zip",
    (
        "bsn",
        "chq",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/bsn-chq.txt.zip",
    (
        "bsn",
        "chr",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/bsn-chr.txt.zip",
    (
        "bsn",
        "cjp",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/bsn-cjp.txt.zip",
    (
        "bsn",
        "cni",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/bsn-cni.txt.zip",
    (
        "bsn",
        "cop",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/bsn-cop.txt.zip",
    (
        "bsn",
        "crp",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/bsn-crp.txt.zip",
    (
        "bsn",
        "cs",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/bsn-cs.txt.zip",
    (
        "bsn",
        "da",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/bsn-da.txt.zip",
    (
        "bsn",
        "de",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/bsn-de.txt.zip",
    (
        "bsn",
        "dik",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/bsn-dik.txt.zip",
    (
        "bsn",
        "dje",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/bsn-dje.txt.zip",
    (
        "bsn",
        "djk",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/bsn-djk.txt.zip",
    (
        "bsn",
        "dop",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/bsn-dop.txt.zip",
    (
        "bsn",
        "ee",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/bsn-ee.txt.zip",
    (
        "bsn",
        "el",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/bsn-el.txt.zip",
    (
        "bsn",
        "en",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/bsn-en.txt.zip",
    (
        "bsn",
        "eo",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/bsn-eo.txt.zip",
    (
        "bsn",
        "es",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/bsn-es.txt.zip",
    (
        "bsn",
        "et",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/bsn-et.txt.zip",
    (
        "bsn",
        "eu",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/bsn-eu.txt.zip",
    (
        "bsn",
        "fi",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/bsn-fi.txt.zip",
    (
        "bsn",
        "fr",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/bsn-fr.txt.zip",
    (
        "bsn",
        "gbi",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/bsn-gbi.txt.zip",
    (
        "bsn",
        "gd",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/bsn-gd.txt.zip",
    (
        "bsn",
        "gu",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/bsn-gu.txt.zip",
    (
        "bsn",
        "gv",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/bsn-gv.txt.zip",
    (
        "bsn",
        "he",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/bsn-he.txt.zip",
    (
        "bsn",
        "hi",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/bsn-hi.txt.zip",
    (
        "bsn",
        "hr",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/bsn-hr.txt.zip",
    (
        "bsn",
        "hu",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/bsn-hu.txt.zip",
    (
        "bsn",
        "hy",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/bsn-hy.txt.zip",
    (
        "bsn",
        "id",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/bsn-id.txt.zip",
    (
        "bsn",
        "is",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/bsn-is.txt.zip",
    (
        "bsn",
        "it",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/bsn-it.txt.zip",
    (
        "bsn",
        "jak",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/bsn-jak.txt.zip",
    (
        "bsn",
        "jap",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/bsn-jap.txt.zip",
    (
        "bsn",
        "jiv",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/bsn-jiv.txt.zip",
    (
        "bsn",
        "kab",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/bsn-kab.txt.zip",
    (
        "bsn",
        "kbh",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/bsn-kbh.txt.zip",
    (
        "bsn",
        "kek",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/bsn-kek.txt.zip",
    (
        "bsn",
        "kn",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/bsn-kn.txt.zip",
    (
        "bsn",
        "ko",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/bsn-ko.txt.zip",
    (
        "bsn",
        "la",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/bsn-la.txt.zip",
    (
        "bsn",
        "lt",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/bsn-lt.txt.zip",
    (
        "bsn",
        "lv",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/bsn-lv.txt.zip",
    (
        "bsn",
        "mam",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/bsn-mam.txt.zip",
    (
        "bsn",
        "mi",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/bsn-mi.txt.zip",
    (
        "bsn",
        "ml",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/bsn-ml.txt.zip",
    (
        "bsn",
        "mr",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/bsn-mr.txt.zip",
    (
        "bsn",
        "my",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/bsn-my.txt.zip",
    (
        "bsn",
        "ne",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/bsn-ne.txt.zip",
    (
        "bsn",
        "nhg",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/bsn-nhg.txt.zip",
    (
        "bsn",
        "nl",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/bsn-nl.txt.zip",
    (
        "bsn",
        "no",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/bsn-no.txt.zip",
    (
        "bsn",
        "ojb",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/bsn-ojb.txt.zip",
    (
        "bsn",
        "pck",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/bsn-pck.txt.zip",
    (
        "bsn",
        "pes",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/bsn-pes.txt.zip",
    (
        "bsn",
        "pl",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/bsn-pl.txt.zip",
    (
        "bsn",
        "plt",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/bsn-plt.txt.zip",
    (
        "bsn",
        "pot",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/bsn-pot.txt.zip",
    (
        "bsn",
        "ppk",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/bsn-ppk.txt.zip",
    (
        "bsn",
        "pt",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/bsn-pt.txt.zip",
    (
        "bsn",
        "quc",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/bsn-quc.txt.zip",
    (
        "bsn",
        "quw",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/bsn-quw.txt.zip",
    (
        "bsn",
        "ro",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/bsn-ro.txt.zip",
    (
        "bsn",
        "rom",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/bsn-rom.txt.zip",
    (
        "bsn",
        "ru",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/bsn-ru.txt.zip",
    (
        "bsn",
        "shi",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/bsn-shi.txt.zip",
    (
        "bsn",
        "sk",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/bsn-sk.txt.zip",
    (
        "bsn",
        "sl",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/bsn-sl.txt.zip",
    (
        "bsn",
        "sn",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/bsn-sn.txt.zip",
    (
        "bsn",
        "so",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/bsn-so.txt.zip",
    (
        "bsn",
        "sq",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/bsn-sq.txt.zip",
    (
        "bsn",
        "sr",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/bsn-sr.txt.zip",
    (
        "bsn",
        "ss",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/bsn-ss.txt.zip",
    (
        "bsn",
        "sv",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/bsn-sv.txt.zip",
    (
        "bsn",
        "syr",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/bsn-syr.txt.zip",
    (
        "bsn",
        "te",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/bsn-te.txt.zip",
    (
        "bsn",
        "th",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/bsn-th.txt.zip",
    (
        "bsn",
        "tl",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/bsn-tl.txt.zip",
    (
        "bsn",
        "tmh",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/bsn-tmh.txt.zip",
    (
        "bsn",
        "tr",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/bsn-tr.txt.zip",
    (
        "bsn",
        "uk",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/bsn-uk.txt.zip",
    (
        "bsn",
        "usp",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/bsn-usp.txt.zip",
    (
        "bsn",
        "vi",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/bsn-vi.txt.zip",
    (
        "bsn",
        "wal",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/bsn-wal.txt.zip",
    (
        "bsn",
        "wo",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/bsn-wo.txt.zip",
    (
        "bsn",
        "xh",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/bsn-xh.txt.zip",
    (
        "bsn",
        "zh",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/bsn-zh.txt.zip",
    (
        "bsn",
        "zu",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/bsn-zu.txt.zip",
    (
        "cak",
        "ceb",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cak-ceb.txt.zip",
    (
        "cak",
        "ch",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cak-ch.txt.zip",
    (
        "cak",
        "chq",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cak-chq.txt.zip",
    (
        "cak",
        "chr",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cak-chr.txt.zip",
    (
        "cak",
        "cjp",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cak-cjp.txt.zip",
    (
        "cak",
        "cni",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cak-cni.txt.zip",
    (
        "cak",
        "cop",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cak-cop.txt.zip",
    (
        "cak",
        "crp",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cak-crp.txt.zip",
    (
        "cak",
        "cs",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cak-cs.txt.zip",
    (
        "cak",
        "da",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cak-da.txt.zip",
    (
        "cak",
        "de",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cak-de.txt.zip",
    (
        "cak",
        "dik",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cak-dik.txt.zip",
    (
        "cak",
        "dje",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cak-dje.txt.zip",
    (
        "cak",
        "djk",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cak-djk.txt.zip",
    (
        "cak",
        "dop",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cak-dop.txt.zip",
    (
        "cak",
        "ee",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cak-ee.txt.zip",
    (
        "cak",
        "el",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cak-el.txt.zip",
    (
        "cak",
        "en",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cak-en.txt.zip",
    (
        "cak",
        "eo",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cak-eo.txt.zip",
    (
        "cak",
        "es",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cak-es.txt.zip",
    (
        "cak",
        "et",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cak-et.txt.zip",
    (
        "cak",
        "eu",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cak-eu.txt.zip",
    (
        "cak",
        "fi",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cak-fi.txt.zip",
    (
        "cak",
        "fr",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cak-fr.txt.zip",
    (
        "cak",
        "gbi",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cak-gbi.txt.zip",
    (
        "cak",
        "gd",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cak-gd.txt.zip",
    (
        "cak",
        "gu",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cak-gu.txt.zip",
    (
        "cak",
        "gv",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cak-gv.txt.zip",
    (
        "cak",
        "he",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cak-he.txt.zip",
    (
        "cak",
        "hi",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cak-hi.txt.zip",
    (
        "cak",
        "hr",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cak-hr.txt.zip",
    (
        "cak",
        "hu",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cak-hu.txt.zip",
    (
        "cak",
        "hy",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cak-hy.txt.zip",
    (
        "cak",
        "id",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cak-id.txt.zip",
    (
        "cak",
        "is",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cak-is.txt.zip",
    (
        "cak",
        "it",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cak-it.txt.zip",
    (
        "cak",
        "jak",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cak-jak.txt.zip",
    (
        "cak",
        "jap",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cak-jap.txt.zip",
    (
        "cak",
        "jiv",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cak-jiv.txt.zip",
    (
        "cak",
        "kab",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cak-kab.txt.zip",
    (
        "cak",
        "kbh",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cak-kbh.txt.zip",
    (
        "cak",
        "kek",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cak-kek.txt.zip",
    (
        "cak",
        "kn",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cak-kn.txt.zip",
    (
        "cak",
        "ko",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cak-ko.txt.zip",
    (
        "cak",
        "la",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cak-la.txt.zip",
    (
        "cak",
        "lt",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cak-lt.txt.zip",
    (
        "cak",
        "lv",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cak-lv.txt.zip",
    (
        "cak",
        "mam",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cak-mam.txt.zip",
    (
        "cak",
        "mi",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cak-mi.txt.zip",
    (
        "cak",
        "ml",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cak-ml.txt.zip",
    (
        "cak",
        "mr",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cak-mr.txt.zip",
    (
        "cak",
        "my",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cak-my.txt.zip",
    (
        "cak",
        "ne",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cak-ne.txt.zip",
    (
        "cak",
        "nhg",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cak-nhg.txt.zip",
    (
        "cak",
        "nl",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cak-nl.txt.zip",
    (
        "cak",
        "no",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cak-no.txt.zip",
    (
        "cak",
        "ojb",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cak-ojb.txt.zip",
    (
        "cak",
        "pck",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cak-pck.txt.zip",
    (
        "cak",
        "pes",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cak-pes.txt.zip",
    (
        "cak",
        "pl",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cak-pl.txt.zip",
    (
        "cak",
        "plt",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cak-plt.txt.zip",
    (
        "cak",
        "pot",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cak-pot.txt.zip",
    (
        "cak",
        "ppk",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cak-ppk.txt.zip",
    (
        "cak",
        "pt",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cak-pt.txt.zip",
    (
        "cak",
        "quc",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cak-quc.txt.zip",
    (
        "cak",
        "quw",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cak-quw.txt.zip",
    (
        "cak",
        "ro",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cak-ro.txt.zip",
    (
        "cak",
        "rom",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cak-rom.txt.zip",
    (
        "cak",
        "ru",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cak-ru.txt.zip",
    (
        "cak",
        "shi",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cak-shi.txt.zip",
    (
        "cak",
        "sk",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cak-sk.txt.zip",
    (
        "cak",
        "sl",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cak-sl.txt.zip",
    (
        "cak",
        "sn",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cak-sn.txt.zip",
    (
        "cak",
        "so",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cak-so.txt.zip",
    (
        "cak",
        "sq",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cak-sq.txt.zip",
    (
        "cak",
        "sr",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cak-sr.txt.zip",
    (
        "cak",
        "ss",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cak-ss.txt.zip",
    (
        "cak",
        "sv",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cak-sv.txt.zip",
    (
        "cak",
        "syr",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cak-syr.txt.zip",
    (
        "cak",
        "te",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cak-te.txt.zip",
    (
        "cak",
        "th",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cak-th.txt.zip",
    (
        "cak",
        "tl",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cak-tl.txt.zip",
    (
        "cak",
        "tmh",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cak-tmh.txt.zip",
    (
        "cak",
        "tr",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cak-tr.txt.zip",
    (
        "cak",
        "uk",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cak-uk.txt.zip",
    (
        "cak",
        "usp",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cak-usp.txt.zip",
    (
        "cak",
        "vi",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cak-vi.txt.zip",
    (
        "cak",
        "wal",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cak-wal.txt.zip",
    (
        "cak",
        "wo",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cak-wo.txt.zip",
    (
        "cak",
        "xh",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cak-xh.txt.zip",
    (
        "cak",
        "zh",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cak-zh.txt.zip",
    (
        "cak",
        "zu",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cak-zu.txt.zip",
    (
        "ceb",
        "ch",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ceb-ch.txt.zip",
    (
        "ceb",
        "chq",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ceb-chq.txt.zip",
    (
        "ceb",
        "chr",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ceb-chr.txt.zip",
    (
        "ceb",
        "cjp",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ceb-cjp.txt.zip",
    (
        "ceb",
        "cni",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ceb-cni.txt.zip",
    (
        "ceb",
        "cop",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ceb-cop.txt.zip",
    (
        "ceb",
        "crp",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ceb-crp.txt.zip",
    (
        "ceb",
        "cs",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ceb-cs.txt.zip",
    (
        "ceb",
        "da",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ceb-da.txt.zip",
    (
        "ceb",
        "de",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ceb-de.txt.zip",
    (
        "ceb",
        "dik",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ceb-dik.txt.zip",
    (
        "ceb",
        "dje",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ceb-dje.txt.zip",
    (
        "ceb",
        "djk",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ceb-djk.txt.zip",
    (
        "ceb",
        "dop",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ceb-dop.txt.zip",
    (
        "ceb",
        "ee",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ceb-ee.txt.zip",
    (
        "ceb",
        "el",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ceb-el.txt.zip",
    (
        "ceb",
        "en",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ceb-en.txt.zip",
    (
        "ceb",
        "eo",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ceb-eo.txt.zip",
    (
        "ceb",
        "es",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ceb-es.txt.zip",
    (
        "ceb",
        "et",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ceb-et.txt.zip",
    (
        "ceb",
        "eu",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ceb-eu.txt.zip",
    (
        "ceb",
        "fi",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ceb-fi.txt.zip",
    (
        "ceb",
        "fr",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ceb-fr.txt.zip",
    (
        "ceb",
        "gbi",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ceb-gbi.txt.zip",
    (
        "ceb",
        "gd",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ceb-gd.txt.zip",
    (
        "ceb",
        "gu",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ceb-gu.txt.zip",
    (
        "ceb",
        "gv",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ceb-gv.txt.zip",
    (
        "ceb",
        "he",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ceb-he.txt.zip",
    (
        "ceb",
        "hi",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ceb-hi.txt.zip",
    (
        "ceb",
        "hr",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ceb-hr.txt.zip",
    (
        "ceb",
        "hu",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ceb-hu.txt.zip",
    (
        "ceb",
        "hy",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ceb-hy.txt.zip",
    (
        "ceb",
        "id",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ceb-id.txt.zip",
    (
        "ceb",
        "is",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ceb-is.txt.zip",
    (
        "ceb",
        "it",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ceb-it.txt.zip",
    (
        "ceb",
        "jak",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ceb-jak.txt.zip",
    (
        "ceb",
        "jap",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ceb-jap.txt.zip",
    (
        "ceb",
        "jiv",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ceb-jiv.txt.zip",
    (
        "ceb",
        "kab",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ceb-kab.txt.zip",
    (
        "ceb",
        "kbh",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ceb-kbh.txt.zip",
    (
        "ceb",
        "kek",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ceb-kek.txt.zip",
    (
        "ceb",
        "kn",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ceb-kn.txt.zip",
    (
        "ceb",
        "ko",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ceb-ko.txt.zip",
    (
        "ceb",
        "la",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ceb-la.txt.zip",
    (
        "ceb",
        "lt",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ceb-lt.txt.zip",
    (
        "ceb",
        "lv",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ceb-lv.txt.zip",
    (
        "ceb",
        "mam",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ceb-mam.txt.zip",
    (
        "ceb",
        "mi",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ceb-mi.txt.zip",
    (
        "ceb",
        "ml",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ceb-ml.txt.zip",
    (
        "ceb",
        "mr",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ceb-mr.txt.zip",
    (
        "ceb",
        "my",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ceb-my.txt.zip",
    (
        "ceb",
        "ne",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ceb-ne.txt.zip",
    (
        "ceb",
        "nhg",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ceb-nhg.txt.zip",
    (
        "ceb",
        "nl",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ceb-nl.txt.zip",
    (
        "ceb",
        "no",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ceb-no.txt.zip",
    (
        "ceb",
        "ojb",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ceb-ojb.txt.zip",
    (
        "ceb",
        "pck",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ceb-pck.txt.zip",
    (
        "ceb",
        "pes",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ceb-pes.txt.zip",
    (
        "ceb",
        "pl",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ceb-pl.txt.zip",
    (
        "ceb",
        "plt",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ceb-plt.txt.zip",
    (
        "ceb",
        "pot",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ceb-pot.txt.zip",
    (
        "ceb",
        "ppk",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ceb-ppk.txt.zip",
    (
        "ceb",
        "pt",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ceb-pt.txt.zip",
    (
        "ceb",
        "quc",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ceb-quc.txt.zip",
    (
        "ceb",
        "quw",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ceb-quw.txt.zip",
    (
        "ceb",
        "ro",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ceb-ro.txt.zip",
    (
        "ceb",
        "rom",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ceb-rom.txt.zip",
    (
        "ceb",
        "ru",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ceb-ru.txt.zip",
    (
        "ceb",
        "shi",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ceb-shi.txt.zip",
    (
        "ceb",
        "sk",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ceb-sk.txt.zip",
    (
        "ceb",
        "sl",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ceb-sl.txt.zip",
    (
        "ceb",
        "sn",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ceb-sn.txt.zip",
    (
        "ceb",
        "so",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ceb-so.txt.zip",
    (
        "ceb",
        "sq",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ceb-sq.txt.zip",
    (
        "ceb",
        "sr",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ceb-sr.txt.zip",
    (
        "ceb",
        "ss",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ceb-ss.txt.zip",
    (
        "ceb",
        "sv",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ceb-sv.txt.zip",
    (
        "ceb",
        "syr",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ceb-syr.txt.zip",
    (
        "ceb",
        "te",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ceb-te.txt.zip",
    (
        "ceb",
        "th",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ceb-th.txt.zip",
    (
        "ceb",
        "tl",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ceb-tl.txt.zip",
    (
        "ceb",
        "tmh",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ceb-tmh.txt.zip",
    (
        "ceb",
        "tr",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ceb-tr.txt.zip",
    (
        "ceb",
        "uk",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ceb-uk.txt.zip",
    (
        "ceb",
        "usp",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ceb-usp.txt.zip",
    (
        "ceb",
        "vi",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ceb-vi.txt.zip",
    (
        "ceb",
        "wal",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ceb-wal.txt.zip",
    (
        "ceb",
        "wo",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ceb-wo.txt.zip",
    (
        "ceb",
        "xh",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ceb-xh.txt.zip",
    (
        "ceb",
        "zh",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ceb-zh.txt.zip",
    (
        "ceb",
        "zu",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ceb-zu.txt.zip",
    (
        "ch",
        "chq",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ch-chq.txt.zip",
    (
        "ch",
        "chr",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ch-chr.txt.zip",
    (
        "ch",
        "cjp",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ch-cjp.txt.zip",
    (
        "ch",
        "cni",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ch-cni.txt.zip",
    (
        "ch",
        "cop",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ch-cop.txt.zip",
    (
        "ch",
        "crp",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ch-crp.txt.zip",
    ("ch", "cs"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ch-cs.txt.zip",
    ("ch", "da"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ch-da.txt.zip",
    ("ch", "de"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ch-de.txt.zip",
    (
        "ch",
        "dik",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ch-dik.txt.zip",
    (
        "ch",
        "dje",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ch-dje.txt.zip",
    (
        "ch",
        "djk",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ch-djk.txt.zip",
    (
        "ch",
        "dop",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ch-dop.txt.zip",
    ("ch", "ee"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ch-ee.txt.zip",
    ("ch", "el"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ch-el.txt.zip",
    ("ch", "en"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ch-en.txt.zip",
    ("ch", "eo"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ch-eo.txt.zip",
    ("ch", "es"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ch-es.txt.zip",
    ("ch", "et"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ch-et.txt.zip",
    ("ch", "eu"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ch-eu.txt.zip",
    ("ch", "fi"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ch-fi.txt.zip",
    ("ch", "fr"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ch-fr.txt.zip",
    (
        "ch",
        "gbi",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ch-gbi.txt.zip",
    ("ch", "gd"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ch-gd.txt.zip",
    ("ch", "gu"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ch-gu.txt.zip",
    ("ch", "gv"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ch-gv.txt.zip",
    ("ch", "he"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ch-he.txt.zip",
    ("ch", "hi"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ch-hi.txt.zip",
    ("ch", "hr"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ch-hr.txt.zip",
    ("ch", "hu"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ch-hu.txt.zip",
    ("ch", "hy"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ch-hy.txt.zip",
    ("ch", "id"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ch-id.txt.zip",
    ("ch", "is"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ch-is.txt.zip",
    ("ch", "it"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ch-it.txt.zip",
    (
        "ch",
        "jak",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ch-jak.txt.zip",
    (
        "ch",
        "jap",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ch-jap.txt.zip",
    (
        "ch",
        "jiv",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ch-jiv.txt.zip",
    (
        "ch",
        "kab",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ch-kab.txt.zip",
    (
        "ch",
        "kbh",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ch-kbh.txt.zip",
    (
        "ch",
        "kek",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ch-kek.txt.zip",
    ("ch", "kn"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ch-kn.txt.zip",
    ("ch", "ko"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ch-ko.txt.zip",
    ("ch", "la"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ch-la.txt.zip",
    ("ch", "lt"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ch-lt.txt.zip",
    ("ch", "lv"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ch-lv.txt.zip",
    (
        "ch",
        "mam",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ch-mam.txt.zip",
    ("ch", "mi"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ch-mi.txt.zip",
    ("ch", "ml"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ch-ml.txt.zip",
    ("ch", "mr"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ch-mr.txt.zip",
    ("ch", "my"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ch-my.txt.zip",
    ("ch", "ne"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ch-ne.txt.zip",
    (
        "ch",
        "nhg",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ch-nhg.txt.zip",
    ("ch", "nl"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ch-nl.txt.zip",
    ("ch", "no"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ch-no.txt.zip",
    (
        "ch",
        "ojb",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ch-ojb.txt.zip",
    (
        "ch",
        "pck",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ch-pck.txt.zip",
    (
        "ch",
        "pes",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ch-pes.txt.zip",
    ("ch", "pl"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ch-pl.txt.zip",
    (
        "ch",
        "plt",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ch-plt.txt.zip",
    (
        "ch",
        "pot",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ch-pot.txt.zip",
    (
        "ch",
        "ppk",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ch-ppk.txt.zip",
    ("ch", "pt"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ch-pt.txt.zip",
    (
        "ch",
        "quc",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ch-quc.txt.zip",
    (
        "ch",
        "quw",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ch-quw.txt.zip",
    ("ch", "ro"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ch-ro.txt.zip",
    (
        "ch",
        "rom",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ch-rom.txt.zip",
    ("ch", "ru"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ch-ru.txt.zip",
    (
        "ch",
        "shi",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ch-shi.txt.zip",
    ("ch", "sk"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ch-sk.txt.zip",
    ("ch", "sl"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ch-sl.txt.zip",
    ("ch", "sn"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ch-sn.txt.zip",
    ("ch", "so"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ch-so.txt.zip",
    ("ch", "sq"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ch-sq.txt.zip",
    ("ch", "sr"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ch-sr.txt.zip",
    ("ch", "ss"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ch-ss.txt.zip",
    ("ch", "sv"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ch-sv.txt.zip",
    (
        "ch",
        "syr",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ch-syr.txt.zip",
    ("ch", "te"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ch-te.txt.zip",
    ("ch", "th"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ch-th.txt.zip",
    ("ch", "tl"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ch-tl.txt.zip",
    (
        "ch",
        "tmh",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ch-tmh.txt.zip",
    ("ch", "tr"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ch-tr.txt.zip",
    ("ch", "uk"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ch-uk.txt.zip",
    (
        "ch",
        "usp",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ch-usp.txt.zip",
    ("ch", "vi"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ch-vi.txt.zip",
    (
        "ch",
        "wal",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ch-wal.txt.zip",
    ("ch", "wo"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ch-wo.txt.zip",
    ("ch", "xh"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ch-xh.txt.zip",
    ("ch", "zh"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ch-zh.txt.zip",
    ("ch", "zu"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ch-zu.txt.zip",
    (
        "chq",
        "chr",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/chq-chr.txt.zip",
    (
        "chq",
        "cjp",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/chq-cjp.txt.zip",
    (
        "chq",
        "cni",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/chq-cni.txt.zip",
    (
        "chq",
        "cop",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/chq-cop.txt.zip",
    (
        "chq",
        "crp",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/chq-crp.txt.zip",
    (
        "chq",
        "cs",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/chq-cs.txt.zip",
    (
        "chq",
        "da",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/chq-da.txt.zip",
    (
        "chq",
        "de",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/chq-de.txt.zip",
    (
        "chq",
        "dik",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/chq-dik.txt.zip",
    (
        "chq",
        "dje",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/chq-dje.txt.zip",
    (
        "chq",
        "djk",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/chq-djk.txt.zip",
    (
        "chq",
        "dop",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/chq-dop.txt.zip",
    (
        "chq",
        "ee",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/chq-ee.txt.zip",
    (
        "chq",
        "el",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/chq-el.txt.zip",
    (
        "chq",
        "en",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/chq-en.txt.zip",
    (
        "chq",
        "eo",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/chq-eo.txt.zip",
    (
        "chq",
        "es",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/chq-es.txt.zip",
    (
        "chq",
        "et",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/chq-et.txt.zip",
    (
        "chq",
        "eu",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/chq-eu.txt.zip",
    (
        "chq",
        "fi",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/chq-fi.txt.zip",
    (
        "chq",
        "fr",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/chq-fr.txt.zip",
    (
        "chq",
        "gbi",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/chq-gbi.txt.zip",
    (
        "chq",
        "gd",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/chq-gd.txt.zip",
    (
        "chq",
        "gu",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/chq-gu.txt.zip",
    (
        "chq",
        "gv",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/chq-gv.txt.zip",
    (
        "chq",
        "he",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/chq-he.txt.zip",
    (
        "chq",
        "hi",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/chq-hi.txt.zip",
    (
        "chq",
        "hr",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/chq-hr.txt.zip",
    (
        "chq",
        "hu",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/chq-hu.txt.zip",
    (
        "chq",
        "hy",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/chq-hy.txt.zip",
    (
        "chq",
        "id",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/chq-id.txt.zip",
    (
        "chq",
        "is",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/chq-is.txt.zip",
    (
        "chq",
        "it",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/chq-it.txt.zip",
    (
        "chq",
        "jak",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/chq-jak.txt.zip",
    (
        "chq",
        "jap",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/chq-jap.txt.zip",
    (
        "chq",
        "jiv",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/chq-jiv.txt.zip",
    (
        "chq",
        "kab",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/chq-kab.txt.zip",
    (
        "chq",
        "kbh",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/chq-kbh.txt.zip",
    (
        "chq",
        "kek",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/chq-kek.txt.zip",
    (
        "chq",
        "kn",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/chq-kn.txt.zip",
    (
        "chq",
        "ko",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/chq-ko.txt.zip",
    (
        "chq",
        "la",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/chq-la.txt.zip",
    (
        "chq",
        "lt",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/chq-lt.txt.zip",
    (
        "chq",
        "lv",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/chq-lv.txt.zip",
    (
        "chq",
        "mam",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/chq-mam.txt.zip",
    (
        "chq",
        "mi",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/chq-mi.txt.zip",
    (
        "chq",
        "ml",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/chq-ml.txt.zip",
    (
        "chq",
        "mr",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/chq-mr.txt.zip",
    (
        "chq",
        "my",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/chq-my.txt.zip",
    (
        "chq",
        "ne",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/chq-ne.txt.zip",
    (
        "chq",
        "nhg",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/chq-nhg.txt.zip",
    (
        "chq",
        "nl",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/chq-nl.txt.zip",
    (
        "chq",
        "no",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/chq-no.txt.zip",
    (
        "chq",
        "ojb",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/chq-ojb.txt.zip",
    (
        "chq",
        "pck",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/chq-pck.txt.zip",
    (
        "chq",
        "pes",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/chq-pes.txt.zip",
    (
        "chq",
        "pl",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/chq-pl.txt.zip",
    (
        "chq",
        "plt",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/chq-plt.txt.zip",
    (
        "chq",
        "pot",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/chq-pot.txt.zip",
    (
        "chq",
        "ppk",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/chq-ppk.txt.zip",
    (
        "chq",
        "pt",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/chq-pt.txt.zip",
    (
        "chq",
        "quc",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/chq-quc.txt.zip",
    (
        "chq",
        "quw",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/chq-quw.txt.zip",
    (
        "chq",
        "ro",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/chq-ro.txt.zip",
    (
        "chq",
        "rom",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/chq-rom.txt.zip",
    (
        "chq",
        "ru",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/chq-ru.txt.zip",
    (
        "chq",
        "shi",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/chq-shi.txt.zip",
    (
        "chq",
        "sk",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/chq-sk.txt.zip",
    (
        "chq",
        "sl",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/chq-sl.txt.zip",
    (
        "chq",
        "sn",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/chq-sn.txt.zip",
    (
        "chq",
        "so",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/chq-so.txt.zip",
    (
        "chq",
        "sq",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/chq-sq.txt.zip",
    (
        "chq",
        "sr",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/chq-sr.txt.zip",
    (
        "chq",
        "ss",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/chq-ss.txt.zip",
    (
        "chq",
        "sv",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/chq-sv.txt.zip",
    (
        "chq",
        "syr",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/chq-syr.txt.zip",
    (
        "chq",
        "te",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/chq-te.txt.zip",
    (
        "chq",
        "th",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/chq-th.txt.zip",
    (
        "chq",
        "tl",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/chq-tl.txt.zip",
    (
        "chq",
        "tmh",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/chq-tmh.txt.zip",
    (
        "chq",
        "tr",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/chq-tr.txt.zip",
    (
        "chq",
        "uk",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/chq-uk.txt.zip",
    (
        "chq",
        "usp",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/chq-usp.txt.zip",
    (
        "chq",
        "vi",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/chq-vi.txt.zip",
    (
        "chq",
        "wal",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/chq-wal.txt.zip",
    (
        "chq",
        "wo",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/chq-wo.txt.zip",
    (
        "chq",
        "xh",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/chq-xh.txt.zip",
    (
        "chq",
        "zh",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/chq-zh.txt.zip",
    (
        "chq",
        "zu",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/chq-zu.txt.zip",
    (
        "chr",
        "cjp",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/chr-cjp.txt.zip",
    (
        "chr",
        "cni",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/chr-cni.txt.zip",
    (
        "chr",
        "cop",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/chr-cop.txt.zip",
    (
        "chr",
        "crp",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/chr-crp.txt.zip",
    (
        "chr",
        "cs",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/chr-cs.txt.zip",
    (
        "chr",
        "da",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/chr-da.txt.zip",
    (
        "chr",
        "de",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/chr-de.txt.zip",
    (
        "chr",
        "dik",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/chr-dik.txt.zip",
    (
        "chr",
        "dje",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/chr-dje.txt.zip",
    (
        "chr",
        "djk",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/chr-djk.txt.zip",
    (
        "chr",
        "dop",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/chr-dop.txt.zip",
    (
        "chr",
        "ee",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/chr-ee.txt.zip",
    (
        "chr",
        "el",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/chr-el.txt.zip",
    (
        "chr",
        "en",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/chr-en.txt.zip",
    (
        "chr",
        "eo",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/chr-eo.txt.zip",
    (
        "chr",
        "es",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/chr-es.txt.zip",
    (
        "chr",
        "et",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/chr-et.txt.zip",
    (
        "chr",
        "eu",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/chr-eu.txt.zip",
    (
        "chr",
        "fi",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/chr-fi.txt.zip",
    (
        "chr",
        "fr",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/chr-fr.txt.zip",
    (
        "chr",
        "gbi",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/chr-gbi.txt.zip",
    (
        "chr",
        "gd",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/chr-gd.txt.zip",
    (
        "chr",
        "gu",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/chr-gu.txt.zip",
    (
        "chr",
        "gv",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/chr-gv.txt.zip",
    (
        "chr",
        "he",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/chr-he.txt.zip",
    (
        "chr",
        "hi",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/chr-hi.txt.zip",
    (
        "chr",
        "hr",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/chr-hr.txt.zip",
    (
        "chr",
        "hu",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/chr-hu.txt.zip",
    (
        "chr",
        "hy",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/chr-hy.txt.zip",
    (
        "chr",
        "id",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/chr-id.txt.zip",
    (
        "chr",
        "is",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/chr-is.txt.zip",
    (
        "chr",
        "it",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/chr-it.txt.zip",
    (
        "chr",
        "jak",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/chr-jak.txt.zip",
    (
        "chr",
        "jap",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/chr-jap.txt.zip",
    (
        "chr",
        "jiv",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/chr-jiv.txt.zip",
    (
        "chr",
        "kab",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/chr-kab.txt.zip",
    (
        "chr",
        "kbh",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/chr-kbh.txt.zip",
    (
        "chr",
        "kek",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/chr-kek.txt.zip",
    (
        "chr",
        "kn",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/chr-kn.txt.zip",
    (
        "chr",
        "ko",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/chr-ko.txt.zip",
    (
        "chr",
        "la",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/chr-la.txt.zip",
    (
        "chr",
        "lt",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/chr-lt.txt.zip",
    (
        "chr",
        "lv",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/chr-lv.txt.zip",
    (
        "chr",
        "mam",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/chr-mam.txt.zip",
    (
        "chr",
        "mi",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/chr-mi.txt.zip",
    (
        "chr",
        "ml",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/chr-ml.txt.zip",
    (
        "chr",
        "mr",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/chr-mr.txt.zip",
    (
        "chr",
        "my",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/chr-my.txt.zip",
    (
        "chr",
        "ne",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/chr-ne.txt.zip",
    (
        "chr",
        "nhg",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/chr-nhg.txt.zip",
    (
        "chr",
        "nl",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/chr-nl.txt.zip",
    (
        "chr",
        "no",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/chr-no.txt.zip",
    (
        "chr",
        "ojb",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/chr-ojb.txt.zip",
    (
        "chr",
        "pck",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/chr-pck.txt.zip",
    (
        "chr",
        "pes",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/chr-pes.txt.zip",
    (
        "chr",
        "pl",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/chr-pl.txt.zip",
    (
        "chr",
        "plt",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/chr-plt.txt.zip",
    (
        "chr",
        "pot",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/chr-pot.txt.zip",
    (
        "chr",
        "ppk",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/chr-ppk.txt.zip",
    (
        "chr",
        "pt",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/chr-pt.txt.zip",
    (
        "chr",
        "quc",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/chr-quc.txt.zip",
    (
        "chr",
        "quw",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/chr-quw.txt.zip",
    (
        "chr",
        "ro",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/chr-ro.txt.zip",
    (
        "chr",
        "rom",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/chr-rom.txt.zip",
    (
        "chr",
        "ru",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/chr-ru.txt.zip",
    (
        "chr",
        "shi",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/chr-shi.txt.zip",
    (
        "chr",
        "sk",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/chr-sk.txt.zip",
    (
        "chr",
        "sl",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/chr-sl.txt.zip",
    (
        "chr",
        "sn",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/chr-sn.txt.zip",
    (
        "chr",
        "so",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/chr-so.txt.zip",
    (
        "chr",
        "sq",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/chr-sq.txt.zip",
    (
        "chr",
        "sr",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/chr-sr.txt.zip",
    (
        "chr",
        "ss",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/chr-ss.txt.zip",
    (
        "chr",
        "sv",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/chr-sv.txt.zip",
    (
        "chr",
        "syr",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/chr-syr.txt.zip",
    (
        "chr",
        "te",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/chr-te.txt.zip",
    (
        "chr",
        "th",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/chr-th.txt.zip",
    (
        "chr",
        "tl",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/chr-tl.txt.zip",
    (
        "chr",
        "tmh",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/chr-tmh.txt.zip",
    (
        "chr",
        "tr",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/chr-tr.txt.zip",
    (
        "chr",
        "uk",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/chr-uk.txt.zip",
    (
        "chr",
        "usp",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/chr-usp.txt.zip",
    (
        "chr",
        "vi",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/chr-vi.txt.zip",
    (
        "chr",
        "wal",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/chr-wal.txt.zip",
    (
        "chr",
        "wo",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/chr-wo.txt.zip",
    (
        "chr",
        "xh",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/chr-xh.txt.zip",
    (
        "chr",
        "zh",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/chr-zh.txt.zip",
    (
        "chr",
        "zu",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/chr-zu.txt.zip",
    (
        "cjp",
        "cni",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cjp-cni.txt.zip",
    (
        "cjp",
        "cop",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cjp-cop.txt.zip",
    (
        "cjp",
        "crp",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cjp-crp.txt.zip",
    (
        "cjp",
        "cs",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cjp-cs.txt.zip",
    (
        "cjp",
        "da",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cjp-da.txt.zip",
    (
        "cjp",
        "de",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cjp-de.txt.zip",
    (
        "cjp",
        "dik",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cjp-dik.txt.zip",
    (
        "cjp",
        "dje",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cjp-dje.txt.zip",
    (
        "cjp",
        "djk",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cjp-djk.txt.zip",
    (
        "cjp",
        "dop",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cjp-dop.txt.zip",
    (
        "cjp",
        "ee",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cjp-ee.txt.zip",
    (
        "cjp",
        "el",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cjp-el.txt.zip",
    (
        "cjp",
        "en",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cjp-en.txt.zip",
    (
        "cjp",
        "eo",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cjp-eo.txt.zip",
    (
        "cjp",
        "es",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cjp-es.txt.zip",
    (
        "cjp",
        "et",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cjp-et.txt.zip",
    (
        "cjp",
        "eu",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cjp-eu.txt.zip",
    (
        "cjp",
        "fi",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cjp-fi.txt.zip",
    (
        "cjp",
        "fr",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cjp-fr.txt.zip",
    (
        "cjp",
        "gbi",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cjp-gbi.txt.zip",
    (
        "cjp",
        "gd",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cjp-gd.txt.zip",
    (
        "cjp",
        "gu",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cjp-gu.txt.zip",
    (
        "cjp",
        "gv",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cjp-gv.txt.zip",
    (
        "cjp",
        "he",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cjp-he.txt.zip",
    (
        "cjp",
        "hi",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cjp-hi.txt.zip",
    (
        "cjp",
        "hr",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cjp-hr.txt.zip",
    (
        "cjp",
        "hu",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cjp-hu.txt.zip",
    (
        "cjp",
        "hy",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cjp-hy.txt.zip",
    (
        "cjp",
        "id",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cjp-id.txt.zip",
    (
        "cjp",
        "is",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cjp-is.txt.zip",
    (
        "cjp",
        "it",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cjp-it.txt.zip",
    (
        "cjp",
        "jak",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cjp-jak.txt.zip",
    (
        "cjp",
        "jap",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cjp-jap.txt.zip",
    (
        "cjp",
        "jiv",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cjp-jiv.txt.zip",
    (
        "cjp",
        "kab",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cjp-kab.txt.zip",
    (
        "cjp",
        "kbh",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cjp-kbh.txt.zip",
    (
        "cjp",
        "kek",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cjp-kek.txt.zip",
    (
        "cjp",
        "kn",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cjp-kn.txt.zip",
    (
        "cjp",
        "ko",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cjp-ko.txt.zip",
    (
        "cjp",
        "la",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cjp-la.txt.zip",
    (
        "cjp",
        "lt",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cjp-lt.txt.zip",
    (
        "cjp",
        "lv",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cjp-lv.txt.zip",
    (
        "cjp",
        "mam",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cjp-mam.txt.zip",
    (
        "cjp",
        "mi",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cjp-mi.txt.zip",
    (
        "cjp",
        "ml",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cjp-ml.txt.zip",
    (
        "cjp",
        "mr",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cjp-mr.txt.zip",
    (
        "cjp",
        "my",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cjp-my.txt.zip",
    (
        "cjp",
        "ne",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cjp-ne.txt.zip",
    (
        "cjp",
        "nhg",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cjp-nhg.txt.zip",
    (
        "cjp",
        "nl",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cjp-nl.txt.zip",
    (
        "cjp",
        "no",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cjp-no.txt.zip",
    (
        "cjp",
        "ojb",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cjp-ojb.txt.zip",
    (
        "cjp",
        "pck",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cjp-pck.txt.zip",
    (
        "cjp",
        "pes",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cjp-pes.txt.zip",
    (
        "cjp",
        "pl",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cjp-pl.txt.zip",
    (
        "cjp",
        "plt",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cjp-plt.txt.zip",
    (
        "cjp",
        "pot",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cjp-pot.txt.zip",
    (
        "cjp",
        "ppk",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cjp-ppk.txt.zip",
    (
        "cjp",
        "pt",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cjp-pt.txt.zip",
    (
        "cjp",
        "quc",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cjp-quc.txt.zip",
    (
        "cjp",
        "quw",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cjp-quw.txt.zip",
    (
        "cjp",
        "ro",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cjp-ro.txt.zip",
    (
        "cjp",
        "rom",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cjp-rom.txt.zip",
    (
        "cjp",
        "ru",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cjp-ru.txt.zip",
    (
        "cjp",
        "shi",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cjp-shi.txt.zip",
    (
        "cjp",
        "sk",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cjp-sk.txt.zip",
    (
        "cjp",
        "sl",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cjp-sl.txt.zip",
    (
        "cjp",
        "sn",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cjp-sn.txt.zip",
    (
        "cjp",
        "so",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cjp-so.txt.zip",
    (
        "cjp",
        "sq",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cjp-sq.txt.zip",
    (
        "cjp",
        "sr",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cjp-sr.txt.zip",
    (
        "cjp",
        "ss",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cjp-ss.txt.zip",
    (
        "cjp",
        "sv",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cjp-sv.txt.zip",
    (
        "cjp",
        "syr",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cjp-syr.txt.zip",
    (
        "cjp",
        "te",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cjp-te.txt.zip",
    (
        "cjp",
        "th",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cjp-th.txt.zip",
    (
        "cjp",
        "tl",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cjp-tl.txt.zip",
    (
        "cjp",
        "tmh",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cjp-tmh.txt.zip",
    (
        "cjp",
        "tr",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cjp-tr.txt.zip",
    (
        "cjp",
        "uk",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cjp-uk.txt.zip",
    (
        "cjp",
        "usp",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cjp-usp.txt.zip",
    (
        "cjp",
        "vi",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cjp-vi.txt.zip",
    (
        "cjp",
        "wal",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cjp-wal.txt.zip",
    (
        "cjp",
        "wo",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cjp-wo.txt.zip",
    (
        "cjp",
        "xh",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cjp-xh.txt.zip",
    (
        "cjp",
        "zh",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cjp-zh.txt.zip",
    (
        "cjp",
        "zu",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cjp-zu.txt.zip",
    (
        "cni",
        "cop",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cni-cop.txt.zip",
    (
        "cni",
        "crp",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cni-crp.txt.zip",
    (
        "cni",
        "cs",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cni-cs.txt.zip",
    (
        "cni",
        "da",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cni-da.txt.zip",
    (
        "cni",
        "de",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cni-de.txt.zip",
    (
        "cni",
        "dik",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cni-dik.txt.zip",
    (
        "cni",
        "dje",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cni-dje.txt.zip",
    (
        "cni",
        "djk",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cni-djk.txt.zip",
    (
        "cni",
        "dop",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cni-dop.txt.zip",
    (
        "cni",
        "ee",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cni-ee.txt.zip",
    (
        "cni",
        "el",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cni-el.txt.zip",
    (
        "cni",
        "en",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cni-en.txt.zip",
    (
        "cni",
        "eo",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cni-eo.txt.zip",
    (
        "cni",
        "es",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cni-es.txt.zip",
    (
        "cni",
        "et",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cni-et.txt.zip",
    (
        "cni",
        "eu",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cni-eu.txt.zip",
    (
        "cni",
        "fi",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cni-fi.txt.zip",
    (
        "cni",
        "fr",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cni-fr.txt.zip",
    (
        "cni",
        "gbi",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cni-gbi.txt.zip",
    (
        "cni",
        "gd",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cni-gd.txt.zip",
    (
        "cni",
        "gu",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cni-gu.txt.zip",
    (
        "cni",
        "gv",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cni-gv.txt.zip",
    (
        "cni",
        "he",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cni-he.txt.zip",
    (
        "cni",
        "hi",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cni-hi.txt.zip",
    (
        "cni",
        "hr",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cni-hr.txt.zip",
    (
        "cni",
        "hu",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cni-hu.txt.zip",
    (
        "cni",
        "hy",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cni-hy.txt.zip",
    (
        "cni",
        "id",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cni-id.txt.zip",
    (
        "cni",
        "is",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cni-is.txt.zip",
    (
        "cni",
        "it",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cni-it.txt.zip",
    (
        "cni",
        "jak",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cni-jak.txt.zip",
    (
        "cni",
        "jap",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cni-jap.txt.zip",
    (
        "cni",
        "jiv",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cni-jiv.txt.zip",
    (
        "cni",
        "kab",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cni-kab.txt.zip",
    (
        "cni",
        "kbh",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cni-kbh.txt.zip",
    (
        "cni",
        "kek",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cni-kek.txt.zip",
    (
        "cni",
        "kn",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cni-kn.txt.zip",
    (
        "cni",
        "ko",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cni-ko.txt.zip",
    (
        "cni",
        "la",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cni-la.txt.zip",
    (
        "cni",
        "lt",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cni-lt.txt.zip",
    (
        "cni",
        "lv",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cni-lv.txt.zip",
    (
        "cni",
        "mam",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cni-mam.txt.zip",
    (
        "cni",
        "mi",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cni-mi.txt.zip",
    (
        "cni",
        "ml",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cni-ml.txt.zip",
    (
        "cni",
        "mr",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cni-mr.txt.zip",
    (
        "cni",
        "my",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cni-my.txt.zip",
    (
        "cni",
        "ne",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cni-ne.txt.zip",
    (
        "cni",
        "nhg",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cni-nhg.txt.zip",
    (
        "cni",
        "nl",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cni-nl.txt.zip",
    (
        "cni",
        "no",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cni-no.txt.zip",
    (
        "cni",
        "ojb",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cni-ojb.txt.zip",
    (
        "cni",
        "pck",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cni-pck.txt.zip",
    (
        "cni",
        "pes",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cni-pes.txt.zip",
    (
        "cni",
        "pl",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cni-pl.txt.zip",
    (
        "cni",
        "plt",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cni-plt.txt.zip",
    (
        "cni",
        "pot",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cni-pot.txt.zip",
    (
        "cni",
        "ppk",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cni-ppk.txt.zip",
    (
        "cni",
        "pt",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cni-pt.txt.zip",
    (
        "cni",
        "quc",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cni-quc.txt.zip",
    (
        "cni",
        "quw",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cni-quw.txt.zip",
    (
        "cni",
        "ro",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cni-ro.txt.zip",
    (
        "cni",
        "rom",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cni-rom.txt.zip",
    (
        "cni",
        "ru",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cni-ru.txt.zip",
    (
        "cni",
        "shi",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cni-shi.txt.zip",
    (
        "cni",
        "sk",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cni-sk.txt.zip",
    (
        "cni",
        "sl",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cni-sl.txt.zip",
    (
        "cni",
        "sn",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cni-sn.txt.zip",
    (
        "cni",
        "so",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cni-so.txt.zip",
    (
        "cni",
        "sq",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cni-sq.txt.zip",
    (
        "cni",
        "sr",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cni-sr.txt.zip",
    (
        "cni",
        "ss",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cni-ss.txt.zip",
    (
        "cni",
        "sv",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cni-sv.txt.zip",
    (
        "cni",
        "syr",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cni-syr.txt.zip",
    (
        "cni",
        "te",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cni-te.txt.zip",
    (
        "cni",
        "th",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cni-th.txt.zip",
    (
        "cni",
        "tl",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cni-tl.txt.zip",
    (
        "cni",
        "tmh",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cni-tmh.txt.zip",
    (
        "cni",
        "tr",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cni-tr.txt.zip",
    (
        "cni",
        "uk",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cni-uk.txt.zip",
    (
        "cni",
        "usp",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cni-usp.txt.zip",
    (
        "cni",
        "vi",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cni-vi.txt.zip",
    (
        "cni",
        "wal",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cni-wal.txt.zip",
    (
        "cni",
        "wo",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cni-wo.txt.zip",
    (
        "cni",
        "xh",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cni-xh.txt.zip",
    (
        "cni",
        "zh",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cni-zh.txt.zip",
    (
        "cni",
        "zu",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cni-zu.txt.zip",
    (
        "cop",
        "crp",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cop-crp.txt.zip",
    (
        "cop",
        "cs",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cop-cs.txt.zip",
    (
        "cop",
        "da",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cop-da.txt.zip",
    (
        "cop",
        "de",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cop-de.txt.zip",
    (
        "cop",
        "dik",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cop-dik.txt.zip",
    (
        "cop",
        "dje",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cop-dje.txt.zip",
    (
        "cop",
        "djk",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cop-djk.txt.zip",
    (
        "cop",
        "dop",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cop-dop.txt.zip",
    (
        "cop",
        "ee",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cop-ee.txt.zip",
    (
        "cop",
        "el",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cop-el.txt.zip",
    (
        "cop",
        "en",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cop-en.txt.zip",
    (
        "cop",
        "eo",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cop-eo.txt.zip",
    (
        "cop",
        "es",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cop-es.txt.zip",
    (
        "cop",
        "et",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cop-et.txt.zip",
    (
        "cop",
        "eu",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cop-eu.txt.zip",
    (
        "cop",
        "fi",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cop-fi.txt.zip",
    (
        "cop",
        "fr",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cop-fr.txt.zip",
    (
        "cop",
        "gbi",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cop-gbi.txt.zip",
    (
        "cop",
        "gd",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cop-gd.txt.zip",
    (
        "cop",
        "gu",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cop-gu.txt.zip",
    (
        "cop",
        "gv",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cop-gv.txt.zip",
    (
        "cop",
        "he",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cop-he.txt.zip",
    (
        "cop",
        "hi",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cop-hi.txt.zip",
    (
        "cop",
        "hr",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cop-hr.txt.zip",
    (
        "cop",
        "hu",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cop-hu.txt.zip",
    (
        "cop",
        "hy",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cop-hy.txt.zip",
    (
        "cop",
        "id",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cop-id.txt.zip",
    (
        "cop",
        "is",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cop-is.txt.zip",
    (
        "cop",
        "it",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cop-it.txt.zip",
    (
        "cop",
        "jak",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cop-jak.txt.zip",
    (
        "cop",
        "jap",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cop-jap.txt.zip",
    (
        "cop",
        "jiv",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cop-jiv.txt.zip",
    (
        "cop",
        "kab",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cop-kab.txt.zip",
    (
        "cop",
        "kbh",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cop-kbh.txt.zip",
    (
        "cop",
        "kek",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cop-kek.txt.zip",
    (
        "cop",
        "kn",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cop-kn.txt.zip",
    (
        "cop",
        "ko",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cop-ko.txt.zip",
    (
        "cop",
        "la",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cop-la.txt.zip",
    (
        "cop",
        "lt",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cop-lt.txt.zip",
    (
        "cop",
        "lv",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cop-lv.txt.zip",
    (
        "cop",
        "mam",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cop-mam.txt.zip",
    (
        "cop",
        "mi",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cop-mi.txt.zip",
    (
        "cop",
        "ml",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cop-ml.txt.zip",
    (
        "cop",
        "mr",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cop-mr.txt.zip",
    (
        "cop",
        "my",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cop-my.txt.zip",
    (
        "cop",
        "ne",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cop-ne.txt.zip",
    (
        "cop",
        "nhg",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cop-nhg.txt.zip",
    (
        "cop",
        "nl",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cop-nl.txt.zip",
    (
        "cop",
        "no",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cop-no.txt.zip",
    (
        "cop",
        "ojb",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cop-ojb.txt.zip",
    (
        "cop",
        "pck",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cop-pck.txt.zip",
    (
        "cop",
        "pes",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cop-pes.txt.zip",
    (
        "cop",
        "pl",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cop-pl.txt.zip",
    (
        "cop",
        "plt",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cop-plt.txt.zip",
    (
        "cop",
        "pot",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cop-pot.txt.zip",
    (
        "cop",
        "ppk",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cop-ppk.txt.zip",
    (
        "cop",
        "pt",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cop-pt.txt.zip",
    (
        "cop",
        "quc",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cop-quc.txt.zip",
    (
        "cop",
        "quw",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cop-quw.txt.zip",
    (
        "cop",
        "ro",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cop-ro.txt.zip",
    (
        "cop",
        "rom",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cop-rom.txt.zip",
    (
        "cop",
        "ru",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cop-ru.txt.zip",
    (
        "cop",
        "shi",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cop-shi.txt.zip",
    (
        "cop",
        "sk",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cop-sk.txt.zip",
    (
        "cop",
        "sl",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cop-sl.txt.zip",
    (
        "cop",
        "sn",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cop-sn.txt.zip",
    (
        "cop",
        "so",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cop-so.txt.zip",
    (
        "cop",
        "sq",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cop-sq.txt.zip",
    (
        "cop",
        "sr",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cop-sr.txt.zip",
    (
        "cop",
        "ss",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cop-ss.txt.zip",
    (
        "cop",
        "sv",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cop-sv.txt.zip",
    (
        "cop",
        "syr",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cop-syr.txt.zip",
    (
        "cop",
        "te",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cop-te.txt.zip",
    (
        "cop",
        "th",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cop-th.txt.zip",
    (
        "cop",
        "tl",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cop-tl.txt.zip",
    (
        "cop",
        "tmh",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cop-tmh.txt.zip",
    (
        "cop",
        "tr",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cop-tr.txt.zip",
    (
        "cop",
        "uk",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cop-uk.txt.zip",
    (
        "cop",
        "usp",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cop-usp.txt.zip",
    (
        "cop",
        "vi",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cop-vi.txt.zip",
    (
        "cop",
        "wal",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cop-wal.txt.zip",
    (
        "cop",
        "wo",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cop-wo.txt.zip",
    (
        "cop",
        "xh",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cop-xh.txt.zip",
    (
        "cop",
        "zh",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cop-zh.txt.zip",
    (
        "cop",
        "zu",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cop-zu.txt.zip",
    (
        "crp",
        "cs",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/crp-cs.txt.zip",
    (
        "crp",
        "da",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/crp-da.txt.zip",
    (
        "crp",
        "de",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/crp-de.txt.zip",
    (
        "crp",
        "dik",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/crp-dik.txt.zip",
    (
        "crp",
        "dje",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/crp-dje.txt.zip",
    (
        "crp",
        "djk",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/crp-djk.txt.zip",
    (
        "crp",
        "dop",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/crp-dop.txt.zip",
    (
        "crp",
        "ee",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/crp-ee.txt.zip",
    (
        "crp",
        "el",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/crp-el.txt.zip",
    (
        "crp",
        "en",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/crp-en.txt.zip",
    (
        "crp",
        "eo",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/crp-eo.txt.zip",
    (
        "crp",
        "es",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/crp-es.txt.zip",
    (
        "crp",
        "et",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/crp-et.txt.zip",
    (
        "crp",
        "eu",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/crp-eu.txt.zip",
    (
        "crp",
        "fi",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/crp-fi.txt.zip",
    (
        "crp",
        "fr",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/crp-fr.txt.zip",
    (
        "crp",
        "gbi",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/crp-gbi.txt.zip",
    (
        "crp",
        "gd",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/crp-gd.txt.zip",
    (
        "crp",
        "gu",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/crp-gu.txt.zip",
    (
        "crp",
        "gv",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/crp-gv.txt.zip",
    (
        "crp",
        "he",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/crp-he.txt.zip",
    (
        "crp",
        "hi",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/crp-hi.txt.zip",
    (
        "crp",
        "hr",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/crp-hr.txt.zip",
    (
        "crp",
        "hu",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/crp-hu.txt.zip",
    (
        "crp",
        "hy",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/crp-hy.txt.zip",
    (
        "crp",
        "id",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/crp-id.txt.zip",
    (
        "crp",
        "is",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/crp-is.txt.zip",
    (
        "crp",
        "it",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/crp-it.txt.zip",
    (
        "crp",
        "jak",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/crp-jak.txt.zip",
    (
        "crp",
        "jap",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/crp-jap.txt.zip",
    (
        "crp",
        "jiv",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/crp-jiv.txt.zip",
    (
        "crp",
        "kab",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/crp-kab.txt.zip",
    (
        "crp",
        "kbh",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/crp-kbh.txt.zip",
    (
        "crp",
        "kek",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/crp-kek.txt.zip",
    (
        "crp",
        "kn",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/crp-kn.txt.zip",
    (
        "crp",
        "ko",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/crp-ko.txt.zip",
    (
        "crp",
        "la",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/crp-la.txt.zip",
    (
        "crp",
        "lt",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/crp-lt.txt.zip",
    (
        "crp",
        "lv",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/crp-lv.txt.zip",
    (
        "crp",
        "mam",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/crp-mam.txt.zip",
    (
        "crp",
        "mi",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/crp-mi.txt.zip",
    (
        "crp",
        "ml",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/crp-ml.txt.zip",
    (
        "crp",
        "mr",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/crp-mr.txt.zip",
    (
        "crp",
        "my",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/crp-my.txt.zip",
    (
        "crp",
        "ne",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/crp-ne.txt.zip",
    (
        "crp",
        "nhg",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/crp-nhg.txt.zip",
    (
        "crp",
        "nl",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/crp-nl.txt.zip",
    (
        "crp",
        "no",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/crp-no.txt.zip",
    (
        "crp",
        "ojb",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/crp-ojb.txt.zip",
    (
        "crp",
        "pck",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/crp-pck.txt.zip",
    (
        "crp",
        "pes",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/crp-pes.txt.zip",
    (
        "crp",
        "pl",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/crp-pl.txt.zip",
    (
        "crp",
        "plt",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/crp-plt.txt.zip",
    (
        "crp",
        "pot",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/crp-pot.txt.zip",
    (
        "crp",
        "ppk",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/crp-ppk.txt.zip",
    (
        "crp",
        "pt",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/crp-pt.txt.zip",
    (
        "crp",
        "quc",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/crp-quc.txt.zip",
    (
        "crp",
        "quw",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/crp-quw.txt.zip",
    (
        "crp",
        "ro",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/crp-ro.txt.zip",
    (
        "crp",
        "rom",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/crp-rom.txt.zip",
    (
        "crp",
        "ru",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/crp-ru.txt.zip",
    (
        "crp",
        "shi",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/crp-shi.txt.zip",
    (
        "crp",
        "sk",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/crp-sk.txt.zip",
    (
        "crp",
        "sl",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/crp-sl.txt.zip",
    (
        "crp",
        "sn",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/crp-sn.txt.zip",
    (
        "crp",
        "so",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/crp-so.txt.zip",
    (
        "crp",
        "sq",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/crp-sq.txt.zip",
    (
        "crp",
        "sr",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/crp-sr.txt.zip",
    (
        "crp",
        "ss",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/crp-ss.txt.zip",
    (
        "crp",
        "sv",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/crp-sv.txt.zip",
    (
        "crp",
        "syr",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/crp-syr.txt.zip",
    (
        "crp",
        "te",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/crp-te.txt.zip",
    (
        "crp",
        "th",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/crp-th.txt.zip",
    (
        "crp",
        "tl",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/crp-tl.txt.zip",
    (
        "crp",
        "tmh",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/crp-tmh.txt.zip",
    (
        "crp",
        "tr",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/crp-tr.txt.zip",
    (
        "crp",
        "uk",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/crp-uk.txt.zip",
    (
        "crp",
        "usp",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/crp-usp.txt.zip",
    (
        "crp",
        "vi",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/crp-vi.txt.zip",
    (
        "crp",
        "wal",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/crp-wal.txt.zip",
    (
        "crp",
        "wo",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/crp-wo.txt.zip",
    (
        "crp",
        "xh",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/crp-xh.txt.zip",
    (
        "crp",
        "zh",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/crp-zh.txt.zip",
    (
        "crp",
        "zu",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/crp-zu.txt.zip",
    ("cs", "da"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cs-da.txt.zip",
    ("cs", "de"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cs-de.txt.zip",
    (
        "cs",
        "dik",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cs-dik.txt.zip",
    (
        "cs",
        "dje",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cs-dje.txt.zip",
    (
        "cs",
        "djk",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cs-djk.txt.zip",
    (
        "cs",
        "dop",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cs-dop.txt.zip",
    ("cs", "ee"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cs-ee.txt.zip",
    ("cs", "el"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cs-el.txt.zip",
    ("cs", "en"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cs-en.txt.zip",
    ("cs", "eo"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cs-eo.txt.zip",
    ("cs", "es"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cs-es.txt.zip",
    ("cs", "et"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cs-et.txt.zip",
    ("cs", "eu"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cs-eu.txt.zip",
    ("cs", "fi"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cs-fi.txt.zip",
    ("cs", "fr"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cs-fr.txt.zip",
    (
        "cs",
        "gbi",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cs-gbi.txt.zip",
    ("cs", "gd"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cs-gd.txt.zip",
    ("cs", "gu"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cs-gu.txt.zip",
    ("cs", "gv"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cs-gv.txt.zip",
    ("cs", "he"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cs-he.txt.zip",
    ("cs", "hi"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cs-hi.txt.zip",
    ("cs", "hr"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cs-hr.txt.zip",
    ("cs", "hu"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cs-hu.txt.zip",
    ("cs", "hy"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cs-hy.txt.zip",
    ("cs", "id"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cs-id.txt.zip",
    ("cs", "is"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cs-is.txt.zip",
    ("cs", "it"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cs-it.txt.zip",
    (
        "cs",
        "jak",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cs-jak.txt.zip",
    (
        "cs",
        "jap",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cs-jap.txt.zip",
    (
        "cs",
        "jiv",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cs-jiv.txt.zip",
    (
        "cs",
        "kab",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cs-kab.txt.zip",
    (
        "cs",
        "kbh",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cs-kbh.txt.zip",
    (
        "cs",
        "kek",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cs-kek.txt.zip",
    ("cs", "kn"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cs-kn.txt.zip",
    ("cs", "ko"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cs-ko.txt.zip",
    ("cs", "la"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cs-la.txt.zip",
    ("cs", "lt"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cs-lt.txt.zip",
    ("cs", "lv"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cs-lv.txt.zip",
    (
        "cs",
        "mam",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cs-mam.txt.zip",
    ("cs", "mi"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cs-mi.txt.zip",
    ("cs", "ml"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cs-ml.txt.zip",
    ("cs", "mr"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cs-mr.txt.zip",
    ("cs", "my"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cs-my.txt.zip",
    ("cs", "ne"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cs-ne.txt.zip",
    (
        "cs",
        "nhg",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cs-nhg.txt.zip",
    ("cs", "nl"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cs-nl.txt.zip",
    ("cs", "no"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cs-no.txt.zip",
    (
        "cs",
        "ojb",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cs-ojb.txt.zip",
    (
        "cs",
        "pck",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cs-pck.txt.zip",
    (
        "cs",
        "pes",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cs-pes.txt.zip",
    ("cs", "pl"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cs-pl.txt.zip",
    (
        "cs",
        "plt",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cs-plt.txt.zip",
    (
        "cs",
        "pot",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cs-pot.txt.zip",
    (
        "cs",
        "ppk",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cs-ppk.txt.zip",
    ("cs", "pt"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cs-pt.txt.zip",
    (
        "cs",
        "quc",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cs-quc.txt.zip",
    (
        "cs",
        "quw",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cs-quw.txt.zip",
    ("cs", "ro"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cs-ro.txt.zip",
    (
        "cs",
        "rom",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cs-rom.txt.zip",
    ("cs", "ru"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cs-ru.txt.zip",
    (
        "cs",
        "shi",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cs-shi.txt.zip",
    ("cs", "sk"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cs-sk.txt.zip",
    ("cs", "sl"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cs-sl.txt.zip",
    ("cs", "sn"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cs-sn.txt.zip",
    ("cs", "so"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cs-so.txt.zip",
    ("cs", "sq"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cs-sq.txt.zip",
    ("cs", "sr"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cs-sr.txt.zip",
    ("cs", "ss"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cs-ss.txt.zip",
    ("cs", "sv"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cs-sv.txt.zip",
    (
        "cs",
        "syr",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cs-syr.txt.zip",
    ("cs", "te"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cs-te.txt.zip",
    ("cs", "th"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cs-th.txt.zip",
    ("cs", "tl"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cs-tl.txt.zip",
    (
        "cs",
        "tmh",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cs-tmh.txt.zip",
    ("cs", "tr"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cs-tr.txt.zip",
    ("cs", "uk"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cs-uk.txt.zip",
    (
        "cs",
        "usp",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cs-usp.txt.zip",
    ("cs", "vi"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cs-vi.txt.zip",
    (
        "cs",
        "wal",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cs-wal.txt.zip",
    ("cs", "wo"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cs-wo.txt.zip",
    ("cs", "xh"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cs-xh.txt.zip",
    ("cs", "zh"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cs-zh.txt.zip",
    ("cs", "zu"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/cs-zu.txt.zip",
    ("da", "de"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/da-de.txt.zip",
    (
        "da",
        "dik",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/da-dik.txt.zip",
    (
        "da",
        "dje",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/da-dje.txt.zip",
    (
        "da",
        "djk",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/da-djk.txt.zip",
    (
        "da",
        "dop",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/da-dop.txt.zip",
    ("da", "ee"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/da-ee.txt.zip",
    ("da", "el"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/da-el.txt.zip",
    ("da", "en"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/da-en.txt.zip",
    ("da", "eo"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/da-eo.txt.zip",
    ("da", "es"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/da-es.txt.zip",
    ("da", "et"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/da-et.txt.zip",
    ("da", "eu"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/da-eu.txt.zip",
    ("da", "fi"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/da-fi.txt.zip",
    ("da", "fr"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/da-fr.txt.zip",
    (
        "da",
        "gbi",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/da-gbi.txt.zip",
    ("da", "gd"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/da-gd.txt.zip",
    ("da", "gu"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/da-gu.txt.zip",
    ("da", "gv"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/da-gv.txt.zip",
    ("da", "he"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/da-he.txt.zip",
    ("da", "hi"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/da-hi.txt.zip",
    ("da", "hr"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/da-hr.txt.zip",
    ("da", "hu"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/da-hu.txt.zip",
    ("da", "hy"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/da-hy.txt.zip",
    ("da", "id"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/da-id.txt.zip",
    ("da", "is"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/da-is.txt.zip",
    ("da", "it"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/da-it.txt.zip",
    (
        "da",
        "jak",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/da-jak.txt.zip",
    (
        "da",
        "jap",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/da-jap.txt.zip",
    (
        "da",
        "jiv",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/da-jiv.txt.zip",
    (
        "da",
        "kab",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/da-kab.txt.zip",
    (
        "da",
        "kbh",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/da-kbh.txt.zip",
    (
        "da",
        "kek",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/da-kek.txt.zip",
    ("da", "kn"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/da-kn.txt.zip",
    ("da", "ko"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/da-ko.txt.zip",
    ("da", "la"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/da-la.txt.zip",
    ("da", "lt"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/da-lt.txt.zip",
    ("da", "lv"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/da-lv.txt.zip",
    (
        "da",
        "mam",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/da-mam.txt.zip",
    ("da", "mi"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/da-mi.txt.zip",
    ("da", "ml"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/da-ml.txt.zip",
    ("da", "mr"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/da-mr.txt.zip",
    ("da", "my"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/da-my.txt.zip",
    ("da", "ne"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/da-ne.txt.zip",
    (
        "da",
        "nhg",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/da-nhg.txt.zip",
    ("da", "nl"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/da-nl.txt.zip",
    ("da", "no"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/da-no.txt.zip",
    (
        "da",
        "ojb",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/da-ojb.txt.zip",
    (
        "da",
        "pck",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/da-pck.txt.zip",
    (
        "da",
        "pes",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/da-pes.txt.zip",
    ("da", "pl"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/da-pl.txt.zip",
    (
        "da",
        "plt",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/da-plt.txt.zip",
    (
        "da",
        "pot",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/da-pot.txt.zip",
    (
        "da",
        "ppk",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/da-ppk.txt.zip",
    ("da", "pt"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/da-pt.txt.zip",
    (
        "da",
        "quc",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/da-quc.txt.zip",
    (
        "da",
        "quw",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/da-quw.txt.zip",
    ("da", "ro"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/da-ro.txt.zip",
    (
        "da",
        "rom",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/da-rom.txt.zip",
    ("da", "ru"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/da-ru.txt.zip",
    (
        "da",
        "shi",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/da-shi.txt.zip",
    ("da", "sk"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/da-sk.txt.zip",
    ("da", "sl"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/da-sl.txt.zip",
    ("da", "sn"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/da-sn.txt.zip",
    ("da", "so"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/da-so.txt.zip",
    ("da", "sq"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/da-sq.txt.zip",
    ("da", "sr"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/da-sr.txt.zip",
    ("da", "ss"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/da-ss.txt.zip",
    ("da", "sv"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/da-sv.txt.zip",
    (
        "da",
        "syr",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/da-syr.txt.zip",
    ("da", "te"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/da-te.txt.zip",
    ("da", "th"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/da-th.txt.zip",
    ("da", "tl"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/da-tl.txt.zip",
    (
        "da",
        "tmh",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/da-tmh.txt.zip",
    ("da", "tr"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/da-tr.txt.zip",
    ("da", "uk"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/da-uk.txt.zip",
    (
        "da",
        "usp",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/da-usp.txt.zip",
    ("da", "vi"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/da-vi.txt.zip",
    (
        "da",
        "wal",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/da-wal.txt.zip",
    ("da", "wo"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/da-wo.txt.zip",
    ("da", "xh"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/da-xh.txt.zip",
    ("da", "zh"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/da-zh.txt.zip",
    ("da", "zu"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/da-zu.txt.zip",
    (
        "de",
        "dik",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/de-dik.txt.zip",
    (
        "de",
        "dje",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/de-dje.txt.zip",
    (
        "de",
        "djk",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/de-djk.txt.zip",
    (
        "de",
        "dop",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/de-dop.txt.zip",
    ("de", "ee"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/de-ee.txt.zip",
    ("de", "el"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/de-el.txt.zip",
    ("de", "en"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/de-en.txt.zip",
    ("de", "eo"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/de-eo.txt.zip",
    ("de", "es"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/de-es.txt.zip",
    ("de", "et"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/de-et.txt.zip",
    ("de", "eu"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/de-eu.txt.zip",
    ("de", "fi"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/de-fi.txt.zip",
    ("de", "fr"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/de-fr.txt.zip",
    (
        "de",
        "gbi",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/de-gbi.txt.zip",
    ("de", "gd"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/de-gd.txt.zip",
    ("de", "gu"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/de-gu.txt.zip",
    ("de", "gv"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/de-gv.txt.zip",
    ("de", "he"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/de-he.txt.zip",
    ("de", "hi"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/de-hi.txt.zip",
    ("de", "hr"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/de-hr.txt.zip",
    ("de", "hu"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/de-hu.txt.zip",
    ("de", "hy"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/de-hy.txt.zip",
    ("de", "id"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/de-id.txt.zip",
    ("de", "is"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/de-is.txt.zip",
    ("de", "it"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/de-it.txt.zip",
    (
        "de",
        "jak",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/de-jak.txt.zip",
    (
        "de",
        "jap",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/de-jap.txt.zip",
    (
        "de",
        "jiv",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/de-jiv.txt.zip",
    (
        "de",
        "kab",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/de-kab.txt.zip",
    (
        "de",
        "kbh",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/de-kbh.txt.zip",
    (
        "de",
        "kek",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/de-kek.txt.zip",
    ("de", "kn"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/de-kn.txt.zip",
    ("de", "ko"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/de-ko.txt.zip",
    ("de", "la"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/de-la.txt.zip",
    ("de", "lt"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/de-lt.txt.zip",
    ("de", "lv"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/de-lv.txt.zip",
    (
        "de",
        "mam",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/de-mam.txt.zip",
    ("de", "mi"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/de-mi.txt.zip",
    ("de", "ml"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/de-ml.txt.zip",
    ("de", "mr"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/de-mr.txt.zip",
    ("de", "my"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/de-my.txt.zip",
    ("de", "ne"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/de-ne.txt.zip",
    (
        "de",
        "nhg",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/de-nhg.txt.zip",
    ("de", "nl"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/de-nl.txt.zip",
    ("de", "no"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/de-no.txt.zip",
    (
        "de",
        "ojb",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/de-ojb.txt.zip",
    (
        "de",
        "pck",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/de-pck.txt.zip",
    (
        "de",
        "pes",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/de-pes.txt.zip",
    ("de", "pl"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/de-pl.txt.zip",
    (
        "de",
        "plt",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/de-plt.txt.zip",
    (
        "de",
        "pot",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/de-pot.txt.zip",
    (
        "de",
        "ppk",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/de-ppk.txt.zip",
    ("de", "pt"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/de-pt.txt.zip",
    (
        "de",
        "quc",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/de-quc.txt.zip",
    (
        "de",
        "quw",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/de-quw.txt.zip",
    ("de", "ro"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/de-ro.txt.zip",
    (
        "de",
        "rom",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/de-rom.txt.zip",
    ("de", "ru"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/de-ru.txt.zip",
    (
        "de",
        "shi",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/de-shi.txt.zip",
    ("de", "sk"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/de-sk.txt.zip",
    ("de", "sl"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/de-sl.txt.zip",
    ("de", "sn"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/de-sn.txt.zip",
    ("de", "so"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/de-so.txt.zip",
    ("de", "sq"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/de-sq.txt.zip",
    ("de", "sr"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/de-sr.txt.zip",
    ("de", "ss"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/de-ss.txt.zip",
    ("de", "sv"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/de-sv.txt.zip",
    (
        "de",
        "syr",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/de-syr.txt.zip",
    ("de", "te"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/de-te.txt.zip",
    ("de", "th"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/de-th.txt.zip",
    ("de", "tl"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/de-tl.txt.zip",
    (
        "de",
        "tmh",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/de-tmh.txt.zip",
    ("de", "tr"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/de-tr.txt.zip",
    ("de", "uk"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/de-uk.txt.zip",
    (
        "de",
        "usp",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/de-usp.txt.zip",
    ("de", "vi"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/de-vi.txt.zip",
    (
        "de",
        "wal",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/de-wal.txt.zip",
    ("de", "wo"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/de-wo.txt.zip",
    ("de", "xh"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/de-xh.txt.zip",
    ("de", "zh"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/de-zh.txt.zip",
    ("de", "zu"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/de-zu.txt.zip",
    (
        "dik",
        "dje",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/dik-dje.txt.zip",
    (
        "dik",
        "djk",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/dik-djk.txt.zip",
    (
        "dik",
        "dop",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/dik-dop.txt.zip",
    (
        "dik",
        "ee",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/dik-ee.txt.zip",
    (
        "dik",
        "el",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/dik-el.txt.zip",
    (
        "dik",
        "en",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/dik-en.txt.zip",
    (
        "dik",
        "eo",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/dik-eo.txt.zip",
    (
        "dik",
        "es",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/dik-es.txt.zip",
    (
        "dik",
        "et",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/dik-et.txt.zip",
    (
        "dik",
        "eu",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/dik-eu.txt.zip",
    (
        "dik",
        "fi",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/dik-fi.txt.zip",
    (
        "dik",
        "fr",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/dik-fr.txt.zip",
    (
        "dik",
        "gbi",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/dik-gbi.txt.zip",
    (
        "dik",
        "gd",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/dik-gd.txt.zip",
    (
        "dik",
        "gu",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/dik-gu.txt.zip",
    (
        "dik",
        "gv",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/dik-gv.txt.zip",
    (
        "dik",
        "he",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/dik-he.txt.zip",
    (
        "dik",
        "hi",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/dik-hi.txt.zip",
    (
        "dik",
        "hr",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/dik-hr.txt.zip",
    (
        "dik",
        "hu",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/dik-hu.txt.zip",
    (
        "dik",
        "hy",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/dik-hy.txt.zip",
    (
        "dik",
        "id",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/dik-id.txt.zip",
    (
        "dik",
        "is",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/dik-is.txt.zip",
    (
        "dik",
        "it",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/dik-it.txt.zip",
    (
        "dik",
        "jak",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/dik-jak.txt.zip",
    (
        "dik",
        "jap",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/dik-jap.txt.zip",
    (
        "dik",
        "jiv",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/dik-jiv.txt.zip",
    (
        "dik",
        "kab",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/dik-kab.txt.zip",
    (
        "dik",
        "kbh",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/dik-kbh.txt.zip",
    (
        "dik",
        "kek",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/dik-kek.txt.zip",
    (
        "dik",
        "kn",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/dik-kn.txt.zip",
    (
        "dik",
        "ko",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/dik-ko.txt.zip",
    (
        "dik",
        "la",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/dik-la.txt.zip",
    (
        "dik",
        "lt",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/dik-lt.txt.zip",
    (
        "dik",
        "lv",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/dik-lv.txt.zip",
    (
        "dik",
        "mam",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/dik-mam.txt.zip",
    (
        "dik",
        "mi",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/dik-mi.txt.zip",
    (
        "dik",
        "ml",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/dik-ml.txt.zip",
    (
        "dik",
        "mr",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/dik-mr.txt.zip",
    (
        "dik",
        "my",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/dik-my.txt.zip",
    (
        "dik",
        "ne",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/dik-ne.txt.zip",
    (
        "dik",
        "nhg",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/dik-nhg.txt.zip",
    (
        "dik",
        "nl",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/dik-nl.txt.zip",
    (
        "dik",
        "no",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/dik-no.txt.zip",
    (
        "dik",
        "ojb",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/dik-ojb.txt.zip",
    (
        "dik",
        "pck",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/dik-pck.txt.zip",
    (
        "dik",
        "pes",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/dik-pes.txt.zip",
    (
        "dik",
        "pl",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/dik-pl.txt.zip",
    (
        "dik",
        "plt",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/dik-plt.txt.zip",
    (
        "dik",
        "pot",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/dik-pot.txt.zip",
    (
        "dik",
        "ppk",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/dik-ppk.txt.zip",
    (
        "dik",
        "pt",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/dik-pt.txt.zip",
    (
        "dik",
        "quc",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/dik-quc.txt.zip",
    (
        "dik",
        "quw",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/dik-quw.txt.zip",
    (
        "dik",
        "ro",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/dik-ro.txt.zip",
    (
        "dik",
        "rom",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/dik-rom.txt.zip",
    (
        "dik",
        "ru",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/dik-ru.txt.zip",
    (
        "dik",
        "shi",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/dik-shi.txt.zip",
    (
        "dik",
        "sk",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/dik-sk.txt.zip",
    (
        "dik",
        "sl",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/dik-sl.txt.zip",
    (
        "dik",
        "sn",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/dik-sn.txt.zip",
    (
        "dik",
        "so",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/dik-so.txt.zip",
    (
        "dik",
        "sq",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/dik-sq.txt.zip",
    (
        "dik",
        "sr",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/dik-sr.txt.zip",
    (
        "dik",
        "ss",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/dik-ss.txt.zip",
    (
        "dik",
        "sv",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/dik-sv.txt.zip",
    (
        "dik",
        "syr",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/dik-syr.txt.zip",
    (
        "dik",
        "te",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/dik-te.txt.zip",
    (
        "dik",
        "th",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/dik-th.txt.zip",
    (
        "dik",
        "tl",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/dik-tl.txt.zip",
    (
        "dik",
        "tmh",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/dik-tmh.txt.zip",
    (
        "dik",
        "tr",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/dik-tr.txt.zip",
    (
        "dik",
        "uk",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/dik-uk.txt.zip",
    (
        "dik",
        "usp",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/dik-usp.txt.zip",
    (
        "dik",
        "vi",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/dik-vi.txt.zip",
    (
        "dik",
        "wal",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/dik-wal.txt.zip",
    (
        "dik",
        "wo",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/dik-wo.txt.zip",
    (
        "dik",
        "xh",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/dik-xh.txt.zip",
    (
        "dik",
        "zh",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/dik-zh.txt.zip",
    (
        "dik",
        "zu",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/dik-zu.txt.zip",
    (
        "dje",
        "djk",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/dje-djk.txt.zip",
    (
        "dje",
        "dop",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/dje-dop.txt.zip",
    (
        "dje",
        "ee",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/dje-ee.txt.zip",
    (
        "dje",
        "el",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/dje-el.txt.zip",
    (
        "dje",
        "en",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/dje-en.txt.zip",
    (
        "dje",
        "eo",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/dje-eo.txt.zip",
    (
        "dje",
        "es",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/dje-es.txt.zip",
    (
        "dje",
        "et",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/dje-et.txt.zip",
    (
        "dje",
        "eu",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/dje-eu.txt.zip",
    (
        "dje",
        "fi",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/dje-fi.txt.zip",
    (
        "dje",
        "fr",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/dje-fr.txt.zip",
    (
        "dje",
        "gbi",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/dje-gbi.txt.zip",
    (
        "dje",
        "gd",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/dje-gd.txt.zip",
    (
        "dje",
        "gu",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/dje-gu.txt.zip",
    (
        "dje",
        "gv",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/dje-gv.txt.zip",
    (
        "dje",
        "he",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/dje-he.txt.zip",
    (
        "dje",
        "hi",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/dje-hi.txt.zip",
    (
        "dje",
        "hr",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/dje-hr.txt.zip",
    (
        "dje",
        "hu",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/dje-hu.txt.zip",
    (
        "dje",
        "hy",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/dje-hy.txt.zip",
    (
        "dje",
        "id",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/dje-id.txt.zip",
    (
        "dje",
        "is",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/dje-is.txt.zip",
    (
        "dje",
        "it",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/dje-it.txt.zip",
    (
        "dje",
        "jak",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/dje-jak.txt.zip",
    (
        "dje",
        "jap",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/dje-jap.txt.zip",
    (
        "dje",
        "jiv",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/dje-jiv.txt.zip",
    (
        "dje",
        "kab",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/dje-kab.txt.zip",
    (
        "dje",
        "kbh",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/dje-kbh.txt.zip",
    (
        "dje",
        "kek",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/dje-kek.txt.zip",
    (
        "dje",
        "kn",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/dje-kn.txt.zip",
    (
        "dje",
        "ko",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/dje-ko.txt.zip",
    (
        "dje",
        "la",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/dje-la.txt.zip",
    (
        "dje",
        "lt",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/dje-lt.txt.zip",
    (
        "dje",
        "lv",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/dje-lv.txt.zip",
    (
        "dje",
        "mam",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/dje-mam.txt.zip",
    (
        "dje",
        "mi",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/dje-mi.txt.zip",
    (
        "dje",
        "ml",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/dje-ml.txt.zip",
    (
        "dje",
        "mr",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/dje-mr.txt.zip",
    (
        "dje",
        "my",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/dje-my.txt.zip",
    (
        "dje",
        "ne",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/dje-ne.txt.zip",
    (
        "dje",
        "nhg",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/dje-nhg.txt.zip",
    (
        "dje",
        "nl",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/dje-nl.txt.zip",
    (
        "dje",
        "no",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/dje-no.txt.zip",
    (
        "dje",
        "ojb",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/dje-ojb.txt.zip",
    (
        "dje",
        "pck",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/dje-pck.txt.zip",
    (
        "dje",
        "pes",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/dje-pes.txt.zip",
    (
        "dje",
        "pl",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/dje-pl.txt.zip",
    (
        "dje",
        "plt",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/dje-plt.txt.zip",
    (
        "dje",
        "pot",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/dje-pot.txt.zip",
    (
        "dje",
        "ppk",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/dje-ppk.txt.zip",
    (
        "dje",
        "pt",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/dje-pt.txt.zip",
    (
        "dje",
        "quc",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/dje-quc.txt.zip",
    (
        "dje",
        "quw",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/dje-quw.txt.zip",
    (
        "dje",
        "ro",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/dje-ro.txt.zip",
    (
        "dje",
        "rom",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/dje-rom.txt.zip",
    (
        "dje",
        "ru",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/dje-ru.txt.zip",
    (
        "dje",
        "shi",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/dje-shi.txt.zip",
    (
        "dje",
        "sk",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/dje-sk.txt.zip",
    (
        "dje",
        "sl",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/dje-sl.txt.zip",
    (
        "dje",
        "sn",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/dje-sn.txt.zip",
    (
        "dje",
        "so",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/dje-so.txt.zip",
    (
        "dje",
        "sq",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/dje-sq.txt.zip",
    (
        "dje",
        "sr",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/dje-sr.txt.zip",
    (
        "dje",
        "ss",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/dje-ss.txt.zip",
    (
        "dje",
        "sv",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/dje-sv.txt.zip",
    (
        "dje",
        "syr",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/dje-syr.txt.zip",
    (
        "dje",
        "te",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/dje-te.txt.zip",
    (
        "dje",
        "th",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/dje-th.txt.zip",
    (
        "dje",
        "tl",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/dje-tl.txt.zip",
    (
        "dje",
        "tmh",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/dje-tmh.txt.zip",
    (
        "dje",
        "tr",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/dje-tr.txt.zip",
    (
        "dje",
        "uk",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/dje-uk.txt.zip",
    (
        "dje",
        "usp",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/dje-usp.txt.zip",
    (
        "dje",
        "vi",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/dje-vi.txt.zip",
    (
        "dje",
        "wal",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/dje-wal.txt.zip",
    (
        "dje",
        "wo",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/dje-wo.txt.zip",
    (
        "dje",
        "xh",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/dje-xh.txt.zip",
    (
        "dje",
        "zh",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/dje-zh.txt.zip",
    (
        "dje",
        "zu",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/dje-zu.txt.zip",
    (
        "djk",
        "dop",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/djk-dop.txt.zip",
    (
        "djk",
        "ee",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/djk-ee.txt.zip",
    (
        "djk",
        "el",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/djk-el.txt.zip",
    (
        "djk",
        "en",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/djk-en.txt.zip",
    (
        "djk",
        "eo",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/djk-eo.txt.zip",
    (
        "djk",
        "es",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/djk-es.txt.zip",
    (
        "djk",
        "et",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/djk-et.txt.zip",
    (
        "djk",
        "eu",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/djk-eu.txt.zip",
    (
        "djk",
        "fi",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/djk-fi.txt.zip",
    (
        "djk",
        "fr",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/djk-fr.txt.zip",
    (
        "djk",
        "gbi",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/djk-gbi.txt.zip",
    (
        "djk",
        "gd",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/djk-gd.txt.zip",
    (
        "djk",
        "gu",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/djk-gu.txt.zip",
    (
        "djk",
        "gv",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/djk-gv.txt.zip",
    (
        "djk",
        "he",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/djk-he.txt.zip",
    (
        "djk",
        "hi",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/djk-hi.txt.zip",
    (
        "djk",
        "hr",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/djk-hr.txt.zip",
    (
        "djk",
        "hu",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/djk-hu.txt.zip",
    (
        "djk",
        "hy",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/djk-hy.txt.zip",
    (
        "djk",
        "id",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/djk-id.txt.zip",
    (
        "djk",
        "is",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/djk-is.txt.zip",
    (
        "djk",
        "it",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/djk-it.txt.zip",
    (
        "djk",
        "jak",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/djk-jak.txt.zip",
    (
        "djk",
        "jap",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/djk-jap.txt.zip",
    (
        "djk",
        "jiv",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/djk-jiv.txt.zip",
    (
        "djk",
        "kab",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/djk-kab.txt.zip",
    (
        "djk",
        "kbh",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/djk-kbh.txt.zip",
    (
        "djk",
        "kek",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/djk-kek.txt.zip",
    (
        "djk",
        "kn",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/djk-kn.txt.zip",
    (
        "djk",
        "ko",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/djk-ko.txt.zip",
    (
        "djk",
        "la",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/djk-la.txt.zip",
    (
        "djk",
        "lt",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/djk-lt.txt.zip",
    (
        "djk",
        "lv",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/djk-lv.txt.zip",
    (
        "djk",
        "mam",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/djk-mam.txt.zip",
    (
        "djk",
        "mi",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/djk-mi.txt.zip",
    (
        "djk",
        "ml",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/djk-ml.txt.zip",
    (
        "djk",
        "mr",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/djk-mr.txt.zip",
    (
        "djk",
        "my",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/djk-my.txt.zip",
    (
        "djk",
        "ne",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/djk-ne.txt.zip",
    (
        "djk",
        "nhg",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/djk-nhg.txt.zip",
    (
        "djk",
        "nl",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/djk-nl.txt.zip",
    (
        "djk",
        "no",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/djk-no.txt.zip",
    (
        "djk",
        "ojb",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/djk-ojb.txt.zip",
    (
        "djk",
        "pck",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/djk-pck.txt.zip",
    (
        "djk",
        "pes",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/djk-pes.txt.zip",
    (
        "djk",
        "pl",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/djk-pl.txt.zip",
    (
        "djk",
        "plt",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/djk-plt.txt.zip",
    (
        "djk",
        "pot",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/djk-pot.txt.zip",
    (
        "djk",
        "ppk",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/djk-ppk.txt.zip",
    (
        "djk",
        "pt",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/djk-pt.txt.zip",
    (
        "djk",
        "quc",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/djk-quc.txt.zip",
    (
        "djk",
        "quw",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/djk-quw.txt.zip",
    (
        "djk",
        "ro",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/djk-ro.txt.zip",
    (
        "djk",
        "rom",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/djk-rom.txt.zip",
    (
        "djk",
        "ru",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/djk-ru.txt.zip",
    (
        "djk",
        "shi",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/djk-shi.txt.zip",
    (
        "djk",
        "sk",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/djk-sk.txt.zip",
    (
        "djk",
        "sl",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/djk-sl.txt.zip",
    (
        "djk",
        "sn",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/djk-sn.txt.zip",
    (
        "djk",
        "so",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/djk-so.txt.zip",
    (
        "djk",
        "sq",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/djk-sq.txt.zip",
    (
        "djk",
        "sr",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/djk-sr.txt.zip",
    (
        "djk",
        "ss",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/djk-ss.txt.zip",
    (
        "djk",
        "sv",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/djk-sv.txt.zip",
    (
        "djk",
        "syr",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/djk-syr.txt.zip",
    (
        "djk",
        "te",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/djk-te.txt.zip",
    (
        "djk",
        "th",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/djk-th.txt.zip",
    (
        "djk",
        "tl",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/djk-tl.txt.zip",
    (
        "djk",
        "tmh",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/djk-tmh.txt.zip",
    (
        "djk",
        "tr",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/djk-tr.txt.zip",
    (
        "djk",
        "uk",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/djk-uk.txt.zip",
    (
        "djk",
        "usp",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/djk-usp.txt.zip",
    (
        "djk",
        "vi",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/djk-vi.txt.zip",
    (
        "djk",
        "wal",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/djk-wal.txt.zip",
    (
        "djk",
        "wo",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/djk-wo.txt.zip",
    (
        "djk",
        "xh",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/djk-xh.txt.zip",
    (
        "djk",
        "zh",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/djk-zh.txt.zip",
    (
        "djk",
        "zu",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/djk-zu.txt.zip",
    (
        "dop",
        "ee",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/dop-ee.txt.zip",
    (
        "dop",
        "el",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/dop-el.txt.zip",
    (
        "dop",
        "en",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/dop-en.txt.zip",
    (
        "dop",
        "eo",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/dop-eo.txt.zip",
    (
        "dop",
        "es",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/dop-es.txt.zip",
    (
        "dop",
        "et",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/dop-et.txt.zip",
    (
        "dop",
        "eu",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/dop-eu.txt.zip",
    (
        "dop",
        "fi",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/dop-fi.txt.zip",
    (
        "dop",
        "fr",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/dop-fr.txt.zip",
    (
        "dop",
        "gbi",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/dop-gbi.txt.zip",
    (
        "dop",
        "gd",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/dop-gd.txt.zip",
    (
        "dop",
        "gu",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/dop-gu.txt.zip",
    (
        "dop",
        "gv",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/dop-gv.txt.zip",
    (
        "dop",
        "he",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/dop-he.txt.zip",
    (
        "dop",
        "hi",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/dop-hi.txt.zip",
    (
        "dop",
        "hr",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/dop-hr.txt.zip",
    (
        "dop",
        "hu",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/dop-hu.txt.zip",
    (
        "dop",
        "hy",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/dop-hy.txt.zip",
    (
        "dop",
        "id",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/dop-id.txt.zip",
    (
        "dop",
        "is",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/dop-is.txt.zip",
    (
        "dop",
        "it",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/dop-it.txt.zip",
    (
        "dop",
        "jak",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/dop-jak.txt.zip",
    (
        "dop",
        "jap",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/dop-jap.txt.zip",
    (
        "dop",
        "jiv",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/dop-jiv.txt.zip",
    (
        "dop",
        "kab",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/dop-kab.txt.zip",
    (
        "dop",
        "kbh",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/dop-kbh.txt.zip",
    (
        "dop",
        "kek",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/dop-kek.txt.zip",
    (
        "dop",
        "kn",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/dop-kn.txt.zip",
    (
        "dop",
        "ko",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/dop-ko.txt.zip",
    (
        "dop",
        "la",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/dop-la.txt.zip",
    (
        "dop",
        "lt",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/dop-lt.txt.zip",
    (
        "dop",
        "lv",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/dop-lv.txt.zip",
    (
        "dop",
        "mam",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/dop-mam.txt.zip",
    (
        "dop",
        "mi",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/dop-mi.txt.zip",
    (
        "dop",
        "ml",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/dop-ml.txt.zip",
    (
        "dop",
        "mr",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/dop-mr.txt.zip",
    (
        "dop",
        "my",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/dop-my.txt.zip",
    (
        "dop",
        "ne",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/dop-ne.txt.zip",
    (
        "dop",
        "nhg",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/dop-nhg.txt.zip",
    (
        "dop",
        "nl",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/dop-nl.txt.zip",
    (
        "dop",
        "no",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/dop-no.txt.zip",
    (
        "dop",
        "ojb",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/dop-ojb.txt.zip",
    (
        "dop",
        "pck",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/dop-pck.txt.zip",
    (
        "dop",
        "pes",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/dop-pes.txt.zip",
    (
        "dop",
        "pl",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/dop-pl.txt.zip",
    (
        "dop",
        "plt",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/dop-plt.txt.zip",
    (
        "dop",
        "pot",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/dop-pot.txt.zip",
    (
        "dop",
        "ppk",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/dop-ppk.txt.zip",
    (
        "dop",
        "pt",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/dop-pt.txt.zip",
    (
        "dop",
        "quc",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/dop-quc.txt.zip",
    (
        "dop",
        "quw",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/dop-quw.txt.zip",
    (
        "dop",
        "ro",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/dop-ro.txt.zip",
    (
        "dop",
        "rom",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/dop-rom.txt.zip",
    (
        "dop",
        "ru",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/dop-ru.txt.zip",
    (
        "dop",
        "shi",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/dop-shi.txt.zip",
    (
        "dop",
        "sk",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/dop-sk.txt.zip",
    (
        "dop",
        "sl",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/dop-sl.txt.zip",
    (
        "dop",
        "sn",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/dop-sn.txt.zip",
    (
        "dop",
        "so",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/dop-so.txt.zip",
    (
        "dop",
        "sq",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/dop-sq.txt.zip",
    (
        "dop",
        "sr",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/dop-sr.txt.zip",
    (
        "dop",
        "ss",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/dop-ss.txt.zip",
    (
        "dop",
        "sv",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/dop-sv.txt.zip",
    (
        "dop",
        "syr",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/dop-syr.txt.zip",
    (
        "dop",
        "te",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/dop-te.txt.zip",
    (
        "dop",
        "th",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/dop-th.txt.zip",
    (
        "dop",
        "tl",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/dop-tl.txt.zip",
    (
        "dop",
        "tmh",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/dop-tmh.txt.zip",
    (
        "dop",
        "tr",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/dop-tr.txt.zip",
    (
        "dop",
        "uk",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/dop-uk.txt.zip",
    (
        "dop",
        "usp",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/dop-usp.txt.zip",
    (
        "dop",
        "vi",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/dop-vi.txt.zip",
    (
        "dop",
        "wal",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/dop-wal.txt.zip",
    (
        "dop",
        "wo",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/dop-wo.txt.zip",
    (
        "dop",
        "xh",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/dop-xh.txt.zip",
    (
        "dop",
        "zh",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/dop-zh.txt.zip",
    (
        "dop",
        "zu",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/dop-zu.txt.zip",
    ("ee", "el"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ee-el.txt.zip",
    ("ee", "en"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ee-en.txt.zip",
    ("ee", "eo"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ee-eo.txt.zip",
    ("ee", "es"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ee-es.txt.zip",
    ("ee", "et"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ee-et.txt.zip",
    ("ee", "eu"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ee-eu.txt.zip",
    ("ee", "fi"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ee-fi.txt.zip",
    ("ee", "fr"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ee-fr.txt.zip",
    (
        "ee",
        "gbi",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ee-gbi.txt.zip",
    ("ee", "gd"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ee-gd.txt.zip",
    ("ee", "gu"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ee-gu.txt.zip",
    ("ee", "gv"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ee-gv.txt.zip",
    ("ee", "he"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ee-he.txt.zip",
    ("ee", "hi"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ee-hi.txt.zip",
    ("ee", "hr"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ee-hr.txt.zip",
    ("ee", "hu"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ee-hu.txt.zip",
    ("ee", "hy"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ee-hy.txt.zip",
    ("ee", "id"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ee-id.txt.zip",
    ("ee", "is"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ee-is.txt.zip",
    ("ee", "it"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ee-it.txt.zip",
    (
        "ee",
        "jak",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ee-jak.txt.zip",
    (
        "ee",
        "jap",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ee-jap.txt.zip",
    (
        "ee",
        "jiv",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ee-jiv.txt.zip",
    (
        "ee",
        "kab",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ee-kab.txt.zip",
    (
        "ee",
        "kbh",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ee-kbh.txt.zip",
    (
        "ee",
        "kek",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ee-kek.txt.zip",
    ("ee", "kn"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ee-kn.txt.zip",
    ("ee", "ko"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ee-ko.txt.zip",
    ("ee", "la"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ee-la.txt.zip",
    ("ee", "lt"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ee-lt.txt.zip",
    ("ee", "lv"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ee-lv.txt.zip",
    (
        "ee",
        "mam",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ee-mam.txt.zip",
    ("ee", "mi"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ee-mi.txt.zip",
    ("ee", "ml"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ee-ml.txt.zip",
    ("ee", "mr"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ee-mr.txt.zip",
    ("ee", "my"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ee-my.txt.zip",
    ("ee", "ne"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ee-ne.txt.zip",
    (
        "ee",
        "nhg",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ee-nhg.txt.zip",
    ("ee", "nl"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ee-nl.txt.zip",
    ("ee", "no"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ee-no.txt.zip",
    (
        "ee",
        "ojb",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ee-ojb.txt.zip",
    (
        "ee",
        "pck",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ee-pck.txt.zip",
    (
        "ee",
        "pes",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ee-pes.txt.zip",
    ("ee", "pl"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ee-pl.txt.zip",
    (
        "ee",
        "plt",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ee-plt.txt.zip",
    (
        "ee",
        "pot",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ee-pot.txt.zip",
    (
        "ee",
        "ppk",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ee-ppk.txt.zip",
    ("ee", "pt"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ee-pt.txt.zip",
    (
        "ee",
        "quc",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ee-quc.txt.zip",
    (
        "ee",
        "quw",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ee-quw.txt.zip",
    ("ee", "ro"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ee-ro.txt.zip",
    (
        "ee",
        "rom",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ee-rom.txt.zip",
    ("ee", "ru"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ee-ru.txt.zip",
    (
        "ee",
        "shi",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ee-shi.txt.zip",
    ("ee", "sk"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ee-sk.txt.zip",
    ("ee", "sl"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ee-sl.txt.zip",
    ("ee", "sn"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ee-sn.txt.zip",
    ("ee", "so"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ee-so.txt.zip",
    ("ee", "sq"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ee-sq.txt.zip",
    ("ee", "sr"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ee-sr.txt.zip",
    ("ee", "ss"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ee-ss.txt.zip",
    ("ee", "sv"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ee-sv.txt.zip",
    (
        "ee",
        "syr",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ee-syr.txt.zip",
    ("ee", "te"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ee-te.txt.zip",
    ("ee", "th"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ee-th.txt.zip",
    ("ee", "tl"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ee-tl.txt.zip",
    (
        "ee",
        "tmh",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ee-tmh.txt.zip",
    ("ee", "tr"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ee-tr.txt.zip",
    ("ee", "uk"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ee-uk.txt.zip",
    (
        "ee",
        "usp",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ee-usp.txt.zip",
    ("ee", "vi"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ee-vi.txt.zip",
    (
        "ee",
        "wal",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ee-wal.txt.zip",
    ("ee", "wo"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ee-wo.txt.zip",
    ("ee", "xh"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ee-xh.txt.zip",
    ("ee", "zh"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ee-zh.txt.zip",
    ("ee", "zu"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ee-zu.txt.zip",
    ("el", "en"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/el-en.txt.zip",
    ("el", "eo"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/el-eo.txt.zip",
    ("el", "es"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/el-es.txt.zip",
    ("el", "et"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/el-et.txt.zip",
    ("el", "eu"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/el-eu.txt.zip",
    ("el", "fi"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/el-fi.txt.zip",
    ("el", "fr"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/el-fr.txt.zip",
    (
        "el",
        "gbi",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/el-gbi.txt.zip",
    ("el", "gd"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/el-gd.txt.zip",
    ("el", "gu"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/el-gu.txt.zip",
    ("el", "gv"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/el-gv.txt.zip",
    ("el", "he"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/el-he.txt.zip",
    ("el", "hi"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/el-hi.txt.zip",
    ("el", "hr"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/el-hr.txt.zip",
    ("el", "hu"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/el-hu.txt.zip",
    ("el", "hy"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/el-hy.txt.zip",
    ("el", "id"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/el-id.txt.zip",
    ("el", "is"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/el-is.txt.zip",
    ("el", "it"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/el-it.txt.zip",
    (
        "el",
        "jak",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/el-jak.txt.zip",
    (
        "el",
        "jap",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/el-jap.txt.zip",
    (
        "el",
        "jiv",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/el-jiv.txt.zip",
    (
        "el",
        "kab",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/el-kab.txt.zip",
    (
        "el",
        "kbh",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/el-kbh.txt.zip",
    (
        "el",
        "kek",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/el-kek.txt.zip",
    ("el", "kn"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/el-kn.txt.zip",
    ("el", "ko"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/el-ko.txt.zip",
    ("el", "la"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/el-la.txt.zip",
    ("el", "lt"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/el-lt.txt.zip",
    ("el", "lv"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/el-lv.txt.zip",
    (
        "el",
        "mam",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/el-mam.txt.zip",
    ("el", "mi"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/el-mi.txt.zip",
    ("el", "ml"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/el-ml.txt.zip",
    ("el", "mr"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/el-mr.txt.zip",
    ("el", "my"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/el-my.txt.zip",
    ("el", "ne"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/el-ne.txt.zip",
    (
        "el",
        "nhg",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/el-nhg.txt.zip",
    ("el", "nl"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/el-nl.txt.zip",
    ("el", "no"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/el-no.txt.zip",
    (
        "el",
        "ojb",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/el-ojb.txt.zip",
    (
        "el",
        "pck",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/el-pck.txt.zip",
    (
        "el",
        "pes",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/el-pes.txt.zip",
    ("el", "pl"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/el-pl.txt.zip",
    (
        "el",
        "plt",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/el-plt.txt.zip",
    (
        "el",
        "pot",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/el-pot.txt.zip",
    (
        "el",
        "ppk",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/el-ppk.txt.zip",
    ("el", "pt"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/el-pt.txt.zip",
    (
        "el",
        "quc",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/el-quc.txt.zip",
    (
        "el",
        "quw",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/el-quw.txt.zip",
    ("el", "ro"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/el-ro.txt.zip",
    (
        "el",
        "rom",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/el-rom.txt.zip",
    ("el", "ru"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/el-ru.txt.zip",
    (
        "el",
        "shi",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/el-shi.txt.zip",
    ("el", "sk"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/el-sk.txt.zip",
    ("el", "sl"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/el-sl.txt.zip",
    ("el", "sn"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/el-sn.txt.zip",
    ("el", "so"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/el-so.txt.zip",
    ("el", "sq"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/el-sq.txt.zip",
    ("el", "sr"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/el-sr.txt.zip",
    ("el", "ss"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/el-ss.txt.zip",
    ("el", "sv"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/el-sv.txt.zip",
    (
        "el",
        "syr",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/el-syr.txt.zip",
    ("el", "te"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/el-te.txt.zip",
    ("el", "th"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/el-th.txt.zip",
    ("el", "tl"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/el-tl.txt.zip",
    (
        "el",
        "tmh",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/el-tmh.txt.zip",
    ("el", "tr"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/el-tr.txt.zip",
    ("el", "uk"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/el-uk.txt.zip",
    (
        "el",
        "usp",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/el-usp.txt.zip",
    ("el", "vi"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/el-vi.txt.zip",
    (
        "el",
        "wal",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/el-wal.txt.zip",
    ("el", "wo"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/el-wo.txt.zip",
    ("el", "xh"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/el-xh.txt.zip",
    ("el", "zh"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/el-zh.txt.zip",
    ("el", "zu"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/el-zu.txt.zip",
    ("en", "eo"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/en-eo.txt.zip",
    ("en", "es"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/en-es.txt.zip",
    ("en", "et"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/en-et.txt.zip",
    ("en", "eu"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/en-eu.txt.zip",
    ("en", "fi"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/en-fi.txt.zip",
    ("en", "fr"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/en-fr.txt.zip",
    (
        "en",
        "gbi",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/en-gbi.txt.zip",
    ("en", "gd"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/en-gd.txt.zip",
    ("en", "gu"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/en-gu.txt.zip",
    ("en", "gv"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/en-gv.txt.zip",
    ("en", "he"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/en-he.txt.zip",
    ("en", "hi"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/en-hi.txt.zip",
    ("en", "hr"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/en-hr.txt.zip",
    ("en", "hu"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/en-hu.txt.zip",
    ("en", "hy"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/en-hy.txt.zip",
    ("en", "id"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/en-id.txt.zip",
    ("en", "is"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/en-is.txt.zip",
    ("en", "it"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/en-it.txt.zip",
    (
        "en",
        "jak",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/en-jak.txt.zip",
    (
        "en",
        "jap",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/en-jap.txt.zip",
    (
        "en",
        "jiv",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/en-jiv.txt.zip",
    (
        "en",
        "kab",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/en-kab.txt.zip",
    (
        "en",
        "kbh",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/en-kbh.txt.zip",
    (
        "en",
        "kek",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/en-kek.txt.zip",
    ("en", "kn"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/en-kn.txt.zip",
    ("en", "ko"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/en-ko.txt.zip",
    ("en", "la"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/en-la.txt.zip",
    ("en", "lt"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/en-lt.txt.zip",
    ("en", "lv"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/en-lv.txt.zip",
    (
        "en",
        "mam",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/en-mam.txt.zip",
    ("en", "mi"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/en-mi.txt.zip",
    ("en", "ml"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/en-ml.txt.zip",
    ("en", "mr"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/en-mr.txt.zip",
    ("en", "my"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/en-my.txt.zip",
    ("en", "ne"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/en-ne.txt.zip",
    (
        "en",
        "nhg",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/en-nhg.txt.zip",
    ("en", "nl"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/en-nl.txt.zip",
    ("en", "no"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/en-no.txt.zip",
    (
        "en",
        "ojb",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/en-ojb.txt.zip",
    (
        "en",
        "pck",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/en-pck.txt.zip",
    (
        "en",
        "pes",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/en-pes.txt.zip",
    ("en", "pl"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/en-pl.txt.zip",
    (
        "en",
        "plt",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/en-plt.txt.zip",
    (
        "en",
        "pot",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/en-pot.txt.zip",
    (
        "en",
        "ppk",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/en-ppk.txt.zip",
    ("en", "pt"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/en-pt.txt.zip",
    (
        "en",
        "quc",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/en-quc.txt.zip",
    (
        "en",
        "quw",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/en-quw.txt.zip",
    ("en", "ro"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/en-ro.txt.zip",
    (
        "en",
        "rom",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/en-rom.txt.zip",
    ("en", "ru"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/en-ru.txt.zip",
    (
        "en",
        "shi",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/en-shi.txt.zip",
    ("en", "sk"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/en-sk.txt.zip",
    ("en", "sl"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/en-sl.txt.zip",
    ("en", "sn"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/en-sn.txt.zip",
    ("en", "so"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/en-so.txt.zip",
    ("en", "sq"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/en-sq.txt.zip",
    ("en", "sr"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/en-sr.txt.zip",
    ("en", "ss"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/en-ss.txt.zip",
    ("en", "sv"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/en-sv.txt.zip",
    (
        "en",
        "syr",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/en-syr.txt.zip",
    ("en", "te"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/en-te.txt.zip",
    ("en", "th"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/en-th.txt.zip",
    ("en", "tl"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/en-tl.txt.zip",
    (
        "en",
        "tmh",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/en-tmh.txt.zip",
    ("en", "tr"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/en-tr.txt.zip",
    ("en", "uk"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/en-uk.txt.zip",
    (
        "en",
        "usp",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/en-usp.txt.zip",
    ("en", "vi"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/en-vi.txt.zip",
    (
        "en",
        "wal",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/en-wal.txt.zip",
    ("en", "wo"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/en-wo.txt.zip",
    ("en", "xh"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/en-xh.txt.zip",
    ("en", "zh"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/en-zh.txt.zip",
    ("en", "zu"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/en-zu.txt.zip",
    ("eo", "es"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/eo-es.txt.zip",
    ("eo", "et"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/eo-et.txt.zip",
    ("eo", "eu"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/eo-eu.txt.zip",
    ("eo", "fi"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/eo-fi.txt.zip",
    ("eo", "fr"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/eo-fr.txt.zip",
    (
        "eo",
        "gbi",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/eo-gbi.txt.zip",
    ("eo", "gd"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/eo-gd.txt.zip",
    ("eo", "gu"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/eo-gu.txt.zip",
    ("eo", "gv"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/eo-gv.txt.zip",
    ("eo", "he"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/eo-he.txt.zip",
    ("eo", "hi"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/eo-hi.txt.zip",
    ("eo", "hr"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/eo-hr.txt.zip",
    ("eo", "hu"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/eo-hu.txt.zip",
    ("eo", "hy"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/eo-hy.txt.zip",
    ("eo", "id"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/eo-id.txt.zip",
    ("eo", "is"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/eo-is.txt.zip",
    ("eo", "it"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/eo-it.txt.zip",
    (
        "eo",
        "jak",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/eo-jak.txt.zip",
    (
        "eo",
        "jap",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/eo-jap.txt.zip",
    (
        "eo",
        "jiv",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/eo-jiv.txt.zip",
    (
        "eo",
        "kab",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/eo-kab.txt.zip",
    (
        "eo",
        "kbh",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/eo-kbh.txt.zip",
    (
        "eo",
        "kek",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/eo-kek.txt.zip",
    ("eo", "kn"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/eo-kn.txt.zip",
    ("eo", "ko"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/eo-ko.txt.zip",
    ("eo", "la"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/eo-la.txt.zip",
    ("eo", "lt"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/eo-lt.txt.zip",
    ("eo", "lv"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/eo-lv.txt.zip",
    (
        "eo",
        "mam",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/eo-mam.txt.zip",
    ("eo", "mi"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/eo-mi.txt.zip",
    ("eo", "ml"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/eo-ml.txt.zip",
    ("eo", "mr"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/eo-mr.txt.zip",
    ("eo", "my"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/eo-my.txt.zip",
    ("eo", "ne"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/eo-ne.txt.zip",
    (
        "eo",
        "nhg",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/eo-nhg.txt.zip",
    ("eo", "nl"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/eo-nl.txt.zip",
    ("eo", "no"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/eo-no.txt.zip",
    (
        "eo",
        "ojb",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/eo-ojb.txt.zip",
    (
        "eo",
        "pck",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/eo-pck.txt.zip",
    (
        "eo",
        "pes",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/eo-pes.txt.zip",
    ("eo", "pl"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/eo-pl.txt.zip",
    (
        "eo",
        "plt",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/eo-plt.txt.zip",
    (
        "eo",
        "pot",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/eo-pot.txt.zip",
    (
        "eo",
        "ppk",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/eo-ppk.txt.zip",
    ("eo", "pt"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/eo-pt.txt.zip",
    (
        "eo",
        "quc",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/eo-quc.txt.zip",
    (
        "eo",
        "quw",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/eo-quw.txt.zip",
    ("eo", "ro"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/eo-ro.txt.zip",
    (
        "eo",
        "rom",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/eo-rom.txt.zip",
    ("eo", "ru"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/eo-ru.txt.zip",
    (
        "eo",
        "shi",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/eo-shi.txt.zip",
    ("eo", "sk"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/eo-sk.txt.zip",
    ("eo", "sl"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/eo-sl.txt.zip",
    ("eo", "sn"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/eo-sn.txt.zip",
    ("eo", "so"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/eo-so.txt.zip",
    ("eo", "sq"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/eo-sq.txt.zip",
    ("eo", "sr"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/eo-sr.txt.zip",
    ("eo", "ss"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/eo-ss.txt.zip",
    ("eo", "sv"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/eo-sv.txt.zip",
    (
        "eo",
        "syr",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/eo-syr.txt.zip",
    ("eo", "te"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/eo-te.txt.zip",
    ("eo", "th"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/eo-th.txt.zip",
    ("eo", "tl"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/eo-tl.txt.zip",
    (
        "eo",
        "tmh",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/eo-tmh.txt.zip",
    ("eo", "tr"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/eo-tr.txt.zip",
    ("eo", "uk"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/eo-uk.txt.zip",
    (
        "eo",
        "usp",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/eo-usp.txt.zip",
    ("eo", "vi"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/eo-vi.txt.zip",
    (
        "eo",
        "wal",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/eo-wal.txt.zip",
    ("eo", "wo"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/eo-wo.txt.zip",
    ("eo", "xh"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/eo-xh.txt.zip",
    ("eo", "zh"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/eo-zh.txt.zip",
    ("eo", "zu"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/eo-zu.txt.zip",
    ("es", "et"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/es-et.txt.zip",
    ("es", "eu"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/es-eu.txt.zip",
    ("es", "fi"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/es-fi.txt.zip",
    ("es", "fr"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/es-fr.txt.zip",
    (
        "es",
        "gbi",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/es-gbi.txt.zip",
    ("es", "gd"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/es-gd.txt.zip",
    ("es", "gu"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/es-gu.txt.zip",
    ("es", "gv"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/es-gv.txt.zip",
    ("es", "he"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/es-he.txt.zip",
    ("es", "hi"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/es-hi.txt.zip",
    ("es", "hr"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/es-hr.txt.zip",
    ("es", "hu"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/es-hu.txt.zip",
    ("es", "hy"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/es-hy.txt.zip",
    ("es", "id"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/es-id.txt.zip",
    ("es", "is"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/es-is.txt.zip",
    ("es", "it"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/es-it.txt.zip",
    (
        "es",
        "jak",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/es-jak.txt.zip",
    (
        "es",
        "jap",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/es-jap.txt.zip",
    (
        "es",
        "jiv",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/es-jiv.txt.zip",
    (
        "es",
        "kab",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/es-kab.txt.zip",
    (
        "es",
        "kbh",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/es-kbh.txt.zip",
    (
        "es",
        "kek",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/es-kek.txt.zip",
    ("es", "kn"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/es-kn.txt.zip",
    ("es", "ko"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/es-ko.txt.zip",
    ("es", "la"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/es-la.txt.zip",
    ("es", "lt"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/es-lt.txt.zip",
    ("es", "lv"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/es-lv.txt.zip",
    (
        "es",
        "mam",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/es-mam.txt.zip",
    ("es", "mi"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/es-mi.txt.zip",
    ("es", "ml"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/es-ml.txt.zip",
    ("es", "mr"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/es-mr.txt.zip",
    ("es", "my"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/es-my.txt.zip",
    ("es", "ne"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/es-ne.txt.zip",
    (
        "es",
        "nhg",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/es-nhg.txt.zip",
    ("es", "nl"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/es-nl.txt.zip",
    ("es", "no"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/es-no.txt.zip",
    (
        "es",
        "ojb",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/es-ojb.txt.zip",
    (
        "es",
        "pck",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/es-pck.txt.zip",
    (
        "es",
        "pes",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/es-pes.txt.zip",
    ("es", "pl"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/es-pl.txt.zip",
    (
        "es",
        "plt",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/es-plt.txt.zip",
    (
        "es",
        "pot",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/es-pot.txt.zip",
    (
        "es",
        "ppk",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/es-ppk.txt.zip",
    ("es", "pt"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/es-pt.txt.zip",
    (
        "es",
        "quc",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/es-quc.txt.zip",
    (
        "es",
        "quw",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/es-quw.txt.zip",
    ("es", "ro"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/es-ro.txt.zip",
    (
        "es",
        "rom",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/es-rom.txt.zip",
    ("es", "ru"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/es-ru.txt.zip",
    (
        "es",
        "shi",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/es-shi.txt.zip",
    ("es", "sk"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/es-sk.txt.zip",
    ("es", "sl"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/es-sl.txt.zip",
    ("es", "sn"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/es-sn.txt.zip",
    ("es", "so"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/es-so.txt.zip",
    ("es", "sq"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/es-sq.txt.zip",
    ("es", "sr"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/es-sr.txt.zip",
    ("es", "ss"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/es-ss.txt.zip",
    ("es", "sv"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/es-sv.txt.zip",
    (
        "es",
        "syr",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/es-syr.txt.zip",
    ("es", "te"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/es-te.txt.zip",
    ("es", "th"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/es-th.txt.zip",
    ("es", "tl"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/es-tl.txt.zip",
    (
        "es",
        "tmh",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/es-tmh.txt.zip",
    ("es", "tr"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/es-tr.txt.zip",
    ("es", "uk"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/es-uk.txt.zip",
    (
        "es",
        "usp",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/es-usp.txt.zip",
    ("es", "vi"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/es-vi.txt.zip",
    (
        "es",
        "wal",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/es-wal.txt.zip",
    ("es", "wo"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/es-wo.txt.zip",
    ("es", "xh"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/es-xh.txt.zip",
    ("es", "zh"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/es-zh.txt.zip",
    ("es", "zu"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/es-zu.txt.zip",
    ("et", "eu"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/et-eu.txt.zip",
    ("et", "fi"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/et-fi.txt.zip",
    ("et", "fr"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/et-fr.txt.zip",
    (
        "et",
        "gbi",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/et-gbi.txt.zip",
    ("et", "gd"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/et-gd.txt.zip",
    ("et", "gu"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/et-gu.txt.zip",
    ("et", "gv"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/et-gv.txt.zip",
    ("et", "he"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/et-he.txt.zip",
    ("et", "hi"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/et-hi.txt.zip",
    ("et", "hr"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/et-hr.txt.zip",
    ("et", "hu"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/et-hu.txt.zip",
    ("et", "hy"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/et-hy.txt.zip",
    ("et", "id"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/et-id.txt.zip",
    ("et", "is"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/et-is.txt.zip",
    ("et", "it"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/et-it.txt.zip",
    (
        "et",
        "jak",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/et-jak.txt.zip",
    (
        "et",
        "jap",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/et-jap.txt.zip",
    (
        "et",
        "jiv",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/et-jiv.txt.zip",
    (
        "et",
        "kab",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/et-kab.txt.zip",
    (
        "et",
        "kbh",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/et-kbh.txt.zip",
    (
        "et",
        "kek",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/et-kek.txt.zip",
    ("et", "kn"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/et-kn.txt.zip",
    ("et", "ko"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/et-ko.txt.zip",
    ("et", "la"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/et-la.txt.zip",
    ("et", "lt"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/et-lt.txt.zip",
    ("et", "lv"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/et-lv.txt.zip",
    (
        "et",
        "mam",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/et-mam.txt.zip",
    ("et", "mi"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/et-mi.txt.zip",
    ("et", "ml"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/et-ml.txt.zip",
    ("et", "mr"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/et-mr.txt.zip",
    ("et", "my"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/et-my.txt.zip",
    ("et", "ne"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/et-ne.txt.zip",
    (
        "et",
        "nhg",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/et-nhg.txt.zip",
    ("et", "nl"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/et-nl.txt.zip",
    ("et", "no"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/et-no.txt.zip",
    (
        "et",
        "ojb",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/et-ojb.txt.zip",
    (
        "et",
        "pck",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/et-pck.txt.zip",
    (
        "et",
        "pes",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/et-pes.txt.zip",
    ("et", "pl"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/et-pl.txt.zip",
    (
        "et",
        "plt",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/et-plt.txt.zip",
    (
        "et",
        "pot",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/et-pot.txt.zip",
    (
        "et",
        "ppk",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/et-ppk.txt.zip",
    ("et", "pt"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/et-pt.txt.zip",
    (
        "et",
        "quc",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/et-quc.txt.zip",
    (
        "et",
        "quw",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/et-quw.txt.zip",
    ("et", "ro"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/et-ro.txt.zip",
    (
        "et",
        "rom",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/et-rom.txt.zip",
    ("et", "ru"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/et-ru.txt.zip",
    (
        "et",
        "shi",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/et-shi.txt.zip",
    ("et", "sk"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/et-sk.txt.zip",
    ("et", "sl"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/et-sl.txt.zip",
    ("et", "sn"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/et-sn.txt.zip",
    ("et", "so"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/et-so.txt.zip",
    ("et", "sq"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/et-sq.txt.zip",
    ("et", "sr"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/et-sr.txt.zip",
    ("et", "ss"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/et-ss.txt.zip",
    ("et", "sv"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/et-sv.txt.zip",
    (
        "et",
        "syr",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/et-syr.txt.zip",
    ("et", "te"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/et-te.txt.zip",
    ("et", "th"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/et-th.txt.zip",
    ("et", "tl"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/et-tl.txt.zip",
    (
        "et",
        "tmh",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/et-tmh.txt.zip",
    ("et", "tr"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/et-tr.txt.zip",
    ("et", "uk"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/et-uk.txt.zip",
    (
        "et",
        "usp",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/et-usp.txt.zip",
    ("et", "vi"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/et-vi.txt.zip",
    (
        "et",
        "wal",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/et-wal.txt.zip",
    ("et", "wo"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/et-wo.txt.zip",
    ("et", "xh"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/et-xh.txt.zip",
    ("et", "zh"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/et-zh.txt.zip",
    ("et", "zu"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/et-zu.txt.zip",
    ("eu", "fi"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/eu-fi.txt.zip",
    ("eu", "fr"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/eu-fr.txt.zip",
    (
        "eu",
        "gbi",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/eu-gbi.txt.zip",
    ("eu", "gd"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/eu-gd.txt.zip",
    ("eu", "gu"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/eu-gu.txt.zip",
    ("eu", "gv"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/eu-gv.txt.zip",
    ("eu", "he"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/eu-he.txt.zip",
    ("eu", "hi"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/eu-hi.txt.zip",
    ("eu", "hr"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/eu-hr.txt.zip",
    ("eu", "hu"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/eu-hu.txt.zip",
    ("eu", "hy"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/eu-hy.txt.zip",
    ("eu", "id"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/eu-id.txt.zip",
    ("eu", "is"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/eu-is.txt.zip",
    ("eu", "it"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/eu-it.txt.zip",
    (
        "eu",
        "jak",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/eu-jak.txt.zip",
    (
        "eu",
        "jap",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/eu-jap.txt.zip",
    (
        "eu",
        "jiv",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/eu-jiv.txt.zip",
    (
        "eu",
        "kab",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/eu-kab.txt.zip",
    (
        "eu",
        "kbh",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/eu-kbh.txt.zip",
    (
        "eu",
        "kek",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/eu-kek.txt.zip",
    ("eu", "kn"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/eu-kn.txt.zip",
    ("eu", "ko"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/eu-ko.txt.zip",
    ("eu", "la"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/eu-la.txt.zip",
    ("eu", "lt"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/eu-lt.txt.zip",
    ("eu", "lv"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/eu-lv.txt.zip",
    (
        "eu",
        "mam",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/eu-mam.txt.zip",
    ("eu", "mi"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/eu-mi.txt.zip",
    ("eu", "ml"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/eu-ml.txt.zip",
    ("eu", "mr"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/eu-mr.txt.zip",
    ("eu", "my"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/eu-my.txt.zip",
    ("eu", "ne"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/eu-ne.txt.zip",
    (
        "eu",
        "nhg",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/eu-nhg.txt.zip",
    ("eu", "nl"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/eu-nl.txt.zip",
    ("eu", "no"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/eu-no.txt.zip",
    (
        "eu",
        "ojb",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/eu-ojb.txt.zip",
    (
        "eu",
        "pck",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/eu-pck.txt.zip",
    (
        "eu",
        "pes",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/eu-pes.txt.zip",
    ("eu", "pl"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/eu-pl.txt.zip",
    (
        "eu",
        "plt",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/eu-plt.txt.zip",
    (
        "eu",
        "pot",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/eu-pot.txt.zip",
    (
        "eu",
        "ppk",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/eu-ppk.txt.zip",
    ("eu", "pt"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/eu-pt.txt.zip",
    (
        "eu",
        "quc",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/eu-quc.txt.zip",
    (
        "eu",
        "quw",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/eu-quw.txt.zip",
    ("eu", "ro"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/eu-ro.txt.zip",
    (
        "eu",
        "rom",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/eu-rom.txt.zip",
    ("eu", "ru"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/eu-ru.txt.zip",
    (
        "eu",
        "shi",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/eu-shi.txt.zip",
    ("eu", "sk"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/eu-sk.txt.zip",
    ("eu", "sl"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/eu-sl.txt.zip",
    ("eu", "sn"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/eu-sn.txt.zip",
    ("eu", "so"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/eu-so.txt.zip",
    ("eu", "sq"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/eu-sq.txt.zip",
    ("eu", "sr"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/eu-sr.txt.zip",
    ("eu", "ss"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/eu-ss.txt.zip",
    ("eu", "sv"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/eu-sv.txt.zip",
    (
        "eu",
        "syr",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/eu-syr.txt.zip",
    ("eu", "te"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/eu-te.txt.zip",
    ("eu", "th"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/eu-th.txt.zip",
    ("eu", "tl"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/eu-tl.txt.zip",
    (
        "eu",
        "tmh",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/eu-tmh.txt.zip",
    ("eu", "tr"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/eu-tr.txt.zip",
    ("eu", "uk"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/eu-uk.txt.zip",
    (
        "eu",
        "usp",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/eu-usp.txt.zip",
    ("eu", "vi"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/eu-vi.txt.zip",
    (
        "eu",
        "wal",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/eu-wal.txt.zip",
    ("eu", "wo"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/eu-wo.txt.zip",
    ("eu", "xh"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/eu-xh.txt.zip",
    ("eu", "zh"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/eu-zh.txt.zip",
    ("eu", "zu"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/eu-zu.txt.zip",
    ("fi", "fr"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/fi-fr.txt.zip",
    (
        "fi",
        "gbi",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/fi-gbi.txt.zip",
    ("fi", "gd"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/fi-gd.txt.zip",
    ("fi", "gu"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/fi-gu.txt.zip",
    ("fi", "gv"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/fi-gv.txt.zip",
    ("fi", "he"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/fi-he.txt.zip",
    ("fi", "hi"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/fi-hi.txt.zip",
    ("fi", "hr"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/fi-hr.txt.zip",
    ("fi", "hu"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/fi-hu.txt.zip",
    ("fi", "hy"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/fi-hy.txt.zip",
    ("fi", "id"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/fi-id.txt.zip",
    ("fi", "is"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/fi-is.txt.zip",
    ("fi", "it"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/fi-it.txt.zip",
    (
        "fi",
        "jak",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/fi-jak.txt.zip",
    (
        "fi",
        "jap",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/fi-jap.txt.zip",
    (
        "fi",
        "jiv",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/fi-jiv.txt.zip",
    (
        "fi",
        "kab",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/fi-kab.txt.zip",
    (
        "fi",
        "kbh",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/fi-kbh.txt.zip",
    (
        "fi",
        "kek",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/fi-kek.txt.zip",
    ("fi", "kn"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/fi-kn.txt.zip",
    ("fi", "ko"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/fi-ko.txt.zip",
    ("fi", "la"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/fi-la.txt.zip",
    ("fi", "lt"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/fi-lt.txt.zip",
    ("fi", "lv"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/fi-lv.txt.zip",
    (
        "fi",
        "mam",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/fi-mam.txt.zip",
    ("fi", "mi"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/fi-mi.txt.zip",
    ("fi", "ml"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/fi-ml.txt.zip",
    ("fi", "mr"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/fi-mr.txt.zip",
    ("fi", "my"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/fi-my.txt.zip",
    ("fi", "ne"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/fi-ne.txt.zip",
    (
        "fi",
        "nhg",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/fi-nhg.txt.zip",
    ("fi", "nl"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/fi-nl.txt.zip",
    ("fi", "no"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/fi-no.txt.zip",
    (
        "fi",
        "ojb",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/fi-ojb.txt.zip",
    (
        "fi",
        "pck",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/fi-pck.txt.zip",
    (
        "fi",
        "pes",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/fi-pes.txt.zip",
    ("fi", "pl"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/fi-pl.txt.zip",
    (
        "fi",
        "plt",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/fi-plt.txt.zip",
    (
        "fi",
        "pot",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/fi-pot.txt.zip",
    (
        "fi",
        "ppk",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/fi-ppk.txt.zip",
    ("fi", "pt"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/fi-pt.txt.zip",
    (
        "fi",
        "quc",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/fi-quc.txt.zip",
    (
        "fi",
        "quw",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/fi-quw.txt.zip",
    ("fi", "ro"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/fi-ro.txt.zip",
    (
        "fi",
        "rom",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/fi-rom.txt.zip",
    ("fi", "ru"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/fi-ru.txt.zip",
    (
        "fi",
        "shi",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/fi-shi.txt.zip",
    ("fi", "sk"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/fi-sk.txt.zip",
    ("fi", "sl"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/fi-sl.txt.zip",
    ("fi", "sn"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/fi-sn.txt.zip",
    ("fi", "so"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/fi-so.txt.zip",
    ("fi", "sq"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/fi-sq.txt.zip",
    ("fi", "sr"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/fi-sr.txt.zip",
    ("fi", "ss"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/fi-ss.txt.zip",
    ("fi", "sv"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/fi-sv.txt.zip",
    (
        "fi",
        "syr",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/fi-syr.txt.zip",
    ("fi", "te"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/fi-te.txt.zip",
    ("fi", "th"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/fi-th.txt.zip",
    ("fi", "tl"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/fi-tl.txt.zip",
    (
        "fi",
        "tmh",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/fi-tmh.txt.zip",
    ("fi", "tr"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/fi-tr.txt.zip",
    ("fi", "uk"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/fi-uk.txt.zip",
    (
        "fi",
        "usp",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/fi-usp.txt.zip",
    ("fi", "vi"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/fi-vi.txt.zip",
    (
        "fi",
        "wal",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/fi-wal.txt.zip",
    ("fi", "wo"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/fi-wo.txt.zip",
    ("fi", "xh"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/fi-xh.txt.zip",
    ("fi", "zh"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/fi-zh.txt.zip",
    ("fi", "zu"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/fi-zu.txt.zip",
    (
        "fr",
        "gbi",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/fr-gbi.txt.zip",
    ("fr", "gd"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/fr-gd.txt.zip",
    ("fr", "gu"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/fr-gu.txt.zip",
    ("fr", "gv"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/fr-gv.txt.zip",
    ("fr", "he"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/fr-he.txt.zip",
    ("fr", "hi"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/fr-hi.txt.zip",
    ("fr", "hr"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/fr-hr.txt.zip",
    ("fr", "hu"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/fr-hu.txt.zip",
    ("fr", "hy"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/fr-hy.txt.zip",
    ("fr", "id"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/fr-id.txt.zip",
    ("fr", "is"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/fr-is.txt.zip",
    ("fr", "it"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/fr-it.txt.zip",
    (
        "fr",
        "jak",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/fr-jak.txt.zip",
    (
        "fr",
        "jap",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/fr-jap.txt.zip",
    (
        "fr",
        "jiv",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/fr-jiv.txt.zip",
    (
        "fr",
        "kab",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/fr-kab.txt.zip",
    (
        "fr",
        "kbh",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/fr-kbh.txt.zip",
    (
        "fr",
        "kek",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/fr-kek.txt.zip",
    ("fr", "kn"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/fr-kn.txt.zip",
    ("fr", "ko"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/fr-ko.txt.zip",
    ("fr", "la"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/fr-la.txt.zip",
    ("fr", "lt"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/fr-lt.txt.zip",
    ("fr", "lv"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/fr-lv.txt.zip",
    (
        "fr",
        "mam",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/fr-mam.txt.zip",
    ("fr", "mi"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/fr-mi.txt.zip",
    ("fr", "ml"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/fr-ml.txt.zip",
    ("fr", "mr"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/fr-mr.txt.zip",
    ("fr", "my"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/fr-my.txt.zip",
    ("fr", "ne"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/fr-ne.txt.zip",
    (
        "fr",
        "nhg",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/fr-nhg.txt.zip",
    ("fr", "nl"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/fr-nl.txt.zip",
    ("fr", "no"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/fr-no.txt.zip",
    (
        "fr",
        "ojb",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/fr-ojb.txt.zip",
    (
        "fr",
        "pck",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/fr-pck.txt.zip",
    (
        "fr",
        "pes",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/fr-pes.txt.zip",
    ("fr", "pl"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/fr-pl.txt.zip",
    (
        "fr",
        "plt",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/fr-plt.txt.zip",
    (
        "fr",
        "pot",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/fr-pot.txt.zip",
    (
        "fr",
        "ppk",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/fr-ppk.txt.zip",
    ("fr", "pt"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/fr-pt.txt.zip",
    (
        "fr",
        "quc",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/fr-quc.txt.zip",
    (
        "fr",
        "quw",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/fr-quw.txt.zip",
    ("fr", "ro"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/fr-ro.txt.zip",
    (
        "fr",
        "rom",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/fr-rom.txt.zip",
    ("fr", "ru"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/fr-ru.txt.zip",
    (
        "fr",
        "shi",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/fr-shi.txt.zip",
    ("fr", "sk"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/fr-sk.txt.zip",
    ("fr", "sl"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/fr-sl.txt.zip",
    ("fr", "sn"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/fr-sn.txt.zip",
    ("fr", "so"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/fr-so.txt.zip",
    ("fr", "sq"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/fr-sq.txt.zip",
    ("fr", "sr"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/fr-sr.txt.zip",
    ("fr", "ss"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/fr-ss.txt.zip",
    ("fr", "sv"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/fr-sv.txt.zip",
    (
        "fr",
        "syr",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/fr-syr.txt.zip",
    ("fr", "te"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/fr-te.txt.zip",
    ("fr", "th"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/fr-th.txt.zip",
    ("fr", "tl"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/fr-tl.txt.zip",
    (
        "fr",
        "tmh",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/fr-tmh.txt.zip",
    ("fr", "tr"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/fr-tr.txt.zip",
    ("fr", "uk"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/fr-uk.txt.zip",
    (
        "fr",
        "usp",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/fr-usp.txt.zip",
    ("fr", "vi"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/fr-vi.txt.zip",
    (
        "fr",
        "wal",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/fr-wal.txt.zip",
    ("fr", "wo"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/fr-wo.txt.zip",
    ("fr", "xh"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/fr-xh.txt.zip",
    ("fr", "zh"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/fr-zh.txt.zip",
    ("fr", "zu"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/fr-zu.txt.zip",
    (
        "gbi",
        "gd",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/gbi-gd.txt.zip",
    (
        "gbi",
        "gu",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/gbi-gu.txt.zip",
    (
        "gbi",
        "gv",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/gbi-gv.txt.zip",
    (
        "gbi",
        "he",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/gbi-he.txt.zip",
    (
        "gbi",
        "hi",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/gbi-hi.txt.zip",
    (
        "gbi",
        "hr",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/gbi-hr.txt.zip",
    (
        "gbi",
        "hu",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/gbi-hu.txt.zip",
    (
        "gbi",
        "hy",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/gbi-hy.txt.zip",
    (
        "gbi",
        "id",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/gbi-id.txt.zip",
    (
        "gbi",
        "is",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/gbi-is.txt.zip",
    (
        "gbi",
        "it",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/gbi-it.txt.zip",
    (
        "gbi",
        "jak",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/gbi-jak.txt.zip",
    (
        "gbi",
        "jap",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/gbi-jap.txt.zip",
    (
        "gbi",
        "jiv",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/gbi-jiv.txt.zip",
    (
        "gbi",
        "kab",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/gbi-kab.txt.zip",
    (
        "gbi",
        "kbh",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/gbi-kbh.txt.zip",
    (
        "gbi",
        "kek",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/gbi-kek.txt.zip",
    (
        "gbi",
        "kn",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/gbi-kn.txt.zip",
    (
        "gbi",
        "ko",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/gbi-ko.txt.zip",
    (
        "gbi",
        "la",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/gbi-la.txt.zip",
    (
        "gbi",
        "lt",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/gbi-lt.txt.zip",
    (
        "gbi",
        "lv",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/gbi-lv.txt.zip",
    (
        "gbi",
        "mam",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/gbi-mam.txt.zip",
    (
        "gbi",
        "mi",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/gbi-mi.txt.zip",
    (
        "gbi",
        "ml",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/gbi-ml.txt.zip",
    (
        "gbi",
        "mr",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/gbi-mr.txt.zip",
    (
        "gbi",
        "my",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/gbi-my.txt.zip",
    (
        "gbi",
        "ne",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/gbi-ne.txt.zip",
    (
        "gbi",
        "nhg",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/gbi-nhg.txt.zip",
    (
        "gbi",
        "nl",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/gbi-nl.txt.zip",
    (
        "gbi",
        "no",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/gbi-no.txt.zip",
    (
        "gbi",
        "ojb",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/gbi-ojb.txt.zip",
    (
        "gbi",
        "pck",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/gbi-pck.txt.zip",
    (
        "gbi",
        "pes",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/gbi-pes.txt.zip",
    (
        "gbi",
        "pl",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/gbi-pl.txt.zip",
    (
        "gbi",
        "plt",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/gbi-plt.txt.zip",
    (
        "gbi",
        "pot",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/gbi-pot.txt.zip",
    (
        "gbi",
        "ppk",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/gbi-ppk.txt.zip",
    (
        "gbi",
        "pt",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/gbi-pt.txt.zip",
    (
        "gbi",
        "quc",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/gbi-quc.txt.zip",
    (
        "gbi",
        "quw",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/gbi-quw.txt.zip",
    (
        "gbi",
        "ro",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/gbi-ro.txt.zip",
    (
        "gbi",
        "rom",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/gbi-rom.txt.zip",
    (
        "gbi",
        "ru",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/gbi-ru.txt.zip",
    (
        "gbi",
        "shi",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/gbi-shi.txt.zip",
    (
        "gbi",
        "sk",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/gbi-sk.txt.zip",
    (
        "gbi",
        "sl",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/gbi-sl.txt.zip",
    (
        "gbi",
        "sn",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/gbi-sn.txt.zip",
    (
        "gbi",
        "so",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/gbi-so.txt.zip",
    (
        "gbi",
        "sq",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/gbi-sq.txt.zip",
    (
        "gbi",
        "sr",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/gbi-sr.txt.zip",
    (
        "gbi",
        "ss",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/gbi-ss.txt.zip",
    (
        "gbi",
        "sv",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/gbi-sv.txt.zip",
    (
        "gbi",
        "syr",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/gbi-syr.txt.zip",
    (
        "gbi",
        "te",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/gbi-te.txt.zip",
    (
        "gbi",
        "th",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/gbi-th.txt.zip",
    (
        "gbi",
        "tl",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/gbi-tl.txt.zip",
    (
        "gbi",
        "tmh",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/gbi-tmh.txt.zip",
    (
        "gbi",
        "tr",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/gbi-tr.txt.zip",
    (
        "gbi",
        "uk",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/gbi-uk.txt.zip",
    (
        "gbi",
        "usp",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/gbi-usp.txt.zip",
    (
        "gbi",
        "vi",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/gbi-vi.txt.zip",
    (
        "gbi",
        "wal",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/gbi-wal.txt.zip",
    (
        "gbi",
        "wo",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/gbi-wo.txt.zip",
    (
        "gbi",
        "xh",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/gbi-xh.txt.zip",
    (
        "gbi",
        "zh",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/gbi-zh.txt.zip",
    (
        "gbi",
        "zu",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/gbi-zu.txt.zip",
    ("gd", "gu"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/gd-gu.txt.zip",
    ("gd", "gv"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/gd-gv.txt.zip",
    ("gd", "he"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/gd-he.txt.zip",
    ("gd", "hi"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/gd-hi.txt.zip",
    ("gd", "hr"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/gd-hr.txt.zip",
    ("gd", "hu"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/gd-hu.txt.zip",
    ("gd", "hy"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/gd-hy.txt.zip",
    ("gd", "id"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/gd-id.txt.zip",
    ("gd", "is"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/gd-is.txt.zip",
    ("gd", "it"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/gd-it.txt.zip",
    (
        "gd",
        "jak",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/gd-jak.txt.zip",
    (
        "gd",
        "jap",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/gd-jap.txt.zip",
    (
        "gd",
        "jiv",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/gd-jiv.txt.zip",
    (
        "gd",
        "kab",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/gd-kab.txt.zip",
    (
        "gd",
        "kbh",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/gd-kbh.txt.zip",
    (
        "gd",
        "kek",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/gd-kek.txt.zip",
    ("gd", "kn"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/gd-kn.txt.zip",
    ("gd", "ko"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/gd-ko.txt.zip",
    ("gd", "la"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/gd-la.txt.zip",
    ("gd", "lt"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/gd-lt.txt.zip",
    ("gd", "lv"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/gd-lv.txt.zip",
    (
        "gd",
        "mam",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/gd-mam.txt.zip",
    ("gd", "mi"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/gd-mi.txt.zip",
    ("gd", "ml"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/gd-ml.txt.zip",
    ("gd", "mr"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/gd-mr.txt.zip",
    ("gd", "my"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/gd-my.txt.zip",
    ("gd", "ne"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/gd-ne.txt.zip",
    (
        "gd",
        "nhg",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/gd-nhg.txt.zip",
    ("gd", "nl"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/gd-nl.txt.zip",
    ("gd", "no"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/gd-no.txt.zip",
    (
        "gd",
        "ojb",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/gd-ojb.txt.zip",
    (
        "gd",
        "pck",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/gd-pck.txt.zip",
    (
        "gd",
        "pes",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/gd-pes.txt.zip",
    ("gd", "pl"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/gd-pl.txt.zip",
    (
        "gd",
        "plt",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/gd-plt.txt.zip",
    (
        "gd",
        "ppk",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/gd-ppk.txt.zip",
    ("gd", "pt"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/gd-pt.txt.zip",
    (
        "gd",
        "quc",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/gd-quc.txt.zip",
    (
        "gd",
        "quw",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/gd-quw.txt.zip",
    ("gd", "ro"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/gd-ro.txt.zip",
    (
        "gd",
        "rom",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/gd-rom.txt.zip",
    ("gd", "ru"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/gd-ru.txt.zip",
    (
        "gd",
        "shi",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/gd-shi.txt.zip",
    ("gd", "sk"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/gd-sk.txt.zip",
    ("gd", "sl"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/gd-sl.txt.zip",
    ("gd", "sn"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/gd-sn.txt.zip",
    ("gd", "so"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/gd-so.txt.zip",
    ("gd", "sq"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/gd-sq.txt.zip",
    ("gd", "sr"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/gd-sr.txt.zip",
    ("gd", "ss"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/gd-ss.txt.zip",
    ("gd", "sv"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/gd-sv.txt.zip",
    (
        "gd",
        "syr",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/gd-syr.txt.zip",
    ("gd", "te"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/gd-te.txt.zip",
    ("gd", "th"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/gd-th.txt.zip",
    ("gd", "tl"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/gd-tl.txt.zip",
    ("gd", "tr"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/gd-tr.txt.zip",
    ("gd", "uk"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/gd-uk.txt.zip",
    (
        "gd",
        "usp",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/gd-usp.txt.zip",
    ("gd", "vi"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/gd-vi.txt.zip",
    (
        "gd",
        "wal",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/gd-wal.txt.zip",
    ("gd", "wo"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/gd-wo.txt.zip",
    ("gd", "xh"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/gd-xh.txt.zip",
    ("gd", "zh"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/gd-zh.txt.zip",
    ("gd", "zu"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/gd-zu.txt.zip",
    ("gu", "gv"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/gu-gv.txt.zip",
    ("gu", "he"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/gu-he.txt.zip",
    ("gu", "hi"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/gu-hi.txt.zip",
    ("gu", "hr"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/gu-hr.txt.zip",
    ("gu", "hu"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/gu-hu.txt.zip",
    ("gu", "hy"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/gu-hy.txt.zip",
    ("gu", "id"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/gu-id.txt.zip",
    ("gu", "is"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/gu-is.txt.zip",
    ("gu", "it"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/gu-it.txt.zip",
    (
        "gu",
        "jak",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/gu-jak.txt.zip",
    (
        "gu",
        "jap",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/gu-jap.txt.zip",
    (
        "gu",
        "jiv",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/gu-jiv.txt.zip",
    (
        "gu",
        "kab",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/gu-kab.txt.zip",
    (
        "gu",
        "kbh",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/gu-kbh.txt.zip",
    (
        "gu",
        "kek",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/gu-kek.txt.zip",
    ("gu", "kn"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/gu-kn.txt.zip",
    ("gu", "ko"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/gu-ko.txt.zip",
    ("gu", "la"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/gu-la.txt.zip",
    ("gu", "lt"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/gu-lt.txt.zip",
    ("gu", "lv"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/gu-lv.txt.zip",
    (
        "gu",
        "mam",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/gu-mam.txt.zip",
    ("gu", "mi"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/gu-mi.txt.zip",
    ("gu", "ml"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/gu-ml.txt.zip",
    ("gu", "mr"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/gu-mr.txt.zip",
    ("gu", "my"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/gu-my.txt.zip",
    ("gu", "ne"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/gu-ne.txt.zip",
    (
        "gu",
        "nhg",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/gu-nhg.txt.zip",
    ("gu", "nl"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/gu-nl.txt.zip",
    ("gu", "no"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/gu-no.txt.zip",
    (
        "gu",
        "ojb",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/gu-ojb.txt.zip",
    (
        "gu",
        "pck",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/gu-pck.txt.zip",
    (
        "gu",
        "pes",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/gu-pes.txt.zip",
    ("gu", "pl"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/gu-pl.txt.zip",
    (
        "gu",
        "plt",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/gu-plt.txt.zip",
    (
        "gu",
        "pot",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/gu-pot.txt.zip",
    (
        "gu",
        "ppk",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/gu-ppk.txt.zip",
    ("gu", "pt"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/gu-pt.txt.zip",
    (
        "gu",
        "quc",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/gu-quc.txt.zip",
    (
        "gu",
        "quw",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/gu-quw.txt.zip",
    ("gu", "ro"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/gu-ro.txt.zip",
    (
        "gu",
        "rom",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/gu-rom.txt.zip",
    ("gu", "ru"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/gu-ru.txt.zip",
    (
        "gu",
        "shi",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/gu-shi.txt.zip",
    ("gu", "sk"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/gu-sk.txt.zip",
    ("gu", "sl"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/gu-sl.txt.zip",
    ("gu", "sn"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/gu-sn.txt.zip",
    ("gu", "so"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/gu-so.txt.zip",
    ("gu", "sq"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/gu-sq.txt.zip",
    ("gu", "sr"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/gu-sr.txt.zip",
    ("gu", "ss"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/gu-ss.txt.zip",
    ("gu", "sv"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/gu-sv.txt.zip",
    (
        "gu",
        "syr",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/gu-syr.txt.zip",
    ("gu", "te"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/gu-te.txt.zip",
    ("gu", "th"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/gu-th.txt.zip",
    ("gu", "tl"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/gu-tl.txt.zip",
    (
        "gu",
        "tmh",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/gu-tmh.txt.zip",
    ("gu", "tr"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/gu-tr.txt.zip",
    ("gu", "uk"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/gu-uk.txt.zip",
    (
        "gu",
        "usp",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/gu-usp.txt.zip",
    ("gu", "vi"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/gu-vi.txt.zip",
    (
        "gu",
        "wal",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/gu-wal.txt.zip",
    ("gu", "wo"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/gu-wo.txt.zip",
    ("gu", "xh"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/gu-xh.txt.zip",
    ("gu", "zh"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/gu-zh.txt.zip",
    ("gu", "zu"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/gu-zu.txt.zip",
    ("gv", "he"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/gv-he.txt.zip",
    ("gv", "hi"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/gv-hi.txt.zip",
    ("gv", "hr"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/gv-hr.txt.zip",
    ("gv", "hu"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/gv-hu.txt.zip",
    ("gv", "hy"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/gv-hy.txt.zip",
    ("gv", "id"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/gv-id.txt.zip",
    ("gv", "is"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/gv-is.txt.zip",
    ("gv", "it"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/gv-it.txt.zip",
    (
        "gv",
        "jak",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/gv-jak.txt.zip",
    (
        "gv",
        "jap",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/gv-jap.txt.zip",
    (
        "gv",
        "jiv",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/gv-jiv.txt.zip",
    (
        "gv",
        "kab",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/gv-kab.txt.zip",
    (
        "gv",
        "kbh",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/gv-kbh.txt.zip",
    (
        "gv",
        "kek",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/gv-kek.txt.zip",
    ("gv", "kn"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/gv-kn.txt.zip",
    ("gv", "ko"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/gv-ko.txt.zip",
    ("gv", "la"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/gv-la.txt.zip",
    ("gv", "lt"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/gv-lt.txt.zip",
    ("gv", "lv"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/gv-lv.txt.zip",
    (
        "gv",
        "mam",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/gv-mam.txt.zip",
    ("gv", "mi"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/gv-mi.txt.zip",
    ("gv", "ml"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/gv-ml.txt.zip",
    ("gv", "mr"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/gv-mr.txt.zip",
    ("gv", "my"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/gv-my.txt.zip",
    ("gv", "ne"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/gv-ne.txt.zip",
    (
        "gv",
        "nhg",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/gv-nhg.txt.zip",
    ("gv", "nl"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/gv-nl.txt.zip",
    ("gv", "no"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/gv-no.txt.zip",
    (
        "gv",
        "ojb",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/gv-ojb.txt.zip",
    (
        "gv",
        "pck",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/gv-pck.txt.zip",
    (
        "gv",
        "pes",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/gv-pes.txt.zip",
    ("gv", "pl"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/gv-pl.txt.zip",
    (
        "gv",
        "plt",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/gv-plt.txt.zip",
    (
        "gv",
        "pot",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/gv-pot.txt.zip",
    (
        "gv",
        "ppk",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/gv-ppk.txt.zip",
    ("gv", "pt"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/gv-pt.txt.zip",
    (
        "gv",
        "quc",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/gv-quc.txt.zip",
    (
        "gv",
        "quw",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/gv-quw.txt.zip",
    ("gv", "ro"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/gv-ro.txt.zip",
    (
        "gv",
        "rom",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/gv-rom.txt.zip",
    ("gv", "ru"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/gv-ru.txt.zip",
    (
        "gv",
        "shi",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/gv-shi.txt.zip",
    ("gv", "sk"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/gv-sk.txt.zip",
    ("gv", "sl"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/gv-sl.txt.zip",
    ("gv", "sn"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/gv-sn.txt.zip",
    ("gv", "so"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/gv-so.txt.zip",
    ("gv", "sq"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/gv-sq.txt.zip",
    ("gv", "sr"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/gv-sr.txt.zip",
    ("gv", "ss"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/gv-ss.txt.zip",
    ("gv", "sv"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/gv-sv.txt.zip",
    (
        "gv",
        "syr",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/gv-syr.txt.zip",
    ("gv", "te"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/gv-te.txt.zip",
    ("gv", "th"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/gv-th.txt.zip",
    ("gv", "tl"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/gv-tl.txt.zip",
    (
        "gv",
        "tmh",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/gv-tmh.txt.zip",
    ("gv", "tr"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/gv-tr.txt.zip",
    ("gv", "uk"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/gv-uk.txt.zip",
    (
        "gv",
        "usp",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/gv-usp.txt.zip",
    ("gv", "vi"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/gv-vi.txt.zip",
    (
        "gv",
        "wal",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/gv-wal.txt.zip",
    ("gv", "wo"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/gv-wo.txt.zip",
    ("gv", "xh"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/gv-xh.txt.zip",
    ("gv", "zh"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/gv-zh.txt.zip",
    ("gv", "zu"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/gv-zu.txt.zip",
    ("he", "hi"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/he-hi.txt.zip",
    ("he", "hr"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/he-hr.txt.zip",
    ("he", "hu"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/he-hu.txt.zip",
    ("he", "hy"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/he-hy.txt.zip",
    ("he", "id"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/he-id.txt.zip",
    ("he", "is"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/he-is.txt.zip",
    ("he", "it"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/he-it.txt.zip",
    (
        "he",
        "jak",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/he-jak.txt.zip",
    (
        "he",
        "jap",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/he-jap.txt.zip",
    (
        "he",
        "jiv",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/he-jiv.txt.zip",
    (
        "he",
        "kab",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/he-kab.txt.zip",
    (
        "he",
        "kbh",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/he-kbh.txt.zip",
    (
        "he",
        "kek",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/he-kek.txt.zip",
    ("he", "kn"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/he-kn.txt.zip",
    ("he", "ko"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/he-ko.txt.zip",
    ("he", "la"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/he-la.txt.zip",
    ("he", "lt"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/he-lt.txt.zip",
    ("he", "lv"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/he-lv.txt.zip",
    (
        "he",
        "mam",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/he-mam.txt.zip",
    ("he", "mi"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/he-mi.txt.zip",
    ("he", "ml"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/he-ml.txt.zip",
    ("he", "mr"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/he-mr.txt.zip",
    ("he", "my"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/he-my.txt.zip",
    ("he", "ne"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/he-ne.txt.zip",
    (
        "he",
        "nhg",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/he-nhg.txt.zip",
    ("he", "nl"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/he-nl.txt.zip",
    ("he", "no"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/he-no.txt.zip",
    (
        "he",
        "ojb",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/he-ojb.txt.zip",
    (
        "he",
        "pck",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/he-pck.txt.zip",
    (
        "he",
        "pes",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/he-pes.txt.zip",
    ("he", "pl"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/he-pl.txt.zip",
    (
        "he",
        "plt",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/he-plt.txt.zip",
    (
        "he",
        "pot",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/he-pot.txt.zip",
    (
        "he",
        "ppk",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/he-ppk.txt.zip",
    ("he", "pt"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/he-pt.txt.zip",
    (
        "he",
        "quc",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/he-quc.txt.zip",
    (
        "he",
        "quw",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/he-quw.txt.zip",
    ("he", "ro"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/he-ro.txt.zip",
    (
        "he",
        "rom",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/he-rom.txt.zip",
    ("he", "ru"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/he-ru.txt.zip",
    (
        "he",
        "shi",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/he-shi.txt.zip",
    ("he", "sk"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/he-sk.txt.zip",
    ("he", "sl"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/he-sl.txt.zip",
    ("he", "sn"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/he-sn.txt.zip",
    ("he", "so"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/he-so.txt.zip",
    ("he", "sq"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/he-sq.txt.zip",
    ("he", "sr"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/he-sr.txt.zip",
    ("he", "ss"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/he-ss.txt.zip",
    ("he", "sv"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/he-sv.txt.zip",
    (
        "he",
        "syr",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/he-syr.txt.zip",
    ("he", "te"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/he-te.txt.zip",
    ("he", "th"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/he-th.txt.zip",
    ("he", "tl"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/he-tl.txt.zip",
    (
        "he",
        "tmh",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/he-tmh.txt.zip",
    ("he", "tr"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/he-tr.txt.zip",
    ("he", "uk"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/he-uk.txt.zip",
    (
        "he",
        "usp",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/he-usp.txt.zip",
    ("he", "vi"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/he-vi.txt.zip",
    (
        "he",
        "wal",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/he-wal.txt.zip",
    ("he", "wo"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/he-wo.txt.zip",
    ("he", "xh"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/he-xh.txt.zip",
    ("he", "zh"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/he-zh.txt.zip",
    ("he", "zu"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/he-zu.txt.zip",
    ("hi", "hr"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/hi-hr.txt.zip",
    ("hi", "hu"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/hi-hu.txt.zip",
    ("hi", "hy"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/hi-hy.txt.zip",
    ("hi", "id"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/hi-id.txt.zip",
    ("hi", "is"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/hi-is.txt.zip",
    ("hi", "it"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/hi-it.txt.zip",
    (
        "hi",
        "jak",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/hi-jak.txt.zip",
    (
        "hi",
        "jap",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/hi-jap.txt.zip",
    (
        "hi",
        "jiv",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/hi-jiv.txt.zip",
    (
        "hi",
        "kab",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/hi-kab.txt.zip",
    (
        "hi",
        "kbh",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/hi-kbh.txt.zip",
    (
        "hi",
        "kek",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/hi-kek.txt.zip",
    ("hi", "kn"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/hi-kn.txt.zip",
    ("hi", "ko"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/hi-ko.txt.zip",
    ("hi", "la"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/hi-la.txt.zip",
    ("hi", "lt"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/hi-lt.txt.zip",
    ("hi", "lv"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/hi-lv.txt.zip",
    (
        "hi",
        "mam",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/hi-mam.txt.zip",
    ("hi", "mi"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/hi-mi.txt.zip",
    ("hi", "ml"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/hi-ml.txt.zip",
    ("hi", "mr"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/hi-mr.txt.zip",
    ("hi", "my"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/hi-my.txt.zip",
    ("hi", "ne"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/hi-ne.txt.zip",
    (
        "hi",
        "nhg",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/hi-nhg.txt.zip",
    ("hi", "nl"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/hi-nl.txt.zip",
    ("hi", "no"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/hi-no.txt.zip",
    (
        "hi",
        "ojb",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/hi-ojb.txt.zip",
    (
        "hi",
        "pck",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/hi-pck.txt.zip",
    (
        "hi",
        "pes",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/hi-pes.txt.zip",
    ("hi", "pl"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/hi-pl.txt.zip",
    (
        "hi",
        "plt",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/hi-plt.txt.zip",
    (
        "hi",
        "pot",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/hi-pot.txt.zip",
    (
        "hi",
        "ppk",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/hi-ppk.txt.zip",
    ("hi", "pt"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/hi-pt.txt.zip",
    (
        "hi",
        "quc",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/hi-quc.txt.zip",
    (
        "hi",
        "quw",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/hi-quw.txt.zip",
    ("hi", "ro"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/hi-ro.txt.zip",
    (
        "hi",
        "rom",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/hi-rom.txt.zip",
    ("hi", "ru"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/hi-ru.txt.zip",
    (
        "hi",
        "shi",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/hi-shi.txt.zip",
    ("hi", "sk"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/hi-sk.txt.zip",
    ("hi", "sl"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/hi-sl.txt.zip",
    ("hi", "sn"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/hi-sn.txt.zip",
    ("hi", "so"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/hi-so.txt.zip",
    ("hi", "sq"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/hi-sq.txt.zip",
    ("hi", "sr"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/hi-sr.txt.zip",
    ("hi", "ss"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/hi-ss.txt.zip",
    ("hi", "sv"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/hi-sv.txt.zip",
    (
        "hi",
        "syr",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/hi-syr.txt.zip",
    ("hi", "te"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/hi-te.txt.zip",
    ("hi", "th"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/hi-th.txt.zip",
    ("hi", "tl"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/hi-tl.txt.zip",
    (
        "hi",
        "tmh",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/hi-tmh.txt.zip",
    ("hi", "tr"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/hi-tr.txt.zip",
    ("hi", "uk"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/hi-uk.txt.zip",
    (
        "hi",
        "usp",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/hi-usp.txt.zip",
    ("hi", "vi"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/hi-vi.txt.zip",
    (
        "hi",
        "wal",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/hi-wal.txt.zip",
    ("hi", "wo"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/hi-wo.txt.zip",
    ("hi", "xh"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/hi-xh.txt.zip",
    ("hi", "zh"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/hi-zh.txt.zip",
    ("hi", "zu"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/hi-zu.txt.zip",
    ("hr", "hu"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/hr-hu.txt.zip",
    ("hr", "hy"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/hr-hy.txt.zip",
    ("hr", "id"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/hr-id.txt.zip",
    ("hr", "is"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/hr-is.txt.zip",
    ("hr", "it"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/hr-it.txt.zip",
    (
        "hr",
        "jak",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/hr-jak.txt.zip",
    (
        "hr",
        "jap",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/hr-jap.txt.zip",
    (
        "hr",
        "jiv",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/hr-jiv.txt.zip",
    (
        "hr",
        "kab",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/hr-kab.txt.zip",
    (
        "hr",
        "kbh",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/hr-kbh.txt.zip",
    (
        "hr",
        "kek",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/hr-kek.txt.zip",
    ("hr", "kn"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/hr-kn.txt.zip",
    ("hr", "ko"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/hr-ko.txt.zip",
    ("hr", "la"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/hr-la.txt.zip",
    ("hr", "lt"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/hr-lt.txt.zip",
    ("hr", "lv"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/hr-lv.txt.zip",
    (
        "hr",
        "mam",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/hr-mam.txt.zip",
    ("hr", "mi"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/hr-mi.txt.zip",
    ("hr", "ml"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/hr-ml.txt.zip",
    ("hr", "mr"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/hr-mr.txt.zip",
    ("hr", "my"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/hr-my.txt.zip",
    ("hr", "ne"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/hr-ne.txt.zip",
    (
        "hr",
        "nhg",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/hr-nhg.txt.zip",
    ("hr", "nl"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/hr-nl.txt.zip",
    ("hr", "no"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/hr-no.txt.zip",
    (
        "hr",
        "ojb",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/hr-ojb.txt.zip",
    (
        "hr",
        "pck",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/hr-pck.txt.zip",
    (
        "hr",
        "pes",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/hr-pes.txt.zip",
    ("hr", "pl"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/hr-pl.txt.zip",
    (
        "hr",
        "plt",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/hr-plt.txt.zip",
    (
        "hr",
        "pot",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/hr-pot.txt.zip",
    (
        "hr",
        "ppk",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/hr-ppk.txt.zip",
    ("hr", "pt"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/hr-pt.txt.zip",
    (
        "hr",
        "quc",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/hr-quc.txt.zip",
    (
        "hr",
        "quw",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/hr-quw.txt.zip",
    ("hr", "ro"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/hr-ro.txt.zip",
    (
        "hr",
        "rom",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/hr-rom.txt.zip",
    ("hr", "ru"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/hr-ru.txt.zip",
    (
        "hr",
        "shi",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/hr-shi.txt.zip",
    ("hr", "sk"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/hr-sk.txt.zip",
    ("hr", "sl"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/hr-sl.txt.zip",
    ("hr", "sn"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/hr-sn.txt.zip",
    ("hr", "so"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/hr-so.txt.zip",
    ("hr", "sq"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/hr-sq.txt.zip",
    ("hr", "sr"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/hr-sr.txt.zip",
    ("hr", "ss"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/hr-ss.txt.zip",
    ("hr", "sv"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/hr-sv.txt.zip",
    (
        "hr",
        "syr",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/hr-syr.txt.zip",
    ("hr", "te"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/hr-te.txt.zip",
    ("hr", "th"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/hr-th.txt.zip",
    ("hr", "tl"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/hr-tl.txt.zip",
    (
        "hr",
        "tmh",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/hr-tmh.txt.zip",
    ("hr", "tr"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/hr-tr.txt.zip",
    ("hr", "uk"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/hr-uk.txt.zip",
    (
        "hr",
        "usp",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/hr-usp.txt.zip",
    ("hr", "vi"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/hr-vi.txt.zip",
    (
        "hr",
        "wal",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/hr-wal.txt.zip",
    ("hr", "wo"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/hr-wo.txt.zip",
    ("hr", "xh"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/hr-xh.txt.zip",
    ("hr", "zh"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/hr-zh.txt.zip",
    ("hr", "zu"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/hr-zu.txt.zip",
    ("hu", "hy"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/hu-hy.txt.zip",
    ("hu", "id"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/hu-id.txt.zip",
    ("hu", "is"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/hu-is.txt.zip",
    ("hu", "it"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/hu-it.txt.zip",
    (
        "hu",
        "jak",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/hu-jak.txt.zip",
    (
        "hu",
        "jap",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/hu-jap.txt.zip",
    (
        "hu",
        "jiv",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/hu-jiv.txt.zip",
    (
        "hu",
        "kab",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/hu-kab.txt.zip",
    (
        "hu",
        "kbh",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/hu-kbh.txt.zip",
    (
        "hu",
        "kek",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/hu-kek.txt.zip",
    ("hu", "kn"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/hu-kn.txt.zip",
    ("hu", "ko"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/hu-ko.txt.zip",
    ("hu", "la"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/hu-la.txt.zip",
    ("hu", "lt"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/hu-lt.txt.zip",
    ("hu", "lv"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/hu-lv.txt.zip",
    (
        "hu",
        "mam",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/hu-mam.txt.zip",
    ("hu", "mi"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/hu-mi.txt.zip",
    ("hu", "ml"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/hu-ml.txt.zip",
    ("hu", "mr"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/hu-mr.txt.zip",
    ("hu", "my"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/hu-my.txt.zip",
    ("hu", "ne"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/hu-ne.txt.zip",
    (
        "hu",
        "nhg",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/hu-nhg.txt.zip",
    ("hu", "nl"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/hu-nl.txt.zip",
    ("hu", "no"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/hu-no.txt.zip",
    (
        "hu",
        "ojb",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/hu-ojb.txt.zip",
    (
        "hu",
        "pck",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/hu-pck.txt.zip",
    (
        "hu",
        "pes",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/hu-pes.txt.zip",
    ("hu", "pl"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/hu-pl.txt.zip",
    (
        "hu",
        "plt",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/hu-plt.txt.zip",
    (
        "hu",
        "pot",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/hu-pot.txt.zip",
    (
        "hu",
        "ppk",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/hu-ppk.txt.zip",
    ("hu", "pt"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/hu-pt.txt.zip",
    (
        "hu",
        "quc",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/hu-quc.txt.zip",
    (
        "hu",
        "quw",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/hu-quw.txt.zip",
    ("hu", "ro"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/hu-ro.txt.zip",
    (
        "hu",
        "rom",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/hu-rom.txt.zip",
    ("hu", "ru"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/hu-ru.txt.zip",
    (
        "hu",
        "shi",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/hu-shi.txt.zip",
    ("hu", "sk"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/hu-sk.txt.zip",
    ("hu", "sl"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/hu-sl.txt.zip",
    ("hu", "sn"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/hu-sn.txt.zip",
    ("hu", "so"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/hu-so.txt.zip",
    ("hu", "sq"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/hu-sq.txt.zip",
    ("hu", "sr"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/hu-sr.txt.zip",
    ("hu", "ss"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/hu-ss.txt.zip",
    ("hu", "sv"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/hu-sv.txt.zip",
    (
        "hu",
        "syr",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/hu-syr.txt.zip",
    ("hu", "te"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/hu-te.txt.zip",
    ("hu", "th"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/hu-th.txt.zip",
    ("hu", "tl"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/hu-tl.txt.zip",
    (
        "hu",
        "tmh",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/hu-tmh.txt.zip",
    ("hu", "tr"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/hu-tr.txt.zip",
    ("hu", "uk"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/hu-uk.txt.zip",
    (
        "hu",
        "usp",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/hu-usp.txt.zip",
    ("hu", "vi"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/hu-vi.txt.zip",
    (
        "hu",
        "wal",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/hu-wal.txt.zip",
    ("hu", "wo"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/hu-wo.txt.zip",
    ("hu", "xh"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/hu-xh.txt.zip",
    ("hu", "zh"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/hu-zh.txt.zip",
    ("hu", "zu"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/hu-zu.txt.zip",
    ("hy", "id"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/hy-id.txt.zip",
    ("hy", "is"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/hy-is.txt.zip",
    ("hy", "it"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/hy-it.txt.zip",
    (
        "hy",
        "jak",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/hy-jak.txt.zip",
    (
        "hy",
        "jap",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/hy-jap.txt.zip",
    (
        "hy",
        "jiv",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/hy-jiv.txt.zip",
    (
        "hy",
        "kab",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/hy-kab.txt.zip",
    (
        "hy",
        "kbh",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/hy-kbh.txt.zip",
    (
        "hy",
        "kek",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/hy-kek.txt.zip",
    ("hy", "kn"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/hy-kn.txt.zip",
    ("hy", "ko"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/hy-ko.txt.zip",
    ("hy", "la"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/hy-la.txt.zip",
    ("hy", "lt"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/hy-lt.txt.zip",
    ("hy", "lv"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/hy-lv.txt.zip",
    (
        "hy",
        "mam",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/hy-mam.txt.zip",
    ("hy", "mi"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/hy-mi.txt.zip",
    ("hy", "ml"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/hy-ml.txt.zip",
    ("hy", "mr"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/hy-mr.txt.zip",
    ("hy", "my"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/hy-my.txt.zip",
    ("hy", "ne"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/hy-ne.txt.zip",
    (
        "hy",
        "nhg",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/hy-nhg.txt.zip",
    ("hy", "nl"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/hy-nl.txt.zip",
    ("hy", "no"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/hy-no.txt.zip",
    (
        "hy",
        "ojb",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/hy-ojb.txt.zip",
    (
        "hy",
        "pck",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/hy-pck.txt.zip",
    (
        "hy",
        "pes",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/hy-pes.txt.zip",
    ("hy", "pl"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/hy-pl.txt.zip",
    (
        "hy",
        "plt",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/hy-plt.txt.zip",
    (
        "hy",
        "pot",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/hy-pot.txt.zip",
    (
        "hy",
        "ppk",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/hy-ppk.txt.zip",
    ("hy", "pt"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/hy-pt.txt.zip",
    (
        "hy",
        "quc",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/hy-quc.txt.zip",
    (
        "hy",
        "quw",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/hy-quw.txt.zip",
    ("hy", "ro"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/hy-ro.txt.zip",
    (
        "hy",
        "rom",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/hy-rom.txt.zip",
    ("hy", "ru"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/hy-ru.txt.zip",
    (
        "hy",
        "shi",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/hy-shi.txt.zip",
    ("hy", "sk"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/hy-sk.txt.zip",
    ("hy", "sl"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/hy-sl.txt.zip",
    ("hy", "sn"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/hy-sn.txt.zip",
    ("hy", "so"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/hy-so.txt.zip",
    ("hy", "sq"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/hy-sq.txt.zip",
    ("hy", "sr"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/hy-sr.txt.zip",
    ("hy", "ss"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/hy-ss.txt.zip",
    ("hy", "sv"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/hy-sv.txt.zip",
    (
        "hy",
        "syr",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/hy-syr.txt.zip",
    ("hy", "te"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/hy-te.txt.zip",
    ("hy", "th"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/hy-th.txt.zip",
    ("hy", "tl"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/hy-tl.txt.zip",
    (
        "hy",
        "tmh",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/hy-tmh.txt.zip",
    ("hy", "tr"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/hy-tr.txt.zip",
    ("hy", "uk"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/hy-uk.txt.zip",
    (
        "hy",
        "usp",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/hy-usp.txt.zip",
    ("hy", "vi"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/hy-vi.txt.zip",
    (
        "hy",
        "wal",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/hy-wal.txt.zip",
    ("hy", "wo"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/hy-wo.txt.zip",
    ("hy", "xh"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/hy-xh.txt.zip",
    ("hy", "zh"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/hy-zh.txt.zip",
    ("hy", "zu"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/hy-zu.txt.zip",
    ("id", "is"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/id-is.txt.zip",
    ("id", "it"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/id-it.txt.zip",
    (
        "id",
        "jak",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/id-jak.txt.zip",
    (
        "id",
        "jap",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/id-jap.txt.zip",
    (
        "id",
        "jiv",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/id-jiv.txt.zip",
    (
        "id",
        "kab",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/id-kab.txt.zip",
    (
        "id",
        "kbh",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/id-kbh.txt.zip",
    (
        "id",
        "kek",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/id-kek.txt.zip",
    ("id", "kn"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/id-kn.txt.zip",
    ("id", "ko"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/id-ko.txt.zip",
    ("id", "la"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/id-la.txt.zip",
    ("id", "lt"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/id-lt.txt.zip",
    ("id", "lv"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/id-lv.txt.zip",
    (
        "id",
        "mam",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/id-mam.txt.zip",
    ("id", "mi"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/id-mi.txt.zip",
    ("id", "ml"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/id-ml.txt.zip",
    ("id", "mr"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/id-mr.txt.zip",
    ("id", "my"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/id-my.txt.zip",
    ("id", "ne"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/id-ne.txt.zip",
    (
        "id",
        "nhg",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/id-nhg.txt.zip",
    ("id", "nl"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/id-nl.txt.zip",
    ("id", "no"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/id-no.txt.zip",
    (
        "id",
        "ojb",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/id-ojb.txt.zip",
    (
        "id",
        "pck",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/id-pck.txt.zip",
    (
        "id",
        "pes",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/id-pes.txt.zip",
    ("id", "pl"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/id-pl.txt.zip",
    (
        "id",
        "plt",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/id-plt.txt.zip",
    (
        "id",
        "pot",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/id-pot.txt.zip",
    (
        "id",
        "ppk",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/id-ppk.txt.zip",
    ("id", "pt"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/id-pt.txt.zip",
    (
        "id",
        "quc",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/id-quc.txt.zip",
    (
        "id",
        "quw",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/id-quw.txt.zip",
    ("id", "ro"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/id-ro.txt.zip",
    (
        "id",
        "rom",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/id-rom.txt.zip",
    ("id", "ru"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/id-ru.txt.zip",
    (
        "id",
        "shi",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/id-shi.txt.zip",
    ("id", "sk"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/id-sk.txt.zip",
    ("id", "sl"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/id-sl.txt.zip",
    ("id", "sn"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/id-sn.txt.zip",
    ("id", "so"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/id-so.txt.zip",
    ("id", "sq"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/id-sq.txt.zip",
    ("id", "sr"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/id-sr.txt.zip",
    ("id", "ss"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/id-ss.txt.zip",
    ("id", "sv"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/id-sv.txt.zip",
    (
        "id",
        "syr",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/id-syr.txt.zip",
    ("id", "te"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/id-te.txt.zip",
    ("id", "th"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/id-th.txt.zip",
    ("id", "tl"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/id-tl.txt.zip",
    (
        "id",
        "tmh",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/id-tmh.txt.zip",
    ("id", "tr"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/id-tr.txt.zip",
    ("id", "uk"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/id-uk.txt.zip",
    (
        "id",
        "usp",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/id-usp.txt.zip",
    ("id", "vi"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/id-vi.txt.zip",
    (
        "id",
        "wal",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/id-wal.txt.zip",
    ("id", "wo"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/id-wo.txt.zip",
    ("id", "xh"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/id-xh.txt.zip",
    ("id", "zh"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/id-zh.txt.zip",
    ("id", "zu"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/id-zu.txt.zip",
    ("is", "it"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/is-it.txt.zip",
    (
        "is",
        "jak",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/is-jak.txt.zip",
    (
        "is",
        "jap",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/is-jap.txt.zip",
    (
        "is",
        "jiv",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/is-jiv.txt.zip",
    (
        "is",
        "kab",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/is-kab.txt.zip",
    (
        "is",
        "kbh",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/is-kbh.txt.zip",
    (
        "is",
        "kek",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/is-kek.txt.zip",
    ("is", "kn"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/is-kn.txt.zip",
    ("is", "ko"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/is-ko.txt.zip",
    ("is", "la"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/is-la.txt.zip",
    ("is", "lt"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/is-lt.txt.zip",
    ("is", "lv"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/is-lv.txt.zip",
    (
        "is",
        "mam",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/is-mam.txt.zip",
    ("is", "mi"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/is-mi.txt.zip",
    ("is", "ml"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/is-ml.txt.zip",
    ("is", "mr"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/is-mr.txt.zip",
    ("is", "my"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/is-my.txt.zip",
    ("is", "ne"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/is-ne.txt.zip",
    (
        "is",
        "nhg",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/is-nhg.txt.zip",
    ("is", "nl"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/is-nl.txt.zip",
    ("is", "no"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/is-no.txt.zip",
    (
        "is",
        "ojb",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/is-ojb.txt.zip",
    (
        "is",
        "pck",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/is-pck.txt.zip",
    (
        "is",
        "pes",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/is-pes.txt.zip",
    ("is", "pl"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/is-pl.txt.zip",
    (
        "is",
        "plt",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/is-plt.txt.zip",
    (
        "is",
        "pot",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/is-pot.txt.zip",
    (
        "is",
        "ppk",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/is-ppk.txt.zip",
    ("is", "pt"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/is-pt.txt.zip",
    (
        "is",
        "quc",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/is-quc.txt.zip",
    (
        "is",
        "quw",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/is-quw.txt.zip",
    ("is", "ro"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/is-ro.txt.zip",
    (
        "is",
        "rom",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/is-rom.txt.zip",
    ("is", "ru"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/is-ru.txt.zip",
    (
        "is",
        "shi",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/is-shi.txt.zip",
    ("is", "sk"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/is-sk.txt.zip",
    ("is", "sl"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/is-sl.txt.zip",
    ("is", "sn"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/is-sn.txt.zip",
    ("is", "so"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/is-so.txt.zip",
    ("is", "sq"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/is-sq.txt.zip",
    ("is", "sr"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/is-sr.txt.zip",
    ("is", "ss"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/is-ss.txt.zip",
    ("is", "sv"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/is-sv.txt.zip",
    (
        "is",
        "syr",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/is-syr.txt.zip",
    ("is", "te"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/is-te.txt.zip",
    ("is", "th"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/is-th.txt.zip",
    ("is", "tl"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/is-tl.txt.zip",
    (
        "is",
        "tmh",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/is-tmh.txt.zip",
    ("is", "tr"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/is-tr.txt.zip",
    ("is", "uk"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/is-uk.txt.zip",
    (
        "is",
        "usp",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/is-usp.txt.zip",
    ("is", "vi"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/is-vi.txt.zip",
    (
        "is",
        "wal",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/is-wal.txt.zip",
    ("is", "wo"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/is-wo.txt.zip",
    ("is", "xh"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/is-xh.txt.zip",
    ("is", "zh"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/is-zh.txt.zip",
    ("is", "zu"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/is-zu.txt.zip",
    (
        "it",
        "jak",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/it-jak.txt.zip",
    (
        "it",
        "jap",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/it-jap.txt.zip",
    (
        "it",
        "jiv",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/it-jiv.txt.zip",
    (
        "it",
        "kab",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/it-kab.txt.zip",
    (
        "it",
        "kbh",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/it-kbh.txt.zip",
    (
        "it",
        "kek",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/it-kek.txt.zip",
    ("it", "kn"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/it-kn.txt.zip",
    ("it", "ko"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/it-ko.txt.zip",
    ("it", "la"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/it-la.txt.zip",
    ("it", "lt"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/it-lt.txt.zip",
    ("it", "lv"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/it-lv.txt.zip",
    (
        "it",
        "mam",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/it-mam.txt.zip",
    ("it", "mi"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/it-mi.txt.zip",
    ("it", "ml"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/it-ml.txt.zip",
    ("it", "mr"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/it-mr.txt.zip",
    ("it", "my"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/it-my.txt.zip",
    ("it", "ne"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/it-ne.txt.zip",
    (
        "it",
        "nhg",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/it-nhg.txt.zip",
    ("it", "nl"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/it-nl.txt.zip",
    ("it", "no"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/it-no.txt.zip",
    (
        "it",
        "ojb",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/it-ojb.txt.zip",
    (
        "it",
        "pck",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/it-pck.txt.zip",
    (
        "it",
        "pes",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/it-pes.txt.zip",
    ("it", "pl"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/it-pl.txt.zip",
    (
        "it",
        "plt",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/it-plt.txt.zip",
    (
        "it",
        "pot",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/it-pot.txt.zip",
    (
        "it",
        "ppk",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/it-ppk.txt.zip",
    ("it", "pt"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/it-pt.txt.zip",
    (
        "it",
        "quc",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/it-quc.txt.zip",
    (
        "it",
        "quw",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/it-quw.txt.zip",
    ("it", "ro"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/it-ro.txt.zip",
    (
        "it",
        "rom",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/it-rom.txt.zip",
    ("it", "ru"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/it-ru.txt.zip",
    (
        "it",
        "shi",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/it-shi.txt.zip",
    ("it", "sk"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/it-sk.txt.zip",
    ("it", "sl"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/it-sl.txt.zip",
    ("it", "sn"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/it-sn.txt.zip",
    ("it", "so"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/it-so.txt.zip",
    ("it", "sq"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/it-sq.txt.zip",
    ("it", "sr"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/it-sr.txt.zip",
    ("it", "ss"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/it-ss.txt.zip",
    ("it", "sv"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/it-sv.txt.zip",
    (
        "it",
        "syr",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/it-syr.txt.zip",
    ("it", "te"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/it-te.txt.zip",
    ("it", "th"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/it-th.txt.zip",
    ("it", "tl"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/it-tl.txt.zip",
    (
        "it",
        "tmh",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/it-tmh.txt.zip",
    ("it", "tr"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/it-tr.txt.zip",
    ("it", "uk"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/it-uk.txt.zip",
    (
        "it",
        "usp",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/it-usp.txt.zip",
    ("it", "vi"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/it-vi.txt.zip",
    (
        "it",
        "wal",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/it-wal.txt.zip",
    ("it", "wo"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/it-wo.txt.zip",
    ("it", "xh"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/it-xh.txt.zip",
    ("it", "zh"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/it-zh.txt.zip",
    ("it", "zu"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/it-zu.txt.zip",
    (
        "jak",
        "jap",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/jak-jap.txt.zip",
    (
        "jak",
        "jiv",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/jak-jiv.txt.zip",
    (
        "jak",
        "kab",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/jak-kab.txt.zip",
    (
        "jak",
        "kbh",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/jak-kbh.txt.zip",
    (
        "jak",
        "kek",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/jak-kek.txt.zip",
    (
        "jak",
        "kn",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/jak-kn.txt.zip",
    (
        "jak",
        "ko",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/jak-ko.txt.zip",
    (
        "jak",
        "la",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/jak-la.txt.zip",
    (
        "jak",
        "lt",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/jak-lt.txt.zip",
    (
        "jak",
        "lv",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/jak-lv.txt.zip",
    (
        "jak",
        "mam",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/jak-mam.txt.zip",
    (
        "jak",
        "mi",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/jak-mi.txt.zip",
    (
        "jak",
        "ml",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/jak-ml.txt.zip",
    (
        "jak",
        "mr",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/jak-mr.txt.zip",
    (
        "jak",
        "my",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/jak-my.txt.zip",
    (
        "jak",
        "ne",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/jak-ne.txt.zip",
    (
        "jak",
        "nhg",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/jak-nhg.txt.zip",
    (
        "jak",
        "nl",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/jak-nl.txt.zip",
    (
        "jak",
        "no",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/jak-no.txt.zip",
    (
        "jak",
        "ojb",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/jak-ojb.txt.zip",
    (
        "jak",
        "pck",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/jak-pck.txt.zip",
    (
        "jak",
        "pes",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/jak-pes.txt.zip",
    (
        "jak",
        "pl",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/jak-pl.txt.zip",
    (
        "jak",
        "plt",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/jak-plt.txt.zip",
    (
        "jak",
        "pot",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/jak-pot.txt.zip",
    (
        "jak",
        "ppk",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/jak-ppk.txt.zip",
    (
        "jak",
        "pt",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/jak-pt.txt.zip",
    (
        "jak",
        "quc",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/jak-quc.txt.zip",
    (
        "jak",
        "quw",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/jak-quw.txt.zip",
    (
        "jak",
        "ro",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/jak-ro.txt.zip",
    (
        "jak",
        "rom",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/jak-rom.txt.zip",
    (
        "jak",
        "ru",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/jak-ru.txt.zip",
    (
        "jak",
        "shi",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/jak-shi.txt.zip",
    (
        "jak",
        "sk",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/jak-sk.txt.zip",
    (
        "jak",
        "sl",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/jak-sl.txt.zip",
    (
        "jak",
        "sn",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/jak-sn.txt.zip",
    (
        "jak",
        "so",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/jak-so.txt.zip",
    (
        "jak",
        "sq",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/jak-sq.txt.zip",
    (
        "jak",
        "sr",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/jak-sr.txt.zip",
    (
        "jak",
        "ss",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/jak-ss.txt.zip",
    (
        "jak",
        "sv",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/jak-sv.txt.zip",
    (
        "jak",
        "syr",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/jak-syr.txt.zip",
    (
        "jak",
        "te",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/jak-te.txt.zip",
    (
        "jak",
        "th",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/jak-th.txt.zip",
    (
        "jak",
        "tl",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/jak-tl.txt.zip",
    (
        "jak",
        "tmh",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/jak-tmh.txt.zip",
    (
        "jak",
        "tr",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/jak-tr.txt.zip",
    (
        "jak",
        "uk",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/jak-uk.txt.zip",
    (
        "jak",
        "usp",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/jak-usp.txt.zip",
    (
        "jak",
        "vi",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/jak-vi.txt.zip",
    (
        "jak",
        "wal",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/jak-wal.txt.zip",
    (
        "jak",
        "wo",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/jak-wo.txt.zip",
    (
        "jak",
        "xh",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/jak-xh.txt.zip",
    (
        "jak",
        "zh",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/jak-zh.txt.zip",
    (
        "jak",
        "zu",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/jak-zu.txt.zip",
    (
        "jap",
        "jiv",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/jap-jiv.txt.zip",
    (
        "jap",
        "kab",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/jap-kab.txt.zip",
    (
        "jap",
        "kbh",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/jap-kbh.txt.zip",
    (
        "jap",
        "kek",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/jap-kek.txt.zip",
    (
        "jap",
        "kn",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/jap-kn.txt.zip",
    (
        "jap",
        "ko",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/jap-ko.txt.zip",
    (
        "jap",
        "la",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/jap-la.txt.zip",
    (
        "jap",
        "lt",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/jap-lt.txt.zip",
    (
        "jap",
        "lv",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/jap-lv.txt.zip",
    (
        "jap",
        "mam",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/jap-mam.txt.zip",
    (
        "jap",
        "mi",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/jap-mi.txt.zip",
    (
        "jap",
        "ml",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/jap-ml.txt.zip",
    (
        "jap",
        "mr",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/jap-mr.txt.zip",
    (
        "jap",
        "my",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/jap-my.txt.zip",
    (
        "jap",
        "ne",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/jap-ne.txt.zip",
    (
        "jap",
        "nhg",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/jap-nhg.txt.zip",
    (
        "jap",
        "nl",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/jap-nl.txt.zip",
    (
        "jap",
        "no",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/jap-no.txt.zip",
    (
        "jap",
        "ojb",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/jap-ojb.txt.zip",
    (
        "jap",
        "pck",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/jap-pck.txt.zip",
    (
        "jap",
        "pes",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/jap-pes.txt.zip",
    (
        "jap",
        "pl",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/jap-pl.txt.zip",
    (
        "jap",
        "plt",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/jap-plt.txt.zip",
    (
        "jap",
        "pot",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/jap-pot.txt.zip",
    (
        "jap",
        "ppk",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/jap-ppk.txt.zip",
    (
        "jap",
        "pt",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/jap-pt.txt.zip",
    (
        "jap",
        "quc",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/jap-quc.txt.zip",
    (
        "jap",
        "quw",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/jap-quw.txt.zip",
    (
        "jap",
        "ro",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/jap-ro.txt.zip",
    (
        "jap",
        "rom",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/jap-rom.txt.zip",
    (
        "jap",
        "ru",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/jap-ru.txt.zip",
    (
        "jap",
        "shi",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/jap-shi.txt.zip",
    (
        "jap",
        "sk",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/jap-sk.txt.zip",
    (
        "jap",
        "sl",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/jap-sl.txt.zip",
    (
        "jap",
        "sn",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/jap-sn.txt.zip",
    (
        "jap",
        "so",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/jap-so.txt.zip",
    (
        "jap",
        "sq",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/jap-sq.txt.zip",
    (
        "jap",
        "sr",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/jap-sr.txt.zip",
    (
        "jap",
        "ss",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/jap-ss.txt.zip",
    (
        "jap",
        "sv",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/jap-sv.txt.zip",
    (
        "jap",
        "syr",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/jap-syr.txt.zip",
    (
        "jap",
        "te",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/jap-te.txt.zip",
    (
        "jap",
        "th",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/jap-th.txt.zip",
    (
        "jap",
        "tl",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/jap-tl.txt.zip",
    (
        "jap",
        "tmh",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/jap-tmh.txt.zip",
    (
        "jap",
        "tr",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/jap-tr.txt.zip",
    (
        "jap",
        "uk",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/jap-uk.txt.zip",
    (
        "jap",
        "usp",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/jap-usp.txt.zip",
    (
        "jap",
        "vi",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/jap-vi.txt.zip",
    (
        "jap",
        "wal",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/jap-wal.txt.zip",
    (
        "jap",
        "wo",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/jap-wo.txt.zip",
    (
        "jap",
        "xh",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/jap-xh.txt.zip",
    (
        "jap",
        "zh",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/jap-zh.txt.zip",
    (
        "jap",
        "zu",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/jap-zu.txt.zip",
    (
        "jiv",
        "kab",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/jiv-kab.txt.zip",
    (
        "jiv",
        "kbh",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/jiv-kbh.txt.zip",
    (
        "jiv",
        "kek",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/jiv-kek.txt.zip",
    (
        "jiv",
        "kn",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/jiv-kn.txt.zip",
    (
        "jiv",
        "ko",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/jiv-ko.txt.zip",
    (
        "jiv",
        "la",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/jiv-la.txt.zip",
    (
        "jiv",
        "lt",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/jiv-lt.txt.zip",
    (
        "jiv",
        "lv",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/jiv-lv.txt.zip",
    (
        "jiv",
        "mam",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/jiv-mam.txt.zip",
    (
        "jiv",
        "mi",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/jiv-mi.txt.zip",
    (
        "jiv",
        "ml",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/jiv-ml.txt.zip",
    (
        "jiv",
        "mr",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/jiv-mr.txt.zip",
    (
        "jiv",
        "my",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/jiv-my.txt.zip",
    (
        "jiv",
        "ne",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/jiv-ne.txt.zip",
    (
        "jiv",
        "nhg",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/jiv-nhg.txt.zip",
    (
        "jiv",
        "nl",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/jiv-nl.txt.zip",
    (
        "jiv",
        "no",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/jiv-no.txt.zip",
    (
        "jiv",
        "ojb",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/jiv-ojb.txt.zip",
    (
        "jiv",
        "pck",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/jiv-pck.txt.zip",
    (
        "jiv",
        "pes",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/jiv-pes.txt.zip",
    (
        "jiv",
        "pl",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/jiv-pl.txt.zip",
    (
        "jiv",
        "plt",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/jiv-plt.txt.zip",
    (
        "jiv",
        "pot",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/jiv-pot.txt.zip",
    (
        "jiv",
        "ppk",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/jiv-ppk.txt.zip",
    (
        "jiv",
        "pt",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/jiv-pt.txt.zip",
    (
        "jiv",
        "quc",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/jiv-quc.txt.zip",
    (
        "jiv",
        "quw",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/jiv-quw.txt.zip",
    (
        "jiv",
        "ro",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/jiv-ro.txt.zip",
    (
        "jiv",
        "rom",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/jiv-rom.txt.zip",
    (
        "jiv",
        "ru",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/jiv-ru.txt.zip",
    (
        "jiv",
        "shi",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/jiv-shi.txt.zip",
    (
        "jiv",
        "sk",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/jiv-sk.txt.zip",
    (
        "jiv",
        "sl",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/jiv-sl.txt.zip",
    (
        "jiv",
        "sn",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/jiv-sn.txt.zip",
    (
        "jiv",
        "so",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/jiv-so.txt.zip",
    (
        "jiv",
        "sq",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/jiv-sq.txt.zip",
    (
        "jiv",
        "sr",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/jiv-sr.txt.zip",
    (
        "jiv",
        "ss",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/jiv-ss.txt.zip",
    (
        "jiv",
        "sv",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/jiv-sv.txt.zip",
    (
        "jiv",
        "syr",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/jiv-syr.txt.zip",
    (
        "jiv",
        "te",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/jiv-te.txt.zip",
    (
        "jiv",
        "th",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/jiv-th.txt.zip",
    (
        "jiv",
        "tl",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/jiv-tl.txt.zip",
    (
        "jiv",
        "tmh",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/jiv-tmh.txt.zip",
    (
        "jiv",
        "tr",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/jiv-tr.txt.zip",
    (
        "jiv",
        "uk",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/jiv-uk.txt.zip",
    (
        "jiv",
        "usp",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/jiv-usp.txt.zip",
    (
        "jiv",
        "vi",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/jiv-vi.txt.zip",
    (
        "jiv",
        "wal",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/jiv-wal.txt.zip",
    (
        "jiv",
        "wo",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/jiv-wo.txt.zip",
    (
        "jiv",
        "xh",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/jiv-xh.txt.zip",
    (
        "jiv",
        "zh",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/jiv-zh.txt.zip",
    (
        "jiv",
        "zu",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/jiv-zu.txt.zip",
    (
        "kab",
        "kbh",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/kab-kbh.txt.zip",
    (
        "kab",
        "kek",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/kab-kek.txt.zip",
    (
        "kab",
        "kn",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/kab-kn.txt.zip",
    (
        "kab",
        "ko",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/kab-ko.txt.zip",
    (
        "kab",
        "la",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/kab-la.txt.zip",
    (
        "kab",
        "lt",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/kab-lt.txt.zip",
    (
        "kab",
        "lv",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/kab-lv.txt.zip",
    (
        "kab",
        "mam",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/kab-mam.txt.zip",
    (
        "kab",
        "mi",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/kab-mi.txt.zip",
    (
        "kab",
        "ml",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/kab-ml.txt.zip",
    (
        "kab",
        "mr",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/kab-mr.txt.zip",
    (
        "kab",
        "my",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/kab-my.txt.zip",
    (
        "kab",
        "ne",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/kab-ne.txt.zip",
    (
        "kab",
        "nhg",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/kab-nhg.txt.zip",
    (
        "kab",
        "nl",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/kab-nl.txt.zip",
    (
        "kab",
        "no",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/kab-no.txt.zip",
    (
        "kab",
        "ojb",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/kab-ojb.txt.zip",
    (
        "kab",
        "pck",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/kab-pck.txt.zip",
    (
        "kab",
        "pes",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/kab-pes.txt.zip",
    (
        "kab",
        "pl",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/kab-pl.txt.zip",
    (
        "kab",
        "plt",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/kab-plt.txt.zip",
    (
        "kab",
        "pot",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/kab-pot.txt.zip",
    (
        "kab",
        "ppk",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/kab-ppk.txt.zip",
    (
        "kab",
        "pt",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/kab-pt.txt.zip",
    (
        "kab",
        "quc",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/kab-quc.txt.zip",
    (
        "kab",
        "quw",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/kab-quw.txt.zip",
    (
        "kab",
        "ro",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/kab-ro.txt.zip",
    (
        "kab",
        "rom",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/kab-rom.txt.zip",
    (
        "kab",
        "ru",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/kab-ru.txt.zip",
    (
        "kab",
        "shi",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/kab-shi.txt.zip",
    (
        "kab",
        "sk",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/kab-sk.txt.zip",
    (
        "kab",
        "sl",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/kab-sl.txt.zip",
    (
        "kab",
        "sn",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/kab-sn.txt.zip",
    (
        "kab",
        "so",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/kab-so.txt.zip",
    (
        "kab",
        "sq",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/kab-sq.txt.zip",
    (
        "kab",
        "sr",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/kab-sr.txt.zip",
    (
        "kab",
        "ss",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/kab-ss.txt.zip",
    (
        "kab",
        "sv",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/kab-sv.txt.zip",
    (
        "kab",
        "syr",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/kab-syr.txt.zip",
    (
        "kab",
        "te",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/kab-te.txt.zip",
    (
        "kab",
        "th",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/kab-th.txt.zip",
    (
        "kab",
        "tl",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/kab-tl.txt.zip",
    (
        "kab",
        "tmh",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/kab-tmh.txt.zip",
    (
        "kab",
        "tr",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/kab-tr.txt.zip",
    (
        "kab",
        "uk",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/kab-uk.txt.zip",
    (
        "kab",
        "usp",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/kab-usp.txt.zip",
    (
        "kab",
        "vi",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/kab-vi.txt.zip",
    (
        "kab",
        "wal",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/kab-wal.txt.zip",
    (
        "kab",
        "wo",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/kab-wo.txt.zip",
    (
        "kab",
        "xh",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/kab-xh.txt.zip",
    (
        "kab",
        "zh",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/kab-zh.txt.zip",
    (
        "kab",
        "zu",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/kab-zu.txt.zip",
    (
        "kbh",
        "kek",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/kbh-kek.txt.zip",
    (
        "kbh",
        "kn",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/kbh-kn.txt.zip",
    (
        "kbh",
        "ko",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/kbh-ko.txt.zip",
    (
        "kbh",
        "la",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/kbh-la.txt.zip",
    (
        "kbh",
        "lt",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/kbh-lt.txt.zip",
    (
        "kbh",
        "lv",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/kbh-lv.txt.zip",
    (
        "kbh",
        "mam",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/kbh-mam.txt.zip",
    (
        "kbh",
        "mi",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/kbh-mi.txt.zip",
    (
        "kbh",
        "ml",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/kbh-ml.txt.zip",
    (
        "kbh",
        "mr",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/kbh-mr.txt.zip",
    (
        "kbh",
        "my",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/kbh-my.txt.zip",
    (
        "kbh",
        "ne",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/kbh-ne.txt.zip",
    (
        "kbh",
        "nhg",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/kbh-nhg.txt.zip",
    (
        "kbh",
        "nl",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/kbh-nl.txt.zip",
    (
        "kbh",
        "no",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/kbh-no.txt.zip",
    (
        "kbh",
        "ojb",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/kbh-ojb.txt.zip",
    (
        "kbh",
        "pck",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/kbh-pck.txt.zip",
    (
        "kbh",
        "pes",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/kbh-pes.txt.zip",
    (
        "kbh",
        "pl",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/kbh-pl.txt.zip",
    (
        "kbh",
        "plt",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/kbh-plt.txt.zip",
    (
        "kbh",
        "pot",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/kbh-pot.txt.zip",
    (
        "kbh",
        "ppk",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/kbh-ppk.txt.zip",
    (
        "kbh",
        "pt",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/kbh-pt.txt.zip",
    (
        "kbh",
        "quc",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/kbh-quc.txt.zip",
    (
        "kbh",
        "quw",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/kbh-quw.txt.zip",
    (
        "kbh",
        "ro",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/kbh-ro.txt.zip",
    (
        "kbh",
        "rom",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/kbh-rom.txt.zip",
    (
        "kbh",
        "ru",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/kbh-ru.txt.zip",
    (
        "kbh",
        "shi",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/kbh-shi.txt.zip",
    (
        "kbh",
        "sk",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/kbh-sk.txt.zip",
    (
        "kbh",
        "sl",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/kbh-sl.txt.zip",
    (
        "kbh",
        "sn",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/kbh-sn.txt.zip",
    (
        "kbh",
        "so",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/kbh-so.txt.zip",
    (
        "kbh",
        "sq",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/kbh-sq.txt.zip",
    (
        "kbh",
        "sr",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/kbh-sr.txt.zip",
    (
        "kbh",
        "ss",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/kbh-ss.txt.zip",
    (
        "kbh",
        "sv",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/kbh-sv.txt.zip",
    (
        "kbh",
        "syr",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/kbh-syr.txt.zip",
    (
        "kbh",
        "te",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/kbh-te.txt.zip",
    (
        "kbh",
        "th",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/kbh-th.txt.zip",
    (
        "kbh",
        "tl",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/kbh-tl.txt.zip",
    (
        "kbh",
        "tmh",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/kbh-tmh.txt.zip",
    (
        "kbh",
        "tr",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/kbh-tr.txt.zip",
    (
        "kbh",
        "uk",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/kbh-uk.txt.zip",
    (
        "kbh",
        "usp",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/kbh-usp.txt.zip",
    (
        "kbh",
        "vi",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/kbh-vi.txt.zip",
    (
        "kbh",
        "wal",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/kbh-wal.txt.zip",
    (
        "kbh",
        "wo",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/kbh-wo.txt.zip",
    (
        "kbh",
        "xh",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/kbh-xh.txt.zip",
    (
        "kbh",
        "zh",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/kbh-zh.txt.zip",
    (
        "kbh",
        "zu",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/kbh-zu.txt.zip",
    (
        "kek",
        "kn",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/kek-kn.txt.zip",
    (
        "kek",
        "ko",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/kek-ko.txt.zip",
    (
        "kek",
        "la",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/kek-la.txt.zip",
    (
        "kek",
        "lt",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/kek-lt.txt.zip",
    (
        "kek",
        "lv",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/kek-lv.txt.zip",
    (
        "kek",
        "mam",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/kek-mam.txt.zip",
    (
        "kek",
        "mi",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/kek-mi.txt.zip",
    (
        "kek",
        "ml",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/kek-ml.txt.zip",
    (
        "kek",
        "mr",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/kek-mr.txt.zip",
    (
        "kek",
        "my",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/kek-my.txt.zip",
    (
        "kek",
        "ne",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/kek-ne.txt.zip",
    (
        "kek",
        "nhg",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/kek-nhg.txt.zip",
    (
        "kek",
        "nl",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/kek-nl.txt.zip",
    (
        "kek",
        "no",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/kek-no.txt.zip",
    (
        "kek",
        "ojb",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/kek-ojb.txt.zip",
    (
        "kek",
        "pck",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/kek-pck.txt.zip",
    (
        "kek",
        "pes",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/kek-pes.txt.zip",
    (
        "kek",
        "pl",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/kek-pl.txt.zip",
    (
        "kek",
        "plt",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/kek-plt.txt.zip",
    (
        "kek",
        "pot",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/kek-pot.txt.zip",
    (
        "kek",
        "ppk",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/kek-ppk.txt.zip",
    (
        "kek",
        "pt",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/kek-pt.txt.zip",
    (
        "kek",
        "quc",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/kek-quc.txt.zip",
    (
        "kek",
        "quw",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/kek-quw.txt.zip",
    (
        "kek",
        "ro",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/kek-ro.txt.zip",
    (
        "kek",
        "rom",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/kek-rom.txt.zip",
    (
        "kek",
        "ru",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/kek-ru.txt.zip",
    (
        "kek",
        "shi",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/kek-shi.txt.zip",
    (
        "kek",
        "sk",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/kek-sk.txt.zip",
    (
        "kek",
        "sl",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/kek-sl.txt.zip",
    (
        "kek",
        "sn",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/kek-sn.txt.zip",
    (
        "kek",
        "so",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/kek-so.txt.zip",
    (
        "kek",
        "sq",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/kek-sq.txt.zip",
    (
        "kek",
        "sr",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/kek-sr.txt.zip",
    (
        "kek",
        "ss",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/kek-ss.txt.zip",
    (
        "kek",
        "sv",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/kek-sv.txt.zip",
    (
        "kek",
        "syr",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/kek-syr.txt.zip",
    (
        "kek",
        "te",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/kek-te.txt.zip",
    (
        "kek",
        "th",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/kek-th.txt.zip",
    (
        "kek",
        "tl",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/kek-tl.txt.zip",
    (
        "kek",
        "tmh",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/kek-tmh.txt.zip",
    (
        "kek",
        "tr",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/kek-tr.txt.zip",
    (
        "kek",
        "uk",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/kek-uk.txt.zip",
    (
        "kek",
        "usp",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/kek-usp.txt.zip",
    (
        "kek",
        "vi",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/kek-vi.txt.zip",
    (
        "kek",
        "wal",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/kek-wal.txt.zip",
    (
        "kek",
        "wo",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/kek-wo.txt.zip",
    (
        "kek",
        "xh",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/kek-xh.txt.zip",
    (
        "kek",
        "zh",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/kek-zh.txt.zip",
    (
        "kek",
        "zu",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/kek-zu.txt.zip",
    ("kn", "ko"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/kn-ko.txt.zip",
    ("kn", "la"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/kn-la.txt.zip",
    ("kn", "lt"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/kn-lt.txt.zip",
    ("kn", "lv"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/kn-lv.txt.zip",
    (
        "kn",
        "mam",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/kn-mam.txt.zip",
    ("kn", "mi"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/kn-mi.txt.zip",
    ("kn", "ml"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/kn-ml.txt.zip",
    ("kn", "mr"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/kn-mr.txt.zip",
    ("kn", "my"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/kn-my.txt.zip",
    ("kn", "ne"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/kn-ne.txt.zip",
    (
        "kn",
        "nhg",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/kn-nhg.txt.zip",
    ("kn", "nl"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/kn-nl.txt.zip",
    ("kn", "no"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/kn-no.txt.zip",
    (
        "kn",
        "ojb",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/kn-ojb.txt.zip",
    (
        "kn",
        "pck",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/kn-pck.txt.zip",
    (
        "kn",
        "pes",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/kn-pes.txt.zip",
    ("kn", "pl"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/kn-pl.txt.zip",
    (
        "kn",
        "plt",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/kn-plt.txt.zip",
    (
        "kn",
        "pot",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/kn-pot.txt.zip",
    (
        "kn",
        "ppk",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/kn-ppk.txt.zip",
    ("kn", "pt"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/kn-pt.txt.zip",
    (
        "kn",
        "quc",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/kn-quc.txt.zip",
    (
        "kn",
        "quw",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/kn-quw.txt.zip",
    ("kn", "ro"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/kn-ro.txt.zip",
    (
        "kn",
        "rom",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/kn-rom.txt.zip",
    ("kn", "ru"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/kn-ru.txt.zip",
    (
        "kn",
        "shi",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/kn-shi.txt.zip",
    ("kn", "sk"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/kn-sk.txt.zip",
    ("kn", "sl"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/kn-sl.txt.zip",
    ("kn", "sn"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/kn-sn.txt.zip",
    ("kn", "so"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/kn-so.txt.zip",
    ("kn", "sq"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/kn-sq.txt.zip",
    ("kn", "sr"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/kn-sr.txt.zip",
    ("kn", "ss"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/kn-ss.txt.zip",
    ("kn", "sv"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/kn-sv.txt.zip",
    (
        "kn",
        "syr",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/kn-syr.txt.zip",
    ("kn", "te"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/kn-te.txt.zip",
    ("kn", "th"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/kn-th.txt.zip",
    ("kn", "tl"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/kn-tl.txt.zip",
    (
        "kn",
        "tmh",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/kn-tmh.txt.zip",
    ("kn", "tr"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/kn-tr.txt.zip",
    ("kn", "uk"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/kn-uk.txt.zip",
    (
        "kn",
        "usp",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/kn-usp.txt.zip",
    ("kn", "vi"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/kn-vi.txt.zip",
    (
        "kn",
        "wal",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/kn-wal.txt.zip",
    ("kn", "wo"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/kn-wo.txt.zip",
    ("kn", "xh"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/kn-xh.txt.zip",
    ("kn", "zh"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/kn-zh.txt.zip",
    ("kn", "zu"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/kn-zu.txt.zip",
    ("ko", "la"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ko-la.txt.zip",
    ("ko", "lt"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ko-lt.txt.zip",
    ("ko", "lv"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ko-lv.txt.zip",
    (
        "ko",
        "mam",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ko-mam.txt.zip",
    ("ko", "mi"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ko-mi.txt.zip",
    ("ko", "ml"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ko-ml.txt.zip",
    ("ko", "mr"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ko-mr.txt.zip",
    ("ko", "my"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ko-my.txt.zip",
    ("ko", "ne"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ko-ne.txt.zip",
    (
        "ko",
        "nhg",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ko-nhg.txt.zip",
    ("ko", "nl"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ko-nl.txt.zip",
    ("ko", "no"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ko-no.txt.zip",
    (
        "ko",
        "ojb",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ko-ojb.txt.zip",
    (
        "ko",
        "pck",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ko-pck.txt.zip",
    (
        "ko",
        "pes",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ko-pes.txt.zip",
    ("ko", "pl"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ko-pl.txt.zip",
    (
        "ko",
        "plt",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ko-plt.txt.zip",
    (
        "ko",
        "pot",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ko-pot.txt.zip",
    (
        "ko",
        "ppk",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ko-ppk.txt.zip",
    ("ko", "pt"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ko-pt.txt.zip",
    (
        "ko",
        "quc",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ko-quc.txt.zip",
    (
        "ko",
        "quw",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ko-quw.txt.zip",
    ("ko", "ro"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ko-ro.txt.zip",
    (
        "ko",
        "rom",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ko-rom.txt.zip",
    ("ko", "ru"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ko-ru.txt.zip",
    (
        "ko",
        "shi",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ko-shi.txt.zip",
    ("ko", "sk"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ko-sk.txt.zip",
    ("ko", "sl"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ko-sl.txt.zip",
    ("ko", "sn"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ko-sn.txt.zip",
    ("ko", "so"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ko-so.txt.zip",
    ("ko", "sq"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ko-sq.txt.zip",
    ("ko", "sr"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ko-sr.txt.zip",
    ("ko", "ss"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ko-ss.txt.zip",
    ("ko", "sv"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ko-sv.txt.zip",
    (
        "ko",
        "syr",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ko-syr.txt.zip",
    ("ko", "te"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ko-te.txt.zip",
    ("ko", "th"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ko-th.txt.zip",
    ("ko", "tl"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ko-tl.txt.zip",
    (
        "ko",
        "tmh",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ko-tmh.txt.zip",
    ("ko", "tr"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ko-tr.txt.zip",
    ("ko", "uk"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ko-uk.txt.zip",
    (
        "ko",
        "usp",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ko-usp.txt.zip",
    ("ko", "vi"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ko-vi.txt.zip",
    (
        "ko",
        "wal",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ko-wal.txt.zip",
    ("ko", "wo"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ko-wo.txt.zip",
    ("ko", "xh"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ko-xh.txt.zip",
    ("ko", "zh"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ko-zh.txt.zip",
    ("ko", "zu"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ko-zu.txt.zip",
    ("la", "lt"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/la-lt.txt.zip",
    ("la", "lv"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/la-lv.txt.zip",
    (
        "la",
        "mam",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/la-mam.txt.zip",
    ("la", "mi"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/la-mi.txt.zip",
    ("la", "ml"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/la-ml.txt.zip",
    ("la", "mr"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/la-mr.txt.zip",
    ("la", "my"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/la-my.txt.zip",
    ("la", "ne"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/la-ne.txt.zip",
    (
        "la",
        "nhg",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/la-nhg.txt.zip",
    ("la", "nl"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/la-nl.txt.zip",
    ("la", "no"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/la-no.txt.zip",
    (
        "la",
        "ojb",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/la-ojb.txt.zip",
    (
        "la",
        "pck",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/la-pck.txt.zip",
    (
        "la",
        "pes",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/la-pes.txt.zip",
    ("la", "pl"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/la-pl.txt.zip",
    (
        "la",
        "plt",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/la-plt.txt.zip",
    (
        "la",
        "pot",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/la-pot.txt.zip",
    (
        "la",
        "ppk",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/la-ppk.txt.zip",
    ("la", "pt"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/la-pt.txt.zip",
    (
        "la",
        "quc",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/la-quc.txt.zip",
    (
        "la",
        "quw",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/la-quw.txt.zip",
    ("la", "ro"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/la-ro.txt.zip",
    (
        "la",
        "rom",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/la-rom.txt.zip",
    ("la", "ru"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/la-ru.txt.zip",
    (
        "la",
        "shi",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/la-shi.txt.zip",
    ("la", "sk"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/la-sk.txt.zip",
    ("la", "sl"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/la-sl.txt.zip",
    ("la", "sn"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/la-sn.txt.zip",
    ("la", "so"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/la-so.txt.zip",
    ("la", "sq"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/la-sq.txt.zip",
    ("la", "sr"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/la-sr.txt.zip",
    ("la", "ss"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/la-ss.txt.zip",
    ("la", "sv"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/la-sv.txt.zip",
    (
        "la",
        "syr",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/la-syr.txt.zip",
    ("la", "te"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/la-te.txt.zip",
    ("la", "th"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/la-th.txt.zip",
    ("la", "tl"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/la-tl.txt.zip",
    (
        "la",
        "tmh",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/la-tmh.txt.zip",
    ("la", "tr"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/la-tr.txt.zip",
    ("la", "uk"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/la-uk.txt.zip",
    (
        "la",
        "usp",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/la-usp.txt.zip",
    ("la", "vi"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/la-vi.txt.zip",
    (
        "la",
        "wal",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/la-wal.txt.zip",
    ("la", "wo"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/la-wo.txt.zip",
    ("la", "xh"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/la-xh.txt.zip",
    ("la", "zh"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/la-zh.txt.zip",
    ("la", "zu"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/la-zu.txt.zip",
    ("lt", "lv"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/lt-lv.txt.zip",
    (
        "lt",
        "mam",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/lt-mam.txt.zip",
    ("lt", "mi"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/lt-mi.txt.zip",
    ("lt", "ml"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/lt-ml.txt.zip",
    ("lt", "mr"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/lt-mr.txt.zip",
    ("lt", "my"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/lt-my.txt.zip",
    ("lt", "ne"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/lt-ne.txt.zip",
    (
        "lt",
        "nhg",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/lt-nhg.txt.zip",
    ("lt", "nl"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/lt-nl.txt.zip",
    ("lt", "no"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/lt-no.txt.zip",
    (
        "lt",
        "ojb",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/lt-ojb.txt.zip",
    (
        "lt",
        "pck",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/lt-pck.txt.zip",
    (
        "lt",
        "pes",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/lt-pes.txt.zip",
    ("lt", "pl"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/lt-pl.txt.zip",
    (
        "lt",
        "plt",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/lt-plt.txt.zip",
    (
        "lt",
        "pot",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/lt-pot.txt.zip",
    (
        "lt",
        "ppk",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/lt-ppk.txt.zip",
    ("lt", "pt"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/lt-pt.txt.zip",
    (
        "lt",
        "quc",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/lt-quc.txt.zip",
    (
        "lt",
        "quw",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/lt-quw.txt.zip",
    ("lt", "ro"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/lt-ro.txt.zip",
    (
        "lt",
        "rom",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/lt-rom.txt.zip",
    ("lt", "ru"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/lt-ru.txt.zip",
    (
        "lt",
        "shi",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/lt-shi.txt.zip",
    ("lt", "sk"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/lt-sk.txt.zip",
    ("lt", "sl"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/lt-sl.txt.zip",
    ("lt", "sn"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/lt-sn.txt.zip",
    ("lt", "so"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/lt-so.txt.zip",
    ("lt", "sq"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/lt-sq.txt.zip",
    ("lt", "sr"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/lt-sr.txt.zip",
    ("lt", "ss"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/lt-ss.txt.zip",
    ("lt", "sv"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/lt-sv.txt.zip",
    (
        "lt",
        "syr",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/lt-syr.txt.zip",
    ("lt", "te"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/lt-te.txt.zip",
    ("lt", "th"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/lt-th.txt.zip",
    ("lt", "tl"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/lt-tl.txt.zip",
    (
        "lt",
        "tmh",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/lt-tmh.txt.zip",
    ("lt", "tr"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/lt-tr.txt.zip",
    ("lt", "uk"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/lt-uk.txt.zip",
    (
        "lt",
        "usp",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/lt-usp.txt.zip",
    ("lt", "vi"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/lt-vi.txt.zip",
    (
        "lt",
        "wal",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/lt-wal.txt.zip",
    ("lt", "wo"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/lt-wo.txt.zip",
    ("lt", "xh"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/lt-xh.txt.zip",
    ("lt", "zh"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/lt-zh.txt.zip",
    ("lt", "zu"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/lt-zu.txt.zip",
    (
        "lv",
        "mam",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/lv-mam.txt.zip",
    ("lv", "mi"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/lv-mi.txt.zip",
    ("lv", "ml"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/lv-ml.txt.zip",
    ("lv", "mr"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/lv-mr.txt.zip",
    ("lv", "my"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/lv-my.txt.zip",
    ("lv", "ne"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/lv-ne.txt.zip",
    (
        "lv",
        "nhg",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/lv-nhg.txt.zip",
    ("lv", "nl"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/lv-nl.txt.zip",
    ("lv", "no"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/lv-no.txt.zip",
    (
        "lv",
        "ojb",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/lv-ojb.txt.zip",
    (
        "lv",
        "pck",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/lv-pck.txt.zip",
    (
        "lv",
        "pes",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/lv-pes.txt.zip",
    ("lv", "pl"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/lv-pl.txt.zip",
    (
        "lv",
        "plt",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/lv-plt.txt.zip",
    (
        "lv",
        "pot",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/lv-pot.txt.zip",
    (
        "lv",
        "ppk",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/lv-ppk.txt.zip",
    ("lv", "pt"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/lv-pt.txt.zip",
    (
        "lv",
        "quc",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/lv-quc.txt.zip",
    (
        "lv",
        "quw",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/lv-quw.txt.zip",
    ("lv", "ro"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/lv-ro.txt.zip",
    (
        "lv",
        "rom",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/lv-rom.txt.zip",
    ("lv", "ru"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/lv-ru.txt.zip",
    (
        "lv",
        "shi",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/lv-shi.txt.zip",
    ("lv", "sk"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/lv-sk.txt.zip",
    ("lv", "sl"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/lv-sl.txt.zip",
    ("lv", "sn"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/lv-sn.txt.zip",
    ("lv", "so"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/lv-so.txt.zip",
    ("lv", "sq"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/lv-sq.txt.zip",
    ("lv", "sr"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/lv-sr.txt.zip",
    ("lv", "ss"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/lv-ss.txt.zip",
    ("lv", "sv"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/lv-sv.txt.zip",
    (
        "lv",
        "syr",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/lv-syr.txt.zip",
    ("lv", "te"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/lv-te.txt.zip",
    ("lv", "th"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/lv-th.txt.zip",
    ("lv", "tl"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/lv-tl.txt.zip",
    (
        "lv",
        "tmh",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/lv-tmh.txt.zip",
    ("lv", "tr"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/lv-tr.txt.zip",
    ("lv", "uk"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/lv-uk.txt.zip",
    (
        "lv",
        "usp",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/lv-usp.txt.zip",
    ("lv", "vi"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/lv-vi.txt.zip",
    (
        "lv",
        "wal",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/lv-wal.txt.zip",
    ("lv", "wo"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/lv-wo.txt.zip",
    ("lv", "xh"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/lv-xh.txt.zip",
    ("lv", "zh"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/lv-zh.txt.zip",
    ("lv", "zu"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/lv-zu.txt.zip",
    (
        "mam",
        "mi",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/mam-mi.txt.zip",
    (
        "mam",
        "ml",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/mam-ml.txt.zip",
    (
        "mam",
        "mr",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/mam-mr.txt.zip",
    (
        "mam",
        "my",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/mam-my.txt.zip",
    (
        "mam",
        "ne",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/mam-ne.txt.zip",
    (
        "mam",
        "nhg",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/mam-nhg.txt.zip",
    (
        "mam",
        "nl",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/mam-nl.txt.zip",
    (
        "mam",
        "no",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/mam-no.txt.zip",
    (
        "mam",
        "ojb",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/mam-ojb.txt.zip",
    (
        "mam",
        "pck",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/mam-pck.txt.zip",
    (
        "mam",
        "pes",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/mam-pes.txt.zip",
    (
        "mam",
        "pl",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/mam-pl.txt.zip",
    (
        "mam",
        "plt",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/mam-plt.txt.zip",
    (
        "mam",
        "pot",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/mam-pot.txt.zip",
    (
        "mam",
        "ppk",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/mam-ppk.txt.zip",
    (
        "mam",
        "pt",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/mam-pt.txt.zip",
    (
        "mam",
        "quc",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/mam-quc.txt.zip",
    (
        "mam",
        "quw",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/mam-quw.txt.zip",
    (
        "mam",
        "ro",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/mam-ro.txt.zip",
    (
        "mam",
        "rom",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/mam-rom.txt.zip",
    (
        "mam",
        "ru",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/mam-ru.txt.zip",
    (
        "mam",
        "shi",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/mam-shi.txt.zip",
    (
        "mam",
        "sk",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/mam-sk.txt.zip",
    (
        "mam",
        "sl",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/mam-sl.txt.zip",
    (
        "mam",
        "sn",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/mam-sn.txt.zip",
    (
        "mam",
        "so",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/mam-so.txt.zip",
    (
        "mam",
        "sq",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/mam-sq.txt.zip",
    (
        "mam",
        "sr",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/mam-sr.txt.zip",
    (
        "mam",
        "ss",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/mam-ss.txt.zip",
    (
        "mam",
        "sv",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/mam-sv.txt.zip",
    (
        "mam",
        "syr",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/mam-syr.txt.zip",
    (
        "mam",
        "te",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/mam-te.txt.zip",
    (
        "mam",
        "th",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/mam-th.txt.zip",
    (
        "mam",
        "tl",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/mam-tl.txt.zip",
    (
        "mam",
        "tmh",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/mam-tmh.txt.zip",
    (
        "mam",
        "tr",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/mam-tr.txt.zip",
    (
        "mam",
        "uk",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/mam-uk.txt.zip",
    (
        "mam",
        "usp",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/mam-usp.txt.zip",
    (
        "mam",
        "vi",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/mam-vi.txt.zip",
    (
        "mam",
        "wal",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/mam-wal.txt.zip",
    (
        "mam",
        "wo",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/mam-wo.txt.zip",
    (
        "mam",
        "xh",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/mam-xh.txt.zip",
    (
        "mam",
        "zh",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/mam-zh.txt.zip",
    (
        "mam",
        "zu",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/mam-zu.txt.zip",
    ("mi", "ml"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/mi-ml.txt.zip",
    ("mi", "mr"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/mi-mr.txt.zip",
    ("mi", "my"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/mi-my.txt.zip",
    ("mi", "ne"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/mi-ne.txt.zip",
    (
        "mi",
        "nhg",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/mi-nhg.txt.zip",
    ("mi", "nl"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/mi-nl.txt.zip",
    ("mi", "no"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/mi-no.txt.zip",
    (
        "mi",
        "ojb",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/mi-ojb.txt.zip",
    (
        "mi",
        "pck",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/mi-pck.txt.zip",
    (
        "mi",
        "pes",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/mi-pes.txt.zip",
    ("mi", "pl"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/mi-pl.txt.zip",
    (
        "mi",
        "plt",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/mi-plt.txt.zip",
    (
        "mi",
        "pot",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/mi-pot.txt.zip",
    (
        "mi",
        "ppk",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/mi-ppk.txt.zip",
    ("mi", "pt"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/mi-pt.txt.zip",
    (
        "mi",
        "quc",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/mi-quc.txt.zip",
    (
        "mi",
        "quw",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/mi-quw.txt.zip",
    ("mi", "ro"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/mi-ro.txt.zip",
    (
        "mi",
        "rom",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/mi-rom.txt.zip",
    ("mi", "ru"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/mi-ru.txt.zip",
    (
        "mi",
        "shi",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/mi-shi.txt.zip",
    ("mi", "sk"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/mi-sk.txt.zip",
    ("mi", "sl"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/mi-sl.txt.zip",
    ("mi", "sn"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/mi-sn.txt.zip",
    ("mi", "so"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/mi-so.txt.zip",
    ("mi", "sq"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/mi-sq.txt.zip",
    ("mi", "sr"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/mi-sr.txt.zip",
    ("mi", "ss"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/mi-ss.txt.zip",
    ("mi", "sv"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/mi-sv.txt.zip",
    (
        "mi",
        "syr",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/mi-syr.txt.zip",
    ("mi", "te"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/mi-te.txt.zip",
    ("mi", "th"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/mi-th.txt.zip",
    ("mi", "tl"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/mi-tl.txt.zip",
    (
        "mi",
        "tmh",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/mi-tmh.txt.zip",
    ("mi", "tr"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/mi-tr.txt.zip",
    ("mi", "uk"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/mi-uk.txt.zip",
    (
        "mi",
        "usp",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/mi-usp.txt.zip",
    ("mi", "vi"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/mi-vi.txt.zip",
    (
        "mi",
        "wal",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/mi-wal.txt.zip",
    ("mi", "wo"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/mi-wo.txt.zip",
    ("mi", "xh"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/mi-xh.txt.zip",
    ("mi", "zh"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/mi-zh.txt.zip",
    ("mi", "zu"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/mi-zu.txt.zip",
    ("ml", "mr"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ml-mr.txt.zip",
    ("ml", "my"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ml-my.txt.zip",
    ("ml", "ne"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ml-ne.txt.zip",
    (
        "ml",
        "nhg",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ml-nhg.txt.zip",
    ("ml", "nl"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ml-nl.txt.zip",
    ("ml", "no"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ml-no.txt.zip",
    (
        "ml",
        "ojb",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ml-ojb.txt.zip",
    (
        "ml",
        "pck",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ml-pck.txt.zip",
    (
        "ml",
        "pes",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ml-pes.txt.zip",
    ("ml", "pl"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ml-pl.txt.zip",
    (
        "ml",
        "plt",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ml-plt.txt.zip",
    (
        "ml",
        "pot",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ml-pot.txt.zip",
    (
        "ml",
        "ppk",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ml-ppk.txt.zip",
    ("ml", "pt"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ml-pt.txt.zip",
    (
        "ml",
        "quc",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ml-quc.txt.zip",
    (
        "ml",
        "quw",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ml-quw.txt.zip",
    ("ml", "ro"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ml-ro.txt.zip",
    (
        "ml",
        "rom",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ml-rom.txt.zip",
    ("ml", "ru"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ml-ru.txt.zip",
    (
        "ml",
        "shi",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ml-shi.txt.zip",
    ("ml", "sk"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ml-sk.txt.zip",
    ("ml", "sl"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ml-sl.txt.zip",
    ("ml", "sn"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ml-sn.txt.zip",
    ("ml", "so"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ml-so.txt.zip",
    ("ml", "sq"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ml-sq.txt.zip",
    ("ml", "sr"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ml-sr.txt.zip",
    ("ml", "ss"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ml-ss.txt.zip",
    ("ml", "sv"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ml-sv.txt.zip",
    (
        "ml",
        "syr",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ml-syr.txt.zip",
    ("ml", "te"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ml-te.txt.zip",
    ("ml", "th"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ml-th.txt.zip",
    ("ml", "tl"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ml-tl.txt.zip",
    (
        "ml",
        "tmh",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ml-tmh.txt.zip",
    ("ml", "tr"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ml-tr.txt.zip",
    ("ml", "uk"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ml-uk.txt.zip",
    (
        "ml",
        "usp",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ml-usp.txt.zip",
    ("ml", "vi"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ml-vi.txt.zip",
    (
        "ml",
        "wal",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ml-wal.txt.zip",
    ("ml", "wo"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ml-wo.txt.zip",
    ("ml", "xh"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ml-xh.txt.zip",
    ("ml", "zh"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ml-zh.txt.zip",
    ("ml", "zu"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ml-zu.txt.zip",
    ("mr", "my"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/mr-my.txt.zip",
    ("mr", "ne"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/mr-ne.txt.zip",
    (
        "mr",
        "nhg",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/mr-nhg.txt.zip",
    ("mr", "nl"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/mr-nl.txt.zip",
    ("mr", "no"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/mr-no.txt.zip",
    (
        "mr",
        "ojb",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/mr-ojb.txt.zip",
    (
        "mr",
        "pck",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/mr-pck.txt.zip",
    (
        "mr",
        "pes",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/mr-pes.txt.zip",
    ("mr", "pl"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/mr-pl.txt.zip",
    (
        "mr",
        "plt",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/mr-plt.txt.zip",
    (
        "mr",
        "pot",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/mr-pot.txt.zip",
    (
        "mr",
        "ppk",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/mr-ppk.txt.zip",
    ("mr", "pt"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/mr-pt.txt.zip",
    (
        "mr",
        "quc",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/mr-quc.txt.zip",
    (
        "mr",
        "quw",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/mr-quw.txt.zip",
    ("mr", "ro"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/mr-ro.txt.zip",
    (
        "mr",
        "rom",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/mr-rom.txt.zip",
    ("mr", "ru"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/mr-ru.txt.zip",
    (
        "mr",
        "shi",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/mr-shi.txt.zip",
    ("mr", "sk"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/mr-sk.txt.zip",
    ("mr", "sl"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/mr-sl.txt.zip",
    ("mr", "sn"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/mr-sn.txt.zip",
    ("mr", "so"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/mr-so.txt.zip",
    ("mr", "sq"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/mr-sq.txt.zip",
    ("mr", "sr"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/mr-sr.txt.zip",
    ("mr", "ss"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/mr-ss.txt.zip",
    ("mr", "sv"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/mr-sv.txt.zip",
    (
        "mr",
        "syr",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/mr-syr.txt.zip",
    ("mr", "te"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/mr-te.txt.zip",
    ("mr", "th"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/mr-th.txt.zip",
    ("mr", "tl"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/mr-tl.txt.zip",
    (
        "mr",
        "tmh",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/mr-tmh.txt.zip",
    ("mr", "tr"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/mr-tr.txt.zip",
    ("mr", "uk"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/mr-uk.txt.zip",
    (
        "mr",
        "usp",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/mr-usp.txt.zip",
    ("mr", "vi"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/mr-vi.txt.zip",
    (
        "mr",
        "wal",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/mr-wal.txt.zip",
    ("mr", "wo"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/mr-wo.txt.zip",
    ("mr", "xh"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/mr-xh.txt.zip",
    ("mr", "zh"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/mr-zh.txt.zip",
    ("mr", "zu"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/mr-zu.txt.zip",
    ("my", "ne"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/my-ne.txt.zip",
    (
        "my",
        "nhg",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/my-nhg.txt.zip",
    ("my", "nl"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/my-nl.txt.zip",
    ("my", "no"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/my-no.txt.zip",
    (
        "my",
        "ojb",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/my-ojb.txt.zip",
    (
        "my",
        "pck",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/my-pck.txt.zip",
    (
        "my",
        "pes",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/my-pes.txt.zip",
    ("my", "pl"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/my-pl.txt.zip",
    (
        "my",
        "plt",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/my-plt.txt.zip",
    (
        "my",
        "pot",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/my-pot.txt.zip",
    (
        "my",
        "ppk",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/my-ppk.txt.zip",
    ("my", "pt"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/my-pt.txt.zip",
    (
        "my",
        "quc",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/my-quc.txt.zip",
    (
        "my",
        "quw",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/my-quw.txt.zip",
    ("my", "ro"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/my-ro.txt.zip",
    (
        "my",
        "rom",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/my-rom.txt.zip",
    ("my", "ru"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/my-ru.txt.zip",
    (
        "my",
        "shi",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/my-shi.txt.zip",
    ("my", "sk"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/my-sk.txt.zip",
    ("my", "sl"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/my-sl.txt.zip",
    ("my", "sn"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/my-sn.txt.zip",
    ("my", "so"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/my-so.txt.zip",
    ("my", "sq"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/my-sq.txt.zip",
    ("my", "sr"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/my-sr.txt.zip",
    ("my", "ss"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/my-ss.txt.zip",
    ("my", "sv"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/my-sv.txt.zip",
    (
        "my",
        "syr",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/my-syr.txt.zip",
    ("my", "te"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/my-te.txt.zip",
    ("my", "th"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/my-th.txt.zip",
    ("my", "tl"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/my-tl.txt.zip",
    (
        "my",
        "tmh",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/my-tmh.txt.zip",
    ("my", "tr"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/my-tr.txt.zip",
    ("my", "uk"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/my-uk.txt.zip",
    (
        "my",
        "usp",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/my-usp.txt.zip",
    ("my", "vi"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/my-vi.txt.zip",
    (
        "my",
        "wal",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/my-wal.txt.zip",
    ("my", "wo"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/my-wo.txt.zip",
    ("my", "xh"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/my-xh.txt.zip",
    ("my", "zh"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/my-zh.txt.zip",
    ("my", "zu"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/my-zu.txt.zip",
    (
        "ne",
        "nhg",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ne-nhg.txt.zip",
    ("ne", "nl"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ne-nl.txt.zip",
    ("ne", "no"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ne-no.txt.zip",
    (
        "ne",
        "ojb",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ne-ojb.txt.zip",
    (
        "ne",
        "pck",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ne-pck.txt.zip",
    (
        "ne",
        "pes",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ne-pes.txt.zip",
    ("ne", "pl"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ne-pl.txt.zip",
    (
        "ne",
        "plt",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ne-plt.txt.zip",
    (
        "ne",
        "pot",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ne-pot.txt.zip",
    (
        "ne",
        "ppk",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ne-ppk.txt.zip",
    ("ne", "pt"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ne-pt.txt.zip",
    (
        "ne",
        "quc",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ne-quc.txt.zip",
    (
        "ne",
        "quw",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ne-quw.txt.zip",
    ("ne", "ro"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ne-ro.txt.zip",
    (
        "ne",
        "rom",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ne-rom.txt.zip",
    ("ne", "ru"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ne-ru.txt.zip",
    (
        "ne",
        "shi",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ne-shi.txt.zip",
    ("ne", "sk"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ne-sk.txt.zip",
    ("ne", "sl"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ne-sl.txt.zip",
    ("ne", "sn"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ne-sn.txt.zip",
    ("ne", "so"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ne-so.txt.zip",
    ("ne", "sq"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ne-sq.txt.zip",
    ("ne", "sr"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ne-sr.txt.zip",
    ("ne", "ss"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ne-ss.txt.zip",
    ("ne", "sv"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ne-sv.txt.zip",
    (
        "ne",
        "syr",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ne-syr.txt.zip",
    ("ne", "te"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ne-te.txt.zip",
    ("ne", "th"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ne-th.txt.zip",
    ("ne", "tl"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ne-tl.txt.zip",
    (
        "ne",
        "tmh",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ne-tmh.txt.zip",
    ("ne", "tr"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ne-tr.txt.zip",
    ("ne", "uk"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ne-uk.txt.zip",
    (
        "ne",
        "usp",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ne-usp.txt.zip",
    ("ne", "vi"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ne-vi.txt.zip",
    (
        "ne",
        "wal",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ne-wal.txt.zip",
    ("ne", "wo"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ne-wo.txt.zip",
    ("ne", "xh"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ne-xh.txt.zip",
    ("ne", "zh"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ne-zh.txt.zip",
    ("ne", "zu"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ne-zu.txt.zip",
    (
        "nhg",
        "nl",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/nhg-nl.txt.zip",
    (
        "nhg",
        "no",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/nhg-no.txt.zip",
    (
        "nhg",
        "ojb",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/nhg-ojb.txt.zip",
    (
        "nhg",
        "pck",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/nhg-pck.txt.zip",
    (
        "nhg",
        "pes",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/nhg-pes.txt.zip",
    (
        "nhg",
        "pl",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/nhg-pl.txt.zip",
    (
        "nhg",
        "plt",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/nhg-plt.txt.zip",
    (
        "nhg",
        "pot",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/nhg-pot.txt.zip",
    (
        "nhg",
        "ppk",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/nhg-ppk.txt.zip",
    (
        "nhg",
        "pt",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/nhg-pt.txt.zip",
    (
        "nhg",
        "quc",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/nhg-quc.txt.zip",
    (
        "nhg",
        "quw",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/nhg-quw.txt.zip",
    (
        "nhg",
        "ro",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/nhg-ro.txt.zip",
    (
        "nhg",
        "rom",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/nhg-rom.txt.zip",
    (
        "nhg",
        "ru",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/nhg-ru.txt.zip",
    (
        "nhg",
        "shi",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/nhg-shi.txt.zip",
    (
        "nhg",
        "sk",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/nhg-sk.txt.zip",
    (
        "nhg",
        "sl",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/nhg-sl.txt.zip",
    (
        "nhg",
        "sn",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/nhg-sn.txt.zip",
    (
        "nhg",
        "so",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/nhg-so.txt.zip",
    (
        "nhg",
        "sq",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/nhg-sq.txt.zip",
    (
        "nhg",
        "sr",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/nhg-sr.txt.zip",
    (
        "nhg",
        "ss",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/nhg-ss.txt.zip",
    (
        "nhg",
        "sv",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/nhg-sv.txt.zip",
    (
        "nhg",
        "syr",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/nhg-syr.txt.zip",
    (
        "nhg",
        "te",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/nhg-te.txt.zip",
    (
        "nhg",
        "th",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/nhg-th.txt.zip",
    (
        "nhg",
        "tl",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/nhg-tl.txt.zip",
    (
        "nhg",
        "tmh",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/nhg-tmh.txt.zip",
    (
        "nhg",
        "tr",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/nhg-tr.txt.zip",
    (
        "nhg",
        "uk",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/nhg-uk.txt.zip",
    (
        "nhg",
        "usp",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/nhg-usp.txt.zip",
    (
        "nhg",
        "vi",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/nhg-vi.txt.zip",
    (
        "nhg",
        "wal",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/nhg-wal.txt.zip",
    (
        "nhg",
        "wo",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/nhg-wo.txt.zip",
    (
        "nhg",
        "xh",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/nhg-xh.txt.zip",
    (
        "nhg",
        "zh",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/nhg-zh.txt.zip",
    (
        "nhg",
        "zu",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/nhg-zu.txt.zip",
    ("nl", "no"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/nl-no.txt.zip",
    (
        "nl",
        "ojb",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/nl-ojb.txt.zip",
    (
        "nl",
        "pck",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/nl-pck.txt.zip",
    (
        "nl",
        "pes",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/nl-pes.txt.zip",
    ("nl", "pl"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/nl-pl.txt.zip",
    (
        "nl",
        "plt",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/nl-plt.txt.zip",
    (
        "nl",
        "pot",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/nl-pot.txt.zip",
    (
        "nl",
        "ppk",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/nl-ppk.txt.zip",
    ("nl", "pt"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/nl-pt.txt.zip",
    (
        "nl",
        "quc",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/nl-quc.txt.zip",
    (
        "nl",
        "quw",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/nl-quw.txt.zip",
    ("nl", "ro"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/nl-ro.txt.zip",
    (
        "nl",
        "rom",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/nl-rom.txt.zip",
    ("nl", "ru"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/nl-ru.txt.zip",
    (
        "nl",
        "shi",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/nl-shi.txt.zip",
    ("nl", "sk"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/nl-sk.txt.zip",
    ("nl", "sl"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/nl-sl.txt.zip",
    ("nl", "sn"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/nl-sn.txt.zip",
    ("nl", "so"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/nl-so.txt.zip",
    ("nl", "sq"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/nl-sq.txt.zip",
    ("nl", "sr"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/nl-sr.txt.zip",
    ("nl", "ss"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/nl-ss.txt.zip",
    ("nl", "sv"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/nl-sv.txt.zip",
    (
        "nl",
        "syr",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/nl-syr.txt.zip",
    ("nl", "te"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/nl-te.txt.zip",
    ("nl", "th"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/nl-th.txt.zip",
    ("nl", "tl"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/nl-tl.txt.zip",
    (
        "nl",
        "tmh",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/nl-tmh.txt.zip",
    ("nl", "tr"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/nl-tr.txt.zip",
    ("nl", "uk"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/nl-uk.txt.zip",
    (
        "nl",
        "usp",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/nl-usp.txt.zip",
    ("nl", "vi"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/nl-vi.txt.zip",
    (
        "nl",
        "wal",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/nl-wal.txt.zip",
    ("nl", "wo"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/nl-wo.txt.zip",
    ("nl", "xh"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/nl-xh.txt.zip",
    ("nl", "zh"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/nl-zh.txt.zip",
    ("nl", "zu"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/nl-zu.txt.zip",
    (
        "no",
        "ojb",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/no-ojb.txt.zip",
    (
        "no",
        "pck",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/no-pck.txt.zip",
    (
        "no",
        "pes",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/no-pes.txt.zip",
    ("no", "pl"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/no-pl.txt.zip",
    (
        "no",
        "plt",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/no-plt.txt.zip",
    (
        "no",
        "pot",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/no-pot.txt.zip",
    (
        "no",
        "ppk",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/no-ppk.txt.zip",
    ("no", "pt"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/no-pt.txt.zip",
    (
        "no",
        "quc",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/no-quc.txt.zip",
    (
        "no",
        "quw",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/no-quw.txt.zip",
    ("no", "ro"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/no-ro.txt.zip",
    (
        "no",
        "rom",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/no-rom.txt.zip",
    ("no", "ru"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/no-ru.txt.zip",
    (
        "no",
        "shi",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/no-shi.txt.zip",
    ("no", "sk"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/no-sk.txt.zip",
    ("no", "sl"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/no-sl.txt.zip",
    ("no", "sn"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/no-sn.txt.zip",
    ("no", "so"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/no-so.txt.zip",
    ("no", "sq"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/no-sq.txt.zip",
    ("no", "sr"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/no-sr.txt.zip",
    ("no", "ss"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/no-ss.txt.zip",
    ("no", "sv"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/no-sv.txt.zip",
    (
        "no",
        "syr",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/no-syr.txt.zip",
    ("no", "te"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/no-te.txt.zip",
    ("no", "th"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/no-th.txt.zip",
    ("no", "tl"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/no-tl.txt.zip",
    (
        "no",
        "tmh",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/no-tmh.txt.zip",
    ("no", "tr"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/no-tr.txt.zip",
    ("no", "uk"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/no-uk.txt.zip",
    (
        "no",
        "usp",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/no-usp.txt.zip",
    ("no", "vi"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/no-vi.txt.zip",
    (
        "no",
        "wal",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/no-wal.txt.zip",
    ("no", "wo"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/no-wo.txt.zip",
    ("no", "xh"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/no-xh.txt.zip",
    ("no", "zh"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/no-zh.txt.zip",
    ("no", "zu"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/no-zu.txt.zip",
    (
        "ojb",
        "pck",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ojb-pck.txt.zip",
    (
        "ojb",
        "pes",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ojb-pes.txt.zip",
    (
        "ojb",
        "pl",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ojb-pl.txt.zip",
    (
        "ojb",
        "plt",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ojb-plt.txt.zip",
    (
        "ojb",
        "pot",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ojb-pot.txt.zip",
    (
        "ojb",
        "ppk",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ojb-ppk.txt.zip",
    (
        "ojb",
        "pt",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ojb-pt.txt.zip",
    (
        "ojb",
        "quc",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ojb-quc.txt.zip",
    (
        "ojb",
        "quw",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ojb-quw.txt.zip",
    (
        "ojb",
        "ro",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ojb-ro.txt.zip",
    (
        "ojb",
        "rom",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ojb-rom.txt.zip",
    (
        "ojb",
        "ru",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ojb-ru.txt.zip",
    (
        "ojb",
        "shi",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ojb-shi.txt.zip",
    (
        "ojb",
        "sk",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ojb-sk.txt.zip",
    (
        "ojb",
        "sl",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ojb-sl.txt.zip",
    (
        "ojb",
        "sn",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ojb-sn.txt.zip",
    (
        "ojb",
        "so",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ojb-so.txt.zip",
    (
        "ojb",
        "sq",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ojb-sq.txt.zip",
    (
        "ojb",
        "sr",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ojb-sr.txt.zip",
    (
        "ojb",
        "ss",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ojb-ss.txt.zip",
    (
        "ojb",
        "sv",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ojb-sv.txt.zip",
    (
        "ojb",
        "syr",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ojb-syr.txt.zip",
    (
        "ojb",
        "te",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ojb-te.txt.zip",
    (
        "ojb",
        "th",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ojb-th.txt.zip",
    (
        "ojb",
        "tl",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ojb-tl.txt.zip",
    (
        "ojb",
        "tmh",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ojb-tmh.txt.zip",
    (
        "ojb",
        "tr",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ojb-tr.txt.zip",
    (
        "ojb",
        "uk",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ojb-uk.txt.zip",
    (
        "ojb",
        "usp",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ojb-usp.txt.zip",
    (
        "ojb",
        "vi",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ojb-vi.txt.zip",
    (
        "ojb",
        "wal",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ojb-wal.txt.zip",
    (
        "ojb",
        "wo",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ojb-wo.txt.zip",
    (
        "ojb",
        "xh",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ojb-xh.txt.zip",
    (
        "ojb",
        "zh",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ojb-zh.txt.zip",
    (
        "ojb",
        "zu",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ojb-zu.txt.zip",
    (
        "pck",
        "pes",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/pck-pes.txt.zip",
    (
        "pck",
        "pl",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/pck-pl.txt.zip",
    (
        "pck",
        "plt",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/pck-plt.txt.zip",
    (
        "pck",
        "pot",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/pck-pot.txt.zip",
    (
        "pck",
        "ppk",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/pck-ppk.txt.zip",
    (
        "pck",
        "pt",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/pck-pt.txt.zip",
    (
        "pck",
        "quc",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/pck-quc.txt.zip",
    (
        "pck",
        "quw",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/pck-quw.txt.zip",
    (
        "pck",
        "ro",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/pck-ro.txt.zip",
    (
        "pck",
        "rom",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/pck-rom.txt.zip",
    (
        "pck",
        "ru",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/pck-ru.txt.zip",
    (
        "pck",
        "shi",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/pck-shi.txt.zip",
    (
        "pck",
        "sk",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/pck-sk.txt.zip",
    (
        "pck",
        "sl",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/pck-sl.txt.zip",
    (
        "pck",
        "sn",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/pck-sn.txt.zip",
    (
        "pck",
        "so",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/pck-so.txt.zip",
    (
        "pck",
        "sq",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/pck-sq.txt.zip",
    (
        "pck",
        "sr",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/pck-sr.txt.zip",
    (
        "pck",
        "ss",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/pck-ss.txt.zip",
    (
        "pck",
        "sv",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/pck-sv.txt.zip",
    (
        "pck",
        "syr",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/pck-syr.txt.zip",
    (
        "pck",
        "te",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/pck-te.txt.zip",
    (
        "pck",
        "th",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/pck-th.txt.zip",
    (
        "pck",
        "tl",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/pck-tl.txt.zip",
    (
        "pck",
        "tmh",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/pck-tmh.txt.zip",
    (
        "pck",
        "tr",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/pck-tr.txt.zip",
    (
        "pck",
        "uk",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/pck-uk.txt.zip",
    (
        "pck",
        "usp",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/pck-usp.txt.zip",
    (
        "pck",
        "vi",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/pck-vi.txt.zip",
    (
        "pck",
        "wal",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/pck-wal.txt.zip",
    (
        "pck",
        "wo",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/pck-wo.txt.zip",
    (
        "pck",
        "xh",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/pck-xh.txt.zip",
    (
        "pck",
        "zh",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/pck-zh.txt.zip",
    (
        "pck",
        "zu",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/pck-zu.txt.zip",
    (
        "pes",
        "pl",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/pes-pl.txt.zip",
    (
        "pes",
        "plt",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/pes-plt.txt.zip",
    (
        "pes",
        "pot",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/pes-pot.txt.zip",
    (
        "pes",
        "ppk",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/pes-ppk.txt.zip",
    (
        "pes",
        "pt",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/pes-pt.txt.zip",
    (
        "pes",
        "quc",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/pes-quc.txt.zip",
    (
        "pes",
        "quw",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/pes-quw.txt.zip",
    (
        "pes",
        "ro",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/pes-ro.txt.zip",
    (
        "pes",
        "rom",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/pes-rom.txt.zip",
    (
        "pes",
        "ru",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/pes-ru.txt.zip",
    (
        "pes",
        "shi",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/pes-shi.txt.zip",
    (
        "pes",
        "sk",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/pes-sk.txt.zip",
    (
        "pes",
        "sl",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/pes-sl.txt.zip",
    (
        "pes",
        "sn",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/pes-sn.txt.zip",
    (
        "pes",
        "so",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/pes-so.txt.zip",
    (
        "pes",
        "sq",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/pes-sq.txt.zip",
    (
        "pes",
        "sr",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/pes-sr.txt.zip",
    (
        "pes",
        "ss",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/pes-ss.txt.zip",
    (
        "pes",
        "sv",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/pes-sv.txt.zip",
    (
        "pes",
        "syr",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/pes-syr.txt.zip",
    (
        "pes",
        "te",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/pes-te.txt.zip",
    (
        "pes",
        "th",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/pes-th.txt.zip",
    (
        "pes",
        "tl",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/pes-tl.txt.zip",
    (
        "pes",
        "tmh",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/pes-tmh.txt.zip",
    (
        "pes",
        "tr",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/pes-tr.txt.zip",
    (
        "pes",
        "uk",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/pes-uk.txt.zip",
    (
        "pes",
        "usp",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/pes-usp.txt.zip",
    (
        "pes",
        "vi",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/pes-vi.txt.zip",
    (
        "pes",
        "wal",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/pes-wal.txt.zip",
    (
        "pes",
        "wo",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/pes-wo.txt.zip",
    (
        "pes",
        "xh",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/pes-xh.txt.zip",
    (
        "pes",
        "zh",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/pes-zh.txt.zip",
    (
        "pes",
        "zu",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/pes-zu.txt.zip",
    (
        "pl",
        "plt",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/pl-plt.txt.zip",
    (
        "pl",
        "pot",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/pl-pot.txt.zip",
    (
        "pl",
        "ppk",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/pl-ppk.txt.zip",
    ("pl", "pt"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/pl-pt.txt.zip",
    (
        "pl",
        "quc",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/pl-quc.txt.zip",
    (
        "pl",
        "quw",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/pl-quw.txt.zip",
    ("pl", "ro"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/pl-ro.txt.zip",
    (
        "pl",
        "rom",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/pl-rom.txt.zip",
    ("pl", "ru"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/pl-ru.txt.zip",
    (
        "pl",
        "shi",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/pl-shi.txt.zip",
    ("pl", "sk"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/pl-sk.txt.zip",
    ("pl", "sl"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/pl-sl.txt.zip",
    ("pl", "sn"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/pl-sn.txt.zip",
    ("pl", "so"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/pl-so.txt.zip",
    ("pl", "sq"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/pl-sq.txt.zip",
    ("pl", "sr"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/pl-sr.txt.zip",
    ("pl", "ss"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/pl-ss.txt.zip",
    ("pl", "sv"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/pl-sv.txt.zip",
    (
        "pl",
        "syr",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/pl-syr.txt.zip",
    ("pl", "te"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/pl-te.txt.zip",
    ("pl", "th"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/pl-th.txt.zip",
    ("pl", "tl"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/pl-tl.txt.zip",
    (
        "pl",
        "tmh",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/pl-tmh.txt.zip",
    ("pl", "tr"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/pl-tr.txt.zip",
    ("pl", "uk"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/pl-uk.txt.zip",
    (
        "pl",
        "usp",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/pl-usp.txt.zip",
    ("pl", "vi"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/pl-vi.txt.zip",
    (
        "pl",
        "wal",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/pl-wal.txt.zip",
    ("pl", "wo"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/pl-wo.txt.zip",
    ("pl", "xh"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/pl-xh.txt.zip",
    ("pl", "zh"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/pl-zh.txt.zip",
    ("pl", "zu"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/pl-zu.txt.zip",
    (
        "plt",
        "pot",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/plt-pot.txt.zip",
    (
        "plt",
        "ppk",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/plt-ppk.txt.zip",
    (
        "plt",
        "pt",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/plt-pt.txt.zip",
    (
        "plt",
        "quc",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/plt-quc.txt.zip",
    (
        "plt",
        "quw",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/plt-quw.txt.zip",
    (
        "plt",
        "ro",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/plt-ro.txt.zip",
    (
        "plt",
        "rom",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/plt-rom.txt.zip",
    (
        "plt",
        "ru",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/plt-ru.txt.zip",
    (
        "plt",
        "shi",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/plt-shi.txt.zip",
    (
        "plt",
        "sk",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/plt-sk.txt.zip",
    (
        "plt",
        "sl",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/plt-sl.txt.zip",
    (
        "plt",
        "sn",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/plt-sn.txt.zip",
    (
        "plt",
        "so",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/plt-so.txt.zip",
    (
        "plt",
        "sq",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/plt-sq.txt.zip",
    (
        "plt",
        "sr",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/plt-sr.txt.zip",
    (
        "plt",
        "ss",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/plt-ss.txt.zip",
    (
        "plt",
        "sv",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/plt-sv.txt.zip",
    (
        "plt",
        "syr",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/plt-syr.txt.zip",
    (
        "plt",
        "te",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/plt-te.txt.zip",
    (
        "plt",
        "th",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/plt-th.txt.zip",
    (
        "plt",
        "tl",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/plt-tl.txt.zip",
    (
        "plt",
        "tmh",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/plt-tmh.txt.zip",
    (
        "plt",
        "tr",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/plt-tr.txt.zip",
    (
        "plt",
        "uk",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/plt-uk.txt.zip",
    (
        "plt",
        "usp",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/plt-usp.txt.zip",
    (
        "plt",
        "vi",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/plt-vi.txt.zip",
    (
        "plt",
        "wal",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/plt-wal.txt.zip",
    (
        "plt",
        "wo",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/plt-wo.txt.zip",
    (
        "plt",
        "xh",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/plt-xh.txt.zip",
    (
        "plt",
        "zh",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/plt-zh.txt.zip",
    (
        "plt",
        "zu",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/plt-zu.txt.zip",
    (
        "pot",
        "ppk",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/pot-ppk.txt.zip",
    (
        "pot",
        "pt",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/pot-pt.txt.zip",
    (
        "pot",
        "quc",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/pot-quc.txt.zip",
    (
        "pot",
        "quw",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/pot-quw.txt.zip",
    (
        "pot",
        "ro",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/pot-ro.txt.zip",
    (
        "pot",
        "rom",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/pot-rom.txt.zip",
    (
        "pot",
        "ru",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/pot-ru.txt.zip",
    (
        "pot",
        "shi",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/pot-shi.txt.zip",
    (
        "pot",
        "sk",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/pot-sk.txt.zip",
    (
        "pot",
        "sl",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/pot-sl.txt.zip",
    (
        "pot",
        "sn",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/pot-sn.txt.zip",
    (
        "pot",
        "so",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/pot-so.txt.zip",
    (
        "pot",
        "sq",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/pot-sq.txt.zip",
    (
        "pot",
        "sr",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/pot-sr.txt.zip",
    (
        "pot",
        "ss",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/pot-ss.txt.zip",
    (
        "pot",
        "sv",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/pot-sv.txt.zip",
    (
        "pot",
        "syr",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/pot-syr.txt.zip",
    (
        "pot",
        "te",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/pot-te.txt.zip",
    (
        "pot",
        "th",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/pot-th.txt.zip",
    (
        "pot",
        "tl",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/pot-tl.txt.zip",
    (
        "pot",
        "tr",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/pot-tr.txt.zip",
    (
        "pot",
        "uk",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/pot-uk.txt.zip",
    (
        "pot",
        "usp",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/pot-usp.txt.zip",
    (
        "pot",
        "vi",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/pot-vi.txt.zip",
    (
        "pot",
        "wal",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/pot-wal.txt.zip",
    (
        "pot",
        "wo",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/pot-wo.txt.zip",
    (
        "pot",
        "xh",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/pot-xh.txt.zip",
    (
        "pot",
        "zh",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/pot-zh.txt.zip",
    (
        "pot",
        "zu",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/pot-zu.txt.zip",
    (
        "ppk",
        "pt",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ppk-pt.txt.zip",
    (
        "ppk",
        "quc",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ppk-quc.txt.zip",
    (
        "ppk",
        "quw",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ppk-quw.txt.zip",
    (
        "ppk",
        "ro",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ppk-ro.txt.zip",
    (
        "ppk",
        "rom",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ppk-rom.txt.zip",
    (
        "ppk",
        "ru",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ppk-ru.txt.zip",
    (
        "ppk",
        "shi",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ppk-shi.txt.zip",
    (
        "ppk",
        "sk",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ppk-sk.txt.zip",
    (
        "ppk",
        "sl",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ppk-sl.txt.zip",
    (
        "ppk",
        "sn",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ppk-sn.txt.zip",
    (
        "ppk",
        "so",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ppk-so.txt.zip",
    (
        "ppk",
        "sq",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ppk-sq.txt.zip",
    (
        "ppk",
        "sr",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ppk-sr.txt.zip",
    (
        "ppk",
        "ss",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ppk-ss.txt.zip",
    (
        "ppk",
        "sv",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ppk-sv.txt.zip",
    (
        "ppk",
        "syr",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ppk-syr.txt.zip",
    (
        "ppk",
        "te",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ppk-te.txt.zip",
    (
        "ppk",
        "th",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ppk-th.txt.zip",
    (
        "ppk",
        "tl",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ppk-tl.txt.zip",
    (
        "ppk",
        "tmh",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ppk-tmh.txt.zip",
    (
        "ppk",
        "tr",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ppk-tr.txt.zip",
    (
        "ppk",
        "uk",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ppk-uk.txt.zip",
    (
        "ppk",
        "usp",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ppk-usp.txt.zip",
    (
        "ppk",
        "vi",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ppk-vi.txt.zip",
    (
        "ppk",
        "wal",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ppk-wal.txt.zip",
    (
        "ppk",
        "wo",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ppk-wo.txt.zip",
    (
        "ppk",
        "xh",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ppk-xh.txt.zip",
    (
        "ppk",
        "zh",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ppk-zh.txt.zip",
    (
        "ppk",
        "zu",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ppk-zu.txt.zip",
    (
        "pt",
        "quc",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/pt-quc.txt.zip",
    (
        "pt",
        "quw",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/pt-quw.txt.zip",
    ("pt", "ro"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/pt-ro.txt.zip",
    (
        "pt",
        "rom",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/pt-rom.txt.zip",
    ("pt", "ru"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/pt-ru.txt.zip",
    (
        "pt",
        "shi",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/pt-shi.txt.zip",
    ("pt", "sk"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/pt-sk.txt.zip",
    ("pt", "sl"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/pt-sl.txt.zip",
    ("pt", "sn"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/pt-sn.txt.zip",
    ("pt", "so"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/pt-so.txt.zip",
    ("pt", "sq"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/pt-sq.txt.zip",
    ("pt", "sr"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/pt-sr.txt.zip",
    ("pt", "ss"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/pt-ss.txt.zip",
    ("pt", "sv"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/pt-sv.txt.zip",
    (
        "pt",
        "syr",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/pt-syr.txt.zip",
    ("pt", "te"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/pt-te.txt.zip",
    ("pt", "th"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/pt-th.txt.zip",
    ("pt", "tl"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/pt-tl.txt.zip",
    (
        "pt",
        "tmh",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/pt-tmh.txt.zip",
    ("pt", "tr"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/pt-tr.txt.zip",
    ("pt", "uk"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/pt-uk.txt.zip",
    (
        "pt",
        "usp",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/pt-usp.txt.zip",
    ("pt", "vi"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/pt-vi.txt.zip",
    (
        "pt",
        "wal",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/pt-wal.txt.zip",
    ("pt", "wo"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/pt-wo.txt.zip",
    ("pt", "xh"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/pt-xh.txt.zip",
    ("pt", "zh"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/pt-zh.txt.zip",
    ("pt", "zu"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/pt-zu.txt.zip",
    (
        "quc",
        "quw",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/quc-quw.txt.zip",
    (
        "quc",
        "ro",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/quc-ro.txt.zip",
    (
        "quc",
        "rom",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/quc-rom.txt.zip",
    (
        "quc",
        "ru",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/quc-ru.txt.zip",
    (
        "quc",
        "shi",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/quc-shi.txt.zip",
    (
        "quc",
        "sk",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/quc-sk.txt.zip",
    (
        "quc",
        "sl",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/quc-sl.txt.zip",
    (
        "quc",
        "sn",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/quc-sn.txt.zip",
    (
        "quc",
        "so",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/quc-so.txt.zip",
    (
        "quc",
        "sq",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/quc-sq.txt.zip",
    (
        "quc",
        "sr",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/quc-sr.txt.zip",
    (
        "quc",
        "ss",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/quc-ss.txt.zip",
    (
        "quc",
        "sv",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/quc-sv.txt.zip",
    (
        "quc",
        "syr",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/quc-syr.txt.zip",
    (
        "quc",
        "te",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/quc-te.txt.zip",
    (
        "quc",
        "th",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/quc-th.txt.zip",
    (
        "quc",
        "tl",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/quc-tl.txt.zip",
    (
        "quc",
        "tmh",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/quc-tmh.txt.zip",
    (
        "quc",
        "tr",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/quc-tr.txt.zip",
    (
        "quc",
        "uk",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/quc-uk.txt.zip",
    (
        "quc",
        "usp",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/quc-usp.txt.zip",
    (
        "quc",
        "vi",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/quc-vi.txt.zip",
    (
        "quc",
        "wal",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/quc-wal.txt.zip",
    (
        "quc",
        "wo",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/quc-wo.txt.zip",
    (
        "quc",
        "xh",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/quc-xh.txt.zip",
    (
        "quc",
        "zh",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/quc-zh.txt.zip",
    (
        "quc",
        "zu",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/quc-zu.txt.zip",
    (
        "quw",
        "ro",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/quw-ro.txt.zip",
    (
        "quw",
        "rom",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/quw-rom.txt.zip",
    (
        "quw",
        "ru",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/quw-ru.txt.zip",
    (
        "quw",
        "shi",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/quw-shi.txt.zip",
    (
        "quw",
        "sk",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/quw-sk.txt.zip",
    (
        "quw",
        "sl",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/quw-sl.txt.zip",
    (
        "quw",
        "sn",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/quw-sn.txt.zip",
    (
        "quw",
        "so",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/quw-so.txt.zip",
    (
        "quw",
        "sq",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/quw-sq.txt.zip",
    (
        "quw",
        "sr",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/quw-sr.txt.zip",
    (
        "quw",
        "ss",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/quw-ss.txt.zip",
    (
        "quw",
        "sv",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/quw-sv.txt.zip",
    (
        "quw",
        "syr",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/quw-syr.txt.zip",
    (
        "quw",
        "te",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/quw-te.txt.zip",
    (
        "quw",
        "th",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/quw-th.txt.zip",
    (
        "quw",
        "tl",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/quw-tl.txt.zip",
    (
        "quw",
        "tmh",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/quw-tmh.txt.zip",
    (
        "quw",
        "tr",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/quw-tr.txt.zip",
    (
        "quw",
        "uk",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/quw-uk.txt.zip",
    (
        "quw",
        "usp",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/quw-usp.txt.zip",
    (
        "quw",
        "vi",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/quw-vi.txt.zip",
    (
        "quw",
        "wal",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/quw-wal.txt.zip",
    (
        "quw",
        "wo",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/quw-wo.txt.zip",
    (
        "quw",
        "xh",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/quw-xh.txt.zip",
    (
        "quw",
        "zh",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/quw-zh.txt.zip",
    (
        "quw",
        "zu",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/quw-zu.txt.zip",
    (
        "ro",
        "rom",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ro-rom.txt.zip",
    ("ro", "ru"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ro-ru.txt.zip",
    (
        "ro",
        "shi",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ro-shi.txt.zip",
    ("ro", "sk"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ro-sk.txt.zip",
    ("ro", "sl"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ro-sl.txt.zip",
    ("ro", "sn"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ro-sn.txt.zip",
    ("ro", "so"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ro-so.txt.zip",
    ("ro", "sq"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ro-sq.txt.zip",
    ("ro", "sr"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ro-sr.txt.zip",
    ("ro", "ss"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ro-ss.txt.zip",
    ("ro", "sv"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ro-sv.txt.zip",
    (
        "ro",
        "syr",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ro-syr.txt.zip",
    ("ro", "te"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ro-te.txt.zip",
    ("ro", "th"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ro-th.txt.zip",
    ("ro", "tl"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ro-tl.txt.zip",
    (
        "ro",
        "tmh",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ro-tmh.txt.zip",
    ("ro", "tr"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ro-tr.txt.zip",
    ("ro", "uk"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ro-uk.txt.zip",
    (
        "ro",
        "usp",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ro-usp.txt.zip",
    ("ro", "vi"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ro-vi.txt.zip",
    (
        "ro",
        "wal",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ro-wal.txt.zip",
    ("ro", "wo"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ro-wo.txt.zip",
    ("ro", "xh"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ro-xh.txt.zip",
    ("ro", "zh"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ro-zh.txt.zip",
    ("ro", "zu"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ro-zu.txt.zip",
    (
        "rom",
        "ru",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/rom-ru.txt.zip",
    (
        "rom",
        "shi",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/rom-shi.txt.zip",
    (
        "rom",
        "sk",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/rom-sk.txt.zip",
    (
        "rom",
        "sl",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/rom-sl.txt.zip",
    (
        "rom",
        "sn",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/rom-sn.txt.zip",
    (
        "rom",
        "so",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/rom-so.txt.zip",
    (
        "rom",
        "sq",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/rom-sq.txt.zip",
    (
        "rom",
        "sr",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/rom-sr.txt.zip",
    (
        "rom",
        "ss",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/rom-ss.txt.zip",
    (
        "rom",
        "sv",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/rom-sv.txt.zip",
    (
        "rom",
        "syr",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/rom-syr.txt.zip",
    (
        "rom",
        "te",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/rom-te.txt.zip",
    (
        "rom",
        "th",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/rom-th.txt.zip",
    (
        "rom",
        "tl",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/rom-tl.txt.zip",
    (
        "rom",
        "tmh",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/rom-tmh.txt.zip",
    (
        "rom",
        "tr",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/rom-tr.txt.zip",
    (
        "rom",
        "uk",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/rom-uk.txt.zip",
    (
        "rom",
        "usp",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/rom-usp.txt.zip",
    (
        "rom",
        "vi",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/rom-vi.txt.zip",
    (
        "rom",
        "wal",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/rom-wal.txt.zip",
    (
        "rom",
        "wo",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/rom-wo.txt.zip",
    (
        "rom",
        "xh",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/rom-xh.txt.zip",
    (
        "rom",
        "zh",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/rom-zh.txt.zip",
    (
        "rom",
        "zu",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/rom-zu.txt.zip",
    (
        "ru",
        "shi",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ru-shi.txt.zip",
    ("ru", "sk"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ru-sk.txt.zip",
    ("ru", "sl"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ru-sl.txt.zip",
    ("ru", "sn"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ru-sn.txt.zip",
    ("ru", "so"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ru-so.txt.zip",
    ("ru", "sq"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ru-sq.txt.zip",
    ("ru", "sr"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ru-sr.txt.zip",
    ("ru", "ss"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ru-ss.txt.zip",
    ("ru", "sv"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ru-sv.txt.zip",
    (
        "ru",
        "syr",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ru-syr.txt.zip",
    ("ru", "te"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ru-te.txt.zip",
    ("ru", "th"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ru-th.txt.zip",
    ("ru", "tl"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ru-tl.txt.zip",
    (
        "ru",
        "tmh",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ru-tmh.txt.zip",
    ("ru", "tr"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ru-tr.txt.zip",
    ("ru", "uk"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ru-uk.txt.zip",
    (
        "ru",
        "usp",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ru-usp.txt.zip",
    ("ru", "vi"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ru-vi.txt.zip",
    (
        "ru",
        "wal",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ru-wal.txt.zip",
    ("ru", "wo"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ru-wo.txt.zip",
    ("ru", "xh"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ru-xh.txt.zip",
    ("ru", "zh"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ru-zh.txt.zip",
    ("ru", "zu"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ru-zu.txt.zip",
    (
        "shi",
        "sk",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/shi-sk.txt.zip",
    (
        "shi",
        "sl",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/shi-sl.txt.zip",
    (
        "shi",
        "sn",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/shi-sn.txt.zip",
    (
        "shi",
        "so",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/shi-so.txt.zip",
    (
        "shi",
        "sq",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/shi-sq.txt.zip",
    (
        "shi",
        "sr",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/shi-sr.txt.zip",
    (
        "shi",
        "ss",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/shi-ss.txt.zip",
    (
        "shi",
        "sv",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/shi-sv.txt.zip",
    (
        "shi",
        "syr",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/shi-syr.txt.zip",
    (
        "shi",
        "te",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/shi-te.txt.zip",
    (
        "shi",
        "th",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/shi-th.txt.zip",
    (
        "shi",
        "tl",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/shi-tl.txt.zip",
    (
        "shi",
        "tmh",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/shi-tmh.txt.zip",
    (
        "shi",
        "tr",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/shi-tr.txt.zip",
    (
        "shi",
        "uk",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/shi-uk.txt.zip",
    (
        "shi",
        "usp",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/shi-usp.txt.zip",
    (
        "shi",
        "vi",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/shi-vi.txt.zip",
    (
        "shi",
        "wal",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/shi-wal.txt.zip",
    (
        "shi",
        "wo",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/shi-wo.txt.zip",
    (
        "shi",
        "xh",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/shi-xh.txt.zip",
    (
        "shi",
        "zh",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/shi-zh.txt.zip",
    (
        "shi",
        "zu",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/shi-zu.txt.zip",
    ("sk", "sl"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/sk-sl.txt.zip",
    ("sk", "sn"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/sk-sn.txt.zip",
    ("sk", "so"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/sk-so.txt.zip",
    ("sk", "sq"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/sk-sq.txt.zip",
    ("sk", "sr"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/sk-sr.txt.zip",
    ("sk", "ss"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/sk-ss.txt.zip",
    ("sk", "sv"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/sk-sv.txt.zip",
    (
        "sk",
        "syr",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/sk-syr.txt.zip",
    ("sk", "te"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/sk-te.txt.zip",
    ("sk", "th"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/sk-th.txt.zip",
    ("sk", "tl"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/sk-tl.txt.zip",
    (
        "sk",
        "tmh",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/sk-tmh.txt.zip",
    ("sk", "tr"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/sk-tr.txt.zip",
    ("sk", "uk"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/sk-uk.txt.zip",
    (
        "sk",
        "usp",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/sk-usp.txt.zip",
    ("sk", "vi"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/sk-vi.txt.zip",
    (
        "sk",
        "wal",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/sk-wal.txt.zip",
    ("sk", "wo"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/sk-wo.txt.zip",
    ("sk", "xh"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/sk-xh.txt.zip",
    ("sk", "zh"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/sk-zh.txt.zip",
    ("sk", "zu"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/sk-zu.txt.zip",
    ("sl", "sn"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/sl-sn.txt.zip",
    ("sl", "so"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/sl-so.txt.zip",
    ("sl", "sq"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/sl-sq.txt.zip",
    ("sl", "sr"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/sl-sr.txt.zip",
    ("sl", "ss"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/sl-ss.txt.zip",
    ("sl", "sv"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/sl-sv.txt.zip",
    (
        "sl",
        "syr",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/sl-syr.txt.zip",
    ("sl", "te"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/sl-te.txt.zip",
    ("sl", "th"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/sl-th.txt.zip",
    ("sl", "tl"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/sl-tl.txt.zip",
    (
        "sl",
        "tmh",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/sl-tmh.txt.zip",
    ("sl", "tr"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/sl-tr.txt.zip",
    ("sl", "uk"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/sl-uk.txt.zip",
    (
        "sl",
        "usp",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/sl-usp.txt.zip",
    ("sl", "vi"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/sl-vi.txt.zip",
    (
        "sl",
        "wal",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/sl-wal.txt.zip",
    ("sl", "wo"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/sl-wo.txt.zip",
    ("sl", "xh"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/sl-xh.txt.zip",
    ("sl", "zh"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/sl-zh.txt.zip",
    ("sl", "zu"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/sl-zu.txt.zip",
    ("sn", "so"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/sn-so.txt.zip",
    ("sn", "sq"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/sn-sq.txt.zip",
    ("sn", "sr"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/sn-sr.txt.zip",
    ("sn", "ss"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/sn-ss.txt.zip",
    ("sn", "sv"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/sn-sv.txt.zip",
    (
        "sn",
        "syr",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/sn-syr.txt.zip",
    ("sn", "te"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/sn-te.txt.zip",
    ("sn", "th"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/sn-th.txt.zip",
    ("sn", "tl"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/sn-tl.txt.zip",
    (
        "sn",
        "tmh",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/sn-tmh.txt.zip",
    ("sn", "tr"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/sn-tr.txt.zip",
    ("sn", "uk"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/sn-uk.txt.zip",
    (
        "sn",
        "usp",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/sn-usp.txt.zip",
    ("sn", "vi"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/sn-vi.txt.zip",
    (
        "sn",
        "wal",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/sn-wal.txt.zip",
    ("sn", "wo"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/sn-wo.txt.zip",
    ("sn", "xh"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/sn-xh.txt.zip",
    ("sn", "zh"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/sn-zh.txt.zip",
    ("sn", "zu"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/sn-zu.txt.zip",
    ("so", "sq"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/so-sq.txt.zip",
    ("so", "sr"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/so-sr.txt.zip",
    ("so", "ss"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/so-ss.txt.zip",
    ("so", "sv"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/so-sv.txt.zip",
    (
        "so",
        "syr",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/so-syr.txt.zip",
    ("so", "te"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/so-te.txt.zip",
    ("so", "th"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/so-th.txt.zip",
    ("so", "tl"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/so-tl.txt.zip",
    (
        "so",
        "tmh",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/so-tmh.txt.zip",
    ("so", "tr"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/so-tr.txt.zip",
    ("so", "uk"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/so-uk.txt.zip",
    (
        "so",
        "usp",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/so-usp.txt.zip",
    ("so", "vi"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/so-vi.txt.zip",
    (
        "so",
        "wal",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/so-wal.txt.zip",
    ("so", "wo"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/so-wo.txt.zip",
    ("so", "xh"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/so-xh.txt.zip",
    ("so", "zh"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/so-zh.txt.zip",
    ("so", "zu"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/so-zu.txt.zip",
    ("sq", "sr"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/sq-sr.txt.zip",
    ("sq", "ss"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/sq-ss.txt.zip",
    ("sq", "sv"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/sq-sv.txt.zip",
    (
        "sq",
        "syr",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/sq-syr.txt.zip",
    ("sq", "te"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/sq-te.txt.zip",
    ("sq", "th"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/sq-th.txt.zip",
    ("sq", "tl"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/sq-tl.txt.zip",
    (
        "sq",
        "tmh",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/sq-tmh.txt.zip",
    ("sq", "tr"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/sq-tr.txt.zip",
    ("sq", "uk"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/sq-uk.txt.zip",
    (
        "sq",
        "usp",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/sq-usp.txt.zip",
    ("sq", "vi"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/sq-vi.txt.zip",
    (
        "sq",
        "wal",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/sq-wal.txt.zip",
    ("sq", "wo"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/sq-wo.txt.zip",
    ("sq", "xh"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/sq-xh.txt.zip",
    ("sq", "zh"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/sq-zh.txt.zip",
    ("sq", "zu"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/sq-zu.txt.zip",
    ("sr", "ss"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/sr-ss.txt.zip",
    ("sr", "sv"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/sr-sv.txt.zip",
    (
        "sr",
        "syr",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/sr-syr.txt.zip",
    ("sr", "te"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/sr-te.txt.zip",
    ("sr", "th"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/sr-th.txt.zip",
    ("sr", "tl"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/sr-tl.txt.zip",
    (
        "sr",
        "tmh",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/sr-tmh.txt.zip",
    ("sr", "tr"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/sr-tr.txt.zip",
    ("sr", "uk"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/sr-uk.txt.zip",
    (
        "sr",
        "usp",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/sr-usp.txt.zip",
    ("sr", "vi"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/sr-vi.txt.zip",
    (
        "sr",
        "wal",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/sr-wal.txt.zip",
    ("sr", "wo"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/sr-wo.txt.zip",
    ("sr", "xh"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/sr-xh.txt.zip",
    ("sr", "zh"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/sr-zh.txt.zip",
    ("sr", "zu"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/sr-zu.txt.zip",
    ("ss", "sv"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ss-sv.txt.zip",
    (
        "ss",
        "syr",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ss-syr.txt.zip",
    ("ss", "te"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ss-te.txt.zip",
    ("ss", "th"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ss-th.txt.zip",
    ("ss", "tl"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ss-tl.txt.zip",
    (
        "ss",
        "tmh",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ss-tmh.txt.zip",
    ("ss", "tr"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ss-tr.txt.zip",
    ("ss", "uk"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ss-uk.txt.zip",
    (
        "ss",
        "usp",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ss-usp.txt.zip",
    ("ss", "vi"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ss-vi.txt.zip",
    (
        "ss",
        "wal",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ss-wal.txt.zip",
    ("ss", "wo"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ss-wo.txt.zip",
    ("ss", "xh"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ss-xh.txt.zip",
    ("ss", "zh"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ss-zh.txt.zip",
    ("ss", "zu"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/ss-zu.txt.zip",
    (
        "sv",
        "syr",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/sv-syr.txt.zip",
    ("sv", "te"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/sv-te.txt.zip",
    ("sv", "th"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/sv-th.txt.zip",
    ("sv", "tl"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/sv-tl.txt.zip",
    (
        "sv",
        "tmh",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/sv-tmh.txt.zip",
    ("sv", "tr"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/sv-tr.txt.zip",
    ("sv", "uk"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/sv-uk.txt.zip",
    (
        "sv",
        "usp",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/sv-usp.txt.zip",
    ("sv", "vi"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/sv-vi.txt.zip",
    (
        "sv",
        "wal",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/sv-wal.txt.zip",
    ("sv", "wo"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/sv-wo.txt.zip",
    ("sv", "xh"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/sv-xh.txt.zip",
    ("sv", "zh"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/sv-zh.txt.zip",
    ("sv", "zu"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/sv-zu.txt.zip",
    (
        "syr",
        "te",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/syr-te.txt.zip",
    (
        "syr",
        "th",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/syr-th.txt.zip",
    (
        "syr",
        "tl",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/syr-tl.txt.zip",
    (
        "syr",
        "tmh",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/syr-tmh.txt.zip",
    (
        "syr",
        "tr",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/syr-tr.txt.zip",
    (
        "syr",
        "uk",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/syr-uk.txt.zip",
    (
        "syr",
        "usp",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/syr-usp.txt.zip",
    (
        "syr",
        "vi",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/syr-vi.txt.zip",
    (
        "syr",
        "wal",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/syr-wal.txt.zip",
    (
        "syr",
        "wo",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/syr-wo.txt.zip",
    (
        "syr",
        "xh",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/syr-xh.txt.zip",
    (
        "syr",
        "zh",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/syr-zh.txt.zip",
    (
        "syr",
        "zu",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/syr-zu.txt.zip",
    ("te", "th"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/te-th.txt.zip",
    ("te", "tl"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/te-tl.txt.zip",
    (
        "te",
        "tmh",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/te-tmh.txt.zip",
    ("te", "tr"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/te-tr.txt.zip",
    ("te", "uk"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/te-uk.txt.zip",
    (
        "te",
        "usp",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/te-usp.txt.zip",
    ("te", "vi"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/te-vi.txt.zip",
    (
        "te",
        "wal",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/te-wal.txt.zip",
    ("te", "wo"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/te-wo.txt.zip",
    ("te", "xh"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/te-xh.txt.zip",
    ("te", "zh"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/te-zh.txt.zip",
    ("te", "zu"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/te-zu.txt.zip",
    ("th", "tl"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/th-tl.txt.zip",
    (
        "th",
        "tmh",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/th-tmh.txt.zip",
    ("th", "tr"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/th-tr.txt.zip",
    ("th", "uk"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/th-uk.txt.zip",
    (
        "th",
        "usp",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/th-usp.txt.zip",
    ("th", "vi"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/th-vi.txt.zip",
    (
        "th",
        "wal",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/th-wal.txt.zip",
    ("th", "wo"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/th-wo.txt.zip",
    ("th", "xh"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/th-xh.txt.zip",
    ("th", "zh"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/th-zh.txt.zip",
    ("th", "zu"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/th-zu.txt.zip",
    (
        "tl",
        "tmh",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/tl-tmh.txt.zip",
    ("tl", "tr"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/tl-tr.txt.zip",
    ("tl", "uk"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/tl-uk.txt.zip",
    (
        "tl",
        "usp",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/tl-usp.txt.zip",
    ("tl", "vi"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/tl-vi.txt.zip",
    (
        "tl",
        "wal",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/tl-wal.txt.zip",
    ("tl", "wo"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/tl-wo.txt.zip",
    ("tl", "xh"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/tl-xh.txt.zip",
    ("tl", "zh"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/tl-zh.txt.zip",
    ("tl", "zu"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/tl-zu.txt.zip",
    (
        "tmh",
        "tr",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/tmh-tr.txt.zip",
    (
        "tmh",
        "uk",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/tmh-uk.txt.zip",
    (
        "tmh",
        "usp",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/tmh-usp.txt.zip",
    (
        "tmh",
        "vi",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/tmh-vi.txt.zip",
    (
        "tmh",
        "wal",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/tmh-wal.txt.zip",
    (
        "tmh",
        "wo",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/tmh-wo.txt.zip",
    (
        "tmh",
        "xh",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/tmh-xh.txt.zip",
    (
        "tmh",
        "zh",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/tmh-zh.txt.zip",
    (
        "tmh",
        "zu",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/tmh-zu.txt.zip",
    ("tr", "uk"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/tr-uk.txt.zip",
    (
        "tr",
        "usp",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/tr-usp.txt.zip",
    ("tr", "vi"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/tr-vi.txt.zip",
    (
        "tr",
        "wal",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/tr-wal.txt.zip",
    ("tr", "wo"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/tr-wo.txt.zip",
    ("tr", "xh"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/tr-xh.txt.zip",
    ("tr", "zh"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/tr-zh.txt.zip",
    ("tr", "zu"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/tr-zu.txt.zip",
    (
        "uk",
        "usp",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/uk-usp.txt.zip",
    ("uk", "vi"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/uk-vi.txt.zip",
    (
        "uk",
        "wal",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/uk-wal.txt.zip",
    ("uk", "wo"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/uk-wo.txt.zip",
    ("uk", "xh"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/uk-xh.txt.zip",
    ("uk", "zh"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/uk-zh.txt.zip",
    ("uk", "zu"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/uk-zu.txt.zip",
    (
        "usp",
        "vi",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/usp-vi.txt.zip",
    (
        "usp",
        "wal",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/usp-wal.txt.zip",
    (
        "usp",
        "wo",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/usp-wo.txt.zip",
    (
        "usp",
        "xh",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/usp-xh.txt.zip",
    (
        "usp",
        "zh",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/usp-zh.txt.zip",
    (
        "usp",
        "zu",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/usp-zu.txt.zip",
    (
        "vi",
        "wal",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/vi-wal.txt.zip",
    ("vi", "wo"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/vi-wo.txt.zip",
    ("vi", "xh"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/vi-xh.txt.zip",
    ("vi", "zh"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/vi-zh.txt.zip",
    ("vi", "zu"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/vi-zu.txt.zip",
    (
        "wal",
        "wo",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/wal-wo.txt.zip",
    (
        "wal",
        "xh",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/wal-xh.txt.zip",
    (
        "wal",
        "zh",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/wal-zh.txt.zip",
    (
        "wal",
        "zu",
    ): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/wal-zu.txt.zip",
    ("wo", "xh"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/wo-xh.txt.zip",
    ("wo", "zh"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/wo-zh.txt.zip",
    ("wo", "zu"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/wo-zu.txt.zip",
    ("xh", "zh"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/xh-zh.txt.zip",
    ("xh", "zu"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/xh-zu.txt.zip",
    ("zh", "zu"): "https://object.pouta.csc.fi/OPUS-bible-uedin/v1/moses/zh-zu.txt.zip",
}


class BibleParaConfig(datasets.BuilderConfig):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, version=datasets.Version(_VERSION, ""), **kwargs)


class BiblePara(datasets.GeneratorBasedBuilder):
    BUILDER_CONFIGS = [
        BibleParaConfig(
            name=f"{lang1}-{lang2}",
            description=f"Translating {lang1} to {lang2} or vice versa",
        )
        for lang1, lang2 in _LANGUAGE_PAIRS.keys()
    ]
    BUILDER_CONFIG_CLASS = BibleParaConfig

    def _info(self):
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=datasets.Features(
                {
                    "id": datasets.Value("string"),
                    "translation": datasets.Translation(languages=tuple(self.config.name.split("-"))),
                },
            ),
            supervised_keys=None,
            homepage=_HOMEPAGE_URL,
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        download_url = _LANGUAGE_PAIRS.get(tuple(self.config.name.split("-")))
        try:
            path = dl_manager.download_and_extract(download_url)
        except ConnectionError:
            path = None
        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                gen_kwargs={"datapath": path},
            )
        ]

    def _generate_examples(self, datapath):
        l1, l2 = self.config.name.split("-")
        if datapath is not None:
            l1_file = _BASE_NAME.format(self.config.name, l1)
            l2_file = _BASE_NAME.format(self.config.name, l2)
            l1_path = os.path.join(datapath, l1_file)
            l2_path = os.path.join(datapath, l2_file)
            try:
                with open(l1_path, encoding="utf-8") as f1, open(l2_path, encoding="utf-8") as f2:
                    for sentence_counter, (x, y) in enumerate(zip(f1, f2)):
                        x = x.strip()
                        y = y.strip()
                        result = (
                            sentence_counter,
                            {
                                "id": str(sentence_counter),
                                "translation": {l1: x, l2: y},
                            },
                        )
                        sentence_counter += 1
                        yield result
            except NotADirectoryError:
                result = (
                    0,
                    {
                        "id": str(0),
                        "translation": {l1: "bad data", l2: "bad data"},
                    },
                )
                yield result
        else:
            print(f"Connection problems for language pair: {self.config.name}")
            result = (
                0,
                {
                    "id": str(0),
                    "translation": {l1: "connection error", l2: "connection error"},
                },
            )
            yield result
