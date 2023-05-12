from datasets.packaged_modules.parquet.parquet import Parquet


def test_parquet_reads_only_supported_files(parquet_path, image_file):
    builder = Parquet()
    generator = builder._generate_tables([[parquet_path, image_file]])
    # Test that it does not raise ArrowInvalid: Parquet magic bytes not found in footer. Either the file is corrupted or this is not a parquet file.
    for _ in generator:
        pass
