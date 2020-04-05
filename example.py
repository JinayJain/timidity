from timidity import Parser, play_notes
from scipy.signal import square, sawtooth
import numpy as np
from scipy.io import wavfile

ps = Parser("songs/untitled_candid.mid")

audio, player = play_notes(*ps.parse(), sawtooth, wait_done=False)

wavfile.write("wav/example_output.wav", 44100, audio)

player.wait_done()
