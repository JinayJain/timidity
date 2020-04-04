def get_bit(x: int, n: int):
    return (x >> n) & 1


def unset_bit(x: int, n: int):
    return x & ~(1 << n)


def get_freq(note: int):
    return 440. * (2 ** ((note - 69.) / 12.))
