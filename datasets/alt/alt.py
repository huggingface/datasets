#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Asian Language Treebank (ALT) Project"""


import os

import datasets


_CITATION = """\
@inproceedings{riza2016introduction,
  title={Introduction of the asian language treebank},
  author={Riza, Hammam and Purwoadi, Michael and Uliniansyah, Teduh and Ti, Aw Ai and Aljunied, Sharifah Mahani and Mai, Luong Chi and Thang, Vu Tat and Thai, Nguyen Phuong and Chea, Vichet and Sam, Sethserey and others},
  booktitle={2016 Conference of The Oriental Chapter of International Committee for Coordination and Standardization of Speech Databases and Assessment Techniques (O-COCOSDA)},
  pages={1--6},
  year={2016},
  organization={IEEE}
}
"""

_HOMEPAGE = "https://www2.nict.go.jp/astrec-att/member/mutiyama/ALT/"

_DESCRIPTION = """\
The ALT project aims to advance the state-of-the-art Asian natural language processing (NLP) techniques through the open collaboration for developing and using ALT. It was first conducted by NICT and UCSY as described in Ye Kyaw Thu, Win Pa Pa, Masao Utiyama, Andrew Finch and Eiichiro Sumita (2016). Then, it was developed under ASEAN IVO as described in this Web page. The process of building ALT began with sampling about 20,000 sentences from English Wikinews, and then these sentences were translated into the other languages. ALT now has 13 languages: Bengali, English, Filipino, Hindi, Bahasa Indonesia, Japanese, Khmer, Lao, Malay, Myanmar (Burmese), Thai, Vietnamese, Chinese (Simplified Chinese).
"""

_URLs = {
    "alt": "https://www2.nict.go.jp/astrec-att/member/mutiyama/ALT/ALT-Parallel-Corpus-20191206.zip",
    "alt-en": "https://www2.nict.go.jp/astrec-att/member/mutiyama/ALT/English-ALT-20170107.zip",
    "alt-jp": "https://www2.nict.go.jp/astrec-att/member/mutiyama/ALT/Japanese-ALT-20170330.zip",
    "alt-my": "https://www2.nict.go.jp/astrec-att/member/mutiyama/ALT/my-alt-190530.zip",
    "alt-my-transliteration": "https://www2.nict.go.jp/astrec-att/member/mutiyama/ALT/my-en-transliteration.zip",
    "alt-my-west-transliteration": "https://www2.nict.go.jp/astrec-att/member/mutiyama/ALT/western-myanmar-transliteration.zip",
    "alt-km": "https://www2.nict.go.jp/astrec-att/member/mutiyama/ALT/km-nova-181101.zip",
}

_SPLIT = {
    "train": "https://www2.nict.go.jp/astrec-att/member/mutiyama/ALT/URL-train.txt",
    "dev": "https://www2.nict.go.jp/astrec-att/member/mutiyama/ALT/URL-dev.txt",
    "test": "https://www2.nict.go.jp/astrec-att/member/mutiyama/ALT/URL-test.txt",
}

_WIKI_URL = "https://www2.nict.go.jp/astrec-att/member/mutiyama/ALT/ALT-Parallel-Corpus-20191206/URL.txt"


class AltParallelConfig(datasets.BuilderConfig):
    """BuilderConfig for ALT."""

    def __init__(self, languages, **kwargs):
        """BuilderConfig for ALT.

        Args:
            for the `datasets.features.text.TextEncoder` used for the features feature.

            languages: languages that will be used for translation. it should be one of the
            **kwargs: keyword arguments forwarded to super.
        """

        name = "alt-parallel"

        description = "ALT Parallel Corpus"
        super(AltParallelConfig, self).__init__(
            name=name,
            description=description,
            version=datasets.Version("1.0.0", ""),
            **kwargs,
        )

        available_langs = set(
            ["bg", "en", "en_tok", "fil", "hi", "id", "ja", "khm", "lo", "ms", "my", "th", "vi", "zh"]
        )
        for language in languages:
            assert language in available_langs

        self.languages = languages


