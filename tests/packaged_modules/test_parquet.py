from contextlib import nullcontext as does_not_raise

import pytest

from datasets.packaged_modules.parquet.parquet import Parquet


@pytest.mark.parametrize("only_supported_extensions, raises", [(None, True), (False, True), (True, False)])
def test_parquet_reads_only_supported_extensions(only_supported_extensions, raises, text_file, image_file):
    config_kwargs = (
        {"only_supported_extensions": only_supported_extensions} if only_supported_extensions is not None else {}
    )
    expectation = pytest.raises(ValueError) if raises else does_not_raise()
    builder = Parquet(**config_kwargs)
    generator = builder._generate_tables([[text_file, image_file]])
    # If image file is read, it raises ArrowInvalid: Parquet magic bytes not found in footer. Either the file is corrupted or this is not a parquet file.
    with expectation:
        for _ in generator:
            pass
