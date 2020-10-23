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
"""A Chinese Language Understanding Evaluation Benchmark (CLUE) benchmark."""

from __future__ import absolute_import, division, print_function

import json
import os
import re
import textwrap

import six

import datasets


_CLUE_CITATION = """\
@misc{xu2020clue,
    title={CLUE: A Chinese Language Understanding Evaluation Benchmark},
    author={Liang Xu and Xuanwei Zhang and Lu Li and Hai Hu and Chenjie Cao and Weitang Liu and Junyi Li and Yudong Li and Kai Sun and Yechen Xu and Yiming Cui and Cong Yu and Qianqian Dong and Yin Tian and Dian Yu and Bo Shi and Jun Zeng and Rongzhao Wang and Weijian Xie and Yanting Li and Yina Patterson and Zuoyu Tian and Yiwen Zhang and He Zhou and Shaoweihua Liu and Qipeng Zhao and Cong Yue and Xinrui Zhang and Zhengliang Yang and Zhenzhong Lan},
    year={2020},
    eprint={2004.05986},
    archivePrefix={arXiv},
    primaryClass={cs.CL}
}
"""

_CLUE_DESCRIPTION = """\
CLUE, A Chinese Language Understanding Evaluation Benchmark
(https://www.cluebenchmarks.com/) is a collection of resources for training,
evaluating, and analyzing Chinese language understanding systems.

"""


