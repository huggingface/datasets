# coding=utf-8
# Copyright 2022 The Google and HuggingFace Datasets Authors and the current dataset script contributor.
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

import glob
import os
import datasets
from datasets.tasks import AutomaticSpeechRecognition

""" XTREME-S Dataset"""

"""TODO(xtreme): Add a description here."""

# TODO(xtreme-s): BibTeX citation
_CITATION = """\
"""

# TODO(xtrem-s): Correct later
_DESCRIPTION = """\
The Cross-lingual TRansfer Evaluation of Multilingual Encoders for Speech (XTREME-S) benchmark is a benchmark designed to evaluate speech representations across languages, tasks, domains and data regimes. It covers XX typologically diverse languages eight total downstream tasks grouped in four families: speech recognition, translation, classification and retrieval.
"""

_ID_TO_LANG = {
    "en": "english",
    "de": "german",
    "nl": "dutch",
    "fr": "french",
    "es": "spanish",
    "it": "italian",
    "pt": "portuguese",
    "pl": "polish",
}

_BABEL_LANG = ["as", "tl", "sw", "lo", "ka"]
_MLS_LANG = ["nl", "en", "fr", "de", "it", "pl", "pt", "es"]
_VOXPOPULI_LANG = []  # TODO(PVP)

_COVOST2_TO_EN_LANG = [f"{source}.en" for source in ["fr", "de", "es", "ca", "it", "ru", "zh", "pt", "fa", "et", "mn", "nl", "tr", "ar", "sv", "lv", "sl", "ta", "ja", "id", "cy"]]
_COVOST2_FROM_EN_LANG = [f"en.{target}" for target in ["de", "ca", "zh", "fa", "et", "mn", "tr", "ar", "sw", "lv", "sl", "ta", "ja", "id", "cy"]]

_COVOST2_LANG = _COVOST2_FROM_EN_LANG + _COVOST2_TO_EN_LANG

_FLORES_LANG = []  # TODO(PVP)
_MINDS_14_LANG = []  # TODO(PVP)

_ALL_LANG = set(_BABEL_LANG + _MLS_LANG + _VOXPOPULI_LANG + _COVOST2_LANG + _FLORES_LANG + _MINDS_14_LANG)

_ALL_DATASET_CONFIGS = {
    "babel": _BABEL_LANG,
    "mls": _MLS_LANG,
    "covost2": _COVOST2_LANG,
    "fleurs": _FLORES_LANG,
    "minds14": _MINDS_14_LANG
}

# _ALL_LANG = ["ar", "as", "ca", "cs", "cy", "da", "de", "en", "en", "en", "en", "es", "et", "fa", "fi", "fr", "hr", "hu", "id", "it", "ja", "ka", "ko", "lo", "lt", "lv", "mn", "nl", "pl", "pt", "ro", "ru", "sk", "sl", "sv", "sw", "ta", "tl", "tr", "zh"]

_ALL_CONFIGS = []  # e.g. mls.en, covost.en.sv, ...
for sub_data, langs in _ALL_DATASET_CONFIGS.items():
    for lang in langs:
        _ALL_CONFIGS.append(f"{sub_data}.{lang}")


_DESCRIPTIONS = {  # TOOD(PVP)
    "babel": "",
    "mls": """\
Multilingual LibriSpeech (MLS) dataset is a large multilingual corpus suitable for speech research. The dataset is derived from read audiobooks from LibriVox and consists of 8 languages - English, German, Dutch, Spanish, French, Italian, Portuguese, Polish.
""",
    "covost2": "",
    "fleurs": "",
    "minds14": "",
}

_CITATIONS = {  # TOOD(PVP)
    "babel": "",
    "mls": """\
@article{Pratap2020MLSAL,
  title={MLS: A Large-Scale Multilingual Dataset for Speech Research},
  author={Vineel Pratap and Qiantong Xu and Anuroop Sriram and Gabriel Synnaeve and Ronan Collobert},
  journal={ArXiv},
  year={2020},
  volume={abs/2012.03411}
}
""",
    "covost2": "",
    "fleurs": "",
    "minds14": "",
}

_HOMEPAGE_URLS = {  # TOOD(PVP)
    "babel": "",
    "mls": "http://www.openslr.org/94",
    "covost2": "",
    "fleurs": "",
    "minds14": "",
}

_DATA_URLS = {  # TOOD(PVP)
    "babel": "",
    "mls": "https://dl.fbaipublicfiles.com/mls/mls_{}.tar.gz",
    "covost2": "",
    "fleurs": "",
    "minds14": "",
}

_DATA_FORMAT = {
    "babel": {k: "" for k in _BABEL_LANG},
    "mls": {k: (_ID_TO_LANG[k],) for k in _MLS_LANG},
    "covost2": {k: "" for k in _COVOST2_LANG},
    "fleurs": {k: "" for k in _FLORES_LANG},
    "minds14": {k: "" for k in _MINDS_14_LANG},
}


