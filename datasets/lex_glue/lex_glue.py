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
"""LexGLUE: A Benchmark Dataset for Legal Language Understanding in English."""

import csv
import json
import textwrap

import datasets


MAIN_CITATION = """\
@article{chalkidis-etal-2021-lexglue,
      title={{LexGLUE}: A Benchmark Dataset for Legal Language Understanding in English},
      author={Chalkidis, Ilias and
      Jana, Abhik and
      Hartung, Dirk and
      Bommarito, Michael and
      Androutsopoulos, Ion and
      Katz, Daniel Martin and
      Aletras, Nikolaos},
      year={2021},
      eprint={2110.00976},
      archivePrefix={arXiv},
      primaryClass={cs.CL},
      note = {arXiv: 2110.00976},
}"""

_DESCRIPTION = """\
Legal General Language Understanding Evaluation (LexGLUE) benchmark is
a collection of datasets for evaluating model performance across a diverse set of legal NLU tasks
"""

ECTHR_ARTICLES = ["2", "3", "5", "6", "8", "9", "10", "11", "14", "P1-1"]

EUROVOC_CONCEPTS = [
    "100163",
    "100164",
    "100165",
    "100166",
    "100167",
    "100168",
    "100169",
    "100170",
    "100171",
    "100172",
    "100173",
    "100174",
    "100175",
    "100176",
    "100177",
    "100178",
    "100179",
    "100180",
    "100181",
    "100182",
    "100183",
    "100184",
    "100185",
    "100186",
    "100187",
    "100188",
    "100189",
    "100190",
    "100191",
    "100192",
    "100193",
    "100194",
    "100195",
    "100196",
    "100197",
    "100198",
    "100199",
    "100200",
    "100201",
    "100202",
    "100203",
    "100204",
    "100205",
    "100206",
    "100207",
    "100208",
    "100209",
    "100210",
    "100211",
    "100212",
    "100213",
    "100214",
    "100215",
    "100216",
    "100217",
    "100218",
    "100219",
    "100220",
    "100221",
    "100222",
    "100223",
    "100224",
    "100225",
    "100226",
    "100227",
    "100228",
    "100229",
    "100230",
    "100231",
    "100232",
    "100233",
    "100234",
    "100235",
    "100236",
    "100237",
    "100238",
    "100239",
    "100240",
    "100241",
    "100242",
    "100243",
    "100244",
    "100245",
    "100246",
    "100247",
    "100248",
    "100249",
    "100250",
    "100251",
    "100252",
    "100253",
    "100254",
    "100255",
    "100256",
    "100257",
    "100258",
    "100259",
    "100260",
    "100261",
    "100262",
    "100263",
    "100264",
    "100265",
    "100266",
    "100267",
    "100268",
    "100269",
    "100270",
    "100271",
    "100272",
    "100273",
    "100274",
    "100275",
    "100276",
    "100277",
    "100278",
    "100279",
    "100280",
    "100281",
    "100282",
    "100283",
    "100284",
    "100285",
    "100286",
    "100287",
    "100288",
    "100289",
]

LEDGAR_CATEGORIES = [
    "Adjustments",
    "Agreements",
    "Amendments",
    "Anti-Corruption Laws",
    "Applicable Laws",
    "Approvals",
    "Arbitration",
    "Assignments",
    "Assigns",
    "Authority",
    "Authorizations",
    "Base Salary",
    "Benefits",
    "Binding Effects",
    "Books",
    "Brokers",
    "Capitalization",
    "Change In Control",
    "Closings",
    "Compliance With Laws",
    "Confidentiality",
    "Consent To Jurisdiction",
    "Consents",
    "Construction",
    "Cooperation",
    "Costs",
    "Counterparts",
    "Death",
    "Defined Terms",
    "Definitions",
    "Disability",
    "Disclosures",
    "Duties",
    "Effective Dates",
    "Effectiveness",
    "Employment",
    "Enforceability",
    "Enforcements",
    "Entire Agreements",
    "Erisa",
    "Existence",
    "Expenses",
    "Fees",
    "Financial Statements",
    "Forfeitures",
    "Further Assurances",
    "General",
    "Governing Laws",
    "Headings",
    "Indemnifications",
    "Indemnity",
    "Insurances",
    "Integration",
    "Intellectual Property",
    "Interests",
    "Interpretations",
    "Jurisdictions",
    "Liens",
    "Litigations",
    "Miscellaneous",
    "Modifications",
    "No Conflicts",
    "No Defaults",
    "No Waivers",
    "Non-Disparagement",
    "Notices",
    "Organizations",
    "Participations",
    "Payments",
    "Positions",
    "Powers",
    "Publicity",
    "Qualifications",
    "Records",
    "Releases",
    "Remedies",
    "Representations",
    "Sales",
    "Sanctions",
    "Severability",
    "Solvency",
    "Specific Performance",
    "Submission To Jurisdiction",
    "Subsidiaries",
    "Successors",
    "Survival",
    "Tax Withholdings",
    "Taxes",
    "Terminations",
    "Terms",
    "Titles",
    "Transactions With Affiliates",
    "Use Of Proceeds",
    "Vacations",
    "Venues",
    "Vesting",
    "Waiver Of Jury Trials",
    "Waivers",
    "Warranties",
    "Withholdings",
]

