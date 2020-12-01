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
"""The General Language Understanding Evaluation (GLUE) benchmark."""

from __future__ import absolute_import, division, print_function

import json
import os
import textwrap

import datasets


_XGLUE_CITATION = """\
@article{Liang2020XGLUEAN,
  title={XGLUE: A New Benchmark Dataset for Cross-lingual Pre-training, Understanding and Generation},
  author={Yaobo Liang and Nan Duan and Yeyun Gong and Ning Wu and Fenfei Guo and Weizhen Qi
  and Ming Gong and Linjun Shou and Daxin Jiang and Guihong Cao and Xiaodong Fan and Ruofei
  Zhang and Rahul Agrawal and Edward Cui and Sining Wei and Taroon Bharti and Ying Qiao
  and Jiun-Hung Chen and Winnie Wu and Shuguang Liu and Fan Yang and Daniel Campos
  and Rangan Majumder and Ming Zhou},
  journal={arXiv},
  year={2020},
  volume={abs/2004.01401}
}
"""

_XGLUE_DESCRIPTION = """\
XGLUE is a new benchmark dataset to evaluate the performance of cross-lingual pre-trained
models with respect to cross-lingual natural language understanding and generation.
The benchmark is composed of the following 11 tasks:
- NER
- POS Tagging (POS)
- News Classification (NC)
- MLQA
- XNLI
- PAWS-X
- Query-Ad Matching (QADSM)
- Web Page Ranking (WPR)
- QA Matching (QAM)
- Question Generation (QG)
- News Title Generation (NTG)

For more information, please take a look at https://microsoft.github.io/XGLUE/.
"""

_XGLUE_ALL_DATA = "https://xglue.blob.core.windows.net/xglue/xglue_full_dataset.tar.gz"

_LANGUAGES = {
    "ner": ["en", "de", "es", "nl"],
    "pos": ["en", "de", "es", "nl", "bg", "el", "fr", "pl", "tr", "vi", "zh", "ur", "hi", "it", "ar", "ru", "th"],
    "mlqa": ["en", "de", "ar", "es", "hi", "vi", "zh"],
    "nc": ["en", "de", "es", "fr", "ru"],
    "xnli": ["en", "ar", "bg", "de", "el", "es", "fr", "hi", "ru", "sw", "th", "tr", "ur", "vi", "zh"],
    "paws-x": ["en", "de", "es", "fr"],
    "qadsm": ["en", "de", "fr"],
    "wpr": ["en", "de", "es", "fr", "it", "pt", "zh"],
    "qam": ["en", "de", "fr"],
    "qg": ["en", "de", "es", "fr", "it", "pt"],
    "ntg": ["en", "de", "es", "fr", "ru"],
}

_PATHS = {
    "mlqa": {
        "train": os.path.join("squad1.1", "train-v1.1.json"),
        "dev": os.path.join("MLQA_V1", "dev", "dev-context-{0}-question-{0}.json"),
        "test": os.path.join("MLQA_V1", "test", "test-context-{0}-question-{0}.json"),
    },
    "xnli": {"train": "multinli.train.en.tsv", "dev": "{}.dev", "test": "{}.test"},
    "paws-x": {
        "train": os.path.join("en", "train.tsv"),
        "dev": os.path.join("{}", "dev_2k.tsv"),
        "test": os.path.join("{}", "test_2k.tsv"),
    },
}
for name in ["ner", "pos"]:
    _PATHS[name] = {"train": "en.train", "dev": "{}.dev", "test": "{}.test"}
for name in ["nc", "qadsm", "wpr", "qam"]:
    _PATHS[name] = {
        "train": "xglue." + name + ".en.train",
        "dev": "xglue." + name + ".{}.dev",
        "test": "xglue." + name + ".{}.test",
    }
for name in ["qg", "ntg"]:
    _PATHS[name] = {"train": "xglue." + name + ".en", "dev": "xglue." + name + ".{}", "test": "xglue." + name + ".{}"}


