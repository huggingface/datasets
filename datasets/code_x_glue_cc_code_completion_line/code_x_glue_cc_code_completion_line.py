import json
from typing import List

import datasets

from .common import Child
from .generated_definitions import DEFINITIONS


_DESCRIPTION = """Complete the unfinished line given previous context. Models are evaluated by exact match and edit similarity.
We propose line completion task to test model's ability to autocomplete a line. Majority code completion systems behave well in token level completion, but fail in completing an unfinished line like a method call with specific parameters, a function signature, a loop condition, a variable definition and so on. When a software develop finish one or more tokens of the current line, the line level completion model is expected to generate the entire line of syntactically correct code.
Line level code completion task shares the train/dev dataset with token level completion. After training a model on CodeCompletion-token, you could directly use it to test on line-level completion."""

_CITATION = """@article{raychev2016probabilistic,
title={Probabilistic Model for Code with Decision Trees},
author={Raychev, Veselin and Bielik, Pavol and Vechev, Martin},
journal={ACM SIGPLAN Notices},
pages={731--747},
year={2016},
publisher={ACM New York, NY, USA}
}
@inproceedings{allamanis2013mining,
title={Mining Source Code Repositories at Massive Scale using Language Modeling},
author={Allamanis, Miltiadis and Sutton, Charles},
booktitle={2013 10th Working Conference on Mining Software Repositories (MSR)},
pages={207--216},
year={2013},
organization={IEEE}
}"""


class CodeXGlueCcCodeCompletionLineImpl(Child):
    _DESCRIPTION = _DESCRIPTION
    _CITATION = _CITATION

    _FEATURES = {
        "id": datasets.Value("int32"),  # Index of the sample
        "input": datasets.Value("string"),  # Input code string
        "gt": datasets.Value("string"),  # Code string to be predicted
    }

    _SUPERVISED_KEYS = ["gt"]

    def generate_urls(self, split_name):
        yield "data", "test.json"

    def _generate_examples(self, split_name, file_paths):
        with open(file_paths["data"], encoding="utf-8") as f:
            for idx, line in enumerate(f):
                entry = json.loads(line)
                entry["id"] = idx
                yield idx, entry


CLASS_MAPPING = {
    "CodeXGlueCcCodeCompletionLine": CodeXGlueCcCodeCompletionLineImpl,
}


class CodeXGlueCcCodeCompletionLine(datasets.GeneratorBasedBuilder):
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
