import glob
import os
from typing import List

import datasets
from datasets.tasks import AutomaticSpeechRecognition


logger = datasets.utils.logging.get_logger(__name__)


class AudioFolderConfig(datasets.BuilderConfig):
    """BuilderConfig for AudioFolder."""

    def __init__(self, *args, sampling_rate, **kwargs):
        self.sampling_rate = sampling_rate

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
            files, transcript, archives = self._split_files_and_archives(files)
            downloaded_files = dl_manager.download(files)
            downloaded_transcript = dl_manager.download(transcript) if transcript else None
            downloaded_dirs = dl_manager.download_and_extract(archives)
            splits.append(
                datasets.SplitGenerator(
                    name=split_name,
                    gen_kwargs={
                        "files": [(file, downloaded_file) for file, downloaded_file in zip(files, downloaded_files)],
                        "transcript_file": downloaded_transcript,
                        "archive_path": downloaded_dirs[0] if downloaded_dirs else None,
                        "archive_files": dl_manager.iter_files(downloaded_dirs[0]) if downloaded_dirs else None,
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
            elif os.path.split(data_file)[-1] == "transcripts.txt":
                transcript = data_file
            else:
                archives.append(data_file)
        if len(archives) > 1:
            raise ValueError("More than one data archive provided, cannot infer data structure")

        return files, transcript, archives

    def _generate_examples(self, files, transcript_file, archive_path, archive_files):

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
            # assuming there is only one transcripts.txt file
            transcript_file = glob.glob(f"{archive_path}/**/*/transcripts.txt")[0]
            transcript = _read_transcript(transcript_file)

            file_idx = 0
            for file in archive_files:
                filename = os.path.split(file)[-1]
                _id, file_ext = os.path.splitext(filename)
                if file_ext.lower() in self.AUDIO_EXTENSIONS:
                    yield file_idx, {
                        "audio": file,
                        "text": transcript[_id],
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
