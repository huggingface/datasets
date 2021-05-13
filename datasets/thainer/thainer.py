import datasets


_CITATION = """\
@misc{Wannaphong Phatthiyaphaibun_2019,
    title={wannaphongcom/thai-ner: ThaiNER 1.3},
    url={https://zenodo.org/record/3550546},
    DOI={10.5281/ZENODO.3550546},
    abstractNote={Thai Named Entity Recognition},
    publisher={Zenodo},
    author={Wannaphong Phatthiyaphaibun},
    year={2019},
    month={Nov}
}
"""

_LICENSE = "CC-BY 3.0"

_DESCRIPTION = """\
ThaiNER (v1.3) is a 6,456-sentence named entity recognition dataset created from expanding the 2,258-sentence
[unnamed dataset](http://pioneer.chula.ac.th/~awirote/Data-Nutcha.zip) by
[Tirasaroj and Aroonmanakun (2012)](http://pioneer.chula.ac.th/~awirote/publications/).
It is used to train NER taggers in [PyThaiNLP](https://github.com/PyThaiNLP/pythainlp).
The NER tags are annotated by [Tirasaroj and Aroonmanakun (2012)]((http://pioneer.chula.ac.th/~awirote/publications/))
for 2,258 sentences and the rest by [@wannaphong](https://github.com/wannaphong/).
The POS tags are done by [PyThaiNLP](https://github.com/PyThaiNLP/pythainlp)'s `perceptron` engine trained on `orchid_ud`.
[@wannaphong](https://github.com/wannaphong/) is now the only maintainer of this dataset.
"""


class ThaiNerConfig(datasets.BuilderConfig):
    """BuilderConfig for ThaiNer."""

    def __init__(self, **kwargs):
        """BuilderConfig for ThaiNer.

        Args:
          **kwargs: keyword arguments forwarded to super.
        """
        super(ThaiNerConfig, self).__init__(**kwargs)


class Thainer(datasets.GeneratorBasedBuilder):

    _DOWNLOAD_URL = "https://github.com/wannaphong/thai-ner/raw/master/model/1.3/data-pos.conll"
    _SENTENCE_SPLITTERS = ["", " ", "\n"]
    _POS_TAGS = [
        "ADJ",
        "ADP",
        "ADV",
        "AUX",
        "CCONJ",
        "DET",
        "NOUN",
        "NUM",
        "PART",
        "PRON",
        "PROPN",
        "PUNCT",
        "SCONJ",
        "VERB",
    ]
    _NER_TAGS = [
        "B-DATE",
        "B-EMAIL",
        "B-LAW",
        "B-LEN",
        "B-LOCATION",
        "B-MONEY",
        "B-ORGANIZATION",
        "B-PERCENT",
        "B-PERSON",
        "B-PHONE",
        "B-TIME",
        "B-URL",
        "B-ZIP",
        "B-ไม่ยืนยัน",
        "I-DATE",
        "I-EMAIL",
        "I-LAW",
        "I-LEN",
        "I-LOCATION",
        "I-MONEY",
        "I-ORGANIZATION",
        "I-PERCENT",
        "I-PERSON",
        "I-PHONE",
        "I-TIME",
        "I-URL",
        "I-ไม่ยืนยัน",
        "O",
    ]

    BUILDER_CONFIGS = [
        ThaiNerConfig(
            name="thainer",
            version=datasets.Version("1.3.0"),
            description="Thai Named Entity Recognition for PyThaiNLP (6,456 sentences)",
        ),
    ]

    def _info(self):
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=datasets.Features(
                {
                    "id": datasets.Value("int32"),
                    "tokens": datasets.Sequence(datasets.Value("string")),
                    "pos_tags": datasets.Sequence(datasets.features.ClassLabel(names=self._POS_TAGS)),
                    "ner_tags": datasets.Sequence(datasets.features.ClassLabel(names=self._NER_TAGS)),
                }
            ),
            supervised_keys=None,
            homepage="https://github.com/wannaphong/thai-ner/",
            citation=_CITATION,
            license=_LICENSE,
        )

    def _split_generators(self, dl_manager):
        data_path = dl_manager.download_and_extract(self._DOWNLOAD_URL)
        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                gen_kwargs={"filepath": data_path},
            ),
        ]

    def _generate_examples(self, filepath):
        with open(filepath, encoding="utf-8") as f:
            guid = 0
            tokens = []
            pos_tags = []
            ner_tags = []

            for line in f:
                if line in self._SENTENCE_SPLITTERS:
                    if tokens:
                        yield guid, {
                            "id": str(guid),
                            "tokens": tokens,
                            "pos_tags": pos_tags,
                            "ner_tags": ner_tags,
                        }
                        guid += 1
                        tokens = []
                        pos_tags = []
                        ner_tags = []
                else:
                    # thainer tokens are tab separated
                    splits = line.split("\t")
                    # replace junk ner tags
                    ner_tag = splits[2].strip() if splits[2].strip() in self._NER_TAGS else "O"
                    tokens.append(splits[0])
                    pos_tags.append(splits[1])
                    ner_tags.append(ner_tag)
            # last example
            if tokens:
                yield guid, {
                    "id": str(guid),
                    "tokens": tokens,
                    "pos_tags": pos_tags,
                    "ner_tags": ner_tags,
                }
