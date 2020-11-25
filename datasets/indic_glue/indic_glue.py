"""The IndicGLUE benchmark."""

from __future__ import absolute_import, division, print_function

import csv
import json
import os
import textwrap

import pandas as pd
import six

import datasets


_INDIC_GLUE_CITATION = """\
    @inproceedings{kakwani2020indicnlpsuite,
    title={{IndicNLPSuite: Monolingual Corpora, Evaluation Benchmarks and Pre-trained Multilingual Language Models for Indian Languages}},
    author={Divyanshu Kakwani and Anoop Kunchukuttan and Satish Golla and Gokul N.C. and Avik Bhattacharyya and Mitesh M. Khapra and Pratyush Kumar},
    year={2020},
    booktitle={Findings of EMNLP},
}
"""

_INDIC_GLUE_DESCRIPTION = """\
    IndicGLUE is a natural language understanding benchmark for Indian languages. It contains a wide
    variety of tasks and covers 11 major Indian languages - as, bn, gu, hi, kn, ml, mr, or, pa, ta, te.
"""

_DESCRIPTIONS = {
    "wnli": textwrap.dedent(
        """
        The Winograd Schema Challenge (Levesque et al., 2011) is a reading comprehension task
        in which a system must read a sentence with a pronoun and select the referent of that pronoun from
        a list of choices. The examples are manually constructed to foil simple statistical methods: Each
        one is contingent on contextual information provided by a single word or phrase in the sentence.
        To convert the problem into sentence pair classification, we construct sentence pairs by replacing
        the ambiguous pronoun with each possible referent. The task is to predict if the sentence with the
        pronoun substituted is entailed by the original sentence. We use a small evaluation set consisting of
        new examples derived from fiction books that was shared privately by the authors of the original
        corpus. While the included training set is balanced between two classes, the test set is imbalanced
        between them (65% not entailment). Also, due to a data quirk, the development set is adversarial:
        hypotheses are sometimes shared between training and development examples, so if a model memorizes the
        training examples, they will predict the wrong label on corresponding development set
        example. As with QNLI, each example is evaluated separately, so there is not a systematic correspondence
        between a model's score on this task and its score on the unconverted original task. We
        call converted dataset WNLI (Winograd NLI). This dataset is translated and publicly released for 3
        Indian languages by AI4Bharat.
        """
    ),
    "copa": textwrap.dedent(
        """
        The Choice Of Plausible Alternatives (COPA) evaluation provides researchers with a tool for assessing
        progress in open-domain commonsense causal reasoning. COPA consists of 1000 questions, split equally
        into development and test sets of 500 questions each. Each question is composed of a premise and two
        alternatives, where the task is to select the alternative that more plausibly has a causal relation
        with the premise. The correct alternative is randomized so that the expected performance of randomly
        guessing is 50%. This dataset is translated and publicly released for 3 languages by AI4Bharat.
        """
    ),
    "sna": textwrap.dedent(
        """
        This dataset is a collection of Bengali News articles. The dataset is used for classifying articles into
        5 different classes namely international, state, kolkata, entertainment and sports.
        """
    ),
    "csqa": textwrap.dedent(
        """
        Given a text with an entity randomly masked, the task is to predict that masked entity from a list of 4
        candidate entities. The dataset contains around 239k examples across 11 languages.
        """
    ),
    "wstp": textwrap.dedent(
        """
        Predict the correct title for a Wikipedia section from a given list of four candidate titles.
        The dataset has 400k examples across 11 Indian languages.
        """
    ),
    "inltkh": textwrap.dedent(
        """
        Obtained from inltk project. The corpus is a collection of headlines tagged with their news category.
        Available for langauges: gu, ml, mr and ta.
        """
    ),
    "bbca": textwrap.dedent(
        """
        This release consists of 4335 Hindi documents with tags from the BBC Hindi News website.
        """
    ),
    "cvit-mkb-clsr": textwrap.dedent(
        """
        CVIT Maan ki Baat Dataset - Given a sentence in language $L_1$ the task is to retrieve its translation
        from a set of candidate sentences in language $L_2$.
        The dataset contains around 39k parallel sentence pairs across 8 Indian languages.
        """
    ),
    "iitp-mr": textwrap.dedent(
        """
        IIT Patna Product Reviews: Sentiment analysis corpus for product reviews posted in Hindi.
        """
    ),
    "iitp-pr": textwrap.dedent(
        """
        IIT Patna Product Reviews: Sentiment analysis corpus for product reviews posted in Hindi.
        """
    ),
    "actsa-sc": textwrap.dedent(
        """
        ACTSA Corpus: Sentiment analysis corpus for Telugu sentences.
        """
    ),
    "md": textwrap.dedent(
        """
        The Hindi Discourse Analysis dataset is a corpus for analyzing discourse modes present in its sentences.
        It contains sentences from stories written by 11 famous authors from the 20th Century. 4-5 stories by
        each author have been selected which were available in the public domain resulting in a collection of 53 stories.
        Most of these short stories were originally written in Hindi but some of them were written in other Indian languages
        and later translated to Hindi.
        """
    ),
    "wiki-ner": textwrap.dedent(
        """
        The WikiANN dataset (Pan et al. 2017) is a dataset with NER annotations for PER, ORG and LOC. It has been constructed using
        the linked entities in Wikipedia pages for 282 different languages including Danish.
        """
    ),
}

