from timidity import Parser, play_notes
from scipy.signal import square

ps = Parser("solong.mid")

play_notes(*ps.parse(), square)