class Alt(datasets.GeneratorBasedBuilder):
    """Asian Language Treebank (ALT) Project"""

    BUILDER_CONFIGS = [
        AltParallelConfig(
            languages=["bg", "en", "en_tok", "fil", "hi", "id", "ja", "khm", "lo", "ms", "my", "th", "vi", "zh"]
        ),
        datasets.BuilderConfig(name="alt-en", version=datasets.Version("1.0.0"), description="English ALT"),
        datasets.BuilderConfig(name="alt-jp", version=datasets.Version("1.0.0"), description="Japanese ALT"),
        datasets.BuilderConfig(name="alt-my", version=datasets.Version("1.0.0"), description="Myanmar ALT"),
        datasets.BuilderConfig(name="alt-km", version=datasets.Version("1.0.0"), description="Khmer ALT"),
        datasets.BuilderConfig(
            name="alt-my-transliteration",
            version=datasets.Version("1.0.0"),
            description="Myanmar-English Transliteration Dataset",
        ),
        datasets.BuilderConfig(
            name="alt-my-west-transliteration",
            version=datasets.Version("1.0.0"),
            description="Latin-Myanmar Transliteration Dataset",
        ),
    ]

    DEFAULT_CONFIG_NAME = "alt-parallel"

    def _info(self):
        if self.config.name.startswith("alt-parallel"):
            features = datasets.Features(
                {
                    "SNT.URLID": datasets.Value("string"),
                    "SNT.URLID.SNTID": datasets.Value("string"),
                    "url": datasets.Value("string"),
                    "translation": datasets.features.Translation(languages=self.config.languages),
                }
            )
        elif self.config.name == "alt-en":
            features = datasets.Features(
                {
                    "SNT.URLID": datasets.Value("string"),
                    "SNT.URLID.SNTID": datasets.Value("string"),
                    "url": datasets.Value("string"),
                    "status": datasets.Value("string"),
                    "value": datasets.Value("string"),
                }
            )
        elif self.config.name == "alt-jp":
            features = datasets.Features(
                {
                    "SNT.URLID": datasets.Value("string"),
                    "SNT.URLID.SNTID": datasets.Value("string"),
                    "url": datasets.Value("string"),
                    "status": datasets.Value("string"),
                    "value": datasets.Value("string"),
                    "word_alignment": datasets.Value("string"),
                    "jp_tokenized": datasets.Value("string"),
                    "en_tokenized": datasets.Value("string"),
                }
            )
        elif self.config.name == "alt-my":
            features = datasets.Features(
                {
                    "SNT.URLID": datasets.Value("string"),
                    "SNT.URLID.SNTID": datasets.Value("string"),
                    "url": datasets.Value("string"),
                    "value": datasets.Value("string"),
                }
            )
        elif self.config.name == "alt-my-transliteration":
            features = datasets.Features(
                {
                    "en": datasets.Value("string"),
                    "my": datasets.Sequence(datasets.Value("string")),
                }
            )
        elif self.config.name == "alt-my-west-transliteration":
            features = datasets.Features(
                {
                    "en": datasets.Value("string"),
                    "my": datasets.Sequence(datasets.Value("string")),
                }
            )
        elif self.config.name == "alt-km":
            features = datasets.Features(
                {
                    "SNT.URLID": datasets.Value("string"),
                    "SNT.URLID.SNTID": datasets.Value("string"),
                    "url": datasets.Value("string"),
                    "km_pos_tag": datasets.Value("string"),
                    "km_tokenized": datasets.Value("string"),
                }
            )
        else:
            raise

        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=features,
            supervised_keys=None,
            homepage=_HOMEPAGE,
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        if self.config.name.startswith("alt-parallel"):
            data_path = dl_manager.download_and_extract(_URLs["alt"])
        else:
            data_path = dl_manager.download_and_extract(_URLs[self.config.name])

        if self.config.name == "alt-my-transliteration" or self.config.name == "alt-my-west-transliteration":
            return [
                datasets.SplitGenerator(
                    name=datasets.Split.TRAIN,
                    gen_kwargs={"basepath": data_path, "split": None},
                )
            ]
        else:
            data_split = {}
            for k in _SPLIT:
                data_split[k] = dl_manager.download_and_extract(_SPLIT[k])

            return [
                datasets.SplitGenerator(
                    name=datasets.Split.TRAIN,
                    gen_kwargs={"basepath": data_path, "split": data_split["train"]},
                ),
                datasets.SplitGenerator(
                    name=datasets.Split.VALIDATION,
                    gen_kwargs={"basepath": data_path, "split": data_split["dev"]},
                ),
                datasets.SplitGenerator(
                    name=datasets.Split.TEST,
                    gen_kwargs={"basepath": data_path, "split": data_split["test"]},
                ),
            ]

    def _generate_examples(self, basepath, split=None):
        allow_urls = {}
        if split is not None:
            with open(split, encoding="utf-8") as fin:
                for line in fin:
                    sp = line.strip().split("\t")
                    urlid = sp[0].replace("URL.", "")
                    allow_urls[urlid] = {"SNT.URLID": urlid, "url": sp[1]}

        data = {}
        if self.config.name.startswith("alt-parallel"):
            files = self.config.languages

            data = {}
            for lang in files:
                file_path = os.path.join(basepath, "ALT-Parallel-Corpus-20191206", f"data_{lang}.txt")
                fin = open(file_path, encoding="utf-8")
                for line in fin:
                    line = line.strip()
                    sp = line.split("\t")

                    _, urlid, sntid = sp[0].split(".")
                    if urlid not in allow_urls:
                        continue

                    if sntid not in data:
                        data[sntid] = {}
                        data[sntid]["SNT.URLID"] = urlid
                        data[sntid]["SNT.URLID.SNTID"] = sntid
                        data[sntid]["url"] = allow_urls[urlid]["url"]
                        data[sntid]["translation"] = {}

                    # Note that Japanese and Myanmar texts have empty sentence fields in this release.
                    if len(sp) >= 2:
                        data[sntid]["translation"][lang] = sp[1]

                fin.close()

        elif self.config.name == "alt-en":
            data = {}
            for fname in ["English-ALT-Draft.txt", "English-ALT-Reviewed.txt"]:
                file_path = os.path.join(basepath, "English-ALT-20170107", fname)
                fin = open(file_path, encoding="utf-8")
                for line in fin:
                    line = line.strip()
                    sp = line.split("\t")

                    _, urlid, sntid = sp[0].split(".")
                    if urlid not in allow_urls:
                        continue

                    d = {
                        "SNT.URLID": urlid,
                        "SNT.URLID.SNTID": sntid,
                        "url": allow_urls[urlid]["url"],
                        "status": None,
                        "value": None,
                    }

                    d["value"] = sp[1]
                    if fname == "English-ALT-Draft.txt":
                        d["status"] = "draft"
                    else:
                        d["status"] = "reviewed"

                    data[sntid] = d
                fin.close()
        elif self.config.name == "alt-jp":
            data = {}
            for fname in ["Japanese-ALT-Draft.txt", "Japanese-ALT-Reviewed.txt"]:
                file_path = os.path.join(basepath, "Japanese-ALT-20170330", fname)
                fin = open(file_path, encoding="utf-8")
                for line in fin:
                    line = line.strip()
                    sp = line.split("\t")
                    _, urlid, sntid = sp[0].split(".")
                    if urlid not in allow_urls:
                        continue

                    d = {
                        "SNT.URLID": urlid,
                        "SNT.URLID.SNTID": sntid,
                        "url": allow_urls[urlid]["url"],
                        "value": None,
                        "status": None,
                        "word_alignment": None,
                        "en_tokenized": None,
                        "jp_tokenized": None,
                    }

                    d["value"] = sp[1]
                    if fname == "Japanese-ALT-Draft.txt":
                        d["status"] = "draft"
                    else:
                        d["status"] = "reviewed"
                    data[sntid] = d
                fin.close()

            keys = {
                "word_alignment": "word-alignment/data_ja.en-ja",
                "en_tokenized": "word-alignment/data_ja.en-tok",
                "jp_tokenized": "word-alignment/data_ja.ja-tok",
            }
            for k in keys:
                file_path = os.path.join(basepath, "Japanese-ALT-20170330", keys[k])
                fin = open(file_path, encoding="utf-8")
                for line in fin:
                    line = line.strip()
                    sp = line.split("\t")

                    # Note that Japanese and Myanmar texts have empty sentence fields in this release.
                    if len(sp) < 2:
                        continue

                    _, urlid, sntid = sp[0].split(".")
                    if urlid not in allow_urls:
                        continue

                    if sntid in data:

                        data[sntid][k] = sp[1]
                fin.close()

        elif self.config.name == "alt-my":
            data = {}
            for fname in ["data"]:
                file_path = os.path.join(basepath, "my-alt-190530", fname)
                fin = open(file_path, encoding="utf-8")
                for line in fin:
                    line = line.strip()
                    sp = line.split("\t")
                    _, urlid, sntid = sp[0].split(".")
                    if urlid not in allow_urls:
                        continue

                    data[sntid] = {
                        "SNT.URLID": urlid,
                        "SNT.URLID.SNTID": sntid,
                        "url": allow_urls[urlid]["url"],
                        "value": sp[1],
                    }
                fin.close()

        elif self.config.name == "alt-km":
            data = {}
            for fname in ["data_km.km-tag.nova", "data_km.km-tok.nova"]:
                file_path = os.path.join(basepath, "km-nova-181101", fname)
                fin = open(file_path, encoding="utf-8")
                for line in fin:
                    line = line.strip()
                    sp = line.split("\t")
                    _, urlid, sntid = sp[0].split(".")
                    if urlid not in allow_urls:
                        continue

                    k = "km_pos_tag" if fname == "data_km.km-tag.nova" else "km_tokenized"
                    if sntid in data:
                        data[sntid][k] = sp[1]
                    else:
                        data[sntid] = {
                            "SNT.URLID": urlid,
                            "SNT.URLID.SNTID": sntid,
                            "url": allow_urls[urlid]["url"],
                            "km_pos_tag": None,
                            "km_tokenized": None,
                        }
                        data[sntid][k] = sp[1]
                fin.close()

        elif self.config.name == "alt-my-transliteration":
            file_path = os.path.join(basepath, "my-en-transliteration", "data.txt")
            # Need to set errors='ignore' because of the unknown error
            # UnicodeDecodeError: 'utf-8' codec can't decode byte 0xff in position 0: invalid start byte
            # It might due to some issues related to Myanmar alphabets
            fin = open(file_path, encoding="utf-8", errors="ignore")
            _id = 0
            for line in fin:
                line = line.strip()

                # I don't know why there are \x00 between |||. They don't show in the editor.
                line = line.replace("\x00", "")
                sp = line.split("|||")

                # When I read data, it seems to have empty sentence betweem the actual sentence. Don't know why?
                if len(sp) < 2:
                    continue

                data[_id] = {"en": sp[0].strip(), "my": [sp[1].strip()]}
                _id += 1
            fin.close()
        elif self.config.name == "alt-my-west-transliteration":
            file_path = os.path.join(basepath, "western-myanmar-transliteration", "321.txt")
            # Need to set errors='ignore' because of the unknown error
            # UnicodeDecodeError: 'utf-8' codec can't decode byte 0xff in position 0: invalid start byte
            # It might due to some issues related to Myanmar alphabets
            fin = open(file_path, encoding="utf-8", errors="ignore")
            _id = 0
            for line in fin:
                line = line.strip()
                line = line.replace("\x00", "")
                sp = line.split("|||")

                data[_id] = {"en": sp[0].strip(), "my": [k.strip() for k in sp[1].split("|")]}
                _id += 1
            fin.close()

        _id = 1
        for k in data:
            yield _id, data[k]
            _id += 1
