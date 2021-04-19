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
"""UniMorph: Universal Morphologies."""


import datasets


_CITATION = """\
@article{sylak2016composition,
  title={The composition and use of the universal morphological feature schema (unimorph schema)},
  author={Sylak-Glassman, John},
  journal={Johns Hopkins University},
  year={2016}
}
"""

_DESCRIPTION = """\
The Universal Morphology (UniMorph) project is a collaborative effort to improve how NLP handles complex morphology in the world’s languages.
The goal of UniMorph is to annotate morphological data in a universal schema that allows an inflected word from any language to be defined by its lexical meaning,
typically carried by the lemma, and by a rendering of its inflectional form in terms of a bundle of morphological features from our schema.
The specification of the schema is described in Sylak-Glassman (2016).
"""

_HOMEPAGE = "https://unimorph.github.io/"

_LICENSE = "CC-BY-SA-3.0"

_URLs = {
    "ady": "https://raw.githubusercontent.com/unimorph/ady/master/ady",
    "sqi": "https://raw.githubusercontent.com/unimorph/sqi/master/sqi",
    "grc": "https://raw.githubusercontent.com/unimorph/grc/master/grc",
    "ara": "https://raw.githubusercontent.com/unimorph/ara/master/ara",
    "hye": "https://raw.githubusercontent.com/unimorph/hye/master/hye",
    "ast": "https://raw.githubusercontent.com/unimorph/ast/master/ast",
    "aze": "https://raw.githubusercontent.com/unimorph/aze/master/aze",
    "bak": "https://raw.githubusercontent.com/unimorph/bak/master/bak",
    "eus": "https://raw.githubusercontent.com/unimorph/eus/master/eus",
    "bel": "https://raw.githubusercontent.com/unimorph/bel/master/bel",
    "ben": "https://raw.githubusercontent.com/unimorph/ben/master/ben",
    "bre": "https://raw.githubusercontent.com/unimorph/bre/master/bre",
    "bul": "https://raw.githubusercontent.com/unimorph/bul/master/bul",
    "cat": "https://raw.githubusercontent.com/unimorph/cat/master/cat",
    "ckb": "https://raw.githubusercontent.com/unimorph/ckb/master/ckb",
    "syc": "https://raw.githubusercontent.com/unimorph/syc/master/syc",
    "cor": "https://raw.githubusercontent.com/unimorph/cor/master/cor",
    "crh": "https://raw.githubusercontent.com/unimorph/crh/master/crh",
    "ces": "https://raw.githubusercontent.com/unimorph/ces/master/ces",
    "dan": "https://raw.githubusercontent.com/unimorph/dan/master/dan",
    "nld": "https://raw.githubusercontent.com/unimorph/nld/master/nld",
    "eng": "https://raw.githubusercontent.com/unimorph/eng/master/eng",
    "est": "https://raw.githubusercontent.com/unimorph/est/master/est",
    "fao": "https://raw.githubusercontent.com/unimorph/fao/master/fao",
    "fin|1": "https://raw.githubusercontent.com/unimorph/fin/master/fin.1",
    "fin|2": "https://raw.githubusercontent.com/unimorph/fin/master/fin.2",
    "fur": "https://raw.githubusercontent.com/unimorph/fur/master/fur",
    "gal": "https://raw.githubusercontent.com/unimorph/gal/master/gal",
    "ell": "https://raw.githubusercontent.com/unimorph/ell/master/ell",
    "kal": "https://raw.githubusercontent.com/unimorph/kal/master/kal",
    "izh": "https://raw.githubusercontent.com/unimorph/izh/master/izh",
    "kbd": "https://raw.githubusercontent.com/unimorph/kbd/master/kbd",
    "kan": "https://raw.githubusercontent.com/unimorph/kan/master/kan",
    "krl": "https://raw.githubusercontent.com/unimorph/krl/master/krl",
    "csb": "https://raw.githubusercontent.com/unimorph/csb/master/csb",
    "kaz": "https://raw.githubusercontent.com/unimorph/kaz/master/kaz",
    "kjh": "https://raw.githubusercontent.com/unimorph/kjh/master/kjh",
    "lld": "https://raw.githubusercontent.com/unimorph/lld/master/lld",
    "liv": "https://raw.githubusercontent.com/unimorph/liv/master/liv",
    "mlt": "https://raw.githubusercontent.com/unimorph/mlt/master/mlt",
    "glv": "https://raw.githubusercontent.com/unimorph/glv/master/glv",
    "arn": "https://raw.githubusercontent.com/unimorph/arn/master/arn",
    "frm": "https://raw.githubusercontent.com/unimorph/frm/master/frm",
    "gmh": "https://raw.githubusercontent.com/unimorph/gmh/master/gmh",
    "gml": "https://raw.githubusercontent.com/unimorph/gml/master/gml",
    "mwf": "https://raw.githubusercontent.com/unimorph/mwf/master/mwf",
    "nap": "https://raw.githubusercontent.com/unimorph/nap/master/nap",
    "xno": "https://raw.githubusercontent.com/unimorph/xno/master/xno",
    "frr": "https://raw.githubusercontent.com/unimorph/frr/master/frr",
    "oci": "https://raw.githubusercontent.com/unimorph/oci/master/oci",
    "xcl": "https://raw.githubusercontent.com/unimorph/xcl/master/xcl",
    "chu": "https://raw.githubusercontent.com/unimorph/chu/master/chu",
    "ang": "https://raw.githubusercontent.com/unimorph/ang/master/ang",
    "fro": "https://raw.githubusercontent.com/unimorph/fro/master/fro",
    "sga": "https://raw.githubusercontent.com/unimorph/sga/master/sga",
    "osx": "https://raw.githubusercontent.com/unimorph/osx/master/osx",
    "pus": "https://raw.githubusercontent.com/unimorph/pus/master/pus",
    "san": "https://raw.githubusercontent.com/unimorph/san/master/san",
    "hbs": "https://raw.githubusercontent.com/unimorph/hbs/master/hbs",
    "swc": "https://raw.githubusercontent.com/unimorph/swc/master/swc",
    "tgk": "https://raw.githubusercontent.com/unimorph/tgk/master/tgk",
    "tat": "https://raw.githubusercontent.com/unimorph/tat/master/tat",
    "tel": "https://raw.githubusercontent.com/unimorph/tel/master/tel",
    "bod": "https://raw.githubusercontent.com/unimorph/bod/master/bod",
    "tuk": "https://raw.githubusercontent.com/unimorph/tuk/master/tuk",
    "uzb": "https://raw.githubusercontent.com/unimorph/uzb/master/uzb",
    "vec": "https://raw.githubusercontent.com/unimorph/vec/master/vec",
    "vot": "https://raw.githubusercontent.com/unimorph/vot/master/vot",
    "fry": "https://raw.githubusercontent.com/unimorph/fry/master/fry",
    "zul": "https://raw.githubusercontent.com/unimorph/zul/master/zul",
    "fra": "https://raw.githubusercontent.com/unimorph/fra/master/fra",
    "kat": "https://raw.githubusercontent.com/unimorph/kat/master/kat",
    "deu": "https://raw.githubusercontent.com/unimorph/deu/master/deu",
    "hai": "https://raw.githubusercontent.com/unimorph/hai/master/hai",
    "heb": "https://raw.githubusercontent.com/unimorph/heb/master/heb",
    "hin": "https://raw.githubusercontent.com/unimorph/hin/master/hin",
    "hun": "https://raw.githubusercontent.com/unimorph/hun/master/hun",
    "isl": "https://raw.githubusercontent.com/unimorph/isl/master/isl",
    "gle": "https://raw.githubusercontent.com/unimorph/gle/master/gle",
    "ita": "https://raw.githubusercontent.com/unimorph/ita/master/ita",
    "klr": "https://raw.githubusercontent.com/unimorph/klr/master/klr",
    "lat": "https://raw.githubusercontent.com/unimorph/lat/master/lat",
    "lav": "https://raw.githubusercontent.com/unimorph/lav/master/lav",
    "lit": "https://raw.githubusercontent.com/unimorph/lit/master/lit",
    "dsb": "https://raw.githubusercontent.com/unimorph/dsb/master/dsb",
    "mkd": "https://raw.githubusercontent.com/unimorph/mkd/master/mkd",
    "nav": "https://raw.githubusercontent.com/unimorph/nav/master/nav",
    "kmr": "https://raw.githubusercontent.com/unimorph/kmr/master/kmr",
    "sme": "https://raw.githubusercontent.com/unimorph/sme/master/sme",
    "nob": "https://raw.githubusercontent.com/unimorph/nob/master/nob",
    "nno": "https://raw.githubusercontent.com/unimorph/nno/master/nno",
    "fas": "https://raw.githubusercontent.com/unimorph/fas/master/fas",
    "pol": "https://raw.githubusercontent.com/unimorph/pol/master/pol",
    "por": "https://raw.githubusercontent.com/unimorph/por/master/por",
    "que": "https://raw.githubusercontent.com/unimorph/que/master/que",
    "ron": "https://raw.githubusercontent.com/unimorph/ron/master/ron",
    "rus": "https://raw.githubusercontent.com/unimorph/rus/master/rus",
    "gla": "https://raw.githubusercontent.com/unimorph/gla/master/gla",
    "slv": "https://raw.githubusercontent.com/unimorph/slv/master/slv",
    "spa": "https://raw.githubusercontent.com/unimorph/spa/master/spa",
    "swe": "https://raw.githubusercontent.com/unimorph/swe/master/swe",
    "tur": "https://raw.githubusercontent.com/unimorph/tur/master/tur",
    "ukr": "https://raw.githubusercontent.com/unimorph/ukr/master/ukr",
    "urd": "https://raw.githubusercontent.com/unimorph/urd/master/urd",
    "cym": "https://raw.githubusercontent.com/unimorph/cym/master/cym",
    "yid": "https://raw.githubusercontent.com/unimorph/yid/master/yid",
    "lud|mikhailovskoye": "https://raw.githubusercontent.com/unimorph/lud/master/lud-mikhailovskoye-dialect.txt",
    "lud|new_written": "https://raw.githubusercontent.com/unimorph/lud/master/lud-new-written-ludian-dialect.txt",
    "lud|southern_ludian_svjatozero": "https://raw.githubusercontent.com/unimorph/lud/master/lud-southern-ludian-svjatozero-dialect.txt",
    "olo|kotkozero": "https://raw.githubusercontent.com/unimorph/olo/master/olo-kotkozero-dialect.txt",
    "olo|new_written": "https://raw.githubusercontent.com/unimorph/olo/master/olo-new-written-livvic-dialect.txt",
    "olo|syamozero": "https://raw.githubusercontent.com/unimorph/olo/master/olo-syamozero-dialect.txt",
    "olo|vedlozero": "https://raw.githubusercontent.com/unimorph/olo/master/olo-vedlozero-dialect.txt",
    "olo|vidlitsa": "https://raw.githubusercontent.com/unimorph/olo/master/olo-vidlitsa-dialect.txt",
    "vep|central_eastern": "https://raw.githubusercontent.com/unimorph/vep/master/vep-central-eastern-veps.txt",
    "vep|central_western": "https://raw.githubusercontent.com/unimorph/vep/master/vep-central-western-veps.txt",
    "vep|new_written": "https://raw.githubusercontent.com/unimorph/vep/master/vep-new-written-veps.txt",
    "vep|northern": "https://raw.githubusercontent.com/unimorph/vep/master/vep-northern-veps.txt",
    "vep|southern": "https://raw.githubusercontent.com/unimorph/vep/master/vep-southern-veps.txt",
}

