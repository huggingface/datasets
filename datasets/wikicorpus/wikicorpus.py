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
"""Wikicorpus dataset."""

import re

import datasets


_CITATION = """\
@inproceedings{reese-etal-2010-wikicorpus,
    title = "{W}ikicorpus: A Word-Sense Disambiguated Multilingual {W}ikipedia Corpus",
    author = "Reese, Samuel  and
      Boleda, Gemma  and
      Cuadros, Montse  and
      Padr{\'o}, Llu{\'i}s  and
      Rigau, German",
    booktitle = "Proceedings of the Seventh International Conference on Language Resources and Evaluation ({LREC}'10)",
    month = may,
    year = "2010",
    address = "Valletta, Malta",
    publisher = "European Language Resources Association (ELRA)",
    url = "http://www.lrec-conf.org/proceedings/lrec2010/pdf/222_Paper.pdf",
    abstract = "This article presents a new freely available trilingual corpus (Catalan, Spanish, English) that contains large portions of the Wikipedia and has been automatically enriched with linguistic information. To our knowledge, this is the largest such corpus that is freely available to the community: In its present version, it contains over 750 million words. The corpora have been annotated with lemma and part of speech information using the open source library FreeLing. Also, they have been sense annotated with the state of the art Word Sense Disambiguation algorithm UKB. As UKB assigns WordNet senses, and WordNet has been aligned across languages via the InterLingual Index, this sort of annotation opens the way to massive explorations in lexical semantics that were not possible before. We present a first attempt at creating a trilingual lexical resource from the sense-tagged Wikipedia corpora, namely, WikiNet. Moreover, we present two by-products of the project that are of use for the NLP community: An open source Java-based parser for Wikipedia pages developed for the construction of the corpus, and the integration of the WSD algorithm UKB in FreeLing.",
}
"""

_DESCRIPTION = """\
The Wikicorpus is a trilingual corpus (Catalan, Spanish, English) that contains large portions of the Wikipedia (based on a 2006 dump) and has been automatically enriched with linguistic information. In its present version, it contains over 750 million words.
"""

_HOMEPAGE = "https://www.cs.upc.edu/~nlp/wikicorpus/"

_LICENSE = "GNU Free Documentation License"

_URLs = "https://www.cs.upc.edu/~nlp/wikicorpus/{form}.{language}.tgz"

_LANGUAGES = ["ca", "es", "en"]
_FORMS = ["raw", "tagged"]

METADATA_PATTERN = re.compile(r'.+id="(?P<id>[^"]+)".+title="(?P<title>[^"]+)".+')


class WikicorpusConfig(datasets.BuilderConfig):
    """BuilderConfig for Wikicorpus."""

    def __init__(self, form=None, language=None, **kwargs):
        """
        Args:
            form: form of the dataset.
            language: language of the dataset.
            **kwargs: keyword arguments forwarded to super.
        """
        super().__init__(
            name=f"{form}_{language}",
            description=f"Wikicorpus dataset in {form} form and {language} language.",
            **kwargs,
        )
        self.form = form
        self.language = language


class Wikicorpus(datasets.GeneratorBasedBuilder):
    """Wikicorpus dataset."""

    VERSION = datasets.Version("1.0.0")
    BUILDER_CONFIG_CLASS = WikicorpusConfig
    BUILDER_CONFIGS = [WikicorpusConfig(form=form, language=language) for form in _FORMS for language in _LANGUAGES]

    def _info(self):
        if self.config.form == "raw":
            features = datasets.Features(
                {
                    "id": datasets.Value("string"),
                    "title": datasets.Value("string"),
                    "text": datasets.Value("string"),
                }
            )
        elif self.config.form == "tagged":
            features = datasets.Features(
                {
                    "id": datasets.Value("string"),
                    "title": datasets.Value("string"),
                    "sentence": datasets.Sequence(datasets.Value("string")),
                    "lemmas": datasets.Sequence(datasets.Value("string")),
                    "pos_tags": datasets.Sequence(datasets.Value("string")),
                    "wordnet_senses": datasets.Sequence(datasets.Value("string")),
                }
            )
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=features,
            supervised_keys=None,
            homepage=_HOMEPAGE,
            license=_LICENSE,
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        url_to_download = _URLs.format(form=self.config.form, language=self.config.language)
        archive = dl_manager.download(url_to_download)
        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                gen_kwargs={
                    "files": dl_manager.iter_archive(archive),
                },
            ),
        ]

    def _generate_examples(self, files):
        for file_idx, (path, f) in enumerate(files):
            example = {}
            # raw
            text = []
            # tagged
            words = []
            lemmas = []
            pos_tags = []
            wordnet_senses = []
            for row_idx, row in enumerate(f):
                row = row.decode("latin-1")
                if self.config.form == "raw":
                    if row.startswith("<doc id"):
                        metadata_match = METADATA_PATTERN.match(row)
                        example["id"] = metadata_match.group("id") if metadata_match else ""
                        example["title"] = metadata_match.group("title") if metadata_match else ""
                    elif row.startswith("</doc>"):
                        pass
                    elif row.startswith("ENDOFARTICLE"):
                        yield f"{file_idx}_{row_idx}", {
                            "id": example["id"],
                            "title": example["title"],
                            "text": "\n".join(text).strip(),
                        }
                        example = {}
                        text = []
                    else:
                        text.append(row)
                elif self.config.form == "tagged":
                    if row.startswith("<doc id"):
                        metadata_match = METADATA_PATTERN.match(row)
                        example["id"] = metadata_match.group("id") if metadata_match else ""
                        example["title"] = metadata_match.group("title") if metadata_match else ""
                    elif row.startswith("</doc>"):
                        pass
                    elif row.startswith("ENDOFARTICLE") or row.startswith("\n"):
                        if len(words) > 1:  # some content besides only (. . Fp 0)
                            yield f"{file_idx}_{row_idx}", {
                                "id": example["id"],
                                "title": example["title"],
                                "sentence": words,
                                "lemmas": lemmas,
                                "pos_tags": pos_tags,
                                "wordnet_senses": wordnet_senses,
                            }
                        words = []
                        lemmas = []
                        pos_tags = []
                        wordnet_senses = []
                        if row.startswith("ENDOFARTICLE"):
                            example = {}
                    else:
                        splits = row.split()
                        for tag, tags in zip(splits, [words, lemmas, pos_tags, wordnet_senses]):
                            tags.append(tag)
