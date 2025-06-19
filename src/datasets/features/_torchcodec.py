import numpy as np
from torchcodec.decoders import AudioDecoder as _AudioDecoder


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