_CITATIONS = {
    "wnli": textwrap.dedent(
        """
        @inproceedings{kakwani2020indicnlpsuite,
        title={{IndicNLPSuite: Monolingual Corpora, Evaluation Benchmarks and Pre-trained Multilingual Language Models for Indian Languages}},
        author={Divyanshu Kakwani and Anoop Kunchukuttan and Satish Golla and Gokul N.C. and Avik Bhattacharyya and Mitesh M. Khapra and Pratyush Kumar},
        year={2020},
        booktitle={Findings of EMNLP},
        }
        @inproceedings{Levesque2011TheWS,
        title={The Winograd Schema Challenge},
        author={H. Levesque and E. Davis and L. Morgenstern},
        booktitle={KR},
        year={2011}
        }
        """
    ),
    "copa": textwrap.dedent(
        """
        @inproceedings{kakwani2020indicnlpsuite,
        title={{IndicNLPSuite: Monolingual Corpora, Evaluation Benchmarks and Pre-trained Multilingual Language Models for Indian Languages}},
        author={Divyanshu Kakwani and Anoop Kunchukuttan and Satish Golla and Gokul N.C. and Avik Bhattacharyya and Mitesh M. Khapra and Pratyush Kumar},
        year={2020},
        booktitle={Findings of EMNLP},
        }
        @inproceedings{Gordon2011SemEval2012T7,
        title={SemEval-2012 Task 7: Choice of Plausible Alternatives: An Evaluation of Commonsense Causal Reasoning},
        author={Andrew S. Gordon and Zornitsa Kozareva and Melissa Roemmele},
        booktitle={SemEval@NAACL-HLT},
        year={2011}
        }
        """
    ),
    "sna": textwrap.dedent(
        """
        https://www.kaggle.com/csoham/classification-bengali-news-articles-indicnlp
        """
    ),
    "csqa": textwrap.dedent(
        """
        @inproceedings{kakwani2020indicnlpsuite,
        title={{IndicNLPSuite: Monolingual Corpora, Evaluation Benchmarks and Pre-trained Multilingual Language Models for Indian Languages}},
        author={Divyanshu Kakwani and Anoop Kunchukuttan and Satish Golla and Gokul N.C. and Avik Bhattacharyya and Mitesh M. Khapra and Pratyush Kumar},
        year={2020},
        booktitle={Findings of EMNLP},
        }
        """
    ),
    "wstp": textwrap.dedent(
        """
        @inproceedings{kakwani2020indicnlpsuite,
        title={{IndicNLPSuite: Monolingual Corpora, Evaluation Benchmarks and Pre-trained Multilingual Language Models for Indian Languages}},
        author={Divyanshu Kakwani and Anoop Kunchukuttan and Satish Golla and Gokul N.C. and Avik Bhattacharyya and Mitesh M. Khapra and Pratyush Kumar},
        year={2020},
        booktitle={Findings of EMNLP},
        }
        """
    ),
    "inltkh": textwrap.dedent(
        """
        https://github.com/goru001/inltk
        """
    ),
    "bbca": textwrap.dedent(
        """
        https://github.com/NirantK/hindi2vec/releases/tag/bbc-hindi-v0.1
        """
    ),
    "cvit-mkb-clsr": textwrap.dedent(
        """
        @inproceedings{siripragada-etal-2020-multilingual,
        title = "A Multilingual Parallel Corpora Collection Effort for {I}ndian Languages",
        author = "Siripragada, Shashank  and
        Philip, Jerin  and
        Namboodiri, Vinay P.  and
        Jawahar, C V",
        booktitle = "Proceedings of the 12th Language Resources and Evaluation Conference",
        month = may,
        year = "2020",
        address = "Marseille, France",
        publisher = "European Language Resources Association",
        url = "https://www.aclweb.org/anthology/2020.lrec-1.462",
        pages = "3743--3751",
        abstract = "We present sentence aligned parallel corpora across 10 Indian Languages - Hindi, Telugu, Tamil, Malayalam, Gujarati, Urdu, Bengali, Oriya, Marathi, Punjabi, and English - many of which are categorized as low resource. The corpora are compiled from online sources which have content shared across languages. The corpora presented significantly extends present resources that are either not large enough or are restricted to a specific domain (such as health). We also provide a separate test corpus compiled from an independent online source that can be independently used for validating the performance in 10 Indian languages. Alongside, we report on the methods of constructing such corpora using tools enabled by recent advances in machine translation and cross-lingual retrieval using deep neural network based methods.",
        language = "English",
        ISBN = "979-10-95546-34-4",
        }
        """
    ),
    "iitp-mr": textwrap.dedent(
        """
        @inproceedings{akhtar-etal-2016-hybrid,
        title = "A Hybrid Deep Learning Architecture for Sentiment Analysis",
        author = "Akhtar, Md Shad  and
        Kumar, Ayush  and
        Ekbal, Asif  and
        Bhattacharyya, Pushpak",
        booktitle = "Proceedings of {COLING} 2016, the 26th International Conference on Computational Linguistics: Technical Papers",
        month = dec,
        year = "2016",
        address = "Osaka, Japan",
        publisher = "The COLING 2016 Organizing Committee",
        url = "https://www.aclweb.org/anthology/C16-1047",
        pages = "482--493",
        abstract = "In this paper, we propose a novel hybrid deep learning archtecture which is highly efficient for sentiment analysis in resource-poor languages. We learn sentiment embedded vectors from the Convolutional Neural Network (CNN). These are augmented to a set of optimized features selected through a multi-objective optimization (MOO) framework. The sentiment augmented optimized vector obtained at the end is used for the training of SVM for sentiment classification. We evaluate our proposed approach for coarse-grained (i.e. sentence level) as well as fine-grained (i.e. aspect level) sentiment analysis on four Hindi datasets covering varying domains. In order to show that our proposed method is generic in nature we also evaluate it on two benchmark English datasets. Evaluation shows that the results of the proposed method are consistent across all the datasets and often outperforms the state-of-art systems. To the best of our knowledge, this is the very first attempt where such a deep learning model is used for less-resourced languages such as Hindi.",
}
        """
    ),
    "iitp-pr": textwrap.dedent(
        """
        @inproceedings{akhtar-etal-2016-hybrid,
        title = "A Hybrid Deep Learning Architecture for Sentiment Analysis",
        author = "Akhtar, Md Shad  and
        Kumar, Ayush  and
        Ekbal, Asif  and
        Bhattacharyya, Pushpak",
        booktitle = "Proceedings of {COLING} 2016, the 26th International Conference on Computational Linguistics: Technical Papers",
        month = dec,
        year = "2016",
        address = "Osaka, Japan",
        publisher = "The COLING 2016 Organizing Committee",
        url = "https://www.aclweb.org/anthology/C16-1047",
        pages = "482--493",
        abstract = "In this paper, we propose a novel hybrid deep learning archtecture which is highly efficient for sentiment analysis in resource-poor languages. We learn sentiment embedded vectors from the Convolutional Neural Network (CNN). These are augmented to a set of optimized features selected through a multi-objective optimization (MOO) framework. The sentiment augmented optimized vector obtained at the end is used for the training of SVM for sentiment classification. We evaluate our proposed approach for coarse-grained (i.e. sentence level) as well as fine-grained (i.e. aspect level) sentiment analysis on four Hindi datasets covering varying domains. In order to show that our proposed method is generic in nature we also evaluate it on two benchmark English datasets. Evaluation shows that the results of the proposed method are consistent across all the datasets and often outperforms the state-of-art systems. To the best of our knowledge, this is the very first attempt where such a deep learning model is used for less-resourced languages such as Hindi.",
    }
        """
    ),
    "actsa-sc": textwrap.dedent(
        """
        @inproceedings{mukku-mamidi-2017-actsa,
        title = "{ACTSA}: Annotated Corpus for {T}elugu Sentiment Analysis",
        author = "Mukku, Sandeep Sricharan  and
        Mamidi, Radhika",
        booktitle = "Proceedings of the First Workshop on Building Linguistically Generalizable {NLP} Systems",
        month = sep,
        year = "2017",
        address = "Copenhagen, Denmark",
        publisher = "Association for Computational Linguistics",
        url = "https://www.aclweb.org/anthology/W17-5408",
        doi = "10.18653/v1/W17-5408",
        pages = "54--58",
        abstract = "Sentiment analysis deals with the task of determining the polarity of a document or sentence and has received a lot of attention in recent years for the English language. With the rapid growth of social media these days, a lot of data is available in regional languages besides English. Telugu is one such regional language with abundant data available in social media, but it{'}s hard to find a labelled data of sentences for Telugu Sentiment Analysis. In this paper, we describe an effort to build a gold-standard annotated corpus of Telugu sentences to support Telugu Sentiment Analysis. The corpus, named ACTSA (Annotated Corpus for Telugu Sentiment Analysis) has a collection of Telugu sentences taken from different sources which were then pre-processed and manually annotated by native Telugu speakers using our annotation guidelines. In total, we have annotated 5457 sentences, which makes our corpus the largest resource currently available. The corpus and the annotation guidelines are made publicly available.",
    }
        """
    ),
    "md": textwrap.dedent(
        """
        @inproceedings{Dhanwal2020AnAD,
        title={An Annotated Dataset of Discourse Modes in Hindi Stories},
        author={Swapnil Dhanwal and Hritwik Dutta and Hitesh Nankani and Nilay Shrivastava and Y. Kumar and Junyi Jessy Li and Debanjan Mahata and Rakesh Gosangi and Haimin Zhang and R. R. Shah and Amanda Stent},
        booktitle={LREC},
        year={2020}
        }
        """
    ),
    "wiki-ner": textwrap.dedent(
        """
        @inproceedings{pan-etal-2017-cross,
        title = "Cross-lingual Name Tagging and Linking for 282 Languages",
        author = "Pan, Xiaoman  and
        Zhang, Boliang  and
        May, Jonathan  and
        Nothman, Joel  and
        Knight, Kevin  and
        Ji, Heng",
        booktitle = "Proceedings of the 55th Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers)",
        month = jul,
        year = "2017",
        address = "Vancouver, Canada",
        publisher = "Association for Computational Linguistics",
        url = "https://www.aclweb.org/anthology/P17-1178",
        doi = "10.18653/v1/P17-1178",
        pages = "1946--1958",
        abstract = "The ambitious goal of this work is to develop a cross-lingual name tagging and linking framework for 282 languages that exist in Wikipedia. Given a document in any of these languages, our framework is able to identify name mentions, assign a coarse-grained or fine-grained type to each mention, and link it to an English Knowledge Base (KB) if it is linkable. We achieve this goal by performing a series of new KB mining methods: generating {``}silver-standard{''} annotations by transferring annotations from English to other languages through cross-lingual links and KB properties, refining annotations through self-training and topic selection, deriving language-specific morphology features from anchor links, and mining word translation pairs from cross-lingual links. Both name tagging and linking results for 282 languages are promising on Wikipedia data and on-Wikipedia data.",
    }
        """
    ),
}

