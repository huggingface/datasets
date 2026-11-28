import pyarrow as pa
import pytest

from datasets import Dataset, Features, Value, load_dataset
from datasets.packaged_modules.csv.csv import Csv


PARSER_MODES = [
    pytest.param({"engine": "pyarrow"}, id="pyarrow"),
    pytest.param({"engine": "python", "skipfooter": 1}, id="python-footer"),
    pytest.param({"skipfooter": 1}, id="inferred-footer"),
]
EXPECTED = {"id": [1, 2, 3, 4, 5], "text": ["α", "second", "third", "fourth", "last"]}


def write_csv(path, options, empty=False):
    rows = [] if empty else [f"{index},{text}\n" for index, text in zip(EXPECTED["id"], EXPECTED["text"])]
    footer = "summary that is not a data record\n" * options.get("skipfooter", 0)
    path.write_text("id,text\n" + "".join(rows) + footer, encoding="utf-8")
    return str(path)


@pytest.mark.parametrize("options", PARSER_MODES)
@pytest.mark.parametrize("chunksize", [1, 2, None])
def test_noniterator_parsers_keep_all_rows_and_arrow_batch_sizes(tmp_path, options, chunksize):
    filename = write_csv(tmp_path / "data.csv", options)
    reader = Csv(cache_dir=str(tmp_path / "cache"), chunksize=chunksize, **options)

    tables = [table for _, table in reader._generate_tables([filename], [[filename]])]

    assert pa.concat_tables(tables).to_pydict() == EXPECTED
    assert [len(table) for table in tables] == (
        [1, 1, 1, 1, 1] if chunksize == 1 else [2, 2, 1] if chunksize == 2 else [5]
    )
    assert reader.config.chunksize == chunksize
    assert reader.config.skipfooter == options.get("skipfooter", 0)


@pytest.mark.parametrize("options", PARSER_MODES)
@pytest.mark.parametrize("streaming", [False, True])
def test_public_csv_readers_use_the_selected_parser(tmp_path, options, streaming):
    filename = write_csv(tmp_path / "data.csv", options)
    features = Features({"id": Value("int32"), "text": Value("string")})
    if streaming:
        dataset = load_dataset(
            "csv", data_files=filename, split="train", streaming=True, features=features, chunksize=2, **options
        )
    else:
        dataset = Dataset.from_csv(
            filename, cache_dir=str(tmp_path / "cache"), features=features, chunksize=2, **options
        )

    assert list(dataset) == [{"id": index, "text": text} for index, text in zip(EXPECTED["id"], EXPECTED["text"])]
    assert dataset.features == features


@pytest.mark.parametrize("options", PARSER_MODES)
def test_header_only_input_still_emits_its_schema(tmp_path, options):
    filename = write_csv(tmp_path / "empty.csv", options, empty=True)
    reader = Csv(cache_dir=str(tmp_path / "cache"), chunksize=2, **options)

    tables = [table for _, table in reader._generate_tables([filename], [[filename]])]

    assert len(tables) == 1
    assert tables[0].column_names == ["id", "text"]
    assert tables[0].num_rows == 0


@pytest.mark.parametrize("options", PARSER_MODES)
def test_parser_settings_apply_independently_to_each_file(tmp_path, options):
    filenames = [write_csv(tmp_path / f"part-{index}.csv", options) for index in range(2)]
    dataset = Dataset.from_csv(filenames, cache_dir=str(tmp_path / "cache"), chunksize=2, **options)

    assert dataset[:] == {name: values * 2 for name, values in EXPECTED.items()}


@pytest.mark.parametrize("engine", [None, "c", "python"])
def test_existing_incremental_parser_modes_are_unchanged(tmp_path, engine):
    filename = write_csv(tmp_path / "data.csv", {})
    reader = Csv(cache_dir=str(tmp_path / "cache"), engine=engine, chunksize=2)

    tables = [table for _, table in reader._generate_tables([filename], [[filename]])]

    assert [len(table) for table in tables] == [2, 2, 1]
    assert pa.concat_tables(tables).to_pydict() == EXPECTED


def test_explicit_c_engine_still_rejects_unsupported_footer_parsing(tmp_path):
    options = {"engine": "c", "skipfooter": 1}
    filename = write_csv(tmp_path / "data.csv", options)
    reader = Csv(cache_dir=str(tmp_path / "cache"), **options)

    with pytest.raises(ValueError, match="skipfooter"):
        list(reader._generate_tables([filename], [[filename]]))
