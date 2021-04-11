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
"""The Sequence labellIng evaLuatIon benChmark fOr spoken laNguagE (SILICONE) benchmark."""


import textwrap

import pandas as pd

import datasets


_SILICONE_CITATION = """\
@inproceedings{chapuis-etal-2020-hierarchical,
    title = "Hierarchical Pre-training for Sequence Labelling in Spoken Dialog",
    author = "Chapuis, Emile  and
      Colombo, Pierre  and
      Manica, Matteo  and
      Labeau, Matthieu  and
      Clavel, Chlo{\'e}",
    booktitle = "Findings of the Association for Computational Linguistics: EMNLP 2020",
    month = nov,
    year = "2020",
    address = "Online",
    publisher = "Association for Computational Linguistics",
    url = "https://www.aclweb.org/anthology/2020.findings-emnlp.239",
    doi = "10.18653/v1/2020.findings-emnlp.239",
    pages = "2636--2648",
    abstract = "Sequence labelling tasks like Dialog Act and Emotion/Sentiment identification are a
        key component of spoken dialog systems. In this work, we propose a new approach to learn
        generic representations adapted to spoken dialog, which we evaluate on a new benchmark we
        call Sequence labellIng evaLuatIon benChmark fOr spoken laNguagE benchmark (SILICONE).
        SILICONE is model-agnostic and contains 10 different datasets of various sizes.
        We obtain our representations with a hierarchical encoder based on transformer architectures,
        for which we extend two well-known pre-training objectives. Pre-training is performed on
        OpenSubtitles: a large corpus of spoken dialog containing over 2.3 billion of tokens. We
        demonstrate how hierarchical encoders achieve competitive results with consistently fewer
        parameters compared to state-of-the-art models and we show their importance for both
        pre-training and fine-tuning.",
}
"""

_SILICONE_DESCRIPTION = """\
The Sequence labellIng evaLuatIon benChmark fOr spoken laNguagE (SILICONE) benchmark is a collection
 of resources for training, evaluating, and analyzing natural language understanding systems
 specifically designed for spoken language. All datasets are in the English language and cover a
 variety of domains including daily life, scripted scenarios, joint task completion, phone call
 conversations, and televsion dialogue. Some datasets additionally include emotion and/or sentimant
 labels.
"""

_URL = "https://raw.githubusercontent.com/eusip/SILICONE-benchmark/main"

SWDA_DA_DESCRIPTION = {
    "sd": "Statement-non-opinion",
    "b": "Acknowledge (Backchannel)",
    "sv": "Statement-opinion",
    "%": "Uninterpretable",
    "aa": "Agree/Accept",
    "ba": "Appreciation",
    "fc": "Conventional-closing",
    "qw": "Wh-Question",
    "nn": "No Answers",
    "bk": "Response Acknowledgement",
    "h": "Hedge",
    "qy^d": "Declarative Yes-No-Question",
    "bh": "Backchannel in Question Form",
    "^q": "Quotation",
    "bf": "Summarize/Reformulate",
    'fo_o_fw_"_by_bc': "Other",
    'fo_o_fw_by_bc_"': "Other",
    "na": "Affirmative Non-yes Answers",
    "ad": "Action-directive",
    "^2": "Collaborative Completion",
    "b^m": "Repeat-phrase",
    "qo": "Open-Question",
    "qh": "Rhetorical-Question",
    "^h": "Hold Before Answer/Agreement",
    "ar": "Reject",
    "ng": "Negative Non-no Answers",
    "br": "Signal-non-understanding",
    "no": "Other Answers",
    "fp": "Conventional-opening",
    "qrr": "Or-Clause",
    "arp_nd": "Dispreferred Answers",
    "t3": "3rd-party-talk",
    "oo_co_cc": "Offers, Options Commits",
    "aap_am": "Maybe/Accept-part",
    "t1": "Downplayer",
    "bd": "Self-talk",
    "^g": "Tag-Question",
    "qw^d": "Declarative Wh-Question",
    "fa": "Apology",
    "ft": "Thanking",
    "+": "Unknown",
    "x": "Unknown",
    "ny": "Unknown",
    "sv_fx": "Unknown",
    "qy_qr": "Unknown",
    "ba_fe": "Unknown",
}