_TEXT_FEATURES = {
    "wnli": {"hypothesis": "sentence1", "premise": "sentence2"},
    "copa": {"premise": "premise", "choice1": "choice1", "choice2": "choice2", "question": "question"},
    "sna": {"text": "text"},
    "csqa": {"question": "question", "answer": "answer", "category": "category", "title": "title"},
    "wstp": {
        "sectionText": "sectionText",
        "correctTitle": "correctTitle",
        "titleA": "titleA",
        "titleB": "titleB",
        "titleC": "titleC",
        "titleD": "titleD",
        "url": "url",
    },
    "inltkh": {"text": "text"},
    "bbca": {"label": "label", "text": "text"},
    "cvit-mkb-clsr": {"sentence1": "sentence1", "sentence2": "sentence2"},
    "iitp-mr": {"text": "text"},
    "iitp-pr": {"text": "text"},
    "actsa-sc": {"text": "text"},
    "md": {"sentence": "sentence", "discourse_mode": "discourse_mode"},
    "wiki-ner": {},
}

_DATA_URLS = {
    "wnli": "https://storage.googleapis.com/ai4bharat-public-indic-nlp-corpora/evaluations/wnli-translated.tar.gz",
    "copa": "https://storage.googleapis.com/ai4bharat-public-indic-nlp-corpora/evaluations/copa-translated.tar.gz",
    "sna": "https://storage.googleapis.com/ai4bharat-public-indic-nlp-corpora/evaluations/soham-articles.tar.gz",
    "csqa": "https://storage.googleapis.com/ai4bharat-public-indic-nlp-corpora/evaluations/wiki-cloze.tar.gz",
    "wstp": "https://storage.googleapis.com/ai4bharat-public-indic-nlp-corpora/evaluations/wiki-section-titles.tar.gz",
    "inltkh": "https://storage.googleapis.com/ai4bharat-public-indic-nlp-corpora/evaluations/inltk-headlines.tar.gz",
    "bbca": "https://storage.googleapis.com/ai4bharat-public-indic-nlp-corpora/evaluations/bbc-articles.tar.gz",
    "cvit-mkb-clsr": "https://storage.googleapis.com/ai4bharat-public-indic-nlp-corpora/evaluations/cvit-mkb.tar.gz",
    "iitp-mr": "https://storage.googleapis.com/ai4bharat-public-indic-nlp-corpora/evaluations/iitp-movie-reviews.tar.gz",
    "iitp-pr": "https://storage.googleapis.com/ai4bharat-public-indic-nlp-corpora/evaluations/iitp-product-reviews.tar.gz",
    "actsa-sc": "https://storage.googleapis.com/ai4bharat-public-indic-nlp-corpora/evaluations/actsa.tar.gz",
    "md": "https://storage.googleapis.com/ai4bharat-public-indic-nlp-corpora/evaluations/midas-discourse.tar.gz",
    "wiki-ner": "https://storage.googleapis.com/ai4bharat-public-indic-nlp-corpora/evaluations/wikiann-ner.tar.gz",
}

