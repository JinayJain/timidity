import numpy as np
import matplotlib.pyplot as plt


def linear(t, initial: float, target: float):
    if(t.shape[0] == 0):
        return t
    assert(initial >= 0 and initial <= 1)
    assert(target >= 0 and target <= 1)
    x = np.linspace(0, 1, num=t.shape[0])
    return (x * (target - initial)) + initial


"""
    attack in ms
    decay in ms
    sustain from 0 to 1
    release in ms
"""


def ADSR(t, attack, decay, sustain, release):  # release not implemented YET
    assert(attack >= 0)
    assert(decay >= 0)
    assert(sustain >= 0)
    assert(release >= 0)

    adsr = np.zeros_like(t)

    t_base = t - np.min(t)
    attack_idx = np.searchsorted(t_base, attack)
    decay_idx = np.searchsorted(t_base, attack + decay)

    adsr[:attack_idx] = linear(t_base[:attack_idx], 0, 1)
    adsr[attack_idx:decay_idx] = linear(
        t_base[attack_idx:decay_idx], 1, sustain)
    adsr[decay_idx:] = sustain

    return adsr
