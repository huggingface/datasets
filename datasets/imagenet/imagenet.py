import os
import shutil

import datasets


_CITATION = """\
@article{imagenet15russakovsky,
    Author = {Olga Russakovsky and Jia Deng and Hao Su and Jonathan Krause and Sanjeev Satheesh and Sean Ma and Zhiheng Huang and Andrej Karpathy and Aditya Khosla and Michael Bernstein and Alexander C. Berg and Li Fei-Fei},
    Title = { {ImageNet Large Scale Visual Recognition Challenge} },
    Year = {2015},
    journal   = {International Journal of Computer Vision (IJCV)},
    doi = {10.1007/s11263-015-0816-y},
    volume={115},
    number={3},
    pages={211-252}
}
"""

_HOMEPAGE = "https://image-net.org/index.php"

_DESCRIPTION = """\
ILSVRC 2012, commonly known as 'ImageNet' is an image dataset organized according to the WordNet hierarchy. Each meaningful concept in WordNet, possibly described by multiple words or word phrases, is called a "synonym set" or "synset". There are more than 100,000 synsets in WordNet, majority of them are nouns (80,000+). In ImageNet, we aim to provide on average 1000 images to illustrate each synset. Images of each concept are quality-controlled and human-annotated. In its completion, we hope ImageNet will offer tens of millions of cleanly sorted images for most of the concepts in the WordNet hierarchy.
"""

_VAL_PREP_SCRIPT_IN1K = "https://raw.githubusercontent.com/soumith/imagenetloader.torch/master/valprep.sh"
_SYNSET_MAPPING_IN1K = "https://gist.githubusercontent.com/apsdehal/f27ebf7d594b5950c91ecf732c0aaf61/raw/0b4cd44dadf7385e6d656424911cf45a113685bc/imagenet_synsets.txt"  # noqa
_DEFAULT_CONFIG_NAME = "2012"


class ImagenetConfig(datasets.BuilderConfig):
    def __init__(
        self,
        name=_DEFAULT_CONFIG_NAME,
        val_prep_script=_VAL_PREP_SCRIPT_IN1K,
        synset_mapping=_SYNSET_MAPPING_IN1K,
        **kwargs,
    ):
        """Config for ImageNet dataset.

        Args:
            name (string, optional): keyword to identify the config. Defaults to _DEFAULT_CONFIG_NAME.
            val_prep_script (string, optional): URL or path to script used to prep val set. Defaults to _VAL_PREP_SCRIPT_IN1K.
            synset_mapping (string, optional): URL or path to synset mapping. Defaults to _SYNSET_MAPPING_IN1K.
        """
        kwargs.pop("version", None)
        super(ImagenetConfig, self).__init__(version=datasets.Version("1.0.0"), name=name, **kwargs)
        self.val_prep_script = val_prep_script
        self.synset_mapping = synset_mapping


