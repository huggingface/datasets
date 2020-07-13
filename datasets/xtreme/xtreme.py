"""TODO(xtreme): Add a description here."""

from __future__ import absolute_import, division, print_function

import csv
import glob
import json
import os
import textwrap

import six

import nlp


# TODO(xtreme): BibTeX citation
_CITATION = """\
@article{hu2020xtreme,
      author    = {Junjie Hu and Sebastian Ruder and Aditya Siddhant and Graham Neubig and Orhan Firat and Melvin Johnson},
      title     = {XTREME: A Massively Multilingual Multi-task Benchmark for Evaluating Cross-lingual Generalization},
      journal   = {CoRR},
      volume    = {abs/2003.11080},
      year      = {2020},
      archivePrefix = {arXiv},
      eprint    = {2003.11080}
}
"""

# TODO(xtrem):
_DESCRIPTION = """\
The Cross-lingual TRansfer Evaluation of Multilingual Encoders (XTREME) benchmark is a benchmark for the evaluation of
the cross-lingual generalization ability of pre-trained multilingual models. It covers 40 typologically diverse languages
(spanning 12 language families) and includes nine tasks that collectively require reasoning about different levels of
syntax and semantics. The languages in XTREME are selected to maximize language diversity, coverage in existing tasks,
and availability of training data. Among these are many under-studied languages, such as the Dravidian languages Tamil
(spoken in southern India, Sri Lanka, and Singapore), Telugu and Malayalam (spoken mainly in southern India), and the
Niger-Congo languages Swahili and Yoruba, spoken in Africa.
"""
_MLQA_LANG = ["ar", "de", "vi", "zh", "en", "es", "hi"]
_XQUAD_LANG = ["ar", "de", "vi", "zh", "en", "es", "hi", "el", "ru", "th", "tr"]
_PAWSX_LANG = ["de", "en", "es", "fr", "ja", "ko", "zh"]
_BUCC_LANG = ["de", "fr", "zh", "ru"]
_TATOEBA_LANG = [
    "afr",
    "ara",
    "ben",
    "bul",
    "deu",
    "cmn",
    "ell",
    "est",
    "eus",
    "fin",
    "fra",
    "heb",
    "hin",
    "hun",
    "ind",
    "ita",
    "jav",
    "jpn",
    "kat",
    "kaz",
    "kor",
    "mal",
    "mar",
    "nld",
    "pes",
    "por",
    "rus",
    "spa",
    "swh",
    "tam",
    "tgl",
    "tha",
    "tur",
    "urd",
    "vie",
]

_UD_POS_LANG = [
    "Afrikaans",
    "Arabic",
    "Basque",
    "Bulgarian",
    "Dutch",
    "English",
    "Estonian",
    "Finnish",
    "French",
    "German",
    "Greek",
    "Hebrew",
    "Hindi",
    "Hungarian",
    "Indonesian",
    "Italian",
    "Japanese",
    "Kazakh",
    "Korean",
    "Chinese",
    "Marathi",
    "Persian",
    "Portuguese",
    "Russian",
    "Spanish",
    "Tagalog",
    "Tamil",
    "Telugu",
    "Thai",
    "Turkish",
    "Urdu",
    "Vietnamese",
    "Yoruba",
]
_PAN_X_LANG = [
    "af",
    "ar",
    "bg",
    "bn",
    "de",
    "el",
    "en",
    "es",
    "et",
    "eu",
    "fa",
    "fi",
    "fr",
    "he",
    "hi",
    "hu",
    "id",
    "it",
    "ja",
    "jv",
    "ka",
    "kk",
    "ko",
    "ml",
    "mr",
    "ms",
    "my",
    "nl",
    "pt",
    "ru",
    "sw",
    "ta",
    "te",
    "th",
    "tl",
    "tr",
    "ur",
    "vi",
    "yo",
    "zh",
]
_PAN_X_FOLDER = "AmazonPhotos.zip"
_NAMES = ["XNLI", "tydiqa", "SQuAD"]
for lang in _PAN_X_LANG:
    _NAMES.append("PAN-X.{}".format(lang))
for lang1 in _MLQA_LANG:
    for lang2 in _MLQA_LANG:
        _NAMES.append("MLQA.{}.{}".format(lang1, lang2))
for lang in _XQUAD_LANG:
    _NAMES.append("XQuAD.{}".format(lang))
