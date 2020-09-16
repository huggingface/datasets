"""TODO(mlqa): Add a description here."""

from __future__ import absolute_import, division, print_function

import json
import os

import datasets


# TODO(mlqa): BibTeX citation
_CITATION = """\
@article{lewis2019mlqa,
  title={MLQA: Evaluating Cross-lingual Extractive Question Answering},
  author={Lewis, Patrick and Oguz, Barlas and Rinott, Ruty and Riedel, Sebastian and Schwenk, Holger},
  journal={arXiv preprint arXiv:1910.07475},
  year={2019}
}
"""

# TODO(mlqa):
_DESCRIPTION = """\
    MLQA (MultiLingual Question Answering) is a benchmark dataset for evaluating cross-lingual question answering performance.
    MLQA consists of over 5K extractive QA instances (12K in English) in SQuAD format in seven languages - English, Arabic,
    German, Spanish, Hindi, Vietnamese and Simplified Chinese. MLQA is highly parallel, with QA instances parallel between
    4 different languages on average.
"""
_URL = "https://dl.fbaipublicfiles.com/MLQA/"
_DEV_TEST_URL = "MLQA_V1.zip"
_TRANSLATE_TEST_URL = "mlqa-translate-test.tar.gz"
_TRANSLATE_TRAIN_URL = "mlqa-translate-train.tar.gz"
_LANG = ["ar", "de", "vi", "zh", "en", "es", "hi"]
_TRANSLATE_LANG = ["ar", "de", "vi", "zh", "es", "hi"]


class MlqaConfig(datasets.BuilderConfig):
    def __init__(self, data_url, **kwargs):
        """BuilderConfig for MLQA

        Args:
          data_url: `string`, url to the dataset
          **kwargs: keyword arguments forwarded to super.
        """
        super(MlqaConfig, self).__init__(
            version=datasets.Version(
                "1.0.0",
            ),
            **kwargs,
        )
        self.data_url = data_url


class Mlqa(datasets.GeneratorBasedBuilder):
    """TODO(mlqa): Short description of my dataset."""

    # TODO(mlqa): Set up version.
    VERSION = datasets.Version("1.0.0")
    BUILDER_CONFIGS = (
        [
            MlqaConfig(
                name="mlqa-translate-train." + lang,
                data_url=_URL + _TRANSLATE_TRAIN_URL,
                description="Machine-translated data for Translate-train (SQuAD Train and Dev sets machine-translated into "
                "Arabic, German, Hindi, Vietnamese, Simplified Chinese and Spanish)",
            )
            for lang in _LANG
            if lang != "en"
        ]
        + [
            MlqaConfig(
                name="mlqa-translate-test." + lang,
                data_url=_URL + _TRANSLATE_TEST_URL,
                description="Machine-translated data for Translate-Test (MLQA-test set machine-translated into English) ",
            )
            for lang in _LANG
            if lang != "en"
        ]
        + [
            MlqaConfig(
                name="mlqa." + lang1 + "." + lang2,
                data_url=_URL + _DEV_TEST_URL,
                description="development and test splits",
            )
            for lang1 in _LANG
            for lang2 in _LANG
        ]
    )

    def _info(self):
        # TODO(mlqa): Specifies the datasets.DatasetInfo object
        return datasets.DatasetInfo(
            # This is the description that will appear on the datasets page.
            description=_DESCRIPTION,
            # datasets.features.FeatureConnectors
            features=datasets.Features(
                {
                    "context": datasets.Value("string"),
                    "question": datasets.Value("string"),
                    "answers": datasets.features.Sequence(
                        {"answer_start": datasets.Value("int32"), "text": datasets.Value("string")}
                    ),
                    "id": datasets.Value("string"),
                    # These are the features of your dataset like images, labels ...
                }
            ),
            # If there's a common (input, target) tuple from the features,
            # specify them here. They'll be used if as_supervised=True in
            # builder.as_dataset.
            supervised_keys=None,
            # Homepage of the dataset for documentation
            homepage="https://github.com/facebookresearch/MLQA",
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        """Returns SplitGenerators."""
        # TODO(mlqa): Downloads the data and defines the splits
        # dl_manager is a datasets.download.DownloadManager that can be used to
        # download and extract URLs
        if self.config.name.startswith("mlqa-translate-train"):
            dl_file = dl_manager.download_and_extract(self.config.data_url)
            lang = self.config.name.split(".")[-1]
            return [
                datasets.SplitGenerator(
                    name=datasets.Split.TRAIN,
                    # These kwargs will be passed to _generate_examples
                    gen_kwargs={
                        "filepath": os.path.join(
                            os.path.join(dl_file, "mlqa-translate-train"),
                            "{}_squad-translate-train-train-v1.1.json".format(lang),
                        )
                    },
                ),
                datasets.SplitGenerator(
                    name=datasets.Split.VALIDATION,
                    # These kwargs will be passed to _generate_examples
                    gen_kwargs={
                        "filepath": os.path.join(
                            os.path.join(dl_file, "mlqa-translate-train"),
                            "{}_squad-translate-train-dev-v1.1.json".format(lang),
                        )
                    },
                ),
            ]

        else:
            if self.config.name.startswith("mlqa."):
                dl_file = dl_manager.download_and_extract(self.config.data_url)
                name = self.config.name.split(".")
                l1, l2 = name[1:]
                return [
                    datasets.SplitGenerator(
                        name=datasets.Split.TEST,
                        # These kwargs will be passed to _generate_examples
                        gen_kwargs={
                            "filepath": os.path.join(
                                os.path.join(dl_file, "MLQA_V1/test"),
                                "test-context-{}-question-{}.json".format(l1, l2),
                            )
                        },
                    ),
                    datasets.SplitGenerator(
                        name=datasets.Split.VALIDATION,
                        # These kwargs will be passed to _generate_examples
                        gen_kwargs={
                            "filepath": os.path.join(
                                os.path.join(dl_file, "MLQA_V1/dev"), "dev-context-{}-question-{}.json".format(l1, l2)
                            )
                        },
                    ),
                ]
            else:
                if self.config.name.startswith("mlqa-translate-test"):
                    dl_file = dl_manager.download_and_extract(self.config.data_url)
                    lang = self.config.name.split(".")[-1]
                    return [
                        datasets.SplitGenerator(
                            name=datasets.Split.TEST,
                            # These kwargs will be passed to _generate_examples
                            gen_kwargs={
                                "filepath": os.path.join(
                                    os.path.join(dl_file, "mlqa-translate-test"),
                                    "translate-test-context-{}-question-{}.json".format(lang, lang),
                                )
                            },
                        ),
                    ]

    def _generate_examples(self, filepath):
        """Yields examples."""
        # TODO(mlqa): Yields (key, example) tuples from the dataset
        with open(filepath, encoding="utf-8") as f:
            data = json.load(f)
        for examples in data["data"]:
            for example in examples["paragraphs"]:
                context = example["context"]
                for qa in example["qas"]:
                    question = qa["question"]
                    id_ = qa["id"]
                    answers = qa["answers"]
                    answers_start = [answer["answer_start"] for answer in answers]
                    answers_text = [answer["text"] for answer in answers]
                    yield id_, {
                        "context": context,
                        "question": question,
                        "answers": {"answer_start": answers_start, "text": answers_text},
                        "id": id_,
                    }
