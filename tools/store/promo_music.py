"""Synthesizes the promo video's music: a calm, warm loop written here, so no licence is involved.

76 BPM in D major, two bars per chord (Dmaj7, Bm7, Gmaj7, Asus), soft pad, a piano-like
arpeggio, a round bass, and a light kick and hat that enter on the second bar and leave
for the last seconds, when the video fades out. Used by promo_video.py; needs numpy.

    python3 tools/store/promo_music.py out.wav 31.5   # to listen to it alone
"""

import sys
import wave

import numpy as np

SR = 44100
BPM = 76
BEAT = 60 / BPM
BAR = 4 * BEAT
CHORDS = [  # (bass root, chord tones) as MIDI notes
    (50, [62, 66, 69, 73]),  # Dmaj7
    (47, [59, 62, 66, 69]),  # Bm7
    (43, [59, 62, 66, 67]),  # Gmaj7
    (45, [57, 62, 64, 69]),  # Asus
]
ARP = [0, 1, 2, 3, 2, 1, 2, 3]  # chord-tone index per eighth note, an octave up


def hz(midi: int) -> float:
    return 440.0 * 2 ** ((midi - 69) / 12)


def seconds(n: float) -> np.ndarray:
    return np.arange(int(n * SR)) / SR


def pluck(freq: float, dur: float, decay: float = 2.6) -> np.ndarray:
    """Piano-like note: a few harmonics, the higher ones dying faster."""
    t = seconds(dur)
    out = np.zeros_like(t)
    for k, amp in ((1, 1.0), (2, 0.42), (3, 0.16), (4, 0.07), (5, 0.03)):
        out += amp * np.sin(2 * np.pi * freq * k * t) * np.exp(-t * decay * k ** 0.6)
    return out * (1 - np.exp(-t / 0.004))


def pad(freqs: list[float], dur: float) -> np.ndarray:
    t = seconds(dur)
    out = np.zeros_like(t)
    for f in freqs:
        for detune in (0.9985, 1.0015):
            out += np.sin(2 * np.pi * f * detune * t) + 0.18 * np.sin(4 * np.pi * f * detune * t)
    env = np.minimum(1, t / 1.2) * np.minimum(1, (dur - t) / 1.2)
    return out * env * (1 + 0.05 * np.sin(2 * np.pi * 0.25 * t)) / len(freqs)


def kick() -> np.ndarray:
    t = seconds(0.4)
    f = 48 + 70 * np.exp(-t / 0.03)
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / 0.11)


def hat(rng: np.random.Generator) -> np.ndarray:
    t = seconds(0.06)
    return np.diff(rng.standard_normal(len(t) + 1)) * np.exp(-t / 0.012)


def add(track: np.ndarray, sound: np.ndarray, at: float, gain: float) -> None:
    i = int(at * SR)
    if i >= len(track):
        return
    n = min(len(sound), len(track) - i)
    track[i:i + n] += sound[:n] * gain


def reverb(x: np.ndarray, seed: int, length: float = 2.4) -> np.ndarray:
    rng = np.random.default_rng(seed)
    t = seconds(length)
    ir = rng.standard_normal(len(t)) * np.exp(-t / 0.55)
    ir[: int(0.012 * SR)] = 0  # a little pre-delay
    n = len(x) + len(ir)
    y = np.fft.irfft(np.fft.rfft(x, n) * np.fft.rfft(ir, n), n)[: len(x)]
    return y / (np.abs(ir).sum() ** 0.5 * 6)


def music(length: float) -> np.ndarray:
    """Stereo float array (n, 2) of `length` seconds, peak 0.8."""
    n = int(length * SR)
    rng = np.random.default_rng(7)
    tonal, piano, low, drums = (np.zeros(n) for _ in range(4))
    drums_end = length - 4.5
    bar = 0
    while bar * BAR < length:
        root, tones = CHORDS[(bar // 2) % len(CHORDS)]
        start = bar * BAR
        if bar % 2 == 0:
            add(tonal, pad([hz(m) for m in tones], 2 * BAR + 1.0), start, 0.22)
            add(low, pluck(hz(root - 12), 2 * BAR, decay=0.9), start, 0.5)
        for e in range(8):
            vel = 0.55 + 0.25 * (e % 4 == 0) + 0.05 * rng.standard_normal()
            add(piano, pluck(hz(tones[ARP[e]] + 12), 2.0), start + e * BEAT / 2, 0.16 * vel)
        if start + BAR <= drums_end and bar >= 1:
            for b in range(4):
                if b % 2 == 0:
                    add(drums, kick(), start + b * BEAT, 0.42)
                add(drums, hat(rng), start + b * BEAT + BEAT / 2, 0.05)
        bar += 1

    left = tonal + low + drums + piano * 0.85 + reverb(tonal + piano, 1) * 0.9
    right = tonal + low + drums + piano * 1.0 + reverb(tonal + piano, 2) * 0.9
    stereo = np.stack([left, right], axis=1)
    t = seconds(length)[:, None]
    stereo *= np.minimum(1, t / 1.5) * np.minimum(1, (length - t) / 2.5)  # fade in, fade out with the video
    return stereo / np.abs(stereo).max() * 0.8


def save(path: str, length: float) -> None:
    data = (music(length) * 32767).astype(np.int16)
    with wave.open(path, "wb") as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes(data.tobytes())


if __name__ == "__main__":
    save(sys.argv[1], float(sys.argv[2]))
