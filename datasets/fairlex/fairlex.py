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
"""Fairlex: A multilingual benchmark for evaluating fairness in legal text processing."""

import json
import os
import textwrap

import datasets


MAIN_CITATION = """\
@inproceedings{chalkidis-etal-2022-fairlex,
    author={Chalkidis, Ilias and Passini, Tommaso and Zhang, Sheng and
            Tomada, Letizia and Schwemer, Sebastian Felix and Søgaard, Anders},
    title={FairLex: A Multilingual Benchmark for Evaluating Fairness in Legal Text Processing},
    booktitle={Proceedings of the 60th Annual Meeting of the Association for Computational Linguistics},
    year={2022},
    address={Dublin, Ireland}
}
"""

_DESCRIPTION = """\
Fairlex: A multilingual benchmark for evaluating fairness in legal text processing.
"""

ECTHR_ARTICLES = ["2", "3", "5", "6", "8", "9", "10", "11", "14", "P1-1"]

SCDB_ISSUE_AREAS = [
    "Criminal Procedure",
    "Civil Rights",
    "First Amendment",
    "Due Process",
    "Privacy",
    "Attorneys",
    "Unions",
    "Economic Activity",
    "Judicial Power",
    "Federalism",
    "Federal Taxation",
]

FSCS_LABELS = ["dismissal", "approval"]

CAIL_LABELS = ["0", "<=12", "<=36", "<=60", "<=120", ">120"]


class FairlexConfig(datasets.BuilderConfig):
    """BuilderConfig for Fairlex."""

    def __init__(
        self,
        label_column,
        url,
        data_url,
        citation,
        label_classes=None,
        multi_label=None,
        attributes=None,
        **kwargs,
    ):
        """BuilderConfig for Fairlex.

        Args:
          label_column: `string`, name of the column in the jsonl file corresponding
            to the label
          url: `string`, url for the original project
          data_url: `string`, url to download the zip file from
          data_file: `string`, filename for data set
          citation: `string`, citation for the data set
          url: `string`, url for information about the data set
          label_classes: `list[string]`, the list of classes if the label is
            categorical. If not provided, then the label will be of type
            `datasets.Value('float32')`.
          multi_label: `boolean`, True if the task is multi-label
          attributes: `List<string>`, names of the protected attributes
          **kwargs: keyword arguments forwarded to super.
        """
        super(FairlexConfig, self).__init__(version=datasets.Version("1.0.0", ""), **kwargs)
        self.label_column = label_column
        self.label_classes = label_classes
        self.multi_label = multi_label
        self.attributes = attributes
        self.url = url
        self.data_url = data_url
        self.citation = citation


