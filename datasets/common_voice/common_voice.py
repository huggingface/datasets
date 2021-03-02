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

from __future__ import absolute_import, division, print_function

import os

import datasets


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
        "Size": "39 MB",
        "Version": "ab_1h_2020-12-11",
        "Validated_Hr_Total": 0.05,
        "Overall_Hr_Total": 1,
        "Number_Of_Voice": 14,
    },
    "as": {
        "Language": "Assamese",
        "Date": "2020-12-11",
        "Size": "39 MB",
        "Version": "ab_1h_2020-12-11",
        "Validated_Hr_Total": 0.05,
        "Overall_Hr_Total": 1,
        "Number_Of_Voice": 14,
    },
    "br": {
        "Language": "Breton",
        "Date": "2020-12-11",
        "Size": "39 MB",
        "Version": "ab_1h_2020-12-11",
        "Validated_Hr_Total": 0.05,
        "Overall_Hr_Total": 1,
        "Number_Of_Voice": 14,
    },
    "ca": {
        "Language": "Catalan",
        "Date": "2020-12-11",
        "Size": "39 MB",
        "Version": "ab_1h_2020-12-11",
        "Validated_Hr_Total": 0.05,
        "Overall_Hr_Total": 1,
        "Number_Of_Voice": 14,
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
        "Size": "39 MB",
        "Version": "ab_1h_2020-12-11",
        "Validated_Hr_Total": 0.05,
        "Overall_Hr_Total": 1,
        "Number_Of_Voice": 14,
    },
    "cy": {
        "Language": "Welsh",
        "Date": "2020-12-11",
        "Size": "39 MB",
        "Version": "ab_1h_2020-12-11",
        "Validated_Hr_Total": 0.05,
        "Overall_Hr_Total": 1,
        "Number_Of_Voice": 14,
    },
    "de": {
        "Language": "German",
        "Date": "2020-12-11",
        "Size": "39 MB",
        "Version": "ab_1h_2020-12-11",
        "Validated_Hr_Total": 0.05,
        "Overall_Hr_Total": 1,
        "Number_Of_Voice": 14,
    },
    "dv": {
        "Language": "Dhivehi",
        "Date": "2020-12-11",
        "Size": "39 MB",
        "Version": "ab_1h_2020-12-11",
        "Validated_Hr_Total": 0.05,
        "Overall_Hr_Total": 1,
        "Number_Of_Voice": 14,
    },
    "el": {
        "Language": "Greek",
        "Date": "2020-12-11",
        "Size": "39 MB",
        "Version": "ab_1h_2020-12-11",
        "Validated_Hr_Total": 0.05,
        "Overall_Hr_Total": 1,
        "Number_Of_Voice": 14,
    },
    "en": {
        "Language": "English",
        "Date": "2020-12-11",
        "Size": "39 MB",
        "Version": "ab_1h_2020-12-11",
        "Validated_Hr_Total": 0.05,
        "Overall_Hr_Total": 1,
        "Number_Of_Voice": 14,
    },
    "eo": {
        "Language": "Esperanto",
        "Date": "2020-12-11",
        "Size": "39 MB",
        "Version": "ab_1h_2020-12-11",
        "Validated_Hr_Total": 0.05,
        "Overall_Hr_Total": 1,
        "Number_Of_Voice": 14,
    },
    "es": {
        "Language": "Spanish",
        "Date": "2020-12-11",
        "Size": "39 MB",
        "Version": "ab_1h_2020-12-11",
        "Validated_Hr_Total": 0.05,
        "Overall_Hr_Total": 1,
        "Number_Of_Voice": 14,
    },
    "et": {
        "Language": "Estonian",
        "Date": "2020-12-11",
        "Size": "39 MB",
        "Version": "ab_1h_2020-12-11",
        "Validated_Hr_Total": 0.05,
        "Overall_Hr_Total": 1,
        "Number_Of_Voice": 14,
    },
    "eu": {
        "Language": "Basque",
        "Date": "2020-12-11",
        "Size": "39 MB",
        "Version": "ab_1h_2020-12-11",
        "Validated_Hr_Total": 0.05,
        "Overall_Hr_Total": 1,
        "Number_Of_Voice": 14,
    },
    "fa": {
        "Language": "Persian",
        "Date": "2020-12-11",
        "Size": "39 MB",
        "Version": "ab_1h_2020-12-11",
        "Validated_Hr_Total": 0.05,
        "Overall_Hr_Total": 1,
        "Number_Of_Voice": 14,
    },
    "fi": {
        "Language": "Finnish",
        "Date": "2020-12-11",
        "Size": "39 MB",
        "Version": "ab_1h_2020-12-11",
        "Validated_Hr_Total": 0.05,
        "Overall_Hr_Total": 1,
        "Number_Of_Voice": 14,
    },
    "fr": {
        "Language": "French",
        "Date": "2020-12-11",
        "Size": "39 MB",
        "Version": "ab_1h_2020-12-11",
        "Validated_Hr_Total": 0.05,
        "Overall_Hr_Total": 1,
        "Number_Of_Voice": 14,
    },
    "fy-NL": {
        "Language": "Frisian",
        "Date": "2020-12-11",
        "Size": "39 MB",
        "Version": "ab_1h_2020-12-11",
        "Validated_Hr_Total": 0.05,
        "Overall_Hr_Total": 1,
        "Number_Of_Voice": 14,
    },
    "ga-IE": {
        "Language": "Irish",
        "Date": "2020-12-11",
        "Size": "39 MB",
        "Version": "ab_1h_2020-12-11",
        "Validated_Hr_Total": 0.05,
        "Overall_Hr_Total": 1,
        "Number_Of_Voice": 14,
    },
    "hi": {
        "Language": "Hindi",
        "Date": "2020-12-11",
        "Size": "39 MB",
        "Version": "ab_1h_2020-12-11",
        "Validated_Hr_Total": 0.05,
        "Overall_Hr_Total": 1,
        "Number_Of_Voice": 14,
    },
    "hsb": {
        "Language": "Sorbian, Upper",
        "Date": "2020-12-11",
        "Size": "39 MB",
        "Version": "ab_1h_2020-12-11",
        "Validated_Hr_Total": 0.05,
        "Overall_Hr_Total": 1,
        "Number_Of_Voice": 14,
    },
    "hu": {
        "Language": "Hungarian",
        "Date": "2020-12-11",
        "Size": "39 MB",
        "Version": "ab_1h_2020-12-11",
        "Validated_Hr_Total": 0.05,
        "Overall_Hr_Total": 1,
        "Number_Of_Voice": 14,
    },
    "ia": {
        "Language": "InterLinguia",
        "Date": "2020-12-11",
        "Size": "39 MB",
        "Version": "ab_1h_2020-12-11",
        "Validated_Hr_Total": 0.05,
        "Overall_Hr_Total": 1,
        "Number_Of_Voice": 14,
    },
    "id": {
        "Language": "Indonesian",
        "Date": "2020-12-11",
        "Size": "39 MB",
        "Version": "ab_1h_2020-12-11",
        "Validated_Hr_Total": 0.05,
        "Overall_Hr_Total": 1,
        "Number_Of_Voice": 14,
    },
    "it": {
        "Language": "Italian",
        "Date": "2020-12-11",
        "Size": "39 MB",
        "Version": "ab_1h_2020-12-11",
        "Validated_Hr_Total": 0.05,
        "Overall_Hr_Total": 1,
        "Number_Of_Voice": 14,
    },
    "ja": {
        "Language": "Japanese",
        "Date": "2020-12-11",
        "Size": "39 MB",
        "Version": "ab_1h_2020-12-11",
        "Validated_Hr_Total": 0.05,
        "Overall_Hr_Total": 1,
        "Number_Of_Voice": 14,
    },
    "ka": {
        "Language": "Georgian",
        "Date": "2020-12-11",
        "Size": "39 MB",
        "Version": "ab_1h_2020-12-11",
        "Validated_Hr_Total": 0.05,
        "Overall_Hr_Total": 1,
        "Number_Of_Voice": 14,
    },
    "kab": {
        "Language": "Kabyle",
        "Date": "2020-12-11",
        "Size": "39 MB",
        "Version": "ab_1h_2020-12-11",
        "Validated_Hr_Total": 0.05,
        "Overall_Hr_Total": 1,
        "Number_Of_Voice": 14,
    },
    "ky": {
        "Language": "Kyrgyz",
        "Date": "2020-12-11",
        "Size": "39 MB",
        "Version": "ab_1h_2020-12-11",
        "Validated_Hr_Total": 0.05,
        "Overall_Hr_Total": 1,
        "Number_Of_Voice": 14,
    },
    "lg": {
        "Language": "Luganda",
        "Date": "2020-12-11",
        "Size": "39 MB",
        "Version": "ab_1h_2020-12-11",
        "Validated_Hr_Total": 0.05,
        "Overall_Hr_Total": 1,
        "Number_Of_Voice": 14,
    },
    "lt": {
        "Language": "Lithuanian",
        "Date": "2020-12-11",
        "Size": "39 MB",
        "Version": "ab_1h_2020-12-11",
        "Validated_Hr_Total": 0.05,
        "Overall_Hr_Total": 1,
        "Number_Of_Voice": 14,
    },
    "lv": {
        "Language": "Latvian",
        "Date": "2020-12-11",
        "Size": "39 MB",
        "Version": "ab_1h_2020-12-11",
        "Validated_Hr_Total": 0.05,
        "Overall_Hr_Total": 1,
        "Number_Of_Voice": 14,
    },
    "mn": {
        "Language": "Mongolian",
        "Date": "2020-12-11",
        "Size": "39 MB",
        "Version": "ab_1h_2020-12-11",
        "Validated_Hr_Total": 0.05,
        "Overall_Hr_Total": 1,
        "Number_Of_Voice": 14,
    },
    "mt": {
        "Language": "Maltese",
        "Date": "2020-12-11",
        "Size": "39 MB",
        "Version": "ab_1h_2020-12-11",
        "Validated_Hr_Total": 0.05,
        "Overall_Hr_Total": 1,
        "Number_Of_Voice": 14,
    },
    "nl": {
        "Language": "Dutch",
        "Date": "2020-12-11",
        "Size": "39 MB",
        "Version": "ab_1h_2020-12-11",
        "Validated_Hr_Total": 0.05,
        "Overall_Hr_Total": 1,
        "Number_Of_Voice": 14,
    },
    "or": {
        "Language": "Odia",
        "Date": "2020-12-11",
        "Size": "39 MB",
        "Version": "ab_1h_2020-12-11",
        "Validated_Hr_Total": 0.05,
        "Overall_Hr_Total": 1,
        "Number_Of_Voice": 14,
    },
    "pa-IN": {
        "Language": "Punjabi",
        "Date": "2020-12-11",
        "Size": "39 MB",
        "Version": "ab_1h_2020-12-11",
        "Validated_Hr_Total": 0.05,
        "Overall_Hr_Total": 1,
        "Number_Of_Voice": 14,
    },
    "pl": {
        "Language": "Polish",
        "Date": "2020-12-11",
        "Size": "39 MB",
        "Version": "ab_1h_2020-12-11",
        "Validated_Hr_Total": 0.05,
        "Overall_Hr_Total": 1,
        "Number_Of_Voice": 14,
    },
    "pt": {
        "Language": "Portuguese",
        "Date": "2020-12-11",
        "Size": "39 MB",
        "Version": "ab_1h_2020-12-11",
        "Validated_Hr_Total": 0.05,
        "Overall_Hr_Total": 1,
        "Number_Of_Voice": 14,
    },
    "rm-sursilv": {
        "Language": "Romansh Sursilvan",
        "Date": "2020-12-11",
        "Size": "39 MB",
        "Version": "ab_1h_2020-12-11",
        "Validated_Hr_Total": 0.05,
        "Overall_Hr_Total": 1,
        "Number_Of_Voice": 14,
    },
    "rm-vallader": {
        "Language": "Romansh Vallader",
        "Date": "2020-12-11",
        "Size": "39 MB",
        "Version": "ab_1h_2020-12-11",
        "Validated_Hr_Total": 0.05,
        "Overall_Hr_Total": 1,
        "Number_Of_Voice": 14,
    },
    "ro": {
        "Language": "Romanian",
        "Date": "2020-12-11",
        "Size": "39 MB",
        "Version": "ab_1h_2020-12-11",
        "Validated_Hr_Total": 0.05,
        "Overall_Hr_Total": 1,
        "Number_Of_Voice": 14,
    },
    "ru": {
        "Language": "Russian",
        "Date": "2020-12-11",
        "Size": "39 MB",
        "Version": "ab_1h_2020-12-11",
        "Validated_Hr_Total": 0.05,
        "Overall_Hr_Total": 1,
        "Number_Of_Voice": 14,
    },
    "rw": {
        "Language": "Kinyarwanda",
        "Date": "2020-12-11",
        "Size": "39 MB",
        "Version": "ab_1h_2020-12-11",
        "Validated_Hr_Total": 0.05,
        "Overall_Hr_Total": 1,
        "Number_Of_Voice": 14,
    },
    "sah": {
        "Language": "Sakha",
        "Date": "2020-12-11",
        "Size": "39 MB",
        "Version": "ab_1h_2020-12-11",
        "Validated_Hr_Total": 0.05,
        "Overall_Hr_Total": 1,
        "Number_Of_Voice": 14,
    },
    "sl": {
        "Language": "Slovenian",
        "Date": "2020-12-11",
        "Size": "39 MB",
        "Version": "ab_1h_2020-12-11",
        "Validated_Hr_Total": 0.05,
        "Overall_Hr_Total": 1,
        "Number_Of_Voice": 14,
    },
    "sv-SE": {
        "Language": "Swedish",
        "Date": "2020-12-11",
        "Size": "39 MB",
        "Version": "ab_1h_2020-12-11",
        "Validated_Hr_Total": 0.05,
        "Overall_Hr_Total": 1,
        "Number_Of_Voice": 14,
    },
    "ta": {
        "Language": "Tamil",
        "Date": "2020-12-11",
        "Size": "39 MB",
        "Version": "ab_1h_2020-12-11",
        "Validated_Hr_Total": 0.05,
        "Overall_Hr_Total": 1,
        "Number_Of_Voice": 14,
    },
    "th": {
        "Language": "Thai",
        "Date": "2020-12-11",
        "Size": "39 MB",
        "Version": "ab_1h_2020-12-11",
        "Validated_Hr_Total": 0.05,
        "Overall_Hr_Total": 1,
        "Number_Of_Voice": 14,
    },
    "tr": {
        "Language": "Turkish",
        "Date": "2020-12-11",
        "Size": "39 MB",
        "Version": "ab_1h_2020-12-11",
        "Validated_Hr_Total": 0.05,
        "Overall_Hr_Total": 1,
        "Number_Of_Voice": 14,
    },
    "tt": {
        "Language": "Tatar",
        "Date": "2020-12-11",
        "Size": "39 MB",
        "Version": "ab_1h_2020-12-11",
        "Validated_Hr_Total": 0.05,
        "Overall_Hr_Total": 1,
        "Number_Of_Voice": 14,
    },
    "uk": {
        "Language": "Ukrainian",
        "Date": "2020-12-11",
        "Size": "39 MB",
        "Version": "ab_1h_2020-12-11",
        "Validated_Hr_Total": 0.05,
        "Overall_Hr_Total": 1,
        "Number_Of_Voice": 14,
    },
    "vi": {
        "Language": "Vietnamese",
        "Date": "2020-12-11",
        "Size": "39 MB",
        "Version": "ab_1h_2020-12-11",
        "Validated_Hr_Total": 0.05,
        "Overall_Hr_Total": 1,
        "Number_Of_Voice": 14,
    },
    "vot": {
        "Language": "Votic",
        "Date": "2020-12-11",
        "Size": "39 MB",
        "Version": "ab_1h_2020-12-11",
        "Validated_Hr_Total": 0.05,
        "Overall_Hr_Total": 1,
        "Number_Of_Voice": 14,
    },
    "zh-CN": {
        "Language": "Chinese (China)",
        "Date": "2020-12-11",
        "Size": "39 MB",
        "Version": "ab_1h_2020-12-11",
        "Validated_Hr_Total": 0.05,
        "Overall_Hr_Total": 1,
        "Number_Of_Voice": 14,
    },
    "zh-HK": {
        "Language": "Chinese (Hong Kong)",
        "Date": "2020-12-11",
        "Size": "39 MB",
        "Version": "ab_1h_2020-12-11",
        "Validated_Hr_Total": 0.05,
        "Overall_Hr_Total": 1,
        "Number_Of_Voice": 14,
    },
    "zh-TW": {
        "Language": "Chinese (Taiwan)",
        "Date": "2020-12-11",
        "Size": "39 MB",
        "Version": "ab_1h_2020-12-11",
        "Validated_Hr_Total": 0.05,
        "Overall_Hr_Total": 1,
        "Number_Of_Voice": 14,
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
    """TODO: Short description of my dataset."""

    @property
    def manual_download_instructions(self):
        return """\
    You need to go to https://commonvoice.mozilla.org/en/datasets,
    and manually download the dataset as a .tar file. Once it is completed,
    a folder will be made containing the files, validated.tsv, train.tsv, test.tsv, reported.tsv, other.tsv, invalidated.tsv, dev.tsv
    and the folder clips containing audiofiles sampled at 48khz. Each clip is around 3-4 seconds in duration with a size of around 20-50 khz

    The downloaded .tar file can be extracted using the `$ tar -xzvf <path/to/downloaded/file>` command.
    The extracted folder is usually called ``cv-corpus-6.1-2020-12-11`` and should contain a folder 
    named after the language id, *e.g.* `en`. Make sure to pass the ``data_dir`` argument to process the Common Voice dataset.

    *E.g.*:

    ```
    from datasets import load_dataset

    # here it is assumed that the folder `cv-corpus-6.1-2020-12-11` has `en` as a subfolder
    common_voice_ds = load_dataset("common_voice", "en", data_dir="./cv-corpus-6.1-2020-12-11")
    ```
    """

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
        )

    def _split_generators(self, dl_manager):
        """Returns SplitGenerators."""
        abs_path_to_data = os.path.abspath(os.path.join(dl_manager.manual_dir, self.config.name))
        abs_path_to_clips = os.path.join(abs_path_to_data, "clips")

        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                gen_kwargs={
                    "filepath": os.path.join(abs_path_to_data, "train.tsv"),
                    "path_to_clips": abs_path_to_clips,
                },
            ),
            datasets.SplitGenerator(
                name=datasets.Split.TEST,
                gen_kwargs={
                    "filepath": os.path.join(abs_path_to_data, "test.tsv"),
                    "path_to_clips": abs_path_to_clips,
                },
            ),
            datasets.SplitGenerator(
                name=datasets.Split.VALIDATION,
                gen_kwargs={
                    "filepath": os.path.join(abs_path_to_data, "dev.tsv"),
                    "path_to_clips": abs_path_to_clips,
                },
            ),
            datasets.SplitGenerator(
                name="other",
                gen_kwargs={
                    "filepath": os.path.join(abs_path_to_data, "other.tsv"),
                    "path_to_clips": abs_path_to_clips,
                },
            ),
            datasets.SplitGenerator(
                name="invalidated",
                gen_kwargs={
                    "filepath": os.path.join(abs_path_to_data, "invalidated.tsv"),
                    "path_to_clips": abs_path_to_clips,
                },
            ),
        ]

    def _generate_examples(self, filepath, path_to_clips):
        """ Yields examples. """
        data_fields = list(self._info().features.keys())
        path_idx = data_fields.index("path")

        with open(filepath, encoding="utf-8") as f:
            lines = f.readlines()
            headline = lines[0]

            column_names = headline.strip().split("\t")
            assert (
                column_names == data_fields
            ), f"The file should have {data_fields} as column names, but has {column_names}"

            for id_, line in enumerate(lines[1:]):
                field_values = line.strip().split("\t")

                # set absolute path for mp3 audio file
                field_values[path_idx] = os.path.join(path_to_clips, field_values[path_idx])

                # if data is incomplete, fill with empty values
                if len(field_values) < len(data_fields):
                    field_values += (len(data_fields) - len(field_values)) * ["''"]

                yield id_, {key: value for key, value in zip(data_fields, field_values)}
