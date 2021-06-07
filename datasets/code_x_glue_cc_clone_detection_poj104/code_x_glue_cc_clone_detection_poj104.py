import os
import os.path
from typing import List

import datasets

from .common import TrainValidTestChild
from .generated_definitions import DEFINITIONS


_DESCRIPTION = """Given a code and a collection of candidates as the input, the task is to return Top K codes with the same semantic. Models are evaluated by MAP score.
We use POJ-104 dataset on this task."""

_CITATION = """@inproceedings{mou2016convolutional,
title={Convolutional neural networks over tree structures for programming language processing},
author={Mou, Lili and Li, Ge and Zhang, Lu and Wang, Tao and Jin, Zhi},
booktitle={Proceedings of the Thirtieth AAAI Conference on Artificial Intelligence},
pages={1287--1293},
year={2016}
}"""


class CodeXGlueCcCloneDetectionPoj104Impl(TrainValidTestChild):
    _DESCRIPTION = _DESCRIPTION
    _CITATION = _CITATION

    _FEATURES = {
        "id": datasets.Value("int32"),  # Index of the sample
        "code": datasets.Value("string"),  # The full text of the function
        "label": datasets.Value("string"),  # The id of problem that the source code solves
    }

    _SUPERVISED_KEYS = ["label"]

    SPLIT_RANGES = {"train": (1, 65), "valid": (65, 81), "test": (81, 195)}

    def generate_urls(self, split_name):
        yield "data", "programs.tar.gz"

    def _generate_examples(self, split_name, file_paths):
        def files(path):
            g = os.walk(path)
            file = []
            for path, dir_list, file_list in g:
                for file_name in file_list:
                    file.append(os.path.join(path, file_name))
            return file

        root_path = file_paths["data"]
        cont = 0
        for i in range(*self.SPLIT_RANGES[split_name]):
            items = files(os.path.join(root_path, "ProgramData/{}".format(i)))
            for item in items:
                js = {}
                js["label"] = item.split("/")[1]
                js["id"] = cont
                js["code"] = open(item, encoding="latin-1").read()
                yield cont, js
                cont += 1


CLASS_MAPPING = {
    "CodeXGlueCcCloneDetectionPoj104": CodeXGlueCcCloneDetectionPoj104Impl,
}


class CodeXGlueCcCloneDetectionPoj104(datasets.GeneratorBasedBuilder):
    BUILDER_CONFIG_CLASS = datasets.BuilderConfig
    BUILDER_CONFIGS = [
        datasets.BuilderConfig(name=name, description=info["description"]) for name, info in DEFINITIONS.items()
    ]

    def _info(self):
        name = self.config.name
        info = DEFINITIONS[name]
        if info["class_name"] in CLASS_MAPPING:
            self.child = CLASS_MAPPING[info["class_name"]](info)
        else:
            raise RuntimeError(f"Unknown python class for dataset configuration {name}")
        ret = self.child._info()
        return ret

    def _split_generators(self, dl_manager: datasets.DownloadManager) -> List[datasets.SplitGenerator]:
        return self.child._split_generators(dl_manager=dl_manager)

    def _generate_examples(self, split_name, file_paths):
        return self.child._generate_examples(split_name, file_paths)
