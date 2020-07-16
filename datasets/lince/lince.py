"""TODO(lince): Add a description here."""

from __future__ import absolute_import, division, print_function

import csv
import os
import re
import textwrap
from itertools import groupby

import numpy as np
import six

import nlp


_CITATION = """\
@inproceedings{aguilar-etal-2020-lince,
    title = "{L}in{CE}: A Centralized Benchmark for Linguistic Code-switching Evaluation",
    author = "Aguilar, Gustavo  and
      Kar, Sudipta  and
      Solorio, Thamar",
    booktitle = "Proceedings of The 12th Language Resources and Evaluation Conference",
    month = may,
    year = "2020",
    address = "Marseille, France",
    publisher = "European Language Resources Association",
    url = "https://www.aclweb.org/anthology/2020.lrec-1.223",
    pages = "1803--1813",
    language = "English",
    ISBN = "979-10-95546-34-4",
}

Note that each LinCE dataset has its own citation. Please see the source to see
the correct citation for each contained dataset."""

_DESCRIPTION = """\
LinCE is a centralized Linguistic Code-switching Evaluation benchmark 
(https://ritual.uh.edu/lince/) that contains data for training and evaluating
NLP systems on code-switching tasks.
"""

_LINCE_URL = "https://ritual.uh.edu/lince/libaccess/eyJ1c2VybmFtZSI6ICJodWdnaW5nZmFjZSBubHAiLCAidXNlcl9pZCI6IDExMSwgImVtYWlsIjogImR1bW15QGVtYWlsLmNvbSJ9"

