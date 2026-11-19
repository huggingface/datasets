import importlib
import textwrap
from contextlib import contextmanager

import pyarrow as pa
import pytest

from datasets import ClassLabel, Features, List, Value, load_dataset
from datasets.builder import InvalidConfigName
from datasets.data_files import DataFilesList
from datasets.packaged_modules.conll.conll import Conll, ConllConfig


@pytest.fixture
def conll2003_file(tmp_path):
    """Minimal CoNLL-2003-style NER file: token POS chunk NER."""
    filename = tmp_path / "sample.conll"
    data = textwrap.dedent(
        """\
        -DOCSTART- -X- -X- O

        EU NNP B-NP B-ORG
        rejects VBZ B-VP O
        German JJ B-NP B-MISC
        call NN I-NP O
        . . O O

        Peter NNP B-NP B-PER
        Blackburn NNP I-NP I-PER
        """
    )
    with open(filename, "w", encoding="utf-8") as f:
        f.write(data)
    return str(filename)


@pytest.fixture
def conll_no_trailing_blank_file(tmp_path):
    """Sentence with no trailing blank line — should still flush."""
    filename = tmp_path / "no_trailing.conll"
    data = "Hello NN\nworld NN\n. ."
    with open(filename, "w", encoding="utf-8") as f:
        f.write(data)
    return str(filename)


@pytest.fixture
def conll_tab_delimited_file(tmp_path):
    """Tab-delimited CoNLL — fields can contain spaces."""
    filename = tmp_path / "tab.conll"
    data = "tok1\tNN\nphrase with spaces\tNNP\n\ntok2\tVB\n"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(data)
    return str(filename)


@pytest.fixture
def conllu_file(tmp_path):
    """CoNLL-U with # comment lines."""
    filename = tmp_path / "sample.conllu"
    data = textwrap.dedent(
        """\
        # sent_id = test-1
        # text = The cat sat.
        1\tThe\tthe\tDET
        2\tcat\tcat\tNOUN
        3\tsat\tsit\tVERB
        4\t.\t.\tPUNCT

        # sent_id = test-2
        1\tHello\thello\tINTJ
        """
    )
    with open(filename, "w", encoding="utf-8") as f:
        f.write(data)
    return str(filename)


def test_config_raises_when_invalid_name() -> None:
    with pytest.raises(InvalidConfigName, match="Bad characters"):
        _ = ConllConfig(name="name-with-*-invalid-character")


@pytest.mark.parametrize("data_files", ["str_path", ["str_path"], DataFilesList(["str_path"], [()])])
def test_config_raises_when_invalid_data_files(data_files) -> None:
    with pytest.raises(ValueError, match="Expected a DataFilesDict"):
        _ = ConllConfig(name="name", data_files=data_files)


def test_config_default_column_names():
    c = ConllConfig(name="test")
    assert c.column_names == ["tokens"]


def test_generate_tables_conll2003_with_full_schema(conll2003_file):
    builder = Conll(
        column_names=["tokens", "pos_tags", "chunk_tags", "ner_tags"],
    )
    generator = builder._generate_tables(base_files=[conll2003_file], files_iterables=[[conll2003_file]])
    pa_table = pa.concat_tables([table for _, table in generator])
    data = pa_table.to_pydict()

    assert data["tokens"] == [
        ["EU", "rejects", "German", "call", "."],
        ["Peter", "Blackburn"],
    ]
    assert data["pos_tags"] == [
        ["NNP", "VBZ", "JJ", "NN", "."],
        ["NNP", "NNP"],
    ]
    assert data["chunk_tags"] == [
        ["B-NP", "B-VP", "B-NP", "I-NP", "O"],
        ["B-NP", "I-NP"],
    ]
    assert data["ner_tags"] == [
        ["B-ORG", "O", "B-MISC", "O", "O"],
        ["B-PER", "I-PER"],
    ]


def test_generate_tables_skips_docstart_by_default(conll2003_file):
    builder = Conll(column_names=["tokens", "pos_tags", "chunk_tags", "ner_tags"])
    generator = builder._generate_tables(base_files=[conll2003_file], files_iterables=[[conll2003_file]])
    pa_table = pa.concat_tables([table for _, table in generator])
    # DOCSTART line should not appear as a token
    all_tokens = sum(pa_table.to_pydict()["tokens"], [])
    assert "-DOCSTART-" not in all_tokens


