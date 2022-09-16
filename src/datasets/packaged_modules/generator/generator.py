from dataclasses import dataclass
from typing import Callable, Optional

import datasets


@dataclass
class GeneratorConfig(datasets.BuilderConfig):
    generator: Optional[Callable] = None
    gen_kwargs: Optional[dict] = None
    features: Optional[datasets.Features] = None

    def __post_init__(self):
        assert self.generator is not None, "generator must be specified"

        if self.gen_kwargs is None:
            self.gen_kwargs = {}


class Generator(datasets.GeneratorBasedBuilder):
    BUILDER_CONFIG_CLASS = GeneratorConfig

    def _info(self):
        return datasets.DatasetInfo(features=self.config.features)

    def _split_generators(self, dl_manager):
        return [datasets.SplitGenerator(name=datasets.Split.TRAIN, gen_kwargs={})]

    def _generate_examples(self):
        for idx, ex in enumerate(self.config.generator(**self.config.gen_kwargs)):
            yield idx, ex
