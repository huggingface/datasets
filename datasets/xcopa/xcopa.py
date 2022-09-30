"""TODO(xcopa): Add a description here."""


import json

import datasets


_HOMEPAGE = "https://github.com/cambridgeltl/xcopa"

_CITATION = """\
  @article{ponti2020xcopa,
  title={{XCOPA: A} Multilingual Dataset for Causal Commonsense Reasoning},
  author={Edoardo M. Ponti, Goran Glava\v{s}, Olga Majewska, Qianchu Liu, Ivan Vuli\'{c} and Anna Korhonen},
  journal={arXiv preprint},
  year={2020},
  url={https://ducdauge.github.io/files/xcopa.pdf}
}

@inproceedings{roemmele2011choice,
  title={Choice of plausible alternatives: An evaluation of commonsense causal reasoning},
  author={Roemmele, Melissa and Bejan, Cosmin Adrian and Gordon, Andrew S},
  booktitle={2011 AAAI Spring Symposium Series},
  year={2011},
  url={https://people.ict.usc.edu/~gordon/publications/AAAI-SPRING11A.PDF},
}
"""

_DESCRIPTION = """\
  XCOPA: A Multilingual Dataset for Causal Commonsense Reasoning
The Cross-lingual Choice of Plausible Alternatives dataset is a benchmark to evaluate the ability of machine learning models to transfer commonsense reasoning across
languages. The dataset is the translation and reannotation of the English COPA (Roemmele et al. 2011) and covers 11 languages from 11 families and several areas around
the globe. The dataset is challenging as it requires both the command of world knowledge and the ability to generalise to new languages. All the details about the
creation of XCOPA and the implementation of the baselines are available in the paper.\n
"""

_LANG = ["et", "ht", "it", "id", "qu", "sw", "zh", "ta", "th", "tr", "vi"]
_URL = "https://raw.githubusercontent.com/cambridgeltl/xcopa/master/{subdir}/{language}/{split}.{language}.jsonl"
_VERSION = datasets.Version("1.1.0", "Minor fixes to the 'question' values in Italian")


class Xcopa(datasets.GeneratorBasedBuilder):
    BUILDER_CONFIGS = [
        datasets.BuilderConfig(
            name=lang,
            description=f"Xcopa language {lang}",
            version=_VERSION,
        )
        for lang in _LANG
    ]
    BUILDER_CONFIGS += [
        datasets.BuilderConfig(
            name=f"translation-{lang}",
            description=f"Xcopa English translation for language {lang}",
            version=_VERSION,
        )
        for lang in _LANG
        if lang != "qu"
    ]

    def _info(self):
        return datasets.DatasetInfo(
            description=_DESCRIPTION + self.config.description,
            features=datasets.Features(
                {
                    "premise": datasets.Value("string"),
                    "choice1": datasets.Value("string"),
                    "choice2": datasets.Value("string"),
                    "question": datasets.Value("string"),
                    "label": datasets.Value("int32"),
                    "idx": datasets.Value("int32"),
                    "changed": datasets.Value("bool"),
                }
            ),
            homepage=_HOMEPAGE,
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        """Returns SplitGenerators."""
        *translation_prefix, language = self.config.name.split("-")
        data_subdir = "data" if not translation_prefix else "data-gmt"
        splits = {datasets.Split.VALIDATION: "val", datasets.Split.TEST: "test"}
        data_urls = {
            split: _URL.format(subdir=data_subdir, language=language, split=splits[split]) for split in splits
        }
        dl_paths = dl_manager.download(data_urls)
        return [
            datasets.SplitGenerator(
                name=split,
                gen_kwargs={"filepath": dl_paths[split]},
            )
            for split in splits
        ]

    def _generate_examples(self, filepath):
        """Yields examples."""
        with open(filepath, encoding="utf-8") as f:
            for row in f:
                data = json.loads(row)
                idx = data["idx"]
                yield idx, data
