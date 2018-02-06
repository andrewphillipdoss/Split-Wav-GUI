from scipy.io import wavfile
import os
import numpy as np
from tqdm import tqdm
from itertools import tee, chain
from settings import *

# set defaul parameters
window_duration = 0.2
step_duration = window_duration / 10.
output_filename_prefix = "Sample_"

def windows(signal, window_size, step_size):
    for start in xrange(0, len(signal), step_size):
        end = start + window_size
        if end >= len(signal):
            break
        yield signal[start:end]

# find the energy of a set of samples
def energy(samples):
    return np.sum(np.power(samples, 2.)) / float(len(samples))

# find where a binary signal goes from 0 to 1
def rising_edges(binary_signal):
    previous_value = 0
    index = 0
    for x in binary_signal:
        if x and not previous_value:
            yield index
        previous_value = x
        index += 1

# find where a binary signal goes from 1 to 0
def falling_edges(binary_signal):
    previous_value = 0
    index = 1
    for x in binary_signal:
        if x and not previous_value:
            yield index
        previous_value = x
        index += 1

def find_silence(silence_threshold, input_filename):
    name_iterator = 0
    print input_filename
    sample_rate, samples = input_data=wavfile.read(filename=input_filename, mmap=True)

    max_amplitude = np.iinfo(samples.dtype).max
    max_energy = energy([max_amplitude])

    window_size = int(window_duration * sample_rate)
    step_size = int(step_duration * sample_rate)

    signal_windows = windows(
        signal=samples,
        window_size=window_size,
        step_size=step_size
    )

    window_energy1, window_energy2 = tee(energy(w) / max_energy for w in tqdm(signal_windows, total=int(len(samples) / float(step_size))))

    window_above_threshold = (e > silence_threshold for e in window_energy1)
    window_below_threshold = (e < silence_threshold for e in window_energy2)

    # find times when wav is split
    end_cut_times = (r * step_duration for r in rising_edges(window_above_threshold))
    start_cut_times = (r * step_duration for r in falling_edges(window_below_threshold))

    #generator is iterated
    cut_times = sorted(chain(start_cut_times, end_cut_times))
    cut_samples = [int(t * sample_rate) for t in cut_times]

    # generate files for cut samples
    for i in xrange(1,len(cut_samples)-1,2):
        name_iterator = name_iterator + 1
        output_filepath = "{}_{:03d}.wav".format(
            os.path.join(output_dir, output_filename_prefix),
            name_iterator
        )
        start = cut_samples[i]
        stop = cut_samples[i+1]
        wavfile.write(
            filename = output_filepath,
            rate = sample_rate,
            data = samples[start:stop]
        )
