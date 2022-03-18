import os
from dataclasses import dataclass
from typing import List

import datasets
from datasets.tasks import AutomaticSpeechRecognition


logger = datasets.utils.logging.get_logger(__name__)


@dataclass
class AudioFolderConfig(datasets.BuilderConfig):
    """BuilderConfig for AudioFolder."""

    sampling_rate: int = 16_000
    # features: Optional[datasets.Features] = None
    # drop_labels: bool = False


class AudioFolder(datasets.GeneratorBasedBuilder):
    BUILDER_CONFIG_CLASS = AudioFolderConfig

    AUDIO_EXTENSIONS: List[str] = []  # definition at the bottom of the script
    # TRANSCRIPT_EXTENSIONS: List[str] = []  # definition at the bottom of the script

    def _info(self):
        return datasets.DatasetInfo(
            features=datasets.Features({
                "audio": datasets.Audio(sampling_rate=self.config.sampling_rate),
                "text": datasets.Value("string"),
                }
            )
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
            downloaded_transcript = dl_manager.download(transcript)
            downloaded_dirs = dl_manager.download_and_extract(archives)
            splits.append(
                datasets.SplitGenerator(
                    name=split_name,
                    gen_kwargs={
                        "files": [
                                     (file, downloaded_file) for file, downloaded_file in zip(files, downloaded_files)
                                 ],
                                 # [
                                 #     (None, dl_manager.iter_files(downloaded_dir)) for downloaded_dir in downloaded_dirs
                                 # ],
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
            if data_file_ext.lower() in self.AUDIO_EXTENSIONS:  # .txt is for transcription file
                files.append(data_file)
            elif os.path.split(data_file)[-1] == "transcripts.txt":
                transcript = data_file
            else:
                archives.append(data_file)
        assert len(archives) <= 1, "More than one data archive provided"

        return files, transcript, archives

    # @staticmethod
    def _read_transcript(self, transcript_filename):
        transcript = dict()
        with open(transcript_filename) as f:
            for line in f:
                audio_id, text = line.strip().split("\t")
                transcript[audio_id] = text

        return transcript

    def _generate_examples(self, files, transcript_file, archive_path, archive_files):

        if files and transcript_file:
            transcript = self._read_transcript(transcript_file)
            # transcript_path = os.path.join(data_dir, "transcripts.txt")

            file_idx = 0
            for file, downloaded_file_or_dir in files:
                audio_filename = os.path.split(file)[-1]
                audio_id, _ = os.path.splitext(audio_filename)
                yield file_idx, {
                    "audio": downloaded_file_or_dir,
                    "text": transcript[audio_id],
                }
                file_idx += 1

        else:  # archive is not None
            transcript = self._read_transcript(os.path.join(archive_path, "transcripts.txt"))

            file_idx = 0
            for file in archive_files:
                _, ext = os.path.splitext(file)
                filename = os.path.split(file)[-1]
                _id, ext = os.path.splitext(filename)
                if ext.lower() in self.AUDIO_EXTENSIONS:
                    yield file_idx, {
                        "audio": file,
                        "text": transcript[_id],
                    }
                    file_idx += 1


AudioFolder.AUDIO_EXTENSIONS = [
    ".wav",
    ".flac",
    ".mp3",
    ".opus",
]

AudioFolder.TRANSCRIPT_EXTENSIONS = [
    ".txt"
]