"""Official script from SUPERB SD task.

Source: https://github.com/s3prl/s3prl/blob/master/s3prl/downstream/diarization/make_rttm.py

Some functions have been adapted.
"""
import argparse
import os

import h5py
import numpy as np
from scipy.signal import medfilt


FMT = "SPEAKER {:s} 1 {:7.2f} {:7.2f} <NA> <NA> {:s} <NA>"


def parse_args():
    parser = argparse.ArgumentParser(description="make rttm from decoded result")
    parser.add_argument("file_list_hdf5")
    parser.add_argument("out_rttm_file")
    parser.add_argument("--threshold", default=0.5, type=float)
    parser.add_argument("--frame_shift", default=160, type=int)  # originally: 256
    parser.add_argument("--subsampling", default=1, type=int)
    parser.add_argument("--median", default=1, type=int)
    parser.add_argument("--sampling_rate", default=16000, type=int)
    return parser.parse_args()


def read_predictions(path):
    data = h5py.File(path, "r")
    return data["T_hat"]


def extract_info_from_files(paths):
    for path in paths:
        session, _ = os.path.splitext(os.path.basename(path))
        predictions = read_predictions(path)
        yield session, predictions


def process(
    predictions, threshold=None, median=None, session=None, frame_shift=160, subsampling=1, sampling_rate=16000
):
    factor = frame_shift * subsampling / sampling_rate
    a = np.where(predictions[:] > threshold, 1, 0)
    if median > 1:
        a = medfilt(a, (median, 1))

    for spkid, frames in enumerate(a.T):
        frames = np.pad(frames, (1, 1), "constant")
        (changes,) = np.where(np.diff(frames, axis=0) != 0)
        for s, e in zip(changes[::2], changes[1::2]):
            yield (
                session,
                s * factor,
                (e - s) * factor,
                session + "_" + str(spkid),
            )


def generate_rttm_line(content):
    rttm_line = FMT.format(*content)
    return rttm_line


def generate_rttm_lines(filepaths, args):
    for session, predictions in extract_info_from_files(filepaths):
        for content in process(
            predictions,
            threshold=args.threshold,
            median=args.median,
            session=session,
            frame_shift=args.frame_shift,
            subsampling=args.subsampling,
            sampling_rate=args.sampling_rate,
        ):
            yield generate_rttm_line(content)


def main(args):
    filepaths = sorted([line.strip() for line in open(args.file_list_hdf5)])
    with open(args.out_rttm_file, "w") as wf:
        for rttm_line in generate_rttm_lines(filepaths, args):
            print(rttm_line, file=wf)


if __name__ == "__main__":
    args = parse_args()
    main(args)
