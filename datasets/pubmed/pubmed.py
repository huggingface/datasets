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
"""TODO: Add a description here."""


import copy
import xml.etree.ElementTree as etree

import datasets


logger = datasets.logging.get_logger(__name__)


# Find for instance the citation on arxiv or on the dataset repo/website
_CITATION = """\
"""

# You can copy an official description
_DESCRIPTION = """\
NLM produces a baseline set of MEDLINE/PubMed citation records in XML format for download on an annual basis. The annual baseline is released in December of each year. Each day, NLM produces update files that include new, revised and deleted citations. See our documentation page for more information.
"""

_HOMEPAGE = "https://www.nlm.nih.gov/databases/download/pubmed_medline.html"

_LICENSE = ""

# TODO: Add link to the official dataset URLs here
# The HuggingFace dataset library don't host the datasets but only point to the original files
# This can be an arbitrary nested dict/list of URLs (see below in `_split_generators` method)
_URLs = [f"ftp://ftp.ncbi.nlm.nih.gov/pubmed/baseline/pubmed21n{i:04d}.xml.gz" for i in range(1, 1063)]


# Copyright Ferry Boender, released under the MIT license.
# Modified by @Narsil to handle more oddities
def deepupdate(target, src):
    """Deep update target dict with src
    For each k,v in src: if k doesn't exist in target, it is deep copied from
    src to target. Otherwise, if v is a list, target[k] is extended with
    src[k]. If v is a set, target[k] is updated with v, If v is a dict,
    recursively deep-update it.

    Examples:
    >>> t = {'name': 'Ferry', 'hobbies': ['programming', 'sci-fi']}
    >>> deepupdate(t, {'hobbies': ['gaming']})
    >>> print(t)
    {'name': 'Ferry', 'hobbies': ['programming', 'sci-fi', 'gaming']}
    """
    for k, v in src.items():
        if k in target and isinstance(target[k], int) and isinstance(v, str):
            try:
                v = int(v)
            except Exception:
                pass
        if k in target and type(target[k]) != type(v):
            logger.warning(f"Ignoring field {k} it's a {type(v)} and we expect a {type(target[k])}")
            continue

        if type(v) == list:
            if k not in target:
                target[k] = copy.deepcopy(v)
            elif isinstance(target[k], list):
                target[k].extend(v)
            elif isinstance(target[k], str):
                # Very special case to handle `AbstractText` which sometimes end up
                # being a list.
                new_v = " ".join(el for el in v if isinstance(el, str))
                target[k] = new_v
            else:
                logger.warning(f"Ignoring field {k} it's a {type(v)} and we expect a {type(target[k])}")
        elif type(v) == dict:
            if k not in target:
                target[k] = copy.deepcopy(v)
            elif isinstance(target[k], dict):
                deepupdate(target[k], v)
            else:
                logger.warning(f"Ignoring field {k} it's a {type(v)} and we expect a {type(target[k])}")
        elif type(v) == set:
            if k not in target:
                target[k] = v.copy()
            elif isinstance(target[k], set):
                target[k].update(v.copy())
            else:
                logger.warning(f"Ignoring field {k} it's a {type(v)} and we expect a {type(target[k])}")
        else:
            if isinstance(target[k], (list, tuple, dict)):
                logger.warning(f"Ignoring field {k} it's a {type(v)} and we expect a {type(target[k])}")
                continue

            target[k] = copy.copy(v)


def default_date():
    return {"Year": 0, "Month": 0, "Day": 0}


def default_inline_article():
    return {
        # 'Journal': Journal,
        "Abstract": {"AbstractText": ""},
        "ArticleTitle": "",
        # 'Pagination': {'MedlinePgn': datasets.Value('string')},
        "AuthorList": {"Author": []},
        "Language": "",
        "GrantList": {
            "Grant": [],
        },
        "PublicationTypeList": {"PublicationType": []},
    }


def default_article():
    return {
        "MedlineCitation": {
            "PMID": 0,
            "DateCompleted": default_date(),
            "NumberOfReferences": 0,
            "DateRevised": default_date(),
            "Article": default_inline_article(),
            "MedlineJournalInfo": {"Country": ""},
            "ChemicalList": {"Chemical": []},
            "CitationSubset": "",
            "MeshHeadingList": {"MeshHeading": []},
        },
        "PubmedData": {
            "ArticleIdList": [{"ArticleId": []}],
            "PublicationStatus": "",
            "History": {"PubMedPubDate": []},
            "ReferenceList": [],
        },
    }


