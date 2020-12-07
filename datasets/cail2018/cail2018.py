from __future__ import absolute_import, division, print_function

import json
import os

import datasets


_CITATION = """\
@misc{xiao2018cail2018,
      title={CAIL2018: A Large-Scale Legal Dataset for Judgment Prediction},
      author={Chaojun Xiao and Haoxi Zhong and Zhipeng Guo and Cunchao Tu and Zhiyuan Liu and Maosong Sun and Yansong Feng and Xianpei Han and Zhen Hu and Heng Wang and Jianfeng Xu},
      year={2018},
      eprint={1807.02478},
      archivePrefix={arXiv},
      primaryClass={cs.CL}
}
"""

_DESCRIPTION = """\
In this paper, we introduce Chinese AI and Law challenge dataset (CAIL2018),
the first large-scale Chinese legal dataset for judgment prediction. CAIL contains more than 2.6 million
criminal cases published by the Supreme People's Court of China, which are several times larger than other
datasets in existing works on judgment prediction. Moreover, the annotations of judgment results are more
detailed and rich. It consists of applicable law articles, charges, and prison terms, which are expected
to be inferred according to the fact descriptions of cases. For comparison, we implement several conventional
text classification baselines for judgment prediction and experimental results show that it is still a
challenge for current models to predict the judgment results of legal cases, especially on prison terms.
To help the researchers make improvements on legal judgment prediction.
"""
_URL = "https://cail.oss-cn-qingdao.aliyuncs.com/CAIL2018_ALL_DATA.zip"


class Cail2018(datasets.GeneratorBasedBuilder):
    VERSION = datasets.Version("1.0.0")

    def _info(self):
        features = datasets.Features(
            {
                "fact": datasets.Value("string"),
                "relevant_articles": datasets.Sequence(datasets.Value("int32")),
                "accusation": datasets.Sequence(datasets.Value("string")),
                "punish_of_money": datasets.Value("float"),
                "criminals": datasets.Sequence(datasets.Value("string")),
                "death_penalty": datasets.Value("bool"),
                "imprisonment": datasets.Value("float"),
                "life_imprisonment": datasets.Value("bool"),
            }
        )
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=features,
            homepage="https://arxiv.org/abs/1807.02478",
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        """Returns SplitGenerators."""

        dl_dir = dl_manager.download_and_extract(_URL)

        return [
            datasets.SplitGenerator(
                name=datasets.Split("exercise_contest_train"),
                gen_kwargs={
                    "filepath": os.path.join(dl_dir, "final_all_data/exercise_contest/data_train.json"),
                    "split": "exercise_contest_train",
                },
            ),
            datasets.SplitGenerator(
                name=datasets.Split("exercise_contest_valid"),
                gen_kwargs={
                    "filepath": os.path.join(dl_dir, "final_all_data/exercise_contest/data_valid.json"),
                    "split": "exercise_contest_valid",
                },
            ),
            datasets.SplitGenerator(
                name=datasets.Split("exercise_contest_test"),
                gen_kwargs={
                    "filepath": os.path.join(dl_dir, "final_all_data/exercise_contest/data_test.json"),
                    "split": "exercise_contest_test",
                },
            ),
            datasets.SplitGenerator(
                name=datasets.Split("first_stage_train"),
                gen_kwargs={
                    "filepath": os.path.join(dl_dir, "final_all_data/first_stage/train.json"),
                    "split": "first_stage_train",
                },
            ),
            datasets.SplitGenerator(
                name=datasets.Split("first_stage_test"),
                gen_kwargs={
                    "filepath": os.path.join(dl_dir, "final_all_data/first_stage/test.json"),
                    "split": "first_stage_test",
                },
            ),
            datasets.SplitGenerator(
                name=datasets.Split("final_test"),
                gen_kwargs={"filepath": os.path.join(dl_dir, "final_all_data/final_test.json"), "split": "final_test"},
            ),
        ]

    def _generate_examples(self, filepath, split):
        """Yields examples."""
        with open(filepath, encoding="utf-8") as f:
            for idx, row in enumerate(f):
                data = json.loads(row)
                yield idx, {
                    "fact": data["fact"],
                    "relevant_articles": data["meta"]["relevant_articles"],
                    "accusation": data["meta"]["accusation"],
                    "punish_of_money": data["meta"]["punish_of_money"],
                    "criminals": data["meta"]["criminals"],
                    "death_penalty": data["meta"]["term_of_imprisonment"]["death_penalty"],
                    "imprisonment": data["meta"]["term_of_imprisonment"]["imprisonment"],
                    "life_imprisonment": data["meta"]["term_of_imprisonment"]["life_imprisonment"],
                }
