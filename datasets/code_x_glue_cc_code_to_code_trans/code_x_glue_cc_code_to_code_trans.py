from typing import List

import datasets

from .generated_definitions import DEFINITIONS

import datasets
import json
import os
import os.path
from .common import Child
from .common import TrainValidTestChild
class CodeXGlueCCCodeToCodeTrans(TrainValidTestChild):
    _DESCRIPTION = """The dataset is collected from several public repos, including Lucene(http://lucene.apache.org/), POI(http://poi.apache.org/), JGit(https://github.com/eclipse/jgit/) and Antlr(https://github.com/antlr/).
        We collect both the Java and C# versions of the codes and find the parallel functions. After removing duplicates and functions with the empty body, we split the whole dataset into training, validation and test sets."""
    _FEATURES = {
        "id": datasets.Value("int32"), # Index of the sample
        "java": datasets.Value("string"),  # The java version of the code
        "cs": datasets.Value("string"),  # The C# version of the code
    }

    def generate_urls(self, split_name):
        for key in "cs", "java":
            yield key, f"{split_name}.java-cs.txt.{key}"

    def _generate_examples(self, split_name, file_paths):
        """This function returns the examples in the raw (text) form."""
        # Open each file (one for java, and one for c#)
        files = {k: open(file_paths[k]) for k in file_paths}

        id_ = 0
        while True:
            # Read a single line from each file
            entries = {k: files[k].readline() for k in file_paths}

            empty = self.check_empty(entries)
            if empty:
                # We are done: end of files
                return

            entries["id"] = id_
            yield id_, entries
            id_ += 1




CLASS_MAPPING={'CodeXGlueCCCodeToCodeTrans':CodeXGlueCCCodeToCodeTrans,
}



class CodeXGlueCCCodeToCodeTransMain(datasets.GeneratorBasedBuilder):
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
