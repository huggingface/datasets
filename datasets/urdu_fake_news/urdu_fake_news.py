"""Urdu Fake News Dataset"""


import glob
import os

import datasets


_CITATION = """
@article{MaazUrdufake2020,
author = {Amjad, Maaz and Sidorov, Grigori and Zhila, Alisa and  G’{o}mez-Adorno, Helena and Voronkov, Ilia  and Gelbukh, Alexander},
title = {Bend the Truth: A Benchmark Dataset for Fake News Detection in Urdu and Its Evaluation},
journal={Journal of Intelligent & Fuzzy Systems},
volume={39},
number={2},
pages={2457-2469},
doi = {10.3233/JIFS-179905},
year={2020},
publisher={IOS Press}
}
"""

_DESCRIPTION = """
Urdu fake news datasets that contain news of 5 different news domains.
These domains are Sports, Health, Technology, Entertainment, and Business.
The real news are collected by combining manual approaches.
"""

_URL = "https://github.com/MaazAmjad/Datasets-for-Urdu-news/blob/master/"
_URL += "Urdu%20Fake%20News%20Dataset.zip?raw=true"


class UrduFakeNews(datasets.GeneratorBasedBuilder):
    VERSION = datasets.Version("1.0.0")

    category_list = [
        "bus",
        "hlth",
        "sp",
        "tch",
        "sbz",
    ]

    def _info(self):
        labels_list = ["Fake", "Real"]

        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=datasets.Features(
                {
                    "news": datasets.Value("string"),
                    "label": datasets.ClassLabel(names=labels_list),
                    "category": datasets.ClassLabel(names=self.category_list),
                }
            ),
            homepage="https://github.com/MaazAmjad/Datasets-for-Urdu-news",
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        """Returns SplitGenerators."""
        dl_path = dl_manager.download_and_extract(_URL)
        input_path = os.path.join(dl_path, "1.Corpus")
        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                gen_kwargs={"pattern": os.path.join(input_path, "Train", "*", "*.txt")},
            ),
            datasets.SplitGenerator(
                name=datasets.Split.TEST,
                gen_kwargs={"pattern": os.path.join(input_path, "Test", "*", "*.txt")},
            ),
        ]

    def _generate_examples(self, pattern=None):
        """Yields examples."""
        for filename in sorted(glob.glob(pattern)):

            with open(filename, encoding="utf-8") as f:
                news = ""
                for line in f:
                    if line == "\n":
                        continue
                    news += line

            name = os.path.basename(filename)
            key = name.rstrip(".txt")

            _class = 1 if ("Real" in filename) else 0
            _class_name = "Real" if ("Real" in filename) else "Fake"
            category = "".join([i for i in key if not i.isdigit()])
            if category == "":
                continue
            category = self.category_list.index(category)

            yield f"{_class_name}_{key}", {"news": news, "label": _class, "category": category}
