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
@pytest.mark.parametrize("use_context_manager", [False, True])
def test_pdf_feature_decode_remote_closes_stream(monkeypatch, use_context_manager):
    pdf_path = Path(__file__).parent / "data" / "test_pdf.pdf"
    stream = pdf_path.open("rb")
    monkeypatch.setattr("datasets.features.pdf.xopen", lambda *args, **kwargs: stream)
    try:
        decoded_example = Pdf().decode_example({"path": "https://example.com/a.pdf", "bytes": None})
        assert decoded_example.stream is stream
        assert not stream.closed
        # Page content is still read lazily, after decode_example returns.
        assert decoded_example.pages[0].extract_text()
        if use_context_manager:
            with decoded_example as pdf:
                assert pdf.pages[0].extract_text()
        else:
            decoded_example.close()
        assert stream.closed
    finally:
        stream.close()


@require_pdfplumber
def test_pdf_feature_decode_remote_closes_stream_on_invalid_pdf(monkeypatch):
    try:
        from pdfplumber.utils.exceptions import PdfminerException
    except ImportError:
        from pdfminer.pdfparser import PDFSyntaxError as PdfminerException

    stream = BytesIO(b"not a PDF")
    monkeypatch.setattr("datasets.features.pdf.xopen", lambda *args, **kwargs: stream)
    try:
        # pdfplumber wraps PDFSyntaxError in newer releases.
        with pytest.raises(PdfminerException, match="No /Root object"):
            Pdf().decode_example({"path": "https://example.com/invalid.pdf", "bytes": None})
        assert stream.closed
    finally:
        stream.close()


@require_pdfplumber
@pytest.mark.parametrize("error_type", [RuntimeError, KeyboardInterrupt])
def test_pdf_feature_decode_remote_closes_stream_on_error(monkeypatch, error_type):
    stream = BytesIO(b"unused")
    error = error_type("decoding interrupted")
    monkeypatch.setattr("datasets.features.pdf.xopen", lambda *args, **kwargs: stream)

    def raise_error(*args, **kwargs):
        raise error

    monkeypatch.setattr("pdfplumber.PDF.__init__", raise_error)
    try:
        with pytest.raises(error_type) as caught:
            Pdf().decode_example({"path": "https://example.com/a.pdf", "bytes": None})
        assert caught.value is error
        assert stream.closed
    finally:
        stream.close()


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
