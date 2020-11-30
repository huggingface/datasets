"""concode - code2text pairs dataset"""
import datasets

from __future__ import absolute_import, division, print_function

import json
import logging
import os

_CITATION = """\
@article{iyer2018mapping,
  title={Mapping language to code in programmatic context},
  author={Iyer, Srinivasan and Konstas, Ioannis and Cheung, Alvin and Zettlemoyer, Luke},
  journal={arXiv preprint arXiv:1808.09588},
  year=2018,
}
"""
_URL = "https://raw.githubusercontent.com/microsoft/CodeXGLUE/main/Text-Code/text-to-code/dataset/concode/"
_URLS = {
    "train": _URL + "train.json",
    "valid": _URL + "dev.json",
    "test": _URL + "test.json",
}

_DESCRIPTION = """Mapping Language to Code in a Programmatic Context"""

class ConcodeConfig(datasets.BuilderConfig):
    """BuilderConfig for Concode Dataset."""

    def __init__(self, **kwargs):
        """BuilderConfig for Concode.

        Args:
          **kwargs: keyword arguments forwarded to super.
        """
        super(ConcodeConfig, self).__init__(**kwargs)

class Concode(datasets.GeneratorBasedBuilder):
    """ConCode: code generation dataset for java NL queries(pre-processed)"""
    VERSION = datasets.Version("1.0.0")

    BUILDER_CONFIGS = [
        ConcodeConfig(
            name="plain_text",
            version=VERSION,
            description="Plain text",
        ),
    ]
    def _info(self):
            return datasets.DatasetInfo(
                description=_DESCRIPTION,
                features=datasets.Features(
                    {
                        "nl": datasets.Value("string"),
                        "code": datasets.Value("string"),
                    }),
            supervised_keys=("ml4code", "source code"),
            homepage="https://github.com/sriniiyer/concode",
            citation=_CITATION,
            )
    def _split_generators(self, dl_manager):
        """Returns SplitGenerators."""
        dl_path = dl_manager.download(_URLS) 
        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                gen_kwargs={"filename": os.path.join(dl_path, "train.json")},
            ),
            datasets.SplitGenerator(
                name=datasets.Split.VALIDATION,
                gen_kwargs={
                    "filename": os.path.join(dl_path, "dev.json")},
            ),
            datasets.SplitGenerator(
                name=datasets.Split.TEST,
                gen_kwargs={
                    "filename": os.path.join(dl_path, "test.json")},
            ),
        ]
    def _generate_examples(self,filepath):
        """Yields examples.

        Each example contains a Nl Query and the corresponding Code.

        Args:
          split: The split to be read(train/dev/test).


        Yields:
          A dictionary of features, all floating point except the input text.
        """
        split = filepath.split(os.sep)[-1].split(".")[-2]
        logging.info("Generating examples from from %s split ",split)
        with open(filepath, encoding="utf-8") as f:
            data = json.load(f)
            nl_list = []
            code_list = []
            for elem_data in data:
                nl_list.append(elem_data["nl"])
                code_list.append(elem_data["code"])
            id = split
            yield id,{"nl":nl_list,"code":code_list}
