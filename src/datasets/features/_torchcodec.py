from pathlib import Path
from typing import Optional

import numpy as np
from torch import Tensor
from torchcodec.decoders import AudioDecoder as _AudioDecoder
from torchcodec.decoders import VideoDecoder as _VideoDecoder


class AudioDecoder(_AudioDecoder):
    def __getitem__(self, key: str):
        if key == "array":
            y = self.get_all_samples().data.cpu().numpy()
            return np.mean(y, axis=tuple(range(y.ndim - 1))) if y.ndim > 1 else y
        elif key == "sampling_rate":
            return self.get_samples_played_in_range(0, 0).sample_rate
        elif hasattr(super(), "__getitem__"):
            return super().__getitem__(key)
        else:
            raise TypeError("'torchcodec.decoders.AudioDecoder' object is not subscriptable")


class VideoDecoder(_VideoDecoder):
    def __init__(
        self,
        source,
        *args,
        audio_stream_index: Optional[int] = None,
        audio_sample_rate: Optional[int] = None,
        audio_num_channels: Optional[int] = None,
        **kwargs,
    ):
        # File-like sources have a single cursor, so a separate AudioDecoder
        # reading from the same object would stomp on the VideoDecoder's reads.
        # Read the bytes up-front so both decoders can be constructed from them.
        if not isinstance(source, (str, Path, bytes, Tensor)) and hasattr(source, "read"):
            if hasattr(source, "seek"):
                source.seek(0)
            source = source.read()
        super().__init__(source, *args, **kwargs)
        self._source = source
        self._audio_stream_index = audio_stream_index
        self._audio_sample_rate = audio_sample_rate
        self._audio_num_channels = audio_num_channels
        self._audio: Optional[AudioDecoder] = None
        self._audio_initialized = False

    @property
    def audio(self) -> Optional[AudioDecoder]:
        """An :class:`AudioDecoder` for the best audio stream in the same
        source, or ``None`` if the source has no audio stream or is a
        ``torch.Tensor`` (raw encoded bytes with no container).

        The decoder is created lazily on first access and cached.
        """
        if not self._audio_initialized:
            if not isinstance(self._source, Tensor):
                try:
                    self._audio = AudioDecoder(
                        self._source,
                        stream_index=self._audio_stream_index,
                        sample_rate=self._audio_sample_rate,
                        num_channels=self._audio_num_channels,
                    )
                except ValueError:
                    pass
            self._audio_initialized = True
        return self._audio
