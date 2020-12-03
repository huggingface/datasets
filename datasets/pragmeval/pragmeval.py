# coding=utf-8
# Copyright 2020 The TensorFlow Datasets Authors and the HuggingFace Datasets Authors.
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
"""The General Language Understanding Evaluation (Pragmeval) benchmark."""

from __future__ import absolute_import, division, print_function

import csv
import os
import textwrap

import six

import datasets


_Pragmeval_CITATION = """\
@misc{sileo2019discoursebased,
      title={Discourse-Based Evaluation of Language Understanding},
      author={Damien Sileo and Tim Van-de-Cruys and Camille Pradel and Philippe Muller},
      year={2019},
      eprint={1907.08672},
      archivePrefix={arXiv},
      primaryClass={cs.CL}
}
"""

_Pragmeval_DESCRIPTION = """\
Evaluation of language understanding with a 11 datasets benchmark focusing on discourse and pragmatics
"""

DATA_URL = "https://www.dropbox.com/s/njcy51alkb17sft/pragmeval.zip?dl=1"


CITATION_DICT = {
    "pdtb": """
     @inproceedings{prasad-etal-2008-penn,
        title = "The {P}enn {D}iscourse {T}ree{B}ank 2.0.",
        author = "Prasad, Rashmi  and
          Dinesh, Nikhil  and
          Lee, Alan  and
          Miltsakaki, Eleni  and
          Robaldo, Livio  and
          Joshi, Aravind  and
          Webber, Bonnie",
        booktitle = "Proceedings of the Sixth International Conference on Language Resources and Evaluation ({LREC}'08)",
        month = may,
        year = "2008",
        address = "Marrakech, Morocco",
        publisher = "European Language Resources Association (ELRA)",
        url = "http://www.lrec-conf.org/proceedings/lrec2008/pdf/754_paper.pdf",
        abstract = "We present the second version of the Penn Discourse Treebank, PDTB-2.0, describing its lexically-grounded annotations of discourse relations and their two abstract object arguments over the 1 million word Wall Street Journal corpus. We describe all aspects of the annotation, including (a) the argument structure of discourse relations, (b) the sense annotation of the relations, and (c) the attribution of discourse relations and each of their arguments. We list the differences between PDTB-1.0 and PDTB-2.0. We present representative statistics for several aspects of the annotation in the corpus.",
    }
    """,
    "stac": """
    @inproceedings{asher-etal-2016-discourse,
        title = "Discourse Structure and Dialogue Acts in Multiparty Dialogue: the {STAC} Corpus",
        author = "Asher, Nicholas  and
          Hunter, Julie  and
          Morey, Mathieu  and
          Farah, Benamara  and
          Afantenos, Stergos",
        booktitle = "Proceedings of the Tenth International Conference on Language Resources and Evaluation ({LREC}'16)",
        month = may,
        year = "2016",
        address = "Portoro{\v{z}}, Slovenia",
        publisher = "European Language Resources Association (ELRA)",
        url = "https://www.aclweb.org/anthology/L16-1432",
        pages = "2721--2727",
        abstract = "This paper describes the STAC resource, a corpus of multi-party chats annotated for discourse structure in the style of SDRT (Asher and Lascarides, 2003; Lascarides and Asher, 2009). The main goal of the STAC project is to study the discourse structure of multi-party dialogues in order to understand the linguistic strategies adopted by interlocutors to achieve their conversational goals, especially when these goals are opposed. The STAC corpus is not only a rich source of data on strategic conversation, but also the first corpus that we are aware of that provides full discourse structures for multi-party dialogues. It has other remarkable features that make it an interesting resource for other topics: interleaved threads, creative language, and interactions between linguistic and extra-linguistic contexts.",
    }
    """,
    "gum": """
    @Article{Zeldes2017,
        author    = {Amir Zeldes},
        title     = {The {GUM} Corpus: Creating Multilayer Resources in the Classroom},
        journal   = {Language Resources and Evaluation},
        year      = {2017},
        volume    = {51},
        number    = {3},
        pages     = {581--612},
        doi       = {http://dx.doi.org/10.1007/s10579-016-9343-x}
     }
    """,
    "emergent": """
    @inproceedings{Ferreira2016EmergentAN,
      title={Emergent: a novel data-set for stance classification},
      author={William Ferreira and Andreas Vlachos},
      booktitle={HLT-NAACL},
      year={2016}
    }
    """,
    "switchboard": """
    @inproceedings{Godfrey:1992:STS:1895550.1895693,
     author = {Godfrey, John J. and Holliman, Edward C. and McDaniel, Jane},
     title = {SWITCHBOARD: Telephone Speech Corpus for Research and Development},
     booktitle = {Proceedings of the 1992 IEEE International Conference on Acoustics, Speech and Signal Processing - Volume 1},
     series = {ICASSP'92},
     year = {1992},
     isbn = {0-7803-0532-9},
     location = {San Francisco, California},
     pages = {517--520},
     numpages = {4},
     url = {http://dl.acm.org/citation.cfm?id=1895550.1895693},
     acmid = {1895693},
     publisher = {IEEE Computer Society},
     address = {Washington, DC, USA},
    }
    """,
    "mrda": """
    @inproceedings{shriberg2004icsi,
      title={The ICSI meeting recorder dialog act (MRDA) corpus},
      author={Shriberg, Elizabeth and Dhillon, Raj and Bhagat, Sonali and Ang, Jeremy and Carvey, Hannah},
      booktitle={Proceedings of the 5th SIGdial Workshop on Discourse and Dialogue at HLT-NAACL 2004},
      year={2004}
    }
    """,
    "persuasiveness": """
    @inproceedings{Persuasion2018Ng,
        title = "Give Me More Feedback: Annotating Argument Persuasiveness and Related Attributes in Student Essays",
        author = "Carlile, Winston  and
          Gurrapadi, Nishant  and
          Ke, Zixuan  and
          Ng, Vincent",
        booktitle = "Proceedings of the 56th Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers)",
        month = jul,
        year = "2018",
        address = "Melbourne, Australia",
        publisher = "Association for Computational Linguistics",
        url = "https://www.aclweb.org/anthology/P18-1058",
        pages = "621--631",
        abstract = "While argument persuasiveness is one of the most important dimensions of argumentative essay quality, it is relatively little studied in automated essay scoring research. Progress on scoring argument persuasiveness is hindered in part by the scarcity of annotated corpora. We present the first corpus of essays that are simultaneously annotated with argument components, argument persuasiveness scores, and attributes of argument components that impact an argument{'}s persuasiveness. This corpus could trigger the development of novel computational models concerning argument persuasiveness that provide useful feedback to students on why their arguments are (un)persuasive in addition to how persuasive they are.",
    }
    """,
    "sarcasm": """
    @InProceedings{OrabySarc,
        author = "Oraby, Shereen
        and Harrison, Vrindavan
        and Reed, Lena
        and Hernandez, Ernesto
        and Riloff, Ellen
        and Walker, Marilyn",
      title ="Creating and Characterizing a Diverse Corpus of Sarcasm in Dialogue",
      booktitle ="Proceedings of the 17th Annual Meeting of the Special Interest Group on      Discourse and Dialogue    ",
      year ="2016",
      publisher ="Association for Computational Linguistics",
      pages ="31--41",
      location ="Los Angeles",
      doi ="10.18653/v1/W16-3604",
      url ="http://aclweb.org/anthology/W16-3604"
    }
    """,
    "squinky": """
    @article{DBLP:journals/corr/Lahiri15,
      author    = {Shibamouli Lahiri},
      title     = {{SQUINKY! A Corpus of Sentence-level Formality, Informativeness,
                   and Implicature}},
      journal   = {CoRR},
      volume    = {abs/1506.02306},
      year      = {2015},
      url       = {http://arxiv.org/abs/1506.02306},
      timestamp = {Wed, 01 Jul 2015 15:10:24 +0200},
      biburl    = {http://dblp.uni-trier.de/rec/bib/journals/corr/Lahiri15},
      bibsource = {dblp computer science bibliography, http://dblp.org}
    }
    """,
    "verifiability": """@inproceedings{park2014identifying,
      title={Identifying appropriate support for propositions in online user comments},
      author={Park, Joonsuk and Cardie, Claire},
      booktitle={Proceedings of the first workshop on argumentation mining},
      pages={29--38},
      year={2014}
    }""",
    "emobank": """"
    @inproceedings{buechel-hahn-2017-emobank,
        title = "{E}mo{B}ank: Studying the Impact of Annotation Perspective and Representation Format on Dimensional Emotion Analysis",
        author = "Buechel, Sven  and
          Hahn, Udo",
        booktitle = "Proceedings of the 15th Conference of the {E}uropean Chapter of the Association for Computational Linguistics: Volume 2, Short Papers",
        month = apr,
        year = "2017",
        address = "Valencia, Spain",
        publisher = "Association for Computational Linguistics",
        url = "https://www.aclweb.org/anthology/E17-2092",
        pages = "578--585",
        abstract = "We describe EmoBank, a corpus of 10k English sentences balancing multiple genres, which we annotated with dimensional emotion metadata in the Valence-Arousal-Dominance (VAD) representation format. EmoBank excels with a bi-perspectival and bi-representational design. On the one hand, we distinguish between writer{'}s and reader{'}s emotions, on the other hand, a subset of the corpus complements dimensional VAD annotations with categorical ones based on Basic Emotions. We find evidence for the supremacy of the reader{'}s perspective in terms of IAA and rating intensity, and achieve close-to-human performance when mapping between dimensional and categorical formats.",
    }
    """,
}

