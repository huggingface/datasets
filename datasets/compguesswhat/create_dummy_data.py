import gzip
import json
import os
from argparse import ArgumentParser

parser = ArgumentParser()
parser.add_argument("-d", "--data_path", type=str, required=True,
                    help="Data path containing the CompGuessWhat?! datasets (files with 'jsonl.gz' extension)")
parser.add_argument("--examples", type=int, default=5, help="Number of games to consider in the dummy dataset")
data_files = {
    "train": "compguesswhat.train.jsonl.gz",
    "valid": "compguesswhat.valid.jsonl.gz",
    "test": "compguesswhat.test.jsonl.gz"
}

COMPGUESSWHAT_ROOT = "datasets/compguesswhat/"


def main(args):
    # args.data_path is the directory containing the already downloaded dataset files
    # we assume that the dataset test was successful and we have the file dataset_info.json
    dataset_info_path = os.path.join(COMPGUESSWHAT_ROOT, "dataset_infos.json")

    if not os.path.exists(dataset_info_path):
        raise ValueError(
            "The file 'dataset_info.json' doesn't exists. Make sure that you run the dataset tests via nlp-cli.")

    with open(dataset_info_path) as in_file:
        dataset_info = json.load(in_file)

    dataset_version = dataset_info["default"]["version"]["version_str"]

    print(f"Creating dummy data for CompGuessWhat?! {dataset_version}")
    dummy_data_path = os.path.join(
        COMPGUESSWHAT_ROOT,
        "dummy",
        dataset_version,
        "dummy_data"
    )

    if not os.path.exists(dummy_data_path):
        os.makedirs(dummy_data_path)

    for split_name, split_file in data_files.items():
        print(f"Generating dummy data for split {split_name} (num. examples = {args.examples})")

        split_filepath = os.path.join(args.data_path, split_file)
        print(f"Reading split file {split_filepath}")
        with gzip.open(split_filepath) as in_file:
            dummy_filepath = os.path.join(
                dummy_data_path,
                split_file
            )
            with gzip.open(dummy_filepath, mode="w") as out_file:
                for i, line in enumerate(in_file):
                    if i > args.examples:
                        break

                    data = json.loads(line.strip())
                    out_file.write(json.dumps(data).encode("utf-8"))
                    out_file.write(b"\n")


if __name__ == "__main__":
    args = parser.parse_args()
    main(args)
