"""The Adversarial GLUE (AdvGLUE) benchmark.
Homepage: https://adversarialglue.github.io/
"""
import json
import os
import textwrap

import datasets


_ADV_GLUE_CITATION = """\
@article{Wang2021AdversarialGA,
  title={Adversarial GLUE: A Multi-Task Benchmark for Robustness Evaluation of Language Models},
  author={Boxin Wang and Chejian Xu and Shuohang Wang and Zhe Gan and Yu Cheng and Jianfeng Gao and Ahmed Hassan Awadallah and B. Li},
  journal={ArXiv},
  year={2021},
  volume={abs/2111.02840}
}
"""

_ADV_GLUE_DESCRIPTION = """\
Adversarial GLUE Benchmark (AdvGLUE) is a comprehensive robustness evaluation benchmark
that focuses on the adversarial robustness evaluation of language models. It covers five
natural language understanding tasks from the famous GLUE tasks and is an adversarial
version of GLUE benchmark.
"""

_MNLI_BASE_KWARGS = dict(
    text_features={
        "premise": "premise",
        "hypothesis": "hypothesis",
    },
    label_classes=["entailment", "neutral", "contradiction"],
    label_column="label",
    data_url="https://dl.fbaipublicfiles.com/glue/data/MNLI.zip",
    data_dir="MNLI",
    citation=textwrap.dedent(
        """\
      @InProceedings{N18-1101,
        author = "Williams, Adina
                  and Nangia, Nikita
                  and Bowman, Samuel",
        title = "A Broad-Coverage Challenge Corpus for
                 Sentence Understanding through Inference",
        booktitle = "Proceedings of the 2018 Conference of
                     the North American Chapter of the
                     Association for Computational Linguistics:
                     Human Language Technologies, Volume 1 (Long
                     Papers)",
        year = "2018",
        publisher = "Association for Computational Linguistics",
        pages = "1112--1122",
        location = "New Orleans, Louisiana",
        url = "http://aclweb.org/anthology/N18-1101"
      }
      @article{bowman2015large,
        title={A large annotated corpus for learning natural language inference},
        author={Bowman, Samuel R and Angeli, Gabor and Potts, Christopher and Manning, Christopher D},
        journal={arXiv preprint arXiv:1508.05326},
        year={2015}
      }"""
    ),
    url="http://www.nyu.edu/projects/bowman/multinli/",
)

ADVGLUE_DEV_URL = "https://adversarialglue.github.io/dataset/dev.zip"