TASK_TO_LABELS = {
    "verifiability": ["experiential", "unverifiable", "non-experiential"],
    "emobank-arousal": ["low", "high"],
    "switchboard": [
        "Response Acknowledgement",
        "Uninterpretable",
        "Or-Clause",
        "Reject",
        "Statement-non-opinion",
        "3rd-party-talk",
        "Repeat-phrase",
        "Hold Before Answer/Agreement",
        "Signal-non-understanding",
        "Offers, Options Commits",
        "Agree/Accept",
        "Dispreferred Answers",
        "Hedge",
        "Action-directive",
        "Tag-Question",
        "Self-talk",
        "Yes-No-Question",
        "Rhetorical-Question",
        "No Answers",
        "Open-Question",
        "Conventional-closing",
        "Other Answers",
        "Acknowledge (Backchannel)",
        "Wh-Question",
        "Declarative Wh-Question",
        "Thanking",
        "Yes Answers",
        "Affirmative Non-yes Answers",
        "Declarative Yes-No-Question",
        "Backchannel in Question Form",
        "Apology",
        "Downplayer",
        "Conventional-opening",
        "Collaborative Completion",
        "Summarize/Reformulate",
        "Negative Non-no Answers",
        "Statement-opinion",
        "Appreciation",
        "Other",
        "Quotation",
        "Maybe/Accept-part",
    ],
    "persuasiveness-eloquence": ["low", "high"],
    "mrda": [
        "Declarative-Question",
        "Statement",
        "Reject",
        "Or-Clause",
        "3rd-party-talk",
        "Continuer",
        "Hold Before Answer/Agreement",
        "Assessment/Appreciation",
        "Signal-non-understanding",
        "Floor Holder",
        "Sympathy",
        "Dispreferred Answers",
        "Reformulate/Summarize",
        "Exclamation",
        "Interrupted/Abandoned/Uninterpretable",
        "Expansions of y/n Answers",
        "Action-directive",
        "Tag-Question",
        "Accept",
        "Rhetorical-question Continue",
        "Self-talk",
        "Rhetorical-Question",
        "Yes-No-question",
        "Open-Question",
        "Rising Tone",
        "Other Answers",
        "Commit",
        "Wh-Question",
        "Repeat",
        "Follow Me",
        "Thanking",
        "Offer",
        "About-task",
        "Reject-part",
        "Affirmative Non-yes Answers",
        "Apology",
        "Downplayer",
        "Humorous Material",
        "Accept-part",
        "Collaborative Completion",
        "Mimic Other",
        "Understanding Check",
        "Misspeak Self-Correction",
        "Or-Question",
        "Topic Change",
        "Negative Non-no Answers",
        "Floor Grabber",
        "Correct-misspeaking",
        "Maybe",
        "Acknowledge-answer",
        "Defending/Explanation",
    ],
    "gum": [
        "preparation",
        "evaluation",
        "circumstance",
        "solutionhood",
        "justify",
        "result",
        "evidence",
        "purpose",
        "concession",
        "elaboration",
        "background",
        "condition",
        "cause",
        "restatement",
        "motivation",
        "antithesis",
        "no_relation",
    ],
    "emergent": ["observing", "for", "against"],
    "persuasiveness-relevance": ["low", "high"],
    "persuasiveness-specificity": ["low", "high"],
    "persuasiveness-strength": ["low", "high"],
    "emobank-dominance": ["low", "high"],
    "squinky-implicature": ["low", "high"],
    "sarcasm": ["notsarc", "sarc"],
    "squinky-formality": ["low", "high"],
    "stac": [
        "Comment",
        "Contrast",
        "Q_Elab",
        "Parallel",
        "Explanation",
        "Narration",
        "Continuation",
        "Result",
        "Acknowledgement",
        "Alternation",
        "Question_answer_pair",
        "Correction",
        "Clarification_question",
        "Conditional",
        "Sequence",
        "Elaboration",
        "Background",
        "no_relation",
    ],
    "pdtb": [
        "Synchrony",
        "Contrast",
        "Asynchronous",
        "Conjunction",
        "List",
        "Condition",
        "Pragmatic concession",
        "Restatement",
        "Pragmatic cause",
        "Alternative",
        "Pragmatic condition",
        "Pragmatic contrast",
        "Instantiation",
        "Exception",
        "Cause",
        "Concession",
    ],
    "persuasiveness-premisetype": [
        "testimony",
        "warrant",
        "invented_instance",
        "common_knowledge",
        "statistics",
        "analogy",
        "definition",
        "real_example",
    ],
    "squinky-informativeness": ["low", "high"],
    "persuasiveness-claimtype": ["Value", "Fact", "Policy"],
    "emobank-valence": ["low", "high"],
}