SCDB_ISSUE_AREAS = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13"]

UNFAIR_CATEGORIES = [
    "Limitation of liability",
    "Unilateral termination",
    "Unilateral change",
    "Content removal",
    "Contract by using",
    "Choice of law",
    "Jurisdiction",
    "Arbitration",
]

CASEHOLD_LABELS = ["0", "1", "2", "3", "4"]


class LexGlueConfig(datasets.BuilderConfig):
    """BuilderConfig for LexGLUE."""

    def __init__(
        self,
        text_column,
        label_column,
        url,
        data_url,
        data_file,
        citation,
        label_classes=None,
        multi_label=None,
        dev_column="dev",
        **kwargs,
    ):
        """BuilderConfig for LexGLUE.

        Args:
          text_column: ``string`, name of the column in the jsonl file corresponding
            to the text
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
          dev_column: `string`, name for the development subset
          **kwargs: keyword arguments forwarded to super.
        """
        super(LexGlueConfig, self).__init__(version=datasets.Version("1.0.0", ""), **kwargs)
        self.text_column = text_column
        self.label_column = label_column
        self.label_classes = label_classes
        self.multi_label = multi_label
        self.dev_column = dev_column
        self.url = url
        self.data_url = data_url
        self.data_file = data_file
        self.citation = citation


