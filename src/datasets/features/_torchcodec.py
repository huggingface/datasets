from torchcodec.decoders import AudioDecoder as _AudioDecoder


class AudioDecoder(_AudioDecoder):
    def __getitem__(self, key: str):
        if key == "array":
            return self.get_all_samples().data
        elif key == "sampling_rate":
            return self.get_samples_played_in_range(0, 0).sample_rate
        elif hasattr(self, "__getitem__"):
            return super().__getitem__(key)
        else:
            raise TypeError("'torchcodec.decoders.AudioDecoder' object is not subscriptable")