for lang in _BUCC_LANG:
    _NAMES.append("bucc18.{}".format(lang))
for lang in _PAWSX_LANG:
    _NAMES.append("PAWS-X.{}".format(lang))
for lang in _TATOEBA_LANG:
    _NAMES.append("tatoeba.{}".format(lang))
for lang in _UD_POS_LANG:
    _NAMES.append("udpos.{}".format(lang))

_DESCRIPTIONS = {
    "tydiqa": textwrap.dedent(
        """Gold passage task (GoldP): Given a passage that is guaranteed to contain the
             answer, predict the single contiguous span of characters that answers the question. This is more similar to
             existing reading comprehension datasets (as opposed to the information-seeking task outlined above).
             This task is constructed with two goals in mind: (1) more directly comparing with prior work and (2) providing
             a simplified way for researchers to use TyDi QA by providing compatibility with existing code for SQuAD 1.1,
             XQuAD, and MLQA. Toward these goals, the gold passage task differs from the primary task in several ways:
             only the gold answer passage is provided rather than the entire Wikipedia article;
             unanswerable questions have been discarded, similar to MLQA and XQuAD;
             we evaluate with the SQuAD 1.1 metrics like XQuAD; and
            Thai and Japanese are removed since the lack of whitespace breaks some tools.
             """
    ),
    "XNLI": textwrap.dedent(
        """
          The Cross-lingual Natural Language Inference (XNLI) corpus is a crowd-sourced collection of 5,000 test and
          2,500 dev pairs for the MultiNLI corpus. The pairs are annotated with textual entailment and translated into
          14 languages: French, Spanish, German, Greek, Bulgarian, Russian, Turkish, Arabic, Vietnamese, Thai, Chinese,
          Hindi, Swahili and Urdu. This results in 112.5k annotated pairs. Each premise can be associated with the
          corresponding hypothesis in the 15 languages, summing up to more than 1.5M combinations. The corpus is made to
          evaluate how to perform inference in any language (including low-resources ones like Swahili or Urdu) when only
          English NLI data is available at training time. One solution is cross-lingual sentence encoding, for which XNLI
          is an evaluation benchmark."""
    ),
    "PAWS-X": textwrap.dedent(
        """
          This dataset contains 23,659 human translated PAWS evaluation pairs and 296,406 machine translated training
          pairs in six typologically distinct languages: French, Spanish, German, Chinese, Japanese, and Korean. All
          translated pairs are sourced from examples in PAWS-Wiki."""
    ),
    "XQuAD": textwrap.dedent(
        """\
          XQuAD (Cross-lingual Question Answering Dataset) is a benchmark dataset for evaluating cross-lingual question
          answering performance. The dataset consists of a subset of 240 paragraphs and 1190 question-answer pairs from
          the development set of SQuAD v1.1 (Rajpurkar et al., 2016) together with their professional translations into
          ten languages: Spanish, German, Greek, Russian, Turkish, Arabic, Vietnamese, Thai, Chinese, and Hindi. Consequently,
          the dataset is entirely parallel across 11 languages."""
    ),
    "MLQA": textwrap.dedent(
        """\
          MLQA (MultiLingual Question Answering) is a benchmark dataset for evaluating cross-lingual question answering performance.
    MLQA consists of over 5K extractive QA instances (12K in English) in SQuAD format in seven languages - English, Arabic,
    German, Spanish, Hindi, Vietnamese and Simplified Chinese. MLQA is highly parallel, with QA instances parallel between
    4 different languages on average."""
    ),
    "tatoeba": textwrap.dedent(
        """\
          his data is extracted from the Tatoeba corpus, dated Saturday 2018/11/17.

          For each languages, we have selected 1000 English sentences and their translations, if available. Please check
          this paper for a description of the languages, their families and scripts as well as baseline results.

          Please note that the English sentences are not identical for all language pairs. This means that the results are
          not directly comparable across languages. In particular, the sentences tend to have less variety for several
          low-resource languages, e.g. "Tom needed water", "Tom needs water", "Tom is getting water", ...
                    """
    ),
    "bucc18": textwrap.dedent(
        """Building and Using Comparable Corpora
          """
    ),
    "udpos": textwrap.dedent(
        """\
    Universal Dependencies (UD) is a framework for consistent annotation of grammar (parts of speech, morphological
    features, and syntactic dependencies) across different human languages. UD is an open community effort with over 200
    contributors producing more than 100 treebanks in over 70 languages. If you’re new to UD, you should start by reading
    the first part of the Short Introduction and then browsing the annotation guidelines.
    """
    ),
    "SQuAD": textwrap.dedent(
        """\
    Stanford Question Answering Dataset (SQuAD) is a reading comprehension \
    dataset, consisting of questions posed by crowdworkers on a set of Wikipedia \
    articles, where the answer to every question is a segment of text, or span, \
    from the corresponding reading passage, or the question might be unanswerable."""
    ),
    "PAN-X": textwrap.dedent(
        """\
    The WikiANN dataset (Pan et al. 2017) is a dataset with NER annotations for PER, ORG and LOC. It has been
    constructed using the linked entities in Wikipedia pages for 282 different languages including Danish. The dataset
    can be loaded with the DaNLP package:"""
    ),
}
_CITATIONS = {
    "tydiqa": textwrap.dedent(
        (
            """\
            @article{tydiqa,
              title   = {TyDi QA: A Benchmark for Information-Seeking Question Answering in Typologically Diverse Languages},
              author  = {Jonathan H. Clark and Eunsol Choi and Michael Collins and Dan Garrette and Tom Kwiatkowski and Vitaly Nikolaev and Jennimaria Palomaki}
              year    = {2020},
              journal = {Transactions of the Association for Computational Linguistics}
              }"""
        )
    ),
    "XNLI": textwrap.dedent(
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
    "XQuAD": textwrap.dedent(
        """
          @article{Artetxe:etal:2019,
              author    = {Mikel Artetxe and Sebastian Ruder and Dani Yogatama},
              title     = {On the cross-lingual transferability of monolingual representations},
              journal   = {CoRR},
              volume    = {abs/1910.11856},
              year      = {2019},
              archivePrefix = {arXiv},
              eprint    = {1910.11856}
        }
        """
    ),
    "MLQA": textwrap.dedent(
        """\
          @article{lewis2019mlqa,
          title={MLQA: Evaluating Cross-lingual Extractive Question Answering},
          author={Lewis, Patrick and Oguz, Barlas and Rinott, Ruty and Riedel, Sebastian and Schwenk, Holger},
          journal={arXiv preprint arXiv:1910.07475},
          year={2019}"""
    ),
    "PAWS-X": textwrap.dedent(
        """\
          @InProceedings{pawsx2019emnlp,
          title = {{PAWS-X: A Cross-lingual Adversarial Dataset for Paraphrase Identification}},
          author = {Yang, Yinfei and Zhang, Yuan and Tar, Chris and Baldridge, Jason},
          booktitle = {Proc. of EMNLP},
          year = {2019}
        }"""
    ),
    "tatoeba": textwrap.dedent(
        """\
                    @article{tatoeba,
            title={Massively Multilingual Sentence Embeddings for Zero-Shot Cross-Lingual Transfer and Beyond},
            author={Mikel, Artetxe and Holger, Schwenk,},
            journal={arXiv:1812.10464v2},
            year={2018}
          }"""
    ),
    "bucc18": textwrap.dedent(""""""),
    "udpos": textwrap.dedent(""""""),
    "SQuAD": textwrap.dedent(
        """\
        @article{2016arXiv160605250R,
           author = {{Rajpurkar}, Pranav and {Zhang}, Jian and {Lopyrev},
                     Konstantin and {Liang}, Percy},
            title = "{SQuAD: 100,000+ Questions for Machine Comprehension of Text}",
          journal = {arXiv e-prints},
             year = 2016,
              eid = {arXiv:1606.05250},
            pages = {arXiv:1606.05250},
            archivePrefix = {arXiv},
           eprint = {1606.05250},
}"""
    ),
    "PAN-X": textwrap.dedent(
        """\
                    @article{pan-x,
            title={Massively Multilingual Sentence Embeddings for Zero-Shot Cross-Lingual Transfer and Beyond},
            author={Xiaoman, Pan and Boliang, Zhang and Jonathan, May and Joel, Nothman and Kevin, Knight and Heng, Ji},
            volume={Proceedings of the 55th Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers}
            year={2017}
          }"""
    ),
}

_TEXT_FEATURES = {
    "XNLI": {"language": "language", "sentence1": "sentence1", "sentence2": "sentence2"},
    "tydiqa": {"id": "id", "title": "title", "context": "context", "question": "question", "answers": "answers"},
    "XQuAD": {"id": "id", "context": "context", "question": "question", "answers": "answers"},
    "MLQA": {"id": "id", "title": "title", "context": "context", "question": "question", "answers": "answers"},
    "tatoeba": {"source_sentence": "", "target_sentence": "", "source_lang": "", "target_lang": ""},
    "bucc18": {"source_sentence": "", "target_sentence": "", "source_lang": "", "target_lang": ""},
    "PAWS-X": {"sentence1": "sentence1", "sentence2": "sentence2"},
    "udpos": {"word": "", "pos_tag": ""},
    "SQuAD": {"id": "id", "title": "title", "context": "context", "question": "question", "answers": "answers"},
    "PAN-X": {"word": "", "ner_tag": "", "lang": ""},
}
_DATA_URLS = {
    "tydiqa": "https://storage.googleapis.com/tydiqa/",
    "XNLI": "https://dl.fbaipublicfiles.com/XNLI/XNLI-1.0.zip",
    "XQuAD": "https://github.com/deepmind/xquad/raw/master/",
    "MLQA": "https://dl.fbaipublicfiles.com/MLQA/MLQA_V1.zip",
    "PAWS-X": "https://storage.googleapis.com/paws/pawsx/x-final.tar.gz",
    "bucc18": "https://comparable.limsi.fr/bucc2018/",
    "tatoeba": "https://github.com/facebookresearch/LASER/raw/master/data/tatoeba/v1",
    "udpos": "https://lindat.mff.cuni.cz/repository/xmlui/bitstream/handle/11234/1-3105/ud-treebanks-v2.5.tgz",
    "SQuAD": "https://rajpurkar.github.io/SQuAD-explorer/dataset/",
    "PAN-X": "",
}

_URLS = {
    "tydiqa": "https://github.com/google-research-datasets/tydiqa",
    "XQuAD": "https://github.com/deepmind/xquad",
    "XNLI": "https://www.nyu.edu/projects/bowman/xnli/",
    "MLQA": "https://github.com/facebookresearch/MLQA",
    "PAWS-X": "https://github.com/google-research-datasets/paws/tree/master/pawsx",
    "bucc18": "https://comparable.limsi.fr/bucc2018/",
    "tatoeba": "https://github.com/facebookresearch/LASER/blob/master/data/tatoeba/v1/README.md",
    "udpos": "https://universaldependencies.org/",
    "SQuAD": "https://rajpurkar.github.io/SQuAD-explorer/",
    "PAN-X": "",
}


class XtremeConfig(nlp.BuilderConfig):
    """BuilderConfig for Break"""

    def __init__(self, data_url, citation, url, text_features, **kwargs):
        """

        Args:
            text_features: `dict[string, string]`, map from the name of the feature
        dict for each text field to the name of the column in the tsv file
            label_column:
            label_classes
            **kwargs: keyword arguments forwarded to super.
        """
        super(XtremeConfig, self).__init__(
            version=nlp.Version("1.0.0", "New split API (https://tensorflow.org/datasets/splits)"), **kwargs
        )
        self.text_features = text_features
        self.data_url = data_url
        self.citation = citation
        self.url = url


class Xtreme(nlp.GeneratorBasedBuilder):
    """TODO(xtreme): Short description of my dataset."""

    # TODO(xtreme): Set up version.
    VERSION = nlp.Version("0.1.0")
    BUILDER_CONFIGS = [
        XtremeConfig(
            name=name,
            description=_DESCRIPTIONS[name.split(".")[0]],
            citation=_CITATIONS[name.split(".")[0]],
            text_features=_TEXT_FEATURES[name.split(".")[0]],
            data_url=_DATA_URLS[name.split(".")[0]],
            url=_URLS[name.split(".")[0]],
        )
        for name in _NAMES
    ]

    @property
    def manual_download_instructions(self):
        if self.config.name.startswith("PAN-X"):
            return """\
             You need to manually download the AmazonPhotos.zip file on Amazon Cloud Drive
             (https://www.amazon.com/clouddrive/share/d3KGCRCIYwhKJF0H3eWA26hjg2ZCRhjpEQtDL70FSBN). The folder containing the saved file
             can be used to load the dataset via `nlp.load_dataset("xtreme", data_dir="<path/to/folder>").
            """
        return None

    def _info(self):
        # TODO(xtreme): Specifies the nlp.DatasetInfo object
        features = {text_feature: nlp.Value("string") for text_feature in six.iterkeys(self.config.text_features)}
        if "answers" in features.keys():
            features["answers"] = nlp.features.Sequence(
                {"answer_start": nlp.Value("int32"), "text": nlp.Value("string")}
            )
        if self.config.name.startswith("PAWS-X"):
            features["label"] = nlp.Value("string")
        if self.config.name == "XNLI":
            features["gold_label"] = nlp.Value("string")

        return nlp.DatasetInfo(
            # This is the description that will appear on the datasets page.
            description=self.config.description + "\n" + _DESCRIPTION,
            # nlp.features.FeatureConnectors
            features=nlp.Features(
                features
                # These are the features of your dataset like images, labels ...
            ),
            # If there's a common (input, target) tuple from the features,
            # specify them here. They'll be used if as_supervised=True in
            # builder.as_dataset.
            supervised_keys=None,
            # Homepage of the dataset for documentation
            homepage="https://github.com/google-research/xtreme" + "\t" + self.config.url,
            citation=self.config.citation + "\n" + _CITATION,
        )

    def _split_generators(self, dl_manager):
        """Returns SplitGenerators."""
        # TODO(xtreme): Downloads the data and defines the splits
        # dl_manager is a nlp.download.DownloadManager that can be used to
        # download and extract URLs

        if self.config.name == "tydiqa":
            train_url = "v1.1/tydiqa-goldp-v1.1-train.json"
            dev_url = "v1.1/tydiqa-goldp-v1.1-dev.json"
            urls_to_download = {
                "train": os.path.join(self.config.data_url, train_url),
                "dev": os.path.join(self.config.data_url, dev_url),
            }
            dl_dir = dl_manager.download_and_extract(urls_to_download)
            return [
                nlp.SplitGenerator(
                    name=nlp.Split.TRAIN,
                    # These kwargs will be passed to _generate_examples
                    gen_kwargs={"filepath": dl_dir["train"]},
                ),
                nlp.SplitGenerator(
                    name=nlp.Split.VALIDATION,
                    # These kwargs will be passed to _generate_examples
                    gen_kwargs={"filepath": dl_dir["dev"]},
                ),
            ]
        if self.config.name == "XNLI":
            dl_dir = dl_manager.download_and_extract(self.config.data_url)
            data_dir = os.path.join(dl_dir, "XNLI-1.0")
            return [
                nlp.SplitGenerator(
                    name=nlp.Split.TEST, gen_kwargs={"filepath": os.path.join(data_dir, "xnli.test.tsv")}
                ),
                nlp.SplitGenerator(
                    name=nlp.Split.VALIDATION, gen_kwargs={"filepath": os.path.join(data_dir, "xnli.dev.tsv")}
                ),
            ]

        if self.config.name.startswith("MLQA"):
            mlqa_downloaded_files = dl_manager.download_and_extract(self.config.data_url)
            l1 = self.config.name.split(".")[1]
            l2 = self.config.name.split(".")[2]
            return [
                nlp.SplitGenerator(
                    name=nlp.Split.TEST,
                    # These kwargs will be passed to _generate_examples
                    gen_kwargs={
                        "filepath": os.path.join(
                            os.path.join(mlqa_downloaded_files, "MLQA_V1/test"),
                            "test-context-{}-question-{}.json".format(l1, l2),
                        )
                    },
                ),
                nlp.SplitGenerator(
                    name=nlp.Split.VALIDATION,
                    # These kwargs will be passed to _generate_examples
                    gen_kwargs={
                        "filepath": os.path.join(
                            os.path.join(mlqa_downloaded_files, "MLQA_V1/dev"),
                            "dev-context-{}-question-{}.json".format(l1, l2),
                        )
                    },
                ),
            ]

        if self.config.name.startswith("XQuAD"):
            lang = self.config.name.split(".")[1]
            xquad_downloaded_file = dl_manager.download_and_extract(
                os.path.join(self.config.data_url, "xquad.{}.json".format(lang))
            )
            return [
                nlp.SplitGenerator(
                    name=nlp.Split.VALIDATION,
                    # These kwargs will be passed to _generate_examples
                    gen_kwargs={"filepath": xquad_downloaded_file},
                ),
            ]
        if self.config.name.startswith("PAWS-X"):
            lang = self.config.name.split(".")[1]
            paws_x_dir = dl_manager.download_and_extract(self.config.data_url)
            data_dir = os.path.join(paws_x_dir, "x-final", lang)
            return [
                nlp.SplitGenerator(
                    name=nlp.Split.VALIDATION,
                    # These kwargs will be passed to _generate_examples
                    gen_kwargs={"filepath": os.path.join(data_dir, "dev_2k.tsv")},
                ),
                nlp.SplitGenerator(
                    name=nlp.Split.TEST,
                    # These kwargs will be passed to _generate_examples
                    gen_kwargs={"filepath": os.path.join(data_dir, "test_2k.tsv")},
                ),
                nlp.SplitGenerator(
                    name=nlp.Split.TRAIN,
                    # These kwargs will be passed to _generate_examples
                    gen_kwargs={
                        "filepath": os.path.join(data_dir, "translated_train.tsv")
                        if lang != "en"
                        else os.path.join(data_dir, "train.tsv")
                    },
                ),
            ]
        elif self.config.name.startswith("tatoeba"):
            lang = self.config.name.split(".")[1]

            tatoeba_source_data = dl_manager.download_and_extract(
                os.path.join(self.config.data_url, "tatoeba.{}-eng.{}".format(lang, lang))
            )
            tatoeba_eng_data = dl_manager.download_and_extract(
                os.path.join(self.config.data_url, "tatoeba.{}-eng.eng".format(lang))
            )
            return [
                nlp.SplitGenerator(
                    name=nlp.Split.VALIDATION,
                    # These kwargs will be passed to _generate_examples
                    gen_kwargs={"filepath": (tatoeba_source_data, tatoeba_eng_data)},
                ),
            ]
        if self.config.name.startswith("bucc18"):
            lang = self.config.name.split(".")[1]
            bucc18_dl_test_dir = dl_manager.download_and_extract(
                os.path.join(self.config.data_url, "bucc2018-{}-en.training-gold.tar.bz2".format(lang))
            )
            bucc18_dl_dev_dir = dl_manager.download_and_extract(
                os.path.join(self.config.data_url, "bucc2018-{}-en.sample-gold.tar.bz2".format(lang))
            )
            return [
                nlp.SplitGenerator(
                    name=nlp.Split.VALIDATION,
                    # These kwargs will be passed to _generate_examples
                    gen_kwargs={"filepath": os.path.join(bucc18_dl_dev_dir, "bucc2018", lang + "-en")},
                ),
                nlp.SplitGenerator(
                    name=nlp.Split.TEST,
                    # These kwargs will be passed to _generate_examples
                    gen_kwargs={"filepath": os.path.join(bucc18_dl_test_dir, "bucc2018", lang + "-en")},
                ),
            ]
        if self.config.name.startswith("udpos"):
            udpos_downloaded_files = dl_manager.download_and_extract(self.config.data_url)
            data_dir = os.path.join(udpos_downloaded_files, "ud-treebanks-v2.5")

            lang = self.config.name.split(".")[1]
            data_dir = os.path.join(data_dir, "*_" + lang + "*")
            folders = sorted(glob.glob(data_dir))

            if lang == "Kazakh":
                return [
                    nlp.SplitGenerator(
                        name=nlp.Split.TEST,
                        # These kwargs will be passed to _generate_examples
                        gen_kwargs={
                            "filepath": [
                                os.path.join(folder, file)
                                for folder in folders
                                for file in sorted(os.listdir(folder))
                                if "test" in file and file.endswith(".conllu")
                            ]
                        },
                    ),
                    nlp.SplitGenerator(
                        name=nlp.Split.TRAIN,
                        # These kwargs will be passed to _generate_examples
                        gen_kwargs={
                            "filepath": [
                                os.path.join(folder, file)
                                for folder in folders
                                for file in sorted(os.listdir(folder))
                                if "train" in file and file.endswith(".conllu")
                            ]
                        },
                    ),
                ]
            elif lang == "Tagalog" or lang == "Thai" or lang == "Yoruba":
                return [
                    nlp.SplitGenerator(
                        name=nlp.Split.TEST,
                        # These kwargs will be passed to _generate_examples
                        gen_kwargs={
                            "filepath": [
                                os.path.join(folder, file)
                                for folder in folders
                                for file in sorted(os.listdir(folder))
                                if "test" in file and file.endswith(".conllu")
                            ]
                        },
                    )
                ]
            else:
                return [
                    nlp.SplitGenerator(
                        name=nlp.Split.VALIDATION,
                        # These kwargs will be passed to _generate_examples
                        gen_kwargs={
                            "filepath": [
                                os.path.join(folder, file)
                                for folder in folders
                                for file in sorted(os.listdir(folder))
                                if "NYUAD" not in folder and "dev" in file and file.endswith(".conllu")
                            ]
                            # we exclude Arabic NYUAD which deos not contains any word, only _
                        },
                    ),
                    nlp.SplitGenerator(
                        name=nlp.Split.TEST,
                        # These kwargs will be passed to _generate_examples
                        gen_kwargs={
                            "filepath": [
                                os.path.join(folder, file)
                                for folder in folders
                                for file in sorted(os.listdir(folder))
                                if "NYUAD" not in folder and "test" in file and file.endswith(".conllu")
                            ]
                        },
                    ),
                    nlp.SplitGenerator(
                        name=nlp.Split.TRAIN,
                        # These kwargs will be passed to _generate_examples
                        gen_kwargs={
                            "filepath": [
                                os.path.join(folder, file)
                                for folder in folders
                                for file in sorted(os.listdir(folder))
                                if "NYUAD" not in folder and "train" in file and file.endswith(".conllu")
                            ]
                        },
                    ),
                ]

        if self.config.name == "SQuAD":

            urls_to_download = {
                "train": os.path.join(self.config.data_url, "train-v1.1.json"),
                "dev": os.path.join(self.config.data_url, "dev-v1.1.json"),
            }
            downloaded_files = dl_manager.download_and_extract(urls_to_download)

            return [
                nlp.SplitGenerator(name=nlp.Split.TRAIN, gen_kwargs={"filepath": downloaded_files["train"]}),
                nlp.SplitGenerator(name=nlp.Split.VALIDATION, gen_kwargs={"filepath": downloaded_files["dev"]}),
            ]

        if self.config.name.startswith("PAN-X"):
            path_to_manual_folder = os.path.abspath(os.path.expanduser(dl_manager.manual_dir))
            panx_path = os.path.join(path_to_manual_folder, _PAN_X_FOLDER)
            if not os.path.exists(panx_path):
                raise FileNotFoundError(
                    "{} does not exist. Make sure you insert a manual dir via `nlp.load_dataset('xtreme', data_dir=...)` that includes {}. Manual download instructions: {}".format(
                        panx_path, _PAN_X_FOLDER, self.manual_download_instructions
                    )
                )

            panx_dl_dir = dl_manager.extract(panx_path)
            lang = self.config.name.split(".")[1]
            lang_folder = dl_manager.extract(os.path.join(panx_dl_dir, lang + ".tar.gz"))
            return [
                nlp.SplitGenerator(
                    name=nlp.Split.VALIDATION,
                    # These kwargs will be passed to _generate_examples
                    gen_kwargs={
                        "filepath": os.path.join(lang_folder, "dev")
                        # we exclude Arabic NYUAD which deos not contains any word, only _
                    },
                ),
                nlp.SplitGenerator(
                    name=nlp.Split.TEST,
                    # These kwargs will be passed to _generate_examples
                    gen_kwargs={"filepath": os.path.join(lang_folder, "test")},
                ),
                nlp.SplitGenerator(
                    name=nlp.Split.TRAIN,
                    # These kwargs will be passed to _generate_examples
                    gen_kwargs={"filepath": os.path.join(lang_folder, "train")},
                ),
            ]

    def _generate_examples(self, filepath):
        """Yields examples."""
        # TODO(xtreme): Yields (key, example) tuples from the dataset

        if self.config.name == "tydiqa" or self.config.name.startswith("MLQA") or self.config.name == "SQuAD":
            with open(filepath) as f:
                data = json.load(f)
                for article in data["data"]:
                    title = article.get("title", "").strip()
                    for paragraph in article["paragraphs"]:
                        context = paragraph["context"].strip()
                        for qa in paragraph["qas"]:
                            question = qa["question"].strip()
                            id_ = qa["id"]

                            answer_starts = [answer["answer_start"] for answer in qa["answers"]]
                            answers = [answer["text"].strip() for answer in qa["answers"]]

                            # Features currently used are "context", "question", and "answers".
                            # Others are extracted here for the ease of future expansions.
                            yield id_, {
                                "title": title,
                                "context": context,
                                "question": question,
                                "id": id_,
                                "answers": {"answer_start": answer_starts, "text": answers},
                            }
        if self.config.name == "XNLI":
            with open(filepath) as f:
                data = csv.DictReader(f, delimiter="\t")
                for id_, row in enumerate(data):
                    yield id_, {
                        "sentence1": row["sentence1"],
                        "sentence2": row["sentence2"],
                        "language": row["language"],
                        "gold_label": row["gold_label"],
                    }
        if self.config.name.startswith("PAWS-X"):
            with open(filepath) as f:
                data = csv.reader(f, delimiter="\t")
                for id_, row in enumerate(data):
                    if len(row) == 4:
                        yield id_, {"sentence1": row[1], "sentence2": row[2], "label": row[3]}
        if self.config.name.startswith("XQuAD"):
            with open(filepath) as f:
                xquad = json.load(f)
                for article in xquad["data"]:
                    for paragraph in article["paragraphs"]:
                        context = paragraph["context"].strip()
                        for qa in paragraph["qas"]:
                            question = qa["question"].strip()
                            id_ = qa["id"]

                            answer_starts = [answer["answer_start"] for answer in qa["answers"]]
                            answers = [answer["text"].strip() for answer in qa["answers"]]

                            # Features currently used are "context", "question", and "answers".
                            # Others are extracted here for the ease of future expansions.
                            yield id_, {
                                "context": context,
                                "question": question,
                                "id": id_,
                                "answers": {"answer_start": answer_starts, "text": answers},
                            }
        if self.config.name.startswith("bucc18"):
            files = sorted(os.listdir(filepath))
            target_file = "/"
            source_file = "/"
            source_target_file = "/"
            for file in files:
                if file.endswith("en"):
                    target_file = os.path.join(filepath, file)
                elif file.endswith("gold"):
                    source_target_file = os.path.join(filepath, file)
                else:
                    source_file = os.path.join(filepath, file)
            with open(target_file) as f:
                data = csv.reader(f, delimiter="\t")
                target_sentences = [row for row in data]
            with open(source_file) as f:
                data = csv.reader(f, delimiter="\t")
                source_sentences = [row for row in data]
            with open(source_target_file) as f:
                data = csv.reader(f, delimiter="\t")
                source_target_ids = [row for row in data]
            for id_, pair in enumerate(source_target_ids):
                source_id = pair[0]
                target_id = pair[1]
                source_sent = ""
                target_sent = ""
                for i in range(len(source_sentences)):
                    if source_sentences[i][0] == source_id:
                        source_sent = source_sentences[i][1]
                        source_id = source_sentences[i][0]
                        break
                for j in range(len(target_sentences)):
                    if target_sentences[j][0] == target_id:
                        target_sent = target_sentences[j][1]
                        target_id = target_sentences[j][0]
                        break
                yield id_, {
                    "source_sentence": source_sent,
                    "target_sentence": target_sent,
                    "source_lang": source_id,
                    "target_lang": target_id,
                }
        if self.config.name.startswith("tatoeba"):
            source_file = filepath[0]
            target_file = filepath[1]
            source_sentences = []
            target_sentences = []
            with open(source_file) as f1:
                for row in f1:
                    source_sentences.append(row)
            with open(target_file) as f2:
                for row in f2:
                    target_sentences.append(row)
            for i in range(len(source_sentences)):
                yield i, {
                    "source_sentence": source_sentences[i],
                    "target_sentence": target_sentences[i],
                    "source_lang": source_file.split(".")[-1],
                    "target_lang": "eng",
                }
        if self.config.name.startswith("udpos"):
            for id_file, file in enumerate(filepath):
                with open(file) as f:
                    data = csv.reader(f, delimiter="\t", quoting=csv.QUOTE_NONE)
                    for id_row, row in enumerate(data):
                        if len(row) >= 10 and row[1] != "_":
                            yield str(id_file) + "_" + str(id_row), {"word": row[1], "pos_tag": row[3]}
        if self.config.name.startswith("PAN-X"):
            with open(filepath) as f:
                data = csv.reader(f, delimiter="\t", quoting=csv.QUOTE_NONE)
                for id_, row in enumerate(data):
                    if row:
                        lang, word = row[0].split(":")[0], row[0].split(":")[1]
                        tag = row[1]
                        yield id_, {"word": word, "ner_tag": tag, "lang": lang}
