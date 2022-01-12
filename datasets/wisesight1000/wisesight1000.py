import datasets


_CITATION = """\
@software{bact_2019_3457447,
  author       = {Suriyawongkul, Arthit and
                  Chuangsuwanich, Ekapol and
                  Chormai, Pattarawat and
                  Polpanumas, Charin},
  title        = {PyThaiNLP/wisesight-sentiment: First release},
  month        = sep,
  year         = 2019,
  publisher    = {Zenodo},
  version      = {v1.0},
  doi          = {10.5281/zenodo.3457447},
  url          = {https://doi.org/10.5281/zenodo.3457447}
}
"""

_LICENSE = "CC0"

_DESCRIPTION = """\
`wisesight1000` contains Thai social media texts randomly drawn from the full `wisesight-sentiment`, tokenized by human annotators.
Out of the labels `neg` (negative), `neu` (neutral), `pos` (positive), `q` (question), 250 samples each. Some texts are removed because
they look like spam.Because these samples are representative of real world content, we believe having these annotaed samples will allow
the community to robustly evaluate tokenization algorithms.
"""


class Wisesight1000Config(datasets.BuilderConfig):
    def __init__(self, **kwargs):
        """BuilderConfig

        Args:
          **kwargs: keyword arguments forwarded to super.
        """
        super(Wisesight1000Config, self).__init__(**kwargs)


class Wisesight1000(datasets.GeneratorBasedBuilder):

    _DOWNLOAD_URL = "https://raw.githubusercontent.com/PyThaiNLP/wisesight-sentiment/master/word-tokenization/wisesight-1000-samples-tokenised.label"
    # character type mapping from https://github.com/rkcosmos/deepcut/blob/master/deepcut/utils.py
    _CHAR_TYPES_DICT = {
        "กขฃคฆงจชซญฎฏฐฑฒณดตถทธนบปพฟภมยรลวศษสฬอ": "c",
        "ฅฉผฟฌหฮ": "n",
        "ะาำิีืึุู": "v",  # า ะ ำ ิ ี ึ ื ั ู ุ
        "เแโใไ": "w",
        "่้๊๋": "t",  # วรรณยุกต์ ่ ้ ๊ ๋
        "์ๆฯ.": "s",  # ์  ๆ ฯ .
        "0123456789๑๒๓๔๕๖๗๘๙": "d",
        '"': "q",
        "‘": "q",
        "’": "q",
        "'": "q",
        " ": "p",
        "abcdefghijklmnopqrstuvwxyz": "s_e",
        "ABCDEFGHIJKLMNOPQRSTUVWXYZ": "b_e",
    }
    _CHAR_TYPE_FLATTEN = {}
    for ks, v in _CHAR_TYPES_DICT.items():
        for k in ks:
            _CHAR_TYPE_FLATTEN[k] = v
    _CHAR_TYPES = ["b_e", "c", "d", "n", "o", "p", "q", "s", "s_e", "t", "v", "w"]

    BUILDER_CONFIGS = [
        Wisesight1000Config(
            name="wisesight1000",
            version=datasets.Version("1.0.0"),
            description="993 word-annotated social media messages sampled from `wisesight-sentiment`",
        ),
    ]

    def _info(self):
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=datasets.Features(
                {
                    "char": datasets.Sequence(datasets.Value("string")),
                    "char_type": datasets.Sequence(datasets.features.ClassLabel(names=self._CHAR_TYPES)),
                    "is_beginning": datasets.Sequence(datasets.features.ClassLabel(names=["neg", "pos"])),
                }
            ),
            supervised_keys=None,
            homepage="https://github.com/PyThaiNLP/wisesight-sentiment",
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
            for _id, line in enumerate(f):
                chars = []
                char_types = []
                is_beginnings = []
                # tokens are pipe separated
                splits = line.split("|")
                for token in splits:
                    for i in range(len(token)):
                        chars.append(token[i])
                        char_types.append(self._CHAR_TYPE_FLATTEN.get(token[i], "o"))
                        is_beginning = 1 if i == 0 else 0
                        is_beginnings.append(is_beginning)
                yield _id, {
                    "char": chars,
                    "char_type": char_types,
                    "is_beginning": is_beginnings,
                }