class LexGLUE(datasets.GeneratorBasedBuilder):
    """LexGLUE: A Benchmark Dataset for Legal Language Understanding in English. Version 1.0"""

    BUILDER_CONFIGS = [
        LexGlueConfig(
            name="ecthr_a",
            description=textwrap.dedent(
                """\
            The European Court of Human Rights (ECtHR) hears allegations that a state has
            breached human rights provisions of the European Convention of Human Rights (ECHR).
            For each case, the dataset provides a list of factual paragraphs (facts) from the case description.
            Each case is mapped to articles of the ECHR that were violated (if any)."""
            ),
            text_column="facts",
            label_column="violated_articles",
            label_classes=ECTHR_ARTICLES,
            multi_label=True,
            dev_column="dev",
            data_url="https://zenodo.org/record/5532997/files/ecthr.tar.gz",
            data_file="ecthr.jsonl",
            url="https://archive.org/details/ECtHR-NAACL2021",
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
        LexGlueConfig(
            name="ecthr_b",
            description=textwrap.dedent(
                """\
            The European Court of Human Rights (ECtHR) hears allegations that a state has
            breached human rights provisions of the European Convention of Human Rights (ECHR).
            For each case, the dataset provides a list of factual paragraphs (facts) from the case description.
            Each case is mapped to articles of ECHR that were allegedly violated (considered by the court)."""
            ),
            text_column="facts",
            label_column="allegedly_violated_articles",
            label_classes=ECTHR_ARTICLES,
            multi_label=True,
            dev_column="dev",
            url="https://archive.org/details/ECtHR-NAACL2021",
            data_url="https://zenodo.org/record/5532997/files/ecthr.tar.gz",
            data_file="ecthr.jsonl",
            citation=textwrap.dedent(
                """\
            @inproceedings{chalkidis-etal-2021-paragraph,
                title = "Paragraph-level Rationale Extraction through Regularization: A case study on {E}uropean Court of Human Rights Cases",
                author = "Chalkidis, Ilias
                and Fergadiotis, Manos
                and Tsarapatsanis, Dimitrios
                and  Aletras, Nikolaos
                and Androutsopoulos, Ion
                and Malakasiotis, Prodromos",
                booktitle = "Proceedings of the 2021 Conference of the North American Chapter of the Association for Computational Linguistics: Human Language Technologies",
                year = "2021",
                address = "Online",
                url = "https://aclanthology.org/2021.naacl-main.22",
            }
            }"""
            ),
        ),
        LexGlueConfig(
            name="eurlex",
            description=textwrap.dedent(
                """\
            European Union (EU) legislation is published in EUR-Lex portal.
            All EU laws are annotated by EU's Publications Office with multiple concepts from the EuroVoc thesaurus,
            a multilingual thesaurus maintained by the Publications Office.
            The current version of EuroVoc contains more than 7k concepts referring to various activities
            of the EU and its Member States (e.g., economics, health-care, trade).
            Given a document, the task is to predict its EuroVoc labels (concepts)."""
            ),
            text_column="text",
            label_column="labels",
            label_classes=EUROVOC_CONCEPTS,
            multi_label=True,
            dev_column="dev",
            url="https://zenodo.org/record/5363165#.YVJOAi8RqaA",
            data_url="https://zenodo.org/record/5532997/files/eurlex.tar.gz",
            data_file="eurlex.jsonl",
            citation=textwrap.dedent(
                """\
            @inproceedings{chalkidis-etal-2021-multieurlex,
              author = {Chalkidis, Ilias and
              Fergadiotis, Manos and
              Androutsopoulos, Ion},
              title = {MultiEURLEX -- A multi-lingual and multi-label legal document
                           classification dataset for zero-shot cross-lingual transfer},
              booktitle = {Proceedings of the 2021 Conference on Empirical Methods
                           in Natural Language Processing},
              year = {2021},
              location = {Punta Cana, Dominican Republic},
            }
            }"""
            ),
        ),
        LexGlueConfig(
            name="scotus",
            description=textwrap.dedent(
                """\
            The US Supreme Court  (SCOTUS) is the highest federal court in the United States of America
            and generally hears only the most controversial or otherwise complex cases which have not
            been sufficiently well solved by lower courts. This is a single-label multi-class classification
            task, where given a document (court opinion), the task is to predict the relevant issue areas.
            The 14 issue areas cluster 278 issues whose focus is on the subject matter of the controversy (dispute)."""
            ),
            text_column="text",
            label_column="issueArea",
            label_classes=SCDB_ISSUE_AREAS,
            multi_label=False,
            dev_column="dev",
            url="http://scdb.wustl.edu/data.php",
            data_url="https://zenodo.org/record/5532997/files/scotus.tar.gz",
            data_file="scotus.jsonl",
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
        LexGlueConfig(
            name="ledgar",
            description=textwrap.dedent(
                """\
            LEDGAR dataset aims contract provision (paragraph) classification.
            The contract provisions come from contracts obtained from the US Securities and Exchange Commission (SEC)
            filings, which are publicly available from EDGAR. Each label represents the single main topic
            (theme) of the corresponding contract provision."""
            ),
            text_column="text",
            label_column="clause_type",
            label_classes=LEDGAR_CATEGORIES,
            multi_label=False,
            dev_column="dev",
            url="https://metatext.io/datasets/ledgar",
            data_url="https://zenodo.org/record/5532997/files/ledgar.tar.gz",
            data_file="ledgar.jsonl",
            citation=textwrap.dedent(
                """\
            @inproceedings{tuggener-etal-2020-ledgar,
                title = "{LEDGAR}: A Large-Scale Multi-label Corpus for Text Classification of Legal Provisions in Contracts",
                author = {Tuggener, Don  and
                  von D{\"a}niken, Pius  and
                  Peetz, Thomas  and
                  Cieliebak, Mark},
                booktitle = "Proceedings of the 12th Language Resources and Evaluation Conference",
                year = "2020",
                address = "Marseille, France",
                url = "https://aclanthology.org/2020.lrec-1.155",
            }
            }"""
            ),
        ),
        LexGlueConfig(
            name="unfair_tos",
            description=textwrap.dedent(
                """\
            The UNFAIR-ToS dataset contains 50 Terms of Service (ToS) from on-line platforms (e.g., YouTube,
            Ebay, Facebook, etc.). The dataset has been annotated on the sentence-level with 8 types of
            unfair contractual terms (sentences), meaning terms that potentially violate user rights
            according to the European consumer law."""
            ),
            text_column="text",
            label_column="labels",
            label_classes=UNFAIR_CATEGORIES,
            multi_label=True,
            dev_column="val",
            url="http://claudette.eui.eu",
            data_url="https://zenodo.org/record/5532997/files/unfair_tos.tar.gz",
            data_file="unfair_tos.jsonl",
            citation=textwrap.dedent(
                """\
            @article{lippi-etal-2019-claudette,
                title = "{CLAUDETTE}: an automated detector of potentially unfair clauses in online terms of service",
                author = {Lippi, Marco
                and Pałka, Przemysław
                and Contissa, Giuseppe
                and Lagioia, Francesca
                and Micklitz, Hans-Wolfgang
                and Sartor, Giovanni
                and Torroni, Paolo},
                journal = "Artificial Intelligence and Law",
                year = "2019",
                publisher = "Springer",
                url = "https://doi.org/10.1007/s10506-019-09243-2",
                pages = "117--139",
            }"""
            ),
        ),
        LexGlueConfig(
            name="case_hold",
            description=textwrap.dedent(
                """\
            The CaseHOLD (Case Holdings on Legal Decisions) dataset contains approx. 53k multiple choice
            questions about holdings of US court cases from the Harvard Law Library case law corpus.
            Holdings are short summaries of legal rulings accompany referenced decisions relevant for the present case.
            The input consists of an excerpt (or prompt) from a court decision, containing a reference
            to a particular case, while the holding statement is masked out. The model must identify
            the correct (masked) holding statement from a selection of five choices."""
            ),
            text_column="text",
            label_column="labels",
            dev_column="dev",
            multi_label=False,
            label_classes=CASEHOLD_LABELS,
            url="https://github.com/reglab/casehold",
            data_url="https://zenodo.org/record/5532997/files/casehold.tar.gz",
            data_file="casehold.csv",
            citation=textwrap.dedent(
                """\
            @inproceedings{Zheng2021,
              author    = {Lucia Zheng and
                           Neel Guha and
                           Brandon R. Anderson and
                           Peter Henderson and
                           Daniel E. Ho},
              title     = {When Does Pretraining Help? Assessing Self-Supervised Learning for
                           Law and the CaseHOLD Dataset},
              year      = {2021},
              booktitle = {International Conference on Artificial Intelligence and Law},
            }"""
            ),
        ),
    ]

    def _info(self):
        if self.config.name == "case_hold":
            features = {
                "context": datasets.Value("string"),
                "endings": datasets.features.Sequence(datasets.Value("string")),
            }
        elif "ecthr" in self.config.name:
            features = {"text": datasets.features.Sequence(datasets.Value("string"))}
        else:
            features = {"text": datasets.Value("string")}
        if self.config.multi_label:
            features["labels"] = datasets.features.Sequence(datasets.ClassLabel(names=self.config.label_classes))
        else:
            features["label"] = datasets.ClassLabel(names=self.config.label_classes)
        return datasets.DatasetInfo(
            description=self.config.description,
            features=datasets.Features(features),
            homepage=self.config.url,
            citation=self.config.citation + "\n" + MAIN_CITATION,
        )

    def _split_generators(self, dl_manager):
        archive = dl_manager.download(self.config.data_url)
        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={
                    "filepath": self.config.data_file,
                    "split": "train",
                    "files": dl_manager.iter_archive(archive),
                },
            ),
            datasets.SplitGenerator(
                name=datasets.Split.TEST,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={
                    "filepath": self.config.data_file,
                    "split": "test",
                    "files": dl_manager.iter_archive(archive),
                },
            ),
            datasets.SplitGenerator(
                name=datasets.Split.VALIDATION,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={
                    "filepath": self.config.data_file,
                    "split": self.config.dev_column,
                    "files": dl_manager.iter_archive(archive),
                },
            ),
        ]

    def _generate_examples(self, filepath, split, files):
        """This function returns the examples in the raw (text) form."""
        if self.config.name == "case_hold":
            if "dummy" in filepath:
                SPLIT_RANGES = {"train": (1, 3), "dev": (3, 5), "test": (5, 7)}
            else:
                SPLIT_RANGES = {"train": (1, 45001), "dev": (45001, 48901), "test": (48901, 52501)}
            for path, f in files:
                if path == filepath:
                    f = (line.decode("utf-8") for line in f)
                    for id_, row in enumerate(list(csv.reader(f))[SPLIT_RANGES[split][0] : SPLIT_RANGES[split][1]]):
                        yield id_, {
                            "context": row[1],
                            "endings": [row[2], row[3], row[4], row[5], row[6]],
                            "label": str(row[12]),
                        }
                    break
        elif self.config.multi_label:
            for path, f in files:
                if path == filepath:
                    for id_, row in enumerate(f):
                        data = json.loads(row.decode("utf-8"))
                        labels = sorted(
                            list(set(data[self.config.label_column]).intersection(set(self.config.label_classes)))
                        )
                        if data["data_type"] == split:
                            yield id_, {
                                "text": data[self.config.text_column],
                                "labels": labels,
                            }
                    break
        else:
            for path, f in files:
                if path == filepath:
                    for id_, row in enumerate(f):
                        data = json.loads(row.decode("utf-8"))
                        if data["data_type"] == split:
                            yield id_, {
                                "text": data[self.config.text_column],
                                "label": data[self.config.label_column],
                            }
                    break