_DATASET_CITATIONS = {
    "lid_spaeng": textwrap.dedent(
        """
        @inproceedings{molina-etal-2016-overview,
           title = "Overview for the Second Shared Task on Language Identification in Code-Switched Data",
           author = "Molina, Giovanni and
                     AlGhamdi, Fahad and
                     Ghoneim, Mahmoud and
                     Hawwari, Abdelati and
                     Rey-Villamizar, Nicolas and
                     Diab, Mona and
                     Solorio, Thamar",
           booktitle = "Proceedings of the Second Workshop on Computational Approaches to Code Switching",
           month = nov,
           year = "2016",
           address = "Austin, Texas",
           publisher = "Association for Computational Linguistics",
           url = "https://www.aclweb.org/anthology/W16-5805",
           doi = "10.18653/v1/W16-5805",
           pages = "40--49",
        }
        """
    ),
    "lid_hineng": textwrap.dedent(
        """
        @inproceedings{mave-etal-2018-language,
           title = "Language Identification and Analysis of Code-Switched Social Media Text",
           author = "Mave, Deepthi and
                     Maharjan, Suraj and
                     Solorio, Thamar",
           booktitle = "Proceedings of the Third Workshop on Computational Approaches to Linguistic Code-Switching",
           month = jul,
           year = "2018",
           address = "Melbourne, Australia",
           publisher = "Association for Computational Linguistics",
           url = "https://www.aclweb.org/anthology/W18-3206",
           pages = "51--61"
        }
        """
    ),
    "lid_msaea": textwrap.dedent(
        """
        @inproceedings{molina-etal-2016-overview,
           title = "Overview for the Second Shared Task on Language Identification in Code-Switched Data",
           author = "Molina, Giovanni and
                     AlGhamdi, Fahad and
                     Ghoneim, Mahmoud and
                     Hawwari, Abdelati and
                     Rey-Villamizar, Nicolas and
                     Diab, Mona and
                     Solorio, Thamar",
           booktitle = "Proceedings of the Second Workshop on Computational Approaches to Code Switching",
           month = nov,
           year = "2016",
           address = "Austin, Texas",
           publisher = "Association for Computational Linguistics",
           url = "https://www.aclweb.org/anthology/W16-5805",
           doi = "10.18653/v1/W16-5805",
           pages = "40--49",
        }
        """
    ),
    "lid_nepeng": textwrap.dedent(
        """
        @inproceedings{solorio-etal-2014-overview,
           title = "Overview for the First Shared Task on Language Identification in Code-Switched Data",
           author = "Solorio, Thamar and
                     Blair, Elizabeth and
                     Maharjan, Suraj and
                     Bethard, Steven and
                     Diab, Mona and
                     Ghoneim, Mahmoud and
                     Hawwari, Abdelati and
                     AlGhamdi, Fahad and
                     Hirschberg, Julia and
                     Chang, Alison and
                     Fung, Pascale",
           booktitle = "Proceedings of the First Workshop on Computational Approaches to Code Switching",
           month = oct,
           year = "2014",
           address = "Doha, Qatar",
           publisher = "Association for Computational Linguistics",
           url = "https://www.aclweb.org/anthology/W14-3907",
           doi = "10.3115/v1/W14-3907",
           pages = "62--72",
        }
        """
    ),
    "pos_spaeng": textwrap.dedent(
        """
        @inproceedings{alghamdi-etal-2016-part,
           title = "Part of Speech Tagging for Code Switched Data",
           author = "AlGhamdi, Fahad and
                     Molina, Giovanni and
                     Diab, Mona and
                     Solorio, Thamar and
                     Hawwari, Abdelati and
                     Soto, Victor and
                     Hirschberg, Julia",
           booktitle = "Proceedings of the Second Workshop on Computational Approaches to Code Switching",
           month = nov,
           year = "2016",
           address = "Austin, Texas",
           publisher = "Association for Computational Linguistics",
           url = "https://www.aclweb.org/anthology/W16-5812",
           doi = "10.18653/v1/W16-5812",
           pages = "98--107",
        }
        """
    ),
    "pos_hineng": textwrap.dedent(
        """
        @inproceedings{singh-etal-2018-twitter,
           title = "A Twitter Corpus for {H}indi-{E}nglish Code Mixed {POS} Tagging",
           author = "Singh, Kushagra and
                     Sen, Indira and
                     Kumaraguru, Ponnurangam",
           booktitle = "Proceedings of the Sixth International Workshop on Natural Language Processing for Social Media",
           month = jul,
           year = "2018",
           address = "Melbourne, Australia",
           publisher = "Association for Computational Linguistics",
           url = "https://www.aclweb.org/anthology/W18-3503",
           doi = "10.18653/v1/W18-3503",
           pages = "12--17"
        }
        """
    ),
    "ner_spaeng": textwrap.dedent(
        """
        @inproceedings{aguilar-etal-2018-named,
           title = {{Named Entity Recognition on Code-Switched Data: Overview of the CALCS 2018 Shared Task}},
           author = "Aguilar, Gustavo and
                     AlGhamdi, Fahad and
                     Soto, Victor and
                     Diab, Mona and
                     Hirschberg, Julia and
                     Solorio, Thamar",
           booktitle = {{Proceedings of the Third Workshop on Computational Approaches to Linguistic Code-Switching}},
           month = jul,
           year = "2018",
           address = "Melbourne, Australia",
           publisher = "Association for Computational Linguistics",
           url = "https://www.aclweb.org/anthology/W18-3219",
           pages = "138--147"
        }  
        """
    ),
    "ner_msaea": textwrap.dedent(
        """
        @inproceedings{aguilar-etal-2018-named,
           title = {{Named Entity Recognition on Code-Switched Data: Overview of the CALCS 2018 Shared Task}},
           author = "Aguilar, Gustavo and
                     AlGhamdi, Fahad and
                     Soto, Victor and
                     Diab, Mona and
                     Hirschberg, Julia and
                     Solorio, Thamar",
           booktitle = {{Proceedings of the Third Workshop on Computational Approaches to Linguistic Code-Switching}},
           month = jul,
           year = "2018",
           address = "Melbourne, Australia",
           publisher = "Association for Computational Linguistics",
           url = "https://www.aclweb.org/anthology/W18-3219",
           pages = "138--147"
        }  
        """
    ),
    "ner_hineng": textwrap.dedent(
        """
        @inproceedings{singh-etal-2018-language,
           title = "Language Identification and Named Entity Recognition in {H}inglish Code Mixed Tweets",
           author = "Singh, Kushagra and
                     Sen, Indira and
                     Kumaraguru, Ponnurangam",
           booktitle = "Proceedings of {ACL} 2018, Student Research Workshop",
           month = jul,
           year = "2018",
           address = "Melbourne, Australia",
           publisher = "Association for Computational Linguistics",
           url = "https://www.aclweb.org/anthology/P18-3008",
           doi = "10.18653/v1/P18-3008",
           pages = "52--58",
        }
        """
    ),
    "sa_spaeng": textwrap.dedent(
        """
        @inproceedings{patwa2020sentimix,
          title={SemEval-2020 Task 9: Overview of Sentiment Analysis of Code-Mixed Tweets},
          author="Patwa, Parth and
                  Aguilar, Gustavo and
                  Kar, Sudipta and
                  Pandey, Suraj and
                  PYKL, Srinivas and
                  Garrette, Dan and
                  Gamb{\"a}ck, Bj{\"o}rn and
                  Chakraborty, Tanmoy and
                  Solorio, Thamar and  
                  Das, Amitava",
          booktitle = "Proceedings of the 14th International Workshop on Semantic Evaluation ({S}em{E}val-2020)",
          year = 2020,
          month = sep,
          address = "Barcelona, Spain",
          publisher = "Association for Computational Linguistics"
        }
        """
    ),
}