def test_generate_tables_keeps_docstart_when_disabled(conll2003_file):
    builder = Conll(
        column_names=["tokens", "pos_tags", "chunk_tags", "ner_tags"],
        skip_docstart=False,
    )
    generator = builder._generate_tables(base_files=[conll2003_file], files_iterables=[[conll2003_file]])
    pa_table = pa.concat_tables([table for _, table in generator])
    all_tokens = sum(pa_table.to_pydict()["tokens"], [])
    assert "-DOCSTART-" in all_tokens


def test_generate_tables_flushes_tail_sentence_without_trailing_blank(
    conll_no_trailing_blank_file,
):
    builder = Conll(column_names=["tokens", "pos_tags"])
    generator = builder._generate_tables(
        base_files=[conll_no_trailing_blank_file],
        files_iterables=[[conll_no_trailing_blank_file]],
    )
    pa_table = pa.concat_tables([table for _, table in generator])
    assert pa_table.to_pydict()["tokens"] == [["Hello", "world", "."]]
    assert pa_table.to_pydict()["pos_tags"] == [["NN", "NN", "."]]


def test_generate_tables_with_tab_delimiter(conll_tab_delimited_file):
    builder = Conll(column_names=["tokens", "pos_tags"], delimiter="\t")
    generator = builder._generate_tables(
        base_files=[conll_tab_delimited_file],
        files_iterables=[[conll_tab_delimited_file]],
    )
    pa_table = pa.concat_tables([table for _, table in generator])
    # 'phrase with spaces' must stay a single token under tab delimiter
    assert pa_table.to_pydict()["tokens"] == [["tok1", "phrase with spaces"], ["tok2"]]


def test_generate_tables_conllu_with_comment_prefix(conllu_file):
    builder = Conll(
        column_names=["id", "form", "lemma", "upos"],
        delimiter="\t",
        comment_prefix="#",
    )
    generator = builder._generate_tables(base_files=[conllu_file], files_iterables=[[conllu_file]])
    pa_table = pa.concat_tables([table for _, table in generator])
    data = pa_table.to_pydict()
    # 2 sentences, comments stripped, # never appears in any column
    assert data["form"] == [["The", "cat", "sat", "."], ["Hello"]]
    assert data["upos"] == [["DET", "NOUN", "VERB", "PUNCT"], ["INTJ"]]
    for col in data.values():
        for sentence in col:
            for cell in sentence:
                assert not cell.startswith("#")


def test_generate_tables_pads_rows_with_fewer_columns(tmp_path):
    """A row with fewer columns than column_names should pad with empty strings."""
    filename = tmp_path / "padded.conll"
    with open(filename, "w", encoding="utf-8") as f:
        f.write("only_token\nfull token POS\n")
    builder = Conll(column_names=["tokens", "pos_tags"])
    generator = builder._generate_tables(base_files=[str(filename)], files_iterables=[[str(filename)]])
    pa_table = pa.concat_tables([table for _, table in generator])
    assert pa_table.to_pydict()["tokens"] == [["only_token", "full"]]
    # First row has empty POS (padded), second has "token" because line had 3 parts but column_names has 2 -> truncated
    assert pa_table.to_pydict()["pos_tags"] == [["", "token"]]


def test_generate_tables_truncates_rows_with_extra_columns(tmp_path):
    """A row with more columns than column_names should truncate."""
    filename = tmp_path / "extra.conll"
    with open(filename, "w", encoding="utf-8") as f:
        f.write("tok POS chunk ner extra_col\n")
    builder = Conll(column_names=["tokens", "pos_tags"])
    generator = builder._generate_tables(base_files=[str(filename)], files_iterables=[[str(filename)]])
    pa_table = pa.concat_tables([table for _, table in generator])
    assert pa_table.to_pydict()["tokens"] == [["tok"]]
    assert pa_table.to_pydict()["pos_tags"] == [["POS"]]


