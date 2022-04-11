import shutil
from pathlib import Path

import fsspec as fs
import requests
from oscar import _BASE_CHECKSUM_FILE_NAME, Oscar, logger


N_EXAMPLES = 2

if __name__ == "__main__":

    for i, config in enumerate(Oscar.BUILDER_CONFIGS):
        logger.info(f"Loading config '{config.name}' ({i + 1}/{len(Oscar.BUILDER_CONFIGS)})")

        # Get data url
        checksum_filename = _BASE_CHECKSUM_FILE_NAME.format(language=config.language)
        checksum_url = config.base_data_url + checksum_filename
        checksum_file_content = requests.get(checksum_url).text.splitlines()
        data_filename = checksum_file_content[0].split("\t")[0]
        data_url = config.base_data_url + data_filename

        # Get a few examples
        with fs.open(data_url, "rt", compression="gzip") as f:
            current_examples = 0
            dummy_content = []
            for line in f:
                dummy_content.append(line)
                current_examples += len(line.strip()) == 0
                if current_examples == N_EXAMPLES:
                    break
            dummy_content = "".join(dummy_content).rstrip()

        # Write dummy files
        dummy_data_dir = Path(__file__).resolve().parent / "dummy" / config.name / str(config.version) / "dummy_data"
        dummy_data_dir.mkdir(parents=True, exist_ok=True)
        (dummy_data_dir / checksum_filename).open("w").write(data_filename + "\t insert_hash_here")
        with fs.open(str(dummy_data_dir / data_filename), "wt", compression="gzip") as f:
            f.write(dummy_content)

        # Compress to dummy_data.zip
        root_dir = str(dummy_data_dir.parent)
        base_name = str(dummy_data_dir)
        base_dir = "dummy_data"
        logger.info(f"Compressing dummy data folder to '{base_name}.zip'")
        shutil.make_archive(base_name, "zip", root_dir, base_dir)
        shutil.rmtree(base_name)
