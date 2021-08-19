"""XL-Sum abstractive summarization dataset."""


import json
import os

import datasets


_CITATION = """\
@inproceedings{hasan-etal-2021-xl,
    title = "{XL}-Sum: Large-Scale Multilingual Abstractive Summarization for 44 Languages",
    author = "Hasan, Tahmid  and
      Bhattacharjee, Abhik  and
      Islam, Md. Saiful  and
      Mubasshir, Kazi  and
      Li, Yuan-Fang  and
      Kang, Yong-Bin  and
      Rahman, M. Sohel  and
      Shahriyar, Rifat",
    booktitle = "Findings of the Association for Computational Linguistics: ACL-IJCNLP 2021",
    month = aug,
    year = "2021",
    address = "Online",
    publisher = "Association for Computational Linguistics",
    url = "https://aclanthology.org/2021.findings-acl.413",
    pages = "4693--4703",
}
"""


_DESCRIPTION = """\
We present XLSum, a comprehensive and diverse dataset comprising 1.35 million professionally
annotated article-summary pairs from BBC, extracted using a set of carefully designed heuristics.
The dataset covers 45 languages ranging from low to high-resource, for many of which no
public dataset is currently available. XL-Sum is highly abstractive, concise,
and of high quality, as indicated by human and intrinsic evaluation.
"""

_HOMEPAGE = "https://github.com/csebuetnlp/xl-sum"

_LICENSE = "Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License (CC BY-NC-SA 4.0)"

_URLS = {
    "amharic": "https://drive.google.com/u/0/uc?id=1RVRaSdwjuILTYFez-Nl73UMv2aubHzD6&export=download",
    "arabic": "https://drive.google.com/u/0/uc?id=1lot6kJ6TPCHuBI6Ky_RQPdYpWaQCk-jl&export=download",
    "azerbaijani": "https://drive.google.com/u/0/uc?id=1DXMWzrWPwA3_bA3MA8s173tcYl-7viq9&export=download",
    "bengali": "https://drive.google.com/u/0/uc?id=1h3GY8Pk1xV3DWo3Ewc9ZJQ4bU7tCS_1R&export=download",
    "burmese": "https://drive.google.com/u/0/uc?id=1PqmC8MAUVi9KSenxmlcfFuH0i3VjEk9L&export=download",
    "chinese_simplified": "https://drive.google.com/u/0/uc?id=18lXt8-QTuowGfaRH8UcAilt-Uehpyhsv&export=download",
    "chinese_traditional": "https://drive.google.com/u/0/uc?id=1j6ln7dwmUwWOiN2SCfIoLA5B-L8ZaiJj&export=download",
    "english": "https://drive.google.com/u/0/uc?id=1KlTW4WTHzDdmigZnqBLdRTCkamISortQ&export=download",
    "french": "https://drive.google.com/u/0/uc?id=1YtC1tzCrwHrAcPCU1VOefChl7-IEYTWF&export=download",
    "gujarati": "https://drive.google.com/u/0/uc?id=1IJdTIR_Im2Saa_F2tW5UNnU2g_dWp1wG&export=download",
    "hausa": "https://drive.google.com/u/0/uc?id=1lMkb_gYpwzd32_-waG_eNaWeehm0OpGZ&export=download",
    "hindi": "https://drive.google.com/u/0/uc?id=1H3PxMwEFyzNxGXpM0KMPOkt4UcdHbiky&export=download",
    "igbo": "https://drive.google.com/u/0/uc?id=1B5td0FABADD3xAEIWO_-ZwBuoV5kW85h&export=download",
    "indonesian": "https://drive.google.com/u/0/uc?id=1FV5o-ZV3mGqGpBQYx_IAEXknmdWpMyNR&export=download",
    "japanese": "https://drive.google.com/u/0/uc?id=1Y5Wk4wI1lrhmy-qRoAF8Ygm0wIu9mHkG&export=download",
    "kirundi": "https://drive.google.com/u/0/uc?id=1DbPJGYoGAfclcvgWTgf0YP48u6gBdS-t&export=download",
    "korean": "https://drive.google.com/u/0/uc?id=1F_f8LonURmklzHH24B_DgFHWsiFps7x0&export=download",
    "kyrgyz": "https://drive.google.com/u/0/uc?id=19YTnLF_m8gCElwMcNhY1VGhznbq8ur5d&export=download",
    "marathi": "https://drive.google.com/u/0/uc?id=1WJNQ5PqqM4FPq7VSWezx1-OFOlZ9dUiU&export=download",
    "nepali": "https://drive.google.com/u/0/uc?id=1o_T_Chy-p-Sn2AnSlvaf97nEyV1A3Tfz&export=download",
    "oromo": "https://drive.google.com/u/0/uc?id=1ZCfG5L8A77P4BvOVm3O7BXQFliGyQCqY&export=download",
    "pashto": "https://drive.google.com/u/0/uc?id=1_zQzLVQgEb7fg4A-NU17C0OBi-W0DQLT&export=download",
    "persian": "https://drive.google.com/u/0/uc?id=1bymTi8KKSB3qZKB1qejEGyOE8LCdEvhn&export=download",
    "pidgin": "https://drive.google.com/u/0/uc?id=17n8UpuZSbWisvkPB7eklM3VARN3iNO6y&export=download",
    "portuguese": "https://drive.google.com/u/0/uc?id=1mwUJtxgDjm-ZerXWusdMc19qYtsgepBT&export=download",
    "punjabi": "https://drive.google.com/u/0/uc?id=1w6yuGHeZOQ-nhZQRd_a7oIpItNY553tL&export=download",
    "russian": "https://drive.google.com/u/0/uc?id=1bGzbX_zYvuCHeT__7LBlG6hkAQ-dfThY&export=download",
    "scottish_gaelic": "https://drive.google.com/u/0/uc?id=1lOHjY8IcnGbrPjia5dD2sT84DYLIytT_&export=download",
    "serbian_cyrillic": "https://drive.google.com/u/0/uc?id=1c_vaD4ydnTcn0pqYMbbVjt7EPIgwfUv9&export=download",
    "serbian_latin": "https://drive.google.com/u/0/uc?id=1JlDU401_3XqbmpaaJnvv7S1aIBd-GoqG&export=download",
    "sinhala": "https://drive.google.com/u/0/uc?id=1HBSvf7T5qh8ox6C7lO1DqKTBVda0vUAo&export=download",
    "somali": "https://drive.google.com/u/0/uc?id=1f9_4DjgTxmfhquJqnSe2x170FILsAiYi&export=download",
    "spanish": "https://drive.google.com/u/0/uc?id=1DDhUTm0cijq4Tx9isaG5AFT9viexBroO&export=download",
    "swahili": "https://drive.google.com/u/0/uc?id=1WitOEsFdJdirZYZr92H0v0HGFpwi2vbh&export=download",
    "tamil": "https://drive.google.com/u/0/uc?id=1ukjkPZktUBvckWliCSotUZYXBalZ3t7h&export=download",
    "telugu": "https://drive.google.com/u/0/uc?id=1cTbqTwYPu5U09U1mBVIN3b71W4B17gOl&export=download",
    "thai": "https://drive.google.com/u/0/uc?id=1bg2pFl2YSWH90J1ll7ZMFHOnaXJ0tejF&export=download",
    "tigrinya": "https://drive.google.com/u/0/uc?id=13Ob4gkiswGPEjj4iTphZD_irpFAcK0P-&export=download",
    "turkish": "https://drive.google.com/u/0/uc?id=1AcnfIw-MnoNq-kpON74RW5DuJBu9MBh8&export=download",
    "ukrainian": "https://drive.google.com/u/0/uc?id=1t5cnjvu3rEhz_LDTPvjTD5EQp5fveeOQ&export=download",
    "urdu": "https://drive.google.com/u/0/uc?id=1Vie5jfHyHBkkW6jLbFNU5qjStcHstOKn&export=download",
    "uzbek": "https://drive.google.com/u/0/uc?id=1FK-TSViqsfBKX8bAGCUD1IlrSirlVwuS&export=download",
    "vietnamese": "https://drive.google.com/u/0/uc?id=1ufC9hPtC-gYNTI9TCXrVudhIXGOFs-al&export=download",
    "welsh": "https://drive.google.com/u/0/uc?id=1mMF9I-KxO83ktJ98aVSRC30bnMTthVV6&export=download",
    "yoruba": "https://drive.google.com/u/0/uc?id=1oHxPjk7PQ0JSkbf906wZYyK4pGdEulLL&export=download",
}