_LANGUAGES = sorted(set([ln.split("|")[0] for ln in _URLs]))

# make multiple splits for the languages with several dialects
_SPLITS = {}
for ln in _URLs:
    if "|" in ln:
        ln_conf, ln_split = ln.split("|")
        _SPLITS[ln_conf] = _SPLITS.get(ln_conf, []) + [ln_split]

_CATEGORIES = {
    "Aktionsart": ["STAT", "DYN", "TEL", "ATEL", "PCT", "DUR", "ACH", "ACCMP", "SEMEL", "ACTY"],
    "Animacy": ["ANIM", "INAN", "HUM", "NHUM"],
    "Argument_Marking": [
        "ARGNO1S",
        "ARGNO2S",
        "ARGNO3S",
        "ARGNO1P",
        "ARGNO2P",
        "ARGNO3P",
        "ARGAC1S",
        "ARGAC2S",
        "ARGAC3S",
        "ARGAC1P",
        "ARGAC2P",
        "ARGAC3P",
        "ARGAB1S",
        "ARGAB2S",
        "ARGAB3S",
        "ARGAB1P",
        "ARGAB2P",
        "ARGAB3P",
        "ARGER1S",
        "ARGER2S",
        "ARGER3S",
        "ARGER1P",
        "ARGER2P",
        "ARGER3P",
        "ARGDA1S",
        "ARGDA2S",
        "ARGDA3S",
        "ARGDA1P",
        "ARGDA2P",
        "ARGDA3P",
        "ARGBE1S",
        "ARGBE2S",
        "ARGBE3S",
        "ARGBE1P",
        "ARGBE2P",
        "ARGBE3P",
    ],
    "Aspect": ["IPFV", "PFV", "PRF", "PROG", "PROSP", "ITER", "HAB"],
    "Case": [
        "NOM",
        "ACC",
        "ERG",
        "ABS",
        "NOMS",
        "DAT",
        "BEN",
        "PRP",
        "GEN",
        "REL",
        "PRT",
        "INS",
        "COM",
        "VOC",
        "COMPV",
        "EQTV",
        "PRIV",
        "PROPR",
        "AVR",
        "FRML",
        "TRANS",
        "BYWAY",
        "INTER",
        "AT",
        "POST",
        "IN",
        "CIRC",
        "ANTE",
        "APUD",
        "ON",
        "ONHR",
        "ONVR",
        "SUB",
        "REM",
        "PROXM",
        "ESS",
        "ALL",
        "ABL",
        "APPRX",
        "TERM",
    ],
    "Comparison": ["CMPR", "SPRL", "AB", "RL", "EQT"],
    "Definiteness": ["DEF", "INDF", "SPEC", "NSPEC"],
    "Deixis": ["PROX", "MED", "REMT", "REF1", "REF2", "NOREF", "PHOR", "VIS", "NVIS", "ABV", "EVEN", "BEL"],
    "Evidentiality": ["FH", "DRCT", "SEN", "VISU", "NVSEN", "AUD", "NFH", "QUOT", "RPRT", "HRSY", "INFER", "ASSUM"],
    "Finiteness": ["FIN", "NFIN"],
    "Gender": [
        "MASC",
        "FEM",
        "NEUT",
        "NAKH1",
        "NAKH2",
        "NAKH3",
        "NAKH4",
        "NAKH5",
        "NAKH6",
        "NAKH7",
        "NAKH8",
        "BANTU1",
        "BANTU2",
        "BANTU3",
        "BANTU4",
        "BANTU5",
        "BANTU6",
        "BANTU7",
        "BANTU8",
        "BANTU9",
        "BANTU10",
        "BANTU11",
        "BANTU12",
        "BANTU13",
        "BANTU14",
        "BANTU15",
        "BANTU16",
        "BANTU17",
        "BANTU18",
        "BANTU19",
        "BANTU20",
        "BANTU21",
        "BANTU22",
        "BANTU23",
    ],
    "Information_Structure": ["TOP", "FOC"],
    "Interrogativity": ["DECL", "INT"],
    "Language_Specific": [
        "LGSPEC1",
        "LGSPEC2",
        "LGSPEC3",
        "LGSPEC4",
        "LGSPEC5",
        "LGSPEC6",
        "LGSPEC7",
        "LGSPEC8",
        "LGSPEC9",
        "LGSPEC10",
    ],
    "Mood": [
        "IND",
        "SBJV",
        "REAL",
        "IRR",
        "AUPRP",
        "AUNPRP",
        "IMP",
        "COND",
        "PURP",
        "INTEN",
        "POT",
        "LKLY",
        "ADM",
        "OBLIG",
        "DEB",
        "PERM",
        "DED",
        "SIM",
        "OPT",
    ],
    "Number": ["SG", "PL", "GRPL", "DU", "TRI", "PAUC", "GRPAUC", "INVN"],
    "Part_Of_Speech": [
        "N",
        "PROPN",
        "ADJ",
        "PRO",
        "CLF",
        "ART",
        "DET",
        "V",
        "ADV",
        "AUX",
        "V.PTCP",
        "V.MSDR",
        "V.CVB",
        "ADP",
        "COMP",
        "CONJ",
        "NUM",
        "PART",
        "INTJ",
    ],
    "Person": ["0", "1", "2", "3", "4", "INCL", "EXCL", "PRX", "OBV"],
    "Polarity": ["POS", "NEG"],
    "Politeness": [
        "INFM",
        "FORM",
        "ELEV",
        "HUMB",
        "POL",
        "AVOID",
        "LOW",
        "HIGH",
        "STELEV",
        "STSUPR",
        "LIT",
        "FOREG",
        "COL",
    ],
    "Possession": [
        "ALN",
        "NALN",
        "PSS1S",
        "PSS2S",
        "PSS2SF",
        "PSS2SM",
        "PSS2SINFM",
        "PSS2SFORM",
        "PSS3S",
        "PSS3SF",
        "PSS3SM",
        "PSS1D",
        "PSS1DI",
        "PSS1DE",
        "PSS2D",
        "PSS2DM",
        "PSS2DF",
        "PSS3D",
        "PSS3DF",
        "PSS3DM",
        "PSS1P",
        "PSS1PI",
        "PSS1PE",
        "PSS2P",
        "PSS2PF",
        "PSS2PM",
        "PSS3PF",
        "PSS3PM",
    ],
    "Switch_Reference": ["SS", "SSADV", "DS", "DSADV", "OR", "SIMMA", "SEQMA", "LOG"],
    "Tense": ["PRS", "PST", "FUT", "IMMED", "HOD", "1DAY", "RCT", "RMT"],
    "Valency": ["IMPRS", "INTR", "TR", "DITR", "REFL", "RECP", "CAUS", "APPL"],
    "Voice": ["ACT", "MID", "PASS", "ANTIP", "DIR", "INV", "AGFOC", "PFOC", "LFOC", "BFOC", "ACFOC", "IFOC", "CFOC"],
}

