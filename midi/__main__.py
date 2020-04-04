from midi.parser import parse_midi
from midi.player import play_notes
from glob import glob
from scipy.io import wavfile
import os
from scipy.signal import sawtooth, square


def run():
    midi_list = glob("songs/*.mid")

    i = 1
    for filename in midi_list:
        print(f"{i}.) {filename}")
        i += 1
    select_idx = int(input("Select a file: ")) - 1
    selection = midi_list[select_idx]

    notes, tpq, bpm = parse_midi(selection)
    audio, player = play_notes(notes, tpq, bpm, sawtooth)

    basename = os.path.splitext(os.path.basename(selection))[0]
    wavfile.write(f"wav/{basename}.wav", 44100, audio)

    player.wait_done()
    print("Done!")


if __name__ == "__main__":
    run()
