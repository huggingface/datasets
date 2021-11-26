import datasets
from datasets.tasks import AutomaticSpeechRecognition


_URL = "https://www.tensorflow.org/datasets/catalog/speech_commands"
_DATA_URL = "http://download.tensorflow.org/data/speech_commands_v0.02.tar.gz"
_DESCRIPTION = "dummy description"
_CITATION = "dummy citation"


class SpeechCommandsConfig(datasets.BuilderConfig):
    """BuilderConfig for SpeechCommands. """

    def __init__(self, *args, **kwargs):
        super(SpeechCommandsConfig, self).__init__(*args, **kwargs)  # version=datasets.Version("0.0.1")


class SpeechCommands(datasets.GeneratorBasedBuilder):
    # DEFAULT_WRITER_BATCH_SIZE = 256
    BUILDER_CONFIG = SpeechCommandsConfig()

    def _info(self):
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=datasets.Features(
                {
                    "file": datasets.Value("string"),
                    "audio": datasets.features.Audio(sampling_rate=16_000),  # TODO check sampling_rate
                    "label": datasets.ClassLabel(),
                    "speaker_id": datasets.Value("string"),
                    "utterance_id": datasets.Value("int8"),
                    "id": datasets.Value("string"),
                }
            ),
            # supervised_keys=("file", "text"),  #TODO
            homepage=_URL,
            citation=_CITATION,
            # TODO: transcription_column?
            task_templates=[AutomaticSpeechRecognition(audio_file_path_column="file")],
        )

    def _split_generators(self, dl_manager):
        pass

    def _generate_examples(self, **kwargs):
        pass
