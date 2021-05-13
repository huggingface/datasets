import os
from functools import reduce
from pathlib import Path

import datasets


_CITATION = """\
@inproceedings{kosawat2009best,
  title={BEST 2009: Thai word segmentation software contest},
  author={Kosawat, Krit and Boriboon, Monthika and Chootrakool, Patcharika and Chotimongkol, Ananlada and Klaithin, Supon and Kongyoung, Sarawoot and Kriengket, Kanyanut and Phaholphinyo, Sitthaa and Purodakananda, Sumonmas and Thanakulwarapas, Tipraporn and others},
  booktitle={2009 Eighth International Symposium on Natural Language Processing},
  pages={83--88},
  year={2009},
  organization={IEEE}
}
@inproceedings{boriboon2009best,
  title={Best corpus development and analysis},
  author={Boriboon, Monthika and Kriengket, Kanyanut and Chootrakool, Patcharika and Phaholphinyo, Sitthaa and Purodakananda, Sumonmas and Thanakulwarapas, Tipraporn and Kosawat, Krit},
  booktitle={2009 International Conference on Asian Language Processing},
  pages={322--327},
  year={2009},
  organization={IEEE}
}
"""

_LICENSE = "CC-BY-NC-SA 3.0"

_DESCRIPTION = """\
`best2009` is a Thai word-tokenization dataset from encyclopedia, novels, news and articles by
[NECTEC](https://www.nectec.or.th/) (148,995/2,252 lines of train/test). It was created for
[BEST 2010: Word Tokenization Competition](https://thailang.nectec.or.th/archive/indexa290.html?q=node/10).
The test set answers are not provided publicly.
"""


class Best2009Config(datasets.BuilderConfig):
    def __init__(self, **kwargs):
        """BuilderConfig

        Args:
          **kwargs: keyword arguments forwarded to super.
        """
        super(Best2009Config, self).__init__(**kwargs)


class Best2009(datasets.GeneratorBasedBuilder):

    _DOWNLOAD_URL = "https://archive.org/download/best_dataset/data.zip"
    _TRAIN_FOLDER = "train"
    _TEST_FOLDER = "test"

    _USELESS_TAGS = {"<NE>": "", "</NE>": "", "<AB>": "", "</AB>": ""}
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
        Best2009Config(
            name="best2009",
            version=datasets.Version("1.0.0"),
            description=_DESCRIPTION,
        ),
    ]

    def _info(self):
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=datasets.Features(
                {
                    "fname": datasets.Value("string"),
                    "char": datasets.Sequence(datasets.Value("string")),
                    "char_type": datasets.Sequence(datasets.features.ClassLabel(names=self._CHAR_TYPES)),
                    "is_beginning": datasets.Sequence(datasets.features.ClassLabel(names=["neg", "pos"])),
                }
            ),
            supervised_keys=None,
            homepage="https://aiforthai.in.th/",
            citation=_CITATION,
            license=_LICENSE,
        )

    def _split_generators(self, dl_manager):
        arch_path = dl_manager.download_and_extract(self._DOWNLOAD_URL)
        data_dir = os.path.join(arch_path, "data")
        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                gen_kwargs={"filepath": os.path.join(data_dir, self._TRAIN_FOLDER), "split": "train"},
            ),
            datasets.SplitGenerator(
                name=datasets.Split.TEST,
                gen_kwargs={"filepath": os.path.join(data_dir, self._TEST_FOLDER), "split": "train"},
            ),
        ]

    def _generate_examples(self, filepath, split):
        for file_idx, fname in enumerate(sorted(Path(filepath).rglob("*.txt"))):
            with open(fname, encoding="utf-8") as f:
                for line_idx, line in enumerate(f):
                    chars = []
                    char_types = []
                    is_beginnings = []
                    # replace useless tokens
                    line = reduce(lambda a, kv: a.replace(*kv), self._USELESS_TAGS.items(), line)
                    # tokens are pipe separated
                    splits = line.split("|")
                    for token in splits:
                        for i in range(len(token)):
                            chars.append(token[i])
                            char_types.append(self._CHAR_TYPE_FLATTEN.get(token[i], "o"))
                            is_beginning = 1 if i == 0 else 0
                            is_beginnings.append(is_beginning)
                    yield f"{file_idx}_{line_idx}", {
                        "fname": fname.name,
                        "char": chars,
                        "char_type": char_types,
                        "is_beginning": is_beginnings if split == "train" else [0 for i in range(len(chars))],
                    }
