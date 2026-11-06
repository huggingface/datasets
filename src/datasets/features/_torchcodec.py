import numpy as np
from torchcodec.decoders import AudioDecoder as _AudioDecoder


class AudioDecoder(_AudioDecoder):
    def __getitem__(self, key: str):
        if key == "array":
            y = self.get_all_samples().data.cpu().numpy()
            if y.ndim <= 1:
                return y
            requested_num_channels = getattr(self, "_hf_num_channels", None)
            # Backward compatibility: default behavior returns mono unless
            # num_channels was explicitly set to a multi-channel value.
            if requested_num_channels is None or requested_num_channels == 1:
                return np.mean(y, axis=tuple(range(y.ndim - 1)))
            return y
        elif key == "sampling_rate":
            return self.get_samples_played_in_range(0, 0).sample_rate
        elif hasattr(super(), "__getitem__"):
            return super().__getitem__(key)
        else:
            raise TypeError("'torchcodec.decoders.AudioDecoder' object is not subscriptable")