class Pubmed(datasets.GeneratorBasedBuilder):
    """Pubmed citations records"""

    BUILDER_CONFIGS = [
        datasets.BuilderConfig(name="2021", description="The 2021 annual record", version=datasets.Version("1.0.0")),
    ]

    # FILLED automatically from features
    SIMPLE_KEYS = {"PubmedArticleSet"}
    LIST_KEYS = {"PubmedArticle"}
    IGNORE_KEYS = set()

    def fill_keys_from_features(self, features):
        if isinstance(features, dict):
            for key, value in features.items():
                if isinstance(value, datasets.Sequence):
                    self.LIST_KEYS.add(key)
                    self.fill_keys_from_features(value.feature)
                else:
                    self.SIMPLE_KEYS.add(key)
                    self.fill_keys_from_features(value)

    def xml_to_dictionnary(self, parentElement):
        data = {}
        if parentElement.tag in {"AbstractText", "ArticleTitle"}:
            # XXX
            # Very special case, it will contain html leading to having very odd structure
            tag = parentElement.tag
            string = etree.tostring(parentElement).decode("utf-8").strip()
            inner_string = string[len(f"<{tag}>") : -len(f"</{tag}>")]
            return {parentElement.tag: inner_string}

        for child in list(parentElement):
            child.text = child.text if (child.text is not None) else " "
            key = child.tag
            if len(child) == 0:
                value = child.text.strip()
            else:
                value = self.xml_to_dictionnary(child)
                if isinstance(value, dict) and set(value.keys()) == {key}:
                    value = value[key]

            if key in data:
                old_value = data[key]
                if isinstance(old_value, dict):
                    data[key] = [old_value, value]
                elif isinstance(old_value, list):
                    data[key].append(value)
            elif key in self.LIST_KEYS:
                data[key] = [value]
            elif key in self.SIMPLE_KEYS:
                data[key] = value
            elif key in self.IGNORE_KEYS:
                continue
            else:
                logger.info(f"Ignoring key {key} from {parentElement.tag}")
                self.IGNORE_KEYS.add(key)

        # Filling defaults
        if parentElement.tag == "MeshHeading" and "QualifierName" not in data:
            data["QualifierName"] = ""
        elif parentElement.tag == "Author":
            if "ForeName" not in data:
                data["ForeName"] = ""
            if "Initials" not in data:
                data["Initials"] = ""
            if "LastName" not in data:
                data["LastName"] = ""
            if "CollectiveName" not in data:
                data["CollectiveName"] = ""
        elif parentElement.tag == "JournalIssue":
            if "Volume" not in data:
                data["Volume"] = ""
            if "Issue" not in data:
                data["Issue"] = ""
        elif parentElement.tag == "Grant" and "GrantID" not in data:
            data["GrantID"] = ""

        return {parentElement.tag: data}

    def _info(self):
        Date = {
            "Year": datasets.Value("int32"),
            "Month": datasets.Value("int32"),
            "Day": datasets.Value("int32"),
        }

        MeshHeading = {"DescriptorName": datasets.Value("string"), "QualifierName": datasets.Value("string")}

        MedlineJournalInfo = {
            "Country": datasets.Value("string"),
            # Too inconsistent
            # 'MedlineTA': datasets.Value('string'),
            # 'NlmUniqueID': datasets.Value('string'),
            # 'ISSNLinking': datasets.Value('string'),
        }
        Chemical = {
            "RegistryNumber": datasets.Value("string"),
            "NameOfSubstance": datasets.Value("string"),
        }
        # Too inconsistent in the data to be used
        # Journal = {
        #         'ISSN': datasets.Value('string'),
        #         'JournalIssue': {
        #             'Volume': datasets.Value('string'),
        #             'Issue': datasets.Value('string'),
        #         },
        #         # 'PubDate': Date,
        #         'Title': datasets.Value('string'),
        #         'ISOAbbreviation': datasets.Value('string')
        #         }
        Author = {
            "LastName": datasets.Value("string"),
            "ForeName": datasets.Value("string"),
            "Initials": datasets.Value("string"),
            "CollectiveName": datasets.Value("string"),
        }
        Reference = {
            "Citation": datasets.Value("string"),
            "CitationId": datasets.Value("int32"),
        }
        Grant = {
            "GrantID": datasets.Value("string"),
            "Agency": datasets.Value("string"),
            "Country": datasets.Value("string"),
        }
        Article = {
            # 'Journal': Journal,
            "Abstract": {"AbstractText": datasets.Value("string")},
            "ArticleTitle": datasets.Value("string"),
            # Too inconistent
            # 'Pagination': {'MedlinePgn': datasets.Value('string')},
            "AuthorList": {"Author": datasets.Sequence(Author)},
            "Language": datasets.Value("string"),
            "GrantList": {
                "Grant": datasets.Sequence(Grant),
            },
            "PublicationTypeList": {"PublicationType": datasets.Sequence(datasets.Value("string"))},
        }
        features = datasets.Features(
            {
                "MedlineCitation": {
                    "PMID": datasets.Value("int32"),
                    "DateCompleted": Date,
                    "NumberOfReferences": datasets.Value("int32"),
                    "DateRevised": Date,
                    "Article": Article,
                    "MedlineJournalInfo": MedlineJournalInfo,
                    "ChemicalList": {"Chemical": datasets.Sequence(Chemical)},
                    "CitationSubset": datasets.Value("string"),
                    "MeshHeadingList": {
                        "MeshHeading": datasets.Sequence(MeshHeading),
                    },
                },
                "PubmedData": {
                    "ArticleIdList": datasets.Sequence({"ArticleId": datasets.Sequence(datasets.Value("string"))}),
                    "PublicationStatus": datasets.Value("string"),
                    "History": {"PubMedPubDate": datasets.Sequence(Date)},
                    "ReferenceList": datasets.Sequence(Reference),
                },
            }
        )
        self.fill_keys_from_features(features)
        return datasets.DatasetInfo(
            # This is the description that will appear on the datasets page.
            description=_DESCRIPTION,
            # This defines the different columns of the dataset and their types
            features=features,  # Here we define them above because they are different between the two configurations
            # If there's a common (input, target) tuple from the features,
            # specify them here. They'll be used if as_supervised=True in
            # builder.as_dataset.
            supervised_keys=None,
            # Homepage of the dataset for documentation
            homepage=_HOMEPAGE,
            # License for the dataset if available
            license=_LICENSE,
            # Citation for the dataset
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        """Returns SplitGenerators."""
        dl_dir = dl_manager.download_and_extract(_URLs)
        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={"filenames": dl_dir},
            ),
        ]

    def update_citation(self, article):
        """
        ArticleId and ArticleIdList are already used field name so we rewrite and
        flatten those as {Citation, CitationId}.
        """
        citations = []
        try:
            list_ = article["PubmedData"]["ReferenceList"]
        except Exception:
            return

        for ref in list_:
            if "Reference" not in ref:
                continue
            for re in ref["Reference"]:
                if "Citation" not in re:
                    continue
                citation = re["Citation"]
                if "ArticleIdList" not in re:
                    continue
                for r in re["ArticleIdList"]:
                    if "ArticleId" not in r:
                        continue
                    for rr in r["ArticleId"]:
                        try:
                            citation = {"Citation": citation, "CitationId": int(rr)}
                        except Exception:
                            continue
                        citations.append(citation)
        article["PubmedData"]["ReferenceList"] = citations

    def _generate_examples(self, filenames):
        """Yields examples."""
        id_ = 0
        for filename in filenames:
            try:
                tree = etree.parse(filename)
                root = tree.getroot()
                xmldict = self.xml_to_dictionnary(root)
            except etree.ParseError:
                logger.warning(f"Ignoring file {filename}, it is malformed")
                continue

            for article in xmldict["PubmedArticleSet"]["PubmedArticle"]:
                self.update_citation(article)
                new_article = default_article()

                try:
                    deepupdate(new_article, article)
                except Exception:
                    logger.warning(f"Ignoring article {article}, it is malformed")
                    continue

                try:
                    _ = self.info.features.encode_example(new_article)
                except Exception as e:
                    logger.warning(f"Ignore example because {e}")
                    continue
                yield id_, new_article
                id_ += 1
