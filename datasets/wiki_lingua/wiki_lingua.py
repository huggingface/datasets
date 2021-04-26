# coding=utf-8
# Copyright 2020 The HuggingFace Datasets Authors and the current dataset script contributor.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""TODO: Add a description here."""


import pickle

import datasets


# Find for instance the citation on arxiv or on the dataset repo/website
_CITATION = """\
@article{ladhak-wiki-2020,
  title   = {WikiLingua: A New Benchmark Dataset for Multilingual Abstractive Summarization},
  authors = {Faisal Ladhak, Esin Durmus, Claire Cardie and Kathleen McKeown},
  journal = {arXiv preprint arXiv:2010.03093},
  year    = {2020},
  url     = {https://arxiv.org/abs/2010.03093}
}
"""

_DESCRIPTION = """\
WikiLingua is a large-scale multilingual dataset for the evaluation of
crosslingual abstractive summarization systems. The dataset includes ~770k
article and summary pairs in 18 languages from WikiHow. The gold-standard
article-summary alignments across languages was done by aligning the images
that are used to describe each how-to step in an article.
"""

_HOMEPAGE = "https://github.com/esdurmus/Wikilingua"

_LICENSE = "CC BY-NC-SA 3.0"

# Download links
_URLs = {
    "arabic": "https://drive.google.com/uc?export=download&id=1__EjA6oZsgXQpggPm-h54jZu3kP6Y6zu",
    "chinese": "https://drive.google.com/uc?export=download&id=1TuWH7uwu6V90QWmZn25qhou1rm97Egmn",
    "czech": "https://drive.google.com/uc?export=download&id=1GcUN6mytEcOMBBOvjJOQzBmEkc-LdgQg",
    "dutch": "https://drive.google.com/uc?export=download&id=1-w-0uqaC6hnRn1F_3XqJEvi09zlcTIhX",
    "english": "https://drive.google.com/uc?export=download&id=11wMGqNVSwwk6zUnDaJEgm3qT71kAHeff",
    "french": "https://drive.google.com/uc?export=download&id=1Uit4Og1pk-br_0UJIO5sdhApyhTuHzqo",
    "german": "https://drive.google.com/uc?export=download&id=1meSNZHxd_0TZLKCRCYGN-Ke3IA5c1qOE",
    "hindi": "https://drive.google.com/uc?export=download&id=1ZyFGufe4puX3vjGPbp4xg9Hca3Gwq22g",
    "indonesian": "https://drive.google.com/uc?export=download&id=1PGa8j1_IqxiGTc3SU6NMB38sAzxCPS34",
    "italian": "https://drive.google.com/uc?export=download&id=1okwGJiOZmTpNRNgJLCnjFF4Q0H1z4l6_",
    "japanese": "https://drive.google.com/uc?export=download&id=1Z2ty5hU0tIGRZRDlFQZLO7b5vijRfvo0",
    "korean": "https://drive.google.com/uc?export=download&id=1cqu_YAgvlyVSzzjcUyP1Cz7q0k8Pw7vN",
    "portuguese": "https://drive.google.com/uc?export=download&id=1GTHUJxxmjLmG2lnF9dwRgIDRFZaOY3-F",
    "russian": "https://drive.google.com/uc?export=download&id=1fUR3MqJ8jTMka6owA0S-Fe6aHmiophc_",
    "spanish": "https://drive.google.com/uc?export=download&id=17FGi8KI9N9SuGe7elM8qU8_3fx4sfgTr",
    "thai": "https://drive.google.com/uc?export=download&id=1QsV8C5EPJrQl37mwva_5-IJOrCaOi2tH",
    "turkish": "https://drive.google.com/uc?export=download&id=1M1M5yIOyjKWGprc3LUeVVwxgKXxgpqxm",
    "vietnamese": "https://drive.google.com/uc?export=download&id=17FGi8KI9N9SuGe7elM8qU8_3fx4sfgTr",
}