class AdvGlueConfig(datasets.BuilderConfig):
    """BuilderConfig for Adversarial GLUE."""

    def __init__(
        self,
        text_features,
        label_column,
        data_url,
        data_dir,
        citation,
        url,
        label_classes=None,
        process_label=lambda x: x,
        **kwargs,
    ):
        """BuilderConfig for Adversarial GLUE.

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
        super(AdvGlueConfig, self).__init__(version=datasets.Version("1.0.0", ""), **kwargs)
        self.text_features = text_features
        self.label_column = label_column
        self.label_classes = label_classes
        self.data_url = data_url
        self.data_dir = data_dir
        self.citation = citation
        self.url = url
        self.process_label = process_label


ADVGLUE_BUILDER_CONFIGS = [
    AdvGlueConfig(
        name="adv_sst2",
        description=textwrap.dedent(
            """Adversarial version of SST-2.
            The Stanford Sentiment Treebank consists of sentences from movie reviews and
            human annotations of their sentiment. The task is to predict the sentiment of a
            given sentence. We use the two-way (positive/negative) class split, and use only
            sentence-level labels."""
        ),
        text_features={"sentence": "sentence"},
        label_classes=["negative", "positive"],
        label_column="label",
        data_url="https://dl.fbaipublicfiles.com/glue/data/SST-2.zip",
        data_dir="SST-2",
        citation=textwrap.dedent(
            """\
            @inproceedings{socher2013recursive,
              title={Recursive deep models for semantic compositionality over a sentiment treebank},
              author={Socher, Richard and Perelygin, Alex and Wu, Jean and Chuang, Jason and Manning, Christopher D and Ng, Andrew and Potts, Christopher},
              booktitle={Proceedings of the 2013 conference on empirical methods in natural language processing},
              pages={1631--1642},
              year={2013}
            }"""
        ),
        url="https://datasets.stanford.edu/sentiment/index.html",
    ),
    AdvGlueConfig(
        name="adv_qqp",
        description=textwrap.dedent(
            """Adversarial version of QQP.
            The Quora Question Pairs2 dataset is a collection of question pairs from the
            community question-answering website Quora. The task is to determine whether a
            pair of questions are semantically equivalent."""
        ),
        text_features={
            "question1": "question1",
            "question2": "question2",
        },
        label_classes=["not_duplicate", "duplicate"],
        label_column="label",
        data_url="https://dl.fbaipublicfiles.com/glue/data/QQP-clean.zip",
        data_dir="QQP",
        citation=textwrap.dedent(
            """\
          @online{WinNT,
            author = {Iyer, Shankar and Dandekar, Nikhil and Csernai, Kornel},
            title = {First Quora Dataset Release: Question Pairs},
            year = {2017},
            url = {https://data.quora.com/First-Quora-Dataset-Release-Question-Pairs},
            urldate = {2019-04-03}
          }"""
        ),
        url="https://data.quora.com/First-Quora-Dataset-Release-Question-Pairs",
    ),
    AdvGlueConfig(
        name="adv_mnli",
        description=textwrap.dedent(
            """Adversarial version of MNLI.
            The Multi-Genre Natural Language Inference Corpus is a crowdsourced
            collection of sentence pairs with textual entailment annotations. Given a premise sentence
            and a hypothesis sentence, the task is to predict whether the premise entails the hypothesis
            (entailment), contradicts the hypothesis (contradiction), or neither (neutral). The premise sentences are
            gathered from ten different sources, including transcribed speech, fiction, and government reports.
            We use the standard test set, for which we obtained private labels from the authors, and evaluate
            on both the matched (in-domain) and mismatched (cross-domain) section. We also use and recommend
            the SNLI corpus as 550k examples of auxiliary training data."""
        ),
        **_MNLI_BASE_KWARGS,
    ),
    AdvGlueConfig(
        name="adv_mnli_mismatched",
        description=textwrap.dedent(
            """Adversarial version of MNLI-mismatched.
          The mismatched validation and test splits from MNLI.
          See the "mnli" BuilderConfig for additional information."""
        ),
        **_MNLI_BASE_KWARGS,
    ),
    AdvGlueConfig(
        name="adv_qnli",
        description=textwrap.dedent(
            """Adversarial version of QNLI.
            The Stanford Question Answering Dataset is a question-answering
            dataset consisting of question-paragraph pairs, where one of the sentences in the paragraph (drawn
            from Wikipedia) contains the answer to the corresponding question (written by an annotator). We
            convert the task into sentence pair classification by forming a pair between each question and each
            sentence in the corresponding context, and filtering out pairs with low lexical overlap between the
            question and the context sentence. The task is to determine whether the context sentence contains
            the answer to the question. This modified version of the original task removes the requirement that
            the model select the exact answer, but also removes the simplifying assumptions that the answer
            is always present in the input and that lexical overlap is a reliable cue."""
        ),  # pylint: disable=line-too-long
        text_features={
            "question": "question",
            "sentence": "sentence",
        },
        label_classes=["entailment", "not_entailment"],
        label_column="label",
        data_url="https://dl.fbaipublicfiles.com/glue/data/QNLIv2.zip",
        data_dir="QNLI",
        citation=textwrap.dedent(
            """\
            @article{rajpurkar2016squad,
              title={Squad: 100,000+ questions for machine comprehension of text},
              author={Rajpurkar, Pranav and Zhang, Jian and Lopyrev, Konstantin and Liang, Percy},
              journal={arXiv preprint arXiv:1606.05250},
              year={2016}
            }"""
        ),
        url="https://rajpurkar.github.io/SQuAD-explorer/",
    ),
    AdvGlueConfig(
        name="adv_rte",
        description=textwrap.dedent(
            """Adversarial version of RTE.
            The Recognizing Textual Entailment (RTE) datasets come from a series of annual textual
            entailment challenges. We combine the data from RTE1 (Dagan et al., 2006), RTE2 (Bar Haim
            et al., 2006), RTE3 (Giampiccolo et al., 2007), and RTE5 (Bentivogli et al., 2009).4 Examples are
            constructed based on news and Wikipedia text. We convert all datasets to a two-class split, where
            for three-class datasets we collapse neutral and contradiction into not entailment, for consistency."""
        ),  # pylint: disable=line-too-long
        text_features={
            "sentence1": "sentence1",
            "sentence2": "sentence2",
        },
        label_classes=["entailment", "not_entailment"],
        label_column="label",
        data_url="https://dl.fbaipublicfiles.com/glue/data/RTE.zip",
        data_dir="RTE",
        citation=textwrap.dedent(
            """\
            @inproceedings{dagan2005pascal,
              title={The PASCAL recognising textual entailment challenge},
              author={Dagan, Ido and Glickman, Oren and Magnini, Bernardo},
              booktitle={Machine Learning Challenges Workshop},
              pages={177--190},
              year={2005},
              organization={Springer}
            }
            @inproceedings{bar2006second,
              title={The second pascal recognising textual entailment challenge},
              author={Bar-Haim, Roy and Dagan, Ido and Dolan, Bill and Ferro, Lisa and Giampiccolo, Danilo and Magnini, Bernardo and Szpektor, Idan},
              booktitle={Proceedings of the second PASCAL challenges workshop on recognising textual entailment},
              volume={6},
              number={1},
              pages={6--4},
              year={2006},
              organization={Venice}
            }
            @inproceedings{giampiccolo2007third,
              title={The third pascal recognizing textual entailment challenge},
              author={Giampiccolo, Danilo and Magnini, Bernardo and Dagan, Ido and Dolan, Bill},
              booktitle={Proceedings of the ACL-PASCAL workshop on textual entailment and paraphrasing},
              pages={1--9},
              year={2007},
              organization={Association for Computational Linguistics}
            }
            @inproceedings{bentivogli2009fifth,
              title={The Fifth PASCAL Recognizing Textual Entailment Challenge.},
              author={Bentivogli, Luisa and Clark, Peter and Dagan, Ido and Giampiccolo, Danilo},
              booktitle={TAC},
              year={2009}
            }"""
        ),
        url="https://aclweb.org/aclwiki/Recognizing_Textual_Entailment",
    ),
]


class AdvGlue(datasets.GeneratorBasedBuilder):
    """The General Language Understanding Evaluation (GLUE) benchmark."""

    DATASETS = ["adv_sst2", "adv_qqp", "adv_mnli", "adv_mnli_mismatched", "adv_qnli", "adv_rte"]
    BUILDER_CONFIGS = ADVGLUE_BUILDER_CONFIGS

    def _info(self):
        features = {text_feature: datasets.Value("string") for text_feature in self.config.text_features.keys()}
        if self.config.label_classes:
            features["label"] = datasets.features.ClassLabel(names=self.config.label_classes)
        else:
            features["label"] = datasets.Value("float32")
        features["idx"] = datasets.Value("int32")
        return datasets.DatasetInfo(
            description=_ADV_GLUE_DESCRIPTION,
            features=datasets.Features(features),
            homepage="https://adversarialglue.github.io/",
            citation=_ADV_GLUE_CITATION,
        )

    def _split_generators(self, dl_manager):
        assert self.config.name in AdvGlue.DATASETS
        data_dir = dl_manager.download_and_extract(ADVGLUE_DEV_URL)
        data_file = os.path.join(data_dir, "dev", "dev.json")
        return [
            datasets.SplitGenerator(
                name=datasets.Split.VALIDATION,
                gen_kwargs={
                    "data_file": data_file,
                },
            )
        ]

    def _generate_examples(self, data_file):
        # We name splits 'adv_sst2' instead of 'sst2' so as not to be confused
        # with the original SST-2. Here they're named like 'sst2' so we have to
        # remove the 'adv_' prefix.
        config_key = self.config.name.replace("adv_", "")
        if config_key == "mnli_mismatched":
            # and they name this split differently.
            config_key = "mnli-mm"
        data = json.loads(open(data_file).read())
        for row in data[config_key]:
            example = {feat: row[col] for feat, col in self.config.text_features.items()}
            example["label"] = self.config.process_label(row[self.config.label_column])
            example["idx"] = row["idx"]
            yield example["idx"], example