class Imagenet(datasets.GeneratorBasedBuilder):
    BUILDER_CONFIG_CLASS = ImagenetConfig

    BUILDER_CONFIGS = [
        ImagenetConfig(
            name="2012",
            val_prep_script=_VAL_PREP_SCRIPT_IN1K,
            synset_mapping=_SYNSET_MAPPING_IN1K,
        ),
    ]

    IMAGE_EXTENSION = ".jpeg"

    @property
    def manual_download_instructions(self):
        return (
            "To use ImageNet you have to download it manually. Please download it from ("
            "https://www.kaggle.com/competitions/imagenet-object-localization-challenge/"
            "data?select=imagenet_object_localization_patched2019.tar.gz). You will "
            "need to login and download the `imagenet_object_localization_patched2019.tar.gz file. "
            "Don't extract the file and point the `datasets` library to the tar file by running "
            "`datasets.load_dataset('imagenet', "
            "data_dir='path/to/folder/imagenet_object_localization_patched2019.tar.gz')`"
        )

    def _info(self):
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=datasets.Features(
                {
                    "image": datasets.Image(),
                }
            ),
            homepage=_HOMEPAGE,
            citation=_CITATION,
        )

    def _prep_validation(self, data_dir, val_prep_script):
        with open(val_prep_script, "r", encoding="utf-8") as f:
            commands = f.readlines()

        for idx, command in enumerate(commands):
            command = command.strip()
            if "mkdir" in command:
                folder = command.split(" ")[-1]
                folder = os.path.join(data_dir, "val", folder)
                os.makedirs(folder, exist_ok=True)
            # mkdir will definitely happen before move in continuous incremental loop.
            elif "mv" in command:
                splits = command.split(" ")
                image_file = splits[1]
                folder = splits[2]
                dst_path = os.path.join(data_dir, "val", folder)
                if os.path.exists(os.path.join(dst_path, image_file)):
                    continue
                src_path = os.path.join(data_dir, "val", image_file)
                if not os.path.exists(src_path):
                    continue
                shutil.move(src_path, dst_path)

    def _build_class_mapping(self, synset_mapping):
        with open(synset_mapping, "r", encoding="utf-8") as f:
            lines = f.readlines()

        mapping = {}
        inverse_mapping = {}

        for line in lines:
            line = line.strip().split(" ", 1)
            # Handle cases of same classes occurring twice
            if line[1] in inverse_mapping:
                splits = line[1].split("_")
                key = splits[0]
                if len(splits) == 2:
                    count = int(splits[1])
                else:
                    count = 0

                mapping[line[0]] = f"{key}_{count + 1}"
                inverse_mapping[f"{key}_{count + 1}"] = 1
            else:
                mapping[line[0]] = line[1]
                inverse_mapping[line[1]] = 1

        return mapping

    def _split_generators(self, dl_manager):
        """Returns SplitGenerators."""
        data_dir = os.path.abspath(os.path.expanduser(dl_manager.extract(dl_manager.manual_dir)))

        if not os.path.exists(data_dir):
            raise FileNotFoundError(
                f"{data_dir} does not exist. Make sure you insert a manual dir via `datasets.load_dataset('matinf', data_dir=...)` that includes files unzipped from the MATINF zip. Manual download instructions: {self.manual_download_instructions}"
            )
        val_prep_script = dl_manager.download(self.config.val_prep_script)
        images_path = os.path.join(data_dir, "ILSVRC", "Data", "CLS-LOC")

        self._prep_validation(images_path, val_prep_script)

        class_mapping = None
        label_classes = sorted(os.listdir(os.path.join(images_path, "train")))

        if self.config.synset_mapping is not None:
            synset_mapping = dl_manager.download(self.config.synset_mapping)
            class_mapping = self._build_class_mapping(synset_mapping)
            label_classes = [class_mapping[label] for label in label_classes]

        self.class_mapping = class_mapping
        self.info.features = datasets.Features(
            {"image": datasets.Image(), "labels": datasets.ClassLabel(names=label_classes)}
        )

        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                gen_kwargs={"files": dl_manager.iter_files(os.path.join(images_path, "train"))},
            ),
            datasets.SplitGenerator(
                name=datasets.Split.VALIDATION,
                gen_kwargs={"files": dl_manager.iter_files(os.path.join(images_path, "val"))},
            ),
            datasets.SplitGenerator(
                name=datasets.Split.TEST,
                gen_kwargs={"files": dl_manager.iter_files(os.path.join(images_path, "test")), "no_labels": True},
            ),
        ]

    def _generate_examples(self, files, no_labels=False):
        """Yields examples."""
        idx = 0
        for file in files:
            _, file_ext = os.path.splitext(file)
            if file_ext.lower() == self.IMAGE_EXTENSION:
                output = {"image": file}

                if not no_labels:
                    output["labels"] = os.path.basename(os.path.dirname(file))
                    if self.class_mapping is not None:
                        output["labels"] = self.class_mapping[output["labels"]]
                else:
                    output["labels"] = -1

                yield idx, output
                idx += 1
