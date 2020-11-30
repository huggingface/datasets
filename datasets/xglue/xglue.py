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

_XGLUE_ALL_DATA = "https://msmarco.blob.core.windows.net/xglue/xglue_public.tar.gz"


class XGlueConfig(datasets.BuilderConfig):
    """BuilderConfig for XGLUE."""

    def __init__(
        self,
        data_dir,
        citation,
        url,
        text_features=None,
        **kwargs,
    ):
        """BuilderConfig for GLUE.

        Args:
          text_features: `dict[string, string]`, map from the name of the feature
            dict for each text field to the name of the column in the tsv file
          label_column: `string`, name of the column in the tsv file corresponding
            to the label
          data_dir: `string`, the path to the folder containing the files in the
            downloaded .tar
          citation: `string`, citation for the data set
          url: `string`, url for information about the data set
          label_classes: `list[string]`, the list of classes if the label is
            categorical. If not provided, then the label will be of type
            `datasets.Value('float32')`.
          process_label: `Function[string, any]`, function  taking in the raw value
            of the label and processing it to the form required by the label feature
          **kwargs: keyword arguments forwarded to super.
        """
        super(XGlueConfig, self).__init__(version=datasets.Version("1.0.0", ""), **kwargs)
        self.text_features = text_features
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
            text_features=["words", "ner"],
            data_dir="dataset/NER",
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
            data_dir="dataset/POS",
            text_features=["words", "pos_tag"],
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
            data_dir="dataset/MLQA",
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
    ]

    def _info(self):
        if self.config.text_features is not None:
            features = {
                text_feature: datasets.Sequence(datasets.Value("string")) for text_feature in self.config.text_features
            }
            features["id"] = datasets.Value("int32")
            return datasets.DatasetInfo(
                description=_XGLUE_DESCRIPTION,
                features=datasets.Features(features),
                homepage=self.config.url,
                citation=self.config.citation + "\n" + _XGLUE_CITATION,
            )
        if self.config.name == "mlqa":
            return datasets.DatasetInfo(
                description=_XGLUE_DESCRIPTION,
                features=datasets.Features(
                    {
                        "context": datasets.Value("string"),
                        "question": datasets.Value("string"),
                        "answers": datasets.features.Sequence(
                            {"answer_start": datasets.Value("int32"), "text": datasets.Value("string")}
                        ),
                        "id": datasets.Value("string"),
                        # These are the features of your dataset like images, labels ...
                    }
                ),
                homepage=self.config.url,
                citation=self.config.citation + "\n" + _XGLUE_CITATION,
            )

    def _split_generators(self, dl_manager):
        all_data_folder = dl_manager.download_and_extract(_XGLUE_ALL_DATA)
        data_folder = all_data_folder + "/" + self.config.data_dir

        if self.config.name in ["pos", "ner"]:
            languages = ["en", "de", "nl", "es"]
            if self.config.name == "pos":
                languages += ["bg", "el", "fr", "pl", "tr", "vi", "zh", "ur", "hi", "it", "ar", "ru", "th"]
            return (
                [
                    datasets.SplitGenerator(
                        name=datasets.Split.TRAIN, gen_kwargs={"data_file": data_folder + "/" + "en.train"}
                    ),
                ]
                + [
                    datasets.SplitGenerator(
                        name=datasets.Split(f"validation.{lang}"),
                        gen_kwargs={"data_file": data_folder + "/" + f"{lang}.dev"},
                    )
                    for lang in languages
                ]
                + [
                    datasets.SplitGenerator(
                        name=datasets.Split(f"test.{lang}"),
                        gen_kwargs={"data_file": data_folder + "/" + f"{lang}.test"},
                    )
                    for lang in languages
                ]
            )
        if self.config.name == "mlqa":
            languages = ["en", "de", "ar", "es", "hi", "vi", "zh"]
            return (
                [
                    datasets.SplitGenerator(
                        name=datasets.Split.TRAIN,
                        gen_kwargs={"data_file": data_folder + "/" + "squad1.1" + "/" + "train-v1.1.json"},
                    ),
                ]
                + [
                    datasets.SplitGenerator(
                        name=datasets.Split(f"validation.{lang}"),
                        gen_kwargs={
                            "data_file": data_folder
                            + "/"
                            + "MLQA_V1"
                            + "/"
                            + "dev"
                            + "/"
                            + f"dev-context-{lang}-question-{lang}.json"
                        },
                    )
                    for lang in languages
                ]
                + [
                    datasets.SplitGenerator(
                        name=datasets.Split(f"test.{lang}"),
                        gen_kwargs={
                            "data_file": data_folder
                            + "/"
                            + "MLQA_V1"
                            + "/"
                            + "test"
                            + "/"
                            + f"test-context-{lang}-question-{lang}.json"
                        },
                    )
                    for lang in languages
                ]
            )

    def _generate_examples(self, data_file, split=None):
        if self.config.name in ["ner", "pos"]:
            words = []
            result = []
            idx = 0
            with open(data_file, "r") as f:
                for line in f:
                    if line.strip() == "":
                        if len(words) > 0:
                            output_dict = {}
                            output_dict[self.config.text_features[0]] = words
                            output_dict[self.config.text_features[1]] = result
                            output_dict["id"] = idx
                            yield idx, output_dict
                            words = []
                            result = []
                            idx += 1
                    else:
                        splits = line.strip().split(" ")
                        words.append(splits[0])
                        result.append(splits[1])
        if self.config.name in ["mlqa"]:
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
                            "id": id_,
                        }
