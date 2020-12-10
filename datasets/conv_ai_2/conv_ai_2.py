from __future__ import absolute_import, division, print_function

import json

import datasets


_DESCRIPTION = """\
ConvAI is a dataset of human-to-bot conversations labelled for quality. \
This data can be used to train a metric for evaluating dialogue systems. \
Moreover, it can be used in the development of chatbots themselves: it contains the information \
on the quality of utterances and entire dialogues, that can guide a dialogue system in search of better answers.
"""

_URL = "https://github.com/DeepPavlov/convai/raw/master/2018/data/summer_wild_evaluation_dialogs.json"


class ConvAi_2(datasets.GeneratorBasedBuilder):
    """ConvAI: A Dataset of Topic-Oriented Human-to-Chatbot Dialogues"""

    VERSION = datasets.Version("1.0.0")
    BUILDER_CONFIGS = [
        datasets.BuilderConfig(
            name="conv_ai_2",
            version=datasets.Version("1.0.0"),
            description="Full training set",
        ),
    ]

    def _info(self):
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=datasets.Features(
                {
                    "id": datasets.Value("string"),
                    "dialog_id": datasets.Value("string"),
                    "dialog": [
                        {
                            "id": datasets.Value("int32"),
                            "sender": datasets.Value("string"),
                            "text": datasets.Value("string"),
                            "sender_class": datasets.Value("string"),
                        }
                    ],
                    "bot_profile": datasets.Sequence([datasets.Value("string")]),
                    "user_profile": datasets.Sequence([datasets.Value("string")]),
                    "eval_score": datasets.Value("int32"),
                    "profile_match": datasets.Value("int32"),
                }
            ),
            supervised_keys=None,
            homepage="https://github.com/DeepPavlov/convai/tree/master/2018",
        )

    def _split_generators(self, dl_manager):
        downloaded_file = dl_manager.download(_URL)

        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                gen_kwargs={"filepath": downloaded_file},
            ),
        ]

    def _generate_examples(self, filepath):
        with open(filepath, encoding="utf-8") as f:
            examples = json.load(f)
            for example in examples:
                example["id"] = example["dialog_id"]
                if example["eval_score"] is None:
                    example["eval_score"] = -1
                if not example["profile_match"]:
                    example["profile_match"] = -1
                yield example["id"], example
