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

# Lint as: python3
"""The Multilingual dIalogAct benchMark."""


import textwrap

import pandas as pd

import datasets


_MIAM_CITATION = """\
@unpublished{
anonymous2021cross-lingual,
title={Cross-Lingual Pretraining Methods for Spoken Dialog},
author={Anonymous},
journal={OpenReview Preprint},
year={2021},
url{https://openreview.net/forum?id=c1oDhu_hagR},
note={anonymous preprint under review}
}
"""

_MIAM_DESCRIPTION = """\
Multilingual dIalogAct benchMark is a collection of resources for training, evaluating, and
analyzing natural language understanding systems specifically designed for spoken language. Datasets
are in English, French, German, Italian and Spanish. They cover a variety of domains including
spontaneous speech, scripted scenarios, and joint task completion. Some datasets additionally include
emotion and/or sentimant labels.
"""

_URL = "https://raw.githubusercontent.com/eusip/MIAM/main"

DIHANA_DA_DESCRIPTION = {
    "Afirmacion": "Feedback_positive",
    "Apertura": "Opening",
    "Cierre": "Closing",
    "Confirmacion": "Acknowledge",
    "Espera": "Hold",
    "Indefinida": "Undefined",
    "Negacion": "Feedback_negative",
    "No_entendido": "Request_clarify",
    "Nueva_consulta": "New_request",
    "Pregunta": "Request",
    "Respuesta": "Reply",
}


class MiamConfig(datasets.BuilderConfig):
    """BuilderConfig for MIAM."""

    def __init__(
        self,
        text_features,
        label_column,
        data_url,
        citation,
        url,
        label_classes=None,
        **kwargs,
    ):
        """BuilderConfig for MIAM.
        Args:
          text_features: `dict[string, string]`, map from the name of the feature
            dict for each text field to the name of the column in the tsv file
          label_column: `string`, name of the column in the csv/txt file corresponding
            to the label
          data_url: `string`, url to download the csv/text file from
          citation: `string`, citation for the data set
          url: `string`, url for information about the data set
          label_classes: `list[string]`, the list of classes if the label is
            categorical. If not provided, then the label will be of type
            `datasets.Value('float32')`.
          **kwargs: keyword arguments forwarded to super.
        """
        super(MiamConfig, self).__init__(version=datasets.Version("1.0.0", ""), **kwargs)
        self.text_features = text_features
        self.label_column = label_column
        self.label_classes = label_classes
        self.data_url = data_url
        self.citation = citation
        self.url = url


