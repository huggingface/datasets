# coding=utf-8
# Copyright 2021 The HuggingFace Datasets Authors and the current dataset script contributor.
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
""" OpenSLR Dataset"""

from __future__ import absolute_import, division, print_function

import os
import re
from pathlib import Path

import datasets
from datasets.tasks import AutomaticSpeechRecognition


_DATA_URL = "https://openslr.org/resources/{}"

_CITATION = """\
SLR32:
@inproceedings{van-niekerk-etal-2017,
    title = {{Rapid development of TTS corpora for four South African languages}},
    author = {Daniel van Niekerk and Charl van Heerden and Marelie Davel and Neil Kleynhans and Oddur Kjartansson
    and Martin Jansche and Linne Ha},
    booktitle = {Proc. Interspeech 2017},
    pages = {2178--2182},
    address = {Stockholm, Sweden},
    month = aug,
    year  = {2017},
    URL   = {http://dx.doi.org/10.21437/Interspeech.2017-1139}
}

SLR35, SLR36, SLR52, SLR53, SLR54:
@inproceedings{kjartansson-etal-sltu2018,
    title = {{Crowd-Sourced Speech Corpora for Javanese, Sundanese,  Sinhala, Nepali, and Bangladeshi Bengali}},
    author = {Oddur Kjartansson and Supheakmungkol Sarin and Knot Pipatsrisawat and Martin Jansche and Linne Ha},
    booktitle = {Proc. The 6th Intl. Workshop on Spoken Language Technologies for Under-Resourced Languages (SLTU)},
    year  = {2018},
    address = {Gurugram, India},
    month = aug,
    pages = {52--55},
    URL   = {https://dx.doi.org/10.21437/SLTU.2018-11},
}

SLR41, SLR42, SLR43, SLR44:
@inproceedings{kjartansson-etal-tts-sltu2018,
    title = {{A Step-by-Step Process for Building TTS Voices Using Open Source Data and Framework for Bangla, Javanese,
    Khmer, Nepali, Sinhala, and Sundanese}},
    author = {Keshan Sodimana and Knot Pipatsrisawat and Linne Ha and Martin Jansche and Oddur Kjartansson and Pasindu
    De Silva and Supheakmungkol Sarin},
    booktitle = {Proc. The 6th Intl. Workshop on Spoken Language Technologies for Under-Resourced Languages (SLTU)},
    year  = {2018},
    address = {Gurugram, India},
    month = aug,
    pages = {66--70},
    URL   = {https://dx.doi.org/10.21437/SLTU.2018-14}
}

SLR63, SLR64, SLR65, SLR66, SLR78, SLR79:
@inproceedings{he-etal-2020-open,
  title = {{Open-source Multi-speaker Speech Corpora for Building Gujarati, Kannada, Malayalam, Marathi, Tamil and
  Telugu Speech Synthesis Systems}},
  author = {He, Fei and Chu, Shan-Hui Cathy and Kjartansson, Oddur and Rivera, Clara and Katanova, Anna and Gutkin,
  Alexander and Demirsahin, Isin and Johny, Cibu and Jansche, Martin and Sarin, Supheakmungkol and Pipatsrisawat, Knot},
  booktitle = {Proceedings of The 12th Language Resources and Evaluation Conference (LREC)},
  month = may,
  year = {2020},
  address = {Marseille, France},
  publisher = {European Language Resources Association (ELRA)},
  pages = {6494--6503},
  url = {https://www.aclweb.org/anthology/2020.lrec-1.800},
  ISBN = "{979-10-95546-34-4},
}

SLR69, SLR76, SLR77:
@inproceedings{kjartansson-etal-2020-open,
    title = {{Open-Source High Quality Speech Datasets for Basque, Catalan and Galician}},
    author = {Kjartansson, Oddur and Gutkin, Alexander and Butryna, Alena and Demirsahin, Isin and Rivera, Clara},
    booktitle = {Proceedings of the 1st Joint Workshop on Spoken Language Technologies for Under-resourced languages
    (SLTU) and Collaboration and Computing for Under-Resourced Languages (CCURL)},
    year = {2020},
    pages = {21--27},
    month = may,
    address = {Marseille, France},
    publisher = {European Language Resources association (ELRA)},
    url = {https://www.aclweb.org/anthology/2020.sltu-1.3},
    ISBN = {979-10-95546-35-1},
}

SLR71, SLR71, SLR72, SLR73, SLR74, SLR75:
@inproceedings{guevara-rukoz-etal-2020-crowdsourcing,
    title = {{Crowdsourcing Latin American Spanish for Low-Resource Text-to-Speech}},
    author = {Guevara-Rukoz, Adriana and Demirsahin, Isin and He, Fei and Chu, Shan-Hui Cathy and Sarin,
    Supheakmungkol and Pipatsrisawat, Knot and Gutkin, Alexander and Butryna, Alena and Kjartansson, Oddur},
    booktitle = {Proceedings of The 12th Language Resources and Evaluation Conference (LREC)},
    year = {2020},
    month = may,
    address = {Marseille, France},
    publisher = {European Language Resources Association (ELRA)},
    url = {https://www.aclweb.org/anthology/2020.lrec-1.801},
    pages = {6504--6513},
    ISBN = {979-10-95546-34-4},
}

SLR80
@inproceedings{oo-etal-2020-burmese,
    title = {{Burmese Speech Corpus, Finite-State Text Normalization and Pronunciation Grammars with an Application
    to Text-to-Speech}},
    author = {Oo, Yin May and Wattanavekin, Theeraphol and Li, Chenfang and De Silva, Pasindu and Sarin,
    Supheakmungkol and Pipatsrisawat, Knot and Jansche, Martin and Kjartansson, Oddur and Gutkin, Alexander},
    booktitle = {Proceedings of The 12th Language Resources and Evaluation Conference (LREC)},
    month = may,
    year = {2020},
    pages = "6328--6339",
    address = {Marseille, France},
    publisher = {European Language Resources Association (ELRA)},
    url = {https://www.aclweb.org/anthology/2020.lrec-1.777},
    ISBN = {979-10-95546-34-4},
}

SLR86
@inproceedings{gutkin-et-al-yoruba2020,
    title = {{Developing an Open-Source Corpus of Yoruba Speech}},
    author = {Alexander Gutkin and Işın Demirşahin and Oddur Kjartansson and Clara Rivera and Kọ́lá Túbọ̀sún},
    booktitle = {Proceedings of Interspeech 2020},
    pages = {404--408},
    month = {October},
    year = {2020},
    address = {Shanghai, China},
    publisher = {International Speech and Communication Association (ISCA)},
    doi = {10.21437/Interspeech.2020-1096},
    url = {https://dx.doi.org/10.21437/Interspeech.2020-1096},
}
"""

