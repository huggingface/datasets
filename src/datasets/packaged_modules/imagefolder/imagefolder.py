from typing import Optional
from dataclasses import dataclass
from pathlib import Path
from typing import List

import pyarrow as pa
import datasets


logger = datasets.utils.logging.get_logger(__name__)

@dataclass
class ImageFolderConfig(datasets.BuilderConfig):
    """BuilderConfig for JSON."""

    features: Optional[datasets.Features] = None

    @property
    def schema(self):
        return pa.schema(self.features.type) if self.features is not None else None


class ImageFolder(datasets.GeneratorBasedBuilder):

    BUILDER_CONFIG_CLASS = ImageFolderConfig

    def _info(self):
        return datasets.DatasetInfo(features=self.config.features)

    def _split_generators(self, dl_manager):
        if not self.config.data_files:
            raise ValueError(f"At least one data file must be specified, but got data_files={self.config.data_files}")
        
        data_files = dl_manager.download_and_extract(self.config.data_files)
        if isinstance(data_files, (str, list, tuple)):
            files = data_files
            if isinstance(files, str):
                files = [files]
            return [datasets.SplitGenerator(name=datasets.Split.TRAIN, gen_kwargs={'archive_path': data_files})]
        splits = []
        for split_name, files in data_files.items():
            if isinstance(files, str):
                files = [files]
            splits.append(datasets.SplitGenerator(name=split_name, gen_kwargs={'archive_path': files}))
        return splits

    def _generate_examples(self, archive_path):
        logger.info("generating examples from = %s", archive_path)
        extensions = {'.jpg', '.jpeg', '.png', '.ppm', '.bmp', '.pgm', '.tif', '.tiff', '.webp'}
        for i, path in enumerate(Path(archive_path).glob('**/*')):
            if path.suffix in extensions:
                yield i, {'file': path.as_posix(), 'labels': path.parent.name.lower()}
