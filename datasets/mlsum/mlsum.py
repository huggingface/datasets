from __future__ import absolute_import, division, print_function

import json
import os

import nlp


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
_URL = "https://gitlab.lip6.fr/scialom/mlsum_data/-/raw/master/MLSUM/"
_LANG = ["de", "es", "fr", "ru", "tu"]


class MlsumConfig(nlp.BuilderConfig):
    def __init__(self, data_url, **kwargs):
        """BuilderConfig for MLQA

        Args:
          data_url: `string`, url to the dataset
          **kwargs: keyword arguments forwarded to super.
        """
        super(MlsumConfig, self).__init__(version=nlp.Version("1.0.0",), **kwargs)
        self.data_url = data_url


class Mlsum(nlp.GeneratorBasedBuilder):

    # TODO(mlqa): Set up version.
    VERSION = nlp.Version("1.0.0")
    BUILDER_CONFIGS = (
        [
            MlsumConfig(
                name=lang,
                data_url=_URL,
                description="",
            )
            for lang in _LANG
        ]
    )

    def _info(self):
        # TODO(mlqa): Specifies the nlp.DatasetInfo object
        return nlp.DatasetInfo(
            # This is the description that will appear on the datasets page.
            description=_DESCRIPTION,
            # nlp.features.FeatureConnectors

            features=nlp.Features(
                {
                    "text": nlp.Value("string"),
                    "summary": nlp.Value("string"),
                    "topic": nlp.Value("string"),
                    "url": nlp.Value("string"),
                    "title": nlp.Value("string"),
                    "date":nlp.Value("string")
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
        # TODO(mlqa): Downloads the data and defines the splits
        # dl_manager is a nlp.download.DownloadManager that can be used to
        # download and extract URLs
        
        lang = self.config.name
        urls_to_download = {
            "test": os.path.join(_URL, lang+"_test.zip"),
            "train": os.path.join(_URL, lang+"_train.zip"),
            "validation": os.path.join(_URL, lang+"_val.zip")
        }
        downloaded_files = dl_manager.download_and_extract(urls_to_download)

        return [
            nlp.SplitGenerator(
                name=nlp.Split.TRAIN,
                    # These kwargs will be passed to _generate_examples
                gen_kwargs={
                    "filepath": os.path.join(downloaded_files["train"], lang+'_train.jsonl'),
                    "lang": lang,
                },
            ),
            nlp.SplitGenerator(
                name=nlp.Split.VALIDATION,
                    # These kwargs will be passed to _generate_examples
                gen_kwargs={
                    "filepath": os.path.join(downloaded_files["validation"], lang+'_val.jsonl'),
                    "lang": lang,
                },
            ),
            nlp.SplitGenerator(
                name=nlp.Split.TEST,
                    # These kwargs will be passed to _generate_examples
                gen_kwargs={
                    "filepath": os.path.join(downloaded_files["test"], lang+'_test.jsonl'),
                    "lang": lang,
                },
            )
        ]

    def _generate_examples(self, filepath, lang):
        """Yields examples."""
        # TODO(mlqa): Yields (key, example) tuples from the dataset
        with open(filepath) as f:
            i = 0
            for line in f: 
                data = json.loads(line)
                i +=1
                yield i, {
                    "text": data["text"],
                    "summary": data["summary"],
                    "topic": data["topic"],
                    "url":data['url'],
                    "title":data["title"],
                    "date":data["date"]
                }
