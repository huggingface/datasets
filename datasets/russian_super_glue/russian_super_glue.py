import json
import os

import datasets

_RUSSIAN_SUPER_GLUE_CITATION = """\
@article{shavrina2020russiansuperglue,
                  title={RussianSuperGLUE: A Russian Language Understanding Evaluation Benchmark},
                  author={Shavrina, Tatiana and Fenogenova, Alena and Emelyanov, Anton and Shevelev, Denis and Artemova,
                  Ekaterina and Malykh, Valentin and Mikhailov, Vladislav and Tikhonova, Maria and Chertok, Andrey and
                  Evlampiev, Andrey},
                  journal={arXiv preprint arXiv:2010.15925},
                  year={2020}
                  }
"""

_RUSSIAN_SUPER_GLUE_DESCRIPTION = """\
Recent advances in the field of universal language models and transformers require the development of a methodology for
their broad diagnostics and testing for general intellectual skills - detection of natural language inference,
commonsense reasoning, ability to perform simple logical operations regardless of text subject or lexicon. For the first
time, a benchmark of nine tasks, collected and organized analogically to the SuperGLUE methodology, was developed from
scratch for the Russian language. We provide baselines, human level evaluation, an open-source framework for evaluating
models and an overall leaderboard of transformer models for the Russian language.
"""

_HOMEPAGE = "https://russiansuperglue.com/"

_LICENSE = "MIT License"

_LIDIRUS_DESCRIPTION = """"\
Linguistic Diagnostic for Russian
LiDiRus is a diagnostic dataset that covers a large volume of linguistic phenomena, while allowing you to evaluate
information systems on a simple test of textual entailment recognition. See more details diagnostics.
"""

_RCB_DESCRIPTION = """\
Russian Commitment Bank
The Russian Commitment Bank is a corpus of naturally occurring discourses whose final sentence contains
a clause-embedding predicate under an entailment canceling operator (question, modal, negation, antecedent
of conditional).
"""

_PARUS_DESCRIPTION = """\
Choice of Plausible Alternatives for Russian language
PARus
"""

_MUSERC_DESCRIPTION = """\
Russian Multi-Sentence Reading Comprehension
MuSeRC
"""

_TERRA_DESCRIPTION = """\
Textual Entailment Recognition for Russian
TERRa
"""

_RUSSE_DESCRIPTION = """\
Russian Words in Context (based on RUSSE)
RUSSE
"""

_RWSD_DESCRIPTION = """\
The Winograd Schema Challenge (Russian)
RWSD
"""

_DANETQA_DESCRIPTION = """\
Yes/no Question Answering Dataset for the Russian
DaNetQA
"""

_RUCOS_DESCRIPTION = """\
Russian Reading Comprehension with Commonsense Reasoning
RuCoS
"""


class RussianSuperGlueConfig(datasets.BuilderConfig):
    """BuilderConfig for Russian SuperGLUE."""

    VERSION = datasets.Version("0.0.1")

    def __init__(self, features, data_url, citation, url, label_classes=("False", "True"), **kwargs):
        """BuilderConfig for Russian SuperGLUE.

        Args:
          features: `list[string]`, list of the features that will appear in the
            feature dict. Should not include "label".
          data_url: `string`, url to download the zip file from.
          citation: `string`, citation for the data set.
          url: `string`, url for information about the data set.
          label_classes: `list[string]`, the list of classes for the label if the
            label is present as a string. Non-string labels will be cast to either
            'False' or 'True'.
          **kwargs: keyword arguments forwarded to super.
        """
        # 0.0.1: Initial version.
        super(RussianSuperGlueConfig, self).__init__(version=self.VERSION, **kwargs)
        self.features = features
        self.label_classes = label_classes
        self.data_url = data_url
        self.citation = citation
        self.url = url


