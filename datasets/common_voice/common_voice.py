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
""" Common Voice Dataset"""


import datasets
from datasets.tasks import AutomaticSpeechRecognition


_DATA_URL = "https://voice-prod-bundler-ee1969a6ce8178826482b88e843c335139bd3fb4.s3.amazonaws.com/cv-corpus-6.1-2020-12-11/{}.tar.gz"

_CITATION = """\
@inproceedings{commonvoice:2020,
  author = {Ardila, R. and Branson, M. and Davis, K. and Henretty, M. and Kohler, M. and Meyer, J. and Morais, R. and Saunders, L. and Tyers, F. M. and Weber, G.},
  title = {Common Voice: A Massively-Multilingual Speech Corpus},
  booktitle = {Proceedings of the 12th Conference on Language Resources and Evaluation (LREC 2020)},
  pages = {4211--4215},
  year = 2020
}
"""

_DESCRIPTION = """\
Common Voice is Mozilla's initiative to help teach machines how real people speak.
The dataset currently consists of 7,335 validated hours of speech in 60 languages, but we’re always adding more voices and languages.
"""

_HOMEPAGE = "https://commonvoice.mozilla.org/en/datasets"

_LICENSE = "https://github.com/common-voice/common-voice/blob/main/LICENSE"

_LANGUAGES = {
    "ab": {
        "Language": "Abkhaz",
        "Date": "2020-12-11",
        "Size": "39 MB",
        "Version": "ab_1h_2020-12-11",
        "Validated_Hr_Total": 0.05,
        "Overall_Hr_Total": 1,
        "Number_Of_Voice": 14,
    },
    "ar": {
        "Language": "Arabic",
        "Date": "2020-12-11",
        "Size": "2 GB",
        "Version": "ar_77h_2020-12-11",
        "Validated_Hr_Total": 49,
        "Overall_Hr_Total": 77,
        "Number_Of_Voice": 672,
    },
    "as": {
        "Language": "Assamese",
        "Date": "2020-12-11",
        "Size": "21 MB",
        "Version": "as_0.78h_2020-12-11",
        "Validated_Hr_Total": 0.74,
        "Overall_Hr_Total": 0.78,
        "Number_Of_Voice": 17,
    },
    "br": {
        "Language": "Breton",
        "Date": "2020-12-11",
        "Size": "444 MB",
        "Version": "br_16h_2020-12-11",
        "Validated_Hr_Total": 7,
        "Overall_Hr_Total": 16,
        "Number_Of_Voice": 157,
    },
    "ca": {
        "Language": "Catalan",
        "Date": "2020-12-11",
        "Size": "19 GB",
        "Version": "ca_748h_2020-12-11",
        "Validated_Hr_Total": 623,
        "Overall_Hr_Total": 748,
        "Number_Of_Voice": 5376,
    },
    "cnh": {
        "Language": "Hakha Chin",
        "Date": "2020-12-11",
        "Size": "39 MB",
        "Version": "ab_1h_2020-12-11",
        "Validated_Hr_Total": 0.05,
        "Overall_Hr_Total": 1,
        "Number_Of_Voice": 14,
    },
    "cs": {
        "Language": "Czech",
        "Date": "2020-12-11",
        "Size": "39 MB",
        "Version": "ab_1h_2020-12-11",
        "Validated_Hr_Total": 0.05,
        "Overall_Hr_Total": 1,
        "Number_Of_Voice": 14,
    },
    "cv": {
        "Language": "Chuvash",
        "Date": "2020-12-11",
        "Size": "419 MB",
        "Version": "cv_16h_2020-12-11",
        "Validated_Hr_Total": 4,
        "Overall_Hr_Total": 16,
        "Number_Of_Voice": 92,
    },
    "cy": {
        "Language": "Welsh",
        "Date": "2020-12-11",
        "Size": "3 GB",
        "Version": "cy_124h_2020-12-11",
        "Validated_Hr_Total": 95,
        "Overall_Hr_Total": 124,
        "Number_Of_Voice": 1382,
    },
    "de": {
        "Language": "German",
        "Date": "2020-12-11",
        "Size": "22 GB",
        "Version": "de_836h_2020-12-11",
        "Validated_Hr_Total": 777,
        "Overall_Hr_Total": 836,
        "Number_Of_Voice": 12659,
    },
    "dv": {
        "Language": "Dhivehi",
        "Date": "2020-12-11",
        "Size": "515 MB",
        "Version": "dv_19h_2020-12-11",
        "Validated_Hr_Total": 18,
        "Overall_Hr_Total": 19,
        "Number_Of_Voice": 167,
    },
    "el": {
        "Language": "Greek",
        "Date": "2020-12-11",
        "Size": "364 MB",
        "Version": "el_13h_2020-12-11",
        "Validated_Hr_Total": 6,
        "Overall_Hr_Total": 13,
        "Number_Of_Voice": 118,
    },
    "en": {
        "Language": "English",
        "Date": "2020-12-11",
        "Size": "56 GB",
        "Version": "en_2181h_2020-12-11",
        "Validated_Hr_Total": 1686,
        "Overall_Hr_Total": 2181,
        "Number_Of_Voice": 66173,
    },
    "eo": {
        "Language": "Esperanto",
        "Date": "2020-12-11",
        "Size": "3 GB",
        "Version": "eo_102h_2020-12-11",
        "Validated_Hr_Total": 90,
        "Overall_Hr_Total": 102,
        "Number_Of_Voice": 574,
    },
    "es": {
        "Language": "Spanish",
        "Date": "2020-12-11",
        "Size": "15 GB",
        "Version": "es_579h_2020-12-11",
        "Validated_Hr_Total": 324,
        "Overall_Hr_Total": 579,
        "Number_Of_Voice": 19484,
    },
    "et": {
        "Language": "Estonian",
        "Date": "2020-12-11",
        "Size": "732 MB",
        "Version": "et_27h_2020-12-11",
        "Validated_Hr_Total": 19,
        "Overall_Hr_Total": 27,
        "Number_Of_Voice": 543,
    },
    "eu": {
        "Language": "Basque",
        "Date": "2020-12-11",
        "Size": "3 GB",
        "Version": "eu_131h_2020-12-11",
        "Validated_Hr_Total": 89,
        "Overall_Hr_Total": 131,
        "Number_Of_Voice": 1028,
    },
    "fa": {
        "Language": "Persian",
        "Date": "2020-12-11",
        "Size": "8 GB",
        "Version": "fa_321h_2020-12-11",
        "Validated_Hr_Total": 282,
        "Overall_Hr_Total": 321,
        "Number_Of_Voice": 3655,
    },
    "fi": {
        "Language": "Finnish",
        "Date": "2020-12-11",
        "Size": "48 MB",
        "Version": "fi_1h_2020-12-11",
        "Validated_Hr_Total": 1,
        "Overall_Hr_Total": 1,
        "Number_Of_Voice": 27,
    },
    "fr": {
        "Language": "French",
        "Date": "2020-12-11",
        "Size": "18 GB",
        "Version": "fr_682h_2020-12-11",
        "Validated_Hr_Total": 623,
        "Overall_Hr_Total": 682,
        "Number_Of_Voice": 12953,
    },
    "fy-NL": {
        "Language": "Frisian",
        "Date": "2020-12-11",
        "Size": "1 GB",
        "Version": "fy-NL_46h_2020-12-11",
        "Validated_Hr_Total": 14,
        "Overall_Hr_Total": 46,
        "Number_Of_Voice": 467,
    },
    "ga-IE": {
        "Language": "Irish",
        "Date": "2020-12-11",
        "Size": "149 MB",
        "Version": "ga-IE_5h_2020-12-11",
        "Validated_Hr_Total": 3,
        "Overall_Hr_Total": 5,
        "Number_Of_Voice": 101,
    },
    "hi": {
        "Language": "Hindi",
        "Date": "2020-12-11",
        "Size": "20 MB",
        "Version": "hi_0.8h_2020-12-11",
        "Validated_Hr_Total": 0.54,
        "Overall_Hr_Total": 0.8,
        "Number_Of_Voice": 31,
    },
    "hsb": {
        "Language": "Sorbian, Upper",
        "Date": "2020-12-11",
        "Size": "76 MB",
        "Version": "hsb_2h_2020-12-11",
        "Validated_Hr_Total": 2,
        "Overall_Hr_Total": 2,
        "Number_Of_Voice": 19,
    },
    "hu": {
        "Language": "Hungarian",
        "Date": "2020-12-11",
        "Size": "232 MB",
        "Version": "hu_8h_2020-12-11",
        "Validated_Hr_Total": 8,
        "Overall_Hr_Total": 8,
        "Number_Of_Voice": 47,
    },
    "ia": {
        "Language": "InterLinguia",
        "Date": "2020-12-11",
        "Size": "216 MB",
        "Version": "ia_8h_2020-12-11",
        "Validated_Hr_Total": 6,
        "Overall_Hr_Total": 8,
        "Number_Of_Voice": 36,
    },
    "id": {
        "Language": "Indonesian",
        "Date": "2020-12-11",
        "Size": "454 MB",
        "Version": "id_17h_2020-12-11",
        "Validated_Hr_Total": 9,
        "Overall_Hr_Total": 17,
        "Number_Of_Voice": 219,
    },
    "it": {
        "Language": "Italian",
        "Date": "2020-12-11",
        "Size": "5 GB",
        "Version": "it_199h_2020-12-11",
        "Validated_Hr_Total": 158,
        "Overall_Hr_Total": 199,
        "Number_Of_Voice": 5729,
    },
    "ja": {
        "Language": "Japanese",
        "Date": "2020-12-11",
        "Size": "146 MB",
        "Version": "ja_5h_2020-12-11",
        "Validated_Hr_Total": 3,
        "Overall_Hr_Total": 5,
        "Number_Of_Voice": 235,
    },
    "ka": {
        "Language": "Georgian",
        "Date": "2020-12-11",
        "Size": "99 MB",
        "Version": "ka_3h_2020-12-11",
        "Validated_Hr_Total": 3,
        "Overall_Hr_Total": 3,
        "Number_Of_Voice": 44,
    },
    "kab": {
        "Language": "Kabyle",
        "Date": "2020-12-11",
        "Size": "16 GB",
        "Version": "kab_622h_2020-12-11",
        "Validated_Hr_Total": 525,
        "Overall_Hr_Total": 622,
        "Number_Of_Voice": 1309,
    },
    "ky": {
        "Language": "Kyrgyz",
        "Date": "2020-12-11",
        "Size": "553 MB",
        "Version": "ky_22h_2020-12-11",
        "Validated_Hr_Total": 11,
        "Overall_Hr_Total": 22,
        "Number_Of_Voice": 134,
    },
    "lg": {
        "Language": "Luganda",
        "Date": "2020-12-11",
        "Size": "199 MB",
        "Version": "lg_8h_2020-12-11",
        "Validated_Hr_Total": 3,
        "Overall_Hr_Total": 8,
        "Number_Of_Voice": 76,
    },
    "lt": {
        "Language": "Lithuanian",
        "Date": "2020-12-11",
        "Size": "129 MB",
        "Version": "lt_4h_2020-12-11",
        "Validated_Hr_Total": 2,
        "Overall_Hr_Total": 4,
        "Number_Of_Voice": 30,
    },
    "lv": {
        "Language": "Latvian",
        "Date": "2020-12-11",
        "Size": "199 MB",
        "Version": "lv_7h_2020-12-11",
        "Validated_Hr_Total": 6,
        "Overall_Hr_Total": 7,
        "Number_Of_Voice": 99,
    },
    "mn": {
        "Language": "Mongolian",
        "Date": "2020-12-11",
        "Size": "464 MB",
        "Version": "mn_17h_2020-12-11",
        "Validated_Hr_Total": 11,
        "Overall_Hr_Total": 17,
        "Number_Of_Voice": 376,
    },
    "mt": {
        "Language": "Maltese",
        "Date": "2020-12-11",
        "Size": "405 MB",
        "Version": "mt_15h_2020-12-11",
        "Validated_Hr_Total": 7,
        "Overall_Hr_Total": 15,
        "Number_Of_Voice": 171,
    },
    "nl": {
        "Language": "Dutch",
        "Date": "2020-12-11",
        "Size": "2 GB",
        "Version": "nl_63h_2020-12-11",
        "Validated_Hr_Total": 59,
        "Overall_Hr_Total": 63,
        "Number_Of_Voice": 1012,
    },
    "or": {
        "Language": "Odia",
        "Date": "2020-12-11",
        "Size": "190 MB",
        "Version": "or_7h_2020-12-11",
        "Validated_Hr_Total": 0.87,
        "Overall_Hr_Total": 7,
        "Number_Of_Voice": 34,
    },
    "pa-IN": {
        "Language": "Punjabi",
        "Date": "2020-12-11",
        "Size": "67 MB",
        "Version": "pa-IN_2h_2020-12-11",
        "Validated_Hr_Total": 0.5,
        "Overall_Hr_Total": 2,
        "Number_Of_Voice": 26,
    },
    "pl": {
        "Language": "Polish",
        "Date": "2020-12-11",
        "Size": "3 GB",
        "Version": "pl_129h_2020-12-11",
        "Validated_Hr_Total": 108,
        "Overall_Hr_Total": 129,
        "Number_Of_Voice": 2647,
    },
    "pt": {
        "Language": "Portuguese",
        "Date": "2020-12-11",
        "Size": "2 GB",
        "Version": "pt_63h_2020-12-11",
        "Validated_Hr_Total": 50,
        "Overall_Hr_Total": 63,
        "Number_Of_Voice": 1120,
    },
    "rm-sursilv": {
        "Language": "Romansh Sursilvan",
        "Date": "2020-12-11",
        "Size": "263 MB",
        "Version": "rm-sursilv_9h_2020-12-11",
        "Validated_Hr_Total": 5,
        "Overall_Hr_Total": 9,
        "Number_Of_Voice": 78,
    },
    "rm-vallader": {
        "Language": "Romansh Vallader",
        "Date": "2020-12-11",
        "Size": "103 MB",
        "Version": "rm-vallader_3h_2020-12-11",
        "Validated_Hr_Total": 2,
        "Overall_Hr_Total": 3,
        "Number_Of_Voice": 39,
    },
    "ro": {
        "Language": "Romanian",
        "Date": "2020-12-11",
        "Size": "250 MB",
        "Version": "ro_9h_2020-12-11",
        "Validated_Hr_Total": 6,
        "Overall_Hr_Total": 9,
        "Number_Of_Voice": 130,
    },
    "ru": {
        "Language": "Russian",
        "Date": "2020-12-11",
        "Size": "3 GB",
        "Version": "ru_130h_2020-12-11",
        "Validated_Hr_Total": 111,
        "Overall_Hr_Total": 130,
        "Number_Of_Voice": 1412,
    },
    "rw": {
        "Language": "Kinyarwanda",
        "Date": "2020-12-11",
        "Size": "40 GB",
        "Version": "rw_1510h_2020-12-11",
        "Validated_Hr_Total": 1183,
        "Overall_Hr_Total": 1510,
        "Number_Of_Voice": 410,
    },
    "sah": {
        "Language": "Sakha",
        "Date": "2020-12-11",
        "Size": "173 MB",
        "Version": "sah_6h_2020-12-11",
        "Validated_Hr_Total": 4,
        "Overall_Hr_Total": 6,
        "Number_Of_Voice": 42,
    },
    "sl": {
        "Language": "Slovenian",
        "Date": "2020-12-11",
        "Size": "212 MB",
        "Version": "sl_7h_2020-12-11",
        "Validated_Hr_Total": 5,
        "Overall_Hr_Total": 7,
        "Number_Of_Voice": 82,
    },
    "sv-SE": {
        "Language": "Swedish",
        "Date": "2020-12-11",
        "Size": "402 MB",
        "Version": "sv-SE_15h_2020-12-11",
        "Validated_Hr_Total": 12,
        "Overall_Hr_Total": 15,
        "Number_Of_Voice": 222,
    },
    "ta": {
        "Language": "Tamil",
        "Date": "2020-12-11",
        "Size": "648 MB",
        "Version": "ta_24h_2020-12-11",
        "Validated_Hr_Total": 14,
        "Overall_Hr_Total": 24,
        "Number_Of_Voice": 266,
    },
    "th": {
        "Language": "Thai",
        "Date": "2020-12-11",
        "Size": "325 MB",
        "Version": "th_12h_2020-12-11",
        "Validated_Hr_Total": 8,
        "Overall_Hr_Total": 12,
        "Number_Of_Voice": 182,
    },
    "tr": {
        "Language": "Turkish",
        "Date": "2020-12-11",
        "Size": "592 MB",
        "Version": "tr_22h_2020-12-11",
        "Validated_Hr_Total": 20,
        "Overall_Hr_Total": 22,
        "Number_Of_Voice": 678,
    },
    "tt": {
        "Language": "Tatar",
        "Date": "2020-12-11",
        "Size": "741 MB",
        "Version": "tt_28h_2020-12-11",
        "Validated_Hr_Total": 26,
        "Overall_Hr_Total": 28,
        "Number_Of_Voice": 185,
    },
    "uk": {
        "Language": "Ukrainian",
        "Date": "2020-12-11",
        "Size": "1 GB",
        "Version": "uk_43h_2020-12-11",
        "Validated_Hr_Total": 30,
        "Overall_Hr_Total": 43,
        "Number_Of_Voice": 459,
    },
    "vi": {
        "Language": "Vietnamese",
        "Date": "2020-12-11",
        "Size": "50 MB",
        "Version": "vi_1h_2020-12-11",
        "Validated_Hr_Total": 0.74,
        "Overall_Hr_Total": 1,
        "Number_Of_Voice": 62,
    },
    "vot": {
        "Language": "Votic",
        "Date": "2020-12-11",
        "Size": "7 MB",
        "Version": "vot_0.28h_2020-12-11",
        "Validated_Hr_Total": 0,
        "Overall_Hr_Total": 0.28,
        "Number_Of_Voice": 3,
    },
    "zh-CN": {
        "Language": "Chinese (China)",
        "Date": "2020-12-11",
        "Size": "2 GB",
        "Version": "zh-CN_78h_2020-12-11",
        "Validated_Hr_Total": 56,
        "Overall_Hr_Total": 78,
        "Number_Of_Voice": 3501,
    },
    "zh-HK": {
        "Language": "Chinese (Hong Kong)",
        "Date": "2020-12-11",
        "Size": "3 GB",
        "Version": "zh-HK_100h_2020-12-11",
        "Validated_Hr_Total": 50,
        "Overall_Hr_Total": 100,
        "Number_Of_Voice": 2536,
    },
    "zh-TW": {
        "Language": "Chinese (Taiwan)",
        "Date": "2020-12-11",
        "Size": "2 GB",
        "Version": "zh-TW_78h_2020-12-11",
        "Validated_Hr_Total": 55,
        "Overall_Hr_Total": 78,
        "Number_Of_Voice": 1444,
    },
}


