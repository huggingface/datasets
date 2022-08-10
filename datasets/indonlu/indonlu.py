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
"""The IndoNLU benchmark is a collection of resources for training, evaluating, and analyzing natural language understanding systems for Bahasa Indonesia"""


import ast
import csv
import textwrap

import datasets


_INDONLU_CITATION = """\
@inproceedings{wilie2020indonlu,
title = {{IndoNLU}: Benchmark and Resources for Evaluating Indonesian Natural Language Understanding},
authors={Bryan Wilie and Karissa Vincentio and Genta Indra Winata and Samuel Cahyawijaya and X. Li and Zhi Yuan Lim and S. Soleman and R. Mahendra and Pascale Fung and Syafri Bahar and A. Purwarianti},
booktitle={Proceedings of the 1st Conference of the Asia-Pacific Chapter of the Association for Computational Linguistics and the 10th International Joint Conference on Natural Language Processing},
year={2020}
}
"""

_INDONLU_DESCRIPTION = """\
The IndoNLU benchmark is a collection of resources for training, evaluating, \
and analyzing natural language understanding systems for Bahasa Indonesia.
"""

_INDONLU_HOMEPAGE = "https://www.indobenchmark.com/"

_INDONLU_LICENSE = "https://raw.githubusercontent.com/indobenchmark/indonlu/master/LICENSE"


class IndonluConfig(datasets.BuilderConfig):
    """BuilderConfig for IndoNLU"""

    def __init__(
        self,
        text_features,
        label_column,
        label_classes,
        train_url,
        valid_url,
        test_url,
        citation,
        **kwargs,
    ):
        """BuilderConfig for IndoNLU.

        Args:
          text_features: `dict[string, string]`, map from the name of the feature
            dict for each text field to the name of the column in the txt/csv/tsv file
          label_column: `string`, name of the column in the txt/csv/tsv file corresponding
            to the label
          label_classes: `list[string]`, the list of classes if the label is categorical
          train_url: `string`, url to train file from
          valid_url: `string`, url to valid file from
          test_url: `string`, url to test file from
          citation: `string`, citation for the data set
          **kwargs: keyword arguments forwarded to super.
        """
        super(IndonluConfig, self).__init__(version=datasets.Version("1.0.0", ""), **kwargs)
        self.text_features = text_features
        self.label_column = label_column
        self.label_classes = label_classes
        self.train_url = train_url
        self.valid_url = valid_url
        self.test_url = test_url
        self.citation = citation


