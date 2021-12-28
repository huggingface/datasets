# Copyright 2020 The HuggingFace Datasets Authors and the current dataset script contributor.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Dataset built from <auto-generated, manually corrected> caption pairs of
YouTube videos with labels capturing the differences between the two."""


import json

import datasets


_CITATION = ""

_DESCRIPTION = """\
Dataset built from pairs of YouTube captions where both 'auto-generated' and
'manually-corrected' captions are available for a single specified language.
This dataset labels two-way (e.g. ignoring single-sided insertions) same-length
token differences in the `diff_type` column. The `default_seq` is composed of
tokens from the 'auto-generated' captions. When a difference occurs between
the 'auto-generated' vs 'manually-corrected' captions types, the `correction_seq`
contains tokens from the 'manually-corrected' captions.
"""

_LICENSE = "MIT License"

_RELEASE_TAG = "v1.0"
_NUM_FILES = 4
_URLS = [
    f"https://raw.githubusercontent.com/2dot71mily/youtube_captions_corrections/{_RELEASE_TAG}/data/transcripts/en/split/youtube_caption_corrections_{i}.json"
    for i in range(_NUM_FILES)
]


class YoutubeCaptionCorrections(datasets.GeneratorBasedBuilder):
    """YouTube captions corrections."""

    def _info(self):
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=datasets.Features(
                {
                    "video_ids": datasets.Value("string"),
                    "default_seq": datasets.Sequence(datasets.Value("string")),
                    "correction_seq": datasets.Sequence(datasets.Value("string")),
                    "diff_type": datasets.Sequence(
                        datasets.features.ClassLabel(
                            names=[
                                "NO_DIFF",
                                "CASE_DIFF",
                                "PUNCUATION_DIFF",
                                "CASE_AND_PUNCUATION_DIFF",
                                "STEM_BASED_DIFF",
                                "DIGIT_DIFF",
                                "INTRAWORD_PUNC_DIFF",
                                "UNKNOWN_TYPE_DIFF",
                                "RESERVED_DIFF",
                            ]
                        )
                    ),
                }
            ),
            supervised_keys=("correction_seq", "diff_type"),
            homepage="https://github.com/2dot71mily/youtube_captions_corrections",
            license=_LICENSE,
        )

    def _split_generators(self, dl_manager):
        """Returns SplitGenerators."""
        downloaded_filepaths = dl_manager.download_and_extract(_URLS)
        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                gen_kwargs={"filepaths": downloaded_filepaths},
            ),
        ]

    def _generate_examples(self, filepaths):
        """Yields examples."""
        for file_idx, fp in enumerate(filepaths):
            with open(fp, encoding="utf-8") as json_file:
                json_lists = list(json_file)
            for line_idx, json_list_str in enumerate(json_lists):
                json_list = json.loads(json_list_str)

                for ctr_idx, result in enumerate(json_list):
                    response = {
                        "video_ids": result["video_ids"],
                        "diff_type": result["diff_type"],
                        "default_seq": result["default_seq"],
                        "correction_seq": result["correction_seq"],
                    }
                    yield f"{file_idx}_{line_idx}_{ctr_idx}", response