class CommonVoiceConfig(datasets.BuilderConfig):
    """BuilderConfig for CommonVoice."""

    def __init__(self, name, sub_version, **kwargs):
        """
        Args:
          data_dir: `string`, the path to the folder containing the files in the
            downloaded .tar
          citation: `string`, citation for the data set
          url: `string`, url for information about the data set
          **kwargs: keyword arguments forwarded to super.
        """
        self.sub_version = sub_version
        self.language = kwargs.pop("language", None)
        self.date_of_snapshot = kwargs.pop("date", None)
        self.size = kwargs.pop("size", None)
        self.validated_hr_total = kwargs.pop("val_hrs", None)
        self.total_hr_total = kwargs.pop("total_hrs", None)
        self.num_of_voice = kwargs.pop("num_of_voice", None)
        description = f"Common Voice speech to text dataset in {self.language} version {self.sub_version} of {self.date_of_snapshot}. The dataset comprises {self.validated_hr_total} of validated transcribed speech data from {self.num_of_voice} speakers. The dataset has a size of {self.size}"
        super(CommonVoiceConfig, self).__init__(
            name=name, version=datasets.Version("6.1.0", ""), description=description, **kwargs
        )


class CommonVoice(datasets.GeneratorBasedBuilder):

    DEFAULT_WRITER_BATCH_SIZE = 1000
    BUILDER_CONFIGS = [
        CommonVoiceConfig(
            name=lang_id,
            language=_LANGUAGES[lang_id]["Language"],
            sub_version=_LANGUAGES[lang_id]["Version"],
            date=_LANGUAGES[lang_id]["Date"],
            size=_LANGUAGES[lang_id]["Size"],
            val_hrs=_LANGUAGES[lang_id]["Validated_Hr_Total"],
            total_hrs=_LANGUAGES[lang_id]["Overall_Hr_Total"],
            num_of_voice=_LANGUAGES[lang_id]["Number_Of_Voice"],
        )
        for lang_id in _LANGUAGES.keys()
    ]

    def _info(self):
        features = datasets.Features(
            {
                "client_id": datasets.Value("string"),
                "path": datasets.Value("string"),
                "audio": datasets.Audio(sampling_rate=48_000),
                "sentence": datasets.Value("string"),
                "up_votes": datasets.Value("int64"),
                "down_votes": datasets.Value("int64"),
                "age": datasets.Value("string"),
                "gender": datasets.Value("string"),
                "accent": datasets.Value("string"),
                "locale": datasets.Value("string"),
                "segment": datasets.Value("string"),
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
        archive = dl_manager.download(_DATA_URL.format(self.config.name))
        path_to_data = "/".join(["cv-corpus-6.1-2020-12-11", self.config.name])
        path_to_clips = "/".join([path_to_data, "clips"])

        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                gen_kwargs={
                    "files": dl_manager.iter_archive(archive),
                    "filepath": "/".join([path_to_data, "train.tsv"]),
                    "path_to_clips": path_to_clips,
                },
            ),
            datasets.SplitGenerator(
                name=datasets.Split.TEST,
                gen_kwargs={
                    "files": dl_manager.iter_archive(archive),
                    "filepath": "/".join([path_to_data, "test.tsv"]),
                    "path_to_clips": path_to_clips,
                },
            ),
            datasets.SplitGenerator(
                name=datasets.Split.VALIDATION,
                gen_kwargs={
                    "files": dl_manager.iter_archive(archive),
                    "filepath": "/".join([path_to_data, "dev.tsv"]),
                    "path_to_clips": path_to_clips,
                },
            ),
            datasets.SplitGenerator(
                name="other",
                gen_kwargs={
                    "files": dl_manager.iter_archive(archive),
                    "filepath": "/".join([path_to_data, "other.tsv"]),
                    "path_to_clips": path_to_clips,
                },
            ),
            datasets.SplitGenerator(
                name="invalidated",
                gen_kwargs={
                    "files": dl_manager.iter_archive(archive),
                    "filepath": "/".join([path_to_data, "invalidated.tsv"]),
                    "path_to_clips": path_to_clips,
                },
            ),
        ]

    def _generate_examples(self, files, filepath, path_to_clips):
        """Yields examples."""
        data_fields = list(self._info().features.keys())

        # audio is not a header of the csv files
        data_fields.remove("audio")
        path_idx = data_fields.index("path")

        all_field_values = {}
        metadata_found = False
        for path, f in files:
            if path == filepath:
                metadata_found = True
                lines = f.readlines()
                headline = lines[0].decode("utf-8")

                column_names = headline.strip().split("\t")
                assert (
                    column_names == data_fields
                ), f"The file should have {data_fields} as column names, but has {column_names}"
                for line in lines[1:]:
                    field_values = line.decode("utf-8").strip().split("\t")
                    # set full path for mp3 audio file
                    audio_path = "/".join([path_to_clips, field_values[path_idx]])
                    all_field_values[audio_path] = field_values
            elif path.startswith(path_to_clips):
                assert metadata_found, "Found audio clips before the metadata TSV file."
                if not all_field_values:
                    break
                if path in all_field_values:
                    field_values = all_field_values[path]

                    # if data is incomplete, fill with empty values
                    if len(field_values) < len(data_fields):
                        field_values += (len(data_fields) - len(field_values)) * ["''"]

                    result = {key: value for key, value in zip(data_fields, field_values)}

                    # set audio feature
                    result["audio"] = {"path": path, "bytes": f.read()}

                    yield path, result
