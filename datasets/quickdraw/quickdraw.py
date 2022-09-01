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
"""Quickdraw dataset"""

import io
import json
import os
import struct
import textwrap
from datetime import datetime

import numpy as np

import datasets
from datasets.tasks import ImageClassification


_CITATION = """\
@article{DBLP:journals/corr/HaE17,
  author    = {David Ha and
               Douglas Eck},
  title     = {A Neural Representation of Sketch Drawings},
  journal   = {CoRR},
  volume    = {abs/1704.03477},
  year      = {2017},
  url       = {http://arxiv.org/abs/1704.03477},
  archivePrefix = {arXiv},
  eprint    = {1704.03477},
  timestamp = {Mon, 13 Aug 2018 16:48:30 +0200},
  biburl    = {https://dblp.org/rec/bib/journals/corr/HaE17},
  bibsource = {dblp computer science bibliography, https://dblp.org}
}
"""

_DESCRIPTION = """\
The Quick Draw Dataset is a collection of 50 million drawings across 345 categories, contributed by players of the game Quick, Draw!.
The drawings were captured as timestamped vectors, tagged with metadata including what the player was asked to draw and in which country the player was located.
"""

_HOMEPAGE = "https://quickdraw.withgoogle.com/data"

_LICENSE = "CC BY 4.0"

_NAMES = """\
aircraft carrier,airplane,alarm clock,ambulance,angel
animal migration,ant,anvil,apple,arm
asparagus,axe,backpack,banana,bandage
barn,baseball bat,baseball,basket,basketball
bat,bathtub,beach,bear,beard
bed,bee,belt,bench,bicycle
binoculars,bird,birthday cake,blackberry,blueberry
book,boomerang,bottlecap,bowtie,bracelet
brain,bread,bridge,broccoli,broom
bucket,bulldozer,bus,bush,butterfly
cactus,cake,calculator,calendar,camel
camera,camouflage,campfire,candle,cannon
canoe,car,carrot,castle,cat
ceiling fan,cell phone,cello,chair,chandelier
church,circle,clarinet,clock,cloud
coffee cup,compass,computer,cookie,cooler
couch,cow,crab,crayon,crocodile
crown,cruise ship,cup,diamond,dishwasher
diving board,dog,dolphin,donut,door
dragon,dresser,drill,drums,duck
dumbbell,ear,elbow,elephant,envelope
eraser,eye,eyeglasses,face,fan
feather,fence,finger,fire hydrant,fireplace
firetruck,fish,flamingo,flashlight,flip flops
floor lamp,flower,flying saucer,foot,fork
frog,frying pan,garden hose,garden,giraffe
goatee,golf club,grapes,grass,guitar
hamburger,hammer,hand,harp,hat
headphones,hedgehog,helicopter,helmet,hexagon
hockey puck,hockey stick,horse,hospital,hot air balloon
hot dog,hot tub,hourglass,house plant,house
hurricane,ice cream,jacket,jail,kangaroo
key,keyboard,knee,knife,ladder
lantern,laptop,leaf,leg,light bulb
lighter,lighthouse,lightning,line,lion
lipstick,lobster,lollipop,mailbox,map
marker,matches,megaphone,mermaid,microphone
microwave,monkey,moon,mosquito,motorbike
mountain,mouse,moustache,mouth,mug
mushroom,nail,necklace,nose,ocean
octagon,octopus,onion,oven,owl
paint can,paintbrush,palm tree,panda,pants
paper clip,parachute,parrot,passport,peanut
pear,peas,pencil,penguin,piano
pickup truck,picture frame,pig,pillow,pineapple
pizza,pliers,police car,pond,pool
popsicle,postcard,potato,power outlet,purse
rabbit,raccoon,radio,rain,rainbow
rake,remote control,rhinoceros,rifle,river
roller coaster,rollerskates,sailboat,sandwich,saw
saxophone,school bus,scissors,scorpion,screwdriver
sea turtle,see saw,shark,sheep,shoe
shorts,shovel,sink,skateboard,skull
skyscraper,sleeping bag,smiley face,snail,snake
snorkel,snowflake,snowman,soccer ball,sock
speedboat,spider,spoon,spreadsheet,square
squiggle,squirrel,stairs,star,steak
stereo,stethoscope,stitches,stop sign,stove
strawberry,streetlight,string bean,submarine,suitcase
sun,swan,sweater,swing set,sword
syringe,t-shirt,table,teapot,teddy-bear
telephone,television,tennis racquet,tent,The Eiffel Tower
The Great Wall of China,The Mona Lisa,tiger,toaster,toe
toilet,tooth,toothbrush,toothpaste,tornado
tractor,traffic light,train,tree,triangle
trombone,truck,trumpet,umbrella,underwear
van,vase,violin,washing machine,watermelon
waterslide,whale,wheel,windmill,wine bottle
wine glass,wristwatch,yoga,zebra,zigzag
"""
_NAMES = [name for line in _NAMES.strip().splitlines() for name in line.strip().split(",")]