class LinceConfig(nlp.BuilderConfig):
    """BuilderConfig for LinCE"""

    def __init__(self, colnames, classes, label_column, **kwargs):
        super(LinceConfig, self).__init__(
            version=nlp.Version("1.0.0", description="The Linguistic Code-switching Evaluation (LinCE) benchmark"),
            **kwargs,
        )
        self.colnames = colnames
        self.classes = classes
        self.label_column = label_column


class Lince(nlp.GeneratorBasedBuilder):
    """TODO(lince): Short description of the LinCE dataset."""

    BUILDER_CONFIG_CLASS = LinceConfig
    BUILDER_CONFIGS = [
        # ==========================================================================================
        # Language Identification (LID) datasets
        LinceConfig(
            name="lid_spaeng",
            data_dir="lid_spaeng",
            colnames={"tokens": 0, "lid": 1},
            classes={"lid": ["lang1", "lang2", "ne", "fw", "ambiguous", "mixed", "other", "unk"]},
            label_column="lid",
            description="Spanish-English language identification dataset (Latin script)",
        ),
        LinceConfig(
            name="lid_hineng",
            data_dir="lid_hineng",
            colnames={"tokens": 0, "lid": 1},
            classes={"lid": ["lang1", "lang2", "ne", "fw", "ambiguous", "mixed", "other", "unk"]},
            label_column="lid",
            description="Hindi-English language identification dataset (Latin script)",
        ),
        LinceConfig(
            name="lid_msaea",
            data_dir="lid_msaea",
            colnames={"tokens": 0, "lid": 1},
            classes={"lid": ["ambiguous", "lang1", "lang2", "mixed", "ne", "other"],},
            label_column="lid",
            description="Modern Standard Arabic-Egyptian Arabic language identification dataset (Persian script)",
        ),
        LinceConfig(
            name="lid_nepeng",
            data_dir="lid_nepeng",
            colnames={"tokens": 0, "lid": 1},
            classes={"lid": ["ambiguous", "lang1", "lang2", "mixed", "ne", "other"],},
            label_column="lid",
            description="Nepali-English language identification dataset (Latin script)",
        ),
        # ==========================================================================================
        # Part-of-Speech (POS) Tagging datasets
        LinceConfig(
            name="pos_spaeng",
            data_dir="pos_spaeng",
            colnames={"tokens": 0, "lid": 1, "pos": 2},
            classes={
                "lid": ["UNK", "eng", "eng&spa", "spa"],
                "pos": [
                    "ADJ",
                    "ADP",
                    "ADV",
                    "AUX",
                    "CONJ",
                    "DET",
                    "INTJ",
                    "NOUN",
                    "NUM",
                    "PART",
                    "PRON",
                    "PROPN",
                    "PUNCT",
                    "SCONJ",
                    "UNK",
                    "VERB",
                    "X",
                ],
            },
            label_column="pos",
            description="Spanish-English part-of-Speech tagging dataset (Latin script)",
        ),
        LinceConfig(
            name="pos_hineng",
            data_dir="pos_hineng",
            colnames={"tokens": 0, "lid": 1, "pos": 2},
            classes={
                "lid": ["en", "hi", "rest"],
                "pos": [
                    "ADJ",
                    "ADP",
                    "ADV",
                    "CONJ",
                    "DET",
                    "NOUN",
                    "NUM",
                    "PART",
                    "PART_NEG",
                    "PRON",
                    "PRON_WH",
                    "PROPN",
                    "VERB",
                    "X",
                ],
            },
            label_column="pos",
            description="Hindi-English part-of-Speech tagging dataset (Latin script)",
        ),
        # ==========================================================================================
        # Named Entity Recongition (NER) datasets
        LinceConfig(
            name="ner_spaeng",
            data_dir="ner_spaeng",
            colnames={"tokens": 0, "lid": 1, "ner": 2},
            classes={
                "lid": ["lang1", "lang2", "ne", "fw", "ambiguous", "mixed", "other", "unk"],
                "ner": [
                    "O",
                    "B-PER",
                    "I-PER",
                    "B-LOC",
                    "I-LOC",
                    "B-ORG",
                    "I-ORG",
                    "B-PROD",
                    "I-PROD",
                    "B-EVENT",
                    "I-EVENT",
                    "B-GROUP",
                    "I-GROUP",
                    "B-TITLE",
                    "I-TITLE",
                    "B-TIME",
                    "I-TIME",
                    "B-OTHER",
                    "I-OTHER",
                ],
            },
            label_column="ner",
            description="Spanish-English named entity recognition dataset (Latin script)",
        ),
        LinceConfig(
            name="ner_msaea",
            data_dir="ner_msaea",
            colnames={"tokens": 0, "ner": 1},
            classes={
                "ner": [
                    "O",
                    "B-PER",
                    "I-PER",
                    "B-LOC",
                    "I-LOC",
                    "B-ORG",
                    "I-ORG",
                    "B-PROD",
                    "I-PROD",
                    "B-EVENT",
                    "I-EVENT",
                    "B-GROUP",
                    "I-GROUP",
                    "B-TITLE",
                    "I-TITLE",
                    "B-TIME",
                    "I-TIME",
                    "B-OTHER",
                    "I-OTHER",
                ],
            },
            label_column="ner",
            description="Modern Standard Arabic-Egyptian Arabic named entity recognition dataset (Persian script)",
        ),
        LinceConfig(
            name="ner_hineng",
            data_dir="ner_hineng",
            colnames={"tokens": 0, "lid": 1, "ner": 2},
            classes={
                "lid": ["en", "hi", "rest"],
                "ner": ["O", "B-PERSON", "I-PERSON", "B-ORGANISATION", "I-ORGANISATION", "B-PLACE", "I-PLACE"],
            },
            label_column="ner",
            description="Hindi-English named entity recognition dataset (Latin script)",
        ),
        # ==========================================================================================
        # Sentiment Analysis (SA) datasets
        LinceConfig(
            name="sa_spaeng",
            data_dir="sa_spaeng",
            colnames={"tokens": 0, "lid": 1, "sa": 2},
            classes={
                "lid": ["lang1", "lang2", "ne", "fw", "ambiguous", "mixed", "other", "unk"],
                "sa": ["positive", "neutral", "negative"],
            },
            label_column="sa",
            description="Spanish-English sentiment analysis dataset (Latin script)",
        ),
    ]

    def _info(self):
        features = {"idx": nlp.Value("int32"), "tokens": nlp.Sequence(nlp.Value("string"))}

        if self.config.name != "ner_msaea":
            features["lid"] = nlp.Sequence(nlp.Value("string"))  # excluding 'ner_msaea', all datasets have 'lid'

        if self.config.name.startswith("pos_"):
            features["pos"] = nlp.Sequence(nlp.Value("string"))

        elif self.config.name.startswith("ner_"):
            features["ner"] = nlp.Sequence(nlp.Value("string"))

        elif self.config.name.startswith("sa_"):
            features["sa"] = nlp.Value("string")

        return nlp.DatasetInfo(
            description=_DESCRIPTION,
            features=nlp.Features(features),
            supervised_keys=None,
            homepage="http://ritual.uh.edu/lince",
            citation=_DATASET_CITATIONS.get(self.config.name, "") + "\n" + _CITATION,
        )

    def _split_generators(self, dl_manager):
        """Returns SplitGenerators."""
        lince_dir = dl_manager.download_and_extract(f"{_LINCE_URL}/{self.config.name}.zip")
        data_dir = os.path.join(lince_dir, self.config.data_dir)
        return [
            nlp.SplitGenerator(
                name=nlp.Split.TRAIN,
                gen_kwargs={"filepath": os.path.join(data_dir, "train.conll"), "colnames": self.config.colnames,},
            ),
            nlp.SplitGenerator(
                name=nlp.Split.VALIDATION,
                gen_kwargs={"filepath": os.path.join(data_dir, "dev.conll"), "colnames": self.config.colnames,},
            ),
            nlp.SplitGenerator(
                name=nlp.Split.TEST,
                gen_kwargs={
                    "filepath": os.path.join(data_dir, "test.conll"),
                    "colnames": {
                        key: self.config.colnames[key]
                        for key in six.iterkeys(self.config.colnames)
                        if key != self.config.label_column
                    },
                },
            ),
        ]

    def _generate_examples(self, filepath, colnames, delimiter="\t", metaregex=r"^# sent_enum = [0-9]+$"):
        def is_empty_line(token_pack):
            return all(field.strip() == "" for field in token_pack)

        index = 0
        for is_empty, pack in groupby(
            csv.reader(open(filepath), delimiter=delimiter, quoting=csv.QUOTE_NONE), is_empty_line
        ):
            if is_empty is False:
                # packed sentence -> [['tok_1', 'lid_1', 'ner_1'], ..., ['tok_n', 'lid_n', 'ner_n']]
                pack = list(pack)
                meta = []

                if re.match(metaregex, pack[0][0]):  # for sentence-level annotations (or meta)
                    meta = pack[0][1:]  # keep the sentence-level labels
                    pack = pack[1:]  # ignore meta fields to unzip

                unpacked = list(zip(*pack))
                if meta:
                    unpacked = unpacked + meta

                row = {feature: unpacked[colnames[feature]] for feature in colnames}
                row["idx"] = index
                index += 1

                # dummy labels for the test set
                if self.config.label_column not in row:
                    if self.config.label_column == "sa":
                        row[self.config.label_column] = ""
                    else:
                        row[self.config.label_column] = [""] * len(row["tokens"])

                yield index, row
