# TiMIDIty

A simple package for playing MIDI files

## Installation

[Timidity](https://pypi.org/project/timidity/) is hosted on the official Python Package Index, so any tool like `pip` can be used to add timidity to your project.

`pip install timidity`

## Usage

You can run timidity without writing any code by typing `python -m timidity` into your console. This will search for any MIDI files in a directory called "songs" and list them for playback.

If you would like to integrate timidity into your script, the library has a simple interface for doing so.

Here is an example of how to use timidity in a script. This will play the MIDI file my_song.mid onto your speakers:

```python
from timidity import Parser, play_notes
import numpy as np

ps = Parser("my_song.mid")

play_notes(*ps.parse(), np.sin)
```
