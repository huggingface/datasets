import os
from dataclasses import dataclass, field
from io import BytesIO
from pathlib import Path
from typing import TYPE_CHECKING, Any, ClassVar, Optional, Union

import numpy as np
import pyarrow as pa

from .. import config
from ..download.download_config import DownloadConfig
from ..table import array_cast
from ..utils.file_utils import is_local_path, xopen
from ..utils.py_utils import no_op_if_value_is_null, string_to_dict


if TYPE_CHECKING:
    from .features import FeatureType


@dataclass
class Midi:
    """Midi [`Feature`] to extract MIDI data from a MIDI file.

    Input: The Midi feature accepts as input:
    - A `str`: Absolute path to the MIDI file (i.e. random access is allowed).
    - A `pathlib.Path`: path to the MIDI file (i.e. random access is allowed).
    - A `dict` with the keys:

        - `path`: String with relative path of the MIDI file to the archive file.
        - `bytes`: Bytes content of the MIDI file.

      This is useful for parquet or webdataset files which embed MIDI files.

    - A `dict` with the keys:

        - `notes`: Array containing the MIDI notes data
        - `tempo`: Float corresponding to the tempo of the MIDI file
        - `resolution`: Integer corresponding to the ticks per quarter note

    Output: The Midi features output data as a dictionary with keys:

    - `notes`: Array containing the MIDI notes data (pitch, velocity, start_time, end_time)
    - `tempo`: Float corresponding to the tempo of the MIDI file
    - `resolution`: Integer corresponding to the ticks per quarter note
    - `instruments`: List of instrument information

    Args:
        decode (`bool`, defaults to `True`):
            Whether to decode the MIDI data. If `False`,
            returns the underlying dictionary in the format `{"path": midi_path, "bytes": midi_bytes}`.
        resolution (`int`, *optional*):
            Target resolution in ticks per quarter note. If `None`, the native resolution is used.

    Example:

    ```py
    >>> from datasets import load_dataset, Midi
    >>> ds = load_dataset("example/midi_dataset", split="train")
    >>> ds = ds.cast_column("midi", Midi())
    >>> ds[0]["midi"]
    {'notes': array([[60, 64, 0.0, 1.0], [62, 64, 1.0, 2.0]]), 'tempo': 120.0, 'resolution': 480, 'instruments': [{'program': 0, 'name': 'Acoustic Grand Piano'}]}
    ```
    """

    decode: bool = True
    resolution: Optional[int] = None
    id: Optional[str] = field(default=None, repr=False)
    # Automatically constructed
    dtype: ClassVar[str] = "dict"
    pa_type: ClassVar[Any] = pa.struct({"bytes": pa.binary(), "path": pa.string()})
    _type: str = field(default="Midi", init=False, repr=False)

    def __call__(self):
        return self.pa_type

    def encode_example(self, value: Union[str, bytes, bytearray, dict]) -> dict:
        """Encode example into a format for Arrow.

        Args:
            value (`str`, `bytes`,`bytearray`,`dict`):
                Data passed as input to Midi feature.

        Returns:
            `dict`
        """

        if value is None:
            raise ValueError("value must be provided")

        if isinstance(value, str):
            return {"bytes": None, "path": value}
        elif isinstance(value, Path):
            return {"bytes": None, "path": str(value.absolute())}
        elif isinstance(value, (bytes, bytearray)):
            return {"bytes": value, "path": None}
        elif "notes" in value:
            # Convert MIDI data to bytes
            midi_data = self._create_midi_from_data(value)
            buffer = BytesIO()
            midi_data.write(buffer)
            return {"bytes": buffer.getvalue(), "path": None}
        elif value.get("path") is not None and os.path.isfile(value["path"]):
            return {"bytes": None, "path": value.get("path")}
        elif value.get("bytes") is not None or value.get("path") is not None:
            # store the MIDI bytes, and path is used to infer the MIDI format using the file extension
            return {"bytes": value.get("bytes"), "path": value.get("path")}
        else:
            raise ValueError(
                f"A MIDI sample should have one of 'path' or 'bytes' but they are missing or None in {value}."
            )

    @classmethod
    def _create_midi_from_data(cls, value: dict) -> "pretty_midi.PrettyMIDI":
        """Create MIDI file from note data."""
        try:
            import pretty_midi
        except ImportError as err:
            raise ImportError("To support encoding MIDI data, please install 'pretty_midi'.") from err



        # Create piano instrument
        piano_program = pretty_midi.instrument_name_to_program('Acoustic Grand Piano')
        piano = pretty_midi.Instrument(program=piano_program)

        notes = value.get("notes", [])
        for note_data in notes:
            if len(note_data) >= 4:
                pitch, velocity, start, end = note_data[:4]
                note = pretty_midi.Note(
                    velocity=int(velocity),
                    pitch=int(pitch),
                    start=float(start),
                    end=float(end)
                )
                piano.notes.append(note)


        if "tempo" in value:
            midi = pretty_midi.PrettyMIDI(initial_tempo=value["tempo"])
        else:
            midi = pretty_midi.PrettyMIDI()

        midi.instruments.append(piano)

        return midi

    def decode_example(
        self, value: dict, token_per_repo_id: Optional[dict[str, Union[str, bool, None]]] = None
    ) -> dict:
        """Decode example MIDI file into MIDI data.

        Args:
            value (`dict`):
                A dictionary with keys:

                - `path`: String with relative MIDI file path.
                - `bytes`: Bytes of the MIDI file.
            token_per_repo_id (`dict`, *optional*):
                To access and decode
                MIDI files from private repositories on the Hub, you can pass
                a dictionary repo_id (`str`) -> token (`bool` or `str`)

        Returns:
            `dict`: Dictionary containing MIDI data with keys:
                - `notes`: Array of [pitch, velocity, start_time, end_time]
                - `tempo`: Float tempo value
                - `resolution`: Integer ticks per quarter note
                - `instruments`: List of instrument information
        """
        try:
            import pretty_midi
        except ImportError as err:
            raise ImportError("To support decoding MIDI data, please install 'pretty_midi'.") from err

        if not self.decode:
            raise RuntimeError("Decoding is disabled for this feature. Please use Midi(decode=True) instead.")

        path, bytes_data = (value["path"], value["bytes"]) if value["bytes"] is not None else (value["path"], None)
        if path is None and bytes_data is None:
            raise ValueError(f"A MIDI sample should have one of 'path' or 'bytes' but both are None in {value}.")

        midi = None
        if bytes_data is not None:
            midi = pretty_midi.PrettyMIDI(BytesIO(bytes_data))
        elif is_local_path(path):
            midi = pretty_midi.PrettyMIDI(path)
        else:
            token_per_repo_id = token_per_repo_id or {}
            source_url = path.split("::")[-1]
            pattern = (
                config.HUB_DATASETS_URL if source_url.startswith(config.HF_ENDPOINT) else config.HUB_DATASETS_HFFS_URL
            )
            source_url_fields = string_to_dict(source_url, pattern)
            token = token_per_repo_id.get(source_url_fields["repo_id"]) if source_url_fields is not None else None

            download_config = DownloadConfig(token=token)
            with xopen(path, "rb", download_config=download_config) as f:
                midi = pretty_midi.PrettyMIDI(BytesIO(f.read()))

        # Extract notes data
        notes = []
        for instrument in midi.instruments:
            for note in instrument.notes:
                notes.append([note.pitch, note.velocity, note.start, note.end])

        # Extract instrument information
        instruments = []
        for instrument in midi.instruments:
            instruments.append({
                "program": instrument.program,
                "name": pretty_midi.program_to_instrument_name(instrument.program)
            })

        # Get tempo
        tempo = 120.0  # Default tempo
        if midi.get_tempo_changes() is not None:
            tempo = midi.get_tempo_changes()[0]

        return {
            "notes": np.array(notes) if notes else np.empty((0, 4)),
            "tempo": tempo,
            "resolution": midi.resolution,
            "instruments": instruments,
            "path": path,
        }

    def flatten(self) -> Union["FeatureType", dict[str, "FeatureType"]]:
        """If in the decodable state, raise an error, otherwise flatten the feature into a dictionary."""
        from .features import Value

        if self.decode:
            raise ValueError("Cannot flatten a decoded Midi feature.")
        return {
            "bytes": Value("binary"),
            "path": Value("string"),
        }

    def cast_storage(self, storage: Union[pa.StringArray, pa.StructArray]) -> pa.StructArray:
        """Cast an Arrow array to the Midi arrow storage type.
        The Arrow types that can be converted to the Midi pyarrow storage type are:

        - `pa.string()` - it must contain the "path" data
        - `pa.binary()` - it must contain the MIDI bytes
        - `pa.struct({"bytes": pa.binary()})`
        - `pa.struct({"path": pa.string()})`
        - `pa.struct({"bytes": pa.binary(), "path": pa.string()})`  - order doesn't matter

        Args:
            storage (`Union[pa.StringArray, pa.StructArray]`):
                PyArrow array to cast.

        Returns:
            `pa.StructArray`: Array in the Midi arrow storage type, that is
                `pa.struct({"bytes": pa.binary(), "path": pa.string()})`
        """
        if pa.types.is_string(storage.type):
            bytes_array = pa.array([None] * len(storage), type=pa.binary())
            storage = pa.StructArray.from_arrays([bytes_array, storage], ["bytes", "path"], mask=storage.is_null())
        elif pa.types.is_binary(storage.type):
            path_array = pa.array([None] * len(storage), type=pa.string())
            storage = pa.StructArray.from_arrays([storage, path_array], ["bytes", "path"], mask=storage.is_null())
        elif pa.types.is_struct(storage.type) and storage.type.get_all_field_indices("notes"):
            storage = pa.array(
                [Midi().encode_example(x) if x is not None else None for x in storage.to_numpy(zero_copy_only=False)]
            )
        elif pa.types.is_struct(storage.type):
            if storage.type.get_field_index("bytes") >= 0:
                bytes_array = storage.field("bytes")
            else:
                bytes_array = pa.array([None] * len(storage), type=pa.binary())
            if storage.type.get_field_index("path") >= 0:
                path_array = storage.field("path")
            else:
                path_array = pa.array([None] * len(storage), type=pa.string())
            storage = pa.StructArray.from_arrays([bytes_array, path_array], ["bytes", "path"], mask=storage.is_null())
        return array_cast(storage, self.pa_type)

    def embed_storage(self, storage: pa.StructArray, token_per_repo_id=None) -> pa.StructArray:
        """Embed MIDI files into the Arrow array.

        Args:
            storage (`pa.StructArray`):
                PyArrow array to embed.

        Returns:
            `pa.StructArray`: Array in the Midi arrow storage type, that is
                `pa.struct({"bytes": pa.binary(), "path": pa.string()})`.
        """
        if token_per_repo_id is None:
            token_per_repo_id = {}

        @no_op_if_value_is_null
        def path_to_bytes(path):
            source_url = path.split("::")[-1]
            pattern = (
                config.HUB_DATASETS_URL if source_url.startswith(config.HF_ENDPOINT) else config.HUB_DATASETS_HFFS_URL
            )
            source_url_fields = string_to_dict(source_url, pattern)
            token = token_per_repo_id.get(source_url_fields["repo_id"]) if source_url_fields is not None else None
            download_config = DownloadConfig(token=token)
            with xopen(path, "rb", download_config=download_config) as f:
                return f.read()

        bytes_array = pa.array(
            [
                (path_to_bytes(x["path"]) if x["bytes"] is None else x["bytes"]) if x is not None else None
                for x in storage.to_pylist()
            ],
            type=pa.binary(),
        )
        path_array = pa.array(
            [os.path.basename(path) if path is not None else None for path in storage.field("path").to_pylist()],
            type=pa.string(),
        )
        storage = pa.StructArray.from_arrays([bytes_array, path_array], ["bytes", "path"], mask=bytes_array.is_null())
        return array_cast(storage, self.pa_type)
