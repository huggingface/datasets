from typing import List

import datasets

from .common import TrainValidTestChild
from .generated_definitions import DEFINITIONS


_DESCRIPTION = """Given a source code, the task is to identify whether it is an insecure code that may attack software systems, such as resource leaks, use-after-free vulnerabilities and DoS attack. We treat the task as binary classification (0/1), where 1 stands for insecure code and 0 for secure code.
The dataset we use comes from the paper Devign: Effective Vulnerability Identification by Learning Comprehensive Program Semantics via Graph Neural Networks. We combine all projects and split 80%/10%/10% for training/dev/test."""
_CITATION = """@inproceedings{zhou2019devign,
title={Devign: Effective vulnerability identification by learning comprehensive program semantics via graph neural networks},
author={Zhou, Yaqin and Liu, Shangqing and Siow, Jingkai and Du, Xiaoning and Liu, Yang},
booktitle={Advances in Neural Information Processing Systems},
pages={10197--10207}, year={2019}"""


class CodeXGlueCcDefectDetectionImpl(TrainValidTestChild):
    _DESCRIPTION = _DESCRIPTION
    _CITATION = _CITATION

    _FEATURES = {
        "id": datasets.Value("int32"),  # Index of the sample
        "func": datasets.Value("string"),  # The source code
        "target": datasets.Value("bool"),  # 0 or 1 (vulnerability or not)
        "project": datasets.Value("string"),  # Original project that contains this code
        "commit_id": datasets.Value("string"),  # Commit identifier in the original project
    }
    _SUPERVISED_KEYS = ["target"]

    def generate_urls(self, split_name):
        yield "index", f"{split_name}.txt"
        yield "data", "function.json"

    def _generate_examples(self, split_name, file_paths):
        import json

        js_all = json.load(open(file_paths["data"], encoding="utf-8"))

        index = set()
        with open(file_paths["index"], encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                index.add(int(line))

        for idx, js in enumerate(js_all):
            if idx in index:
                js["id"] = idx
                js["target"] = int(js["target"]) == 1
                yield idx, js


CLASS_MAPPING = {
    "CodeXGlueCcDefectDetection": CodeXGlueCcDefectDetectionImpl,
}


class CodeXGlueCcDefectDetection(datasets.GeneratorBasedBuilder):
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
