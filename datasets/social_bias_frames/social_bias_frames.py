# coding=utf-8
# Copyright 2020 The TensorFlow Datasets Authors and the HuggingFace Datasets Authors.
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
"""Social Bias Frames"""


import csv

import datasets


_CITATION = """\
@inproceedings{sap2020socialbiasframes,
   title={Social Bias Frames: Reasoning about Social and Power Implications of Language},
   author={Sap, Maarten and Gabriel, Saadia and Qin, Lianhui and Jurafsky, Dan and Smith, Noah A and Choi, Yejin},
   year={2020},
   booktitle={ACL},
}
"""

_DESCRIPTION = """\
Social Bias Frames is a new way of representing the biases and offensiveness that are implied in language.
For example, these frames are meant to distill the implication that "women (candidates) are less qualified"
behind the statement "we shouldn’t lower our standards to hire more women."
"""

_DATA_URL = "https://homes.cs.washington.edu/~msap/social-bias-frames/SBIC.v2.tgz"


class SocialBiasFrames(datasets.GeneratorBasedBuilder):
    """TSocial Bias Frame"""

    def _info(self):
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=datasets.Features(
                {
                    "whoTarget": datasets.Value("string"),
                    "intentYN": datasets.Value("string"),
                    "sexYN": datasets.Value("string"),
                    "sexReason": datasets.Value("string"),
                    "offensiveYN": datasets.Value("string"),
                    "annotatorGender": datasets.Value("string"),
                    "annotatorMinority": datasets.Value("string"),
                    "sexPhrase": datasets.Value("string"),
                    "speakerMinorityYN": datasets.Value("string"),
                    "WorkerId": datasets.Value("string"),
                    "HITId": datasets.Value("string"),
                    "annotatorPolitics": datasets.Value("string"),
                    "annotatorRace": datasets.Value("string"),
                    "annotatorAge": datasets.Value("string"),
                    "post": datasets.Value("string"),
                    "targetMinority": datasets.Value("string"),
                    "targetCategory": datasets.Value("string"),
                    "targetStereotype": datasets.Value("string"),
                    "dataSource": datasets.Value("string"),
                }
            ),
            # No default supervised_keys (as we have to pass both premise
            # and hypothesis as input).
            supervised_keys=None,
            homepage="https://homes.cs.washington.edu/~msap/social-bias-frames/",
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        archive = dl_manager.download(_DATA_URL)
        return [
            datasets.SplitGenerator(
                name=datasets.Split.TEST,
                gen_kwargs={"filepath": "SBIC.v2.tst.csv", "files": dl_manager.iter_archive(archive)},
            ),
            datasets.SplitGenerator(
                name=datasets.Split.VALIDATION,
                gen_kwargs={"filepath": "SBIC.v2.dev.csv", "files": dl_manager.iter_archive(archive)},
            ),
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                gen_kwargs={"filepath": "SBIC.v2.trn.csv", "files": dl_manager.iter_archive(archive)},
            ),
        ]

    def _generate_examples(self, filepath, files):
        """This function returns the examples in the raw (text) form."""
        for path, f in files:
            if path == filepath:
                lines = (line.decode("utf-8") for line in f)
                reader = csv.DictReader(lines)
                for idx, row in enumerate(reader):
                    yield idx, row
                break
