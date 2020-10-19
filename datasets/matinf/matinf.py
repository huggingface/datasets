from __future__ import absolute_import, division, print_function

import csv
import os

import six

import datasets


_CITATION = """\
@inproceedings{xu-etal-2020-matinf,
    title = "{MATINF}: A Jointly Labeled Large-Scale Dataset for Classification, Question Answering and Summarization",
    author = "Xu, Canwen  and
      Pei, Jiaxin  and
      Wu, Hongtao  and
      Liu, Yiyu  and
      Li, Chenliang",
    booktitle = "Proceedings of the 58th Annual Meeting of the Association for Computational Linguistics",
    month = jul,
    year = "2020",
    address = "Online",
    publisher = "Association for Computational Linguistics",
    url = "https://www.aclweb.org/anthology/2020.acl-main.330",
    pages = "3586--3596",
}

"""

_DESCRIPTION = """\
MATINF is the first jointly labeled large-scale dataset for classification, question answering and summarization.
 MATINF contains 1.07 million question-answer pairs with human-labeled categories and user-generated question
 descriptions. Based on such rich information, MATINF is applicable for three major NLP tasks, including classification,
 question answering, and summarization. We benchmark existing methods and a novel multi-task baseline over MATINF to
 inspire further research. Our comprehensive comparison and experiments over MATINF and other datasets demonstrate the
 merits held by MATINF.
"""


class MatinfConfig(datasets.BuilderConfig):
    """BuilderConfig for MATINF."""

    def __init__(
        self,
        text_features,
        label_column,
        label_classes=None,
        **kwargs,
    ):
        """BuilderConfig for MATINF.

        Args:
          text_features: `dict[string, string]`, map from the name of the feature
            dict for each text field to the name of the column in the tsv file
          label_column: `string`, name of the column in the tsv file corresponding
            to the label
          label_classes: `list[string]`, the list of classes if the label is
            categorical. If not provided, then the label will be of type
            `datasets.Value('float32')`.
          **kwargs: keyword arguments forwarded to super.
        """
        super(MatinfConfig, self).__init__(version=datasets.Version("1.0.0"), **kwargs)
        self.text_features = text_features
        self.label_column = label_column
        self.label_classes = label_classes


class Matinf(datasets.GeneratorBasedBuilder):
    VERSION = datasets.Version("1.0.0")

    BUILDER_CONFIGS = [
        MatinfConfig(
            name="age_classification",
            text_features=["question", "description"],
            label_column="class",
            label_classes=["0-1岁", "1-2岁", "2-3岁"],
        ),
        MatinfConfig(
            name="topic_classification",
            text_features=["question", "description"],
            label_column="class",
            label_classes=[
                "产褥期保健",
                "儿童过敏",
                "动作发育",
                "婴幼保健",
                "婴幼心理",
                "婴幼早教",
                "婴幼期喂养",
                "婴幼营养",
                "孕期保健",
                "家庭教育",
                "幼儿园",
                "未准父母",
                "流产和不孕",
                "疫苗接种",
                "皮肤护理",
                "宝宝上火",
                "腹泻",
                "婴幼常见病",
            ],
        ),
        MatinfConfig(
            name="summarization",
            text_features=["description", "question"],
            label_column=None,
        ),
        MatinfConfig(
            name="qa",
            text_features=["question", "answer"],
            label_column=None,
        ),
    ]

    @property
    def manual_download_instructions(self):
        return (
            "To use MATINF you have to download it manually. Please fill this google form ("
            "https://forms.gle/nkH4LVE4iNQeDzsc9). You will receive a download link and a password once you "
            "complete the form. Please extract all files in one folder and load the dataset with: "
            "`datasets.load_dataset('matinf', data_dir='path/to/folder/folder_name')`"
        )

    def _info(self):
        features = {text_feature: datasets.Value("string") for text_feature in self.config.text_features}
        if self.config.label_classes:
            features["label"] = datasets.features.ClassLabel(names=self.config.label_classes)
        features["id"] = datasets.Value("int32")
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=datasets.Features(features),
            homepage="https://github.com/WHUIR/MATINF",
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        """Returns SplitGenerators."""
        data_dir = os.path.abspath(os.path.expanduser(dl_manager.manual_dir))

        if not os.path.exists(data_dir):
            raise FileNotFoundError(
                "{} does not exist. Make sure you insert a manual dir via `datasets.load_dataset('matinf', data_dir=...)` that includes files unzipped from the MATINF zip. Manual download instructions: {}".format(
                    data_dir, self.manual_download_instructions
                )
            )
        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                gen_kwargs={"filepath": os.path.join(data_dir, "train.csv")},
            ),
            datasets.SplitGenerator(
                name=datasets.Split.TEST,
                gen_kwargs={"filepath": os.path.join(data_dir, "test.csv")},
            ),
            datasets.SplitGenerator(
                name=datasets.Split.VALIDATION,
                gen_kwargs={"filepath": os.path.join(data_dir, "dev.csv")},
            ),
        ]

    def _generate_examples(self, filepath):
        """Yields examples."""
        label_classes = self.config.label_classes

        with open(filepath, encoding="utf8") as f:
            reader = csv.DictReader(f)

            for n, row in enumerate(reader):
                example = {feat: row[feat] for feat in self.config.text_features}
                example["id"] = row["id"]

                if self.config.label_column:
                    label = row[self.config.label_column]
                    if label_classes and label not in label_classes:
                        continue  # Split age/topic classification
                    example["label"] = label

                # Filter out corrupted rows.
                for value in six.itervalues(example):
                    if value is None:
                        break
                else:
                    yield example["id"], example
