import json

from datasets.packaged_modules.eval.eval import Eval


def test_infer_features_skips_logs_without_samples(tmp_path):
    empty_log = tmp_path / "empty"
    empty_log.mkdir()
    nonempty_log = tmp_path / "nonempty"
    samples_dir = nonempty_log / "samples"
    samples_dir.mkdir(parents=True)
    sample_file = samples_dir / "1_epoch_1.json"
    sample_file.write_text(json.dumps({"id": 1, "epoch": 1}))

    features = Eval()._infer_features([list(empty_log.iterdir()), [str(sample_file)]])

    assert features is not None
    assert set(features) == {"id", "epoch"}