@pytest.mark.parametrize("num_sentences", [0, 1, 1000, 1001, 2000, 2001])
@pytest.mark.parametrize("trailing_blank", [False, True])
def test_generate_tables_batches_sentences(tmp_path, num_sentences, trailing_blank):
    filename = tmp_path / "batched.conll"
    sentences = [f"token{i} NN\n. ." for i in range(num_sentences)]
    filename.write_text("\n\n".join(sentences) + ("\n\n" if trailing_blank else ""), encoding="utf-8")
    builder = Conll(column_names=["tokens", "pos_tags"])
    batches = list(builder._generate_tables(base_files=[str(filename)], files_iterables=[[str(filename)]]))

    expected_sizes = [1000] * (num_sentences // 1000)
    if num_sentences % 1000:
        expected_sizes.append(num_sentences % 1000)
    assert [table.num_rows for _, table in batches] == expected_sizes
    assert len({str(key) for key, _ in batches}) == len(batches)
    if batches:
        assert pa.concat_tables([table for _, table in batches]).to_pydict() == {
            "tokens": [[f"token{i}", "."] for i in range(num_sentences)],
            "pos_tags": [["NN", "."] for _ in range(num_sentences)],
        }


def test_generate_tables_yields_before_reading_entire_file(tmp_path, monkeypatch):
    filename = tmp_path / "streamed.conll"
    filename.write_text("token NN\n\n" * 2001, encoding="utf-8")
    lines_read = []

    @contextmanager
    def tracked_open(*args, **kwargs):
        with open(*args, **kwargs) as f:

            def tracked_lines():
                for line in f:
                    lines_read.append(line)
                    yield line

            yield tracked_lines()

    monkeypatch.setattr(importlib.import_module(Conll.__module__), "open", tracked_open, raising=False)
    builder = Conll(column_names=["tokens", "pos_tags"])
    generator = builder._generate_tables(base_files=[str(filename)], files_iterables=[[str(filename)]])
    try:
        _, first_table = next(generator)
        assert first_table.num_rows == 1000
        assert len(lines_read) == 2000
    finally:
        generator.close()


def test_generate_tables_batches_multiple_files_in_shard(tmp_path):
    files = []
    for file_idx in range(2):
        filename = tmp_path / f"{file_idx}.conll"
        filename.write_text("\n\n".join(f"token{file_idx}-{i} NN" for i in range(3)), encoding="utf-8")
        files.append(str(filename))
    builder = Conll(column_names=["tokens", "pos_tags"], batch_size=2)
    batches = list(builder._generate_tables(base_files=files, files_iterables=[files]))

    assert [table.num_rows for _, table in batches] == [2, 1, 2, 1]
    assert [key.original_shard_id for key, _ in batches] == [0, 0, 0, 0]
    assert [key.item_or_batch_id for key, _ in batches] == [0, 1, 2, 3]
    assert pa.concat_tables([table for _, table in batches]).to_pydict() == {
        "tokens": [[f"token{file_idx}-{i}"] for file_idx in range(2) for i in range(3)],
        "pos_tags": [["NN"] for _ in range(6)],
    }


@pytest.mark.parametrize("streaming", [False, True])
@pytest.mark.parametrize("with_features", [False, True])
def test_load_dataset_batches_preserve_sentences(tmp_path, streaming, with_features):
    filename = tmp_path / "loaded.conll"
    filename.write_text("\n\n".join(f"token{i} NN\n. ." for i in range(5)), encoding="utf-8")
    features = (
        Features({"tokens": List(Value("string")), "pos_tags": List(ClassLabel(names=["NN", "."]))})
        if with_features
        else None
    )
    ds = load_dataset(
        "conll",
        data_files=str(filename),
        split="train",
        column_names=["tokens", "pos_tags"],
        batch_size=2,
        features=features,
        streaming=streaming,
        cache_dir=str(tmp_path / "cache"),
    )
    assert list(ds) == [
        {"tokens": [f"token{i}", "."], "pos_tags": [0, 1] if with_features else ["NN", "."]} for i in range(5)
    ]
    if with_features:
        assert ds.features == features


def test_generate_tables_empty_column_names_raises(tmp_path):
    """Empty column_names should raise a clear ValueError."""
    filename = tmp_path / "x.conll"
    with open(filename, "w", encoding="utf-8") as f:
        f.write("a b\n")
    builder = Conll(column_names=[])
    generator = builder._generate_tables(base_files=[str(filename)], files_iterables=[[str(filename)]])
    with pytest.raises(ValueError, match="column_names must be a non-empty list"):
        list(generator)
