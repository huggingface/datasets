import json

import datasets


_CITATION = """\
@article{scialom2020mlsum,
  title={MLSUM: The Multilingual Summarization Corpus},
  author={Scialom, Thomas and Dray, Paul-Alexis and Lamprier, Sylvain and Piwowarski, Benjamin and Staiano, Jacopo},
  journal={arXiv preprint arXiv:2004.14900},
  year={2020}
}
"""

_DESCRIPTION = """\
We present MLSUM, the first large-scale MultiLingual SUMmarization dataset.
Obtained from online newspapers, it contains 1.5M+ article/summary pairs in five different languages -- namely, French, German, Spanish, Russian, Turkish.
Together with English newspapers from the popular CNN/Daily mail dataset, the collected data form a large scale multilingual dataset which can enable new research directions for the text summarization community.
We report cross-lingual comparative analyses based on state-of-the-art systems.
These highlight existing biases which motivate the use of a multi-lingual dataset.
"""

_URL = "https://gitlab.lip6.fr/scialom/mlsum_data/-/raw/master/MLSUM"
_LANG = ["de", "es", "fr", "ru", "tu"]


class Mlsum(datasets.GeneratorBasedBuilder):

    BUILDER_CONFIGS = [
        datasets.BuilderConfig(
            name=lang,
            version=datasets.Version("1.0.0"),
            description="",
        )
        for lang in _LANG
    ]

    def _info(self):
        return datasets.DatasetInfo(
            # This is the description that will appear on the datasets page.
            description=_DESCRIPTION,
            # datasets.features.FeatureConnectors
            features=datasets.Features(
                {
                    "text": datasets.Value("string"),
                    "summary": datasets.Value("string"),
                    "topic": datasets.Value("string"),
                    "url": datasets.Value("string"),
                    "title": datasets.Value("string"),
                    "date": datasets.Value("string")
                    # These are the features of your dataset like images, labels ...
                }
            ),
            # If there's a common (input, target) tuple from the features,
            # specify them here. They'll be used if as_supervised=True in
            # builder.as_dataset.
            supervised_keys=None,
            # Homepage of the dataset for documentation
            homepage="",
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        """Returns SplitGenerators."""
        # dl_manager is a datasets.download.DownloadManager that can be used to
        # download and extract URLs

        lang = self.config.name
        urls_to_download = {
            "train": f"{_URL}/{lang}_train.jsonl",
            "validation": f"{_URL}/{lang}_val.jsonl",
            "test": f"{_URL}/{lang}_test.jsonl",
        }
        downloaded_files = dl_manager.download(urls_to_download)

        return [
            datasets.SplitGenerator(
                name=split,
                gen_kwargs={
                    "filepath": downloaded_files[split],
                },
            )
            for split in [datasets.Split.TRAIN, datasets.Split.VALIDATION, datasets.Split.TEST]
        ]

    def _generate_examples(self, filepath):
        """Yields examples."""
        with open(filepath, encoding="utf-8") as f:
            for id_, line in enumerate(f):
                data = json.loads(line)
                yield id_, {
                    "text": data["text"],
                    "summary": data["summary"],
                    "topic": data["topic"],
                    "url": data["url"],
                    "title": data["title"],
                    "date": data["date"],
                }