def get_labels(task):
    return TASK_TO_LABELS[task]


class PragmevalConfig(datasets.BuilderConfig):
    """BuilderConfig for Pragmeval."""

    def __init__(
        self,
        text_features,
        label_classes=None,
        process_label=lambda x: x,
        **kwargs,
    ):
        """BuilderConfig for Pragmeval.
        Args:
          text_features: `dict[string, string]`, map from the name of the feature
            dict for each text field to the name of the column in the tsv file
          label_column: `string`, name of the column in the tsv file corresponding
            to the label
          data_url: `string`, url to download the zip file from
          data_dir: `string`, the path to the folder containing the tsv files in the
            downloaded zip
          citation: `string`, citation for the data set
          url: `string`, url for information about the data set
          label_classes: `list[string]`, the list of classes if the label is
            categorical. If not provided, then the label will be of type
            `datasets.Value('float32')`.
          process_label: `Function[string, any]`, function  taking in the raw value
            of the label and processing it to the form required by the label feature
          **kwargs: keyword arguments forwarded to super.
        """

        super(PragmevalConfig, self).__init__(version=datasets.Version("1.0.0", ""), **kwargs)

        self.text_features = text_features
        self.label_column = "label"
        self.label_classes = get_labels(self.name)
        self.data_url = DATA_URL
        self.data_dir = os.path.join("pragmeval", self.name)
        self.citation = textwrap.dedent(CITATION_DICT[self.name.split("-")[0]])
        self.process_label = process_label
        self.description = ""
        self.url = ""


