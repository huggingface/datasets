import gzip
import json
import os
from argparse import ArgumentParser


parser = ArgumentParser()
parser.add_argument(
    "-d",
    "--data_path",
    type=str,
    required=True,
    help="Data path containing the CompGuessWhat?! datasets (files with 'jsonl.gz' extension)",
)
parser.add_argument(
    "--examples",
    type=int,
    default=5,
    help="Number of games to consider in the dummy dataset",
)
original_data_files = {
    "train": "compguesswhat.train.jsonl.gz",
    "valid": "compguesswhat.valid.jsonl.gz",
    "test": "compguesswhat.test.jsonl.gz",
}

zs_data_files = {
    "nd_valid": "compguesswhat.nd_valid.jsonl.gz",
    "od_valid": "compguesswhat.od_valid.jsonl.gz",
    "nd_test": "compguesswhat.nd_test.jsonl.gz",
    "od_test": "compguesswhat.od_test.jsonl.gz",
}

COMPGUESSWHAT_ROOT = "datasets/compguesswhat/"


def create_dummy_data_for_split(data_path, dataset_name, dataset_version, data_files):
    full_dataset_name = "-".join(["compguesswhat", dataset_name])
    dummy_data_path = os.path.join(
        COMPGUESSWHAT_ROOT,
        "dummy",
        full_dataset_name,
        dataset_version,
        "dummy_data",
        full_dataset_name,
        dataset_version,
    )

    if not os.path.exists(dummy_data_path):
        os.makedirs(dummy_data_path)

    for split_name, split_file in data_files.items():
        print(f"Generating dummy data for split {split_name} (num. examples = {args.examples})")

        split_filepath = os.path.join(data_path, full_dataset_name, dataset_version, split_file)
        print(f"Reading split file {split_filepath}")
        with gzip.open(split_filepath) as in_file:
            dummy_filepath = os.path.join(dummy_data_path, split_file)
            with gzip.open(dummy_filepath, mode="w") as out_file:
                for i, line in enumerate(in_file):
                    if i > args.examples:
                        break

                    data = json.loads(line.strip())
                    out_file.write(json.dumps(data).encode("utf-8"))
                    out_file.write(b"\n")


def main(args):
    # args.data_path is the directory containing the already downloaded dataset files
    # we assume that the dataset test was successful and we have the file dataset_info.json
    dataset_info_path = os.path.join(COMPGUESSWHAT_ROOT, "dataset_infos.json")

    if not os.path.exists(dataset_info_path):
        raise ValueError(
            "The file 'dataset_info.json' doesn't exists. Make sure that you run the dataset tests via datasets-cli."
        )

    with open(dataset_info_path, encoding="utf-8") as in_file:
        dataset_info = json.load(in_file)

    dataset_version = dataset_info["compguesswhat-original"]["version"]["version_str"]

    print(f"Creating dummy data for CompGuessWhat?! {dataset_version}")

    print("Original dataset...")
    create_dummy_data_for_split(args.data_path, "original", dataset_version, original_data_files)

    print("Zero-shot dataset...")
    create_dummy_data_for_split(args.data_path, "zero_shot", dataset_version, zs_data_files)


if __name__ == "__main__":
    args = parser.parse_args()
    main(args)
