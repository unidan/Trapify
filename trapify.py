import numpy as np


CHUNK_SIZE = 2048

def split_phase_and_power(transform):
    """
    Takes the raw fourier transform and returns a tuple of (power, phase, scale_factor)
    Power is the absolute value of transform / scale_factor such that sum(power) = 1
    phase is the phase of each value in the transform
    """
    power = np.abs(transform)
    phase = np.angle(transform)
    scale_factor = np.max(power)
    if scale_factor == 0:
        return power, phase, 1
    else:
        return power / scale_factor, phase, scale_factor

def combine_phase_and_power(power, phase, scale_factor):
    """
    Combines the phase and power and scale factor components
    """
    return np.multiply(power, np.exp(1j * phase)) * scale_factor
    
def chunkify(song):
    """
    An iterable that returns the chunks of the fourier transform
    """
    assert len(song) >= CHUNK_SIZE * 2
    for i in xrange(0, len(song) - CHUNK_SIZE, CHUNK_SIZE):
        yield np.fft.rfft(song[i: i + CHUNK_SIZE])

def unchunkify(chunks):
    """
    Takes the cunks and recombines them
    """
    recreated_chunks = map(lambda x: np.fft.irfft(combine_phase_and_power(*x)), chunks)
    return np.concatenate(recreated_chunks)

def trapify(power):
    return power

def process(song):
    chunks = list(chunkify(song))
    split_chunks = map(split_phase_and_power, chunks)
    trapified = map(lambda c: (trapify(c[0]), c[1], c[2]), split_chunks)
    powers = map(lambda x: x[0], trapified)
    #plt.imshow(np.log(1+np.array(powers).T), cmap='hot', interpolation='bilinear')
    new_song = unchunkify(trapified)
    return new_song