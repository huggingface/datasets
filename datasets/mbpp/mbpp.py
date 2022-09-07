import json
from pathlib import Path
import datasets


_DESCRIPTION = """\
The MBPP (Mostly Basic Python Problems) dataset consists of around 1,000 crowd-sourced Python
programming problems, designed to be solvable by entry level programmers, covering programming
fundamentals, standard library functionality, and so on. Each problem consists of a task
description, code solution and 3 automated test cases. The sanitized subset of the data has been 
hand-verified by the authors.
"""

_URLs = {
    "full": "https://raw.githubusercontent.com/google-research/google-research/master/mbpp/mbpp.jsonl",
    "sanitized": "https://raw.githubusercontent.com/google-research/google-research/master/mbpp/sanitized-mbpp.json",
}

_CITATION = """\
@article{austin2021program,
  title={Program Synthesis with Large Language Models},
  author={Austin, Jacob and Odena, Augustus and Nye, Maxwell and Bosma, Maarten and Michalewski, Henryk and Dohan, David and Jiang, Ellen and Cai, Carrie and Terry, Michael and Le, Quoc and others},
  journal={arXiv preprint arXiv:2108.07732},
  year={2021}
}"""

_HOMEPAGE = "https://github.com/google-research/google-research/tree/master/mbpp"

_LICENSE = "CC-BY-4.0"


class MBPP(datasets.GeneratorBasedBuilder):
    """MBPP: Mostly Basic Python Problems Dataset"""

    VERSION = datasets.Version("1.0.2")

    BUILDER_CONFIGS = [
        datasets.BuilderConfig(
            name="full",
            version=datasets.Version("1.0.2"),
            description=_DESCRIPTION,
        ),
        datasets.BuilderConfig(
            name="sanitized",
            version=datasets.Version("1.0.2"),
            description=_DESCRIPTION
        )
    ]

    DEFAULT_CONFIG_NAME = "full"

    def _info(self):
        if self.config.name == "full":
            features = datasets.Features(
                {
                    "task_id": datasets.Value("int32"),
                    "text": datasets.Value("string"),
                    "code": datasets.Value("string"),
                    "test_list": datasets.Sequence(datasets.Value("string")),
                    "test_setup_code": datasets.Value("string"),
                    "challenge_test_list": datasets.Sequence(datasets.Value("string")),
                }
            )
        elif self.config.name == "sanitized":
            features = datasets.Features(
                {
                    "source_file": datasets.Value("string"),
                    "task_id": datasets.Value("int32"),
                    "prompt": datasets.Value("string"),
                    "code": datasets.Value("string"),
                    "test_imports": datasets.Sequence(datasets.Value("string")),
                    "test_list": datasets.Sequence(datasets.Value("string")),
                }
            )
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=features,
            supervised_keys=None,
            homepage=_HOMEPAGE,
            license=_LICENSE,
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        """Returns SplitGenerators."""
        config_urls = _URLs[self.config.name]
        data_dir = dl_manager.download_and_extract(config_urls)
        path = Path(data_dir)
        path.parent
        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                gen_kwargs={
                    "filepath": data_dir,
                    "split": "train"
                },
            ),
            datasets.SplitGenerator(
                name=datasets.Split.TEST,
                gen_kwargs={
                    "filepath": data_dir,
                    "split": "test"
                },
            ),
            datasets.SplitGenerator(
                name=datasets.Split.VALIDATION,
                gen_kwargs={
                    "filepath": data_dir,
                    "split": "validation"
                },
            ),
            datasets.SplitGenerator(
                name=datasets.Split("prompt"),
                gen_kwargs={
                    "filepath": data_dir,
                    "split": "prompt"
                },
            )
        ]

    def _generate_examples(self, filepath, split):
        if self.config.name == "full":
            def _read_lines(fn, start, end):
                data = []
                with open(fn, encoding="utf-8") as f:
                    for line in f:
                        sample = json.loads(line)
                        if start <= sample['task_id'] <= end:
                            data.append(sample)
                        elif sample['task_id'] > end:
                            break
                return data
            if split == 'test':
                data = _read_lines(filepath, 11, 510)
            elif split == 'train':
                data = _read_lines(filepath, 601, 974)
            elif split == 'validation':
                data = _read_lines(filepath, 511, 600)
            elif split == 'prompt':
                data = _read_lines(filepath, 1, 10)
        elif self.config.name == "sanitized":
            with open(filepath, encoding="utf-8") as f: 
                data = json.load(f)
            if split == 'test':
                data = [ sample for sample in data if 11 <= sample['task_id'] <= 510 ]
            elif split == 'train':
                data = [ sample for sample in data if 601 <= sample['task_id'] <= 974 ]
            elif split == 'validation':
                data = [ sample for sample in data if 511 <= sample['task_id'] <= 600 ]
            elif split == 'prompt':
                data = [ sample for sample in data if 1 <= sample['task_id'] <= 10 ]
        id_ = 0
        for sample in data:
            yield id_, sample
            id_ += 1
