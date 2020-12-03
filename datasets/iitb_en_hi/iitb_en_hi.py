# coding=utf-8
# Copyright 2020 The HuggingFace Datasets Authors and the current dataset script contributor.
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
"""IIT Bombay English-Hindi Corpus"""

from __future__ import absolute_import, division, print_function

import os
import datasets


_CITATION = """\
Anoop Kunchukuttan, Pratik Mehta, Pushpak Bhattacharyya. \
The IIT Bombay English-Hindi Parallel Corpus. Language Resources and Evaluation Conference. 2018.
"""


_DESCRIPTION = """\
he IIT Bombay English-Hindi corpus contains parallel corpus for English-Hindi corpus collected from a variety of existing sources \
and corpora developed at the Center for Indian Language Technology, IIT Bombay over the years.\
The dataset contains 1,609,682 english to hindi translation pairs.
"""

_URLs = {
    "train": "http://www.cfilt.iitb.ac.in/iitb_parallel/iitb_corpus_download/parallel.tgz",
    "dev-test": "http://www.cfilt.iitb.ac.in/iitb_parallel/iitb_corpus_download/dev_test.tgz",
}


class IitbEnHi(datasets.GeneratorBasedBuilder):
    """IIT Bombay English-Hindi Corpus"""

    VERSION = datasets.Version("1.0.0")

    BUILDER_CONFIGS = [
        datasets.BuilderConfig(
            name="iitb_en_hi", description="IIT Bombay English-Hindi Corpus", version=datasets.Version("1.0.0")
        )
    ]

    def _info(self):
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=datasets.Features(
                {
                    "english_text": datasets.Value("string"),
                    "hindi_text": datasets.Value("string"),
                }
            ),
            supervised_keys=None,
            homepage="http://www.cfilt.iitb.ac.in/iitb_parallel/",
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        """Returns SplitGenerators."""
        data_dir = dl_manager.download_and_extract(_URLs)
        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                gen_kwargs={
                    "input_filepath_english": os.path.join(data_dir["train"], "parallel", "IITB.en-hi.en"),
                    "input_filepath_hindi": os.path.join(data_dir["train"], "parallel", "IITB.en-hi.hi"),
                },
            ),
            datasets.SplitGenerator(
                name=datasets.Split.TEST,
                gen_kwargs={
                    "input_filepath_english": os.path.join(data_dir["dev-test"], "dev_test", "test.en"),
                    "input_filepath_hindi": os.path.join(data_dir["dev-test"], "dev_test", "test.hi"),
                },
            ),
            datasets.SplitGenerator(
                name=datasets.Split.VALIDATION,
                gen_kwargs={
                    "input_filepath_english": os.path.join(data_dir["dev-test"], "dev_test", "dev.en"),
                    "input_filepath_hindi": os.path.join(data_dir["dev-test"], "dev_test", "dev.hi"),
                },
            ),
        ]

    def _generate_examples(self, input_filepath_english, input_filepath_hindi):
        with open(input_filepath_english) as en_texts, open(input_filepath_hindi) as hi_texts:
            for idx, (en_text, hi_texts) in enumerate(zip(en_texts, hi_texts)):
                yield idx, {"english_text": en_text, "hindi_text": hi_texts}
