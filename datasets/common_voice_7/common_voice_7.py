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


import os

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
        "Date": "2021-07-21",
        "Language": "Kazakh",
        "Number_Of_Voice": 35,
        "Overall_Hr_Total": 4.07,
        "Size": "96.828631 MB",
        "Validated_Hr_Total": 2.07,
        "Version": "ab_4h_2021-07-21",
    },
    "ar": {
        "Date": "2021-07-21",
        "Language": "Greek",
        "Number_Of_Voice": 1052,
        "Overall_Hr_Total": 137.17,
        "Size": "2947.03861 MB",
        "Validated_Hr_Total": 85.78,
        "Version": "ar_137h_2021-07-21",
    },
    "as": {
        "Date": "2021-07-21",
        "Language": "Lithuanian",
        "Number_Of_Voice": 37,
        "Overall_Hr_Total": 1.4,
        "Size": "34.89825 MB",
        "Validated_Hr_Total": 1.33,
        "Version": "as_1h_2021-07-21",
    },
    "az": {
        "Date": "2021-07-21",
        "Language": "Chinese (Hong Kong)",
        "Number_Of_Voice": 4,
        "Overall_Hr_Total": 0.05,
        "Size": "1.083579 MB",
        "Validated_Hr_Total": 0,
        "Version": "az_0h_2021-07-21",
    },
    "ba": {
        "Date": "2021-07-21",
        "Language": "Tamil",
        "Number_Of_Voice": 861,
        "Overall_Hr_Total": 263.83,
        "Size": "5325.656457 MB",
        "Validated_Hr_Total": 247.18,
        "Version": "ba_263h_2021-07-21",
    },
    "bas": {
        "Date": "2021-07-21",
        "Language": "Sakha",
        "Number_Of_Voice": 28,
        "Overall_Hr_Total": 2.61,
        "Size": "52.096262 MB",
        "Validated_Hr_Total": 1.69,
        "Version": "bas_2h_2021-07-21",
    },
    "be": {
        "Date": "2021-07-21",
        "Language": "Uyghur",
        "Number_Of_Voice": 3831,
        "Overall_Hr_Total": 356.66,
        "Size": "7305.605035 MB",
        "Validated_Hr_Total": 275.22,
        "Version": "be_356h_2021-07-21",
    },
    "bg": {
        "Date": "2021-07-21",
        "Language": "Serbian",
        "Number_Of_Voice": 39,
        "Overall_Hr_Total": 6.12,
        "Size": "129.479983 MB",
        "Validated_Hr_Total": 5.02,
        "Version": "bg_6h_2021-07-21",
    },
    "br": {
        "Date": "2021-07-21",
        "Language": "Esperanto",
        "Number_Of_Voice": 170,
        "Overall_Hr_Total": 19.57,
        "Size": "521.023883 MB",
        "Validated_Hr_Total": 9.22,
        "Version": "br_19h_2021-07-21",
    },
    "ca": {
        "Date": "2021-07-21",
        "Language": "Bulgarian",
        "Number_Of_Voice": 6095,
        "Overall_Hr_Total": 917.52,
        "Size": "24307.605172 MB",
        "Validated_Hr_Total": 789.62,
        "Version": "ca_917h_2021-07-21",
    },
    "cnh": {
        "Date": "2021-07-21",
        "Language": "Guarani",
        "Number_Of_Voice": 298,
        "Overall_Hr_Total": 5.74,
        "Size": "161.377408 MB",
        "Validated_Hr_Total": 2.42,
        "Version": "cnh_5h_2021-07-21",
    },
    "cs": {
        "Date": "2021-07-21",
        "Language": "Interlingua",
        "Number_Of_Voice": 484,
        "Overall_Hr_Total": 63.59,
        "Size": "1648.345476 MB",
        "Validated_Hr_Total": 49.82,
        "Version": "cs_63h_2021-07-21",
    },
    "cv": {
        "Date": "2021-07-21",
        "Language": "Kurmanji Kurdish",
        "Number_Of_Voice": 93,
        "Overall_Hr_Total": 18.53,
        "Size": "486.325136 MB",
        "Validated_Hr_Total": 5.2,
        "Version": "cv_18h_2021-07-21",
    },
    "cy": {
        "Date": "2021-07-21",
        "Language": "Belarusian",
        "Number_Of_Voice": 1655,
        "Overall_Hr_Total": 141.87,
        "Size": "3800.15061 MB",
        "Validated_Hr_Total": 110.9,
        "Version": "cy_141h_2021-07-21",
    },
    "de": {
        "Date": "2021-07-21",
        "Language": "Breton",
        "Number_Of_Voice": 15620,
        "Overall_Hr_Total": 1035.5,
        "Size": "27463.071197 MB",
        "Validated_Hr_Total": 965.16,
        "Version": "de_1035h_2021-07-21",
    },
    "dv": {
        "Date": "2021-07-21",
        "Language": "Maltese",
        "Number_Of_Voice": 271,
        "Overall_Hr_Total": 53.9,
        "Size": "1258.575355 MB",
        "Validated_Hr_Total": 33.05,
        "Version": "dv_53h_2021-07-21",
    },
    "el": {
        "Date": "2021-07-21",
        "Language": "Armenian",
        "Number_Of_Voice": 271,
        "Overall_Hr_Total": 23.11,
        "Size": "579.685993 MB",
        "Validated_Hr_Total": 13.34,
        "Version": "el_23h_2021-07-21",
    },
    "en": {
        "Date": "2021-07-21",
        "Language": "Abkhaz",
        "Number_Of_Voice": 75879,
        "Overall_Hr_Total": 2637.14,
        "Size": "70115.911389 MB",
        "Validated_Hr_Total": 2015.02,
        "Version": "en_2637h_2021-07-21",
    },
    "eo": {
        "Date": "2021-07-21",
        "Language": "Estonian",
        "Number_Of_Voice": 1066,
        "Overall_Hr_Total": 844.67,
        "Size": "18560.215763 MB",
        "Validated_Hr_Total": 748.1,
        "Version": "eo_844h_2021-07-21",
    },
    "es": {
        "Date": "2021-07-21",
        "Language": "Azerbaijani",
        "Number_Of_Voice": 21761,
        "Overall_Hr_Total": 683.81,
        "Size": "18379.233074 MB",
        "Validated_Hr_Total": 377.81,
        "Version": "es_683h_2021-07-21",
    },
    "et": {
        "Date": "2021-07-21",
        "Language": "Hausa",
        "Number_Of_Voice": 718,
        "Overall_Hr_Total": 43.63,
        "Size": "1107.863883 MB",
        "Validated_Hr_Total": 32.27,
        "Version": "et_43h_2021-07-21",
    },
    "eu": {
        "Date": "2021-07-21",
        "Language": "German",
        "Number_Of_Voice": 1050,
        "Overall_Hr_Total": 132.47,
        "Size": "3689.025098 MB",
        "Validated_Hr_Total": 91.36,
        "Version": "eu_132h_2021-07-21",
    },
    "fa": {
        "Date": "2021-07-21",
        "Language": "Arabic",
        "Number_Of_Voice": 3835,
        "Overall_Hr_Total": 334.94,
        "Size": "9173.036961 MB",
        "Validated_Hr_Total": 293.98,
        "Version": "fa_334h_2021-07-21",
    },
    "fi": {
        "Date": "2021-07-21",
        "Language": "Portuguese",
        "Number_Of_Voice": 139,
        "Overall_Hr_Total": 12.31,
        "Size": "268.332961 MB",
        "Validated_Hr_Total": 6.74,
        "Version": "fi_12h_2021-07-21",
    },
    "fr": {
        "Date": "2021-07-21",
        "Language": "Assamese",
        "Number_Of_Voice": 15391,
        "Overall_Hr_Total": 834.16,
        "Size": "22312.655903 MB",
        "Validated_Hr_Total": 747.13,
        "Version": "fr_834h_2021-07-21",
    },
    "fy-NL": {
        "Date": "2021-07-21",
        "Language": "Mongolian",
        "Number_Of_Voice": 678,
        "Overall_Hr_Total": 75.63,
        "Size": "1821.742478 MB",
        "Validated_Hr_Total": 29.74,
        "Version": "fy-NL_75h_2021-07-21",
    },
    "ga-IE": {
        "Date": "2021-07-21",
        "Language": "Polish",
        "Number_Of_Voice": 132,
        "Overall_Hr_Total": 7.97,
        "Size": "203.941551 MB",
        "Validated_Hr_Total": 3.91,
        "Version": "ga-IE_7h_2021-07-21",
    },
    "gl": {
        "Date": "2021-07-21",
        "Language": "Thai",
        "Number_Of_Voice": 106,
        "Overall_Hr_Total": 7.83,
        "Size": "161.168322 MB",
        "Validated_Hr_Total": 7.37,
        "Version": "gl_7h_2021-07-21",
    },
    "gn": {
        "Date": "2021-07-21",
        "Language": "Urdu",
        "Number_Of_Voice": 55,
        "Overall_Hr_Total": 1.71,
        "Size": "33.178619 MB",
        "Validated_Hr_Total": 0.53,
        "Version": "gn_1h_2021-07-21",
    },
    "ha": {
        "Date": "2021-07-21",
        "Language": "Chinese (Taiwan)",
        "Number_Of_Voice": 17,
        "Overall_Hr_Total": 3.03,
        "Size": "63.636525 MB",
        "Validated_Hr_Total": 1.85,
        "Version": "ha_3h_2021-07-21",
    },
    "hi": {
        "Date": "2021-07-21",
        "Language": "Kinyarwanda",
        "Number_Of_Voice": 214,
        "Overall_Hr_Total": 11.84,
        "Size": "252.728592 MB",
        "Validated_Hr_Total": 8.56,
        "Version": "hi_11h_2021-07-21",
    },
    "hsb": {
        "Date": "2021-07-21",
        "Language": "Hungarian",
        "Number_Of_Voice": 19,
        "Overall_Hr_Total": 2.8,
        "Size": "79.355401 MB",
        "Validated_Hr_Total": 2.34,
        "Version": "hsb_2h_2021-07-21",
    },
    "hu": {
        "Date": "2021-07-21",
        "Language": "Romansh Sursilvan",
        "Number_Of_Voice": 169,
        "Overall_Hr_Total": 21.86,
        "Size": "518.917337 MB",
        "Validated_Hr_Total": 16.88,
        "Version": "hu_21h_2021-07-21",
    },
    "hy-AM": {
        "Date": "2021-07-21",
        "Language": "Tatar",
        "Number_Of_Voice": 28,
        "Overall_Hr_Total": 2.79,
        "Size": "59.015187 MB",
        "Validated_Hr_Total": 1.34,
        "Version": "hy-AM_2h_2021-07-21",
    },
    "ia": {
        "Date": "2021-07-21",
        "Language": "Finnish",
        "Number_Of_Voice": 53,
        "Overall_Hr_Total": 16.06,
        "Size": "394.42455 MB",
        "Validated_Hr_Total": 12.25,
        "Version": "ia_16h_2021-07-21",
    },
    "id": {
        "Date": "2021-07-21",
        "Language": "Persian",
        "Number_Of_Voice": 340,
        "Overall_Hr_Total": 49.5,
        "Size": "1147.111673 MB",
        "Validated_Hr_Total": 23.75,
        "Version": "id_49h_2021-07-21",
    },
    "it": {
        "Date": "2021-07-21",
        "Language": "Welsh",
        "Number_Of_Voice": 6407,
        "Overall_Hr_Total": 317.29,
        "Size": "8054.153738 MB",
        "Validated_Hr_Total": 288.82,
        "Version": "it_317h_2021-07-21",
    },
    "ja": {
        "Date": "2021-07-21",
        "Language": "Frisian",
        "Number_Of_Voice": 397,
        "Overall_Hr_Total": 29.96,
        "Size": "670.230519 MB",
        "Validated_Hr_Total": 26.93,
        "Version": "ja_29h_2021-07-21",
    },
    "ka": {
        "Date": "2021-07-21",
        "Language": "Latvian",
        "Number_Of_Voice": 114,
        "Overall_Hr_Total": 7.17,
        "Size": "173.494246 MB",
        "Validated_Hr_Total": 6.73,
        "Version": "ka_7h_2021-07-21",
    },
    "kab": {
        "Date": "2021-07-21",
        "Language": "Basaa",
        "Number_Of_Voice": 1408,
        "Overall_Hr_Total": 656.11,
        "Size": "17857.634451 MB",
        "Validated_Hr_Total": 548.56,
        "Version": "kab_656h_2021-07-21",
    },
    "kk": {
        "Date": "2021-07-21",
        "Language": "Swedish",
        "Number_Of_Voice": 66,
        "Overall_Hr_Total": 1.44,
        "Size": "29.59703 MB",
        "Validated_Hr_Total": 0.73,
        "Version": "kk_1h_2021-07-21",
    },
    "kmr": {
        "Date": "2021-07-21",
        "Language": "Slovenian",
        "Number_Of_Voice": 278,
        "Overall_Hr_Total": 52.56,
        "Size": "1008.380764 MB",
        "Validated_Hr_Total": 45.49,
        "Version": "kmr_52h_2021-07-21",
    },
    "ky": {
        "Date": "2021-07-21",
        "Language": "Hindi",
        "Number_Of_Voice": 227,
        "Overall_Hr_Total": 44.25,
        "Size": "1032.606586 MB",
        "Validated_Hr_Total": 37.04,
        "Version": "ky_44h_2021-07-21",
    },
    "lg": {
        "Date": "2021-07-21",
        "Language": "Russian",
        "Number_Of_Voice": 260,
        "Overall_Hr_Total": 80,
        "Size": "1722.86 MB",
        "Validated_Hr_Total": 31.18,
        "Version": "lg_80h_2021-07-21",
    },
    "lt": {
        "Date": "2021-07-21",
        "Language": "Romanian",
        "Number_Of_Voice": 232,
        "Overall_Hr_Total": 19.87,
        "Size": "440.325435 MB",
        "Validated_Hr_Total": 16.38,
        "Version": "lt_19h_2021-07-21",
    },
    "lv": {
        "Date": "2021-07-21",
        "Language": "French",
        "Number_Of_Voice": 113,
        "Overall_Hr_Total": 8.24,
        "Size": "220.119979 MB",
        "Validated_Hr_Total": 6.88,
        "Version": "lv_8h_2021-07-21",
    },
    "mn": {
        "Date": "2021-07-21",
        "Language": "Georgian",
        "Number_Of_Voice": 435,
        "Overall_Hr_Total": 18.17,
        "Size": "502.934499 MB",
        "Validated_Hr_Total": 12.17,
        "Version": "mn_18h_2021-07-21",
    },
    "mt": {
        "Date": "2021-07-21",
        "Language": "Luganda",
        "Number_Of_Voice": 200,
        "Overall_Hr_Total": 16.46,
        "Size": "444.369609 MB",
        "Validated_Hr_Total": 8.17,
        "Version": "mt_16h_2021-07-21",
    },
    "nl": {
        "Date": "2021-07-21",
        "Language": "Chuvash",
        "Number_Of_Voice": 1352,
        "Overall_Hr_Total": 98.86,
        "Size": "2490.744175 MB",
        "Validated_Hr_Total": 93.35,
        "Version": "nl_98h_2021-07-21",
    },
    "or": {
        "Date": "2021-07-21",
        "Language": "Punjabi",
        "Number_Of_Voice": 41,
        "Overall_Hr_Total": 7.64,
        "Size": "210.775441 MB",
        "Validated_Hr_Total": 0.94,
        "Version": "or_7h_2021-07-21",
    },
    "pa-IN": {
        "Date": "2021-07-21",
        "Language": "Dutch",
        "Number_Of_Voice": 46,
        "Overall_Hr_Total": 3.32,
        "Size": "87.690513 MB",
        "Validated_Hr_Total": 1.49,
        "Version": "pa-IN_3h_2021-07-21",
    },
    "pl": {
        "Date": "2021-07-21",
        "Language": "Indonesian",
        "Number_Of_Voice": 2918,
        "Overall_Hr_Total": 152.64,
        "Size": "4016.577061 MB",
        "Validated_Hr_Total": 129.1,
        "Version": "pl_152h_2021-07-21",
    },
    "pt": {
        "Date": "2021-07-21",
        "Language": "Spanish",
        "Number_Of_Voice": 2038,
        "Overall_Hr_Total": 112.08,
        "Size": "2724.725035 MB",
        "Validated_Hr_Total": 84.66,
        "Version": "pt_112h_2021-07-21",
    },
    "rm-sursilv": {
        "Date": "2021-07-21",
        "Language": "Italian",
        "Number_Of_Voice": 80,
        "Overall_Hr_Total": 10.24,
        "Size": "281.830812 MB",
        "Validated_Hr_Total": 5.98,
        "Version": "rm-sursilv_10h_2021-07-21",
    },
    "rm-vallader": {
        "Date": "2021-07-21",
        "Language": "Japanese",
        "Number_Of_Voice": 49,
        "Overall_Hr_Total": 4.13,
        "Size": "114.127527 MB",
        "Validated_Hr_Total": 2.31,
        "Version": "rm-vallader_4h_2021-07-21",
    },
    "ro": {
        "Date": "2021-07-21",
        "Language": "Sorbian, Upper",
        "Number_Of_Voice": 302,
        "Overall_Hr_Total": 31.72,
        "Size": "728.306654 MB",
        "Validated_Hr_Total": 11.18,
        "Version": "ro_31h_2021-07-21",
    },
    "ru": {
        "Date": "2021-07-21",
        "Language": "Czech",
        "Number_Of_Voice": 2136,
        "Overall_Hr_Total": 173.06,
        "Size": "4536.990731 MB",
        "Validated_Hr_Total": 148.77,
        "Version": "ru_173h_2021-07-21",
    },
    "rw": {
        "Date": "2021-07-21",
        "Language": "Irish",
        "Number_Of_Voice": 1023,
        "Overall_Hr_Total": 2255.22,
        "Size": "58295.067948 MB",
        "Validated_Hr_Total": 1894.16,
        "Version": "rw_2255h_2021-07-21",
    },
    "sah": {
        "Date": "2021-07-21",
        "Language": "Votic",
        "Number_Of_Voice": 45,
        "Overall_Hr_Total": 6.59,
        "Size": "181.815287 MB",
        "Validated_Hr_Total": 4.42,
        "Version": "sah_6h_2021-07-21",
    },
    "sk": {
        "Date": "2021-07-21",
        "Language": "Slovak",
        "Number_Of_Voice": 82,
        "Overall_Hr_Total": 12.64,
        "Size": "259.299408 MB",
        "Validated_Hr_Total": 10.77,
        "Version": "sk_12h_2021-07-21",
    },
    "sl": {
        "Date": "2021-07-21",
        "Language": "Bashkir",
        "Number_Of_Voice": 113,
        "Overall_Hr_Total": 10,
        "Size": "265.780682 MB",
        "Validated_Hr_Total": 9.18,
        "Version": "sl_10h_2021-07-21",
    },
    "sr": {
        "Date": "2021-07-21",
        "Language": "Uzbek",
        "Number_Of_Voice": 11,
        "Overall_Hr_Total": 0.51,
        "Size": "9.879034 MB",
        "Validated_Hr_Total": 0.19,
        "Version": "sr_0h_2021-07-21",
    },
    "sv-SE": {
        "Date": "2021-07-21",
        "Language": "Galician",
        "Number_Of_Voice": 682,
        "Overall_Hr_Total": 45.68,
        "Size": "1053.186277 MB",
        "Validated_Hr_Total": 35.19,
        "Version": "sv-SE_45h_2021-07-21",
    },
    "ta": {
        "Date": "2021-07-21",
        "Language": "Hakha Chin",
        "Number_Of_Voice": 580,
        "Overall_Hr_Total": 216.21,
        "Size": "4726.923179 MB",
        "Validated_Hr_Total": 198.32,
        "Version": "ta_216h_2021-07-21",
    },
    "th": {
        "Date": "2021-07-21",
        "Language": "Romansh Vallader",
        "Number_Of_Voice": 7212,
        "Overall_Hr_Total": 255.27,
        "Size": "5370.380496 MB",
        "Validated_Hr_Total": 133.78,
        "Version": "th_255h_2021-07-21",
    },
    "tr": {
        "Date": "2021-07-21",
        "Language": "Dhivehi",
        "Number_Of_Voice": 960,
        "Overall_Hr_Total": 37.92,
        "Size": "939.617663 MB",
        "Validated_Hr_Total": 30.85,
        "Version": "tr_37h_2021-07-21",
    },
    "tt": {
        "Date": "2021-07-21",
        "Language": "Catalan",
        "Number_Of_Voice": 203,
        "Overall_Hr_Total": 29.72,
        "Size": "794.848701 MB",
        "Validated_Hr_Total": 28.52,
        "Version": "tt_29h_2021-07-21",
    },
    "ug": {
        "Date": "2021-07-21",
        "Language": "Turkish",
        "Number_Of_Voice": 296,
        "Overall_Hr_Total": 44.26,
        "Size": "929.601304 MB",
        "Validated_Hr_Total": 41.31,
        "Version": "ug_44h_2021-07-21",
    },
    "uk": {
        "Date": "2021-07-21",
        "Language": "Kyrgyz",
        "Number_Of_Voice": 615,
        "Overall_Hr_Total": 66.68,
        "Size": "1694.344342 MB",
        "Validated_Hr_Total": 56.1,
        "Version": "uk_66h_2021-07-21",
    },
    "ur": {
        "Date": "2021-07-21",
        "Language": "Ukrainian",
        "Number_Of_Voice": 25,
        "Overall_Hr_Total": 1.64,
        "Size": "34.41152 MB",
        "Validated_Hr_Total": 0.59,
        "Version": "ur_1h_2021-07-21",
    },
    "uz": {
        "Date": "2021-07-21",
        "Language": "Vietnamese",
        "Number_Of_Voice": 7,
        "Overall_Hr_Total": 0.8,
        "Size": "14.900815 MB",
        "Validated_Hr_Total": 0.24,
        "Version": "uz_0h_2021-07-21",
    },
    "vi": {
        "Date": "2021-07-21",
        "Language": "Odia",
        "Number_Of_Voice": 138,
        "Overall_Hr_Total": 14.83,
        "Size": "310.698285 MB",
        "Validated_Hr_Total": 3.25,
        "Version": "vi_14h_2021-07-21",
    },
    "vot": {
        "Date": "2021-07-21",
        "Language": "Chinese (China)",
        "Number_Of_Voice": 5,
        "Overall_Hr_Total": 0.28,
        "Size": "7.892226 MB",
        "Validated_Hr_Total": 0,
        "Version": "vot_0h_2021-07-21",
    },
    "zh-CN": {
        "Date": "2021-07-21",
        "Language": "Basque",
        "Number_Of_Voice": 3792,
        "Overall_Hr_Total": 86.91,
        "Size": "2369.27356 MB",
        "Validated_Hr_Total": 63.24,
        "Version": "zh-CN_86h_2021-07-21",
    },
    "zh-HK": {
        "Date": "2021-07-21",
        "Language": "Kabyle",
        "Number_Of_Voice": 2656,
        "Overall_Hr_Total": 113.68,
        "Size": "3048.576629 MB",
        "Validated_Hr_Total": 96.35,
        "Version": "zh-HK_113h_2021-07-21",
    },
    "zh-TW": {
        "Date": "2021-07-21",
        "Language": "English",
        "Number_Of_Voice": 1584,
        "Overall_Hr_Total": 85.66,
        "Size": "2333.969324 MB",
        "Validated_Hr_Total": 60.73,
        "Version": "zh-TW_85h_2021-07-21",
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
            name=name,
            version=datasets.Version("6.1.0", ""),
            description=description,
            **kwargs,
        )


