from .parser import Note
import simpleaudio as sa
import numpy as np
from .envelopes import linear, ADSR


def get_freq(note):
    return (440. * (2 ** ((note - 69) / 12.)))


def get_note(t, wave, pitch, velocity):
    return wave(t * get_freq(pitch) * 2 * np.pi) * (velocity / 127.)


def play_notes(notes, ticks_per_quarter, bpm, wave, wait_done=True):

    sample_rate = 44100
    volume = 0.5

    def to_seconds(tick):
        return ((tick * 60) / (bpm * ticks_per_quarter))

    song_time = to_seconds(notes[-1].end)

    t = np.linspace(0., song_time, (int)(song_time * sample_rate), False)
    song = np.zeros_like(t)

    for idx, note in enumerate(notes):
        print("\rArranging notes... %d / %d" % (idx + 1, len(notes)), end='')
        start_pos = np.searchsorted(t, to_seconds(note.start))
        end_pos = np.searchsorted(t, to_seconds(note.end))

        note_t = t[start_pos:end_pos]
        envelope, release = ADSR(note_t, 0.5, 0.2, 0.7, 0.2)
        song[start_pos:end_pos] += get_note(note_t, wave,
                                            note.pitch, note.velocity) * envelope
    print()

    song = song / np.max(song)
    audio = (song * volume * (2 ** 15 - 1)).astype(np.int16)

    print("Playing song...")
    player = sa.play_buffer(audio, 1, 2, sample_rate)

    if wait_done:
        player.wait_done()

    return audio, player
