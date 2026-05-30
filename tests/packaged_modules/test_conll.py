import textwrap

import pyarrow as pa
import pytest

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


def test_generate_tables_empty_column_names_raises(tmp_path):
    """Empty column_names should raise a clear ValueError."""
    filename = tmp_path / "x.conll"
    with open(filename, "w", encoding="utf-8") as f:
        f.write("a b\n")
    builder = Conll(column_names=[])
    generator = builder._generate_tables(base_files=[str(filename)], files_iterables=[[str(filename)]])
    with pytest.raises(ValueError, match="column_names must be a non-empty list"):
        list(generator)
