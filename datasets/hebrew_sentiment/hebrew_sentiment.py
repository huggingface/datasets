"""HebrewSentiment: A Modern Hebrew Sentiment Analysis Dataset."""

from __future__ import absolute_import, division, print_function

import csv

import datasets


_DESCRIPTION = """\
HebrewSentiment is a data set consists of 12,804 user comments to posts on the official Facebook page of Israel’s
president, Mr. Reuven Rivlin. In October 2015, we used the open software application Netvizz (Rieder,
2013) to scrape all the comments to all of the president’s posts in the period of June – August 2014,
the first three months of Rivlin’s presidency.2 While the president’s posts aimed at reconciling tensions
and called for tolerance and empathy, the sentiment expressed in the comments to the president’s posts
was polarized between citizens who warmly thanked the president, and citizens that fiercely critiqued his
policy. Of the 12,804 comments, 370 are neutral; 8,512 are positive, 3,922 negative.

Data Annotation: A trained researcher examined each comment and determined its sentiment value,
where comments with an overall positive sentiment were assigned the value 1, comments with an overall
negative sentiment were assigned the value -1, and comments that are off-topic to the post’s content
were assigned the value 0. We validated the coding scheme by asking a second trained researcher to
code the same data. There was substantial agreement between raters (N of agreements: 10623, N of
disagreements: 2105, Coehn’s Kappa = 0.697, p = 0).
"""

_CITATION = """\
@inproceedings{amram-etal-2018-representations,
    title = "Representations and Architectures in Neural Sentiment Analysis for Morphologically Rich Languages: A Case Study from {M}odern {H}ebrew",
    author = "Amram, Adam  and
      Ben David, Anat  and
      Tsarfaty, Reut",
    booktitle = "Proceedings of the 27th International Conference on Computational Linguistics",
    month = aug,
    year = "2018",
    address = "Santa Fe, New Mexico, USA",
    publisher = "Association for Computational Linguistics",
    url = "https://www.aclweb.org/anthology/C18-1190",
    pages = "2242--2252",
    abstract = "This paper empirically studies the effects of representation choices on neural sentiment analysis for Modern Hebrew, a morphologically rich language (MRL) for which no sentiment analyzer currently exists. We study two dimensions of representational choices: (i) the granularity of the input signal (token-based vs. morpheme-based), and (ii) the level of encoding of vocabulary items (string-based vs. character-based). We hypothesise that for MRLs, languages where multiple meaning-bearing elements may be carried by a single space-delimited token, these choices will have measurable effects on task perfromance, and that these effects may vary for different architectural designs {---} fully-connected, convolutional or recurrent. Specifically, we hypothesize that morpheme-based representations will have advantages in terms of their generalization capacity and task accuracy, due to their better OOV coverage. To empirically study these effects, we develop a new sentiment analysis benchmark for Hebrew, based on 12K social media comments, and provide two instances of these data: in token-based and morpheme-based settings. Our experiments show that representation choices empirical effects vary with architecture type. While fully-connected and convolutional networks slightly prefer token-based settings, RNNs benefit from a morpheme-based representation, in accord with the hypothesis that explicit morphological information may help generalize. Our endeavour also delivers the first state-of-the-art broad-coverage sentiment analyzer for Hebrew, with over 89% accuracy, alongside an established benchmark to further study the effects of linguistic representation choices on neural networks{'} task performance.",
}
"""

_TRAIN_TOKEN_DOWNLOAD_URL = (
    "https://github.com/omilab/Neural-Sentiment-Analyzer-for-Modern-Hebrew/blob/master/data/token_train.tsv?raw=true"
)
_TEST_TOKEN_DOWNLOAD_URL = (
    "https://github.com/omilab/Neural-Sentiment-Analyzer-for-Modern-Hebrew/blob/master/data/token_test.tsv?raw=true"
)
_TRAIN_MORPH_DOWNLOAD_URL = (
    "https://github.com/omilab/Neural-Sentiment-Analyzer-for-Modern-Hebrew/blob/master/data/morph_train.tsv?raw=true"
)
_TEST_MORPH_DOWNLOAD_URL = (
    "https://github.com/omilab/Neural-Sentiment-Analyzer-for-Modern-Hebrew/blob/master/data/morph_test.tsv?raw=true"
)


class HebrewSentimentConfig(datasets.BuilderConfig):
    """BuilderConfig for HebrewSentiment."""

    def __init__(self, granularity="token", **kwargs):
        """BuilderConfig for HebrewSentiment.
        Args:
          **kwargs: keyword arguments forwarded to super.
        """
        assert granularity in {"token", "morph"}
        self.granularity = granularity
        super(HebrewSentimentConfig, self).__init__(**kwargs)


class HebrewSentiment(datasets.GeneratorBasedBuilder):
    """HebrewSentiment: A Modern Hebrew Sentiment Analysis Dataset."""

    BUILDER_CONFIG_CLASS = HebrewSentimentConfig

    DEFAULT_CONFIG_NAME = "token"

    BUILDER_CONFIGS = [
        HebrewSentimentConfig(
            name="token",
            version=datasets.Version("1.0.0", ""),
            description="Hebrew Sentiment Dataset with token-based tokenization.",
            granularity="token",
        ),
        HebrewSentimentConfig(
            name="morph",
            version=datasets.Version("1.0.0", ""),
            description="Hebrew Sentiment Dataset with morpheme-based tokenization.",
            granularity="morph",
        ),
    ]

    def _info(self):
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=datasets.Features(
                {
                    "text": datasets.Value("string"),
                    "label": datasets.features.ClassLabel(names=["pos", "neg", "off-topic"]),
                }
            ),
            homepage="https://github.com/omilab/Neural-Sentiment-Analyzer-for-Modern-Hebrew",
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        train_url = _TRAIN_TOKEN_DOWNLOAD_URL if self.config.granularity == "token" else _TRAIN_MORPH_DOWNLOAD_URL
        train_path = dl_manager.download_and_extract(train_url)
        test_url = _TEST_TOKEN_DOWNLOAD_URL if self.config.granularity == "token" else _TEST_MORPH_DOWNLOAD_URL
        test_path = dl_manager.download_and_extract(test_url)

        return [
            datasets.SplitGenerator(name=datasets.Split.TRAIN, gen_kwargs={"filepath": train_path}),
            datasets.SplitGenerator(name=datasets.Split.TEST, gen_kwargs={"filepath": test_path}),
        ]

    def _generate_examples(self, filepath):
        """Generate Hebrew Sentiment examples."""
        with open(filepath, encoding="utf-8") as csv_file:
            csv_reader = csv.DictReader(csv_file, fieldnames=["text", "label"], delimiter="\t")
            for id_, row in enumerate(csv_reader):
                row["label"] = int(row["label"])
                yield id_, row
