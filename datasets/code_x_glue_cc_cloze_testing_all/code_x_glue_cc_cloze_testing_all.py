import json
from typing import List

import datasets

from .common import Child
from .generated_definitions import DEFINITIONS


_DESCRIPTION = """Cloze tests are widely adopted in Natural Languages Processing to evaluate the performance of the trained language models. The task is aimed to predict the answers for the blank with the context of the blank, which can be formulated as a multi-choice classification problem.
Here we present the two cloze testing datasets in code domain with six different programming languages: ClozeTest-maxmin and ClozeTest-all. Each instance in the dataset contains a masked code function, its docstring and the target word.
The only difference between ClozeTest-maxmin and ClozeTest-all is their selected words sets, where ClozeTest-maxmin only contains two words while ClozeTest-all contains 930 words."""

_CITATION = """@article{CodeXGLUE,
title={CodeXGLUE: An Open Challenge for Code Intelligence},
journal={arXiv},
year={2020},
}
@article{feng2020codebert,
title={CodeBERT: A Pre-Trained Model for Programming and Natural Languages},
author={Feng, Zhangyin and Guo, Daya and Tang, Duyu and Duan, Nan and Feng, Xiaocheng and Gong, Ming and Shou, Linjun and Qin, Bing and Liu, Ting and Jiang, Daxin and others},
journal={arXiv preprint arXiv:2002.08155},
year={2020}
}
@article{husain2019codesearchnet,
title={CodeSearchNet Challenge: Evaluating the State of Semantic Code Search},
author={Husain, Hamel and Wu, Ho-Hsiang and Gazit, Tiferet and Allamanis, Miltiadis and Brockschmidt, Marc},
journal={arXiv preprint arXiv:1909.09436},
year={2019}
}"""


class CodeXGlueCcClozeTestingImpl(Child):
    _DESCRIPTION = _DESCRIPTION
    _CITATION = _CITATION

    _FEATURES = {
        "id": datasets.Value("int32"),  # Index of the sample
        "idx": datasets.Value("string"),  # Original index in the dataset
        "nl_tokens": datasets.features.Sequence(datasets.Value("string")),  # Natural language tokens
        "pl_tokens": datasets.features.Sequence(datasets.Value("string")),  # Programming language tokens
    }

    def generate_urls(self, split_name):
        yield "data", "clozeTest.json"

    def _generate_examples(self, split_name, file_paths):
        with open(file_paths["data"], encoding="utf-8") as f:
            j = json.load(f)
            index = 0
            for entry in j:
                yield index, dict(
                    id=index, idx=entry["idx"], nl_tokens=entry["nl_tokens"], pl_tokens=entry["pl_tokens"]
                )
                index += 1


CLASS_MAPPING = {
    "CodeXGlueCcClozeTestingAll": CodeXGlueCcClozeTestingImpl,
}


class CodeXGlueCcClozeTestingAll(datasets.GeneratorBasedBuilder):
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
