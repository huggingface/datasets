# coding=utf-8
# Copyright 2020 The HuggingFace Datasets Authors and the current dataset script contributor.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""WLASL: A large-scale dataset for Word-Level American Sign Language"""

from __future__ import absolute_import, division, print_function

import json
import urllib.request
from urllib.error import ContentTooShortError

from tqdm import tqdm

import datasets


_DESCRIPTION = """
A large-scale dataset for Word-Level American Sign Language
"""

_CITATION = """\
@inproceedings{dataset:li2020word,
    title={Word-level Deep Sign Language Recognition from Video: A New Large-scale Dataset and Methods Comparison},
    author={Li, Dongxu and Rodriguez, Cristian and Yu, Xin and Li, Hongdong},
    booktitle={The IEEE Winter Conference on Applications of Computer Vision},
    pages={1459--1469},
    year={2020}
}
"""

_URL = (
    "https://raw.githubusercontent.com/dxli94/WLASL/0ac8108282aba99226e29c066cb8eab847ef62da/start_kit/WLASL_v0.3.json"
)

_HOMEPAGE = "https://dxli94.github.io/WLASL/"

_ASLPRO_HEADERS = [
    ("User-Agent", "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7"),
    ("Referer", "http://www.aslpro.com/cgi-bin/aslpro/aslpro.cgi"),
]


def download_aslpro(url: str, dst_path: str):
    # ASL Pro videos are in swf format
    opener = urllib.request.build_opener()
    opener.addheaders = _ASLPRO_HEADERS
    urllib.request.install_opener(opener)

    try:
        urllib.request.urlretrieve(url, dst_path)
    except ContentTooShortError:
        pass


def download_youtube(url, dst_path):
    import youtube_dl  # Required for YouTube downloads

    ydl_opts = {"format": "bestvideo", "outtmpl": dst_path}
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        try:
            ydl.download([url])
        except youtube_dl.utils.DownloadError as e:
            print("Problem downloading youtube video", url)


class WLASL(datasets.GeneratorBasedBuilder):
    """WLASL: A large-scale dataset for Word-Level American Sign Language"""

    VERSION = datasets.Version("0.3.0")

    def _info(self):
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            # This defines the different columns of the dataset and their types
            features=datasets.Features(
                {
                    "video": datasets.Value("string"),  # Video path
                    "url": datasets.Value("string"),  # Remote file URL
                    "start": datasets.Value("int32"),  # Start frame
                    "end": datasets.Value("int32"),  # End frame
                    "fps": datasets.Value("int32"),  # Frames per Second
                    "signer_id": datasets.Value("int32"),  # Unique ID of signer
                    "bbox": datasets.features.Sequence(datasets.Value("int32")),  # Array of integers
                    "gloss": datasets.Value("string"),  # American sign language gloss
                    "gloss_variation": datasets.Value("int32"),  # Variation ID of gloss
                }
            ),
            homepage=_HOMEPAGE,
            citation=_CITATION,
        )

    def _download_video(self, url: str, dl_manager):
        if "aslpro" in url:
            return dl_manager.download_custom(url, download_aslpro)
        elif "youtube" in url or "youtu.be" in url:
            return dl_manager.download_custom(url, download_youtube)
        else:
            return dl_manager.download(url)

    def _download_videos(self, data, dl_manager):
        videos = {}
        for datum in data:
            for instance in datum["instances"]:
                videos[instance["video_id"]] = instance["url"]

        paths = {}
        for video_id, video in tqdm(videos.items(), total=len(videos)):
            try:
                paths[video_id] = self._download_video(video, dl_manager)
            except (FileNotFoundError, ConnectionError) as err:
                print("Failed to download", video, str(err))

        return paths

    def _split_generators(self, dl_manager):
        """Returns SplitGenerators."""

        data_path = dl_manager.download(_URL)

        # Download videos and update paths
        with open(data_path, "r") as f:
            data = json.load(f)
            paths = self._download_videos(data, dl_manager)
            for datum in data:
                for instance in datum["instances"]:
                    instance["video"] = paths[instance["video_id"]] if instance["video_id"] in paths else None

        processed_path = data_path + ".processed"
        with open(processed_path, "w") as f:
            json.dump(data, f)

        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                gen_kwargs={"data_path": processed_path, "split": "train"},
            ),
            datasets.SplitGenerator(
                name=datasets.Split.VALIDATION,
                gen_kwargs={"data_path": processed_path, "split": "val"},
            ),
            datasets.SplitGenerator(
                name=datasets.Split.TEST,
                gen_kwargs={"data_path": processed_path, "split": "test"},
            ),
        ]

    def _generate_examples(self, data_path, split):
        """ Yields examples. """

        with open(data_path, "r", encoding="utf-8") as f:
            data = json.load(f)

            counter = 0
            for datum in data:
                for instance in datum["instances"]:
                    if instance["split"] == split and instance["video"] is not None:
                        yield counter, {
                            "video": instance["video"],
                            "url": instance["url"],
                            "start": instance["frame_start"],
                            "end": instance["frame_end"],
                            "fps": instance["fps"],
                            "signer_id": instance["signer_id"],
                            "bbox": instance["bbox"],
                            "gloss": datum["gloss"],
                            "gloss_variation": instance["variation_id"],
                        }
                    counter += 1