_DESCRIPTION = """\
OpenSLR is a site devoted to hosting speech and language resources, such as training corpora for speech recognition,
and software related to speech recognition. We intend to be a convenient place for anyone to put resources that
they have created, so that they can be downloaded publicly.
"""

_HOMEPAGE = "https://openslr.org/"

_LICENSE = ""

_RESOURCES = {
    "SLR32": {
        "Language": "South African",
        "LongName": "High quality TTS data for four South African languages (af, st, tn, xh)",
        "Category": "Speech",
        "Summary": "Multi-speaker TTS data for four South African languages, Afrikaans, Sesotho, "
        "Setswana and isiXhosa.",
        "Files": ["af_za.tar.gz", "st_za.tar.gz", "tn_za.tar.gz", "xh_za.tar.gz"],
        "IndexFiles": [
            "https://s3.amazonaws.com/datasets.huggingface.co/openslr/SLR32/af_za/line_index.tsv",
            "https://s3.amazonaws.com/datasets.huggingface.co/openslr/SLR32/st_za/line_index.tsv",
            "https://s3.amazonaws.com/datasets.huggingface.co/openslr/SLR32/tn_za/line_index.tsv",
            "https://s3.amazonaws.com/datasets.huggingface.co/openslr/SLR32/xh_za/line_index.tsv",
        ],
        "DataDirs": ["af_za/za/afr/wavs", "st_za/za/sso/wavs", "tn_za/za/tsn/wavs", "xh_za/za/xho/wavs"],
    },
    "SLR35": {
        "Language": "Javanese",
        "LongName": "Large Javanese ASR training data set",
        "Category": "Speech",
        "Summary": "Javanese ASR training data set containing ~185K utterances",
        "Files": [
            "asr_javanese_0.zip",
            "asr_javanese_1.zip",
            "asr_javanese_2.zip",
            "asr_javanese_3.zip",
            "asr_javanese_4.zip",
            "asr_javanese_5.zip",
            "asr_javanese_6.zip",
            "asr_javanese_7.zip",
            "asr_javanese_8.zip",
            "asr_javanese_9.zip",
            "asr_javanese_a.zip",
            "asr_javanese_b.zip",
            "asr_javanese_c.zip",
            "asr_javanese_d.zip",
            "asr_javanese_e.zip",
            "asr_javanese_f.zip",
        ],
        "IndexFiles": ["asr_javanese/utt_spk_text.tsv"] * 16,
        "DataDirs": ["asr_javanese/data"] * 16,
    },
    "SLR36": {
        "Language": "Sundanese",
        "LongName": "Large Sundanese ASR training data set",
        "Category": "Speech",
        "Summary": "Sundanese ASR training data set containing ~220K utterances",
        "Files": [
            "asr_sundanese_0.zip",
            "asr_sundanese_1.zip",
            "asr_sundanese_2.zip",
            "asr_sundanese_3.zip",
            "asr_sundanese_4.zip",
            "asr_sundanese_5.zip",
            "asr_sundanese_6.zip",
            "asr_sundanese_7.zip",
            "asr_sundanese_8.zip",
            "asr_sundanese_9.zip",
            "asr_sundanese_a.zip",
            "asr_sundanese_b.zip",
            "asr_sundanese_c.zip",
            "asr_sundanese_d.zip",
            "asr_sundanese_e.zip",
            "asr_sundanese_f.zip",
        ],
        "IndexFiles": ["asr_sundanese/utt_spk_text.tsv"] * 16,
        "DataDirs": ["asr_sundanese/data"] * 16,
    },
    "SLR41": {
        "Language": "Javanese",
        "LongName": "High quality TTS data for Javanese",
        "Category": "Speech",
        "Summary": "Multi-speaker TTS data for Javanese (jv-ID)",
        "Files": ["jv_id_female.zip", "jv_id_male.zip"],
        "IndexFiles": ["jv_id_female/line_index.tsv", "jv_id_male/line_index.tsv"],
        "DataDirs": ["jv_id_female/wavs", "jv_id_male/wavs"],
    },
    "SLR42": {
        "Language": "Khmer",
        "LongName": "High quality TTS data for Khmer",
        "Category": "Speech",
        "Summary": "Multi-speaker TTS data for Khmer (km-KH)",
        "Files": ["km_kh_male.zip"],
        "IndexFiles": ["km_kh_male/line_index.tsv"],
        "DataDirs": ["km_kh_male/wavs"],
    },
    "SLR43": {
        "Language": "Nepali",
        "LongName": "High quality TTS data for Nepali",
        "Category": "Speech",
        "Summary": "Multi-speaker TTS data for Nepali (ne-NP)",
        "Files": ["ne_np_female.zip"],
        "IndexFiles": ["ne_np_female/line_index.tsv"],
        "DataDirs": ["ne_np_female/wavs"],
    },
    "SLR44": {
        "Language": "Sundanese",
        "LongName": "High quality TTS data for Sundanese",
        "Category": "Speech",
        "Summary": "Multi-speaker TTS data for Javanese Sundanese (su-ID)",
        "Files": ["su_id_female.zip", "su_id_male.zip"],
        "IndexFiles": ["su_id_female/line_index.tsv", "su_id_male/line_index.tsv"],
        "DataDirs": ["su_id_female/wavs", "su_id_male/wavs"],
    },
    "SLR52": {
        "Language": "Sinhala",
        "LongName": "Large Sinhala ASR training data set",
        "Category": "Speech",
        "Summary": "Sinhala ASR training data set containing ~185K utterances",
        "Files": [
            "asr_sinhala_0.zip",
            "asr_sinhala_1.zip",
            "asr_sinhala_2.zip",
            "asr_sinhala_3.zip",
            "asr_sinhala_4.zip",
            "asr_sinhala_5.zip",
            "asr_sinhala_6.zip",
            "asr_sinhala_7.zip",
            "asr_sinhala_8.zip",
            "asr_sinhala_9.zip",
            "asr_sinhala_a.zip",
            "asr_sinhala_b.zip",
            "asr_sinhala_c.zip",
            "asr_sinhala_d.zip",
            "asr_sinhala_e.zip",
            "asr_sinhala_f.zip",
        ],
        "IndexFiles": ["asr_sinhala/utt_spk_text.tsv"] * 16,
        "DataDirs": ["asr_sinhala/data"] * 16,
    },
    "SLR53": {
        "Language": "Bengali",
        "LongName": "Large Bengali ASR training data set",
        "Category": "Speech",
        "Summary": "Bengali ASR training data set containing ~196K utterances",
        "Files": [
            "asr_bengali_0.zip",
            "asr_bengali_1.zip",
            "asr_bengali_2.zip",
            "asr_bengali_3.zip",
            "asr_bengali_4.zip",
            "asr_bengali_5.zip",
            "asr_bengali_6.zip",
            "asr_bengali_7.zip",
            "asr_bengali_8.zip",
            "asr_bengali_9.zip",
            "asr_bengali_a.zip",
            "asr_bengali_b.zip",
            "asr_bengali_c.zip",
            "asr_bengali_d.zip",
            "asr_bengali_e.zip",
            "asr_bengali_f.zip",
        ],
        "IndexFiles": ["asr_bengali/utt_spk_text.tsv"] * 16,
        "DataDirs": ["asr_bengali/data"] * 16,
    },
    "SLR54": {
        "Language": "Nepali",
        "LongName": "Large Nepali ASR training data set",
        "Category": "Speech",
        "Summary": "Nepali ASR training data set containing ~157K utterances",
        "Files": [
            "asr_nepali_0.zip",
            "asr_nepali_1.zip",
            "asr_nepali_2.zip",
            "asr_nepali_3.zip",
            "asr_nepali_4.zip",
            "asr_nepali_5.zip",
            "asr_nepali_6.zip",
            "asr_nepali_7.zip",
            "asr_nepali_8.zip",
            "asr_nepali_9.zip",
            "asr_nepali_a.zip",
            "asr_nepali_b.zip",
            "asr_nepali_c.zip",
            "asr_nepali_d.zip",
            "asr_nepali_e.zip",
            "asr_nepali_f.zip",
        ],
        "IndexFiles": ["asr_nepali/utt_spk_text.tsv"] * 16,
        "DataDirs": ["asr_nepali/data"] * 16,
    },
    "SLR63": {
        "Language": "Malayalam",
        "LongName": "Crowdsourced high-quality Malayalam multi-speaker speech data set",
        "Category": "Speech",
        "Summary": "Data set which contains recordings of native speakers of Malayalam",
        "Files": ["ml_in_female.zip", "ml_in_male.zip"],
        "IndexFiles": ["line_index.tsv", "line_index.tsv"],
        "DataDirs": ["", ""],
    },
    "SLR64": {
        "Language": "Marathi",
        "LongName": "Crowdsourced high-quality Marathi multi-speaker speech data set",
        "Category": "Speech",
        "Summary": "Data set which contains recordings of native speakers of Marathi",
        "Files": ["mr_in_female.zip"],
        "IndexFiles": ["line_index.tsv"],
        "DataDirs": ["", ""],
    },
    "SLR65": {
        "Language": "Tamil",
        "LongName": "Crowdsourced high-quality Tamil multi-speaker speech data set",
        "Category": "Speech",
        "Summary": "Data set which contains recordings of native speakers of Tamil",
        "Files": ["ta_in_female.zip", "ta_in_male.zip"],
        "IndexFiles": ["line_index.tsv", "line_index.tsv"],
        "DataDirs": ["", ""],
    },
    "SLR66": {
        "Language": "Telugu",
        "LongName": "Crowdsourced high-quality Telugu multi-speaker speech data set",
        "Category": "Speech",
        "Summary": "Data set which contains recordings of native speakers of Telugu",
        "Files": ["te_in_female.zip", "te_in_male.zip"],
        "IndexFiles": ["line_index.tsv", "line_index.tsv"],
        "DataDirs": ["", ""],
    },
    "SLR69": {
        "Language": "Catalan",
        "LongName": "Crowdsourced high-quality Catalan speech data set",
        "Category": "Speech",
        "Summary": "Data set which contains recordings of Catalan",
        "Files": ["ca_es_female.zip", "ca_es_male.zip"],
        "IndexFiles": ["line_index.tsv", "line_index.tsv"],
        "DataDirs": ["", ""],
    },
    "SLR70": {
        "Language": "Nigerian English",
        "LongName": "Crowdsourced high-quality Nigerian English speech data set",
        "Category": "Speech",
        "Summary": "Data set which contains recordings of Nigerian English",
        "Files": ["en_ng_female.zip", "en_ng_male.zip"],
        "IndexFiles": ["line_index.tsv", "line_index.tsv"],
        "DataDirs": ["", ""],
    },
    "SLR71": {
        "Language": "Chilean Spanish",
        "LongName": "Crowdsourced high-quality Chilean Spanish speech data set",
        "Category": "Speech",
        "Summary": "Data set which contains recordings of Chilean Spanish",
        "Files": ["es_cl_female.zip", "es_cl_male.zip"],
        "IndexFiles": ["line_index.tsv", "line_index.tsv"],
        "DataDirs": ["", ""],
    },
    "SLR72": {
        "Language": "Columbian Spanish",
        "LongName": "Crowdsourced high-quality Columbian Spanish speech data set",
        "Category": "Speech",
        "Summary": "Data set which contains recordings of Columbian Spanish",
        "Files": ["es_co_female.zip", "es_co_male.zip"],
        "IndexFiles": ["line_index.tsv", "line_index.tsv"],
        "DataDirs": ["", ""],
    },
    "SLR73": {
        "Language": "Peruvian Spanish",
        "LongName": "Crowdsourced high-quality Peruvian Spanish speech data set",
        "Category": "Speech",
        "Summary": "Data set which contains recordings of Peruvian Spanish",
        "Files": ["es_pe_female.zip", "es_pe_male.zip"],
        "IndexFiles": ["line_index.tsv", "line_index.tsv"],
        "DataDirs": ["", ""],
    },
    "SLR74": {
        "Language": "Puerto Rico Spanish",
        "LongName": "Crowdsourced high-quality Puerto Rico Spanish speech data set",
        "Category": "Speech",
        "Summary": "Data set which contains recordings of Puerto Rico Spanish",
        "Files": ["es_pr_female.zip"],
        "IndexFiles": ["line_index.tsv"],
        "DataDirs": [""],
    },
    "SLR75": {
        "Language": "Venezuelan Spanish",
        "LongName": "Crowdsourced high-quality Venezuelan Spanish speech data set",
        "Category": "Speech",
        "Summary": "Data set which contains recordings of Venezuelan Spanish",
        "Files": ["es_ve_female.zip", "es_ve_male.zip"],
        "IndexFiles": ["line_index.tsv", "line_index.tsv"],
        "DataDirs": ["", ""],
    },
    "SLR76": {
        "Language": "Basque",
        "LongName": "Crowdsourced high-quality Basque speech data set",
        "Category": "Speech",
        "Summary": "Data set which contains recordings of Basque",
        "Files": ["eu_es_female.zip", "eu_es_male.zip"],
        "IndexFiles": ["line_index.tsv", "line_index.tsv"],
        "DataDirs": ["", ""],
    },
    "SLR77": {
        "Language": "Galician",
        "LongName": "Crowdsourced high-quality Galician speech data set",
        "Category": "Speech",
        "Summary": "Data set which contains recordings of Galician",
        "Files": ["gl_es_female.zip", "gl_es_male.zip"],
        "IndexFiles": ["line_index.tsv", "line_index.tsv"],
        "DataDirs": ["", ""],
    },
    "SLR78": {
        "Language": "Gujarati",
        "LongName": "Crowdsourced high-quality Gujarati multi-speaker speech data set",
        "Category": "Speech",
        "Summary": "Data set which contains recordings of native speakers of Gujarati",
        "Files": ["gu_in_female.zip", "gu_in_male.zip"],
        "IndexFiles": ["line_index.tsv", "line_index.tsv"],
        "DataDirs": ["", ""],
    },
    "SLR79": {
        "Language": "Kannada",
        "LongName": "Crowdsourced high-quality Kannada multi-speaker speech data set",
        "Category": "Speech",
        "Summary": "Data set which contains recordings of native speakers of Kannada",
        "Files": ["kn_in_female.zip", "kn_in_male.zip"],
        "IndexFiles": ["line_index.tsv", "line_index.tsv"],
        "DataDirs": ["", ""],
    },
    "SLR80": {
        "Language": "Burmese",
        "LongName": "Crowdsourced high-quality Burmese speech data set",
        "Category": "Speech",
        "Summary": "Data set which contains recordings of Burmese",
        "Files": ["my_mm_female.zip"],
        "IndexFiles": ["line_index.tsv"],
        "DataDirs": [""],
    },
    "SLR86": {
        "Language": "Yoruba",
        "LongName": "Crowdsourced high-quality Yoruba speech data set",
        "Category": "Speech",
        "Summary": "Data set which contains recordings of Yoruba",
        "Files": ["yo_ng_female.zip", "yo_ng_male.zip"],
        "IndexFiles": ["line_index.tsv", "line_index.tsv"],
        "DataDirs": ["", ""],
    },
}


