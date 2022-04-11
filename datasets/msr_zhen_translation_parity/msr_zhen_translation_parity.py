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
"""Microsoft Research: Translator Human Parity Data"""


import os

import datasets


_DESCRIPTION = """\
Translator Human Parity Data

Human evaluation results and translation output for the Translator Human Parity Data release,
as described in https://blogs.microsoft.com/ai/machine-translation-news-test-set-human-parity/.
The Translator Human Parity Data release contains all human evaluation results and translations
related to our paper "Achieving Human Parity on Automatic Chinese to English News Translation",
published on March 14, 2018.
"""

_LICENSE = """\
See the Microsoft Research Data License Agreement.
"""

_CITATION = """\
@misc{hassan2018achieving,
      title={Achieving Human Parity on Automatic Chinese to English News Translation},
      author={ Hany Hassan and Anthony Aue and Chang Chen and Vishal Chowdhary and Jonathan Clark
               and Christian Federmann and Xuedong Huang and Marcin Junczys-Dowmunt and William Lewis
               and Mu Li and Shujie Liu and Tie-Yan Liu and Renqian Luo and Arul Menezes and Tao Qin
               and Frank Seide and Xu Tan and Fei Tian and Lijun Wu and Shuangzhi Wu and Yingce Xia
               and Dongdong Zhang and Zhirui Zhang and Ming Zhou},
      year={2018},
      eprint={1803.05567},
      archivePrefix={arXiv},
      primaryClass={cs.CL}
}"""

_FILE_PATHS = [
    ["References", "Translator-HumanParityData-Reference-HT.txt"],
    ["References", "Translator-HumanParityData-Reference-PE.txt"],
    ["Translations", "Translator-HumanParityData-Combo-4.txt"],
    ["Translations", "Translator-HumanParityData-Combo-5.txt"],
    ["Translations", "Translator-HumanParityData-Combo-6.txt"],
    ["Translations", "Translator-HumanParityData-Online-A-1710.txt"],
]

_FEATURE_NAMES = ["Reference-HT", "Reference-PE", "Combo-4", "Combo-5", "Combo-6", "Online-A-1710"]


class MsrZhenTranslationParity(datasets.GeneratorBasedBuilder):
    """Microsoft Research: Translator Human Parity Data"""

    VERSION = datasets.Version("1.0.0")

    @property
    def manual_download_instructions(self):
        return """\
    You need to go to https://msropendata.com/datasets/93f9aa87-9491-45ac-81c1-6498b6be0d0b,
    and manually download translatorhumanparitydata2.zip (or translatorhumanparitydata2.tar.gz).
    Once it is completed, extract its content into a directory, <path/to/folder>.
    Within this directory, there are three subdirectories, Translations, References, and Evaluations.
    The <path/to/folder> can e.g. be "~/Downloads/translatorhumanparitydata2", if you just double click the .zip file.
    msr_zhen_translation_parity can then be loaded using the following command
    `datasets.load_dataset("msr_zhen_translation_parity", data_dir="<path/to/folder>")`.
    """

    def _info(self):
        feature_names = _FEATURE_NAMES
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=datasets.Features({k: datasets.Value("string") for k in feature_names}),
            supervised_keys=None,
            homepage="https://msropendata.com/datasets/93f9aa87-9491-45ac-81c1-6498b6be0d0b",
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        """Returns SplitGenerators."""
        path_to_manual_file = os.path.abspath(os.path.expanduser(dl_manager.manual_dir))

        if not os.path.exists(path_to_manual_file):
            raise FileNotFoundError(
                f"{path_to_manual_file} does not exist. Make sure you insert a manual dir via `datasets.load_dataset('msr_zhen_translation_parity', data_dir=...)`. Manual download instructions: {self.manual_download_instructions})"
            )
        return [datasets.SplitGenerator(name=datasets.Split.TRAIN, gen_kwargs={"path": path_to_manual_file})]

    def _generate_examples(self, path=None, title_set=None):
        data = []
        for fp in _FILE_PATHS:
            filepath = os.path.join(path, fp[0], fp[1])
            with open(filepath, encoding="utf-8-sig") as f:
                data.append(f.readlines())
        examples = len(data[0])
        for i in range(examples):
            record = [x[i].rstrip("\r\n") for x in data]
            yield i, dict(zip(_FEATURE_NAMES, record))