_URLS = {
    "wnli": "https://indicnlp.ai4bharat.org/indic-glue/#natural-language-inference",
    "copa": "https://indicnlp.ai4bharat.org/indic-glue/#natural-language-inference",
    "sna": "https://indicnlp.ai4bharat.org/indic-glue/#news-category-classification",
    "csqa": "https://indicnlp.ai4bharat.org/indic-glue/#cloze-style-question-answering",
    "wstp": "https://indicnlp.ai4bharat.org/indic-glue/#wikipedia-section-title-prediction",
    "inltkh": "https://indicnlp.ai4bharat.org/indic-glue/#news-category-classification",
    "bbca": "https://indicnlp.ai4bharat.org/indic-glue/#news-category-classification",
    "cvit-mkb-clsr": "https://indicnlp.ai4bharat.org/indic-glue/#cross-lingual-sentence-retrieval",
    "iitp-mr": "https://indicnlp.ai4bharat.org/indic-glue/#sentiment-analysis",
    "iitp-pr": "https://indicnlp.ai4bharat.org/indic-glue/#sentiment-analysis",
    "actsa-sc": "https://indicnlp.ai4bharat.org/indic-glue/#sentiment-analysis",
    "md": "https://indicnlp.ai4bharat.org/indic-glue/#discourse-analysis",
    "wiki-ner": "https://indicnlp.ai4bharat.org/indic-glue/#named-entity-recognition",
}

