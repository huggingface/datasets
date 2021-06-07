import json
from typing import List

import datasets

from .common import Child
from .generated_definitions import DEFINITIONS


_DESCRIPTION = """We use concode dataset which is a widely used code generation dataset from Iyer's EMNLP 2018 paper Mapping Language to Code in Programmatic Context. See paper for details."""
_CITATION = """@article{iyer2018mapping,
title={Mapping language to code in programmatic context},
author={Iyer, Srinivasan and Konstas, Ioannis and Cheung, Alvin and Zettlemoyer, Luke},
journal={arXiv preprint arXiv:1808.09588},
year={2018}
}"""


class CodeXGlueTcTextToCodeImpl(Child):
    _DESCRIPTION = _DESCRIPTION
    _CITATION = _CITATION

    _FEATURES = {
        "id": datasets.Value("int32"),  # Index of the sample
        "nl": datasets.Value("string"),  # The natural language description of the task
        "code": datasets.Value("string"),  # The programming source code for the task
    }

    _SUPERVISED_KEYS = ["code"]

    SPLITS = {"train": datasets.Split.TRAIN, "dev": datasets.Split.VALIDATION, "test": datasets.Split.TEST}

    def generate_urls(self, split_name):
        yield "data", f"concode/{split_name}.json"

    def _generate_examples(self, split_name, file_paths):
        with open(file_paths["data"], encoding="utf-8") as f:
            for idx, line in enumerate(f):
                entry = json.loads(line)
                entry["id"] = idx
                yield idx, entry


CLASS_MAPPING = {
    "CodeXGlueTcTextToCode": CodeXGlueTcTextToCodeImpl,
}


class CodeXGlueTcTextToCode(datasets.GeneratorBasedBuilder):
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
