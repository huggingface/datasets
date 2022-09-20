import xml.etree.ElementTree as ET
from collections import Counter
from dataclasses import dataclass
from typing import Optional

import datasets


logger = datasets.utils.logging.get_logger(__name__)


@dataclass
class XmlConfig(datasets.BuilderConfig):
    """BuilderConfig for XML."""

    features: Optional[datasets.Features] = None
    field: Optional[str] = None


class Xml(datasets.GeneratorBasedBuilder):
    BUILDER_CONFIG_CLASS = XmlConfig

    def _info(self):
        return datasets.DatasetInfo(features=self.config.features)

    def _split_generators(self, dl_manager):
        if not self.config.data_files:
            raise ValueError(f"At least one data file must be specified, but got data_files={self.config.data_files}")
        data_files = dl_manager.download_and_extract(self.config.data_files)
        if isinstance(data_files, (str, list, tuple)):
            data_files = {datasets.Split.TRAIN: data_files}
        splits = []
        for split_name, files in data_files.items():
            splits.append(datasets.SplitGenerator(name=split_name, gen_kwargs={"files": dl_manager.iter_files(files)}))
        return splits

    def _generate_examples(self, files):
        uid = 0
        for file in files:
            for _, element in ET.iterparse(file):
                if element.tag == self.config.field:  # TODO: if no field is passed
                    yield uid, parse_xml_element(element)
                    uid += 1


def parse_xml_element(element: ET.Element):
    text = element.text.strip() if element.text else None
    data = {
        **{f"@{key}": value for key, value in element.items()},
        **({"#text": text} if text else {}),
        **MultiDict([(subelement.tag, parse_xml_element(subelement)) for subelement in element]).to_dict(),
    }
    if data.keys() == set(["#text"]):
        data = data["#text"]
    return data


class MultiDict:
    def __init__(self, iterable):
        self.iterable = iterable

    def to_dict(self):
        result = {}
        counter = Counter([k for k, _ in self.iterable])
        for key, value in self.iterable:
            result[key] = value if counter[key] == 1 else result.get(key, []) + [value]
        return result
