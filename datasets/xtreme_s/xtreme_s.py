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

import csv
import glob
import os
from pathlib import Path
from tqdm import tqdm
from typing import Tuple, Dict, List

from ast import literal_eval
from collections import defaultdict
import pandas as pd

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
_VOXPOPULI_LANG = ["en", "de", "fr", "es", "pl", "it", "ro", "hu", "cs", "nl", "fi", "hr", "sk", "sl"]

# fmt: off
_COVOST2_TO_EN_LANG = [
    f"{source}.en"
    for source in [
        "fr", "de", "es", "ca", "it", "ru", "zh", "pt", "fa", "et", "mn", "nl", "tr", "ar", "sv", "lv", "sl", "ta", "ja", "id", "cy",
    ]
]
_COVOST2_FROM_EN_LANG = [
    f"en.{target}"
    for target in [
        "de", "ca", "zh", "fa", "et", "mn", "tr", "ar", "sw", "lv", "sl", "ta", "ja", "id", "cy",
    ]
]
_COVOST2_LANG = _COVOST2_FROM_EN_LANG + _COVOST2_TO_EN_LANG

_MINDS_14_LANG = [
    "aux-en", "cs-CZ", "de-DE", "en-AU", "en-GB", "en-US", "es-ES", "fr-FR", "it-IT", "ko-KR", "nl-NL", "pl-PL", "pt-PT", "ru-RU", "zh-CN",
]
_FLORES_LANG = []  # TODO(PVP)

_ALL_LANG = set(_BABEL_LANG + _MLS_LANG + _VOXPOPULI_LANG + _COVOST2_LANG + _FLORES_LANG + _MINDS_14_LANG)

_ALL_DATASET_CONFIGS = {
    "babel": _BABEL_LANG,
    "mls": _MLS_LANG,
    "voxpopuli": _VOXPOPULI_LANG,
    "covost2": _COVOST2_LANG,
    "fleurs": _FLORES_LANG,
    "minds14": _MINDS_14_LANG,
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
    "voxpopuli": "",
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
    "voxpopuli": "",
    "covost2": "",
    "fleurs": "",
    "minds14": "",
}

_HOMEPAGE_URLS = {  # TOOD(PVP)
    "babel": "",
    "mls": "http://www.openslr.org/94",
    "voxpopuli": "",
    "covost2": "",
    "fleurs": "",
    "minds14": "",
}

_VOXPOPULI_AUDIO_URLS = ['https://dl.fbaipublicfiles.com/voxpopuli/audios/original_2009.tar', 'https://dl.fbaipublicfiles.com/voxpopuli/audios/original_2010.tar', 'https://dl.fbaipublicfiles.com/voxpopuli/audios/original_2011.tar', 'https://dl.fbaipublicfiles.com/voxpopuli/audios/original_2012.tar', 'https://dl.fbaipublicfiles.com/voxpopuli/audios/original_2013.tar', 'https://dl.fbaipublicfiles.com/voxpopuli/audios/original_2014.tar', 'https://dl.fbaipublicfiles.com/voxpopuli/audios/original_2015.tar', 'https://dl.fbaipublicfiles.com/voxpopuli/audios/original_2016.tar', 'https://dl.fbaipublicfiles.com/voxpopuli/audios/original_2017.tar', 'https://dl.fbaipublicfiles.com/voxpopuli/audios/original_2018.tar', 'https://dl.fbaipublicfiles.com/voxpopuli/audios/original_2019.tar', 'https://dl.fbaipublicfiles.com/voxpopuli/audios/original_2020.tar']

