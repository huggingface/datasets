import json
import os

import datasets


_CITATION = """\
@dataset{kobkrit_viriyayudhakorn_2021_4539916,
  author       = {Kobkrit Viriyayudhakorn and
                  Charin Polpanumas},
  title        = {iapp_wiki_qa_squad},
  month        = feb,
  year         = 2021,
  publisher    = {Zenodo},
  version      = 1,
  doi          = {10.5281/zenodo.4539916},
  url          = {https://doi.org/10.5281/zenodo.4539916}
}
"""

_DESCRIPTION = """\
`iapp_wiki_qa_squad` is an extractive question answering dataset from Thai Wikipedia articles.
It is adapted from [the original iapp-wiki-qa-dataset](https://github.com/iapp-technology/iapp-wiki-qa-dataset)
to [SQuAD](https://rajpurkar.github.io/SQuAD-explorer/) format, resulting in
5761/742/739 questions from 1529/191/192 articles.
"""


class IappWikiQaSquadConfig(datasets.BuilderConfig):
    def __init__(self, **kwargs):
        """BuilderConfig

        Args:
          **kwargs: keyword arguments forwarded to super.
        """
        super(IappWikiQaSquadConfig, self).__init__(**kwargs)


class IappWikiQaSquad(datasets.GeneratorBasedBuilder):
    _DOWNLOAD_URL = "https://github.com/iapp-technology/iapp-wiki-qa-dataset/raw/main/squad_format/data.zip"
    _TRAIN_FILE = "train.jsonl"
    _VALID_FILE = "valid.jsonl"
    _TEST_FILE = "test.jsonl"

    BUILDER_CONFIGS = [
        IappWikiQaSquadConfig(
            name="iapp_wiki_qa_squad",
            version=datasets.Version("1.0.0"),
            description=_DESCRIPTION,
        ),
    ]

    def _info(self):
        return datasets.DatasetInfo(
            # This is the description that will appear on the datasets page.
            description=_DESCRIPTION,
            # datasets.features.FeatureConnectors
            features=datasets.Features(
                {
                    "question_id": datasets.Value("string"),
                    "article_id": datasets.Value("string"),
                    "title": datasets.Value("string"),
                    "context": datasets.Value("string"),
                    "question": datasets.Value("string"),
                    "answers": datasets.features.Sequence(
                        {
                            "text": datasets.Value("string"),
                            "answer_start": datasets.Value("int32"),
                            "answer_end": datasets.Value("int32"),
                        }
                    ),
                }
            ),
            # If there's a common (input, target) tuple from the features,
            # specify them here. They'll be used if as_supervised=True in
            # builder.as_dataset.
            supervised_keys=None,
            # Homepage of the dataset for documentation
            homepage="https://github.com/iapp-technology/iapp-wiki-qa-dataset/",
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        arch_path = dl_manager.download_and_extract(self._DOWNLOAD_URL)
        data_dir = os.path.join(arch_path, "data")
        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                gen_kwargs={"filepath": os.path.join(data_dir, self._TRAIN_FILE)},
            ),
            datasets.SplitGenerator(
                name=datasets.Split.VALIDATION,
                gen_kwargs={"filepath": os.path.join(data_dir, self._VALID_FILE)},
            ),
            datasets.SplitGenerator(
                name=datasets.Split.TEST,
                gen_kwargs={"filepath": os.path.join(data_dir, self._TEST_FILE)},
            ),
        ]

    def _generate_examples(self, filepath):
        """Yields examples."""
        with open(filepath, encoding="utf-8") as f:
            for id_, row in enumerate(f):
                data = json.loads(row)

                yield id_, {
                    "question_id": data["question_id"],
                    "article_id": data["article_id"],
                    "title": data["title"],
                    "context": data["context"],
                    "question": data["question"],
                    "answers": {
                        "text": data["answers"]["text"],
                        "answer_start": data["answers"]["answer_start"],
                        "answer_end": data["answers"]["answer_end"],
                    },
                }
