# coding=utf-8
# Copyright 2020 The TensorFlow Datasets Authors and the HuggingFace NLP Authors.
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

from __future__ import absolute_import, division, print_function

import csv
import os

import nlp


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

_DATA_URL = "https://homes.cs.washington.edu/~msap/social-bias-frames/SocialBiasFrames_v2.tgz"


class SocialBiasFrames(nlp.GeneratorBasedBuilder):
    """TSocial Bias Frame"""

    def _info(self):
        return nlp.DatasetInfo(
            description=_DESCRIPTION,
            features=nlp.Features(
                {
                    "whoTarget": nlp.Value("string"),
                    "intentYN": nlp.Value("string"),
                    "sexYN": nlp.Value("string"),
                    "sexReason": nlp.Value("string"),
                    "offensiveYN": nlp.Value("string"),
                    "annotatorGender": nlp.Value("string"),
                    "annotatorMinority": nlp.Value("string"),
                    "sexPhrase": nlp.Value("string"),
                    "speakerMinorityYN": nlp.Value("string"),
                    "WorkerId": nlp.Value("string"),
                    "HITId": nlp.Value("string"),
                    "annotatorPolitics": nlp.Value("string"),
                    "annotatorRace": nlp.Value("string"),
                    "annotatorAge": nlp.Value("string"),
                    "post": nlp.Value("string"),
                    "targetMinority": nlp.Value("string"),
                    "targetCategory": nlp.Value("string"),
                    "targetStereotype": nlp.Value("string"),
                }
            ),
            # No default supervised_keys (as we have to pass both premise
            # and hypothesis as input).
            supervised_keys=None,
            homepage="https://homes.cs.washington.edu/~msap/social-bias-frames/",
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        dl_dir = dl_manager.download_and_extract(_DATA_URL)
        return [
            nlp.SplitGenerator(name=nlp.Split.TEST, gen_kwargs={"filepath": os.path.join(dl_dir, "SBFv2.tst.csv")}),
            nlp.SplitGenerator(
                name=nlp.Split.VALIDATION, gen_kwargs={"filepath": os.path.join(dl_dir, "SBFv2.dev.csv")}
            ),
            nlp.SplitGenerator(name=nlp.Split.TRAIN, gen_kwargs={"filepath": os.path.join(dl_dir, "SBFv2.trn.csv")}),
        ]

    def _generate_examples(self, filepath):
        """This function returns the examples in the raw (text) form."""
        with open(filepath) as f:
            reader = csv.DictReader(f)
            for idx, row in enumerate(reader):
                yield idx, row
