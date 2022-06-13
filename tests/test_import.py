import sys

from .utils import require_tf


@require_tf
def test_import_datasets_doesnt_import_tensorfow():
    import datasets  # noqa

    assert "tensorflow" not in sys.modules