class RussianSuperGlue(datasets.GeneratorBasedBuilder):

    BUILDER_CONFIGS = [
        RussianSuperGlueConfig(
            name="lidirus",
            description=_LIDIRUS_DESCRIPTION,
            features=[
                "sentence1", "sentence2", "knowledge", "lexical-semantics", "logic", "predicate-argument-structure"
            ],
            label_classes=["entailment", "not_entailment"],
            data_url="https://russiansuperglue.com/tasks/download/LiDiRus",
            citation="",
            url="https://russiansuperglue.com/tasks/task_info/LiDiRus",
        ),
        RussianSuperGlueConfig(
            name="rcb",
            description=_RCB_DESCRIPTION,
            features=["premise", "hypothesis", "verb", "negation"],
            label_classes=["entailment", "contradiction", "neutral"],
            data_url="https://russiansuperglue.com/tasks/download/RCB",
            citation=_RUSSIAN_SUPER_GLUE_CITATION,
            url="https://russiansuperglue.com/tasks/task_info/RCB",
        ),
        RussianSuperGlueConfig(
            name="parus",
            description=_PARUS_DESCRIPTION,
            label_classes=["choice1", "choice2"],
            features=["premise", "choice1", "choice2", "question"],
            data_url="https://russiansuperglue.com/tasks/download/PARus",
            citation=_RUSSIAN_SUPER_GLUE_CITATION,
            url="https://russiansuperglue.com/tasks/task_info/PARus",
        ),
        RussianSuperGlueConfig(
            name="terra",
            description=_TERRA_DESCRIPTION,
            features=["premise", "hypothesis"],
            label_classes=["entailment", "not_entailment"],
            data_url="https://russiansuperglue.com/tasks/download/TERRa",
            citation="",
            url="https://russiansuperglue.com/tasks/task_info/TERRa",
        ),
    ]

    def _info(self):
        features = {feature: datasets.Value("string") for feature in self.config.features}

        features["label"] = datasets.features.ClassLabel(names=self.config.label_classes)
        features["idx"] = datasets.Value("int32")

        return datasets.DatasetInfo(
            description=_RUSSIAN_SUPER_GLUE_DESCRIPTION + self.config.description,
            features=datasets.Features(features),
            homepage=self.config.url,
            citation=self.config.citation + "\n" + _RUSSIAN_SUPER_GLUE_CITATION,
        )

    def _split_generators(self, dl_manager: datasets.DownloadManager):
        dl_dir = dl_manager.download_and_extract(self.config.data_url) or ""
        task_name = _get_task_name_from_data_url(self.config.data_url)
        dl_dir = os.path.join(dl_dir, task_name)
        if self.config.name == "lidirus":
            return [
                datasets.SplitGenerator(
                    name=datasets.Split.TEST,
                    gen_kwargs={
                        "data_file": os.path.join(dl_dir, f"{task_name}.jsonl"),
                        "split": datasets.Split.TEST,
                    },
                ),
            ]
        else:
            return [
                datasets.SplitGenerator(
                    name=datasets.Split.TRAIN,
                    gen_kwargs={
                        "data_file": os.path.join(dl_dir, "train.jsonl"),
                        "split": datasets.Split.TRAIN,
                    },
                ),
                datasets.SplitGenerator(
                    name=datasets.Split.VALIDATION,
                    gen_kwargs={
                        "data_file": os.path.join(dl_dir, "val.jsonl"),
                        "split": datasets.Split.VALIDATION,
                    },
                ),
                datasets.SplitGenerator(
                    name=datasets.Split.TEST,
                    gen_kwargs={
                        "data_file": os.path.join(dl_dir, "test.jsonl"),
                        "split": datasets.Split.TEST,
                    },
                ),
            ]

    def _generate_examples(self, data_file: str, split: datasets.Split):
        with open(data_file, encoding="utf-8") as file:
            for line in file:
                row = json.loads(line)

                if self.config.name in ("lidirus", "rcb"):
                    # features may be missing
                    example = {feature: row.get(feature, "") for feature in self.config.features}
                else:
                    example = {feature: row[feature] for feature in self.config.features}

                example["idx"] = row["idx"]

                if "label" in row:
                    if self.config.name == "parus":
                        example["label"] = "choice2" if row["label"] else "choice1"
                    else:
                        example["label"] = _cast_label(row["label"])
                else:
                    assert split == datasets.Split.TEST, row
                    example["label"] = -1

                yield example["idx"], example


def _get_task_name_from_data_url(data_url: str) -> str:
    return data_url.split("/")[-1]


def _cast_label(label):
    """Converts the label into the appropriate string version."""
    if isinstance(label, str):
        return label
    elif isinstance(label, bool):
        return "True" if label else "False"
    elif isinstance(label, int):
        assert label in (0, 1)
        return str(label)
    else:
        raise ValueError("Invalid label format.")
