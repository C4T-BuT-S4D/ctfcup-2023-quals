#!/usr/bin/env python3

import math
import tempfile
import os
import sys
import json
import uuid
import subprocess
from dataclasses import dataclass

import librosa
import numpy as np
import pydub
import soundfile
from pydub.playback import play
from pydub.utils import make_chunks


@dataclass
class Sample:
    id: str
    audio: pydub.AudioSegment
    feature: np.ndarray
    letter: str


def split_recording(
    recording: pydub.AudioSegment, expected=10
) -> list[pydub.AudioSegment]:
    chunks = []
    is_silence = True
    for chunk in make_chunks(recording, 10):
        if math.isinf(chunk.dBFS):
            is_silence = True
        elif is_silence:
            chunks.append(chunk)
            is_silence = False
        else:
            chunks[-1] += chunk

    chunks = list(filter(lambda c: c.duration_seconds > 0.1, chunks))

    assert len(chunks) == expected, f"got {len(chunks)} chunks instead of {expected}"

    return chunks


def calc_feature(data, sr) -> np.ndarray:
    # return librosa.feature.mfcc(y=data, sr=sr, n_mfcc=64, hop_length=128, n_fft=512)
    return librosa.feature.chroma_cens(y=data, sr=sr, n_chroma=40, bins_per_octave=80)


def prepare_sample(
    recording: pydub.AudioSegment, new_sr=48000
) -> tuple[pydub.AudioSegment, np.ndarray]:
    with tempfile.NamedTemporaryFile(suffix=".wav") as f:
        recording.export(f.name, format="wav")
        data, sr = librosa.load(f.name, sr=new_sr)
        soundfile.write(f.name, data, sr, "PCM_16")
        mfcc = calc_feature(data, sr)
        return pydub.AudioSegment.from_wav(f.name), mfcc


def load_samples() -> list[Sample]:
    if not os.path.exists("samples"):
        return []

    handled = set()
    samples = []
    for file in os.listdir("samples"):
        id = file.split(".")[0]
        if id in handled:
            continue

        audio = pydub.AudioSegment.from_wav(f"samples/{id}.wav")
        data, sr = librosa.load(f"samples/{id}.wav")
        feature = calc_feature(data, sr)
        with open(f"samples/{id}.json") as f:
            data = json.load(f)

        samples.append(
            Sample(id=id, audio=audio, feature=feature, letter=data["letter"])
        )

    return samples


def next_recording() -> list[tuple[pydub.AudioSegment, np.ndarray]]:
    subprocess.check_call(["./env/bin/python3", "generate.py"])
    recording = pydub.AudioSegment.from_mp3("out.mp3")
    chunks = split_recording(recording)
    chunks = [prepare_sample(chunk) for chunk in chunks]
    return chunks


def find_closest_sample(
    samples: list[Sample], recording_sample_feature: np.ndarray
) -> tuple[Sample, float]:
    minimal, _ = librosa.sequence.dtw(samples[0].feature, recording_sample_feature)
    minimal = minimal[minimal.shape[0] - 1][minimal.shape[1] - 1]
    best_sample = samples[0]

    for sample in samples[1:]:
        cur, _ = librosa.sequence.dtw(sample.feature, recording_sample_feature)
        cur = cur[cur.shape[0] - 1][cur.shape[1] - 1]

        if cur < minimal:
            minimal = cur
            best_sample = sample

    return best_sample, minimal


def save_sample(sample: Sample):
    os.makedirs("samples", exist_ok=True)

    sample.audio.export(f"samples/{sample.id}.wav", format="wav")
    with open(f"samples/{sample.id}.json", "w") as f:
        json.dump({"letter": sample.letter}, f)

    print(f"Saved new sample {sample.id}")


def main() -> int:
    mode = sys.argv[1]
    if mode not in ["collect", "run"]:
        print(
            "First argument should be execution mode, either collect or run",
            file=sys.stderr,
        )
        return 1

    samples = load_samples()

    while True:
        recording_samples = next_recording()
        for recording_sample in recording_samples:
            if len(samples) == 0:
                print(
                    "No samples are collected yet, please fill in the first sample info"
                )

                play(recording_sample[0])
                letter = input("Sample letter: ")

                new_sample = Sample(
                    id=uuid.uuid4(),
                    audio=recording_sample[0],
                    feature=recording_sample[1],
                    letter=letter,
                )

                save_sample(new_sample)
                samples.append(new_sample)
            else:
                closest_sample, closest_dtw = find_closest_sample(
                    samples, recording_sample[1]
                )

                print(
                    f"Identified next recording as closest to {closest_sample.id} with dtw={closest_dtw}, letter {closest_sample.letter}"
                )

                if mode == "collect":
                    play(recording_sample[0])

                    correct = input("Is this really the same sample? ")
                    if correct == "y":
                        continue

                    letter = input("What is its actual letter? ")

                    new_sample = Sample(
                        id=uuid.uuid4(),
                        audio=recording_sample[0],
                        feature=recording_sample[1],
                        letter=letter,
                    )

                    save_sample(new_sample)
                    samples.append(new_sample)

    return 0


if __name__ == "__main__":
    sys.exit(main())
