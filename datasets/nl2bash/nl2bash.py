"""Natural Language and Bash Command Dataset"""
from __future__ import absolute_import, division, print_function

import json
import os

import datasets


_CITATION = """
@inproceedings{LinWZE2018:NL2Bash, 
  author = {Xi Victoria Lin and Chenglong Wang and Luke Zettlemoyer and Michael D. Ernst}, 
  title = {NL2Bash: A Corpus and Semantic Parser for Natural Language Interface to the Linux Operating System}, 
  booktitle = {Proceedings of the Eleventh International Conference on Language Resources
               and Evaluation {LREC} 2018, Miyazaki (Japan), 7-12 May, 2018.},
  year = {2018} 
}
"""
_DESCRIPTION = """A set of ~10,000 bash one-liners collected from websites such as StackOverflow paired with their English descriptions written by Bash programmers.

Dataset features includes:
  - nl_query: Input Natural Language Text.
  - cmd: Command corresponding to the nl_query.
This dataset can be downloaded upon requests
"""
_URL = "https://ibm.ent.box.com/v/nl2bash-data"


class Nl2Bash(datasets.GeneratorBasedBuilder):
    VERSION = datasets.Version("1.0.0")

    def _info(self):
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=datasets.Features(
                {"nl_query": datasets.Value("string"), "cmd": datasets.Value("string")}
            ),
            supervised_keys=[""],
            homepage="https://github.com/IBM/clai/blob/nlc2cmd/docs/nl2bash-data.md",
            citation=_CITATION,
        )
    def _split_generators(self, dl_manager):
        """ Downloads Rotten Tomatoes sentences. """
        extracted_folder_path = dl_manager.download_and_extract(_URL)
        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                gen_kwargs={"split_key": "train", "data_dir": extracted_folder_path},
            ),
            datasets.SplitGenerator(
                name=datasets.Split.VALIDATION,
                gen_kwargs={"split_key": "validation", "data_dir": extracted_folder_path},
            ),
            datasets.SplitGenerator(
                name=datasets.Split.TEST,
                gen_kwargs={"split_key": "test", "data_dir": extracted_folder_path},
            ),
        ]
    def _get_examples_from_split(self, split_key, data_dir):
        """Reads Rotten Tomatoes sentences and splits into 80% train,
        10% validation, and 10% test, as is the practice set out in Jinfeng
        Li, ``TEXTBUGGER: Generating Adversarial Text Against Real-world
        Applications.''
        """
        file_dir = os.path.join(data_dir, "nl2bash-data.json")
        with open(file_dir, 'r') as f:
            data = json.load(f)

        data_len = len(data)

        # 80/10/10 split
        i1 = int(data_len * 0.8)
        i2 = int(data_len * 0.9)
        i3 = int(data_len*1.0)
        train_samples = [data[str(i)] for i in range(0,i1)]
        validation_samples = [data[str(i)] for i in range(i1,i2)]
        test_samples  = [data[str(i)] for i in range(i2,i3)]
        train_samples = data[:i1] + data[:i1]

        if split_key == "train":
            return (train_samples)
        if split_key == "validation":
            return (validation_samples)
        if split_key == "test":
            return (test_samples)
        else:
            raise ValueError(f"Invalid split key {split_key}")
    def _generate_examples(self,split,data_dir):
        data = self._get_examples_from_split(split,data_dir)
        yield {"nl_query" : [i["invocation"] for i in data],
                "cmd":[i["cmd"] for i in data]}
