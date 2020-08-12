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
"""Utilities for generating the C4 dataset."""

from __future__ import absolute_import, division, print_function

import functools
import gzip
import hashlib
import io
import re
import threading


# WET file constants
_PAGE_DELIMITER = "WARC/1.0"
_URL_KEY = "WARC-Target-URI:"
_URL_DATE = "WARC-Date:"
_CONTENT_TYPE = "Content-Type:"
_CONTENT_LEN = "Content-Length:"
_METADATA_PREFIXES = ("WARC", "CONTENT-", "Content-")

# Filters
_MIN_WORDS_PER_LINE = 5
_MIN_NUM_SENTENCES = 3
_MAX_WORD_LENGTH = 1000
_END_MARKS = (".", "?", "!", '"')
_ELLIPSIS = "..."
_POLICY_SUBSTRINGS = [
    "terms of use",
    "privacy policy",
    "cookie policy",
    "uses cookies",
    "use of cookies",
    "use cookies",
]

# Memoized sentence tokenizer.
_SENTENCE_TOKENIZER = None


def get_counter_inc_fn(namespace):
    import apache_beam as beam

    def counter_inc_fn(counter, amt=1):
        beam.metrics.Metrics.counter(namespace, counter).inc(amt)

    return counter_inc_fn


def get_hashed_url_filter_fn(predicate_fn):
    import tensorflow.compat.v2 as tf

    def filter_fn(el):
        url, _ = el
        val = int(hashlib.md5(tf.compat.as_text(url).encode("utf-8")).hexdigest(), 16)
        return predicate_fn(val)

    return filter_fn


def _load_sentence_tokenizer():
    """Returns a sentence tokenization function."""
    # Lock to avoid a race-condition in the creation of the download directory.
    with threading.Lock():
        import nltk

        nltk.download("punkt")
        return nltk.data.load("nltk:tokenizers/punkt/english.pickle")


def _get_sentences(text):
    import tensorflow.compat.v2 as tf

    global _SENTENCE_TOKENIZER
    if not _SENTENCE_TOKENIZER:
        _SENTENCE_TOKENIZER = _load_sentence_tokenizer()
    return list(_SENTENCE_TOKENIZER.tokenize(tf.compat.as_text(text)))


def _get_sentences_by_line(text, lower=False):
    sentences = []
    for line in text.splitlines():
        sentences.append([s.lower() if lower else s for s in _get_sentences(line)])
    return sentences


def is_language(page, language, min_probability=0.99):
    """Returns True iff text is in `language` with at least `min_probability`."""
    unused_url, features = page
    text = features["text"]

    counter_inc_fn = get_counter_inc_fn("detected-lang")

    # Make langdetect predictions deterministic.
    import langdetect

    langdetect.DetectorFactory.seed = 0
    try:
        predictions = langdetect.detect_langs(text)
    except langdetect.lang_detect_exception.LangDetectException:
        counter_inc_fn("langdetect-exception")
        return False
    if not predictions:
        counter_inc_fn("page-filtered-nolangpredictions")
        return False
    best_prediction = predictions[0]
    if best_prediction.prob < min_probability:
        counter_inc_fn("page-filtered-lowlangdetectconf")
        return False
    if best_prediction.lang != language:
        counter_inc_fn("page-filtered-ignoredlang")
        counter_inc_fn("page-filtered-ignoredlang-%s" % (best_prediction.lang))
        return False
    counter_inc_fn("page-emited-%s" % best_prediction.lang)
    return True


def get_clean_page_fn(badwords=None):
    """Returns `clean_page` with pre-compiled badword and citation regexes."""
    # Used to filter citation from Wikipedia pages (among others).
    citation_regex = re.compile(r"\[\d*\]|\[edit\]|\[citation needed\]")
    if badwords:
        badwords_regex = re.compile("[^a-z]({})[^a-z]".format("|".join(badwords or [])))
    else:
        badwords_regex = None
    return functools.partial(clean_page, citation_regex=citation_regex, badwords_regex=badwords_regex)