class Indonlu(datasets.GeneratorBasedBuilder):
    """Indonesian Natural Language Understanding (IndoNLU) benchmark"""

    BUILDER_CONFIGS = [
        IndonluConfig(
            name="emot",
            description=textwrap.dedent(
                """\
            An emotion classification dataset collected from the social media
            platform Twitter (Saputri et al., 2018). The dataset consists of
            around 4000 Indonesian colloquial language tweets, covering five
            different emotion labels: sadness, anger, love, fear, and happy."""
            ),
            text_features={"tweet": "tweet"},
            # label classes sorted refer to https://github.com/indobenchmark/indonlu/blob/master/utils/data_utils.py
            label_classes=["sadness", "anger", "love", "fear", "happy"],
            label_column="label",
            train_url="https://raw.githubusercontent.com/indobenchmark/indonlu/master/dataset/emot_emotion-twitter/train_preprocess.csv",
            valid_url="https://raw.githubusercontent.com/indobenchmark/indonlu/master/dataset/emot_emotion-twitter/valid_preprocess.csv",
            test_url="https://raw.githubusercontent.com/indobenchmark/indonlu/master/dataset/emot_emotion-twitter/test_preprocess_masked_label.csv",
            citation=textwrap.dedent(
                """\
            @inproceedings{saputri2018emotion,
              title={Emotion Classification on Indonesian Twitter Dataset},
              author={Mei Silviana Saputri, Rahmad Mahendra, and Mirna Adriani},
              booktitle={Proceedings of the 2018 International Conference on Asian Language Processing(IALP)},
              pages={90--95},
              year={2018},
              organization={IEEE}
            }"""
            ),
        ),
        IndonluConfig(
            name="smsa",
            description=textwrap.dedent(
                """\
            This sentence-level sentiment analysis dataset (Purwarianti and Crisdayanti, 2019)
            is a collection of comments and reviews in Indonesian obtained from multiple online
            platforms. The text was crawled and then annotated by several Indonesian linguists
            to construct this dataset. There are three possible sentiments on the SmSA
            dataset: positive, negative, and neutral."""
            ),
            text_features={"text": "text"},
            # label classes sorted refer to https://github.com/indobenchmark/indonlu/blob/master/utils/data_utils.py
            label_classes=["positive", "neutral", "negative"],
            label_column="label",
            train_url="https://raw.githubusercontent.com/indobenchmark/indonlu/master/dataset/smsa_doc-sentiment-prosa/train_preprocess.tsv",
            valid_url="https://raw.githubusercontent.com/indobenchmark/indonlu/master/dataset/smsa_doc-sentiment-prosa/valid_preprocess.tsv",
            test_url="https://raw.githubusercontent.com/indobenchmark/indonlu/master/dataset/smsa_doc-sentiment-prosa/test_preprocess_masked_label.tsv",
            citation=textwrap.dedent(
                """\
            @inproceedings{purwarianti2019improving,
              title={Improving Bi-LSTM Performance for Indonesian Sentiment Analysis Using Paragraph Vector},
              author={Ayu Purwarianti and Ida Ayu Putu Ari Crisdayanti},
              booktitle={Proceedings of the 2019 International Conference of Advanced Informatics: Concepts, Theory and Applications (ICAICTA)},
              pages={1--5},
              year={2019},
              organization={IEEE}
            }"""
            ),
        ),
        IndonluConfig(
            name="casa",
            description=textwrap.dedent(
                """\
            An aspect-based sentiment analysis dataset consisting of around a thousand car reviews collected
            from multiple Indonesian online automobile platforms (Ilmania et al., 2018). The dataset covers
            six aspects of car quality. We define the task to be a multi-label classification task, where
            each label represents a sentiment for a single aspect with three possible values: positive,
            negative, and neutral."""
            ),
            text_features={"sentence": "sentence"},
            # label classes sorted refer to https://github.com/indobenchmark/indonlu/blob/master/utils/data_utils.py
            label_classes=["negative", "neutral", "positive"],
            label_column=["fuel", "machine", "others", "part", "price", "service"],
            train_url="https://raw.githubusercontent.com/indobenchmark/indonlu/master/dataset/casa_absa-prosa/train_preprocess.csv",
            valid_url="https://raw.githubusercontent.com/indobenchmark/indonlu/master/dataset/casa_absa-prosa/valid_preprocess.csv",
            test_url="https://raw.githubusercontent.com/indobenchmark/indonlu/master/dataset/casa_absa-prosa/test_preprocess_masked_label.csv",
            citation=textwrap.dedent(
                """\
            @inproceedings{ilmania2018aspect,
              title={Aspect Detection and Sentiment Classification Using Deep Neural Network for Indonesian Aspect-based Sentiment Analysis},
              author={Arfinda Ilmania, Abdurrahman, Samuel Cahyawijaya, Ayu Purwarianti},
              booktitle={Proceedings of the 2018 International Conference on Asian Language Processing(IALP)},
              pages={62--67},
              year={2018},
              organization={IEEE}
            }"""
            ),
        ),
        IndonluConfig(
            name="hoasa",
            description=textwrap.dedent(
                """\
            An aspect-based sentiment analysis dataset consisting of hotel reviews collected from the hotel
            aggregator platform, AiryRooms (Azhar et al., 2019). The dataset covers ten different aspects of
            hotel quality. Each review is labeled with a single sentiment label for each aspect. There are
            four possible sentiment classes for each sentiment label: positive, negative, neutral, and
            positive-negative. The positivenegative label is given to a review that contains multiple sentiments
            of the same aspect but for different objects (e.g., cleanliness of bed and toilet)."""
            ),
            text_features={"sentence": "sentence"},
            # label classes sorted refer to https://github.com/indobenchmark/indonlu/blob/master/utils/data_utils.py
            label_classes=["neg", "neut", "pos", "neg_pos"],
            label_column=[
                "ac",
                "air_panas",
                "bau",
                "general",
                "kebersihan",
                "linen",
                "service",
                "sunrise_meal",
                "tv",
                "wifi",
            ],
            train_url="https://raw.githubusercontent.com/indobenchmark/indonlu/master/dataset/hoasa_absa-airy/train_preprocess.csv",
            valid_url="https://raw.githubusercontent.com/indobenchmark/indonlu/master/dataset/hoasa_absa-airy/valid_preprocess.csv",
            test_url="https://raw.githubusercontent.com/indobenchmark/indonlu/master/dataset/hoasa_absa-airy/test_preprocess_masked_label.csv",
            citation=textwrap.dedent(
                """\
            @inproceedings{azhar2019multi,
              title={Multi-label Aspect Categorization with Convolutional Neural Networks and Extreme Gradient Boosting},
              author={A. N. Azhar, M. L. Khodra, and A. P. Sutiono}
              booktitle={Proceedings of the 2019 International Conference on Electrical Engineering and Informatics (ICEEI)},
              pages={35--40},
              year={2019}
            }"""
            ),
        ),
        IndonluConfig(
            name="wrete",
            description=textwrap.dedent(
                """\
            The Wiki Revision Edits Textual Entailment dataset (Setya and Mahendra, 2018) consists of 450 sentence pairs
            constructed from Wikipedia revision history. The dataset contains pairs of sentences and binary semantic
            relations between the pairs. The data are labeled as entailed when the meaning of the second sentence can be
            derived from the first one, and not entailed otherwise."""
            ),
            text_features={
                "premise": "premise",
                "hypothesis": "hypothesis",
                "category": "category",
            },
            # label classes sorted refer to https://github.com/indobenchmark/indonlu/blob/master/utils/data_utils.py
            label_classes=["NotEntail", "Entail_or_Paraphrase"],
            label_column="label",
            train_url="https://raw.githubusercontent.com/indobenchmark/indonlu/master/dataset/wrete_entailment-ui/train_preprocess.csv",
            valid_url="https://raw.githubusercontent.com/indobenchmark/indonlu/master/dataset/wrete_entailment-ui/valid_preprocess.csv",
            test_url="https://raw.githubusercontent.com/indobenchmark/indonlu/master/dataset/wrete_entailment-ui/test_preprocess_masked_label.csv",
            citation=textwrap.dedent(
                """\
            @inproceedings{setya2018semi,
              title={Semi-supervised Textual Entailment on Indonesian Wikipedia Data},
              author={Ken Nabila Setya and Rahmad Mahendra},
              booktitle={Proceedings of the 2018 International Conference on Computational Linguistics and Intelligent Text Processing (CICLing)},
              year={2018}
            }"""
            ),
        ),
        IndonluConfig(
            name="posp",
            description=textwrap.dedent(
                """\
            This Indonesian part-of-speech tagging (POS) dataset (Hoesen and Purwarianti, 2018) is collected from Indonesian
            news websites. The dataset consists of around 8000 sentences with 26 POS tags. The POS tag labels follow the
            Indonesian Association of Computational Linguistics (INACL) POS Tagging Convention."""
            ),
            text_features={"tokens": "tokens"},
            # label classes sorted refer to https://github.com/indobenchmark/indonlu/blob/master/utils/data_utils.py
            label_classes=[
                "B-PPO",
                "B-KUA",
                "B-ADV",
                "B-PRN",
                "B-VBI",
                "B-PAR",
                "B-VBP",
                "B-NNP",
                "B-UNS",
                "B-VBT",
                "B-VBL",
                "B-NNO",
                "B-ADJ",
                "B-PRR",
                "B-PRK",
                "B-CCN",
                "B-$$$",
                "B-ADK",
                "B-ART",
                "B-CSN",
                "B-NUM",
                "B-SYM",
                "B-INT",
                "B-NEG",
                "B-PRI",
                "B-VBE",
            ],
            label_column="pos_tags",
            train_url="https://raw.githubusercontent.com/indobenchmark/indonlu/master/dataset/posp_pos-prosa/train_preprocess.txt",
            valid_url="https://raw.githubusercontent.com/indobenchmark/indonlu/master/dataset/posp_pos-prosa/valid_preprocess.txt",
            test_url="https://raw.githubusercontent.com/indobenchmark/indonlu/master/dataset/posp_pos-prosa/test_preprocess_masked_label.txt",
            citation=textwrap.dedent(
                """\
            @inproceedings{hoesen2018investigating,
              title={Investigating Bi-LSTM and CRF with POS Tag Embedding for Indonesian Named Entity Tagger},
              author={Devin Hoesen and Ayu Purwarianti},
              booktitle={Proceedings of the 2018 International Conference on Asian Language Processing (IALP)},
              pages={35--38},
              year={2018},
              organization={IEEE}
            }"""
            ),
        ),
        IndonluConfig(
            name="bapos",
            description=textwrap.dedent(
                """\
            This POS tagging dataset (Dinakaramani et al., 2014) contains about 1000 sentences, collected from the PAN Localization
            Project. In this dataset, each word is tagged by one of 23 POS tag classes. Data splitting used in this benchmark follows
            the experimental setting used by Kurniawan and Aji (2018)"""
            ),
            text_features={"tokens": "tokens"},
            # label classes sorted refer to https://github.com/indobenchmark/indonlu/blob/master/utils/data_utils.py
            label_classes=[
                "B-PR",
                "B-CD",
                "I-PR",
                "B-SYM",
                "B-JJ",
                "B-DT",
                "I-UH",
                "I-NND",
                "B-SC",
                "I-WH",
                "I-IN",
                "I-NNP",
                "I-VB",
                "B-IN",
                "B-NND",
                "I-CD",
                "I-JJ",
                "I-X",
                "B-OD",
                "B-RP",
                "B-RB",
                "B-NNP",
                "I-RB",
                "I-Z",
                "B-CC",
                "B-NEG",
                "B-VB",
                "B-NN",
                "B-MD",
                "B-UH",
                "I-NN",
                "B-PRP",
                "I-SC",
                "B-Z",
                "I-PRP",
                "I-OD",
                "I-SYM",
                "B-WH",
                "B-FW",
                "I-CC",
                "B-X",
            ],
            label_column="pos_tags",
            train_url="https://raw.githubusercontent.com/indobenchmark/indonlu/master/dataset/bapos_pos-idn/train_preprocess.txt",
            valid_url="https://raw.githubusercontent.com/indobenchmark/indonlu/master/dataset/bapos_pos-idn/valid_preprocess.txt",
            test_url="https://raw.githubusercontent.com/indobenchmark/indonlu/master/dataset/bapos_pos-idn/test_preprocess_masked_label.txt",
            citation=textwrap.dedent(
                """\
            @inproceedings{dinakaramani2014designing,
              title={Designing an Indonesian Part of Speech Tagset and Manually Tagged Indonesian Corpus},
              author={Arawinda Dinakaramani, Fam Rashel, Andry Luthfi, and Ruli Manurung},
              booktitle={Proceedings of the 2014 International Conference on Asian Language Processing (IALP)},
              pages={66--69},
              year={2014},
              organization={IEEE}
            }
            @inproceedings{kurniawan2019toward,
              title={Toward a Standardized and More Accurate Indonesian Part-of-Speech Tagging},
              author={Kemal Kurniawan and Alham Fikri Aji},
              booktitle={Proceedings of the 2018 International Conference on Asian Language Processing (IALP)},
              pages={303--307},
              year={2018},
              organization={IEEE}
            }"""
            ),
        ),
        IndonluConfig(
            name="terma",
            description=textwrap.dedent(
                """\
            This span-extraction dataset is collected from the hotel aggregator platform, AiryRooms (Septiandri and Sutiono, 2019;
            Fernando et al., 2019). The dataset consists of thousands of hotel reviews, which each contain a span label for aspect
            and sentiment words representing the opinion of the reviewer on the corresponding aspect. The labels use
            Inside-Outside-Beginning (IOB) tagging representation with two kinds of tags, aspect and sentiment."""
            ),
            text_features={"tokens": "tokens"},
            # label classes sorted refer to https://github.com/indobenchmark/indonlu/blob/master/utils/data_utils.py
            label_classes=["I-SENTIMENT", "O", "I-ASPECT", "B-SENTIMENT", "B-ASPECT"],
            label_column="seq_label",
            train_url="https://raw.githubusercontent.com/indobenchmark/indonlu/master/dataset/terma_term-extraction-airy/train_preprocess.txt",
            valid_url="https://raw.githubusercontent.com/indobenchmark/indonlu/master/dataset/terma_term-extraction-airy/valid_preprocess.txt",
            test_url="https://raw.githubusercontent.com/indobenchmark/indonlu/master/dataset/terma_term-extraction-airy/test_preprocess_masked_label.txt",
            citation=textwrap.dedent(
                """\
            @article{winatmoko2019aspect,
              title={Aspect and Opinion Term Extraction for Hotel Reviews Using Transfer Learning and Auxiliary Labels},
              author={Yosef Ardhito Winatmoko, Ali Akbar Septiandri, Arie Pratama Sutiono},
              journal={arXiv preprint arXiv:1909.11879},
              year={2019}
            }
            @article{fernando2019aspect,
              title={Aspect and Opinion Terms Extraction Using Double Embeddings and Attention Mechanism for Indonesian Hotel Reviews},
              author={Jordhy Fernando, Masayu Leylia Khodra, Ali Akbar Septiandri},
              journal={arXiv preprint arXiv:1908.04899},
              year={2019}
            }"""
            ),
        ),
        IndonluConfig(
            name="keps",
            description=textwrap.dedent(
                """\
            This keyphrase extraction dataset (Mahfuzh et al., 2019) consists of text from Twitter discussing
            banking products and services and is written in the Indonesian language. A phrase containing
            important information is considered a keyphrase. Text may contain one or more keyphrases since
            important phrases can be located at different positions. The dataset follows the IOB chunking format,
            which represents the position of the keyphrase."""
            ),
            text_features={"tokens": "tokens"},
            # label classes sorted refer to https://github.com/indobenchmark/indonlu/blob/master/utils/data_utils.py
            label_classes=["O", "B", "I"],
            label_column="seq_label",
            train_url="https://raw.githubusercontent.com/indobenchmark/indonlu/master/dataset/keps_keyword-extraction-prosa/train_preprocess.txt",
            valid_url="https://raw.githubusercontent.com/indobenchmark/indonlu/master/dataset/keps_keyword-extraction-prosa/valid_preprocess.txt",
            test_url="https://raw.githubusercontent.com/indobenchmark/indonlu/master/dataset/keps_keyword-extraction-prosa/test_preprocess_masked_label.txt",
            citation=textwrap.dedent(
                """\
            @inproceedings{mahfuzh2019improving,
              title={Improving Joint Layer RNN based Keyphrase Extraction by Using Syntactical Features},
              author={Miftahul Mahfuzh, Sidik Soleman, and Ayu Purwarianti},
              booktitle={Proceedings of the 2019 International Conference of Advanced Informatics: Concepts, Theory and Applications (ICAICTA)},
              pages={1--6},
              year={2019},
              organization={IEEE}
            }"""
            ),
        ),
        IndonluConfig(
            name="nergrit",
            description=textwrap.dedent(
                """\
            This NER dataset is taken from the Grit-ID repository, and the labels are spans in IOB chunking representation.
            The dataset consists of three kinds of named entity tags, PERSON (name of person), PLACE (name of location), and
            ORGANIZATION (name of organization)."""
            ),
            text_features={"tokens": "tokens"},
            # label classes sorted refer to https://github.com/indobenchmark/indonlu/blob/master/utils/data_utils.py
            label_classes=["I-PERSON", "B-ORGANISATION", "I-ORGANISATION", "B-PLACE", "I-PLACE", "O", "B-PERSON"],
            label_column="ner_tags",
            train_url="https://raw.githubusercontent.com/indobenchmark/indonlu/master/dataset/nergrit_ner-grit/train_preprocess.txt",
            valid_url="https://raw.githubusercontent.com/indobenchmark/indonlu/master/dataset/nergrit_ner-grit/valid_preprocess.txt",
            test_url="https://raw.githubusercontent.com/indobenchmark/indonlu/master/dataset/nergrit_ner-grit/test_preprocess_masked_label.txt",
            citation=textwrap.dedent(
                """\
            @online{nergrit2019,
              title={NERGrit Corpus},
              author={NERGrit Developers},
              year={2019},
              url={https://github.com/grit-id/nergrit-corpus}
            }"""
            ),
        ),
        IndonluConfig(
            name="nerp",
            description=textwrap.dedent(
                """\
            This NER dataset (Hoesen and Purwarianti, 2018) contains texts collected from several Indonesian news websites.
            There are five labels available in this dataset, PER (name of person), LOC (name of location), IND (name of product or brand),
            EVT (name of the event), and FNB (name of food and beverage). The NERP dataset uses the IOB chunking format."""
            ),
            text_features={"tokens": "tokens"},
            # label classes sorted refer to https://github.com/indobenchmark/indonlu/blob/master/utils/data_utils.py
            label_classes=[
                "I-PPL",
                "B-EVT",
                "B-PLC",
                "I-IND",
                "B-IND",
                "B-FNB",
                "I-EVT",
                "B-PPL",
                "I-PLC",
                "O",
                "I-FNB",
            ],
            label_column="ner_tags",
            train_url="https://raw.githubusercontent.com/indobenchmark/indonlu/master/dataset/nerp_ner-prosa/train_preprocess.txt",
            valid_url="https://raw.githubusercontent.com/indobenchmark/indonlu/master/dataset/nerp_ner-prosa/valid_preprocess.txt",
            test_url="https://raw.githubusercontent.com/indobenchmark/indonlu/master/dataset/nerp_ner-prosa/test_preprocess_masked_label.txt",
            citation=textwrap.dedent(
                """\
            @inproceedings{hoesen2018investigating,
              title={Investigating Bi-LSTM and CRF with POS Tag Embedding for Indonesian Named Entity Tagger},
              author={Devin Hoesen and Ayu Purwarianti},
              booktitle={Proceedings of the 2018 International Conference on Asian Language Processing (IALP)},
              pages={35--38},
              year={2018},
              organization={IEEE}
            }"""
            ),
        ),
        IndonluConfig(
            name="facqa",
            description=textwrap.dedent(
                """\
            The goal of the FacQA dataset is to find the answer to a question from a provided short passage from
            a news article (Purwarianti et al., 2007). Each row in the FacQA dataset consists of a question,
            a short passage, and a label phrase, which can be found inside the corresponding short passage.
            There are six categories of questions: date, location, name, organization, person, and quantitative."""
            ),
            text_features={"question": "question", "passage": "passage"},
            # label classes sorted refer to https://github.com/indobenchmark/indonlu/blob/master/utils/data_utils.py
            label_classes=["O", "B", "I"],
            label_column="seq_label",
            train_url="https://raw.githubusercontent.com/indobenchmark/indonlu/master/dataset/facqa_qa-factoid-itb/train_preprocess.csv",
            valid_url="https://raw.githubusercontent.com/indobenchmark/indonlu/master/dataset/facqa_qa-factoid-itb/valid_preprocess.csv",
            test_url="https://raw.githubusercontent.com/indobenchmark/indonlu/master/dataset/facqa_qa-factoid-itb/test_preprocess_masked_label.csv",
            citation=textwrap.dedent(
                """\
            @inproceedings{purwarianti2007machine,
              title={A Machine Learning Approach for Indonesian Question Answering System},
              author={Ayu Purwarianti, Masatoshi Tsuchiya, and Seiichi Nakagawa},
              booktitle={Proceedings of Artificial Intelligence and Applications },
              pages={573--578},
              year={2007}
            }"""
            ),
        ),
    ]

    def _info(self):
        sentence_features = ["terma", "keps", "facqa"]
        ner_ = ["nergrit", "nerp"]
        pos_ = ["posp", "bapos"]

        if self.config.name in (sentence_features + ner_ + pos_):
            features = {
                text_feature: datasets.Sequence(datasets.Value("string"))
                for text_feature in self.config.text_features.keys()
            }
        else:
            features = {text_feature: datasets.Value("string") for text_feature in self.config.text_features}

        if self.config.label_classes:
            if self.config.name in sentence_features:
                features["seq_label"] = datasets.Sequence(
                    datasets.features.ClassLabel(names=self.config.label_classes)
                )
            elif self.config.name in ner_:
                features["ner_tags"] = datasets.Sequence(datasets.features.ClassLabel(names=self.config.label_classes))
            elif self.config.name in pos_:
                features["pos_tags"] = datasets.Sequence(datasets.features.ClassLabel(names=self.config.label_classes))
            elif self.config.name == "casa" or self.config.name == "hoasa":
                for label in self.config.label_column:
                    features[label] = datasets.features.ClassLabel(names=self.config.label_classes)
            else:
                features["label"] = datasets.features.ClassLabel(names=self.config.label_classes)

        return datasets.DatasetInfo(
            description=self.config.description,
            features=datasets.Features(features),
            homepage=_INDONLU_HOMEPAGE,
            citation=self.config.citation + "\n" + _INDONLU_CITATION,
        )

    def _split_generators(self, dl_manager):
        """Returns SplitGenerators."""
        train_path = dl_manager.download_and_extract(self.config.train_url)
        valid_path = dl_manager.download_and_extract(self.config.valid_url)
        test_path = dl_manager.download_and_extract(self.config.test_url)
        return [
            datasets.SplitGenerator(name=datasets.Split.TRAIN, gen_kwargs={"filepath": train_path}),
            datasets.SplitGenerator(name=datasets.Split.VALIDATION, gen_kwargs={"filepath": valid_path}),
            datasets.SplitGenerator(name=datasets.Split.TEST, gen_kwargs={"filepath": test_path}),
        ]

    def _generate_examples(self, filepath):
        """Yields examples."""
        csv_file = ["emot", "wrete", "facqa", "casa", "hoasa"]
        tsv_file = ["smsa"]
        txt_file = ["terma", "keps"]
        txt_file_pos = ["posp", "bapos"]
        txt_file_ner = ["nergrit", "nerp"]

        with open(filepath, encoding="utf-8") as f:

            if self.config.name in csv_file:
                reader = csv.reader(f, delimiter=",", quotechar='"', quoting=csv.QUOTE_ALL)
                next(reader)  # skip first row which is header

                for id_, row in enumerate(reader):
                    if self.config.name == "emot":
                        label, tweet = row
                        yield id_, {"tweet": tweet, "label": label}
                    elif self.config.name == "wrete":
                        premise, hypothesis, category, label = row
                        yield id_, {"premise": premise, "hypothesis": hypothesis, "category": category, "label": label}
                    elif self.config.name == "facqa":
                        question, passage, seq_label = row
                        yield id_, {
                            "question": ast.literal_eval(question),
                            "passage": ast.literal_eval(passage),
                            "seq_label": ast.literal_eval(seq_label),
                        }
                    elif self.config.name == "casa" or self.config.name == "hoasa":
                        sentence, *labels = row
                        sentence = {"sentence": sentence}
                        label = {l: labels[idx] for idx, l in enumerate(self.config.label_column)}
                        yield id_, {**sentence, **label}
            elif self.config.name in tsv_file:
                reader = csv.reader(f, delimiter="\t", quoting=csv.QUOTE_NONE)

                for id_, row in enumerate(reader):
                    if self.config.name == "smsa":
                        text, label = row
                        yield id_, {"text": text, "label": label}
            elif self.config.name in (txt_file + txt_file_pos + txt_file_ner):
                id_ = 0
                tokens = []
                seq_label = []
                for line in f:
                    if len(line.strip()) > 0:
                        token, label = line[:-1].split("\t")
                        tokens.append(token)
                        seq_label.append(label)
                    else:
                        if self.config.name in txt_file:
                            yield id_, {"tokens": tokens, "seq_label": seq_label}
                        elif self.config.name in txt_file_pos:
                            yield id_, {"tokens": tokens, "pos_tags": seq_label}
                        elif self.config.name in txt_file_ner:
                            yield id_, {"tokens": tokens, "ner_tags": seq_label}
                        id_ += 1
                        tokens = []
                        seq_label = []
                # add last example
                if tokens:
                    if self.config.name in txt_file:
                        yield id_, {"tokens": tokens, "seq_label": seq_label}
                    elif self.config.name in txt_file_pos:
                        yield id_, {"tokens": tokens, "pos_tags": seq_label}
                    elif self.config.name in txt_file_ner:
                        yield id_, {"tokens": tokens, "ner_tags": seq_label}
