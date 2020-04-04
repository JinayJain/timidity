from .parser import Note
import simpleaudio as sa
import numpy as np


def play_notes(notes, ticks_per_quarter, bpm, wave, wait_done=True):

    sample_rate = 44100
    volume = 0.5

    def to_seconds(tick):
        return ((tick * 60) / (bpm * ticks_per_quarter))

    def get_freq(note):
        return (440. * (2 ** ((note - 69) / 12.)))

    song_time = to_seconds(notes[-1].end)

    t = np.linspace(0., song_time, (int)(song_time * sample_rate), False)
    song = np.zeros_like(t)

    for idx, note in enumerate(notes):
        print("\rArranging notes... %d / %d" % (idx + 1, len(notes)), end='')
        start_pos = np.searchsorted(t, to_seconds(note.start))
        end_pos = np.searchsorted(t, to_seconds(note.end))

        song[start_pos:end_pos] += wave(
            t[start_pos:end_pos] * get_freq(note.pitch) * 2 * np.pi) * (note.velocity / 127.)

    print()

    song = song / np.max(song)
    audio = (song * (2 ** 15 - 1) * volume).astype(np.int16)

    print("Playing song...")
    player = sa.play_buffer(audio, 1, 2, sample_rate)

    if wait_done:
        player.wait_done()

    return audio, player
