import glob
import os
from typing import List

import datasets
from datasets.tasks import AutomaticSpeechRecognition


logger = datasets.utils.logging.get_logger(__name__)


class AudioFolderConfig(datasets.BuilderConfig):
    """BuilderConfig for AudioFolder."""

    def __init__(self, *args, sampling_rate=None, transcripts_filename="transcripts.txt",  **kwargs):
        if not sampling_rate:
            raise ValueError("To load an audio dataset, you must provide the `sampling_rate` parameter. "
                             "For example: "
                             ">>> load_dataset(\"audiofolder\", data_dir=\"path/to/dir\", sampling_rate=16_000)")
        self.sampling_rate = sampling_rate
        self.transcripts_filename = transcripts_filename

        super(AudioFolderConfig, self).__init__(
            *args, **kwargs
        )


class AudioFolder(datasets.GeneratorBasedBuilder):
    BUILDER_CONFIG_CLASS = AudioFolderConfig

    AUDIO_EXTENSIONS: List[str] = []  # definition at the bottom of the script

    def _info(self):
        return datasets.DatasetInfo(
            features=datasets.Features(
                {
                    "audio": datasets.Audio(sampling_rate=self.config.sampling_rate),
                    "text": datasets.Value("string"),
                }
            ),
            task_templates=[AutomaticSpeechRecognition(audio_file_path_column="audio", transcription_column="text")],
        )

    def _split_generators(self, dl_manager):
        if not self.config.data_files:
            raise ValueError(f"At least one data file must be specified, but got data_files={self.config.data_files}")

        data_files = self.config.data_files
        splits = []

        for split_name, files in data_files.items():
            if isinstance(files, str):
                files = [files]
            files, transcript, archive = self._split_files_and_archives(files)
            downloaded_files = dl_manager.download(files)
            downloaded_transcript = dl_manager.download(transcript) if transcript else None
            downloaded_dir = dl_manager.download_and_extract(archive) if archive else None
            splits.append(
                datasets.SplitGenerator(
                    name=split_name,
                    gen_kwargs={
                        # for loading from local folder
                        "files": [(file, downloaded_file) for file, downloaded_file in zip(files, downloaded_files)],
                        "transcript_file": downloaded_transcript,
                        # for loading from archive
                        "archive_files": dl_manager.iter_files(downloaded_dir)
                    },
                )
            )

        return splits

    def _split_files_and_archives(self, data_files):
        files, archives, transcript = [], [], None
        for data_file in data_files:
            _, data_file_ext = os.path.splitext(data_file)
            if data_file_ext.lower() in self.AUDIO_EXTENSIONS:
                files.append(data_file)
            elif os.path.split(data_file)[-1] == self.config.transcripts_filename:
                transcript = data_file
            else:
                archives.append(data_file)
        if len(archives) > 1:
            raise ValueError("More than one data archive provided, cannot infer data structure")

        return files, transcript, archives[0] if archives else None

    def _generate_examples(self, files, transcript_file, archive_files):

        # from local directory
        if files and transcript_file:
            transcript = _read_transcript(transcript_file)

            file_idx = 0
            for file, downloaded_file_or_dir in files:
                audio_filename = os.path.split(file)[-1]
                audio_id, _ = os.path.splitext(audio_filename)
                yield file_idx, {
                    "audio": downloaded_file_or_dir,
                    "text": transcript[audio_id],
                }
                file_idx += 1

        # from archive
        else:  # archive is not None

            audio_data, transcript = dict(), None
            for file in archive_files:
                filename = os.path.split(file)[-1]
                if filename == self.config.transcripts_filename:
                    transcript = _read_transcript(file)
                file_id, file_ext = os.path.splitext(filename)
                if file_ext in self.AUDIO_EXTENSIONS:
                    audio_data[file_id] = file

            if not transcript:
                raise FileNotFoundError("Transcript file not found in provided archive.")

            file_idx = 0
            for file_id, file in audio_data.items():
                yield file_idx, {
                    "audio": file,
                    "text": transcript[file_id]
                }
                file_idx += 1


def _read_transcript(transcript_filename):
    transcript = dict()
    with open(transcript_filename) as f:
        for line in f:
            # TODO: remove extension just in case too
            audio_id, text = line.strip().split("\t")
            transcript[audio_id] = text

    return transcript


# TODO: get full list of extensions
AudioFolder.AUDIO_EXTENSIONS = [
    ".wav",
    ".flac",
    ".mp3",
    ".opus",
]