class ClueConfig(datasets.BuilderConfig):
    """BuilderConfig for CLUE."""

    def __init__(
        self,
        data_url,
        text_features=None,
        label_column=None,
        data_dir="",
        citation="",
        url="",
        label_classes=None,
        process_label=lambda x: x,
        **kwargs,
    ):
        """BuilderConfig for CLUE.

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
        super(ClueConfig, self).__init__(version=datasets.Version("1.0.0", ""), **kwargs)
        self.text_features = text_features
        self.label_column = label_column
        self.label_classes = label_classes
        self.data_url = data_url
        self.data_dir = data_dir
        self.citation = citation
        self.url = url
        self.process_label = process_label


class Clue(datasets.GeneratorBasedBuilder):
    """A Chinese Language Understanding Evaluation Benchmark (CLUE) benchmark."""

    BUILDER_CONFIGS = [
        ClueConfig(
            name="afqmc",
            description=textwrap.dedent(
                """\
            Ant Financial Question Matching Corpus is a dataset for Chinese
            question matching (similar to QQP).
            """
            ),
            text_features={"sentence1": "sentence1", "sentence2": "sentence2"},
            label_classes=["0", "1"],
            label_column="label",
            data_url="https://storage.googleapis.com/cluebenchmark/tasks/afqmc_public.zip",
            url="https://dc.cloud.alipay.com/index#/topic/data?id=8",
        ),
        ClueConfig(
            name="tnews",
            description=textwrap.dedent(
                """\
            Toutiao Short Text Classification for News is a dataset for Chinese
            short news classification.
            """
            ),
            text_features={"sentence": "sentence"},
            label_classes=[
                "100",
                "101",
                "102",
                "103",
                "104",
                "106",
                "107",
                "108",
                "109",
                "110",
                "112",
                "113",
                "114",
                "115",
                "116",
            ],
            label_column="label",
            data_url="https://storage.googleapis.com/cluebenchmark/tasks/tnews_public.zip",
            url="https://github.com/skdjfla/toutiao-text-classfication-dataset",
        ),
        ClueConfig(
            name="iflytek",
            description=textwrap.dedent(
                """\
            IFLYTEK Long Text Classification for News is a dataset for Chinese
            long text classification. The text is crawled from an app market.
            """
            ),
            text_features={"sentence": "sentence"},
            label_classes=[str(label) for label in range(119)],
            label_column="label",
            data_url="https://storage.googleapis.com/cluebenchmark/tasks/iflytek_public.zip",
        ),
        ClueConfig(
            name="cmnli",
            description=textwrap.dedent(
                """\
            Chinese Multi-Genre NLI is a dataset for Chinese Natural Language
            Inference. It consists of XNLI (Chinese subset) and translated MNLI.
            """
            ),
            text_features={"sentence1": "sentence1", "sentence2": "sentence2"},
            label_classes=["neutral", "entailment", "contradiction"],
            label_column="label",
            data_url="https://storage.googleapis.com/cluebenchmark/tasks/cmnli_public.zip",
            data_dir="cmnli_public",
        ),
        ClueConfig(
            name="cluewsc2020",
            description=textwrap.dedent(
                """\
            CLUE Winograd Scheme Challenge (CLUEWSC 2020) is a Chinese WSC dataset.
            The text is from contemporary literature and annotated by human experts.
            The task is to determine which noun the pronoun in the sentence refers to.
            The question appears in the form of true and false discrimination.
            """
            ),
            text_features={"text": "text", "target": "target"},
            label_classes=["false", "true"],
            label_column="label",
            data_url="https://storage.googleapis.com/cluebenchmark/tasks/cluewsc2020_public.zip",
        ),
        ClueConfig(
            name="csl",
            description=textwrap.dedent(
                """\
            Chinese Scientific Literature Dataset (CSL) is taken from the abstracts of
            Chinese papers and their keywords. The papers are selected from some core
            journals of Chinese social sciences and natural sciences. TF-IDF is used to
            generate a mixture of fake keywords and real keywords in the paper to construct
            abstract-keyword pairs. The task goal is to judge whether the keywords are
            all real keywords based on the abstract.
            """
            ),
            text_features={"abst": "abst", "keyword": "keyword", "corpus_id": "id"},
            label_classes=["0", "1"],
            label_column="label",
            data_url="https://storage.googleapis.com/cluebenchmark/tasks/csl_public.zip",
            url="https://github.com/P01son6415/CSL",
        ),
        ClueConfig(
            name="cmrc2018",
            description=textwrap.dedent(
                """\
            CMRC2018 is the first Chinese Span-Extraction Machine Reading Comprehension
            Dataset. The task requires to set up a system that reads context,
            question and extract the answer from the context (the answer is a continuous
            span in the context).
            """
            ),
            data_url="https://storage.googleapis.com/cluebenchmark/tasks/cmrc2018_public.zip",
            url="https://hfl-rc.github.io/cmrc2018/",
            citation=textwrap.dedent(
                """\
                  @article{cmrc2018-dataset,
                  title={A Span-Extraction Dataset for Chinese Machine Reading Comprehension},
                  author={Cui, Yiming and Liu, Ting and Xiao, Li and Chen, Zhipeng and Ma, Wentao and Che, Wanxiang and Wang, Shijin and Hu, Guoping},
                  journal={arXiv preprint arXiv:1810.07366},
                  year={2018}
                }"""
            ),
        ),
        ClueConfig(
            name="drcd",
            description=textwrap.dedent(
                """\
            Delta Reading Comprehension Dataset (DRCD) belongs to the general field of traditional
            Chinese machine reading comprehension data set. This data set is expected to become a
            standard Chinese reading comprehension data set suitable for transfer learning.
            """
            ),
            data_url="https://storage.googleapis.com/cluebenchmark/tasks/drcd_public.zip",
            url="https://github.com/DRCKnowledgeTeam/DRCD",
        ),
        ClueConfig(
            name="chid",
            description=textwrap.dedent(
                """\
            Chinese IDiom Dataset for Cloze Test (CHID) contains many masked idioms in the text.
            The candidates contain similar idioms to the real ones.
            """
            ),
            text_features={"candidates": "candidates", "content": "content"},
            data_url="https://storage.googleapis.com/cluebenchmark/tasks/chid_public.zip",
            url="https://arxiv.org/abs/1906.01265",
            citation=textwrap.dedent(
                """\
                  @article{Zheng_2019,
                   title={ChID: A Large-scale Chinese IDiom Dataset for Cloze Test},
                   url={http://dx.doi.org/10.18653/v1/P19-1075},
                   DOI={10.18653/v1/p19-1075},
                   journal={Proceedings of the 57th Annual Meeting of the Association for Computational Linguistics},
                   publisher={Association for Computational Linguistics},
                   author={Zheng, Chujie and Huang, Minlie and Sun, Aixin},
                   year={2019}
                }"""
            ),
        ),
        ClueConfig(
            name="c3",
            description=textwrap.dedent(
                """\
            Multiple-Choice Chinese Machine Reading Comprehension (C3, or C^3) is a Chinese
            multi-choice reading comprehension data set, including mixed type data sets
            such as dialogue and long text. Both the training and validation sets are
            the concatenation of the dialogue and long-text subsets.
            """
            ),
            text_features={"candidates": "candidates", "content": "content"},
            data_url="https://storage.googleapis.com/cluebenchmark/tasks/c3_public.zip",
            url="https://arxiv.org/abs/1904.09679",
            citation=textwrap.dedent(
                """\
                  @article{sun2020investigating,
                      author    = {Kai Sun and
                                   Dian Yu and
                                   Dong Yu and
                                   Claire Cardie},
                      title     = {Investigating Prior Knowledge for Challenging Chinese Machine Reading
                                   Comprehension},
                      journal   = {Trans. Assoc. Comput. Linguistics},
                      volume    = {8},
                      pages     = {141--155},
                      year      = {2020},
                      url       = {https://transacl.org/ojs/index.php/tacl/article/view/1882}
                    }"""
            ),
        ),
        ClueConfig(
            name="ocnli",
            description=textwrap.dedent(
                """\
            OCNLI stands for Original Chinese Natural Language Inference. It is a corpus for
            Chinese Natural Language Inference, collected following closely the procedures of MNLI,
            but with enhanced strategies aiming for more challenging inference pairs. We want to
            emphasize we did not use human/machine translation in creating the dataset, and thus
            our Chinese texts are original and not translated.
            """
            ),
            text_features={"sentence1": "sentence1", "sentence2": "sentence2"},
            label_classes=["neutral", "entailment", "contradiction"],
            label_column="label",
            data_url="https://github.com/CLUEbenchmark/OCNLI/archive/02d55cb3c7dc984682677b8dd81db6a1e4710720.zip",
            data_dir="OCNLI-02d55cb3c7dc984682677b8dd81db6a1e4710720/data/ocnli",
            url="https://arxiv.org/abs/2010.05444",
            citation=textwrap.dedent(
                """\
                  @inproceedings{ocnli,
                    title={OCNLI: Original Chinese Natural Language Inference},
                    author={Hai Hu and Kyle Richardson and Liang Xu and Lu Li and Sandra Kuebler and Larry Moss},
                    booktitle={Findings of EMNLP},
                    year={2020},
                    url={https://arxiv.org/abs/2010.05444}
                }"""
            ),
        ),
        ClueConfig(
            name="diagnostics",
            description=textwrap.dedent(
                """\
            Diagnostic set, used to evaluate the performance of different models on 9 Chinese language
            phenomena summarized by linguists.

            Use the model trained on CMNLI to directly predict the result on this diagnostic set.
            """
            ),
            text_features={"sentence1": "premise", "sentence2": "hypothesis"},
            label_classes=["neutral", "entailment", "contradiction"],
            label_column="label",
            data_url="https://storage.googleapis.com/cluebenchmark/tasks/clue_diagnostics_public.zip",
        ),
    ]

    def _info(self):
        if self.config.name in ["afqmc", "tnews", "iflytek", "cmnli", "diagnostics", "ocnli"]:
            features = {
                text_feature: datasets.Value("string") for text_feature in six.iterkeys(self.config.text_features)
            }
            if self.config.label_classes:
                features["label"] = datasets.features.ClassLabel(names=self.config.label_classes)
            else:
                features["label"] = datasets.Value("float32")
            features["idx"] = datasets.Value("int32")
        elif self.config.name == "cluewsc2020":
            features = {
                "idx": datasets.Value("int32"),
                "text": datasets.Value("string"),
                "label": datasets.features.ClassLabel(names=["true", "false"]),
                "target": {
                    "span1_text": datasets.Value("string"),
                    "span2_text": datasets.Value("string"),
                    "span1_index": datasets.Value("int32"),
                    "span2_index": datasets.Value("int32"),
                },
            }
        elif self.config.name == "csl":
            features = {
                "idx": datasets.Value("int32"),
                "corpus_id": datasets.Value("int32"),
                "abst": datasets.Value("string"),
                "label": datasets.features.ClassLabel(names=self.config.label_classes),
                "keyword": datasets.Sequence(datasets.Value("string")),
            }
        elif self.config.name in ["cmrc2018", "drcd"]:
            features = {
                "id": datasets.Value("string"),
                "context": datasets.Value("string"),
                "question": datasets.Value("string"),
                "answers": datasets.Sequence(
                    {
                        "text": datasets.Value("string"),
                        "answer_start": datasets.Value("int32"),
                    }
                ),
            }
        elif self.config.name == "chid":
            features = {
                "idx": datasets.Value("int32"),
                "candidates": datasets.Sequence(datasets.Value("string")),
                "content": datasets.Sequence(datasets.Value("string")),
                "answers": datasets.features.Sequence(
                    {
                        "text": datasets.Value("string"),
                        "candidate_id": datasets.Value("int32"),
                    }
                ),
            }
        elif self.config.name == "c3":
            features = {
                "id": datasets.Value("int32"),
                "context": datasets.Sequence(datasets.Value("string")),
                "question": datasets.Value("string"),
                "choice": datasets.Sequence(datasets.Value("string")),
                "answer": datasets.Value("string"),
            }
        else:
            raise NotImplementedError(
                "This task is not implemented. If you believe"
                " this task was recently added to the CLUE benchmark, "
                "please open a GitHub issue and we will add it."
            )

        return datasets.DatasetInfo(
            description=_CLUE_DESCRIPTION,
            features=datasets.Features(features),
            homepage=self.config.url,
            citation=self.config.citation + "\n" + _CLUE_CITATION,
        )

    def _split_generators(self, dl_manager):
        dl_dir = dl_manager.download_and_extract(self.config.data_url)
        data_dir = os.path.join(dl_dir, self.config.data_dir)
        test_split = datasets.SplitGenerator(
            name=datasets.Split.TEST,
            gen_kwargs={
                "data_file": os.path.join(
                    data_dir, "test.json" if self.config.name != "diagnostics" else "diagnostics_test.json"
                ),
                "split": "test",
            },
        )

        split_list = [test_split]

        if self.config.name != "diagnostics":
            train_split = datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                gen_kwargs={
                    "data_file": os.path.join(
                        data_dir or "", "train.json" if self.config.name != "c3" else "d-train.json"
                    ),
                    "split": "train",
                },
            )
            val_split = datasets.SplitGenerator(
                name=datasets.Split.VALIDATION,
                gen_kwargs={
                    "data_file": os.path.join(
                        data_dir or "", "dev.json" if self.config.name != "c3" else "d-dev.json"
                    ),
                    "split": "dev",
                },
            )
            split_list += [train_split, val_split]

        if self.config.name == "cmrc2018":
            split_list.append(
                datasets.SplitGenerator(
                    name=datasets.Split("trial"),
                    gen_kwargs={
                        "data_file": os.path.join(data_dir or "", "trial.json"),
                        "split": "trial",
                    },
                )
            )

        return split_list

    def _generate_examples(self, data_file, split):
        process_label = self.config.process_label
        label_classes = self.config.label_classes

        if self.config.name == "chid" and split != "test":
            answer_file = os.path.join(os.path.dirname(data_file), "{}_answer.json".format(split))
            answer_dict = json.load(open(answer_file, encoding="utf8"))

        if self.config.name == "c3":
            if split == "test":
                files = [data_file]
            else:
                data_dir = os.path.dirname(data_file)
                files = [os.path.join(data_dir, "{}-{}.json".format(typ, split)) for typ in ["d", "m"]]
            data = []
            for f in files:
                data_subset = json.load(open(f, encoding="utf8"))
                data += data_subset
            for idx, entry in enumerate(data):
                for question in entry[1]:
                    example = {
                        "id": idx if split != "test" else int(question["id"]),
                        "context": entry[0],
                        "question": question["question"],
                        "choice": question["choice"],
                        "answer": question["answer"] if split != "test" else "",
                    }
                    yield example["id"], example

        else:
            with open(data_file, encoding="utf8") as f:
                if self.config.name in ["cmrc2018", "drcd"]:
                    data = json.load(f)
                    for example in data["data"]:
                        for paragraph in example["paragraphs"]:
                            context = paragraph["context"].strip()
                            for qa in paragraph["qas"]:
                                question = qa["question"].strip()
                                id_ = qa["id"]

                                answer_starts = [answer["answer_start"] for answer in qa["answers"]]
                                answers = [answer["text"].strip() for answer in qa["answers"]]

                                yield id_, {
                                    "context": context,
                                    "question": question,
                                    "id": id_,
                                    "answers": {
                                        "answer_start": answer_starts,
                                        "text": answers,
                                    },
                                }

                else:
                    for n, line in enumerate(f):
                        row = json.loads(line)
                        example = {feat: row[col] for feat, col in six.iteritems(self.config.text_features)}
                        example["idx"] = n if self.config.name != "diagnostics" else int(row["index"])
                        if self.config.name == "chid":  # CHID has a separate gold label file
                            contents = example["content"]
                            candidates = example["candidates"]
                            idiom_list = []
                            if split != "test":
                                for content in contents:
                                    idioms = re.findall(r"#idiom\d+#", content)
                                    for idiom in idioms:
                                        idiom_list.append(
                                            {
                                                "candidate_id": answer_dict[idiom],
                                                "text": candidates[answer_dict[idiom]],
                                            }
                                        )
                            example["answers"] = idiom_list

                        elif self.config.label_column in row:
                            label = row[self.config.label_column]
                            # Notice: some labels in CMNLI and OCNLI are invalid. We drop these data.
                            if self.config.name in ["cmnli", "ocnli"] and label == "-":
                                continue
                            # For some tasks, the label is represented as 0 and 1 in the tsv
                            # files and needs to be cast to integer to work with the feature.
                            if label_classes and label not in label_classes:
                                label = int(label) if label else None
                            example["label"] = process_label(label)
                        else:
                            example["label"] = process_label(-1)

                        # Filter out corrupted rows.
                        for value in six.itervalues(example):
                            if value is None:
                                break
                        else:
                            yield example["idx"], example
