import copy

import numpy as np
import torch
from torchcodec.decoders import AudioDecoder as _AudioDecoder


class AudioDecoder(_AudioDecoder):
    _hf_torch = False

    def _hf_to_torch(self, **torch_tensor_kwargs):
        decoder = copy.copy(self)
        decoder._hf_torch = True
        decoder._hf_torch_kwargs = {
            name: value for name, value in torch_tensor_kwargs.items() if name in ("device", "dtype")
        }
        return decoder

    def __getitem__(self, key: str):
        if key == "array":
            y = self.get_all_samples().data
            if self._hf_torch:
                if y.ndim > 1:
                    y = torch.mean(y, dim=tuple(range(y.ndim - 1)))
                torch_tensor_kwargs = getattr(self, "_hf_torch_kwargs", {})
                return y.to(**torch_tensor_kwargs) if torch_tensor_kwargs else y
            y = y.cpu().numpy()
            return np.mean(y, axis=tuple(range(y.ndim - 1))) if y.ndim > 1 else y
        elif key == "sampling_rate":
            return self.get_samples_played_in_range(0, 0).sample_rate
        elif hasattr(super(), "__getitem__"):
            return super().__getitem__(key)
        else:
            raise TypeError("'torchcodec.decoders.AudioDecoder' object is not subscriptable")
