import json
import logging
import os

import numpy as np
from PIL import Image
from transformers import AutoTokenizer

import datasets


_CITATION = """
@article{Xu2020LayoutXLMMP,
  title         = {LayoutXLM: Multimodal Pre-training for Multilingual Visually-rich Document Understanding},
  author        = {Yiheng Xu and Tengchao Lv and Lei Cui and Guoxin Wang and Yijuan Lu and Dinei Florencio and Cha Zhang and Furu Wei},
  year          = {2021},
  eprint        = {2104.08836},
  archivePrefix = {arXiv},
  primaryClass  = {cs.CL}
}
"""

_DESCRIPTION = """
XFUND is a multilingual form understanding benchmark dataset that includes human-labeled forms with key-value pairs in 7 languages (Chinese, Japanese, Spanish, French, Italian, German, Portuguese).
"""

_VERSION = datasets.Version("1.0.0")

_URL = "https://github.com/doc-analysis/XFUN/releases/download/v1.0/"
_LANG = ["zh", "de", "es", "fr", "it", "ja", "pt"]

logger = logging.getLogger(__name__)


def normalize_bbox(bbox, size):
    return [
        int(1000 * bbox[0] / size[0]),
        int(1000 * bbox[1] / size[1]),
        int(1000 * bbox[2] / size[0]),
        int(1000 * bbox[3] / size[1]),
    ]


def simplify_bbox(bbox):
    return [
        min(bbox[0::2]),
        min(bbox[1::2]),
        max(bbox[2::2]),
        max(bbox[3::2]),
    ]


def merge_bbox(bbox_list):
    x0, y0, x1, y1 = list(zip(*bbox_list))
    return [min(x0), min(y0), max(x1), max(y1)]


def load_image(image_path):
    with Image.open(image_path) as image:
        w, h = image.size
        image = image.resize((224, 224), resample=Image.BILINEAR)
        image_arr = np.asarray(image.copy())  # copy to make it writeable
        image_arr = image_arr[:, :, ::-1]  # BGR -> RGB
        image_arr = np.transpose(image_arr, axes=(2, 0, 1))
    return image_arr, (w, h)


class XFUNConfig(datasets.BuilderConfig):
    """BuilderConfig for XFUN."""

    def __init__(self, lang, additional_langs=None, **kwargs):
        """
        Args:
            lang: string, language for the input text
            **kwargs: keyword arguments forwarded to super.
        """
        super(XFUNConfig, self).__init__(**kwargs)
        self.lang = lang
        self.additional_langs = additional_langs