class CommonVoice(datasets.GeneratorBasedBuilder):

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

    @property
    def manual_download_instructions(self):
        return f"""
                     You need to manually the dataset from `https://commonvoice.mozilla.org/en/datasets`.
                     Make sure you choose the version `Common Voice Corpus 7.0`.
                     Choose a language of your choice and find the corresponding language-id, *e.g.*, `Abkhaz` with language-id `ab`. The following language-ids are available:

                     {list(_LANGUAGES.keys())}

                     Next, you will have to enter your email address to download the dataset in the `tar.gz` format. Save the file under <path-to-file>.
                     The file should then be extracted with: ``tar -xvzf <path-to-file>`` which will extract a folder called ``cv-corpus-7.0-2021-07-21``.
                     The dataset can then be loaded with `datasets.load_dataset("common_voice", <language-id>, data_dir="<path-to-'cv-corpus-7.0-2021-07-21'-folder>", ignore_verifications=True).
        """

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
            task_templates=[
                AutomaticSpeechRecognition(
                    audio_file_path_column="path", transcription_column="sentence"
                )
            ],
        )

    def _split_generators(self, dl_manager):
        """Returns SplitGenerators."""
        manual_dir = os.path.abspath(os.path.expanduser(dl_manager.manual_dir))

        if not os.path.exists(manual_dir):
            raise FileNotFoundError(
                "{} does not exist. Make sure you insert a manual dir via `datasets.load_dataset('common_voice', 'ab', data_dir=...)` that includes the stories downloaded from the original repository. Manual download instructions: {}".format(
                    manual_dir, self.manual_download_instructions
                )
            )

        #        abs_path_to_data = os.path.join(manual_dir, "cv-corpus-7.0-2021-07-21", self.config.name)
        abs_path_to_data = os.path.join(manual_dir, self.config.name)
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
        """Yields examples."""
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
                field_values[path_idx] = os.path.join(
                    path_to_clips, field_values[path_idx]
                )

                # if data is incomplete, fill with empty values
                if len(field_values) < len(data_fields):
                    field_values += (len(data_fields) - len(field_values)) * ["''"]

                yield id_, {key: value for key, value in zip(data_fields, field_values)}
