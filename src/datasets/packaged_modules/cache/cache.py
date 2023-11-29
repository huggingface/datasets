from datasets import DatasetInfo, GeneratorBasedBuilder, SplitGenerator


class Cache(GeneratorBasedBuilder):
    def _info(self) -> DatasetInfo:
        return DatasetInfo()

    def _split_generators(self, dl_manager):
        return [SplitGenerator(name=name, gen_kwargs={}) for name in self.info.splits]
