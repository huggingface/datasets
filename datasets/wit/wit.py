import gzip
import json

import datasets
from datasets import Features, Sequence, Value


_CITATION = """@article{srinivasan2021wit,
  title={WIT: Wikipedia-based Image Text Dataset for Multimodal Multilingual Machine Learning},
  author={Srinivasan, Krishna and Raman, Karthik and Chen, Jiecao and Bendersky, Michael and Najork, Marc},
  journal={arXiv preprint arXiv:2103.01913},
  year={2021}
}
"""
_DESCRIPTION = """Wikipedia-based Image Text (WIT) Dataset is a large multimodal multilingual dataset. WIT is composed of a curated set
 of 37.6 million entity rich image-text examples with 11.5 million unique images across 108 Wikipedia languages. Its
 size enables WIT to be used as a pretraining dataset for multimodal machine learning models.
"""
_HOMEPAGE = "https://github.com/google-research-datasets/wit"
_URL = "https://storage.googleapis.com/huggingface-nlp/datasets/wit/"
_URLS = {"train": [_URL + f"part-{'%05d' % i}-48a6f07e-bb86-4735-aac7-883349f41a28-c000.json.gz" for i in range(400)]}


class Wit(datasets.GeneratorBasedBuilder):
    """WIT: Wikipedia-based Image Text Dataset for Multimodal Multilingual Machine Learning"""

    def _info(self):
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=Features(
                {
                    "b64_bytes": Value("string"),
                    "embedding": Sequence(Value("float64")),
                    "image_url": Value("string"),
                    "metadata_url": Value("string"),
                    "original_height": Value("int32"),
                    "original_width": Value("int32"),
                    "mime_type": Value("string"),
                    "caption_attribution_description": Value("string"),
                    "wit_features": Sequence(
                        {
                            "language": Value("string"),
                            "page_url": Value("string"),
                            "attribution_passes_lang_id": Value("string"),
                            "caption_alt_text_description": Value("string"),
                            "caption_reference_description": Value("string"),
                            "caption_title_and_reference_description": Value("string"),
                            "context_page_description": Value("string"),
                            "context_section_description": Value("string"),
                            "hierarchical_section_title": Value("string"),
                            "is_main_image": Value("string"),
                            "page_changed_recently": Value("string"),
                            "page_title": Value("string"),
                            "section_title": Value("string"),
                        }
                    ),
                }
            ),
            homepage=_HOMEPAGE,
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        """Returns SplitGenerators."""
        urls_to_download = _URLS
        downloaded_files = dl_manager.download_and_extract(urls_to_download)
        return [
            datasets.SplitGenerator(name=datasets.Split.TRAIN, gen_kwargs={"filepaths": downloaded_files["train"]}),
        ]

    def _generate_examples(self, filepaths):
        """Yields examples."""
        wit_feature_names = self.info.features["wit_features"].feature.keys()
        example_id = 0
        for filepath in filepaths:
            with gzip.open(filepath, mode="rt", encoding="utf-8") as f:
                for i, line in enumerate(f):
                    line = line.strip()
                    row_data = json.loads(line, encoding="utf-8")
                    for feature in row_data["wit_features"]:
                        # If a feature is missing from feature dict, add it as None
                        for fname in wit_feature_names:
                            if fname not in feature:
                                feature[fname] = None
                        # Here we take redundant values from wit_features and add them to row_data to avoid unnecessary duplication
                        extra_wit_feature_keys = [k for k in feature.keys() if k not in wit_feature_names]
                        for k in extra_wit_feature_keys:
                            data = feature.pop(k)
                            if isinstance(data, list):
                                data = data[0]
                            row_data[k] = data
                    # Check row_data now for missing keys, adding None for most, but -1 for int features to avoid failures.
                    missing_keys = [x for x in self.info.features.keys() if x not in row_data]
                    for missing_key in missing_keys:
                        row_data[missing_key] = (
                            None if missing_key not in ["original_height", "original_width"] else -1
                        )
                    example_id += 1
                    yield str(example_id), row_data
