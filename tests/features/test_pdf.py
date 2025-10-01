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
    assert isinstance(batch["pdf"], list) and all(
        isinstance(item, pdfplumber.pdf.PDF) for item in batch["pdf"]
    )
    column = dset["pdf"]
    assert len(column) == 1
    assert isinstance(column, list) and all(
        isinstance(item, pdfplumber.pdf.PDF) for item in column
    )

    # from bytes
    with open(pdf_path, "rb") as f:
        data = {"pdf": [f.read()]}
    dset = Dataset.from_dict(data, features=features)
    item = dset[0]
    assert item.keys() == {"pdf"}
    assert isinstance(item["pdf"], pdfplumber.pdf.PDF)
