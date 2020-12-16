import itertools
import os
import pickle
import shutil
from glob import glob
from os.path import join as pjoin


_URLs = {
    "arabic": "https://drive.google.com/uc?export=download&id=1__EjA6oZsgXQpggPm-h54jZu3kP6Y6zu",
    "chinese": "https://drive.google.com/uc?export=download&id=1TuWH7uwu6V90QWmZn25qhou1rm97Egmn",
    "czech": "https://drive.google.com/uc?export=download&id=1GcUN6mytEcOMBBOvjJOQzBmEkc-LdgQg",
    "dutch": "https://drive.google.com/uc?export=download&id=1-w-0uqaC6hnRn1F_3XqJEvi09zlcTIhX",
    "english": "https://drive.google.com/uc?export=download&id=11wMGqNVSwwk6zUnDaJEgm3qT71kAHeff",
    "french": "https://drive.google.com/uc?export=download&id=1Uit4Og1pk-br_0UJIO5sdhApyhTuHzqo",
    "german": "https://drive.google.com/uc?export=download&id=1meSNZHxd_0TZLKCRCYGN-Ke3IA5c1qOE",
    "hindi": "https://drive.google.com/uc?export=download&id=1ZyFGufe4puX3vjGPbp4xg9Hca3Gwq22g",
    "indonesian": "https://drive.google.com/uc?export=download&id=1PGa8j1_IqxiGTc3SU6NMB38sAzxCPS34",
    "italian": "https://drive.google.com/uc?export=download&id=1okwGJiOZmTpNRNgJLCnjFF4Q0H1z4l6_",
    "japanese": "https://drive.google.com/uc?export=download&id=1Z2ty5hU0tIGRZRDlFQZLO7b5vijRfvo0",
    "korean": "https://drive.google.com/uc?export=download&id=1cqu_YAgvlyVSzzjcUyP1Cz7q0k8Pw7vN",
    "portuguese": "https://drive.google.com/uc?export=download&id=1GTHUJxxmjLmG2lnF9dwRgIDRFZaOY3-F",
    "russian": "https://drive.google.com/uc?export=download&id=1fUR3MqJ8jTMka6owA0S-Fe6aHmiophc_",
    "spanish": "https://drive.google.com/uc?export=download&id=17FGi8KI9N9SuGe7elM8qU8_3fx4sfgTr",
    "thai": "https://drive.google.com/uc?export=download&id=1QsV8C5EPJrQl37mwva_5-IJOrCaOi2tH",
    "turkish": "https://drive.google.com/uc?export=download&id=1M1M5yIOyjKWGprc3LUeVVwxgKXxgpqxm",
    "vietnamese": "https://drive.google.com/uc?export=download&id=17FGi8KI9N9SuGe7elM8qU8_3fx4sfgTr",
}


def sanitize_url(url):
    """Convert the url into correct format"""
    url = url.replace("https://drive.google.com/", "")
    url = url.replace("?", "%3F")
    url = url.replace("=", "%3D")
    url = url.replace("&", "%26")
    return url


def create():
    """Creates the dummy pickle file with a subset of data"""
    # 1. Download the google drive folder : https://drive.google.com/drive/folders/1PFvXUOsW_KSEzFm5ixB8J8BDB8zRRfHW
    # and specify the decompressed folder location
    downloaded_data_path = "/Users/katnoria/Downloads/WikiLingua"
    files = glob(f"{downloaded_data_path}/*.pkl")
    base_path = "/Users/katnoria/dev/projects/workspaces/python/datasets"
    for key in _URLs.keys():
        # data = load_dataset('./datasets/wiki_lingua', key)
        print(f"Finding {key}.pkl")
        filepath = [name for name in files if name.endswith(f"{key}.pkl")][0]
        with open(filepath, "rb") as f:
            data = pickle.load(f)

        data_subset = dict(itertools.islice(data.items(), 3))
        fname = sanitize_url(_URLs[key])
        dirname = pjoin(base_path, f"datasets/wiki_lingua/dummy/{key}/1.1.0/dummy_data")
        if not os.path.exists(dirname):
            print(f"created folder {dirname}")
            os.makedirs(dirname)
        fname = pjoin(dirname, fname)
        print(f"creating for {key}:{fname}")
        with open(fname, "wb") as f:
            pickle.dump(data_subset, f)
        print("SUCCESS")


def zip():
    """Zip the file"""
    base_path = "/Users/katnoria/dev/projects/workspaces/python/datasets"
    for key in _URLs.keys():
        # dirname = pjoin(base_path, f"datasets/wiki_lingua/dummy/{key}/1.1.0/dummy_data")
        dirname = pjoin(base_path, f"datasets/wiki_lingua/dummy/{key}/1.1.0")
        print(f"Zipping {dirname}")
        shutil.make_archive(f"{dirname}/dummy_data", "zip", dirname, "dummy_data")
        shutil.rmtree(f"{dirname}/dummy_data")
        print(f"Deleted folder {dirname}/dummy_data")


# Utility script to create the dummy data and zip the contents
# 1. Create data
create()
# 2. Zip contents
zip()