_INDIC_GLUE_URL = "https://indicnlp.ai4bharat.org/indic-glue/"

_WNLI_LANGS = ["en", "hi", "gu", "mr"]
_COPA_LANGS = ["en", "hi", "gu", "mr"]
_SNA_LANGS = ["bn"]
_CSQA_LANGS = ["as", "bn", "gu", "hi", "kn", "ml", "mr", "or", "pa", "ta", "te"]
_WSTP_LANGS = ["as", "bn", "gu", "hi", "kn", "ml", "mr", "or", "pa", "ta", "te"]
_iNLTKH_LANGS = ["gu", "ml", "mr", "ta", "te"]
_BBCA_LANGS = ["hi"]
_CVIT_MKB_CLSR = ["en-bn", "en-gu", "en-hi", "en-ml", "en-mr", "en-or", "en-ta", "en-te", "en-ur"]
_IITP_MR_LANGS = ["hi"]
_IITP_PR_LANGS = ["hi"]
_ACTSA_LANGS = ["te"]
_MD_LANGS = ["hi"]
_WIKI_NER_LANGS = ["as", "bn", "gu", "hi", "kn", "ml", "mr", "or", "pa", "ta", "te"]

_NAMES = []

for lang in _WNLI_LANGS:
    _NAMES.append(f"wnli.{lang}")

for lang in _COPA_LANGS:
    _NAMES.append(f"copa.{lang}")

for lang in _SNA_LANGS:
    _NAMES.append(f"sna.{lang}")

for lang in _CSQA_LANGS:
    _NAMES.append(f"csqa.{lang}")

for lang in _WSTP_LANGS:
    _NAMES.append(f"wstp.{lang}")

for lang in _iNLTKH_LANGS:
    _NAMES.append(f"inltkh.{lang}")

for lang in _BBCA_LANGS:
    _NAMES.append(f"bbca.{lang}")

for lang in _CVIT_MKB_CLSR:
    _NAMES.append(f"cvit-mkb-clsr.{lang}")

for lang in _IITP_MR_LANGS:
    _NAMES.append(f"iitp-mr.{lang}")

for lang in _IITP_PR_LANGS:
    _NAMES.append(f"iitp-pr.{lang}")

for lang in _ACTSA_LANGS:
    _NAMES.append(f"actsa-sc.{lang}")

for lang in _MD_LANGS:
    _NAMES.append(f"md.{lang}")

for lang in _WIKI_NER_LANGS:
    _NAMES.append(f"wiki-ner.{lang}")


class IndicGlueConfig(datasets.BuilderConfig):
    """BuilderConfig for IndicGLUE."""

    def __init__(self, data_url, citation, url, text_features, **kwargs):
        """
        Args:

          data_url: `string`, url to download the zip file from.
          citation: `string`, citation for the data set.
          url: `string`, url for information about the data set.
          text_features: `dict[string, string]`, map from the name of the feature
        dict for each text field to the name of the column in the csv/json file
          **kwargs: keyword arguments forwarded to super.
        """
        super(IndicGlueConfig, self).__init__(version=datasets.Version("1.0.0", ""), **kwargs)
        self.data_url = data_url
        self.citation = citation
        self.url = url
        self.text_features = text_features