class XFUN(datasets.GeneratorBasedBuilder):
    """XFUN dataset."""

    BUILDER_CONFIGS = [XFUNConfig(name=f"xfun.{lang}", lang=lang, version=_VERSION) for lang in _LANG]

    tokenizer = AutoTokenizer.from_pretrained("xlm-roberta-base")

    def _info(self):
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            citation=_CITATION,
            features=datasets.Features(
                {
                    "id": datasets.Value("string"),
                    "input_ids": datasets.Sequence(datasets.Value("int64")),
                    "bbox": datasets.Sequence(datasets.Sequence(datasets.Value("int64"))),
                    "labels": datasets.Sequence(
                        datasets.ClassLabel(
                            names=["O", "B-QUESTION", "B-ANSWER", "B-HEADER", "I-ANSWER", "I-QUESTION", "I-HEADER"]
                        )
                    ),
                    "image": datasets.Array3D(shape=(3, 224, 224), dtype="uint8"),
                    "entities": datasets.Sequence(
                        {
                            "start": datasets.Value("int64"),
                            "end": datasets.Value("int64"),
                            "label": datasets.ClassLabel(names=["HEADER", "QUESTION", "ANSWER"]),
                        }
                    ),
                    "relations": datasets.Sequence(
                        {
                            "head": datasets.Value("int64"),
                            "tail": datasets.Value("int64"),
                            "start_index": datasets.Value("int64"),
                            "end_index": datasets.Value("int64"),
                        }
                    ),
                }
            ),
            version=_VERSION,
            supervised_keys=None,
        )

    def _split_generators(self, dl_manager):
        """Returns SplitGenerators."""
        urls_to_download = {
            "train": [f"{_URL}{self.config.lang}.train.json", f"{_URL}{self.config.lang}.train.zip"],
            "val": [f"{_URL}{self.config.lang}.val.json", f"{_URL}{self.config.lang}.val.zip"],
            # "test": [f"{_URL}{self.config.lang}.test.json", f"{_URL}{self.config.lang}.test.zip"],
        }
        downloaded_files = dl_manager.download_and_extract(urls_to_download)
        train_files_for_many_langs = [downloaded_files["train"]]
        val_files_for_many_langs = [downloaded_files["val"]]
        # test_files_for_many_langs = [downloaded_files["test"]]
        if self.config.additional_langs:
            additional_langs = self.config.additional_langs.split("+")
            if "all" in additional_langs:
                additional_langs = [lang for lang in _LANG if lang != self.config.lang]
            for lang in additional_langs:
                urls_to_download = {"train": [f"{_URL}{lang}.train.json", f"{_URL}{lang}.train.zip"]}
                additional_downloaded_files = dl_manager.download_and_extract(urls_to_download)
                train_files_for_many_langs.append(additional_downloaded_files["train"])

        logger.info(f"Training on {self.config.lang} with additional langs({self.config.additional_langs})")
        logger.info(f"Evaluating on {self.config.lang}")
        logger.info(f"Testing on {self.config.lang}")
        return [
            datasets.SplitGenerator(name=datasets.Split.TRAIN, gen_kwargs={"filepaths": train_files_for_many_langs}),
            datasets.SplitGenerator(
                name=datasets.Split.VALIDATION, gen_kwargs={"filepaths": val_files_for_many_langs}
            ),
            # datasets.SplitGenerator(name=datasets.Split.TEST, gen_kwargs={"filepaths": test_files_for_many_langs}),
        ]

    def _generate_examples(self, filepaths):
        for filepath in filepaths:
            logger.info("Generating examples from = %s", filepath)
            with open(filepath[0], "r", encoding="utf-8") as f:
                data = json.load(f)

            for doc in data["documents"]:
                doc["img"]["fpath"] = os.path.join(filepath[1], doc["img"]["fname"])
                image, size = load_image(doc["img"]["fpath"])
                document = doc["document"]
                tokenized_doc = {"input_ids": [], "bbox": [], "labels": []}
                entities = []
                relations = []
                id2label = {}
                entity_id_to_index_map = {}
                empty_entity = set()
                for line in document:
                    if len(line["text"]) == 0:
                        empty_entity.add(line["id"])
                        continue
                    id2label[line["id"]] = line["label"]
                    relations.extend([tuple(sorted(l)) for l in line["linking"]])
                    tokenized_inputs = self.tokenizer(
                        line["text"],
                        add_special_tokens=False,
                        return_offsets_mapping=True,
                        return_attention_mask=False,
                    )
                    text_length = 0
                    ocr_length = 0
                    bbox = []
                    last_box = None
                    for token_id, offset in zip(tokenized_inputs["input_ids"], tokenized_inputs["offset_mapping"]):
                        if token_id == 6:
                            bbox.append(None)
                            continue
                        text_length += offset[1] - offset[0]
                        tmp_box = []
                        while ocr_length < text_length:
                            ocr_word = line["words"].pop(0)
                            ocr_length += len(
                                self.tokenizer._tokenizer.normalizer.normalize_str(ocr_word["text"].strip())
                            )
                            tmp_box.append(simplify_bbox(ocr_word["box"]))
                        if len(tmp_box) == 0:
                            tmp_box = last_box
                        bbox.append(normalize_bbox(merge_bbox(tmp_box), size))
                        last_box = tmp_box
                    bbox = [
                        [bbox[i + 1][0], bbox[i + 1][1], bbox[i + 1][0], bbox[i + 1][1]] if b is None else b
                        for i, b in enumerate(bbox)
                    ]
                    if line["label"] == "other":
                        label = ["O"] * len(bbox)
                    else:
                        label = [f"I-{line['label'].upper()}"] * len(bbox)
                        label[0] = f"B-{line['label'].upper()}"
                    tokenized_inputs.update({"bbox": bbox, "labels": label})
                    if label[0] != "O":
                        entity_id_to_index_map[line["id"]] = len(entities)
                        entities.append(
                            {
                                "start": len(tokenized_doc["input_ids"]),
                                "end": len(tokenized_doc["input_ids"]) + len(tokenized_inputs["input_ids"]),
                                "label": line["label"].upper(),
                            }
                        )
                    for i in tokenized_doc:
                        tokenized_doc[i] = tokenized_doc[i] + tokenized_inputs[i]
                relations = list(set(relations))
                relations = [rel for rel in relations if rel[0] not in empty_entity and rel[1] not in empty_entity]
                kvrelations = []
                for rel in relations:
                    pair = [id2label[rel[0]], id2label[rel[1]]]
                    if pair == ["question", "answer"]:
                        kvrelations.append(
                            {"head": entity_id_to_index_map[rel[0]], "tail": entity_id_to_index_map[rel[1]]}
                        )
                    elif pair == ["answer", "question"]:
                        kvrelations.append(
                            {"head": entity_id_to_index_map[rel[1]], "tail": entity_id_to_index_map[rel[0]]}
                        )
                    else:
                        continue

                def get_relation_span(rel):
                    bound = []
                    for entity_index in [rel["head"], rel["tail"]]:
                        bound.append(entities[entity_index]["start"])
                        bound.append(entities[entity_index]["end"])
                    return min(bound), max(bound)

                relations = sorted(
                    [
                        {
                            "head": rel["head"],
                            "tail": rel["tail"],
                            "start_index": get_relation_span(rel)[0],
                            "end_index": get_relation_span(rel)[1],
                        }
                        for rel in kvrelations
                    ],
                    key=lambda x: x["head"],
                )
                chunk_size = 512
                for chunk_id, index in enumerate(range(0, len(tokenized_doc["input_ids"]), chunk_size)):
                    item = {}
                    for k in tokenized_doc:
                        item[k] = tokenized_doc[k][index : index + chunk_size]
                    entities_in_this_span = []
                    global_to_local_map = {}
                    for entity_id, entity in enumerate(entities):
                        if (
                            index <= entity["start"] < index + chunk_size
                            and index <= entity["end"] < index + chunk_size
                        ):
                            entity["start"] = entity["start"] - index
                            entity["end"] = entity["end"] - index
                            global_to_local_map[entity_id] = len(entities_in_this_span)
                            entities_in_this_span.append(entity)
                    relations_in_this_span = []
                    for relation in relations:
                        if (
                            index <= relation["start_index"] < index + chunk_size
                            and index <= relation["end_index"] < index + chunk_size
                        ):
                            relations_in_this_span.append(
                                {
                                    "head": global_to_local_map[relation["head"]],
                                    "tail": global_to_local_map[relation["tail"]],
                                    "start_index": relation["start_index"] - index,
                                    "end_index": relation["end_index"] - index,
                                }
                            )
                    item.update(
                        {
                            "id": f"{doc['id']}_{chunk_id}",
                            "image": image,
                            "entities": entities_in_this_span,
                            "relations": relations_in_this_span,
                        }
                    )
                    yield f"{doc['id']}_{chunk_id}", item
