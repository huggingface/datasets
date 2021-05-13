"""Ethos  dataset"""


import pandas as pd

import datasets


logger = datasets.logging.get_logger(__name__)


_CITATION = """
@misc{mollas2020ethos,
      title={ETHOS: an Online Hate Speech Detection Dataset},
      author={Ioannis Mollas and Zoe Chrysopoulou and Stamatis Karlos and Grigorios Tsoumakas},
      year={2020},
      eprint={2006.08328},
      archivePrefix={arXiv},
      primaryClass={cs.CL}
}
 """

_DESCRIPTION = """

ETHOS: onlinE haTe speecH detectiOn dataSet. This repository contains a dataset for hate speech
detection on social media platforms, called Ethos. There are two variations of the dataset:

Ethos_Dataset_Binary: contains 998 comments in the dataset alongside with a label
about hate speech presence or absence. 565 of them do not contain hate speech,
while the rest of them, 433, contain.

Ethos_Dataset_Multi_Label: which contains 8 labels for the 433 comments with hate speech content.
These labels are violence (if it incites (1) or not (0) violence), directed_vs_general (if it is
directed to a person (1) or a group (0)), and 6 labels about the category of hate speech like,
gender, race, national_origin, disability, religion and sexual_orientation.
"""

_URL = "https://github.com/intelligence-csd-auth-gr/Ethos-Hate-Speech-Dataset"


class EthosConfig(datasets.BuilderConfig):
    """BuilderConfig for Ethos."""

    def __init__(self, variation="binary", **kwargs):
        """Constructs an EthosDataset.

        Args:
        variation: can be binary or multilabel
        **kwargs: keyword arguments forwarded to super.
        """
        if variation.lower() == "binary":
            self.variation = "binary"
        elif variation.lower() == "multilabel":
            self.variation = "multilabel"
        else:
            logger.warning("Wrong variation. Could be either 'binary' or 'multilabel', using 'binary' instead.")
            self.variation = "binary"
        super(EthosConfig, self).__init__(**kwargs)


class Ethos(datasets.GeneratorBasedBuilder):
    BUILDER_CONFIG_CLASS = EthosConfig

    BUILDER_CONFIGS = [
        EthosConfig(
            name="binary",
            version=datasets.Version("1.0.0", ""),
            description="Ethos Binary",
            variation="binary",
        ),
        EthosConfig(
            name="multilabel",
            version=datasets.Version("1.0.0", ""),
            description="Ethos Multi Label",
            variation="multilabel",
        ),
    ]

    def _info(self):
        if self.config.variation == "binary":
            f = datasets.Features(
                {
                    "text": datasets.Value("string"),
                    "label": datasets.features.ClassLabel(names=["no_hate_speech", "hate_speech"]),
                }
            )
        else:
            f = datasets.Features(
                {
                    "text": datasets.Value("string"),
                    "violence": datasets.ClassLabel(names=["not_violent", "violent"]),
                    "directed_vs_generalized": datasets.ClassLabel(names=["generalied", "directed"]),
                    "gender": datasets.ClassLabel(names=["false", "true"]),
                    "race": datasets.ClassLabel(names=["false", "true"]),
                    "national_origin": datasets.ClassLabel(names=["false", "true"]),
                    "disability": datasets.ClassLabel(names=["false", "true"]),
                    "religion": datasets.ClassLabel(names=["false", "true"]),
                    "sexual_orientation": datasets.ClassLabel(names=["false", "true"]),
                }
            )
        return datasets.DatasetInfo(
            features=f,
            supervised_keys=None,
            homepage="https://github.com/intelligence-csd-auth-gr/Ethos-Hate-Speech-Dataset/tree/masterethos/ethos_data",
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        if self.config.variation == "binary":
            url = {
                "train": "https://raw.githubusercontent.com/intelligence-csd-auth-gr/Ethos-Hate-Speech-Dataset"
                "/master/ethos/ethos_data/Ethos_Dataset_Binary.csv"
            }
        else:
            url = {
                "train": "https://raw.githubusercontent.com/intelligence-csd-auth-gr/Ethos-Hate-Speech-Dataset"
                "/master/ethos/ethos_data/Ethos_Dataset_Multi_Label.csv"
            }
        downloaded_files = dl_manager.download_and_extract(url)

        return [datasets.SplitGenerator(name=datasets.Split.TRAIN, gen_kwargs={"filepath": downloaded_files["train"]})]

    def _generate_examples(self, filepath):
        """Yields examples."""

        data = pd.read_csv(filepath, delimiter=";")
        if self.config.variation == "binary":

            x = data["comment"].values
            y = [1 if i >= 0.5 else 0 for i in data["isHate"].values]
            class_names = ["no_hate_speech", "hate_speech"]
            for i in range(len(x)):
                _id = i
                yield _id, {"text": x[i], "label": class_names[y[i]]}
        else:
            x = data["comment"].values
            y_temp = data.loc[:, data.columns != "comment"].values
            y = []
            for yt in y_temp:
                yi = []
                for i in yt:
                    if i >= 0.5:
                        yi.append(int(1))
                    else:
                        yi.append(int(0))
                y.append(yi)
            for i in range(len(x)):
                _id = i
                yield _id, {
                    "text": x[i],
                    "violence": y[i][0],
                    "directed_vs_generalized": y[i][1],
                    "gender": y[i][2],
                    "race": y[i][3],
                    "national_origin": y[i][4],
                    "disability": y[i][5],
                    "religion": y[i][6],
                    "sexual_orientation": y[i][7],
                }