class IndicGlue(datasets.GeneratorBasedBuilder):

    BUILDER_CONFIGS = [
        IndicGlueConfig(
            name=name,
            description=_DESCRIPTIONS[name.split(".")[0]],
            text_features=_TEXT_FEATURES[name.split(".")[0]],
            data_url=_DATA_URLS[name.split(".")[0]],
            citation=_CITATIONS[name.split(".")[0]],
            url=_URLS[name.split(".")[0]],
        )
        for name in _NAMES
    ]

    def _info(self):
        features = {text_feature: datasets.Value("string") for text_feature in six.iterkeys(self.config.text_features)}

        if self.config.name.startswith("copa"):
            features["label"] = datasets.Value("int32")

        if self.config.name.startswith("sna"):
            features["label"] = datasets.features.ClassLabel(
                names=["kolkata", "state", "national", "sports", "entertainment", "international"]
            )

        if self.config.name.startswith("inltkh"):
            features["label"] = datasets.features.ClassLabel(
                names=[
                    "entertainment",
                    "business",
                    "tech",
                    "sports",
                    "state",
                    "spirituality",
                    "tamil-cinema",
                    "positive",
                    "negative",
                    "neutral",
                ]
            )

        if self.config.name.startswith("iitp"):
            features["label"] = datasets.features.ClassLabel(names=["negative", "neutral", "positive"])

        if self.config.name.startswith("wnli"):
            features["label"] = datasets.features.ClassLabel(names=["not_entailment", "entailment", "None"])

        if self.config.name.startswith("actsa"):
            features["label"] = datasets.features.ClassLabel(names=["positive", "negative"])

        if self.config.name.startswith("csqa"):
            features["options"] = datasets.features.Sequence(datasets.Value("string"))
            features["out_of_context_options"] = datasets.features.Sequence(datasets.Value("string"))

        if self.config.name.startswith("md"):
            features["story_number"] = datasets.Value("int32")
            features["id"] = datasets.Value("int32")

        if self.config.name.startswith("wiki-ner"):
            features["tokens"] = datasets.features.Sequence(datasets.Value("string"))
            features["ner_tags"] = datasets.features.Sequence(
                datasets.features.ClassLabel(names=["B-LOC", "B-ORG", "B-PER", "I-LOC", "I-ORG", "I-PER", "O"])
            )
            features["additional_info"] = datasets.features.Sequence(
                datasets.features.Sequence(datasets.Value("string"))
            )

        return datasets.DatasetInfo(
            description=_INDIC_GLUE_DESCRIPTION + "\n" + self.config.description,
            features=datasets.Features(features),
            homepage=self.config.url,
            citation=_INDIC_GLUE_CITATION + "\n" + self.config.citation,
        )

    def _split_generators(self, dl_manager):

        if self.config.name.startswith("wnli"):
            dl_dir = dl_manager.download_and_extract(self.config.data_url)
            task_name = self._get_task_name_from_data_url(self.config.data_url)
            dl_dir = os.path.join(dl_dir, task_name + "/" + self.config.name.split(".")[1])
            return [
                datasets.SplitGenerator(
                    name=datasets.Split.TRAIN,
                    gen_kwargs={
                        "datafile": os.path.join(dl_dir, "train.csv"),
                        "split": datasets.Split.TRAIN,
                        "key": "train-split",
                    },
                ),
                datasets.SplitGenerator(
                    name=datasets.Split.VALIDATION,
                    gen_kwargs={
                        "datafile": os.path.join(dl_dir, "dev.csv"),
                        "split": datasets.Split.VALIDATION,
                        "key": "val-split",
                    },
                ),
                datasets.SplitGenerator(
                    name=datasets.Split.TEST,
                    gen_kwargs={
                        "datafile": os.path.join(dl_dir, "test.csv"),
                        "split": datasets.Split.TEST,
                        "key": "test-split",
                    },
                ),
            ]

        if self.config.name.startswith("copa"):
            dl_dir = dl_manager.download_and_extract(self.config.data_url)
            task_name = self._get_task_name_from_data_url(self.config.data_url)
            dl_dir = os.path.join(dl_dir, task_name + "/" + self.config.name.split(".")[1])

            return [
                datasets.SplitGenerator(
                    name=datasets.Split.TRAIN,
                    gen_kwargs={
                        "datafile": os.path.join(dl_dir, "train.jsonl"),
                        "split": datasets.Split.TRAIN,
                        "key": "train-split",
                    },
                ),
                datasets.SplitGenerator(
                    name=datasets.Split.VALIDATION,
                    gen_kwargs={
                        "datafile": os.path.join(dl_dir, "val.jsonl"),
                        "split": datasets.Split.VALIDATION,
                        "key": "val-split",
                    },
                ),
                datasets.SplitGenerator(
                    name=datasets.Split.TEST,
                    gen_kwargs={
                        "datafile": os.path.join(dl_dir, "test.jsonl"),
                        "split": datasets.Split.TEST,
                        "key": "test-split",
                    },
                ),
            ]

        if self.config.name.startswith("sna"):
            dl_dir = dl_manager.download_and_extract(self.config.data_url)
            task_name = self._get_task_name_from_data_url(self.config.data_url)
            dl_dir = os.path.join(dl_dir, task_name + "/" + self.config.name.split(".")[1])

            return [
                datasets.SplitGenerator(
                    name=datasets.Split.TRAIN,
                    gen_kwargs={
                        "datafile": os.path.join(dl_dir, "bn-train.csv"),
                        "split": datasets.Split.TRAIN,
                    },
                ),
                datasets.SplitGenerator(
                    name=datasets.Split.VALIDATION,
                    gen_kwargs={
                        "datafile": os.path.join(dl_dir, "bn-valid.csv"),
                        "split": datasets.Split.VALIDATION,
                    },
                ),
                datasets.SplitGenerator(
                    name=datasets.Split.TEST,
                    gen_kwargs={
                        "datafile": os.path.join(dl_dir, "bn-test.csv"),
                        "split": datasets.Split.TEST,
                    },
                ),
            ]

        if self.config.name.startswith("csqa"):
            dl_dir = dl_manager.download_and_extract(self.config.data_url)
            task_name = self._get_task_name_from_data_url(self.config.data_url)
            dl_dir = os.path.join(dl_dir, task_name)

            return [
                datasets.SplitGenerator(
                    name=datasets.Split.TEST,
                    gen_kwargs={
                        "datafile": os.path.join(dl_dir, f"{self.config.name.split('.')[1]}.json"),
                        "split": datasets.Split.TEST,
                    },
                )
            ]

        if self.config.name.startswith("wstp"):
            dl_dir = dl_manager.download_and_extract(self.config.data_url)
            task_name = self._get_task_name_from_data_url(self.config.data_url)
            dl_dir = os.path.join(dl_dir, task_name + "/" + self.config.name.split(".")[1])

            return [
                datasets.SplitGenerator(
                    name=datasets.Split.TRAIN,
                    gen_kwargs={
                        "datafile": os.path.join(dl_dir, f"{self.config.name.split('.')[1]}-train.json"),
                        "split": datasets.Split.TRAIN,
                    },
                ),
                datasets.SplitGenerator(
                    name=datasets.Split.VALIDATION,
                    gen_kwargs={
                        "datafile": os.path.join(dl_dir, f"{self.config.name.split('.')[1]}-valid.json"),
                        "split": datasets.Split.VALIDATION,
                    },
                ),
                datasets.SplitGenerator(
                    name=datasets.Split.TEST,
                    gen_kwargs={
                        "datafile": os.path.join(dl_dir, f"{self.config.name.split('.')[1]}-test.json"),
                        "split": datasets.Split.TEST,
                    },
                ),
            ]

        if (
            self.config.name.startswith("inltkh")
            or self.config.name.startswith("iitp")
            or self.config.name.startswith("actsa")
        ):
            dl_dir = dl_manager.download_and_extract(self.config.data_url)
            task_name = self._get_task_name_from_data_url(self.config.data_url)
            dl_dir = os.path.join(dl_dir, task_name + "/" + self.config.name.split(".")[1])

            return [
                datasets.SplitGenerator(
                    name=datasets.Split.TRAIN,
                    gen_kwargs={
                        "datafile": os.path.join(dl_dir, f"{self.config.name.split('.')[1]}-train.csv"),
                        "split": datasets.Split.TRAIN,
                    },
                ),
                datasets.SplitGenerator(
                    name=datasets.Split.VALIDATION,
                    gen_kwargs={
                        "datafile": os.path.join(dl_dir, f"{self.config.name.split('.')[1]}-valid.csv"),
                        "split": datasets.Split.VALIDATION,
                    },
                ),
                datasets.SplitGenerator(
                    name=datasets.Split.TEST,
                    gen_kwargs={
                        "datafile": os.path.join(dl_dir, f"{self.config.name.split('.')[1]}-test.csv"),
                        "split": datasets.Split.TEST,
                    },
                ),
            ]

        if self.config.name.startswith("bbca"):
            dl_dir = dl_manager.download_and_extract(self.config.data_url)
            task_name = self._get_task_name_from_data_url(self.config.data_url)
            dl_dir = os.path.join(dl_dir, task_name + "/" + self.config.name.split(".")[1])

            return [
                datasets.SplitGenerator(
                    name=datasets.Split.TRAIN,
                    gen_kwargs={
                        "datafile": os.path.join(dl_dir, f"{self.config.name.split('.')[1]}-train.csv"),
                        "split": datasets.Split.TRAIN,
                    },
                ),
                datasets.SplitGenerator(
                    name=datasets.Split.TEST,
                    gen_kwargs={
                        "datafile": os.path.join(dl_dir, f"{self.config.name.split('.')[1]}-test.csv"),
                        "split": datasets.Split.TEST,
                    },
                ),
            ]

        if self.config.name.startswith("cvit"):
            dl_dir = dl_manager.download_and_extract(self.config.data_url)
            task_name = self._get_task_name_from_data_url(self.config.data_url)
            dl_dir = os.path.join(dl_dir, task_name + "/" + self.config.name.split(".")[1])

            return [
                datasets.SplitGenerator(
                    name=datasets.Split.TEST,
                    gen_kwargs={
                        "datafile": None,
                        "src": os.path.join(dl_dir, f"mkb.{self.config.name.split('.')[1].split('-')[0]}"),
                        "tgt": os.path.join(dl_dir, f"mkb.{self.config.name.split('.')[1].split('-')[1]}"),
                        "split": datasets.Split.TEST,
                    },
                )
            ]

        if self.config.name.startswith("md"):
            dl_dir = dl_manager.download_and_extract(self.config.data_url)
            task_name = self._get_task_name_from_data_url(self.config.data_url)
            dl_dir = os.path.join(dl_dir, task_name + "/" + self.config.name.split(".")[1])

            return [
                datasets.SplitGenerator(
                    name=datasets.Split.TRAIN,
                    gen_kwargs={
                        "datafile": os.path.join(dl_dir, "train.json"),
                        "split": datasets.Split.TRAIN,
                    },
                ),
                datasets.SplitGenerator(
                    name=datasets.Split.VALIDATION,
                    gen_kwargs={
                        "datafile": os.path.join(dl_dir, "val.json"),
                        "split": datasets.Split.VALIDATION,
                    },
                ),
                datasets.SplitGenerator(
                    name=datasets.Split.TEST,
                    gen_kwargs={
                        "datafile": os.path.join(dl_dir, "test.json"),
                        "split": datasets.Split.TEST,
                    },
                ),
            ]

        if self.config.name.startswith("wiki-ner"):
            dl_dir = dl_manager.download_and_extract(self.config.data_url)
            task_name = self._get_task_name_from_data_url(self.config.data_url)
            dl_dir = os.path.join(dl_dir, task_name + "/" + self.config.name.split(".")[1])

            return [
                datasets.SplitGenerator(
                    name=datasets.Split.TRAIN,
                    gen_kwargs={
                        "datafile": os.path.join(dl_dir, f"{self.config.name.split('.')[1]}-train.txt"),
                        "split": datasets.Split.TRAIN,
                    },
                ),
                datasets.SplitGenerator(
                    name=datasets.Split.VALIDATION,
                    gen_kwargs={
                        "datafile": os.path.join(dl_dir, f"{self.config.name.split('.')[1]}-valid.txt"),
                        "split": datasets.Split.VALIDATION,
                    },
                ),
                datasets.SplitGenerator(
                    name=datasets.Split.TEST,
                    gen_kwargs={
                        "datafile": os.path.join(dl_dir, f"{self.config.name.split('.')[1]}-test.txt"),
                        "split": datasets.Split.TEST,
                    },
                ),
            ]

    def _generate_examples(self, **args):
        """Yields examples."""
        filepath = args["datafile"]

        if self.config.name.startswith("wnli"):
            if args["key"] == "test-split":
                with open(filepath, encoding="utf-8") as f:
                    data = csv.DictReader(f)
                    for id_, row in enumerate(data):
                        yield id_, {"hypothesis": row["sentence1"], "premise": row["sentence2"], "label": "None"}
            else:
                with open(filepath, encoding="utf-8") as f:
                    data = csv.DictReader(f)
                    for id_, row in enumerate(data):
                        label = "entailment" if row["label"] else "not_entailment"
                        yield id_, {
                            "hypothesis": row["sentence1"],
                            "premise": row["sentence2"],
                            "label": label,
                        }

        if self.config.name.startswith("copa"):
            if args["key"] == "test-split":
                with open(filepath, "r", encoding="utf-8") as f:
                    lines = f.readlines()
                    data = map(lambda l: json.loads(l), lines)
                    data = list(data)
                    for id_, row in enumerate(data):
                        yield id_, {
                            "premise": row["premise"],
                            "choice1": row["choice1"],
                            "choice2": row["choice2"],
                            "question": row["question"],
                            "label": 0,
                        }
            else:
                with open(filepath, "r", encoding="utf-8") as f:
                    lines = f.readlines()
                    data = map(lambda l: json.loads(l), lines)
                    data = list(data)
                    for id_, row in enumerate(data):
                        yield id_, {
                            "premise": row["premise"],
                            "choice1": row["choice1"],
                            "choice2": row["choice2"],
                            "question": row["question"],
                            "label": row["label"],
                        }

        if self.config.name.startswith("sna"):
            df = pd.read_csv(filepath, names=["label", "text"])
            for id_, row in df.iterrows():
                yield id_, {"text": row["text"], "label": row["label"]}

        if self.config.name.startswith("csqa"):
            with open(filepath, encoding="utf-8") as f:
                data = json.load(f)
                df = pd.DataFrame(data["cloze_data"])
                df["out_of_context_options"].loc[df["out_of_context_options"].isnull()] = (
                    df["out_of_context_options"].loc[df["out_of_context_options"].isnull()].apply(lambda x: [])
                )
                for id_, row in df.iterrows():
                    yield id_, {
                        "question": row["question"],
                        "answer": row["answer"],
                        "category": row["category"],
                        "title": row["title"],
                        "out_of_context_options": row["out_of_context_options"],
                        "options": row["options"],
                    }

        if self.config.name.startswith("wstp"):
            df = pd.read_json(filepath)
            for id_, row in df.iterrows():
                yield id_, {
                    "sectionText": row["sectionText"],
                    "correctTitle": row["correctTitle"],
                    "titleA": row["titleA"],
                    "titleB": row["titleB"],
                    "titleC": row["titleC"],
                    "titleD": row["titleD"],
                    "url": row["url"],
                }

        if (
            self.config.name.startswith("inltkh")
            or self.config.name.startswith("bbca")
            or self.config.name.startswith("iitp")
        ):
            df = pd.read_csv(filepath, names=["label", "text"])
            for id_, row in df.iterrows():
                yield id_, {"text": row["text"], "label": row["label"]}

        if self.config.name.startswith("actsa"):
            df = pd.read_csv(filepath, names=["label", "text"])
            for id_, row in df.iterrows():
                label = "positive" if row["label"] else "negative"
                yield id_, {"text": row["text"], "label": label}

        if self.config.name.startswith("cvit"):
            source = args["src"]
            target = args["tgt"]

            src, tgt = open(source, "r", encoding="utf-8"), open(target, "r", encoding="utf-8")
            src, tgt = src.readlines(), tgt.readlines()

            for id_, row in enumerate(zip(src, tgt)):
                yield id_, {"sentence1": row[0], "sentence2": row[1]}

        if self.config.name.startswith("md"):
            df = pd.read_json(filepath)
            for id_, row in df.iterrows():
                yield id_, {
                    "story_number": row["Story_no"],
                    "sentence": row["Sentence"],
                    "discourse_mode": row["Discourse Mode"],
                    "id": row["id"],
                }

        if self.config.name.startswith("wiki-ner"):
            with open(filepath, "r", encoding="utf-8") as f:
                data = f.readlines()
                for id_, row in enumerate(data):
                    tokens = []
                    labels = []
                    infos = []

                    row = row.split()

                    if len(row) == 0:
                        yield id_, {"tokens": tokens, "ner_tags": labels, "additional_info": infos}
                        continue

                    tokens.append(row[0])
                    labels.append(row[-1])
                    infos.append(row[1:-1])

    def _get_task_name_from_data_url(self, data_url):
        return data_url.split("/")[-1].split(".")[0]