class Miam(datasets.GeneratorBasedBuilder):
    """The Multilingual dIalogAct benchMark."""

    BUILDER_CONFIGS = [
        MiamConfig(
            name="dihana",
            description=textwrap.dedent(
                """\
            The Dihana corpus primarily consists of spontaneous speech. The corpus is annotated
            using three different levels of labels. The first level is dedicated to the generic
            task-independent DA and the two additional are made with task-specific information. We
            focus on the 11 first level tags."""
            ),
            text_features={
                "Speaker": "Speaker",
                "Utterance": "Utterance",
                "Dialogue_Act": "Dialogue_Act",
                "Dialogue_ID": "Dialogue_ID",
                "File_ID": "File_ID",
            },
            label_classes=list(DIHANA_DA_DESCRIPTION.keys()),
            label_column="Dialogue_Act",
            data_url={
                "train": _URL + "/dihana/train.csv",
                "dev": _URL + "/dihana/dev.csv",
                "test": _URL + "/dihana/test.csv",
            },
            citation=textwrap.dedent(
                """\
            @inproceedings{benedi2006design,
            title={Design and acquisition of a telephone spontaneous speech dialogue corpus in Spanish: DIHANA},
            author={Bened{\'i}, Jos{\'e}-Miguel and Lleida, Eduardo and Varona, Amparo and Castro, Mar{\'i}a-Jos{\'e} and Galiano, Isabel and Justo, Raquel and L{\'o}pez, I and Miguel, Antonio},
            booktitle={Fifth International Conference on Language Resources and Evaluation (LREC)},
            pages={1636--1639},
            year={2006}
            }
            @inproceedings{post2013improved,
            title={Improved speech-to-text translation with the Fisher and Callhome Spanish--English speech translation corpus},
            author={Post, Matt and Kumar, Gaurav and Lopez, Adam and Karakos, Damianos and Callison-Burch, Chris and Khudanpur, Sanjeev},
            booktitle={Proc. IWSLT},
            year={2013}
            }
            @article{coria2005predicting,
            title={Predicting obligation dialogue acts from prosodic and speaker infomation},
            author={Coria, S and Pineda, L},
            journal={Research on Computing Science (ISSN 1665-9899), Centro de Investigacion en Computacion, Instituto Politecnico Nacional, Mexico City},
            year={2005}
            }"""
            ),
            url="",
        ),
        MiamConfig(
            name="ilisten",
            description=textwrap.dedent(
                """\
            "itaLIan Speech acT labEliNg" (iLISTEN) is a corpus of annotated dialogue turns labeled
            for speech acts."""
            ),
            text_features={
                "Speaker": "Speaker",
                "Utterance": "Utterance",
                "Dialogue_Act": "Dialogue_Act",
                "Dialogue_ID": "Dialogue_ID",
            },
            label_classes=[
                "AGREE",
                "ANSWER",
                "CLOSING",
                "ENCOURAGE-SORRY",
                "GENERIC-ANSWER",
                "INFO-REQUEST",
                "KIND-ATTITUDE_SMALL-TALK",
                "OFFER-GIVE-INFO",
                "OPENING",
                "PERSUASION-SUGGEST",
                "QUESTION",
                "REJECT",
                "SOLICITATION-REQ_CLARIFICATION",
                "STATEMENT",
                "TALK-ABOUT-SELF",
            ],
            label_column="Dialogue_Act",
            data_url={
                "train": _URL + "/ilisten/train.csv",
                "dev": _URL + "/ilisten/dev.csv",
                "test": _URL + "/ilisten/test.csv",
            },
            citation=textwrap.dedent(
                """\
            @article{basile2018overview,
            title={Overview of the Evalita 2018itaLIan Speech acT labEliNg (iLISTEN) Task},
            author={Basile, Pierpaolo and Novielli, Nicole},
            journal={EVALITA Evaluation of NLP and Speech Tools for Italian},
            volume={12},
            pages={44},
            year={2018}
            }"""
            ),
            url="",
        ),
        MiamConfig(
            name="loria",
            description=textwrap.dedent(
                """\
            The LORIA Nancy dialog corpus is derived from human-machine interactions in a serious
            game setting."""
            ),
            text_features={
                "Speaker": "Speaker",
                "Utterance": "Utterance",
                "Dialogue_Act": "Dialogue_Act",
                "Dialogue_ID": "Dialogue_ID",
                "File_ID": "File_ID",
            },
            label_classes=[
                "ack",
                "ask",
                "find_mold",
                "find_plans",
                "first_step",
                "greet",
                "help",
                "inform",
                "inform_engine",
                "inform_job",
                "inform_material_space",
                "informer_conditioner",
                "informer_decoration",
                "informer_elcomps",
                "informer_end_manufacturing",
                "kindAtt",
                "manufacturing_reqs",
                "next_step",
                "no",
                "other",
                "quality_control",
                "quit",
                "reqRep",
                "security_policies",
                "staff_enterprise",
                "staff_job",
                "studies_enterprise",
                "studies_job",
                "todo_failure",
                "todo_irreparable",
                "yes",
            ],
            label_column="Dialogue_Act",
            data_url={
                "train": _URL + "/loria/train.csv",
                "dev": _URL + "/loria/dev.csv",
                "test": _URL + "/loria/test.csv",
            },
            citation=textwrap.dedent(
                """\
            @inproceedings{barahona2012building,
            title={Building and exploiting a corpus of dialog interactions between french speaking virtual and human agents},
            author={Barahona, Lina Maria Rojas and Lorenzo, Alejandra and Gardent, Claire},
            booktitle={The eighth international conference on Language Resources and Evaluation (LREC)},
            pages={1428--1435},
            year={2012}
            }"""
            ),
            url="",
        ),
        MiamConfig(
            name="maptask",
            description=textwrap.dedent(
                """\
            The HCRC MapTask Corpus was constructed through the verbal collaboration of participants
            in order to construct a map route. This corpus is small (27k utterances). As there is
            no standard train/dev/test split performance depends on the split."""
            ),
            text_features={
                "Speaker": "Speaker",
                "Utterance": "Utterance",
                "Dialogue_Act": "Dialogue_Act",
                "Dialogue_ID": "Dialogue_ID",
                "File_ID": "File_ID",
            },
            label_classes=[
                "acknowledge",
                "align",
                "check",
                "clarify",
                "explain",
                "instruct",
                "query_w",
                "query_yn",
                "ready",
                "reply_n",
                "reply_w",
                "reply_y",
            ],
            label_column="Dialogue_Act",
            data_url={
                "train": _URL + "/maptask/train.csv",
                "dev": _URL + "/maptask/dev.csv",
                "test": _URL + "/maptask/test.csv",
            },
            citation=textwrap.dedent(
                """\
            @inproceedings{thompson1993hcrc,
            title={The HCRC map task corpus: natural dialogue for speech recognition},
            author={Thompson, Henry S and Anderson, Anne H and Bard, Ellen Gurman and Doherty-Sneddon,
            Gwyneth and Newlands, Alison and Sotillo, Cathy},
            booktitle={HUMAN LANGUAGE TECHNOLOGY: Proceedings of a Workshop Held at Plainsboro, New Jersey, March 21-24, 1993},
            year={1993}
            }"""
            ),
            url="http://groups.inf.ed.ac.uk/maptask/",
        ),
        MiamConfig(
            name="vm2",
            description=textwrap.dedent(
                """\
            The VERBMOBIL corpus consist of transcripts of multi-party meetings hand-annotated with
            dialog acts. It is the second biggest dataset with around 110k utterances."""
            ),
            text_features={
                "Utterance": "Utterance",
                "Dialogue_Act": "Dialogue_Act",
                "Speaker": "Speaker",
                "Dialogue_ID": "Dialogue_ID",
            },
            label_classes=[
                "ACCEPT",
                "BACKCHANNEL",
                "BYE",
                "CLARIFY",
                "CLOSE",
                "COMMIT",
                "CONFIRM",
                "DEFER",
                "DELIBERATE",
                "DEVIATE_SCENARIO",
                "EXCLUDE",
                "EXPLAINED_REJECT",
                "FEEDBACK",
                "FEEDBACK_NEGATIVE",
                "FEEDBACK_POSITIVE",
                "GIVE_REASON",
                "GREET",
                "INFORM",
                "INIT",
                "INTRODUCE",
                "NOT_CLASSIFIABLE",
                "OFFER",
                "POLITENESS_FORMULA",
                "REJECT",
                "REQUEST",
                "REQUEST_CLARIFY",
                "REQUEST_COMMENT",
                "REQUEST_COMMIT",
                "REQUEST_SUGGEST",
                "SUGGEST",
                "THANK",
            ],
            label_column="Dialogue_Act",
            data_url={
                "train": _URL + "/vm2/train.csv",
                "dev": _URL + "/vm2/dev.csv",
                "test": _URL + "/vm2/test.csv",
            },
            citation=textwrap.dedent(
                """\
            @book{kay1992verbmobil,
            title={Verbmobil: A translation system for face-to-face dialog},
            author={Kay, Martin},
            year={1992},
            publisher={University of Chicago Press}
            }"""
            ),
            url="",
        ),
    ]

    def _info(self):
        features = {text_feature: datasets.Value("string") for text_feature in self.config.text_features.keys()}
        if self.config.label_classes:
            features["Label"] = datasets.features.ClassLabel(names=self.config.label_classes)
        features["Idx"] = datasets.Value("int32")
        return datasets.DatasetInfo(
            description=_MIAM_DESCRIPTION,
            features=datasets.Features(features),
            homepage=self.config.url,
            citation=self.config.citation + "\n" + _MIAM_CITATION,
        )

    def _split_generators(self, dl_manager):
        data_files = dl_manager.download(self.config.data_url)
        splits = []
        splits.append(
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                gen_kwargs={
                    "data_file": data_files["train"],
                    "split": "train",
                },
            )
        )
        splits.append(
            datasets.SplitGenerator(
                name=datasets.Split.VALIDATION,
                gen_kwargs={
                    "data_file": data_files["dev"],
                    "split": "dev",
                },
            )
        )
        splits.append(
            datasets.SplitGenerator(
                name=datasets.Split.TEST,
                gen_kwargs={
                    "data_file": data_files["test"],
                    "split": "test",
                },
            )
        )
        return splits

    def _generate_examples(self, data_file, split):
        df = pd.read_csv(data_file, delimiter=",", header=0, quotechar='"', dtype=str)[
            self.config.text_features.keys()
        ]

        rows = df.to_dict(orient="records")

        for n, row in enumerate(rows):
            example = row
            example["Idx"] = n

            if self.config.label_column in example:
                label = example[self.config.label_column]
                example["Label"] = label

            yield example["Idx"], example