_LANGUAGES = _URLS.keys()


class Xlsum(datasets.GeneratorBasedBuilder):
    VERSION = datasets.Version("2.0.0")

    BUILDER_CONFIGS = [
        datasets.BuilderConfig(name="{}".format(lang), version=datasets.Version("2.0.0")) for lang in _LANGUAGES
    ]

    def _info(self):
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=datasets.Features(
                {
                    "id": datasets.Value("string"),
                    "url": datasets.Value("string"),
                    "title": datasets.Value("string"),
                    "summary": datasets.Value("string"),
                    "text": datasets.Value("string"),
                }
            ),
            supervised_keys=None,
            homepage=_HOMEPAGE,
            citation=_CITATION,
            license=_LICENSE,
            version=self.VERSION,
        )

    def _split_generators(self, dl_manager):
        """Returns SplitGenerators."""
        lang = str(self.config.name)
        url = _URLS[lang]

        data_dir = dl_manager.download_and_extract(url)
        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                gen_kwargs={
                    "filepath": os.path.join(data_dir, lang + "_train.jsonl"),
                },
            ),
            datasets.SplitGenerator(
                name=datasets.Split.TEST,
                gen_kwargs={
                    "filepath": os.path.join(data_dir, lang + "_test.jsonl"),
                },
            ),
            datasets.SplitGenerator(
                name=datasets.Split.VALIDATION,
                gen_kwargs={
                    "filepath": os.path.join(data_dir, lang + "_val.jsonl"),
                },
            ),
        ]

    def _generate_examples(self, filepath):
        """Yields examples as (key, example) tuples."""
        with open(filepath, encoding="utf-8") as f:
            for idx_, row in enumerate(f):
                data = json.loads(row)
                yield idx_, {
                    "id": data["id"],
                    "url": data["url"],
                    "title": data["title"],
                    "summary": data["summary"],
                    "text": data["text"],
                }
