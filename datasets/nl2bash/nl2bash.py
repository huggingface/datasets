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
"""Natural Language and Bash Command Dataset"""
from __future__ import absolute_import, division, print_function
import json
import os
import datasets


_CITATION = """
@inproceedings{LinWZE2018:NL2Bash, 
  author = {Xi Victoria Lin and Chenglong Wang and Luke Zettlemoyer and Michael D. Ernst}, 
  title = {NL2Bash: A Corpus and Semantic Parser for Natural Language Interface to the Linux Operating System}, 
  booktitle = {Proceedings of the Eleventh International Conference on Language Resources
               and Evaluation {LREC} 2018, Miyazaki (Japan), 7-12 May, 2018.},
  year = {2018} 
}
"""
_DESCRIPTION = """A set of ~10,000 bash one-liners collected from websites such as StackOverflow paired with their English descriptions written by Bash programmers.

Dataset features includes:
  - nl_query: Input Natural Language Text.
  - cmd: Command corresponding to the nl_query.
This dataset can be downloaded upon requests
"""


class Nl2Bash(datasets.GeneratorBasedBuilder):
    VERSION = datasets.Version("1.0.0")
    _URL = r"https://public.boxcloud.com/d/1/b1!dEnPhi3cJnrTx38SOwI-VQgP3gdCXBMkpM9vwc8S_kZdT_yCJpChpWop8OQgYviNmDwlSn0WBTuNeSxzdZkOY_qKwn65h-6GVYb1Txx6ceDao68YEvCH0gnc6GPqwJ4DKewBtieKiI1vzvPPJnkGhFHdi-L1j5d6KNdLHF1OSUzLz67pFW5O4HVmDiV_28s11UwLzPCtKpKBKxBp5Ab3qYd7cjfJYwrmNM3r6mmMJeZgLYq5AJAZoX0PTlIxJNz6jZIJPxJdiK7TgnQq-roZoCpXkPtqSth_Dwd1pBdXpSqFZdJ_a6UGypvriGxqyJKkRr1k6yi3NhxKvMD3WoNb-vQOZm4bbghmWm_FENhXVwG9IsJ6xDhkZWvcI2zRnGP0SFoKBISky7shebItFUVmHbsM1mKMtjFanh6qLMo6ZZ3T7kYFR1PW0Rv7uFDOwlsvpHLHs0c3VS90kvU_sekrIUJ3obWRPbsLOTidWkn0P8koMzCtJdpUpwYw85LG1QYhWup0ZyDR_m0ivPbclN1aT6xOe0XKUAzAlZlJ18X-zpCrQHXRUxXWzuoQ31cCG5uy9kp8F1WQuvj7vpwvlfeZKD-Z4Ez9rEeCKXuijU_uQ6DoFfKvk5c8WgRGwpNHKCYFjvV-Ll9Fk89I5cGypXbSXCTa3a3zu2ytX9QVehIEhTsczK1WL9LnjcXIODUaDA40Mtp5fUbIizFMw4u3jTMAtbNf7btBa7ZbvJF_V-8Dt6nGMLytc4gXDbyMc_VHe_caTZqzHeezxHMF9nrCBpn4_0jLyiH33hL8-ADxTCF-P7k5hLRyAVka9fAlNoShTnHMsrkc7hkqcD_Z6dvuMmIrS4WOUZZon1ZUftGMou7slKYVa2krWRkwd0V-jH83A0fAQn7m1pgv8w6HSYExrA1KN73u0JSqoFM4N9Ujj4DMm9gwCPOfwwbFokOZlv61xR_0RE7cxm57sHZNiuVjiApbAyOBaJuV6lXg3BhbZlHJJiztLZE9rhR93JPp0-UAGfb_K5bmBJPnA_UoD5WqnhiPoYsTwyKZ5onYN6_IJ8F3WZAiUKjbWFGXz6cHy-5xmr_vkzojHlUjzEg1k-_MCuobsx_i4sY-1S4u1HsSoo6gbZRsEZ0VyAl6j7AiqUeWInsF3s263UA3QBdYDDSapv7DMY-_jG8MOcwqhzFPrtNK49brn1PlZnRMC6FaNUoG4sbIf7o8x7tMa_aQBpcRAWYqn5iTOklWECaTQBetxa6-_doweLSvlmqG3RdQSrM4SIVmtS79KzgN0SZqibdb5GM0PpmHBM5MhigQ3602PoPLboDOQtdKSPsGxXg./download"
    def _info(self):
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=datasets.Features({"nl_query": datasets.Value("string"), "cmd": datasets.Value("string")}),
            supervised_keys=[""],
            homepage="https://github.com/IBM/clai/blob/nlc2cmd/docs/nl2bash-data.md",
            citation=_CITATION,
        )
    def _split_generators(self, dl_manager):
        """ Downloads nl2bash-data.json """
        dl_manager._download_config = datasets.utils.file_utils.DownloadConfig()
        extracted_folder_path = dl_manager.download_and_extract(url_or_urls =self._URL)
        print(extracted_folder_path)
        return [datasets.SplitGenerator(name=datasets.Split.TRAIN, gen_kwargs={"datapath": extracted_folder_path})]
    def _get_examples(self, split_key, data_dir):
        """Returns natural language queries and the corresponding commands
        """
        file_dir = os.path.join(data_dir, "nl2bash-data.json")
        with open(file_dir, 'r') as f:
            data = json.load(f)

        data_len = len(data)

        # 80/10/10 split
        i1 = int(data_len * 0.8)
        i2 = int(data_len * 0.9)
        i3 = int(data_len*1.0)
        train_samples = [data[str(i)] for i in range(1,i1)]
        validation_samples = [data[str(i)] for i in range(i1,i2)]
        test_samples  = [data[str(i)] for i in range(i2,i3)]

        if split_key == "train":
            return (train_samples)
        if split_key == "validation":
            return (validation_samples)
        if split_key == "test":
            return (test_samples)
        else:
            raise ValueError(f"Invalid split key {split_key}")
    def _generate_examples(self,split,data_dir):
        """Given a split("train","validation","test") gets nl-cmd pair"""
        data = self._get_examples_from_split(split,data_dir)
        output_dict = {"nl_query" : [i["invocation"] for i in data],
                "cmd":[i["cmd"] for i in data]}
        yield output_dict