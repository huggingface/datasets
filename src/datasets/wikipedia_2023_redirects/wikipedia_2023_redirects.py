# coding=utf-8
"""Wikipedia 2023 snapshot with redirect resolution and pageviews aggregation.
"""
from __future__ import annotations

import csv
import html
import xml.etree.ElementTree as ET
from dataclasses import dataclass
from typing import Dict, Iterator, List, Optional, Tuple

import datasets

_CITATION = """\
@misc{wikipedia2023redirects,
  title        = {Wikipedia 2023 with Redirects and Pageviews},
  author       = {Wikimedia Foundation},
  year         = {2023},
  howpublished = {https://dumps.wikimedia.org/},
  note         = {Aggregated by this dataset loader. Wikipedia text is CC BY-SA 3.0; pageviews data is public domain.}
}
"""

_DESCRIPTION = """\
Wikipedia 2023 snapshot with redirect resolution and 2023 pageview aggregates.
Each example is one canonical page with id, title, url, text, redirects, pageviews_2023, timestamp.
"""

_HOMEPAGE = "https://dumps.wikimedia.org/"
_LICENSE = "CC-BY-SA-3.0 (Wikipedia text), Public Domain (pageviews)"


class Wikipedia2023RedirectsConfig(datasets.BuilderConfig):
    def __init__(self, language: str = "en", **kwargs):
        super().__init__(version=datasets.Version("1.0.0"), **kwargs)
        self.language = language


class Wikipedia2023Redirects(datasets.GeneratorBasedBuilder):
    BUILDER_CONFIG_CLASS = Wikipedia2023RedirectsConfig
    BUILDER_CONFIGS = [
        Wikipedia2023RedirectsConfig(name="default", language="en", description="English Wikipedia 2023 with redirects + pageviews"),
    ]
    DEFAULT_CONFIG_NAME = "default"

    def _info(self) -> datasets.DatasetInfo:
        features = datasets.Features(
            {
                "id": datasets.Value("string"),
                "title": datasets.Value("string"),
                "url": datasets.Value("string"),
                "text": datasets.Value("string"),
                "redirects": datasets.Sequence(datasets.Value("string")),
                "pageviews_2023": datasets.Value("int32"),
                "timestamp": datasets.Value("string"),
            }
        )
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=features,
            homepage=_HOMEPAGE,
            license=_LICENSE,
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager: datasets.DownloadManager):
        urls = self._get_urls_for_config()
        paths = dl_manager.download_and_extract(urls)
        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                gen_kwargs={
                    "articles_path": paths["articles_xml"],
                    "redirects_path": paths["redirects_tsv"],
                    "pageviews_path": paths["pageviews_tsv"],
                    "language": self.config.language,
                },
            )
        ]

    def _get_urls_for_config(self) -> Dict[str, str]:
        return {
            "articles_xml": "utils/dummy_data/wikipedia_2023_redirects/articles.xml",
            "redirects_tsv": "utils/dummy_data/wikipedia_2023_redirects/redirects.tsv",
            "pageviews_tsv": "utils/dummy_data/wikipedia_2023_redirects/pageviews_2023.tsv",
        }

    def _generate_examples(
        self,
        articles_path: str,
        redirects_path: str,
        pageviews_path: str,
        language: str,
    ) -> Iterator[Tuple[str, Dict]]:
        redirects = self._load_redirects(redirects_path)
        pageviews = self._load_pageviews(pageviews_path)

        for page in self._iter_pages_from_xml(articles_path):
            if page.is_redirect:
                continue
            title = page.title
            aliases = self._aliases_for_title(redirects, title)
            pv = pageviews.get(self._normalize(title), 0)
            url = f"https://{language}.wikipedia.org/wiki/{self._title_to_url(title)}"

            record = {
                "id": page.id,
                "title": title,
                "url": url,
                "text": page.text,
                "redirects": aliases,
                "pageviews_2023": int(pv),
                "timestamp": page.timestamp or "",
            }
            yield page.id, record

    @staticmethod
    def _normalize(title: str) -> str:
        return title.replace(" ", "_")

    @staticmethod
    def _title_to_url(title: str) -> str:
        return Wikipedia2023Redirects._normalize(title)

    @staticmethod
    def _aliases_for_title(redirects: Dict[str, str], canonical_title: str) -> List[str]:
        canon_norm = Wikipedia2023Redirects._normalize(canonical_title)
        return [src for src, dst in redirects.items() if dst == canon_norm]

    @dataclass
    class Page:
        id: str
        title: str
        text: str
        timestamp: Optional[str]
        is_redirect: bool

    def _iter_pages_from_xml(self, xml_path: str) -> Iterator["Wikipedia2023Redirects.Page"]:
        with open(xml_path, "rb") as f:
            xml = f.read()
        root = ET.fromstring(xml)
        for page_el in root.findall("./page"):
            title_el = page_el.find("title")
            id_el = page_el.find("id")
            rev_el = page_el.find("revision")
            redirect_el = page_el.find("redirect")

            title = title_el.text if title_el is not None else ""
            page_id = id_el.text if id_el is not None else ""
            timestamp = None
            text = ""
            if rev_el is not None:
                ts_el = rev_el.find("timestamp")
                timestamp = ts_el.text if ts_el is not None else None
                text_el = rev_el.find("text")
                text = text_el.text if text_el is not None else ""

            title = html.unescape(title or "")
            text = html.unescape(text or "")

            is_redirect = redirect_el is not None
            yield self.Page(
                id=str(page_id),
                title=str(title),
                text=str(text),
                timestamp=str(timestamp) if timestamp else None,
                is_redirect=bool(is_redirect),
            )

    def _load_redirects(self, tsv_path: str) -> Dict[str, str]:
        redir: Dict[str, str] = {}
        with open(tsv_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                src, dst = line.split("\t", 1)
                redir[self._normalize(src)] = self._normalize(dst)
        return redir

    def _load_pageviews(self, tsv_path: str) -> Dict[str, int]:
        views: Dict[str, int] = {}
        with open(tsv_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                title, views_str = line.split("\t", 1)
                try:
                    v = int(views_str)
                except Exception:
                    v = 0
                t = self._normalize(title)
                views[t] = views.get(t, 0) + v
        return views
