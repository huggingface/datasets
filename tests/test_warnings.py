import pytest

from datasets import inspect_metric, list_metrics, load_metric


@pytest.fixture
def mock_emitted_deprecation_warnings(monkeypatch):
    monkeypatch.setattr("datasets.utils.deprecation_utils._emitted_deprecation_warnings", set())


# Used by list_metrics
@pytest.fixture
def mock_hfh(monkeypatch):
    class MetricMock:
        def __init__(self, metric_id):
            self.id = metric_id

    class HfhMock:
        _metrics = [MetricMock(metric_id) for metric_id in ["accuracy", "mse", "precision", "codeparrot/apps_metric"]]

        def list_metrics(self):
            return self._metrics

    monkeypatch.setattr("datasets.inspect.huggingface_hub", HfhMock())


@pytest.mark.parametrize(
    "func, args", [(load_metric, ("metrics/mse",)), (list_metrics, ()), (inspect_metric, ("metrics/mse", "tmp_path"))]
)
def test_metric_deprecation_warning(func, args, mock_emitted_deprecation_warnings, mock_hfh, tmp_path):
    if "tmp_path" in args:
        args = tuple(arg if arg != "tmp_path" else tmp_path for arg in args)
    with pytest.warns(FutureWarning, match="https://huggingface.co/docs/evaluate"):
        func(*args)
