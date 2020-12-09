import json
import os
import os.path
from typing import List

import datasets

from .common import TrainValidTestChild
from .generated_definitions import DEFINITIONS


class CodeXGlueCCCloneDetectionPOJ104(TrainValidTestChild):
    _DESCRIPTION = """Given a code and a collection of candidates as the input, the task is to return Top K codes with the same semantic. Models are evaluated by MAP score.
We use POJ-104 dataset on this task."""

    _CITATION = """@inproceedings{mou2016convolutional,
  title={Convolutional neural networks over tree structures for programming language processing},
  author={Mou, Lili and Li, Ge and Zhang, Lu and Wang, Tao and Jin, Zhi},
  booktitle={Proceedings of the Thirtieth AAAI Conference on Artificial Intelligence},
  pages={1287--1293},
  year={2016}
}"""
    _FEATURES = {
        "id": datasets.Value("int32"),  # Index of the sample
        "code": datasets.Value("string"),  # The full text of the function
        "label": datasets.Value("string"),  # The id of problem that the source code solves
    }

    _SUPERVISED_KEYS = ["label"]

    SPLIT_RANGES = {"train": (1, 65), "valid": (65, 81), "test": (81, 195)}

    def generate_urls(self, split_name):
        yield "data", "programs.tar.gz"

    def pregenerate_all(self, root_path):
        def files(path):
            g = os.walk(path)
            file = []
            for path, dir_list, file_list in g:
                for file_name in file_list:
                    file.append(os.path.join(path, file_name))
            return file

        cont = 0
        for split_name, range_info in self.SPLIT_RANGES.items():
            with open(os.path.join(root_path, f"{split_name}.jsonl"), "w") as f:
                for i in range(*range_info):
                    items = files(os.path.join(root_path, "ProgramData/{}".format(i)))
                    for item in items:
                        js = {}
                        js["label"] = item.split("/")[1]
                        js["index"] = str(cont)
                        js["code"] = open(item, encoding="latin-1").read()
                        f.write(json.dumps(js) + "\n")
                        cont += 1

    def _generate_examples(self, split_name, file_pathes):
        root_path = file_pathes["data"]

        mark_file = os.path.join(root_path, ".mark")

        if not os.path.exists(mark_file):
            self.pregenerate_all(root_path)

        with open(mark_file, "w") as f:
            f.write("finished")

        json_file = os.path.join(root_path, f"{split_name}.jsonl")

        with open(json_file) as f:
            for idx, line in enumerate(f):
                entry = json.loads(line)
                idx = int(entry["index"])
                label = entry["label"]
                e = dict(id=idx, label=label, code=entry["code"])
                yield idx, e


CLASS_MAPPING = {
    "CodeXGlueCCCloneDetectionPOJ104": CodeXGlueCCCloneDetectionPOJ104,
}


class CodeXGlueCCCloneDetectionPoj104Main(datasets.GeneratorBasedBuilder):
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

    def _generate_examples(self, split_name, file_pathes):
        return self.child._generate_examples(split_name, file_pathes)
