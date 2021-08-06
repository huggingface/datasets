"""Official evaluation script for SUPERB SD task.

Source: https://github.com/s3prl/s3prl/blob/master/s3prl/downstream/diarization/score.sh

Some functions have been adapted.
"""

from make_rttm import process


def evaluate(predictions, session=None, frame_shift=160, sampling_rate=16000, subsampling=1):

    for median in [1, 11]:
        for threshold in [0.3, 0.4, 0.5, 0.6, 0.7]:
            for content in process(
                predictions,
                threshold=threshold,
                median=median,
                session=session,
                frame_shift=frame_shift,
                subsampling=subsampling,
                sampling_rate=sampling_rate,
            ):
                yield content


def main():
    pass


if __name__ == "__main__":
    main()
