"""TODO concode - code2text pairs dataset"""
import json
import logging

import datasets


_CITATION = """\
@article{iyer2018mapping,
  title={Mapping language to code in programmatic context},
  author={Iyer, Srinivasan and Konstas, Ioannis and Cheung, Alvin and Zettlemoyer, Luke},
  journal={arXiv preprint arXiv: 1808.09588},
  year=2018,}"""
_URL = "https://raw.githubusercontent.com/microsoft/CodeXGLUE/main/Text-Code/text-to-code/dataset/concode/"
_URLS = {
    "train": _URL + "train.json",
    "dev": _URL + "dev.json",
    "test": _URL + "test.json",
}
_DESCRIPTION = """Mapping Language to Code in a Programmatic Context.
concode dataset which a widely used code generation dataset from Iyer's EMNLP 2018 paper
Generate source code of class member functions in Java, given natural language descriptionand class environment. Class environment is the programmatic context provided by therest of the class, including other member variables and member functions in class.
"""


class CodeXGlue_ConcodeConfig(datasets.BuilderConfig):
    """BuilderConfig for Concode Dataset."""

    def __init__(self, **kwargs):
        """BuilderConfig for Concode.
        Args:
          **kwargs: keyword arguments forwarded to super.
        """
        super(CodeXGlue_ConcodeConfig, self).__init__(**kwargs)


class Concode(datasets.GeneratorBasedBuilder):
    """ConCode: code generation dataset for java NL queries(pre-processed)"""

    VERSION = datasets.Version("1.0.0")

    BUILDER_CONFIGS = [
        CodeXGlue_ConcodeConfig(
            name="plain_text",
            version=VERSION,
            description="Plain text",
        )
    ]

    def _info(self):
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=datasets.Features(
                {
                    "natural_lang": datasets.Value("string"),
                    "code": datasets.Value("string"),
                }
            ),
            supervised_keys=("ml4code", "source code"),
            homepage="https: //github.com/sriniiyer/concode",
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        """Returns SplitGenerators."""
        dl_path = dl_manager.download(_URLS)
        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                gen_kwargs={"filename": dl_path["train"]},
            ),
            datasets.SplitGenerator(
                name=datasets.Split.VALIDATION,
                gen_kwargs={"filename": dl_path["dev"]},
            ),
            datasets.SplitGenerator(
                name=datasets.Split.TEST,
                gen_kwargs={"filename": dl_path["test"]},
            ),
        ]

    def _generate_examples(self, filename):
        """Yields examples.
        Each example contains a Natural Language Query and the corresponding Code.
        Args:
          filename: path of the file to be read.
        Yields:
          A dictionary of natural_lang and corresponding code in code field
        """
        logging.info("Generating examples from from %s split ", filename)
        id = 0
        with open(filename, encoding="utf-8") as f:
            for elem_data in f:
                elem_data = json.loads(elem_data)
                elem_data = {"natural_lang": elem_data["nl"], "code": elem_data["code"]}
                yield id, elem_data
                id += 1  # increment id