MRDA_DA_DESCRIPTION = {
    "s": "Statement/Subjective Statement",
    "d": "Declarative Question",
    "b": "Backchannel",
    "f": '"Follow-me"',
    "q": "Question",
}

IEMOCAP_E_DESCRIPTION = {
    "ang": "Anger",
    "dis": "Disgust",
    "exc": "Excitement",
    "fea": "Fear",
    "fru": "Frustration",
    "hap": "Happiness",
    "neu": "Neutral",
    "oth": "Other",
    "sad": "Sadness",
    "sur": "Surprise",
    "xxx": "Unknown",
}


class SiliconeConfig(datasets.BuilderConfig):
    """BuilderConfig for SILICONE."""

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
        """BuilderConfig for SILICONE.
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
        super(SiliconeConfig, self).__init__(version=datasets.Version("1.0.0", ""), **kwargs)
        self.text_features = text_features
        self.label_column = label_column
        self.label_classes = label_classes
        self.data_url = data_url
        self.citation = citation
        self.url = url


class Silicone(datasets.GeneratorBasedBuilder):
    """The Sequence labellIng evaLuatIon benChmark fOr spoken laNguagE (SILICONE) benchmark."""

    BUILDER_CONFIGS = [
        SiliconeConfig(
            name="dyda_da",
            description=textwrap.dedent(
                """\
            The DailyDialog Act Corpus contains multi-turn dialogues and is supposed to reflect daily
            communication by covering topics about daily life. The dataset is manually labelled with
             dialog act and emotions. It is the third biggest corpus of SILICONE with 102k utterances."""
            ),
            text_features={
                "Utterance": "Utterance",
                "Dialogue_Act": "Dialogue_Act",
                "Dialogue_ID": "Dialogue_ID",
            },
            label_classes=["commissive", "directive", "inform", "question"],
            label_column="Dialogue_Act",
            data_url={
                "train": _URL + "/dyda/train.csv",
                "dev": _URL + "/dyda/dev.csv",
                "test": _URL + "/dyda/test.csv",
            },
            citation=textwrap.dedent(
                """\
            @InProceedings{li2017dailydialog,
            author = {Li, Yanran and Su, Hui and Shen, Xiaoyu and Li, Wenjie and Cao, Ziqiang and Niu, Shuzi},
            title = {DailyDialog: A Manually Labelled Multi-turn Dialogue Dataset},
            booktitle = {Proceedings of The 8th International Joint Conference on Natural Language Processing (IJCNLP 2017)},
            year = {2017}
            }"""
            ),
            url="http://yanran.li/dailydialog.html",
        ),
        SiliconeConfig(
            name="dyda_e",
            description=textwrap.dedent(
                """\
            The DailyDialog Act Corpus contains multi-turn dialogues and is supposed to reflect daily
            communication by covering topics about daily life. The dataset is manually labelled with
             dialog act and emotions. It is the third biggest corpus of SILICONE with 102k utterances."""
            ),
            text_features={
                "Utterance": "Utterance",
                "Emotion": "Emotion",
                "Dialogue_ID": "Dialogue_ID",
            },
            label_classes=["anger", "disgust", "fear", "happiness", "no emotion", "sadness", "surprise"],
            label_column="Emotion",
            data_url={
                "train": _URL + "/dyda/train.csv",
                "dev": _URL + "/dyda/dev.csv",
                "test": _URL + "/dyda/test.csv",
            },
            citation=textwrap.dedent(
                """\
            @InProceedings{li2017dailydialog,
            author = {Li, Yanran and Su, Hui and Shen, Xiaoyu and Li, Wenjie and Cao, Ziqiang and Niu, Shuzi},
            title = {DailyDialog: A Manually Labelled Multi-turn Dialogue Dataset},
            booktitle = {Proceedings of The 8th International Joint Conference on Natural Language Processing (IJCNLP 2017)},
            year = {2017}
            }"""
            ),
            url="http://yanran.li/dailydialog.html",
        ),
        SiliconeConfig(
            name="iemocap",
            description=textwrap.dedent(
                """\
            The IEMOCAP database is a multi-modal database of ten speakers. It consists of dyadic
            sessions where actors perform improvisations or scripted scenarios. Emotion categories
            are: anger, happiness, sadness, neutral, excitement, frustration, fear, surprise, and other.
            There is no official split of this dataset."""
            ),
            text_features={
                "Dialogue_ID": "Dialogue_ID",
                "Utterance_ID": "Utterance_ID",
                "Utterance": "Utterance",
                "Emotion": "Emotion",
            },
            label_classes=list(IEMOCAP_E_DESCRIPTION.keys()),
            label_column="Emotion",
            data_url={
                "train": _URL + "/iemocap/train.csv",
                "dev": _URL + "/iemocap/dev.csv",
                "test": _URL + "/iemocap/test.csv",
            },
            citation=textwrap.dedent(
                """\
            @article{busso2008iemocap,
            title={IEMOCAP: Interactive emotional dyadic motion capture database},
            author={Busso, Carlos and Bulut, Murtaza and Lee, Chi-Chun and Kazemzadeh, Abe and Mower,
            Emily and Kim, Samuel and Chang, Jeannette N and Lee, Sungbok and Narayanan, Shrikanth S},
            journal={Language resources and evaluation},
            volume={42},
            number={4},
            pages={335},
            year={2008},
            publisher={Springer}
            }"""
            ),
            url="https://sail.usc.edu/iemocap/",
        ),
        SiliconeConfig(
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
                "train": _URL + "/maptask/train.txt",
                "dev": _URL + "/maptask/dev.txt",
                "test": _URL + "/maptask/test.txt",
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
        SiliconeConfig(
            name="meld_e",
            description=textwrap.dedent(
                """\
            The Multimodal EmotionLines Dataset enhances and extends the EmotionLines dataset where
            multiple speakers participate in the dialogue."""
            ),
            text_features={
                "Utterance": "Utterance",
                "Speaker": "Speaker",
                "Emotion": "Emotion",
                "Dialogue_ID": "Dialogue_ID",
                "Utterance_ID": "Utterance_ID",
            },
            label_classes=["anger", "disgust", "fear", "joy", "neutral", "sadness", "surprise"],
            label_column="Emotion",
            data_url={
                "train": _URL + "/meld/train.csv",
                "dev": _URL + "/meld/dev.csv",
                "test": _URL + "/meld/test.csv",
            },
            citation=textwrap.dedent(
                """\
            @article{chen2018emotionlines,
            title={Emotionlines: An emotion corpus of multi-party conversations},
            author={Chen, Sheng-Yeh and Hsu, Chao-Chun and Kuo, Chuan-Chun and Ku, Lun-Wei and others},
            journal={arXiv preprint arXiv:1802.08379},
            year={2018}
            }"""
            ),
            url="https://affective-meld.github.io/",
        ),
        SiliconeConfig(
            name="meld_s",
            description=textwrap.dedent(
                """\
            The Multimodal EmotionLines Dataset enhances and extends the EmotionLines dataset where
            multiple speakers participate in the dialogue."""
            ),
            text_features={
                "Utterance": "Utterance",
                "Speaker": "Speaker",
                "Sentiment": "Sentiment",
                "Dialogue_ID": "Dialogue_ID",
                "Utterance_ID": "Utterance_ID",
            },
            label_classes=["negative", "neutral", "positive"],
            label_column="Sentiment",
            data_url={
                "train": _URL + "/meld/train.csv",
                "dev": _URL + "/meld/dev.csv",
                "test": _URL + "/meld/test.csv",
            },
            citation=textwrap.dedent(
                """\
            @article{chen2018emotionlines,
            title={Emotionlines: An emotion corpus of multi-party conversations},
            author={Chen, Sheng-Yeh and Hsu, Chao-Chun and Kuo, Chuan-Chun and Ku, Lun-Wei and others},
            journal={arXiv preprint arXiv:1802.08379},
            year={2018}
            }"""
            ),
            url="https://affective-meld.github.io/",
        ),
        SiliconeConfig(
            name="mrda",
            description=textwrap.dedent(
                """\
            ICSI MRDA Corpus consist of transcripts of multi-party meetings hand-annotated with dialog
            acts. It is the second biggest dataset with around 110k utterances."""
            ),
            text_features={
                "Utterance_ID": "Utterance_ID",
                "Dialogue_Act": "Dialogue_Act",
                "Channel_ID": "Channel_ID",
                "Speaker": "Speaker",
                "Dialogue_ID": "Dialogue_ID",
                "Utterance": "Utterance",
            },
            label_classes=list(MRDA_DA_DESCRIPTION.keys()),
            label_column="Dialogue_Act",
            data_url={
                "train": _URL + "/mrda/train.csv",
                "dev": _URL + "/mrda/dev.csv",
                "test": _URL + "/mrda/test.csv",
            },
            citation=textwrap.dedent(
                """\
            @techreport{shriberg2004icsi,
            title={The ICSI meeting recorder dialog act (MRDA) corpus},
            author={Shriberg, Elizabeth and Dhillon, Raj and Bhagat, Sonali and Ang, Jeremy and Carvey, Hannah},
            year={2004},
            institution={INTERNATIONAL COMPUTER SCIENCE INST BERKELEY CA}
            }"""
            ),
            url="https://www.aclweb.org/anthology/W04-2319",
        ),
        SiliconeConfig(
            name="oasis",
            description=textwrap.dedent(
                """\
            The Bt Oasis Corpus (Oasis) contains the transcripts of live calls made to the BT and
            operator services. This corpus is rather small (15k utterances). There is no standard
            train/dev/test split."""
            ),
            text_features={
                "Speaker": "Speaker",
                "Utterance": "Utterance",
                "Dialogue_Act": "Dialogue_Act",
            },
            label_classes=[
                "accept",
                "ackn",
                "answ",
                "answElab",
                "appreciate",
                "backch",
                "bye",
                "complete",
                "confirm",
                "correct",
                "direct",
                "directElab",
                "echo",
                "exclaim",
                "expressOpinion",
                "expressPossibility",
                "expressRegret",
                "expressWish",
                "greet",
                "hold",
                "identifySelf",
                "inform",
                "informCont",
                "informDisc",
                "informIntent",
                "init",
                "negate",
                "offer",
                "pardon",
                "raiseIssue",
                "refer",
                "refuse",
                "reqDirect",
                "reqInfo",
                "reqModal",
                "selfTalk",
                "suggest",
                "thank",
                "informIntent-hold",
                "correctSelf",
                "expressRegret-inform",
                "thank-identifySelf",
            ],
            label_column="Dialogue_Act",
            data_url={
                "train": _URL + "/oasis/train.txt",
                "dev": _URL + "/oasis/dev.txt",
                "test": _URL + "/oasis/test.txt",
            },
            citation=textwrap.dedent(
                """\
            @inproceedings{leech2003generic,
            title={Generic speech act annotation for task-oriented dialogues},
            author={Leech, Geoffrey and Weisser, Martin},
            booktitle={Proceedings of the corpus linguistics 2003 conference},
            volume={16},
            pages={441--446},
            year={2003},
            organization={Lancaster: Lancaster University}
            }"""
            ),
            url="http://groups.inf.ed.ac.uk/oasis/",
        ),
        SiliconeConfig(
            name="sem",
            description=textwrap.dedent(
                """\
            The SEMAINE database comes from the Sustained Emotionally coloured Human-Machine Interaction
            using Nonverbal Expression project. This dataset has been annotated on three sentiments
            labels: positive, negative and neutral. It is built on Multimodal Wizard of Oz experiment
            where participants held conversations with an operator who adopted various roles designed
            to evoke emotional reactions. There is no official split on this dataset."""
            ),
            text_features={
                "Utterance": "Utterance",
                "NbPairInSession": "NbPairInSession",
                "Dialogue_ID": "Dialogue_ID",
                "SpeechTurn": "SpeechTurn",
                "Speaker": "Speaker",
                "Sentiment": "Sentiment",
            },
            label_classes=["Negative", "Neutral", "Positive"],
            label_column="Sentiment",
            data_url={
                "train": _URL + "/sem/train.csv",
                "dev": _URL + "/sem/dev.csv",
                "test": _URL + "/sem/test.csv",
            },
            citation=textwrap.dedent(
                """\
            @article{mckeown2011semaine,
            title={The semaine database: Annotated multimodal records of emotionally colored conversations
            between a person and a limited agent},
            author={McKeown, Gary and Valstar, Michel and Cowie, Roddy and Pantic, Maja and Schroder, Marc},
            journal={IEEE transactions on affective computing},
            volume={3},
            number={1},
            pages={5--17},
            year={2011},
            publisher={IEEE}
            }"""
            ),
            url="https://ieeexplore.ieee.org/document/5959155",
        ),
        SiliconeConfig(
            name="swda",
            description=textwrap.dedent(
                """\
            Switchboard Dialog Act Corpus (SwDA) is a telephone speech corpus consisting of two-sided
            telephone conversations with provided topics. This dataset includes additional features
            such as speaker id and topic information."""
            ),
            text_features={
                "Utterance": "Utterance",
                "Dialogue_Act": "Dialogue_Act",
                "From_Caller": "From_Caller",
                "To_Caller": "To_Caller",
                "Topic": "Topic",
                "Dialogue_ID": "Dialogue_ID",
                "Conv_ID": "Conv_ID",
            },
            label_classes=list(SWDA_DA_DESCRIPTION.keys()),
            label_column="Dialogue_Act",
            data_url={
                "train": _URL + "/swda/train.csv",
                "dev": _URL + "/swda/dev.csv",
                "test": _URL + "/swda/test.csv",
            },
            citation=textwrap.dedent(
                """\
            @article{stolcke2000dialogue,
            title={Dialogue act modeling for automatic tagging and recognition of conversational speech},
            author={Stolcke, Andreas and Ries, Klaus and Coccaro, Noah and Shriberg, Elizabeth and
            Bates, Rebecca and Jurafsky, Daniel and Taylor, Paul and Martin, Rachel and Ess-Dykema,
            Carol Van and Meteer, Marie},
            journal={Computational linguistics},
            volume={26},
            number={3},
            pages={339--373},
            year={2000},
            publisher={MIT Press}
            }"""
            ),
            url="https://web.stanford.edu/~jurafsky/ws97/",
        ),
    ]

    def _info(self):
        features = {text_feature: datasets.Value("string") for text_feature in self.config.text_features.keys()}
        if self.config.label_classes:
            features["Label"] = datasets.features.ClassLabel(names=self.config.label_classes)
        features["Idx"] = datasets.Value("int32")
        return datasets.DatasetInfo(
            description=_SILICONE_DESCRIPTION,
            features=datasets.Features(features),
            homepage=self.config.url,
            citation=self.config.citation + "\n" + _SILICONE_CITATION,
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
        if self.config.name not in ("maptask", "iemocap", "oasis"):
            df = pd.read_csv(data_file, delimiter=",", header=0, quotechar='"', dtype=str)[
                self.config.text_features.keys()
            ]

        if self.config.name == "iemocap":
            df = pd.read_csv(
                data_file,
                delimiter=",",
                header=0,
                quotechar='"',
                names=["Dialogue_ID", "Utterance_ID", "Utterance", "Emotion", "Valence", "Activation", "Dominance"],
                dtype=str,
            )[self.config.text_features.keys()]

        if self.config.name in ("maptask", "oasis"):
            df = pd.read_csv(data_file, delimiter="|", names=["Speaker", "Utterance", "Dialogue_Act"], dtype=str)[
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
