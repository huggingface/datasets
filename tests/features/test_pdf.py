from io import BytesIO
from pathlib import Path

import pytest

from datasets import Dataset, Features, Pdf

from ..utils import require_pdfplumber


@require_pdfplumber
@pytest.mark.parametrize(
    "build_example",
    [
        lambda pdf_path: pdf_path,
        lambda pdf_path: Path(pdf_path),
        lambda pdf_path: open(pdf_path, "rb").read(),
        lambda pdf_path: {"path": pdf_path},
        lambda pdf_path: {"path": pdf_path, "bytes": None},
        lambda pdf_path: {"path": pdf_path, "bytes": open(pdf_path, "rb").read()},
        lambda pdf_path: {"path": None, "bytes": open(pdf_path, "rb").read()},
        lambda pdf_path: {"bytes": open(pdf_path, "rb").read()},
    ],
)
def test_pdf_feature_encode_example(shared_datadir, build_example):
    import pdfplumber

    pdf_path = str(shared_datadir / "test_pdf.pdf")
    pdf = Pdf()
    encoded_example = pdf.encode_example(build_example(pdf_path))
    assert isinstance(encoded_example, dict)
    assert encoded_example.keys() == {"bytes", "path"}
    assert encoded_example["bytes"] is not None or encoded_example["path"] is not None
    decoded_example = pdf.decode_example(encoded_example)
    assert isinstance(decoded_example, pdfplumber.pdf.PDF)


@require_pdfplumber
def test_pdf_feature_decode_example_remote_non_hub_url(shared_datadir, monkeypatch):
    import pdfplumber

    pdf_path = shared_datadir / "test_pdf.pdf"
    monkeypatch.setattr("datasets.features.pdf.xopen", lambda *args, **kwargs: BytesIO(pdf_path.read_bytes()))

    decoded_example = Pdf().decode_example({"path": "https://example.com/a.pdf", "bytes": None})

    assert isinstance(decoded_example, pdfplumber.pdf.PDF)


@require_pdfplumber
def test_pdf_decode_example_is_idempotent(shared_datadir):
    pdf_path = str(shared_datadir / "test_pdf.pdf")
    decoded_example = Pdf().decode_example({"path": pdf_path, "bytes": None})
    # decoding an already decoded example returns it as is, so decoding twice is a no-op
    assert Pdf().decode_example(decoded_example) is decoded_example


@require_pdfplumber
def test_iterable_dataset_with_pdf_feature_decoded_twice(shared_datadir):
    import pdfplumber

    pdf_path = str(shared_datadir / "test_pdf.pdf")
    ds = Dataset.from_dict({"pdf": [pdf_path] * 3}, features=Features({"pdf": Pdf()})).to_iterable_dataset()
    # streaming a dataset from the Hub decodes it in threads, and `.decode()` after another step decodes again
    ds = ds.decode(num_threads=2).shuffle(seed=0, buffer_size=3).decode(num_threads=2)
    examples = list(ds)
    assert len(examples) == 3
    assert all(isinstance(example["pdf"], pdfplumber.pdf.PDF) for example in examples)


@require_pdfplumber
def test_dataset_with_pdf_feature(shared_datadir):
    import pdfplumber

    pdf_path = str(shared_datadir / "test_pdf.pdf")
    data = {"pdf": [pdf_path]}
    features = Features({"pdf": Pdf()})
    dset = Dataset.from_dict(data, features=features)
    item = dset[0]
    assert item.keys() == {"pdf"}
    assert isinstance(item["pdf"], pdfplumber.pdf.PDF)
    batch = dset[:1]
    assert len(batch) == 1
    assert batch.keys() == {"pdf"}
    assert isinstance(batch["pdf"], list) and all(isinstance(item, pdfplumber.pdf.PDF) for item in batch["pdf"])
    column = dset["pdf"]
    assert len(column) == 1
    assert isinstance(column, list) and all(isinstance(item, pdfplumber.pdf.PDF) for item in column)

    # from bytes
    with open(pdf_path, "rb") as f:
        data = {"pdf": [f.read()]}
    dset = Dataset.from_dict(data, features=features)
    item = dset[0]
    assert item.keys() == {"pdf"}
    assert isinstance(item["pdf"], pdfplumber.pdf.PDF)
