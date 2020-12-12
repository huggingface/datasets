"""HebrewThisWorld: A corpus from https://thisworld.online/."""

from __future__ import absolute_import, division, print_function

import csv

import datasets

_DESCRIPTION = """\
HebrewThisWorld is a data set consists of 2028 issues of the newspaper 'This World' edited by Uri Avnery and were published between 1950 and 1989 
(more information on the About page). 
Released under the AGPLv3 license.
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

_TRAIN_DOWNLOAD_URL = (
    "https://drive.google.com/file/d/13lNbAIl8n1NLpfo7x9681mwAcwe-hUD2/view?usp=sharing"
)


class HebrewThisWorld(datasets.GeneratorBasedBuilder):
    """HebrewThisWorld: A Modern Hebrew Sentiment Analysis Dataset."""

    def _info(self):
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=datasets.Features(
                {
                    "issue_num": datasets.Value("int32"),
                    "page_count": datasets.Value("int32"),
                    "date": datasets.Value("string"),
                    "date_he": datasets.Value("string"),
                    "year": datasets.Value("int32"),
                    "href": datasets.Value("string"),
                    "pdf": datasets.Value("string"),
                    "coverpage": datasets.Value("string"),
                    "backpage": datasets.Value("string"),
                    "content": datasets.Value("string"),
                    "url": datasets.Value("string"),
                }
            ),
            homepage="https://github.com/thisworld1/thisworld.online/",
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        train_path = dl_manager.download_and_extract(_TRAIN_DOWNLOAD_URL)

        return [
            datasets.SplitGenerator(name=datasets.Split.TRAIN, gen_kwargs={"filepath": train_path}),
        ]

    def _generate_examples(self, filepath):
        """Generate Hebrew ThisWorld examples."""
        with open(filepath, encoding="utf-8") as csv_file:
            csv_reader = csv.DictReader(csv_file,
                                        fieldnames=["issue_num", "page_count", "date", "date_he", "year", "href", "pdf",
                                                    "coverpage", "backpage", "content", "url"])
            for id_, data in enumerate(csv_reader):
                yield id_, {
                    "issue_num": data["issue_num"],
                    "page_count": data["page_count"],
                    "date": data["date"],
                    "date_he": data["date_he"],
                    "year": data["year"],
                    "href": data["href"],
                    "pdf": data["pdf"],
                    "coverpage": data["coverpage"],
                    "backpage": data["backpage"],
                    "content": data["content"],
                    "url": data["url"]
                }