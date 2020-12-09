from typing import List

import datasets

from .common import TrainValidTestChild
from .generated_definitions import DEFINITIONS


class CodeXGlueCCCodeRefinement(TrainValidTestChild):
    _DESCRIPTION = """We use the dataset released by this paper(https://arxiv.org/pdf/1812.08693.pdf). The source side is a Java function with bugs and the target side is the refined one. All the function and variable names are normalized. Their dataset contains two subsets ( i.e.small and medium) based on the function length."""
    _FEATURES = {
        "id": datasets.Value("int32"),  # Index of the sample
        "buggy": datasets.Value("string"),  # The buggy version of the code
        "fixed": datasets.Value("string"),  # The correct version of the code
    }

    _SUPERVISED_KEYS = ["fixed"]

    def generate_urls(self, split_name):
        size = self.info["parameters"]["size"]
        for key in "buggy", "fixed":
            yield key, f"{size}/{split_name}.buggy-fixed.{key}"

    def _generate_examples(self, split_name, file_pathes):
        """This function returns the examples in the raw (text) form."""
        # Open each file (one for java, and one for c#)
        files = {k: open(file_pathes[k]) for k in file_pathes}

        id_ = 0
        while True:
            # Read a single line from each file
            entries = {k: files[k].readline() for k in file_pathes}

            empty = self.check_empty(entries)
            if empty:
                # We are done: end of files
                return

            entries["id"] = id_
            yield id_, entries
            id_ += 1


CLASS_MAPPING = {
    "CodeXGlueCCCodeRefinement": CodeXGlueCCCodeRefinement,
}


class CodeXGlueCCCodeRefinementMain(datasets.GeneratorBasedBuilder):
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
