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


@require_pdfplumber
@pytest.mark.parametrize("position", [0, 19])
def test_pdf_feature_encode_in_memory_pdf(shared_datadir, position):
    import pdfplumber

    data = (shared_datadir / "test_pdf.pdf").read_bytes()
    with pdfplumber.open(BytesIO(data)) as pdf:
        pdf.stream.seek(position)
        encoded = Pdf().encode_example(pdf)
        assert encoded == {"path": None, "bytes": data}
        assert pdf.stream.tell() == position
        assert not pdf.stream.closed
        assert Pdf().encode_example(pdf) == encoded
        decoded = Pdf().decode_example(encoded)
        assert decoded.pages[0].extract_text() == pdf.pages[0].extract_text()


@require_pdfplumber
@pytest.mark.parametrize("operation", ["from_dict", "map"])
def test_dataset_with_in_memory_pdf(shared_datadir, operation):
    import pdfplumber

    data = (shared_datadir / "test_pdf.pdf").read_bytes()
    features = Features({"pdf": Pdf()})
    with pdfplumber.open(BytesIO(data)) as pdf:
        if operation == "from_dict":
            dataset = Dataset.from_dict({"pdf": [pdf]}, features=features)
        else:
            dataset = Dataset.from_dict({"pdf": [data]}, features=features).map(
                lambda example: {"pdf": example["pdf"]}
            )
        encoded = dataset.cast_column("pdf", Pdf(decode=False))[0]["pdf"]
        assert encoded == {"path": None, "bytes": data}
        assert dataset[0]["pdf"].pages[0].extract_text() == pdf.pages[0].extract_text()