class OpenSlrConfig(datasets.BuilderConfig):
    """BuilderConfig for OpenSlr."""

    def __init__(self, name, **kwargs):
        """
        Args:
          data_dir: `string`, the path to the folder containing the files in the
            downloaded .tar
          citation: `string`, citation for the data set
          url: `string`, url for information about the data set
          **kwargs: keyword arguments forwarded to super.
        """
        self.language = kwargs.pop("language", None)
        self.long_name = kwargs.pop("long_name", None)
        self.category = kwargs.pop("category", None)
        self.summary = kwargs.pop("summary", None)
        self.files = kwargs.pop("files", None)
        self.index_files = kwargs.pop("index_files", None)
        self.data_dirs = kwargs.pop("data_dirs", None)
        description = (
            f"Open Speech and Language Resources dataset in {self.language}. Name: {self.name}, "
            f"Summary: {self.summary}."
        )
        super(OpenSlrConfig, self).__init__(name=name, description=description, **kwargs)


class OpenSlr(datasets.GeneratorBasedBuilder):
    DEFAULT_WRITER_BATCH_SIZE = 32

    BUILDER_CONFIGS = [
        OpenSlrConfig(
            name=resource_id,
            language=_RESOURCES[resource_id]["Language"],
            long_name=_RESOURCES[resource_id]["LongName"],
            category=_RESOURCES[resource_id]["Category"],
            summary=_RESOURCES[resource_id]["Summary"],
            files=_RESOURCES[resource_id]["Files"],
            index_files=_RESOURCES[resource_id]["IndexFiles"],
            data_dirs=_RESOURCES[resource_id]["DataDirs"],
        )
        for resource_id in _RESOURCES.keys()
    ]

    def _info(self):
        features = datasets.Features(
            {
                "path": datasets.Value("string"),
                "audio": datasets.Audio(sampling_rate=48_000),
                "sentence": datasets.Value("string"),
            }
        )

        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=features,
            supervised_keys=None,
            homepage=_HOMEPAGE,
            license=_LICENSE,
            citation=_CITATION,
            task_templates=[
                AutomaticSpeechRecognition(audio_file_path_column="path", transcription_column="sentence")
            ],
        )

    def _split_generators(self, dl_manager):
        """Returns SplitGenerators."""
        resource_number = self.config.name.replace("SLR", "")
        urls = [f"{_DATA_URL.format(resource_number)}/{file}" for file in self.config.files]
        if urls[0].endswith(".zip"):
            dl_paths = dl_manager.download_and_extract(urls)
            path_to_indexs = [os.path.join(path, f"{self.config.index_files[i]}") for i, path in enumerate(dl_paths)]
            path_to_datas = [os.path.join(path, f"{self.config.data_dirs[i]}") for i, path in enumerate(dl_paths)]
            archives = None
        else:
            archives = dl_manager.download(urls)
            path_to_indexs = dl_manager.download(self.config.index_files)
            path_to_datas = self.config.data_dirs

        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                gen_kwargs={
                    "path_to_indexs": path_to_indexs,
                    "path_to_datas": path_to_datas,
                    "archive_files": [dl_manager.iter_archive(archive) for archive in archives] if archives else None,
                },
            ),
        ]

    def _generate_examples(self, path_to_indexs, path_to_datas, archive_files):
        """Yields examples."""

        counter = -1
        if self.config.name in ["SLR35", "SLR36", "SLR52", "SLR53", "SLR54"]:
            sentence_index = {}
            for i, path_to_index in enumerate(path_to_indexs):
                with open(path_to_index, encoding="utf-8") as f:
                    lines = f.readlines()
                    for id_, line in enumerate(lines):
                        field_values = re.split(r"\t\t?", line.strip())
                        filename, user_id, sentence = field_values
                        sentence_index[filename] = sentence
                for path_to_data in sorted(Path(path_to_datas[i]).rglob("*.flac")):
                    filename = path_to_data.stem
                    if path_to_data.stem not in sentence_index:
                        continue
                    path = str(path_to_data.resolve())
                    sentence = sentence_index[filename]
                    counter += 1
                    yield counter, {"path": path, "audio": path, "sentence": sentence}
        elif self.config.name in ["SLR32"]:  # use archives
            for path_to_index, path_to_data, files in zip(path_to_indexs, path_to_datas, archive_files):
                sentences = {}
                with open(path_to_index, encoding="utf-8") as f:
                    for line in f:
                        # Following regexs are needed to normalise the lines, since the datasets
                        # are not always consistent and have bugs:
                        line = re.sub(r"\t[^\t]*\t", "\t", line.strip())
                        field_values = re.split(r"\t\t?", line)
                        if len(field_values) != 2:
                            continue
                        filename, sentence = field_values
                        # set absolute path for audio file
                        path = f"{path_to_data}/{filename}.wav"
                        sentences[path] = sentence
                for path, f in files:
                    if path.startswith(path_to_data):
                        counter += 1
                        audio = {"path": path, "bytes": f.read()}
                        yield counter, {"path": path, "audio": audio, "sentence": sentences[path]}
        else:
            for i, path_to_index in enumerate(path_to_indexs):
                with open(path_to_index, encoding="utf-8") as f:
                    lines = f.readlines()
                    for id_, line in enumerate(lines):
                        # Following regexs are needed to normalise the lines, since the datasets
                        # are not always consistent and have bugs:
                        line = re.sub(r"\t[^\t]*\t", "\t", line.strip())
                        field_values = re.split(r"\t\t?", line)
                        if len(field_values) != 2:
                            continue
                        filename, sentence = field_values
                        # set absolute path for audio file
                        path = os.path.join(path_to_datas[i], f"{filename}.wav")
                        counter += 1
                        yield counter, {"path": path, "audio": path, "sentence": sentence}