class XtremeSConfig(datasets.BuilderConfig):
    """BuilderConfig for xtreme-s"""

    def __init__(self, name, dataset_name, lang_name, description, citation, homepage, data_format, data_url):
        super(XtremeSConfig, self).__init__(
            name=self.name, version=datasets.Version("1.0.0", ""), description=self.description
        )
        self.name = name
        self.dataset_name = dataset_name
        self.lang_name = lang_name
        self.description = description
        self.citation = citation
        self.homepage = homepage
        self.data_format = data_format
        self.data_url = data_url.format(*self.data_format)


def _build_config(name):
    dataset_name = name.split(".")[0]
    lang_name = ".".join(name.split(".")[1:])

    return XtremeSConfig(
        name=name,
        dataset_name=dataset_name,
        lang_name=lang_name,
        description=_DESCRIPTIONS[dataset_name],
        citation=_CITATIONS[dataset_name],
        homepage=_HOMEPAGE_URLS[dataset_name],
        data_format=_DATA_FORMAT[dataset_name][lang_name],
        data_url=_DATA_URLS[dataset_name],
    )


class XtremeS(datasets.GeneratorBasedBuilder):

    DEFAULT_WRITER_BATCH_SIZE = 1000
    BUILDER_CONFIGS = [_build_config(name) for name in _ALL_CONFIGS]

    def _info(self):
        task_templates = None
        if self.config.dataset_name in ["mls", "voxpopuli", "babel"]:
            # asr
            features = datasets.Features(
                {
                    "path": datasets.Value("string"),
                    "audio": datasets.Audio(sampling_rate=16_000),
                    "target": datasets.Value("string"),
                }
            )
            task_templates = [AutomaticSpeechRecognition(audio_file_path_column="path", transcription_column="text")]
        elif self.config.dataset_name in ["covost2"]:
            # speech translation
            features = datasets.Features(
                {
                    "path": datasets.Value("string"),
                    "audio": datasets.Audio(sampling_rate=48_000),
                    "transcription": datasets.Value("string"),
                    "target": datasets.Value("string"),
                }
            )
        elif self.config.dataset_name == "fleurs":
            # language identification
            # TODO(PVP/Anton)
            pass

        elif self.dataset_name == "minds14":
            # intent classification
            # TODO(PVP/Anton)
            pass

        return datasets.DatasetInfo(
            description=self.config.description + "\n" + _DESCRIPTION,
            features=features,
            supervised_keys=("audio", "target"),
            homepage=self.config.homepage,
            citation=self.config.citation + "\n" + _CITATION,
            task_templates=task_templates,
        )

    def _split_generators(self, dl_manager):
        archive_path = dl_manager.download_and_extract(self.config.data_url)
        data_path = os.path.join(archive_path, f"mls_{_ID_TO_LANG[self.config.lang_name]}")

        if self.config.dataset_name == "mls":
            return self._split_generators_mls(data_path)

    def _generate_examples(self, *args, **kwargs):
        if self.config.dataset_name == "mls":
            yield from self._generate_mls_examples(*args, **kwargs)

    # MLS
    def _split_generators_mls(self, data_path):
        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN, gen_kwargs={"data_dir": os.path.join(data_path, "train"), "sub_folder": "limited_supervision/9hr"}
            ),
            datasets.SplitGenerator(
                name=datasets.Split.VALIDATION, gen_kwargs={"data_dir": os.path.join(data_path, "dev")}
            ),
            datasets.SplitGenerator(
                name=datasets.Split.TEST, gen_kwargs={"data_dir": os.path.join(data_path, "test")}
            ),
        ]

    def _generate_mls_examples(self, data_dir, sub_folder=""):
        """Generate examples from a Multilingual LibriSpeech data dir."""
        transcript_path = os.path.join(data_dir, "transcripts.txt")
        key = 0
        all_ids = None

        # find relevant ids
        sub_path = os.path.join(data_dir, sub_folder)
        all_ids_paths = glob.glob(sub_path + "/*/*.txt") + glob.glob(sub_path + "/*.txt")
        all_ids = []
        for path in all_ids_paths:
            with open(path, "r", encoding="utf-8") as f:
                all_ids += [line.strip() for line in f.readlines()]

        all_ids = set(all_ids)

        with open(transcript_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                _id, transcript = line.split("\t")

                if _id not in all_ids:
                    # filter-out audios not contained in the 9/10h version
                    continue

                audio_file = f"{_id}.flac"
                speaker_id, chapter_id = [int(el) for el in _id.split("_")[:2]]

                yield key, {
                    "path": os.path.join(data_dir, "audio", str(speaker_id), str(chapter_id), audio_file),
                    "audio": os.path.join(data_dir, "audio", str(speaker_id), str(chapter_id), audio_file),
                    "target": transcript,
                }
                key += 1
