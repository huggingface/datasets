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
"""The French Language Understanding Evaluation (FLUE) benchmark."""

from __future__ import absolute_import, division, print_function

import csv
import os
import re
import textwrap
import unicodedata
from shutil import copyfile

import six
from lxml import etree

import datasets


_FLUE_CITATION = """\
@misc{le2019flaubert,
    title={FlauBERT: Unsupervised Language Model Pre-training for French},
    author={Hang Le and Loïc Vial and Jibril Frej and Vincent Segonne and Maximin Coavoux and Benjamin Lecouteux and Alexandre Allauzen and Benoît Crabbé and Laurent Besacier and Didier Schwab},
    year={2019},
    eprint={1912.05372},
    archivePrefix={arXiv},
    primaryClass={cs.CL}
}
"""

_FLUE_DESCRIPTION = """\
FLUE is an evaluation setup for French NLP systems similar to the popular GLUE benchmark. The goal is to enable further reproducible experiments in the future and to share models and progress on the French language.
"""


class FlueConfig(datasets.BuilderConfig):
    """BuilderConfig for FLUE."""

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
        """BuilderConfig for FLUE.

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
        super(FlueConfig, self).__init__(version=datasets.Version("1.0.0", ""), **kwargs)
        self.text_features = text_features
        self.label_column = label_column
        self.label_classes = label_classes
        self.data_url = data_url
        self.data_dir = data_dir
        self.citation = citation
        self.url = url
        self.process_label = process_label


class Flue(datasets.GeneratorBasedBuilder):
    """The French Language Understanding Evaluation (FLUE) benchmark."""

    BUILDER_CONFIGS = [
        FlueConfig(
            name="CLS",
            description=textwrap.dedent(
                """\
            This is a binary classification task. It consists in classifying Amazon reviews for three product categories:
            books, DVD, and music. Each sample contains a review text and the associated rating from 1 to 5 stars. Reviews
            rated above 3 is labeled as positive, and those rated less than 3 is labeled as negative. The train and test sets
            are balanced, including around 1k positive and 1k negative reviews for a total of 2k reviews in each dataset. Only
            the French portion is taken to create the binary text classification task in FLUE and report the accuracy on the test set."""
            ),
            text_features={"text": "text"},
            label_classes=["negative", "positive"],
            label_column="label",
            data_url="https://zenodo.org/record/3251672/files/cls-acl10-unprocessed.tar.gz",
            data_dir="",
            url="",
            citation="",
        ),
        FlueConfig(
            name="PAWS-X",
            description=textwrap.dedent(
                """\
            This dataset contains 23,659 human translated PAWS evaluation pairs and 296,406 machine translated training
            pairs in six typologically distinct languages: French, Spanish, German, Chinese, Japanese, and Korean. All
            translated pairs are sourced from examples in PAWS-Wiki. Only the related dataset for French is taken to perform
            the paraphrasing task and report the accuracy on the test set."""
            ),
            text_features={"sentence1": "sentence1", "sentence2": "sentence2"},
            data_url="https://storage.googleapis.com/paws/pawsx/x-final.tar.gz",
            label_column="label",
            data_dir="",
            url="https://github.com/google-research-datasets/paws/tree/master/pawsx",
            citation=textwrap.dedent(
                """\
            @InProceedings{pawsx2019emnlp,
                title = {{PAWS-X: A Cross-lingual Adversarial Dataset for Paraphrase Identification}},
                author = {Yang, Yinfei and Zhang, Yuan and Tar, Chris and Baldridge, Jason},
                booktitle = {Proc. of EMNLP},
                year = {2019}
            }"""
            ),
        ),
        FlueConfig(
            name="XNLI",
            description=textwrap.dedent(
                """
                The Cross-lingual Natural Language Inference (XNLI) corpus is a crowd-sourced collection of 5,000 test and
                2,500 dev pairs for the MultiNLI corpus. The pairs are annotated with textual entailment and translated into
                14 languages: French, Spanish, German, Greek, Bulgarian, Russian, Turkish, Arabic, Vietnamese, Thai, Chinese,
                Hindi, Swahili and Urdu. This results in 112.5k annotated pairs. Each premise can be associated with the
                corresponding hypothesis in the 15 languages, summing up to more than 1.5M combinations. The corpus is made to
                evaluate how to perform inference in any language (including low-resources ones like Swahili or Urdu) when only
                English NLI data is available at training time. One solution is cross-lingual sentence encoding, for which XNLI
                is an evaluation benchmark. Only the related datasets for French is taken to perform the NLI task and report
                the accuracy on the test set."""
            ),
            text_features={"premise": "premise", "hypo": "hypo"},
            data_url={
                "train": "https://dl.fbaipublicfiles.com/XNLI/XNLI-MT-1.0.zip",
                "dev_test": "https://dl.fbaipublicfiles.com/XNLI/XNLI-1.0.zip",
            },
            label_classes=["contradiction", "entailment", "neutral"],
            label_column="label",
            data_dir="",
            url="https://www.nyu.edu/projects/bowman/xnli/",
            citation=textwrap.dedent(
                """\
                @InProceedings{conneau2018xnli,
                author = {Conneau, Alexis
                                and Rinott, Ruty
                                and Lample, Guillaume
                                and Williams, Adina
                                and Bowman, Samuel R.
                                and Schwenk, Holger
                                and Stoyanov, Veselin},
                title = {XNLI: Evaluating Cross-lingual Sentence Representations},
                booktitle = {Proceedings of the 2018 Conference on Empirical Methods
                            in Natural Language Processing},
                year = {2018},
                publisher = {Association for Computational Linguistics},
                location = {Brussels, Belgium},
                }"""
            ),
        ),
        FlueConfig(
            name="WSD-V",
            description=textwrap.dedent(
                """
                French Verb Sense Disambiguation task."""
            ),
            text_features={
                "sentence": "sentence",
                "pos_tags": "pos_tags",
                "lemmas": "lemmas",
                "fine_pos_tags": "fine_pos_tags",
            },
            data_url="http://www.llf.cnrs.fr/dataset/fse/FSE-1.1-10_12_19.tar.gz",
            label_classes=["disambiguate_tokens_ids", "disambiguate_labels"],
            label_column="disambiguate_labels",
            data_dir="FSE-1.1-191210",
            url="http://www.llf.cnrs.fr/dataset/fse/",
            citation="",
        ),
    ]

    def _info(self):
        if self.config.name == "CLS" or self.config.name == "XNLI":
            features = {
                text_feature: datasets.Value("string") for text_feature in six.iterkeys(self.config.text_features)
            }
            features[self.config.label_column] = datasets.features.ClassLabel(names=self.config.label_classes)
            features["idx"] = datasets.Value("int32")
        elif self.config.name == "WSD-V":
            features = {
                text_feature: datasets.Sequence(datasets.Value("string"))
                for text_feature in six.iterkeys(self.config.text_features)
            }
            features["fine_pos_tags"] = datasets.Sequence(
                datasets.features.ClassLabel(
                    names=[
                        "DET",
                        "P+D",
                        "CC",
                        "VS",
                        "P",
                        "CS",
                        "NC",
                        "NPP",
                        "ADJWH",
                        "VINF",
                        "VPP",
                        "ADVWH",
                        "PRO",
                        "V",
                        "CLO",
                        "PREF",
                        "VPR",
                        "PROREL",
                        "ADV",
                        "PROWH",
                        "N",
                        "DETWH",
                        "ADJ",
                        "P+PRO",
                        "ET",
                        "VIMP",
                        "CLS",
                        "PONCT",
                        "I",
                        "CLR",
                    ]
                )
            )
            features["pos_tags"] = datasets.Sequence(
                datasets.features.ClassLabel(
                    names=[
                        "V",
                        "PREF",
                        "P+D",
                        "I",
                        "A",
                        "P+PRO",
                        "PRO",
                        "P",
                        "anonyme",
                        "D",
                        "C",
                        "CL",
                        "ET",
                        "PONCT",
                        "ADV",
                        "N",
                    ]
                )
            )
            features["disambiguate_tokens_ids"] = datasets.Sequence(datasets.Value("int32"))
            features["disambiguate_labels"] = datasets.Sequence(datasets.Value("string"))
            features["idx"] = datasets.Value("string")
        else:
            features = {
                text_feature: datasets.Value("string") for text_feature in six.iterkeys(self.config.text_features)
            }
            features[self.config.label_column] = datasets.Value("int32")
            features["idx"] = datasets.Value("int32")
        return datasets.DatasetInfo(
            description=_FLUE_DESCRIPTION,
            features=datasets.Features(features),
            homepage=self.config.url,
            citation=self.config.citation + "\n" + _FLUE_CITATION,
        )

    def _split_generators(self, dl_manager):
        if self.config.name == "CLS":
            data_folder = dl_manager.download_and_extract(self.config.data_url)

            return [
                datasets.SplitGenerator(
                    name=datasets.Split.TRAIN,
                    gen_kwargs={
                        "data_file": os.path.join(data_folder, "cls-acl10-unprocessed", "fr"),
                        "split": "train",
                    },
                ),
                datasets.SplitGenerator(
                    name=datasets.Split.TEST,
                    gen_kwargs={
                        "data_file": os.path.join(data_folder, "cls-acl10-unprocessed", "fr"),
                        "split": "test",
                    },
                ),
            ]
        elif self.config.name == "PAWS-X":
            data_folder = dl_manager.download_and_extract(self.config.data_url)

            return [
                datasets.SplitGenerator(
                    name=datasets.Split.VALIDATION,
                    gen_kwargs={
                        "data_file": os.path.join(data_folder, "x-final", "fr", "dev_2k.tsv"),
                        "split": "",
                    },
                ),
                datasets.SplitGenerator(
                    name=datasets.Split.TEST,
                    gen_kwargs={
                        "data_file": os.path.join(data_folder, "x-final", "fr", "test_2k.tsv"),
                        "split": "",
                    },
                ),
                datasets.SplitGenerator(
                    name=datasets.Split.TRAIN,
                    gen_kwargs={
                        "data_file": os.path.join(data_folder, "x-final", "fr", "translated_train.tsv"),
                        "split": "",
                    },
                ),
            ]
        elif self.config.name == "XNLI":
            data_folder = dl_manager.download_and_extract(self.config.data_url)
            return [
                datasets.SplitGenerator(
                    name=datasets.Split.VALIDATION,
                    gen_kwargs={
                        "data_file": os.path.join(data_folder["dev_test"], "XNLI-1.0", "xnli.dev.tsv"),
                        "split": "dev",
                    },
                ),
                datasets.SplitGenerator(
                    name=datasets.Split.TEST,
                    gen_kwargs={
                        "data_file": os.path.join(data_folder["dev_test"], "XNLI-1.0", "xnli.test.tsv"),
                        "split": "test",
                    },
                ),
                datasets.SplitGenerator(
                    name=datasets.Split.TRAIN,
                    gen_kwargs={
                        "data_file": os.path.join(
                            data_folder["train"], "XNLI-MT-1.0", "multinli", "multinli.train.fr.tsv"
                        ),
                        "split": "train",
                    },
                ),
            ]
        elif self.config.name == "WSD-V":
            data_folder = dl_manager.download_and_extract(self.config.data_url)
            self._wsdv_prepare_data(os.path.join(data_folder, self.config.data_dir))

            return [
                datasets.SplitGenerator(
                    name=datasets.Split.TRAIN,
                    gen_kwargs={
                        "data_file": os.path.join(data_folder, self.config.data_dir),
                        "split": "train",
                    },
                ),
                datasets.SplitGenerator(
                    name=datasets.Split.TEST,
                    gen_kwargs={
                        "data_file": os.path.join(data_folder, self.config.data_dir),
                        "split": "test",
                    },
                ),
            ]

    def _generate_examples(self, data_file, split):
        if self.config.name == "CLS":
            for category in ["books", "dvd", "music"]:
                file_path = os.path.join(data_file, category, split + ".review")
                with open(file_path, "rt", encoding="utf-8") as f:
                    next(f)
                    id = 0
                    text = f.read()
                    for id_, line in enumerate(text.split("\n\n")):
                        if len(line) > 9:
                            id += 1
                            review_text, label = self._cls_extractor(line)
                            yield id_, {"idx": id, "text": review_text, "label": label}
        elif self.config.name == "PAWS-X":
            with open(data_file, encoding="utf-8") as f:
                data = csv.reader(f, delimiter="\t")
                next(data)  # skip header
                id = 0
                for id_, row in enumerate(data):
                    if len(row) == 4:
                        id += 1
                        yield id_, {
                            "idx": id,
                            "sentence1": self._cleaner(row[1]),
                            "sentence2": self._cleaner(row[2]),
                            "label": int(row[3].strip()),
                        }
        elif self.config.name == "XNLI":
            with open(data_file, encoding="utf-8") as f:
                data = csv.reader(f, delimiter="\t", quoting=csv.QUOTE_NONE)
                next(data)
                id = 0
                for id_, row in enumerate(data):
                    if split == "train":
                        id += 1
                        yield id_, {
                            "idx": id,
                            "premise": self._cleaner(row[0]),
                            "hypo": self._cleaner(row[1]),
                            "label": row[2].strip().replace("contradictory", "contradiction"),
                        }
                    else:
                        if row[0] == "fr":
                            id += 1
                            yield id_, {
                                "idx": id,
                                "premise": self._cleaner(row[6]),
                                "hypo": self._cleaner(row[7]),
                                "label": row[1].strip(),  # the label is already "contradiction" in the dev/test
                            }
        elif self.config.name == "WSD-V":
            wsd_rdr = WSDDatasetReader()
            for inst in wsd_rdr.read_from_data_dirs([os.path.join(data_file, split)]):
                yield inst[0], {
                    "idx": inst[0],
                    "sentence": inst[1],
                    "pos_tags": inst[2],
                    "lemmas": inst[3],
                    "fine_pos_tags": inst[4],
                    "disambiguate_tokens_ids": inst[5],
                    "disambiguate_labels": inst[6],
                }

    def _cls_extractor(self, line):
        """
        Extract review and label for CLS dataset
        from: https://github.com/getalp/Flaubert/blob/master/flue/extract_split_cls.py
        """
        m = re.search(r"(?<=<rating>)\d+.\d+(?=<\/rating>)", line)
        label = "positive" if int(float(m.group(0))) > 3 else "negative"  # rating == 3 are already removed
        category = re.search(r"(?<=<category>)\w+(?=<\/category>)", line)

        if category == "dvd":
            m = re.search(r"(?<=\/url><text>)(.|\n|\t|\f)+(?=\<\/title><summary>)", line)
        else:
            m = re.search(r"(?<=\/url><text>)(.|\n|\t|\f)+(?=\<\/text><title>)", line)

        review_text = m.group(0)

        return self._cleaner(review_text), label

    def _convert_to_unicode(self, text):
        """
        Converts `text` to Unicode (if it's not already), assuming UTF-8 input.
        from: https://github.com/getalp/Flaubert/blob/master/tools/clean_text.py
        """
        # six_ensure_text is copied from https://github.com/benjaminp/six
        def six_ensure_text(s, encoding="utf-8", errors="strict"):
            if isinstance(s, six.binary_type):
                return s.decode(encoding, errors)
            elif isinstance(s, six.text_type):
                return s
            else:
                raise TypeError("not expecting type '%s'" % type(s))

        return six_ensure_text(text, encoding="utf-8", errors="ignore")

    def _cleaner(self, text):
        """
        Clean up an input text
        from: https://github.com/getalp/Flaubert/blob/master/tools/clean_text.py
        """
        # Convert and normalize the unicode underlying representation
        text = self._convert_to_unicode(text)
        text = unicodedata.normalize("NFC", text)

        # Normalize whitespace characters and remove carriage return
        remap = {ord("\f"): " ", ord("\r"): "", ord("\n"): "", ord("\t"): ""}
        text = text.translate(remap)

        # Normalize URL links
        pattern = re.compile(r"(?:www|http)\S+|<\S+|\w+\/*>")
        text = re.sub(pattern, "", text)

        # remove multiple spaces in text
        pattern = re.compile(r"( ){2,}")
        text = re.sub(pattern, r" ", text)

        return text

    def _wsdv_prepare_data(self, dirpath):
        """ Get data paths from FSE dir"""
        paths = {}

        for f in os.listdir(dirpath):
            if f.startswith("FSE"):
                data = "test"
            else:
                data = "train"

            paths["_".join((data, f))] = os.path.join(dirpath, f)

        test_dirpath = os.path.join(dirpath, "test")
        os.makedirs(test_dirpath, exist_ok=True)
        train_dirpath = os.path.join(dirpath, "train")
        os.makedirs(train_dirpath, exist_ok=True)
        # copy FSE file to new test directory
        for k, v in paths.items():
            data = k.split("_")[0]
            filename = k.split("_")[1]
            copyfile(v, os.path.join(dirpath, data, filename))


# The WSDDatasetReader classes come from https://github.com/getalp/Flaubert/blob/master/flue/wsd/verbs/modules/dataset.py
class WSDDatasetReader:
    """ Class to read a WSD data directory. The directory should contain .data.xml and .gold.key.txt files"""

    def get_data_paths(self, indir):
        """ Get file paths from WSD dir """
        xml_fpath, gold_fpath = None, None

        for f in os.listdir(indir):
            if f.endswith(".data.xml"):
                xml_fpath = os.path.join(indir, f)
            if f.endswith(".gold.key.txt"):
                gold_fpath = os.path.join(indir, f)
        return xml_fpath, gold_fpath

    def read_gold(self, infile):
        """Read .gold.key.txt and return data as dict.
        :param infile: fpath to .gold.key.txt file
        :type infile: str
        :return: return data into dict format : {str(instance_id): set(label)}
        :rtype: dict
        """
        return {
            line.split()[0]: tuple(line.rstrip("\n").split()[1:])
            for line in open(infile, encoding="utf-8").readlines()
        }

    def read_from_data_dirs(self, data_dirs):
        """ Read WSD data and return as WSDDataset """
        for d in data_dirs:
            xml_fpath, gold_fpath = self.get_data_paths(d)

            # read gold file
            id2gold = self.read_gold(gold_fpath)

            sentences = self.read_sentences(d)

            # Parse xml
            tree = etree.parse(xml_fpath)
            corpus = tree.getroot()

            # process data
            # iterate over document
            for text in corpus:
                # iterates over sentences
                for sentence in text:
                    sent_id = sentence.get("id")  # sentence id
                    sent = next(sentences)  # get sentence
                    pos_tags = []
                    lemmas = []
                    fine_pos_tags = []
                    disambiguate_tokens_ids = []
                    disambiguate_labels = []
                    tok_idx = 0

                    # iterate over tokens
                    for tok in sentence:
                        lemma, pos, fine_pos_tag = tok.get("lemma"), tok.get("pos"), tok.get("fine_pos")

                        pos_tags.append(pos)
                        lemmas.append(lemma)
                        fine_pos_tags.append(fine_pos_tag)
                        wf = tok.text
                        subtokens = wf.split(" ")

                        # add sense annotated token
                        if tok.tag == "instance":
                            id = tok.get("id")

                            target_labels = id2gold[id]
                            target_first_label = target_labels[0]

                            # We focus on the head of the target mwe instance
                            if pos == "VERB":
                                tgt_idx = tok_idx  # head is mostly the first token as most mwe verb targets are phrasal verbs (i.g lift up)
                            else:
                                tgt_idx = (
                                    tok_idx + len(subtokens) - 1
                                )  # other pos head are generally the last token of the mwe (i.g European Union)

                            disambiguate_tokens_ids.append(tgt_idx)
                            disambiguate_labels.append(target_first_label)

                        tok_idx += 1

                    yield (
                        sent_id,
                        sent,
                        pos_tags,
                        lemmas,
                        fine_pos_tags,
                        disambiguate_tokens_ids,
                        disambiguate_labels,
                    )

    def read_sentences(self, data_dir, keep_mwe=True):
        """ Read sentences from WSD data"""

        xml_fpath, _ = self.get_data_paths(data_dir)
        return self.read_sentences_from_xml(xml_fpath, keep_mwe=keep_mwe)

    def read_sentences_from_xml(self, infile, keep_mwe=False):
        """ Read sentences from xml file """

        # Parse xml
        tree = etree.parse(infile)
        corpus = tree.getroot()

        for text in corpus:
            for sentence in text:
                if keep_mwe:
                    sent = [tok.text.replace(" ", "_") for tok in sentence]
                else:
                    sent = [subtok for tok in sentence for subtok in tok.text.split(" ")]
                yield sent

    def read_target_keys(self, infile):
        """ Read target keys """
        return [x.rstrip("\n") for x in open(infile, encoding="utf-8").readlines()]
