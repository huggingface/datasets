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

    def _generate_examples(self, files, split_name):
        cont = 0
        for path, f in files:
            # path are in the format ProgramData/{index}/{filename}
            label = int(path.split("/")[1])
            if self.SPLIT_RANGES[split_name][0] <= label <= self.SPLIT_RANGES[split_name][1]:
                js = {}
                js["label"] = str(label)
                js["id"] = cont
                js["code"] = f.read().decode("latin-1")
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
        name = self.config.name
        info = DEFINITIONS[name]
        archive = dl_manager.download(info["raw_url"] + "/programs.tar.gz")
        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={"files": dl_manager.iter_archive(archive), "split_name": "train"},
            ),
            datasets.SplitGenerator(
                name=datasets.Split.VALIDATION,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={"files": dl_manager.iter_archive(archive), "split_name": "valid"},
            ),
            datasets.SplitGenerator(
                name=datasets.Split.TEST,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={"files": dl_manager.iter_archive(archive), "split_name": "test"},
            ),
        ]

    def _generate_examples(self, files, split_name):
        return self.child._generate_examples(files, split_name)