def clean_page(
    url_and_features,
    citation_regex,
    badwords_regex=None,
    counter_inc_fn=None,
    min_words_per_line=_MIN_WORDS_PER_LINE,
    min_num_sentences=_MIN_NUM_SENTENCES,
    max_word_length=_MAX_WORD_LENGTH,
):
    """Cleans a CommonCrawl page, yielding nothing if it should be skipped.

    Cleaning removes lines with no end marks or with too few words. After line
    filtering, pages are filtered out if they have too few sentences based on a
    simple count of end marks.

    Args:
        url_and_features: tuple(string, dict), the url and features of the page.
        citation_regex: Regex to use for finding Wikipedia-like citations to filter.
        badwords_regex: Regex to use for finding badwords. Default None, which means
            don't apply badwords filtering.
        counter_inc_fn: function, a function taking the name of a counter to be
            incremented and the (optional) amount. Defaults to a beam Metric counter.
        min_words_per_line: int, the minimum number of words a line needs to not be
            removed.
        min_num_sentences: int, the minimum number of sentences a page needs to not
            be skipped.
        max_word_length: int, the maximum number of characters allowed in a word.
            Lines containing a word with too many characters are removed.
    Yields:
        The url and cleaned text for the page.
    """
    url, features = url_and_features
    text = features["text"]

    if not counter_inc_fn:
        counter_inc_fn = get_counter_inc_fn("clean-page")

    lines = text.splitlines()
    valid_lines = []
    num_sentences = 0

    def line_has_too_long_word(line):
        for word in line.split():
            if len(word) > max_word_length:
                return True
        return False

    for line in lines:
        line = line.strip()
        if line_has_too_long_word(line):
            counter_inc_fn("lines-with-too-long-word")
            continue
        line = citation_regex.sub("", line)
        if not line.endswith(_END_MARKS) or line.endswith(_ELLIPSIS):
            counter_inc_fn("lines-no-endmark")
            continue
        if len(line.split()) < min_words_per_line:
            counter_inc_fn("lines-too-short")
            continue
        line_lower = line.lower()
        # Remove documents which contain lorem ipsum
        if "lorem ipsum" in line_lower:
            counter_inc_fn("filtered-page-loremipsum")
            return
        # Remove "javascript must be enabled" notices
        if "javascript" in line_lower:
            counter_inc_fn("lines-javascript")
            continue
        # Remove docs which probably contain javascript code
        if "{" in line:
            counter_inc_fn("filtered-page-squigglybracket")
            return
        # Remove policy lines
        if any(p in line_lower for p in _POLICY_SUBSTRINGS):
            counter_inc_fn("lines-policy")
            continue
        # If any badword appears on its own in the line, skip this doc
        if badwords_regex:
            badwords_found = badwords_regex.search(line_lower)
            if badwords_found is not None:
                counter_inc_fn("filtered-page-badword")
                return
        num_sentences += len(_get_sentences(line))
        valid_lines.append(line)
        counter_inc_fn("lines-valid")

    if num_sentences < min_num_sentences:
        counter_inc_fn("filtered-page-toofewsentences")
        return
    counter_inc_fn("emitted-clean-pages")
    features["text"] = "\n".join(valid_lines).strip()
    yield url, features


def _hash_line(line):
    import tensorflow.compat.v2 as tf

    m = hashlib.md5()
    m.update(tf.compat.as_text(line).encode("utf-8").strip().lower())
    return m.hexdigest()


def _emit_url_to_lines(page):
    """Emits url to all (lower-cased, hashed) lines."""
    url, features = page
    text = features["text"]
    for line in text.split("\n"):
        yield _hash_line(line), url


def _emit_line_to_urls(el, counter_inc_fn):
    """Emits (hashed) line to all but one url."""
    import tensorflow.compat.v2 as tf

    line, urls = el
    # Materialize urls as a list.
    urls = list(urls)
    # Hash urls and sort to have a consistent, but unbiased, selection when the
    # same urls exist for multiple lines.
    skip_url = min(urls, key=lambda x: hashlib.md5(tf.compat.as_text(x).encode("utf-8")).hexdigest())
    for url in urls:
        if url != skip_url:
            yield url, line
    counter_inc_fn("emitted-line-duplicate", amt=len(urls) - 1)


def _remove_lines_from_text(el, counter_inc_fn, min_num_sentences=_MIN_NUM_SENTENCES):
    """Removes matching lines from the page.

    Process the result of a join containing a single value for 'features' and zero
    or more values for 'lines'. Each value in 'lines' is a lower-cased, hashed
    line.

    If a line has fewer sentences than `max_window_size`, the full line is
    compared for a match.

    Args:
        el: `(string, {'features': features_dict, 'lines': [string]})`,
            element containing the result of a join on key with both the page text
            and lower-cased, hashed lines to remove.
        counter_inc_fn: function, a function taking the name of a counter to be
            incremented and the (optional) amount.
        min_num_sentences: int, the minimum number of sentences a page needs to not
            be skipped.

    Yields:
        url: The URL of the page.
        features: The page features with lines removed from text.
    """
    url, join_values = el
    features = join_values["features"]

    assert len(features) == 1, "Invalid page count (%d) for %s" % (len(features), url)
    features = features[0]
    text = features["text"]
    lines_to_remove = set(join_values["lines"])
    new_lines = []
    hashed_lines = set()
    for line in text.split("\n"):
        hashed_line = _hash_line(line)
        if hashed_line in lines_to_remove:
            counter_inc_fn("filtered-lines-duplicate")
        elif hashed_line not in hashed_lines:
            new_lines.append(line)
            hashed_lines.add(hashed_line)
    new_text = "\n".join(new_lines)
    if len(_get_sentences(new_text)) < min_num_sentences:
        counter_inc_fn("filtered-doc-toofewsentences")
        return
    new_features = features.copy()
    new_features["text"] = new_text
    yield (url, new_features)