class Pragmeval(datasets.GeneratorBasedBuilder):

    """The General Language Understanding Evaluation (Pragmeval) benchmark."""

    BUILDER_CONFIG_CLASS = PragmevalConfig

    BUILDER_CONFIGS = [
        PragmevalConfig(
            name="verifiability",
            text_features={"sentence": "sentence"},
        ),
        PragmevalConfig(
            name="emobank-arousal",
            text_features={"sentence": "sentence"},
        ),
        PragmevalConfig(
            name="switchboard",
            text_features={"sentence": "sentence"},
        ),
        PragmevalConfig(
            name="persuasiveness-eloquence",
            text_features={"sentence1": "sentence1", "sentence2": "sentence2"},
        ),
        PragmevalConfig(
            name="mrda",
            text_features={"sentence": "sentence"},
        ),
        PragmevalConfig(
            name="gum",
            text_features={"sentence1": "sentence1", "sentence2": "sentence2"},
        ),
        PragmevalConfig(
            name="emergent",
            text_features={"sentence1": "sentence1", "sentence2": "sentence2"},
        ),
        PragmevalConfig(
            name="persuasiveness-relevance",
            text_features={"sentence1": "sentence1", "sentence2": "sentence2"},
        ),
        PragmevalConfig(
            name="persuasiveness-specificity",
            text_features={"sentence1": "sentence1", "sentence2": "sentence2"},
        ),
        PragmevalConfig(
            name="persuasiveness-strength",
            text_features={"sentence1": "sentence1", "sentence2": "sentence2"},
        ),
        PragmevalConfig(
            name="emobank-dominance",
            text_features={"sentence": "sentence"},
        ),
        PragmevalConfig(
            name="squinky-implicature",
            text_features={"sentence": "sentence"},
        ),
        PragmevalConfig(
            name="sarcasm",
            text_features={"sentence1": "sentence1", "sentence2": "sentence2"},
        ),
        PragmevalConfig(
            name="squinky-formality",
            text_features={"sentence": "sentence"},
        ),
        PragmevalConfig(
            name="stac",
            text_features={"sentence1": "sentence1", "sentence2": "sentence2"},
        ),
        PragmevalConfig(
            name="pdtb",
            text_features={"sentence1": "sentence1", "sentence2": "sentence2"},
        ),
        PragmevalConfig(
            name="persuasiveness-premisetype",
            text_features={"sentence1": "sentence1", "sentence2": "sentence2"},
        ),
        PragmevalConfig(
            name="squinky-informativeness",
            text_features={"sentence": "sentence"},
        ),
        PragmevalConfig(
            name="persuasiveness-claimtype",
            text_features={"sentence1": "sentence1", "sentence2": "sentence2"},
        ),
        PragmevalConfig(
            name="emobank-valence",
            text_features={"sentence": "sentence"},
        ),
    ]

    def _info(self):
        features = {text_feature: datasets.Value("string") for text_feature in six.iterkeys(self.config.text_features)}
        if self.config.label_classes:
            features["label"] = datasets.features.ClassLabel(names=self.config.label_classes)
        else:
            features["label"] = datasets.Value("float32")
        features["idx"] = datasets.Value("int32")
        return datasets.DatasetInfo(
            description=_Pragmeval_DESCRIPTION,
            features=datasets.Features(features),
            homepage=self.config.url,
            citation=self.config.citation + "\n" + _Pragmeval_CITATION,
        )

    def _split_generators(self, dl_manager):
        dl_dir = dl_manager.download_and_extract(self.config.data_url)
        data_dir = os.path.join(dl_dir, self.config.data_dir)

        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                gen_kwargs={
                    "data_file": os.path.join(data_dir or "", "train.tsv"),
                    "split": "train",
                },
            ),
            datasets.SplitGenerator(
                name=datasets.Split.VALIDATION,
                gen_kwargs={
                    "data_file": os.path.join(data_dir or "", "dev.tsv"),
                    "split": "dev",
                },
            ),
            datasets.SplitGenerator(
                name=datasets.Split.TEST,
                gen_kwargs={
                    "data_file": os.path.join(data_dir or "", "test.tsv"),
                    "split": "test",
                },
            ),
        ]

    def _generate_examples(self, data_file, split):

        process_label = self.config.process_label
        label_classes = self.config.label_classes

        with open(data_file, encoding="utf8") as f:
            reader = csv.DictReader(f, delimiter="\t", quoting=csv.QUOTE_NONE)

            for n, row in enumerate(reader):

                example = {feat: row[col] for feat, col in six.iteritems(self.config.text_features)}
                example["idx"] = n

                if self.config.label_column in row:
                    label = row[self.config.label_column]
                    if label_classes and label not in label_classes:
                        label = int(label) if label else None
                    example["label"] = process_label(label)
                else:
                    example["label"] = process_label(-1)
                yield example["idx"], example