_CONFIG_NAME_TO_BASE_URL = {
    "raw": "https://storage.googleapis.com/quickdraw_dataset/full/raw/{}.ndjson",
    "preprocessed_simplified_drawings": "https://storage.googleapis.com/quickdraw_dataset/full/binary/{}.bin",
    "preprocessed_bitmaps": "https://storage.googleapis.com/quickdraw_dataset/full/numpy_bitmap/{}.npy",
    "sketch_rnn": "https://storage.googleapis.com/quickdraw_dataset/sketchrnn/{}.npz",
    "sketch_rnn_full": "https://storage.googleapis.com/quickdraw_dataset/sketchrnn/{}.full.npz",
}


class Quickdraw(datasets.GeneratorBasedBuilder):
    """Quickdraw dataset"""

    VERSION = datasets.Version("1.0.0")

    BUILDER_CONFIGS = [
        datasets.BuilderConfig(name="raw", version=VERSION, description="The raw moderated dataset"),
        datasets.BuilderConfig(
            name="preprocessed_simplified_drawings",
            version=VERSION,
            description=textwrap.dedent(
                """\
            The simplified version of the dataset with the simplified vectors, removed timing information, and the data positioned and scaled into a 256x256 region.
            The simplification process was:
                1.Align the drawing to the top-left corner, to have minimum values of 0.
                2.Uniformly scale the drawing, to have a maximum value of 255.
                3.Resample all strokes with a 1 pixel spacing.
                4.Simplify all strokes using the Ramer-Douglas-Peucker algorithm with an epsilon value of 2.0.
                """
            ),
        ),
        datasets.BuilderConfig(
            name="preprocessed_bitmaps",
            version=VERSION,
            description="The preprocessed dataset where all the simplified drawings have been rendered into a 28x28 grayscale bitmap.",
        ),
        datasets.BuilderConfig(
            name="sketch_rnn",
            version=VERSION,
            description=textwrap.dedent(
                """\
                This dataset was used for training the Sketch-RNN model from the paper https://arxiv.org/abs/1704.03477.
                In this dataset, 75K samples (70K Training, 2.5K Validation, 2.5K Test) has been randomly selected from each category,
                processed with RDP line simplification with an epsilon parameter of 2.0
                """
            ),
        ),
        datasets.BuilderConfig(
            name="sketch_rnn_full",
            version=VERSION,
            description="Compared to the `sketch_rnn` config, this version provides the full data for each category for training more complex models.",
        ),
    ]

    DEFAULT_CONFIG_NAME = "preprocessed_bitmaps"

    def _info(self):
        if self.config.name == "raw":
            features = datasets.Features(
                {
                    "key_id": datasets.Value("string"),
                    "word": datasets.ClassLabel(names=_NAMES),
                    "recognized": datasets.Value("bool"),
                    "timestamp": datasets.Value("timestamp[us, tz=UTC]"),
                    "countrycode": datasets.Value("string"),
                    "drawing": datasets.Sequence(
                        {
                            "x": datasets.Sequence(datasets.Value("float32")),
                            "y": datasets.Sequence(datasets.Value("float32")),
                            "t": datasets.Sequence(datasets.Value("int32")),
                        }
                    ),
                }
            )
        elif self.config.name == "preprocessed_simplified_drawings":
            features = datasets.Features(
                {
                    "key_id": datasets.Value("string"),
                    "word": datasets.ClassLabel(names=_NAMES),
                    "recognized": datasets.Value("bool"),
                    "timestamp": datasets.Value("timestamp[us, tz=UTC]"),
                    "countrycode": datasets.Value("string"),
                    "drawing": datasets.Sequence(
                        {
                            "x": datasets.Sequence(datasets.Value("uint8")),
                            "y": datasets.Sequence(datasets.Value("uint8")),
                        }
                    ),
                }
            )
        elif self.config.name == "preprocessed_bitmaps":
            features = datasets.Features(
                {
                    "image": datasets.Image(),
                    "label": datasets.ClassLabel(names=_NAMES),
                }
            )
        else:  # sketch_rnn, sketch_rnn_full
            features = datasets.Features(
                {
                    "word": datasets.ClassLabel(names=_NAMES),
                    "drawing": datasets.Array2D(shape=(None, 3), dtype="int16"),
                }
            )
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=features,
            homepage=_HOMEPAGE,
            license=_LICENSE,
            citation=_CITATION,
            task_templates=[ImageClassification(image_column="image", label_column="label")]
            if self.config.name == "preprocessed_bitmaps"
            else None,
        )

    def _split_generators(self, dl_manager):
        base_url = _CONFIG_NAME_TO_BASE_URL[self.config.name]
        if not self.config.name.startswith("sketch_rnn"):
            files = dl_manager.download(
                {name: url for name, url in zip(_NAMES, [base_url.format(name) for name in _NAMES])}
            )
            return [
                datasets.SplitGenerator(
                    name=datasets.Split.TRAIN,
                    gen_kwargs={
                        "files": files,
                        "split": "train",
                    },
                ),
            ]
        else:
            files = dl_manager.download_and_extract(
                {name: url for name, url in zip(_NAMES, [base_url.format(name) for name in _NAMES])}
            )
            return [
                datasets.SplitGenerator(
                    name=datasets.Split.TRAIN,
                    gen_kwargs={
                        "files": files,
                        "split": "train",
                    },
                ),
                datasets.SplitGenerator(
                    name=datasets.Split.VALIDATION,
                    gen_kwargs={
                        "files": files,
                        "split": "valid",
                    },
                ),
                datasets.SplitGenerator(
                    name=datasets.Split.TEST,
                    gen_kwargs={
                        "files": files,
                        "split": "test",
                    },
                ),
            ]

    def _generate_examples(self, files, split):
        if self.config.name == "raw":
            idx = 0
            for _, file in files.items():
                with open(file, encoding="utf-8") as f:
                    for line in f:
                        example = json.loads(line)
                        example["timestamp"] = datetime.strptime(example["timestamp"], "%Y-%m-%d %H:%M:%S.%f %Z")
                        example["drawing"] = [{"x": x, "y": y, "t": t} for x, y, t in example["drawing"]]
                        yield idx, example
                        idx += 1
        elif self.config.name == "preprocessed_simplified_drawings":
            idx = 0
            for label, file in files.items():
                with open(file, "rb") as f:
                    while True:
                        try:
                            example = process_struct(f)
                            example["word"] = label
                            yield idx, example
                        except struct.error:
                            break
                        idx += 1
        elif self.config.name == "preprocessed_bitmaps":
            idx = 0
            for label, file in files.items():
                with open(file, "rb") as f:
                    images = np.load(f)
                    for image in images:
                        yield idx, {
                            "image": image.reshape(28, 28),
                            "label": label,
                        }
                        idx += 1
        else:  # sketch_rnn, sketch_rnn_full
            idx = 0
            for label, file in files.items():
                with open(os.path.join(file, f"{split}.npy"), "rb") as f:
                    # read entire file since f.seek is not supported in the streaming mode
                    drawings = np.load(io.BytesIO(f.read()), encoding="latin1", allow_pickle=True)
                    for drawing in drawings:
                        yield idx, {
                            "word": label,
                            "drawing": drawing,
                        }
                        idx += 1


def process_struct(fileobj):
    """
    Process a struct from a binary file object.

    The code for this function is borrowed from the following link:
    https://github.com/googlecreativelab/quickdraw-dataset/blob/f0f3beef0fc86393b3771cdf1fc94828b76bc89b/examples/binary_file_parser.py#L19
    """
    (key_id,) = struct.unpack("Q", fileobj.read(8))
    (country_code,) = struct.unpack("2s", fileobj.read(2))
    (recognized,) = struct.unpack("b", fileobj.read(1))
    (timestamp,) = struct.unpack("I", fileobj.read(4))
    (n_strokes,) = struct.unpack("H", fileobj.read(2))
    drawing = []
    for _ in range(n_strokes):
        (n_points,) = struct.unpack("H", fileobj.read(2))
        fmt = str(n_points) + "B"
        x = struct.unpack(fmt, fileobj.read(n_points))
        y = struct.unpack(fmt, fileobj.read(n_points))
        drawing.append({"x": list(x), "y": list(y)})

    return {
        "key_id": str(key_id),
        "recognized": recognized,
        "timestamp": datetime.fromtimestamp(timestamp),
        "countrycode": country_code.decode("utf-8"),
        "drawing": drawing,
    }