def remove_duplicate_text(pages):
    """Utility to remove duplicate lines across text documents."""
    # Output: url, lines
    import apache_beam as beam

    counter_inc_fn = get_counter_inc_fn("dedupe-lines")
    lines_to_remove = (
        pages
        | beam.FlatMap(_emit_url_to_lines)
        | "group_sentences" >> beam.GroupByKey()
        | beam.FlatMap(_emit_line_to_urls, counter_inc_fn=counter_inc_fn)
    )

    # Output: url, text
    final_docs = (
        {"features": pages, "lines": lines_to_remove}
        | "group_features_and_lines_by_url" >> beam.CoGroupByKey()
        | beam.FlatMap(_remove_lines_from_text, counter_inc_fn=counter_inc_fn)
    )

    return final_docs


def split_wet_file(wet_file_path, counter_inc_fn=None):
    """Split a WET file into separate pages."""
    from absl import logging

    logging.info("Splitting file: %s", wet_file_path)
    if not counter_inc_fn:
        counter_inc_fn = get_counter_inc_fn("split-wet-file")
    counter_inc_fn("wet-file")

    import apache_beam as beam

    with beam.io.filesystems.FileSystems.open(wet_file_path) as f, gzip.GzipFile(fileobj=f) as g:
        url = None
        content = None
        content_len = None
        content_type = None
        timestamp = None

        def _maybe_get_page():
            """Generate a (url, {features}) page."""
            if not url and url is not None:
                counter_inc_fn("page-filtered-nourl")
            if not content and content is not None:
                counter_inc_fn("page-filtered-nocontent")
            if not content_type and content_type is not None:
                counter_inc_fn("page-nocontenttype")
            if not content_len and content_len is not None:
                counter_inc_fn("page-nocontentlen")
            if not timestamp and timestamp is not None:
                counter_inc_fn("page-notimestamp")
            if content and url:
                counter_inc_fn("page-emitted")
                return (
                    url,
                    {
                        "text": "\n".join(content),
                        "content-type": content_type,
                        "content-length": content_len,
                        "timestamp": timestamp,
                        "url": url,
                    },
                )
            return None

        for line in io.TextIOWrapper(g, encoding="utf-8"):
            line = line.strip()
            if not line:
                continue
            if line == _PAGE_DELIMITER:
                page = _maybe_get_page()
                if page:
                    yield page
                url = ""
                content = []
                content_len = ""
                content_type = ""
                timestamp = ""

            if line.startswith(_URL_KEY):
                url = line[len(_URL_KEY) :].strip()

            if line.startswith(_URL_DATE):
                timestamp = line[len(_URL_DATE) :].strip()

            if line.startswith(_CONTENT_TYPE):
                content_type = line[len(_CONTENT_TYPE) :].strip()

            if line.startswith(_CONTENT_LEN):
                content_len = line[len(_CONTENT_LEN) :].strip()

            if line.startswith(_METADATA_PREFIXES):
                continue

            content.append(line)

        page = _maybe_get_page()
        if page:
            yield page


def dedupe_urls(el):
    """Returns the first value for a given URL."""
    counter_inc_fn = get_counter_inc_fn("dedupe-urls")
    url, vals = el
    cnt = 0
    v = None
    for v in vals:
        cnt += 1
    counter_inc_fn("filtered-url-duplicate", cnt - 1)
    counter_inc_fn("unique-url")
    return url, v


def is_valid_length(el, max_length=1.9e5):
    """Returns False iff page's text is too long."""
    counter_inc_fn = get_counter_inc_fn("is-valid-length")
    _, page = el
    if len(page["text"]) > max_length:
        counter_inc_fn("filtered-page-contenttoolong")
        return False
    counter_inc_fn("valid-length")
    return True


def is_realnews_domain(el, realnews_domains):
    """Returns False iff page's (sub)domain is not allowed."""
    import tldextract

    counter_inc_fn = get_counter_inc_fn("is-realnews-domain")
    url, _ = el
    ext = tldextract.extract(url)
    main_domain = ext.domain + "." + ext.suffix
    if main_domain not in realnews_domains:
        counter_inc_fn("filtered-url-invaliddomain")
        return False
    allowed_subdomains = realnews_domains[main_domain]
    if isinstance(allowed_subdomains, list) and ext.subdomain not in allowed_subdomains:
        counter_inc_fn("filtered-url-invalidsubdomain")
        return False
    counter_inc_fn("realnews-domain")
    return True


def filter_by_webtextlike(el):
    """Yields only pages with a matching WebText-like URL."""
    counter_inc_fn = get_counter_inc_fn("filter-by-webtextlike")
    url, join_values = el
    text = join_values["text"]
    webtextlike = join_values["webtextlike_urls"]
    if not webtextlike:
        counter_inc_fn("filtered-url-notwebtextlike")
        return
    if not text:
        counter_inc_fn("missing-webtextlike")
        return
    assert len(text) == 1
    counter_inc_fn("found-webtextlike")
    yield url, text[0]


def normalize_url(el):
    import tensorflow.compat.v2 as tf

    url, val = el
    url = tf.compat.as_text(url)
    url = re.sub(r"https?:\/\/(www\.)?", "", url)
    url = re.sub(r"\?(utm_|ref|feed).*", "", url)
    url = url.rstrip("/")
    return url, val
