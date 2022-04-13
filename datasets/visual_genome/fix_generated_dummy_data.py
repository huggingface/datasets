import json
import re
from pathlib import Path
from zipfile import ZipFile


def main():
    dummy_dir = Path(__file__).parent / "dummy"
    config_paths = list(dummy_dir.iterdir())

    for config in config_paths:
        versions = list(config.iterdir())
        assert len(versions) == 1, versions
        version = versions[0]
        zip_filepath = version / "dummy_data.zip"

        # We need to open the zip file
        with ZipFile(zip_filepath, "r") as zip_dir:
            with zip_dir.open("dummy_data/image_data.json.zip/image_data.json", "r") as fi:
                image_metadatas = json.load(fi)

        default_jpg_path = Path(__file__).parent / "huggingface.jpg"
        with ZipFile(zip_filepath, "a") as zip_dir:
            for image_metadata in image_metadatas:
                url = image_metadata["url"]

                matches = re.match(r"https://cs.stanford.edu/people/rak248/VG_100K(?:_(2))?/[0-9]+.jpg", url)
                assert matches is not None

                # Find where locally the images should be
                vg_version = matches.group(1)
                if vg_version is None:
                    local_path = re.sub(
                        "https://cs.stanford.edu/people/rak248/VG_100K", "dummy_data/images.zip/VG_100K", url
                    )
                else:
                    local_path = re.sub(
                        f"https://cs.stanford.edu/people/rak248/VG_100K_{vg_version}",
                        f"dummy_data/images{vg_version}.zip/VG_100K_{vg_version}",
                        url,
                    )

                # Write those images.
                zip_dir.write(filename=default_jpg_path, arcname=local_path)


if __name__ == "__main__":
    main()
