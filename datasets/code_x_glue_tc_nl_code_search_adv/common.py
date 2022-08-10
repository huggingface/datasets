from typing import List

import datasets


# Citation, taken from https://github.com/microsoft/CodeXGLUE
_DEFAULT_CITATION = """@article{CodeXGLUE,
         title={CodeXGLUE: A Benchmark Dataset and Open Challenge for Code Intelligence},
         year={2020},}"""


class Child:
    _DESCRIPTION = None
    _FEATURES = None
    _CITATION = None
    SPLITS = {"train": datasets.Split.TRAIN}
    _SUPERVISED_KEYS = None

    def __init__(self, info):
        self.info = info

    def homepage(self):
        return self.info["project_url"]

    def _info(self):
        # This is the description that will appear on the datasets page.
        return datasets.DatasetInfo(
            description=self.info["description"] + "\n\n" + self._DESCRIPTION,
            features=datasets.Features(self._FEATURES),
            homepage=self.homepage(),
            citation=self._CITATION or _DEFAULT_CITATION,
            supervised_keys=self._SUPERVISED_KEYS,
        )

    def _split_generators(self, dl_manager: datasets.DownloadManager) -> List[datasets.SplitGenerator]:
        SPLITS = self.SPLITS
        _URL = self.info["raw_url"]
        urls_to_download = {}
        for split in SPLITS:
            if split not in urls_to_download:
                urls_to_download[split] = {}

            for key, url in self.generate_urls(split):
                if not url.startswith("http"):
                    url = _URL + "/" + url
                urls_to_download[split][key] = url

        downloaded_files = {}
        for k, v in urls_to_download.items():
            downloaded_files[k] = dl_manager.download_and_extract(v)

        return [
            datasets.SplitGenerator(
                name=SPLITS[k],
                gen_kwargs={"split_name": k, "file_paths": downloaded_files[k]},
            )
            for k in SPLITS
        ]

    def check_empty(self, entries):
        all_empty = all([v == "" for v in entries.values()])
        all_non_empty = all([v != "" for v in entries.values()])

        if not all_non_empty and not all_empty:
            raise RuntimeError("Parallel data files should have the same number of lines.")

        return all_empty


class TrainValidTestChild(Child):
    SPLITS = {
        "train": datasets.Split.TRAIN,
        "valid": datasets.Split.VALIDATION,
        "test": datasets.Split.TEST,
    }
