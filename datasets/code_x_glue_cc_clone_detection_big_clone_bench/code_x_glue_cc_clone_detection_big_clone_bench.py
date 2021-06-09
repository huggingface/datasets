from typing import List

import datasets

from .common import TrainValidTestChild
from .generated_definitions import DEFINITIONS


_DESCRIPTION = """Given two codes as the input, the task is to do binary classification (0/1), where 1 stands for semantic equivalence and 0 for others. Models are evaluated by F1 score.
The dataset we use is BigCloneBench and filtered following the paper Detecting Code Clones with Graph Neural Network and Flow-Augmented Abstract Syntax Tree."""

_CITATION = """@inproceedings{svajlenko2014towards,
title={Towards a big data curated benchmark of inter-project code clones},
author={Svajlenko, Jeffrey and Islam, Judith F and Keivanloo, Iman and Roy, Chanchal K and Mia, Mohammad Mamun},
booktitle={2014 IEEE International Conference on Software Maintenance and Evolution},
pages={476--480},
year={2014},
organization={IEEE}
}

@inproceedings{wang2020detecting,
title={Detecting Code Clones with Graph Neural Network and Flow-Augmented Abstract Syntax Tree},
author={Wang, Wenhan and Li, Ge and Ma, Bo and Xia, Xin and Jin, Zhi},
booktitle={2020 IEEE 27th International Conference on Software Analysis, Evolution and Reengineering (SANER)},
pages={261--271},
year={2020},
organization={IEEE}
}"""


class CodeXGlueCcCloneDetectionBigCloneBenchImpl(TrainValidTestChild):
    _DESCRIPTION = _DESCRIPTION
    _CITATION = _CITATION

    _FEATURES = {
        "id": datasets.Value("int32"),  # Index of the sample
        "id1": datasets.Value("int32"),  # The first function id
        "id2": datasets.Value("int32"),  # The second function id
        "func1": datasets.Value("string"),  # The full text of the first function
        "func2": datasets.Value("string"),  # The full text of the second function
        "label": datasets.Value("bool"),  # 1 is the functions are not equivalent, 0 otherwise
    }

    _SUPERVISED_KEYS = ["label"]

    def generate_urls(self, split_name):
        yield "index", f"{split_name}.txt"
        yield "data", "data.jsonl"

    def _generate_examples(self, split_name, file_paths):
        import json

        js_all = {}

        with open(file_paths["data"], encoding="utf-8") as f:
            for idx, line in enumerate(f):
                entry = json.loads(line)
                js_all[int(entry["idx"])] = entry["func"]

        with open(file_paths["index"], encoding="utf-8") as f:
            for idx, line in enumerate(f):
                line = line.strip()
                idx1, idx2, label = [int(i) for i in line.split("\t")]
                func1 = js_all[idx1]
                func2 = js_all[idx2]

                yield idx, dict(id=idx, id1=idx1, id2=idx2, func1=func1, func2=func2, label=(label == 1))


CLASS_MAPPING = {
    "CodeXGlueCcCloneDetectionBigCloneBench": CodeXGlueCcCloneDetectionBigCloneBenchImpl,
}


class CodeXGlueCcCloneDetectionBigCloneBench(datasets.GeneratorBasedBuilder):
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