_TAG_TO_CAT = dict([(tag, cat) for cat, tags in _CATEGORIES.items() for tag in tags])


class UniversalMorphologies(datasets.GeneratorBasedBuilder):
    """UniMorph: Universal Morphologies."""

    BUILDER_CONFIGS = [
        datasets.BuilderConfig(
            name=f"{language_iso}",
            version=datasets.Version("1.0.0"),
            description=f"Universal Morphologies for {language_iso}",
        )
        for language_iso in _LANGUAGES
    ]

    DEFAULT_CONFIG_NAME = "ady"  # It's not mandatory to have a default configuration. Just use one if it make sense.

    def _info(self):
        features = datasets.Features(
            {
                "lemma": datasets.Value("string"),
                "forms": datasets.Sequence(
                    dict(
                        [("word", datasets.Value("string"))]
                        + [
                            (cat, datasets.Sequence(datasets.ClassLabel(names=tasks)))
                            for cat, tasks in _CATEGORIES.items()
                        ]
                        + [("Other", datasets.Sequence(datasets.Value("string")))]  # for misspecified tags
                    )
                ),
            }
        )
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=features,  # Here we define them above because they are different between the two configurations
            supervised_keys=None,
            homepage=_HOMEPAGE,
            license=_LICENSE,
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        """Returns SplitGenerators."""
        config_urls = dict([(ln, f_url) for ln, f_url in _URLs.items() if ln.split("|")[0] == self.config.name])
        data_dir = dl_manager.download_and_extract(config_urls)
        if self.config.name in _SPLITS:
            return [
                datasets.SplitGenerator(
                    name=spl,
                    gen_kwargs={
                        "filepath": data_dir[f"{self.config.name}|{spl}"],
                    },
                )
                for spl in _SPLITS[self.config.name]
            ]
        else:
            return [
                datasets.SplitGenerator(
                    name=datasets.Split.TRAIN,
                    gen_kwargs={
                        "filepath": data_dir[self.config.name],
                    },
                )
            ]

    def _generate_examples(self, filepath):
        all_forms = {}
        # we need to do a full path first to gather all forms of a lemma
        with open(filepath, encoding="utf-8") as f:
            forms = []
            for row in f:
                if row.strip() == "" or row.strip().startswith("#"):
                    continue
                lemma, word, tags = row.strip().split("\t")
                all_forms[lemma] = all_forms.get(lemma, [])
                tag_list = tags.replace("NDEF", "INDF").split(";")
                form = dict([("word", word), ("Other", [])] + [(cat, []) for cat, tasks in _CATEGORIES.items()])
                for tag_pre in tag_list:
                    tag = tag_pre.split("+")
                    if tag[0] in _TAG_TO_CAT:
                        form[_TAG_TO_CAT[tag[0]]] = tag
                    else:
                        form["Other"] += tag
                all_forms[lemma] += [form]
        for id_, (lemma, forms) in enumerate(all_forms.items()):
            res = {"lemma": lemma, "forms": {}}
            for k in ["word", "Other"] + list(_CATEGORIES.keys()):
                res["forms"][k] = [form[k] for form in forms]
            yield id_, res