class Fairlex(datasets.GeneratorBasedBuilder):
    """Fairlex: A multilingual benchmark for evaluating fairness in legal text processing. Version 1.0"""

    BUILDER_CONFIGS = [
        FairlexConfig(
            name="ecthr",
            description=textwrap.dedent(
                """\
            The European Court of Human Rights (ECtHR) hears allegations that a state has breached human rights
            provisions of the European Convention of Human Rights (ECHR). We use the dataset of Chalkidis et al.
            (2021), which contains 11K cases from ECtHR's public database. Each case is mapped to articles of the ECHR
            that were violated (if any). This is a multi-label text classification task. Given the facts of a case,
            the goal is to predict the ECHR articles that were violated, if any, as decided (ruled) by the court."""
            ),
            label_column="labels",
            label_classes=ECTHR_ARTICLES,
            multi_label=True,
            attributes=[
                ("applicant_age", ["n/a", "<=35", "<=65", ">65"]),
                ("applicant_gender", ["n/a", "male", "female"]),
                ("defendant_state", ["C.E. European", "Rest of Europe"]),
            ],
            data_url="https://zenodo.org/record/6322643/files/ecthr.zip",
            url="https://huggingface.co/datasets/ecthr_cases",
            citation=textwrap.dedent(
                """\
            @inproceedings{chalkidis-etal-2021-paragraph,
                title = "Paragraph-level Rationale Extraction through Regularization: A case study on {E}uropean Court of Human Rights Cases",
                author = "Chalkidis, Ilias  and
                  Fergadiotis, Manos  and
                  Tsarapatsanis, Dimitrios  and
                  Aletras, Nikolaos  and
                  Androutsopoulos, Ion  and
                  Malakasiotis, Prodromos",
                booktitle = "Proceedings of the 2021 Conference of the North American Chapter of the Association for Computational Linguistics: Human Language Technologies",
                month = jun,
                year = "2021",
                address = "Online",
                publisher = "Association for Computational Linguistics",
                url = "https://aclanthology.org/2021.naacl-main.22",
                doi = "10.18653/v1/2021.naacl-main.22",
                pages = "226--241",
            }
            }"""
            ),
        ),
        FairlexConfig(
            name="scotus",
            description=textwrap.dedent(
                """\
            The US Supreme Court (SCOTUS) is the highest federal court in the United States of America and generally
            hears only the most controversial or otherwise complex cases which have not been sufficiently well solved
            by lower courts. We combine information from SCOTUS opinions with the Supreme Court DataBase (SCDB)
            (Spaeth, 2020). SCDB provides metadata (e.g., date of publication, decisions, issues, decision directions
            and many more) for all cases. We consider the available 14 thematic issue areas (e.g, Criminal Procedure,
            Civil Rights, Economic Activity, etc.). This is a single-label multi-class document classification task.
            Given the court opinion, the goal is to predict the issue area whose focus is on the subject matter
            of the controversy (dispute). """
            ),
            label_column="label",
            label_classes=SCDB_ISSUE_AREAS,
            multi_label=False,
            attributes=[
                ("decision_direction", ["conservative", "liberal"]),
                ("respondent_type", ["other", "person", "organization", "public entity", "facility"]),
            ],
            url="http://scdb.wustl.edu/data.php",
            data_url="https://zenodo.org/record/6322643/files/scotus.zip",
            citation=textwrap.dedent(
                """\
            @misc{spaeth2020,
             author = {Harold J. Spaeth and Lee Epstein and Andrew D. Martin, Jeffrey A. Segal
             and Theodore J. Ruger and Sara C. Benesh},
             year = {2020},
             title ={{Supreme Court Database, Version 2020 Release 01}},
             url= {http://Supremecourtdatabase.org},
             howpublished={Washington University Law}
            }"""
            ),
        ),
        FairlexConfig(
            name="fscs",
            description=textwrap.dedent(
                """\
            The Federal Supreme Court of Switzerland (FSCS) is the last level of appeal in Switzerland and similarly
            to SCOTUS, the court generally hears only the most controversial or otherwise complex cases which have
            not been sufficiently well solved by lower courts. The court often focus only on small parts of previous
            decision, where they discuss possible wrong reasoning by the lower court. The Swiss-Judgment-Predict
            dataset (Niklaus et al., 2021) contains more than 85K decisions from the FSCS written in one of three
            languages (50K German, 31K French, 4K Italian) from the years 2000 to 2020. The dataset is not parallel,
            i.e., all cases are unique and decisions are written only in a single language. The dataset provides labels
            for a simplified binary (approval, dismissal) classification task. Given the facts of the case, the goal
            is to predict if the plaintiff's request is valid or partially valid."""
            ),
            label_column="label",
            label_classes=FSCS_LABELS,
            multi_label=False,
            attributes=[
                ("decision_language", ["de", "fr", "it"]),
                ("legal_area", ["other", "public law", "penal law", "civil law", "social law", "insurance law"]),
                (
                    "court_region",
                    [
                        "n/a",
                        "Région lémanique",
                        "Zürich",
                        "Espace Mittelland",
                        "Northwestern Switzerland",
                        "Eastern Switzerland",
                        "Central Switzerland",
                        "Ticino",
                        "Federation",
                    ],
                ),
            ],
            url="https://github.com/JoelNiklaus/SwissCourtRulingCorpus",
            data_url="https://zenodo.org/record/6322643/files/fscs.zip",
            citation=textwrap.dedent(
                """\
            @InProceedings{niklaus-etal-2021-swiss,
              author = {Niklaus, Joel
                            and Chalkidis, Ilias
                            and Stürmer, Matthias},
              title = {Swiss-Court-Predict: A Multilingual Legal Judgment Prediction Benchmark},
              booktitle = {Proceedings of the 2021 Natural Legal Language Processing Workshop},
              year = {2021},
              location = {Punta Cana, Dominican Republic},
            }"""
            ),
        ),
        FairlexConfig(
            name="cail",
            description=textwrap.dedent(
                """\
            The Supreme People's Court of China (CAIL) is the last level of appeal in China and considers cases that
            originated from the high people's courts concerning matters of national importance. The Chinese AI and Law
            challenge (CAIL) dataset (Xiao et al., 2018) is a Chinese legal NLP dataset for judgment prediction and
            contains over 1m criminal cases. The dataset provides labels for relevant article of criminal code
            prediction, charge (type of crime) prediction, imprisonment term (period) prediction, and monetary penalty
            prediction. The updated (soft) version of the CAIL dataset has 104K criminal court cases. The tasks is
            crime severity prediction task, a multi-class classification task, where given the facts of a case,
            the goal is to predict how severe was the committed crime with respect to the imprisonment term.
            We approximate crime severity by the length of imprisonment term, split in 6 clusters
            (0, >=12, >=36, >=60, >=120, >120 months)."""
            ),
            label_column="label",
            label_classes=CAIL_LABELS,
            multi_label=False,
            attributes=[
                ("defendant_gender", ["male", "female"]),
                ("court_region", ["Beijing", "Liaoning", "Hunan", "Guangdong", "Sichuan", "Guangxi", "Zhejiang"]),
            ],
            url="https://github.com/thunlp/LegalPLMs",
            data_url="https://zenodo.org/record/6322643/files/cail.zip",
            citation=textwrap.dedent(
                """\
            @article{wang-etal-2021-equality,
                  title={Equality before the Law: Legal Judgment Consistency Analysis for Fairness},
                  author={Yuzhong Wang and Chaojun Xiao and Shirong Ma and Haoxi Zhong and Cunchao Tu and Tianyang Zhang and Zhiyuan Liu and Maosong Sun},
                  year={2021},
                  journal={Science China  - Information Sciences},
                  url={https://arxiv.org/abs/2103.13868}
            }"""
            ),
        ),
    ]

    def _info(self):
        features = {"text": datasets.Value("string")}
        if self.config.multi_label:
            features["labels"] = datasets.features.Sequence(datasets.ClassLabel(names=self.config.label_classes))
        else:
            features["label"] = datasets.ClassLabel(names=self.config.label_classes)
        for attribute_name, attribute_groups in self.config.attributes:
            features[attribute_name] = datasets.ClassLabel(names=attribute_groups)
        return datasets.DatasetInfo(
            description=self.config.description,
            features=datasets.Features(features),
            homepage=self.config.url,
            citation=self.config.citation + "\n" + MAIN_CITATION,
        )

    def _split_generators(self, dl_manager):
        data_dir = dl_manager.download_and_extract(self.config.data_url)
        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={
                    "filepath": os.path.join(data_dir, "train.jsonl"),
                    "split": "train",
                },
            ),
            datasets.SplitGenerator(
                name=datasets.Split.TEST,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={
                    "filepath": os.path.join(data_dir, "test.jsonl"),
                    "split": "test",
                },
            ),
            datasets.SplitGenerator(
                name=datasets.Split.VALIDATION,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={
                    "filepath": os.path.join(data_dir, "val.jsonl"),
                    "split": "val",
                },
            ),
        ]

    def _generate_examples(self, filepath, split):
        """This function returns the examples in the raw (text) form."""
        with open(filepath, encoding="utf-8") as f:
            for id_, row in enumerate(f):
                data = json.loads(row)
                example = {
                    "text": data["text"],
                    self.config.label_column: data[self.config.label_column],
                }
                for attribute_name, _ in self.config.attributes:
                    example[attribute_name] = data["attributes"][attribute_name]
                yield id_, example