_DATA_URLS = {  # TODO(PVP)
    "babel": "",
    "mls": ["https://dl.fbaipublicfiles.com/mls/mls_{}.tar.gz"],
    "voxpopuli": _VOXPOPULI_AUDIO_URLS + ["https://dl.fbaipublicfiles.com/voxpopuli/annotations/asr/asr_{}.tsv.gz"],
    "covost2": [
        "https://voice-prod-bundler-ee1969a6ce8178826482b88e843c335139bd3fb4.s3.amazonaws.com/cv-corpus-4-2019-12-10/{}.tar.gz",
        "https://dl.fbaipublicfiles.com/covost/covost_v2.{}_{}.tsv.tar.gz",
    ],
    "fleurs": "",
    "minds14": ["http://poly-public-data.s3.amazonaws.com/MInDS-14/MInDS-14.zip"],
}
# fmt: on


class XtremeSConfig(datasets.BuilderConfig):
    """BuilderConfig for xtreme-s"""

    def __init__(self, name, dataset_name, lang_name, description, citation, homepage, data_urls):
        super(XtremeSConfig, self).__init__(
            name=self.name,
            version=datasets.Version("1.0.0", ""),
            description=self.description,
        )
        self.name = name
        self.dataset_name = dataset_name
        self.lang_name = lang_name
        self.description = description
        self.citation = citation
        self.homepage = homepage
        self.data_urls = data_urls


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
        data_urls=_DATA_URLS[dataset_name],
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
        elif self.config.dataset_name == "minds14":
            features = datasets.Features(
                {
                    "path": datasets.Value("string"),
                    "audio": datasets.Audio(sampling_rate=8_000),
                    "transcription": datasets.Value("string"),
                    "english_transcription": datasets.Value("string"),
                    "target": datasets.ClassLabel(
                        names=[
                            "abroad",
                            "address",
                            "app_error",
                            "atm_limit",
                            "balance",
                            "business_loan",
                            "card_issues",
                            "cash_deposit",
                            "direct_debit",
                            "freeze",
                            "high_value_payment",
                            "joint_account",
                            "latest_transactions",
                            "pay_bill",
                        ]
                    ),
                }
            )
        elif self.config.dataset_name == "fleurs":
            # language identification
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

    def _split_generators(self, *args, **kwargs):
        if self.config.dataset_name == "mls":
            return self._mls_split_generators(*args, **kwargs)
        elif self.config.dataset_name == "voxpopuli":
            return self._voxpopuli_split_generators(*args, **kwargs)
        elif self.config.dataset_name == "covost2":
            return self._covost_2_split_generators(*args, **kwargs)
        elif self.config.dataset_name == "minds14":
            return self._minds14_split_generators(*args, **kwargs)

    def _generate_examples(self, *args, **kwargs):
        if self.config.dataset_name == "mls":
            yield from self._mls_generate_examples(*args, **kwargs)
        elif self.config.dataset_name == "voxpopuli":
            yield from self._voxpopuli_generate_examples(*args, **kwargs)
        elif self.config.dataset_name == "covost2":
            yield from self._covost_2_generate_examples(*args, **kwargs)
        elif self.config.dataset_name == "minds14":
            yield from self._minds14_generate_examples(*args, **kwargs)

    # MLS
    def _mls_split_generators(self, dl_manager):
        lang = _ID_TO_LANG[self.config.lang_name]

        archive_path = dl_manager.download_and_extract(self.config.data_urls[0].format(lang))
        data_path = os.path.join(archive_path, f"mls_{_ID_TO_LANG[self.config.lang_name]}")

        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                gen_kwargs={
                    "data_dir": os.path.join(data_path, "train"),
                    "sub_folder": "limited_supervision/9hr",
                },
            ),
            datasets.SplitGenerator(
                name=datasets.Split.VALIDATION,
                gen_kwargs={"data_dir": os.path.join(data_path, "dev")},
            ),
            datasets.SplitGenerator(
                name=datasets.Split.TEST,
                gen_kwargs={"data_dir": os.path.join(data_path, "test")},
            ),
        ]

    def _mls_generate_examples(self, data_dir, sub_folder=""):
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

    # Voxpopuli
    def _voxpopuli_split_generators(self, dl_manager):
        # TODO(PVP) - need to add warning here that even for a single
        # language ALL files need to be downloaded because all langs archive_path
        # mixed in single audio files
        if hasattr(dl_manager, "download_config"):
            # last file is text file
            dl_manager.download_config.num_proc = len(_VOXPOPULI_AUDIO_URLS)

        extracted_audio_data_list = dl_manager.download_and_extract(self.config.data_urls[:-1])
        extracted_audio_data_dict = {str(i + 2009): extracted_audio_data_list[i] for i in range(len(extracted_audio_data_list))}

        extracted_text_data = dl_manager.download_and_extract(self.config.data_urls[-1].format(self.config.lang_name))

        # TODO(PVP) - add print statement that this takes a while or into tqdm
        # split audio data and save in cached extracted folders so that it
        # only has to be done once
        split_audio_data = self._voxpopuli_split_audio(extracted_audio_data_dict, extracted_text_data)

        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                gen_kwargs={
                    "audio_data": split_audio_data,
                    "text_data": extracted_text_data,
                    "split": "train",
                },
            ),
            datasets.SplitGenerator(
                name=datasets.Split.VALIDATION,
                gen_kwargs={
                    "audio_data": split_audio_data,
                    "text_data": extracted_text_data,
                    "split": "dev",
                },
            ),
            datasets.SplitGenerator(
                name=datasets.Split.TEST,
                gen_kwargs={
                    "audio_data": split_audio_data,
                    "text_data": extracted_text_data,
                    "split": "test",
                },
            ),
        ]

    def _voxpopuli_split_audio(self, audio_data_dict, text_data, sub_folder="original"):
        """This function is heavily inspired from https://github.com/facebookresearch/voxpopuli/blob/main/voxpopuli/get_asr_data.py"""

        def cut_session(info: Tuple[str, Dict[str, List[Tuple[float, float]]]]) -> None:
            # this function requires both torch, and torchaudio to be installed
            in_path, out_path_to_timestamps = info

            has_to_load_audio = False
            for out_path, timestamps in out_path_to_timestamps.items():
                if not os.path.exists(out_path):
                    has_to_load_audio = True

            if not has_to_load_audio:
                return

            try:
                import torchaudio
                import torch
            except ImportError as e:
                raise ValueError(
                    "Loading voxpopuli requires `torchaudio` to be installed."
                    "You can install torchaudio with `pip install torchaudio`." + e
                )

            waveform, sr = torchaudio.load(in_path)
            duration = waveform.size(1)
            for out_path, timestamps in out_path_to_timestamps.items():
                if not os.path.exists(out_path):
                    segment = torch.cat(
                        [waveform[:, int(s * sr): min(int(t * sr), duration)]
                         for s, t in timestamps],
                        dim=1
                    )
                    torchaudio.save(out_path, segment, sr)

        output_paths = {}

        time_stamps = defaultdict(dict)
        with open(text_data, encoding="utf-8") as csv_file:
            csv_reader = csv.reader(csv_file, delimiter="|")
            for row in csv_reader:
                id_, _, session_id, _, _, _, _, _, _, _, _, time_stamp, split, gender = row
                if split not in ["train", "dev", "test"]:
                    continue

                year = session_id[:4]
                audio_data = audio_data_dict[year]

                split_audio_output_folder = os.path.join(audio_data, "transcribed_data", self.config.lang_name)
                Path(split_audio_output_folder).mkdir(exist_ok=True, parents=True)
                output_paths[id_] = os.path.join(split_audio_output_folder, f"{session_id}-{id_}.ogg")

                audio_sample_path = os.path.join(audio_data, sub_folder, year, f"{session_id}_original.ogg")
                time_stamps[audio_sample_path][output_paths[id_]] = [(t[0], t[1]) for t in literal_eval(time_stamp)]

        time_stamps = tqdm(list(time_stamps.items()))
        # TODO(PVP): add note here that audio is cut and that this might take a while
        for time_stamp in time_stamps:
            cut_session(time_stamp)

        return output_paths

    def _voxpopuli_generate_examples(self, audio_data, text_data, split):
        key = 0
        with open(text_data, encoding="utf-8") as csv_file:
            csv_reader = csv.reader(csv_file, delimiter="|")
            next(csv_reader)
            for row in csv_reader:
                id_, _, _, _, _, transcript, _, _, _, _, _, _, split_of_sample, _ = row
                if split_of_sample != split:
                    continue

                yield key, {
                    "path": audio_data[id_],
                    "audio": audio_data[id_],
                    "target": transcript,
                }
                key += 1

    # Covost2
    def _covost_2_split_generators(self, dl_manager):
        source_lang, target_lang = self.config.lang_name.split(".")
        audio_url, translation_url = tuple(self.config.data_urls)

        audio_data = dl_manager.download_and_extract(audio_url.format(source_lang))
        text_data = dl_manager.download_and_extract(translation_url.format(source_lang, target_lang))

        covost_tsv_path = os.path.join(text_data, f"covost_v2.{source_lang}_{target_lang}.tsv")
        cv_tsv_path = os.path.join(audio_data, "validated.tsv")

        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                gen_kwargs={
                    "source_path": audio_data,
                    "covost_tsv_path": covost_tsv_path,
                    "cv_tsv_path": cv_tsv_path,
                    "split": "train",
                },
            ),
            datasets.SplitGenerator(
                name=datasets.Split.VALIDATION,
                gen_kwargs={
                    "source_path": audio_data,
                    "covost_tsv_path": covost_tsv_path,
                    "cv_tsv_path": cv_tsv_path,
                    "split": "dev",
                },
            ),
            datasets.SplitGenerator(
                name=datasets.Split.TEST,
                gen_kwargs={
                    "source_path": audio_data,
                    "covost_tsv_path": covost_tsv_path,
                    "cv_tsv_path": cv_tsv_path,
                    "split": "test",
                },
            ),
        ]

    def _covost_2_generate_examples(self, source_path, covost_tsv_path, cv_tsv_path, split):
        def _load_df_from_tsv(path):
            return pd.read_csv(
                path,
                sep="\t",
                header=0,
                encoding="utf-8",
                escapechar="\\",
                quoting=csv.QUOTE_NONE,
                na_filter=False,
            )

        covost_tsv = _load_df_from_tsv(covost_tsv_path)
        cv_tsv = _load_df_from_tsv(cv_tsv_path)

        df = pd.merge(
            left=cv_tsv[["path", "sentence", "client_id"]],
            right=covost_tsv[["path", "translation", "split"]],
            how="inner",
            on="path",
        )

        if split == "train":
            df = df[(df["split"] == "train") | (df["split"] == "train_covost")]
        else:
            df = df[df["split"] == split]

        for i, row in df.iterrows():
            yield i, {
                "path": os.path.join(source_path, "clips", row["path"]),
                "audio": os.path.join(source_path, "clips", row["path"]),
                "transcription": row["sentence"],
                "target": row["translation"],
            }

    # MINDS-14
    def _minds14_split_generators(self, dl_manager):
        archive_path = dl_manager.download_and_extract(self.config.data_urls[0])
        audio_path = dl_manager.extract(os.path.join(archive_path, "MInDS-14", "audio.zip"))
        text_path = dl_manager.extract(os.path.join(archive_path, "MInDS-14", "text.zip"))

        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                gen_kwargs={
                    "audio_path": audio_path,
                    "text_path": os.path.join(text_path, "{}.csv".format(self.config.lang_name)),
                },
            ),
        ]

    def _minds14_generate_examples(self, audio_path, text_path):
        key = 0
        with open(text_path, encoding="utf-8") as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=",", skipinitialspace=True)
            next(csv_reader)
            for row in csv_reader:
                file_path, transcription, english_transcription, target = row
                audio_path = os.path.join(audio_path, *file_path.split("/"))
                yield key, {
                    "path": audio_path,
                    "audio": audio_path,
                    "transcription": transcription,
                    "english_transcription": english_transcription,
                    "target": target.lower(),
                }
                key += 1
