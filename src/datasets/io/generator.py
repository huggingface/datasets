from typing import Callable, Optional

from .. import Features
from ..packaged_modules.generator.generator import Generator
from .abc import AbstractDatasetInputStream


class GeneratorDatasetInputStream(AbstractDatasetInputStream):
    def __init__(
        self,
        generator: Callable,
        features: Optional[Features] = None,
        cache_dir: str = None,
        keep_in_memory: bool = False,
        streaming: bool = False,
        gen_kwargs: Optional[dict] = None,
        **kwargs,
    ):
        super().__init__(
            features=features, cache_dir=cache_dir, keep_in_memory=keep_in_memory, streaming=streaming, **kwargs
        )
        self.builder = Generator(
            cache_dir=cache_dir,
            features=features,
            generator=generator,
            gen_kwargs=gen_kwargs,
            **kwargs,
        )

    def read(self):
        # Build iterable dataset
        if self.streaming:
            dataset = self.builder.as_streaming_dataset(split="train")
        # Build regular (map-style) dataset
        else:
            download_config = None
            download_mode = None
            ignore_verifications = False
            use_auth_token = None
            base_path = None

            self.builder.download_and_prepare(
                download_config=download_config,
                download_mode=download_mode,
                ignore_verifications=ignore_verifications,
                # try_from_hf_gcs=try_from_hf_gcs,
                base_path=base_path,
                use_auth_token=use_auth_token,
            )
            dataset = self.builder.as_dataset(
                split="train", ignore_verifications=ignore_verifications, in_memory=self.keep_in_memory
            )
        return dataset
