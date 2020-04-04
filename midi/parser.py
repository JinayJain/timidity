from .util import get_bit, unset_bit
from .skips import midi_skips, meta_not_skips
from collections import namedtuple
import logging

Note = namedtuple('Note', ['pitch', 'velocity', 'start', 'end'])


class Parser:
    def __init__(self, filename):
        self.filename = filename
        self.file = open(filename, "rb")
        self.notes = []
        self.open_notes = [{}] * 16
        self.bpm = 120
        print("Created MIDI parser on file %s" % filename)

    def __del__(self):
        self.file.close()

    def read_int(self, n):
        return int.from_bytes(self.file.read(n), 'big')

    def read_str(self, n):
        return str(self.file.read(n).decode('utf-8'))

    def peek(self, n):
        ret = self.file.read(n)
        self.file.seek(self.file.tell() - n)
        return ret

    def read_var_int(self):
        ret = 0
        next_byte = True
        while next_byte:
            ret = ret << 7
            b = self.read_int(1)
            ret = ret + unset_bit(b, 7)
            next_byte = get_bit(b, 7)

        return ret

    def move(self, offset):
        self.file.seek(self.file.tell() + offset)

    def skip_bytes(self, n):
        if n == -1:
            n = self.read_var_int()

        self.move(n)

    def event_midi(self, evt):
        evt_type = evt >> 4
        channel = evt & 0x0F

        if midi_skips.get(evt_type):
            self.skip_bytes(midi_skips.get(evt_type))
            return

        if evt_type == 0x8:  # Note Off
            note = self.read_int(1)
            vel = self.read_int(1)
            # assert(not self.open_notes[channel].get(note, (-1, 0))[0] == -1)
            start_time, vel = self.open_notes[channel][note]
            self.notes.append(Note(note, vel, start_time, self.time))
            self.open_notes[channel][note] = (-1, 0)
        elif evt_type == 0x9:  # Note On
            note = self.read_int(1)
            vel = self.read_int(1)

            logging.debug("Playing note %d at vel %d on channel %d" %
                          (note, vel, channel))
            if vel == 0:
                # assert(not self.open_notes[channel].get(
                #     note, (-1, 0))[0] == -1)

                # unpack note
                start_time, vel = self.open_notes[channel][note]
                self.notes.append(Note(note, vel, start_time, self.time))
                self.open_notes[channel][note] = (-1, 0)
            else:
                # assert(self.open_notes[channel].get(note, (-1, 0))[0] == -1)

                self.open_notes[channel][note] = (self.time, vel)

    def event_sysex(self, evt):
        raise Exception("Oh no it's a SysEx.")

    def event_meta(self, evt):
        evt_type = self.read_int(1)
        evt_len = self.read_var_int()

        if not evt_type in meta_not_skips:
            self.skip_bytes(evt_len)
            return

        if evt_type == 0x2F:
            self.end_of_track = True
            logging.debug("End of track.")
        elif evt_type == 0x51:
            micro_per_quarter = self.read_int(3)
            self.bpm = round(6.e7 / (float)(micro_per_quarter))
            print("BPM: %d" % self.bpm)
        elif evt_type == 0x58:
            self.time_sig = (self.read_int(1), 2 ** self.read_int(1))
            self.clocks_per_tick = self.read_int(1)  # no clue what this means
            assert(self.read_int(1) == 8)  # 8 32nd's per quarter
            print("Time Signature: %d / %d" % self.time_sig)
        else:
            raise Exception("Unhandled meta event %x" % evt_type)

    def parse(self):
        assert(self.read_str(4) == "MThd")
        assert(self.read_int(4) == 6)

        self.midi_fmt = self.read_int(2)
        self.n_tracks = self.read_int(2)

        div_read = self.read_int(2)
        assert(not get_bit(div_read, 15))

        self.ticks_per_quarter = div_read

        for i_track in range(self.n_tracks):
            self.time = 0
            assert(self.read_str(4) == "MTrk")
            track_len = self.read_int(4)
            # track_len = 128  # TODO REMOVE

            init_pos = self.file.tell()

            logging.debug("Reading track %d with length %d" %
                          (i_track, track_len))

            self.end_of_track = False
            while self.file.tell() - init_pos < track_len and not self.end_of_track:
                dt = self.read_var_int()
                self.time += dt
                evt = self.read_int(1)

                logging.debug('------')
                logging.debug("Deltatime: %d" % dt)
                logging.debug(hex(evt))

                if evt < 0x80:
                    assert(prev_status)
                    logging.debug("Running status: %s" % hex(prev_status))
                    self.move(-1)
                    self.event_midi(prev_status)
                elif evt < 0xF0:  # MIDI event
                    self.event_midi(evt)
                    prev_status = evt
                elif evt < 0xF7:  # SysEx event
                    self.event_sysex(evt)
                elif evt == 0xFF:  # Meta event
                    self.event_meta(evt)
                else:
                    logging.debug("Unknown event %x" % evt)

        logging.debug(self.open_notes)
        return (self.notes, self.ticks_per_quarter, self.bpm)


def parse_midi(filename: str):
    print("Playing MIDI file %s" % filename.split('/')[-1])  # jank
    ps = Parser(filename)
    notes, tpq, bpm = ps.parse()
    del ps

    return (notes, tpq, bpm)
