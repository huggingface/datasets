# coding=utf-8
# Copyright 2020 The TensorFlow Datasets Authors and the HuggingFace NLP Authors.
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
"""C4 dataset based on Common Crawl."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import json
import os

import logging
import nlp
from . import c4_utils
_DESCRIPTION = """\
A colossal, cleaned version of Common Crawl's web crawl corpus.

Based on Common Crawl dataset: "https://commoncrawl.org"

Due to the overhead of cleaning the dataset, it is recommend you prepare it with
a distributed service like Cloud Dataflow. More info at
https://www.tensorflow.org/datasets/beam_datasets.
"""
_CITATION = """
@article{2019t5,
    author = {Colin Raffel and Noam Shazeer and Adam Roberts and Katherine Lee and Sharan Narang and Michael Matena and Yanqi Zhou and Wei Li and Peter J. Liu},
    title = {Exploring the Limits of Transfer Learning with a Unified Text-to-Text Transformer},
    journal = {arXiv e-prints},
    year = {2019},
    archivePrefix = {arXiv},
    eprint = {1910.10683},
}
"""
_VERSION = nlp.Version("2.3.0", "Deduplicate lines within a page.")

_SUPPORTED_VERSIONS = [
        nlp.Version("2.2.1", "Update dataset_info.json"),
        nlp.Version("2.2.0"),
]

_DOWNLOAD_HOST = "https://commoncrawl.s3.amazonaws.com"
_WET_PATH_URL = "https://commoncrawl.s3.amazonaws.com/crawl-data/CC-MAIN-{cc_version}/wet.paths.gz"
_REALNEWS_DOMAINS_URL = "https://raw.githubusercontent.com/rowanz/grover/38f7184bd87237ae2d3bc330b99f1e2e246f6d51/realnews/domain_to_allowed_subdomains.json"
_BADWORDS_URL = "https://raw.githubusercontent.com/LDNOOBW/List-of-Dirty-Naughty-Obscene-and-Otherwise-Bad-Words/25e679f03d96baa721cde20db9944649e8d0a844/{lang}"
_CHECKSUMS_URL = "https://storage.googleapis.com/tfds-data/manual_checksums/c4.txt"
_OPENWEBTEXT_URLS_ZIP = "OpenWebText.zip"
_OPENWEBTEXT_URLS_URL = "https://mega.nz/#F!EZZD0YwJ!9_PlEQzdMVLaNdKv_ICNVQ"
_OPENWEBTEXT_URLS_FILE_PATTERN = "OpenWebText/Version 1/URLs/*.txt"

_DEFAULT_CC_VERSIONS = ("2019-18",)  # April 2019
_DEFAULT_WEBTEXTLIKE_CC_VERSIONS = (  # August 2018 - July 2019
        "2018-34", "2018-39", "2018-43", "2018-47", "2018-51",
        "2019-04", "2019-09", "2019-13", "2019-18", "2019-22", "2019-26", "2019-30")


class C4Config(nlp.BuilderConfig):
    """BuilderConfig for C4 dataset."""

    def __init__(self,
                             language,
                             cc_versions=None,
                             clean=True,
                             realnewslike=False,
                             webtextlike=False,
                             **kwargs):
        """BuilderConfig for C4.

        Args:
            language: string, the language code, or "all" to disable language
                filtering.
            cc_versions: tuple(string), a collection of versions of Common Crawl to
                use as the raw source text. Set to None to use defaults.
            clean: bool, whether to clean the dataset for badwords, duplications, etc.
            realnewslike: bool, whether to limit to news domains as compiled by
                RealNews.
            webtextlike: bool, whether to limit to WebText-like URLs.
            **kwargs: keyword arguments forwarded to super.
        """
        name_parts = [language]
        if cc_versions:
            name_parts.append("_".join(cc_versions))
        if not clean:
            name_parts.append("noclean")
        if realnewslike:
            name_parts.append("realnewslike")
        if webtextlike:
            name_parts.append("webtextlike")
        name = ".".join(name_parts)
        super(C4Config, self).__init__(
                name=name,
                version=_VERSION,
                supported_versions=_SUPPORTED_VERSIONS,
                **kwargs)
        self.lang = language
        self.cc_versions = cc_versions or (
                _DEFAULT_WEBTEXTLIKE_CC_VERSIONS if webtextlike else
                _DEFAULT_CC_VERSIONS)
        self.clean = clean
        self.realnewslike = realnewslike
        self.webtextlike = webtextlike


class C4(nlp.BeamBasedBuilder):
    """C4 dataset based on Common Crawl."""

    MANUAL_DOWNLOAD_INSTRUCTIONS = """\
    For the WebText-like config, you must manually download 'OpenWebText.zip'
    (from https://mega.nz/#F!EZZD0YwJ!9_PlEQzdMVLaNdKv_ICNVQ) and the Common Crawl
    WET files from August 2018 to July 2019
    (https://commoncrawl.org/the-data/get-started/) and place them in the
    `manual_dir`.
    """

    BUILDER_CONFIGS = [
            C4Config(language="en", description="English C4 dataset."),
            C4Config(
                    language="en",
                    clean=False,
                    description="Disables all cleaning (deduplication, removal based on bad words, "
                    "etc.)"),
            C4Config(
                    language="en",
                    realnewslike=True,
                    description="Filters from the default config to only include content from the "
                    "domains used in the 'RealNews' dataset (Zellers et al., 2019)."),
            C4Config(
                    language="en",
                    webtextlike=True,
                    description="Filters from the default config to only include content from the "
                    "URLs in OpenWebText (https://github.com/jcpeterson/openwebtext)."),
    ]

    def _info(self):
        features = {
                "text": nlp.string,
                "url": nlp.string,
        }
        if self.version > "1.0.0":
            features.update({
                    "content-type": nlp.string,
                    "content-length": nlp.string,
                    "timestamp": nlp.string,
            })
        return nlp.DatasetInfo(
                builder=self,
                description=_DESCRIPTION,
                features=nlp.features.FeaturesDict(features),
                citation=_CITATION,
                homepage=
                "https://github.com/google-research/text-to-text-transfer-transformer#datasets",
        )

    def _split_generators(self, dl_manager, pipeline):
        dl_manager.download_checksums(_CHECKSUMS_URL)

        # We will automatically down the default CC version(s), but others need to
        # be manually downloaded.
        cc_versions = set(self.builder_config.cc_versions)
        auto_cc_versions = cc_versions & set(_DEFAULT_CC_VERSIONS)
        manual_cc_versions = cc_versions - set(_DEFAULT_CC_VERSIONS)

        files_to_download = {}
        files_to_download["wet_urls"] = [
                _WET_PATH_URL.format(cc_version=cc_version)
                for cc_version in auto_cc_versions]
        if self.builder_config.clean:
            files_to_download["badwords"] = _BADWORDS_URL.format(
                    lang=self.builder_config.lang)
        if self.builder_config.realnewslike:
            files_to_download["realnews_domains"] = _REALNEWS_DOMAINS_URL
        file_paths = dl_manager.download_and_extract(files_to_download)

        if self.builder_config.webtextlike:
            owt_path = os.path.join(dl_manager.manual_dir, _OPENWEBTEXT_URLS_ZIP)
            if not nlp.io.gfile.exists(owt_path):
                raise AssertionError(
                        "For the WebText-like config, you must manually download the "
                        "following file from {0} and place it in {1}: {2}".format(
                                _OPENWEBTEXT_URLS_URL, dl_manager.manual_dir,
                                _OPENWEBTEXT_URLS_ZIP))
            file_paths["openwebtext_urls_zip"] = dl_manager.extract(owt_path)

        wet_urls = []
        for wet_urls_path in file_paths["wet_urls"]:
            with open(wet_urls_path) as f:
                wet_urls.extend(["%s/%s" % (_DOWNLOAD_HOST, l.strip()) for l in f])
        file_paths.update(dl_manager.download({"wet_files": wet_urls}))

        for cc_version in manual_cc_versions:
            cc_dir = os.path.join(dl_manager.manual_dir, cc_version)
            wet_files = nlp.io.gfile.glob(os.path.join(cc_dir, "*.warc.wet.gz"))
            if not nlp.io.gfile.exists(cc_dir):
                raise AssertionError(
                        "For the non-default Common Crawl version {0}, you must manually "
                        "download the WET files to the directory {1}.".format(
                                cc_version, cc_dir))
            logging.info(
                    "Adding %d WET files for manually downloaded version %s.",
                    len(wet_files), cc_version)
            file_paths["wet_files"].extend(wet_files)

        page_content_pcollection = self._get_page_content(pipeline, file_paths)
        return [
                nlp.SplitGenerator(
                        name=nlp.Split.TRAIN,
                        gen_kwargs=dict(
                                split="train",
                                page_content=page_content_pcollection,
                                hashed_url_predicate=lambda x: x % 1000 != 0  # 99.9%
                        ),
                ),
                nlp.SplitGenerator(
                        name=nlp.Split.VALIDATION,
                        gen_kwargs=dict(
                                split="validation",
                                page_content=page_content_pcollection,
                                hashed_url_predicate=lambda x: x % 1000 == 0  # 0.01%
                        ),
                ),
        ]

    def _get_page_content(self, pipeline, file_paths):
        """Build PCollection of un-split page content."""
        beam = nlp.lazy_imports.apache_beam

        # Parse WET files and filter by length.
        # Output: url, text
        page_content = (
                pipeline
                | beam.Create(file_paths["wet_files"])
                | beam.FlatMap(c4_utils.split_wet_file)
                | beam.Filter(c4_utils.is_valid_length))

        # Optionally filter for RealNews domains.
        # Output: url, text
        if self.builder_config.realnewslike:
            with open(file_paths["realnews_domains"]) as f:
                realnews_domains = json.load(f)
            page_content = (
                    page_content
                    | beam.Filter(c4_utils.is_realnews_domain, realnews_domains))

        # Normalize and deduplicate by URL.
        # Output: url, text
        page_content = (
                page_content
                | "normalize_url" >> beam.Map(c4_utils.normalize_url)
                | "group_url" >> beam.GroupByKey()
                | beam.Map(c4_utils.dedupe_urls))

        # Optionally filter for WebText-like URLs.
        # Output: url, text
        if self.builder_config.webtextlike:
            webtextlike_urls = (
                    pipeline
                    | "read_webtextlike_urls" >>
                    beam.io.ReadFromText(
                            os.path.join(file_paths["openwebtext_urls_zip"],
                                                     _OPENWEBTEXT_URLS_FILE_PATTERN))
                    | "add_dummy_page" >> beam.Map(lambda x: (x, ""))
                    | "normal_webtext_url" >> beam.Map(c4_utils.normalize_url))
            page_content = (
                    {
                            "text": page_content,
                            "webtextlike_urls": webtextlike_urls
                    }
                    | "group_webtextlike_urls" >> beam.CoGroupByKey()
                    | beam.FlatMap(c4_utils.filter_by_webtextlike))

        # Optionally clean pages of badwords, boilerpolate text, and duplicate
        # spans of sentences.
        # Output: url, text
        if self.builder_config.clean:
            with open(file_paths["badwords"]) as f:
                badwords = [l.strip() for l in f]
            page_content = (
                    page_content
                    | "clean_pages" >> beam.FlatMap(c4_utils.get_clean_page_fn(badwords)))
            page_content = c4_utils.remove_duplicate_text(page_content)

        # Optionally filter out non-`language` pages. We do this after cleaning
        # since it may change the predominate language.
        if self.builder_config.lang != "all":
            page_content |= beam.Filter(
                    c4_utils.is_language, language=self.builder_config.lang)

        return page_content

    def _build_pcollection(
            self, unused_pipeline, split, page_content, hashed_url_predicate):
        beam = nlp.lazy_imports.apache_beam

        def _emit_examples(el):
            c4_utils.get_counter_inc_fn(split)("examples")
            _, features = el
            return features["url"], {
                    "url": features["url"],
                    "text": features["text"],
                    "content-type": features["content-type"],
                    "content-length": features["content-length"],
                    "timestamp": features["timestamp"]
            }
        return (page_content
                        | beam.Filter(
                                c4_utils.get_hashed_url_filter_fn(hashed_url_predicate))
                        | beam.Map(_emit_examples))