class WikiLingua(datasets.GeneratorBasedBuilder):
    """TODO: Short description of my dataset."""

    VERSION = datasets.Version("1.1.0")

    # This is an example of a dataset with multiple configurations.
    # If you don't want/need to define several sub-sets in your dataset,
    # just remove the BUILDER_CONFIG_CLASS and the BUILDER_CONFIGS attributes.

    # If you need to make complex sub-parts in the datasets with configurable options
    # You can create your own builder configuration class to store attribute, inheriting from datasets.BuilderConfig
    # BUILDER_CONFIG_CLASS = MyBuilderConfig

    # You will  be able to load one or the other configurations in the following list with
    # data = datasets.load_dataset('my_dataset', 'first_domain')
    # data = datasets.load_dataset('my_dataset', 'second_domain')
    BUILDER_CONFIGS = [
        datasets.BuilderConfig(name="arabic", version=VERSION, description="A subset of article-summary in Arabic"),
        datasets.BuilderConfig(name="chinese", version=VERSION, description="A subset of article-summary in Chinese"),
        datasets.BuilderConfig(name="czech", version=VERSION, description="A subset of article-summary in Czech"),
        datasets.BuilderConfig(name="dutch", version=VERSION, description="A subset of article-summary in Dutch"),
        datasets.BuilderConfig(name="english", version=VERSION, description="A subset of article-summary in English"),
        datasets.BuilderConfig(name="french", version=VERSION, description="A subset of article-summary in  French"),
        datasets.BuilderConfig(name="german", version=VERSION, description="A subset of article-summary in German"),
        datasets.BuilderConfig(name="hindi", version=VERSION, description="A subset of article-summary in Hindi"),
        datasets.BuilderConfig(
            name="indonesian", version=VERSION, description="A subset of article-summary in Indonesian"
        ),
        datasets.BuilderConfig(name="italian", version=VERSION, description="A subset of article-summary in Italian"),
        datasets.BuilderConfig(
            name="japanese", version=VERSION, description="A subset of article-summary in Japanese"
        ),
        datasets.BuilderConfig(name="korean", version=VERSION, description="A subset of article-summary in Korean"),
        datasets.BuilderConfig(
            name="portuguese", version=VERSION, description="A subset of article-summary in Portuguese"
        ),
        datasets.BuilderConfig(name="russian", version=VERSION, description="A subset of article-summary in Russian"),
        datasets.BuilderConfig(name="spanish", version=VERSION, description="A subset of article-summary in Spanish"),
        datasets.BuilderConfig(name="thai", version=VERSION, description="A subset of article-summary in Thai"),
        datasets.BuilderConfig(name="turkish", version=VERSION, description="A subset of article-summary in Turkish"),
        datasets.BuilderConfig(
            name="vietnamese", version=VERSION, description="A subset of article-summary in Vietnamese"
        ),
    ]

    DEFAULT_CONFIG_NAME = "english"

    def _info(self):
        if self.config.name == "english":
            features = datasets.Features(
                {
                    "url": datasets.Value("string"),
                    "article": datasets.Sequence(
                        {
                            "section_name": datasets.Value("string"),
                            "document": datasets.Value("string"),
                            "summary": datasets.Value("string"),
                        }
                    ),
                }
            )
        else:
            features = datasets.Features(
                {
                    "url": datasets.Value("string"),
                    "article": datasets.Sequence(
                        {
                            "section_name": datasets.Value("string"),
                            "document": datasets.Value("string"),
                            "summary": datasets.Value("string"),
                            "english_url": datasets.Value("string"),
                            "english_section_name": datasets.Value("string"),
                        }
                    ),
                }
            )

        return datasets.DatasetInfo(
            # This is the description that will appear on the datasets page.
            description=_DESCRIPTION,
            # This defines the different columns of the dataset and their types
            features=features,  # Here we define them above because they are different between the two configurations
            # If there's a common (input, target) tuple from the features,
            # specify them here. They'll be used if as_supervised=True in
            # builder.as_dataset.
            supervised_keys=None,
            # Homepage of the dataset for documentation
            homepage=_HOMEPAGE,
            # License for the dataset if available
            license=_LICENSE,
            # Citation for the dataset
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        """Returns SplitGenerators."""
        my_urls = _URLs[self.config.name]
        # See create_dummy.py to create new dummy data
        train_fname = dl_manager.download_and_extract(my_urls)
        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={
                    "filepath": train_fname,
                    "split": "train",
                },
            ),
        ]

    def _process_article(self, article):
        """Parse the article and convert into list of dict"""
        processed_article = []
        for key, value in article.items():
            row = {"section_name": key, "document": value["document"], "summary": value["summary"]}

            if self.config.name != "english":
                row["english_url"] = value["english_url"]
                row["english_section_name"] = value["english_section_name"]
            processed_article.append(row)

        return processed_article

    def _generate_examples(self, filepath, split):
        """Yields examples."""
        with open(filepath, "rb") as f:
            data = pickle.load(f)
            for id_, row in enumerate(data.items()):
                yield id_, {"url": row[0], "article": self._process_article(row[1])}
