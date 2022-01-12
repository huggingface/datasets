import glob
import os
from pathlib import Path

import datasets


_CITATION = """\
@article{boonkwan2020annotation,
  title={The Annotation Guideline of LST20 Corpus},
  author={Boonkwan, Prachya and Luantangsrisuk, Vorapon and Phaholphinyo, Sitthaa and Kriengket, Kanyanat and Leenoi, Dhanon and Phrombut, Charun and Boriboon, Monthika and Kosawat, Krit and Supnithi, Thepchai},
  journal={arXiv preprint arXiv:2008.05055},
  year={2020}
}
"""

_DESCRIPTION = """\
LST20 Corpus is a dataset for Thai language processing developed by National Electronics and Computer Technology Center (NECTEC), Thailand.
It offers five layers of linguistic annotation: word boundaries, POS tagging, named entities, clause boundaries, and sentence boundaries.
At a large scale, it consists of 3,164,002 words, 288,020 named entities, 248,181 clauses, and 74,180 sentences, while it is annotated with
16 distinct POS tags. All 3,745 documents are also annotated with one of 15 news genres. Regarding its sheer size, this dataset is
considered large enough for developing joint neural models for NLP.
Manually download at https://aiforthai.in.th/corpus.php
"""


class Lst20Config(datasets.BuilderConfig):
    """BuilderConfig for Lst20"""

    def __init__(self, **kwargs):
        """BuilderConfig for Lst20.

        Args:
          **kwargs: keyword arguments forwarded to super.
        """
        super(Lst20Config, self).__init__(**kwargs)


class Lst20(datasets.GeneratorBasedBuilder):
    """Lst20 dataset."""

    _SENTENCE_SPLITTERS = ["", " ", "\n"]
    _TRAINING_FOLDER = "train"
    _VALID_FOLDER = "eval"
    _TEST_FOLDER = "test"
    _POS_TAGS = ["NN", "VV", "PU", "CC", "PS", "AX", "AV", "FX", "NU", "AJ", "CL", "PR", "NG", "PA", "XX", "IJ"]
    _NER_TAGS = [
        "O",
        "B_BRN",
        "B_DES",
        "B_DTM",
        "B_LOC",
        "B_MEA",
        "B_NUM",
        "B_ORG",
        "B_PER",
        "B_TRM",
        "B_TTL",
        "I_BRN",
        "I_DES",
        "I_DTM",
        "I_LOC",
        "I_MEA",
        "I_NUM",
        "I_ORG",
        "I_PER",
        "I_TRM",
        "I_TTL",
        "E_BRN",
        "E_DES",
        "E_DTM",
        "E_LOC",
        "E_MEA",
        "E_NUM",
        "E_ORG",
        "E_PER",
        "E_TRM",
        "E_TTL",
    ]
    _CLAUSE_TAGS = ["O", "B_CLS", "I_CLS", "E_CLS"]

    BUILDER_CONFIGS = [
        Lst20Config(name="lst20", version=datasets.Version("1.0.0"), description="LST20 dataset"),
    ]

    @property
    def manual_download_instructions(self):
        return """\
  You need to
  1. Manually download `AIFORTHAI-LST20Corpus.tar.gz` from https://aiforthai.in.th/corpus.php (login required; website mostly in Thai)
  2. Extract the .tar.gz; this will result in folder `LST20Corpus`
  The <path/to/folder> can e.g. be `~/Downloads/LST20Corpus`.
  lst20 can then be loaded using the following command `datasets.load_dataset("lst20", data_dir="<path/to/folder>")`.
  """

    def _info(self):
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=datasets.Features(
                {
                    "id": datasets.Value("string"),
                    "fname": datasets.Value("string"),
                    "tokens": datasets.Sequence(datasets.Value("string")),
                    "pos_tags": datasets.Sequence(datasets.features.ClassLabel(names=self._POS_TAGS)),
                    "ner_tags": datasets.Sequence(datasets.features.ClassLabel(names=self._NER_TAGS)),
                    "clause_tags": datasets.Sequence(datasets.features.ClassLabel(names=self._CLAUSE_TAGS)),
                }
            ),
            supervised_keys=None,
            homepage="https://aiforthai.in.th/",
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        """Returns SplitGenerators."""

        data_dir = os.path.abspath(os.path.expanduser(dl_manager.manual_dir))

        # check if manual folder exists
        if not os.path.exists(data_dir):
            raise FileNotFoundError(
                f"{data_dir} does not exist. Make sure you insert a manual dir via `datasetts.load_dataset('lst20', data_dir=...)`. Manual download instructions: {self.manual_download_instructions})"
            )

        # check number of .txt files
        nb_train = len(glob.glob(os.path.join(data_dir, "train", "*.txt")))
        nb_valid = len(glob.glob(os.path.join(data_dir, "eval", "*.txt")))
        nb_test = len(glob.glob(os.path.join(data_dir, "test", "*.txt")))
        assert (
            nb_train > 0
        ), f"No files found in train/*.txt.\nManual download instructions:{self.manual_download_instructions})"
        assert (
            nb_valid > 0
        ), f"No files found in eval/*.txt.\nManual download instructions:{self.manual_download_instructions})"
        assert (
            nb_test > 0
        ), f"No files found in test/*.txt.\nManual download instructions:{self.manual_download_instructions})"

        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                gen_kwargs={"filepath": os.path.join(data_dir, self._TRAINING_FOLDER)},
            ),
            datasets.SplitGenerator(
                name=datasets.Split.VALIDATION,
                gen_kwargs={"filepath": os.path.join(data_dir, self._VALID_FOLDER)},
            ),
            datasets.SplitGenerator(
                name=datasets.Split.TEST,
                gen_kwargs={"filepath": os.path.join(data_dir, self._TEST_FOLDER)},
            ),
        ]

    def _generate_examples(self, filepath):
        for file_idx, fname in enumerate(sorted(glob.glob(os.path.join(filepath, "*.txt")))):
            with open(fname, encoding="utf-8") as f:
                guid = 0
                tokens = []
                pos_tags = []
                ner_tags = []
                clause_tags = []

                for line in f:
                    if line in self._SENTENCE_SPLITTERS:
                        if tokens:
                            yield f"{file_idx}_{guid}", {
                                "id": str(guid),
                                "fname": Path(fname).name,
                                "tokens": tokens,
                                "pos_tags": pos_tags,
                                "ner_tags": ner_tags,
                                "clause_tags": clause_tags,
                            }
                            guid += 1
                            tokens = []
                            pos_tags = []
                            ner_tags = []
                            clause_tags = []
                    else:
                        # LST20 tokens are tab separated
                        splits = line.split("\t")
                        # replace junk ner tags
                        ner_tag = splits[2] if splits[2] in self._NER_TAGS else "O"
                        tokens.append(splits[0])
                        pos_tags.append(splits[1])
                        ner_tags.append(ner_tag)
                        clause_tags.append(splits[3].rstrip())
                # last example
                if tokens:
                    yield f"{file_idx}_{guid}", {
                        "id": str(guid),
                        "fname": Path(fname).name,
                        "tokens": tokens,
                        "pos_tags": pos_tags,
                        "ner_tags": ner_tags,
                        "clause_tags": clause_tags,
                    }