class XGlueConfig(datasets.BuilderConfig):
    """BuilderConfig for XGLUE."""

    def __init__(
        self,
        data_dir,
        citation,
        url,
        **kwargs,
    ):
        """BuilderConfig for XGLUE.

        Args:
          data_dir: `string`, the path to the folder containing the files in the
            downloaded .tar
          citation: `string`, citation for the data set
          url: `string`, url for information about the data set
          **kwargs: keyword arguments forwarded to super.
        """
        super(XGlueConfig, self).__init__(version=datasets.Version("1.0.0", ""), **kwargs)
        self.data_dir = data_dir
        self.citation = citation
        self.url = url


class XGlue(datasets.GeneratorBasedBuilder):
    """The Cross-lingual Pre-training, Understanding and Generation (XGlue) Benchmark."""

    BUILDER_CONFIGS = [
        XGlueConfig(
            name="ner",
            description=textwrap.dedent(
                """\
            The shared task of CoNLL-2003 concerns language-independent named entity recognition.
            We will concentrate on four types of named entities:
            persons, locations, organizations and names of miscellaneous entities
            that do not belong to the previous three groups.
            """
            ),
            data_dir="NER",
            citation=textwrap.dedent(
                """\
            @article{Sang2003IntroductionTT,
              title={Introduction to the CoNLL-2003 Shared Task: Language-Independent Named Entity Recognition},
              author={Erik F. Tjong Kim Sang and Fien De Meulder},
              journal={ArXiv},
              year={2003},
              volume={cs.CL/0306050}
            },
            @article{Sang2002IntroductionTT,
              title={Introduction to the CoNLL-2002 Shared Task: Language-Independent Named Entity Recognition},
              author={Erik F. Tjong Kim Sang},
              journal={ArXiv},
              year={2002},
              volume={cs.CL/0209010}
            }"""
            ),
            url="https://www.clips.uantwerpen.be/conll2003/ner/",
        ),
        XGlueConfig(
            name="pos",
            description=textwrap.dedent(
                """\
            Universal Dependencies (UD) is a project that is developing cross-linguistically consistent treebank
            annotation for many languages, with the goal of facilitating multilingual parser development, cross-lingual
            learning, and parsing research from a language typology perspective. The annotation scheme is based on an
            evolution of (universal) Stanford dependencies (de Marneffe et al., 2006, 2008, 2014), Google universal
            part-of-speech tags (Petrov et al., 2012), and the Interset interlingua for morphosyntactic tagsets
            (Zeman, 2008). The general philosophy is to provide a universal inventory of categories and guidelines
            to facilitate consistent annotation of similar constructions across languages, while
            allowing language-specific extensions when necessary.
            """
            ),
            data_dir="POS",
            citation=textwrap.dedent(
                """\
            @misc{11234/1-3105,
              title={Universal Dependencies 2.5},
              author={Zeman, Daniel and Nivre, Joakim and Abrams, Mitchell and Aepli, et al.},
              url={http://hdl.handle.net/11234/1-3105},
              note={{LINDAT}/{CLARIAH}-{CZ} digital library at the Institute of Formal and Applied Linguistics ({{\'U}FAL}), Faculty of Mathematics and Physics, Charles University},
              copyright={Licence Universal Dependencies v2.5},
              year={2019}
            }"""
            ),
            url="https://universaldependencies.org/",
        ),
        XGlueConfig(
            name="mlqa",
            description=textwrap.dedent(
                """\
            MLQA (MultiLingual Question Answering) is a benchmark dataset for evaluating cross-lingual question answering
            performance. MLQA consists of over 5K extractive QA instances (12K in English) in SQuAD format in seven languages
            - English, Arabic, German, Spanish, Hindi, Vietnamese and Simplified Chinese.
            MLQA is highly parallel, with QA instances parallel between 4 different languages on average.
            """
            ),
            data_dir="MLQA",
            citation=textwrap.dedent(
                """\
            @article{Lewis2019MLQAEC,
              title={MLQA: Evaluating Cross-lingual Extractive Question Answering},
              author={Patrick Lewis and Barlas Oguz and Ruty Rinott and Sebastian Riedel and Holger Schwenk},
              journal={ArXiv},
              year={2019},
              volume={abs/1910.07475}
            }"""
            ),
            url="https://github.com/facebookresearch/MLQA",
        ),
        XGlueConfig(
            name="nc",
            description=textwrap.dedent(
                """\
            This task aims to predict the category given a news article. It covers
            5 languages, including English, Spanish, French,
            German and Russian. Each labeled instance is a
            3-tuple: <news title, news body, category>. The
            category number is 10. We crawl this dataset from
            a commercial news website. Accuracy (ACC) of
            the multi-class classification is used as the metric.
            """
            ),
            data_dir="NC",
            citation="",
            url="",
        ),
        XGlueConfig(
            name="xnli",
            description=textwrap.dedent(
                """\
            XNLI is a subset of a few thousand examples from MNLI which has been translated
            into a 14 different languages (some low-ish resource). As with MNLI, the goal is
            to predict textual entailment (does sentence A imply/contradict/neither sentence
            B) and is a classification task (given two sentences, predict one of three
            labels).
            """
            ),
            data_dir="XNLI",
            citation=textwrap.dedent(
                """\
            @inproceedings{Conneau2018XNLIEC,
              title={XNLI: Evaluating Cross-lingual Sentence Representations},
              author={Alexis Conneau and Guillaume Lample and Ruty Rinott and Adina Williams and Samuel R. Bowman and Holger Schwenk and Veselin Stoyanov},
              booktitle={EMNLP},
              year={2018}
            }"""
            ),
            url="https://github.com/facebookresearch/XNLI",
        ),
        XGlueConfig(
            name="paws-x",
            description=textwrap.dedent(
                """\
            PAWS-X contains 23,659 human translated PAWS (Paraphrase Adversaries from Word Scrambling) evaluation pairs and 296,406 machine translated training pairs in six typologically distinct languages: French, Spanish, German, Chinese, Japanese, and Korean. All translated pairs are sourced from examples in PAWS-Wiki.
            """
            ),
            data_dir="PAWSX",
            citation=textwrap.dedent(
                """\
            @article{Yang2019PAWSXAC,
              title={PAWS-X: A Cross-lingual Adversarial Dataset for Paraphrase Identification},
              author={Yinfei Yang and Yuan Zhang and Chris Tar and Jason Baldridge},
              journal={ArXiv},
              year={2019},
              volume={abs/1908.11828}
            }"""
            ),
            url="https://github.com/google-research-datasets/paws/tree/master/pawsx",
        ),
        XGlueConfig(
            name="qadsm",
            description=textwrap.dedent(
                """\
            Query-Ad Matching (QADSM) task aims
            to predict whether an advertisement (ad) is relevant to an input query. It covers 3 languages, including English, French and German. Each labeled instance is a 4-tuple: <query, ad title, ad description, label>. The label indicates whether the
            ad is relevant to the query (Good), or not (Bad).
            This dataset was constructed based on a commercial search engine. Accuracy (ACC) of the binary classification should be used as the metric.
            """
            ),
            data_dir="QADSM",
            citation="",
            url="",
        ),
        XGlueConfig(
            name="wpr",
            description=textwrap.dedent(
                """\
                Tthe Web Page Ranking (WPR) task aims to
                predict whether a web page is relevant to an input query. It covers 7 languages, including English, German, French, Spanish, Italian, Portuguese and Chinese. Each labeled instance is a
                4-tuple: <query, web page title, web page snippet, label>. The relevance label contains 5 ratings: Perfect (4), Excellent (3), Good (2), Fair (1)
                and Bad (0). The dataset is constructed based on a
                commercial search engine. Normalize Discounted
                Cumulative Gain (nDCG) should be used as the metric.
            """
            ),
            data_dir="WPR",
            citation="",
            url="",
        ),
        XGlueConfig(
            name="qam",
            description=textwrap.dedent(
                """\
                The QA Matching (QAM) task aims to predict whether a <question, passage> pair is a QA pair.
                It covers 3 languages, including English, French
                and German. Each labeled instance is a 3-tuple:
                <question, passage, label>. The label indicates
                whether the passage is the answer of the question
                (1), or not (0). This dataset is constructed  based on
                a commercial search engine. Accuracy (ACC) of
                the binary classification should be used as the metric.
            """
            ),
            data_dir="QAM",
            citation="",
            url="",
        ),
        XGlueConfig(
            name="qg",
            description=textwrap.dedent(
                """\
                The Question Generation (QG) task aims to
generate a question for a given passage. <passage, question> pairs were collected from a commercial search engine. It covers 6 languages, including English, French, German, Spanish, Italian and
Portuguese. BLEU-4 score should be used as the metric.
            """
            ),
            data_dir="QG",
            citation="",
            url="",
        ),
        XGlueConfig(
            name="ntg",
            description=textwrap.dedent(
                """\
                News Title Generation (NTG) task aims
                to generate a proper title for a given news body.
                We collect <news body, news title> pairs from a
                commercial news website. It covers 5 languages,
                including German, English, French, Spanish and
                Russian. BLEU-4 score should be used as the metric.
            """
            ),
            data_dir="NTG",
            citation="",
            url="",
        ),
    ]

    def _info(self):
        if self.config.name == "ner":
            features = {
                "words": datasets.Sequence(datasets.Value("string")),
                "ner": datasets.Sequence(
                    datasets.features.ClassLabel(
                        names=[
                            "O",
                            "B-PER",
                            "I-PER",
                            "B-ORG",
                            "I-ORG",
                            "B-LOC",
                            "I-LOC",
                            "B-MISC",
                            "I-MISC",
                        ]
                    )
                ),
            }
        elif self.config.name == "pos":
            features = {
                "words": datasets.Sequence(datasets.Value("string")),
                "pos": datasets.Sequence(
                    datasets.features.ClassLabel(
                        names=[
                            "ADJ",
                            "ADP",
                            "ADV",
                            "AUX",
                            "CCONJ",
                            "DET",
                            "INTJ",
                            "NOUN",
                            "NUM",
                            "PART",
                            "PRON",
                            "PROPN",
                            "PUNCT",
                            "SCONJ",
                            "SYM",
                            "VERB",
                            "X",
                        ]
                    )
                ),
            }
        elif self.config.name == "mlqa":
            features = {
                "context": datasets.Value("string"),
                "question": datasets.Value("string"),
                "answers": datasets.features.Sequence(
                    {"answer_start": datasets.Value("int32"), "text": datasets.Value("string")}
                ),
                # These are the features of your dataset like images, labels ...
            }
        elif self.config.name == "nc":
            features = {
                "news_title": datasets.Value("string"),
                "news_body": datasets.Value("string"),
                "news_category": datasets.ClassLabel(
                    names=[
                        "foodanddrink",
                        "sports",
                        "travel",
                        "finance",
                        "lifestyle",
                        "news",
                        "entertainment",
                        "health",
                        "video",
                        "autos",
                    ]
                ),
            }
        elif self.config.name == "xnli":
            features = {
                "premise": datasets.Value("string"),
                "hypothesis": datasets.Value("string"),
                "label": datasets.features.ClassLabel(names=["entailment", "neutral", "contradiction"]),
            }
        elif self.config.name == "paws-x":
            features = {
                "sentence1": datasets.Value("string"),
                "sentence2": datasets.Value("string"),
                "label": datasets.features.ClassLabel(names=["different", "same"]),
            }
        elif self.config.name == "qadsm":
            features = {
                "query": datasets.Value("string"),
                "ad_title": datasets.Value("string"),
                "ad_description": datasets.Value("string"),
                "relevance_label": datasets.features.ClassLabel(names=["Bad", "Good"]),
            }
        elif self.config.name == "wpr":
            features = {
                "query": datasets.Value("string"),
                "web_page_title": datasets.Value("string"),
                "web_page_snippet": datasets.Value("string"),
                "relavance_label": datasets.features.ClassLabel(names=["Bad", "Fair", "Good", "Excellent", "Perfect"]),
            }
        elif self.config.name == "qam":
            features = {
                "question": datasets.Value("string"),
                "answer": datasets.Value("string"),
                "label": datasets.features.ClassLabel(names=["False", "True"]),
            }
        elif self.config.name == "qg":
            features = {
                "answer_passage": datasets.Value("string"),
                "question": datasets.Value("string"),
            }
        elif self.config.name == "ntg":
            features = {
                "news_body": datasets.Value("string"),
                "news_title": datasets.Value("string"),
            }

        return datasets.DatasetInfo(
            description=_XGLUE_DESCRIPTION,
            features=datasets.Features(features),
            homepage=self.config.url,
            citation=self.config.citation + "\n" + _XGLUE_CITATION,
        )

    def _split_generators(self, dl_manager):
        all_data_folder = dl_manager.download_and_extract(_XGLUE_ALL_DATA)
        data_folder = os.path.join(all_data_folder, "xglue_full_dataset", self.config.data_dir)
        name = self.config.name

        languages = _LANGUAGES[name]
        return (
            [
                datasets.SplitGenerator(
                    name=datasets.Split.TRAIN,
                    gen_kwargs={"data_file": os.path.join(data_folder, _PATHS[name]["train"]), "split": "train"},
                ),
            ]
            + [
                datasets.SplitGenerator(
                    name=datasets.Split(f"validation.{lang}"),
                    gen_kwargs={
                        "data_file": os.path.join(data_folder, _PATHS[name]["dev"].format(lang)),
                        "split": "dev",
                    },
                )
                for lang in languages
            ]
            + [
                datasets.SplitGenerator(
                    name=datasets.Split(f"test.{lang}"),
                    gen_kwargs={
                        "data_file": os.path.join(data_folder, _PATHS[name]["test"].format(lang)),
                        "split": "test",
                    },
                )
                for lang in languages
            ]
        )

    def _generate_examples(self, data_file, split=None):
        keys = list(self._info().features.keys())

        if self.config.name == "mlqa":
            with open(data_file, encoding="utf-8") as f:
                data = json.load(f)
            for examples in data["data"]:
                for example in examples["paragraphs"]:
                    context = example["context"]
                    for qa in example["qas"]:
                        question = qa["question"]
                        id_ = qa["id"]
                        answers = qa["answers"]
                        answers_start = [answer["answer_start"] for answer in answers]
                        answers_text = [answer["text"] for answer in answers]
                        yield id_, {
                            "context": context,
                            "question": question,
                            "answers": {"answer_start": answers_start, "text": answers_text},
                        }
        elif self.config.name in ["ner", "pos"]:
            words = []
            result = []
            idx = -1
            with open(data_file, encoding="utf-8") as f:
                for line in f:
                    if line.strip() == "":
                        if len(words) > 0:
                            out_dict = {keys[0]: words, keys[1]: result}
                            words = []
                            result = []
                            idx += 1
                            yield idx, out_dict
                    else:
                        splits = line.strip().split(" ")
                        words.append(splits[0])
                        result.append(splits[1])
        elif self.config.name in ["ntg", "qg"]:
            with open(data_file + ".src." + split, encoding="utf-8") as src_f, open(
                data_file + ".tgt." + split, encoding="utf-8"
            ) as tgt_f:
                for idx, (src_line, tgt_line) in enumerate(zip(src_f, tgt_f)):
                    yield idx, {keys[0]: src_line.strip(), keys[1]: tgt_line.strip()}
        else:
            _process_dict = {
                "paws-x": {"0": "different", "1": "same"},
                "xnli": {"contradictory": "contradiction"},
                "qam": {"0": "False", "1": "True"},
                "wpr": {"0": "Bad", "1": "Fair", "2": "Good", "3": "Excellent", "4": "Perfect"},
            }

            def _process(value):
                if self.config.name in _process_dict and value in _process_dict[self.config.name]:
                    return _process_dict[self.config.name][value]
                return value

            with open(data_file, encoding="utf-8") as f:
                for idx, line in enumerate(f):
                    if data_file.split(".")[-1] == "tsv" and idx == 0:
                        continue
                    items = line.strip().split("\t")
                    yield idx, {
                        key: _process(value)
                        for key, value in zip(keys, items[1:] if self.config.name == "paws-x" else items)
                    }
