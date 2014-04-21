#!/usr/bin/env python

import sys
import numpy as np

from marsyas_util import create

def main():
    N = 2**12
    fname = sys.argv[1] #Text file
    fname2 = sys.argv[2] #Wav file

    with open(fname, 'r') as f:
        file_data = np.array([line.split() for line in f if len(line.split()) == 3])

    time_data =  [(float(item[0]), float(item[1]), item[2]) for item in file_data[:,0:3]]
    print time_data[1]

    netspec = ["Series/net",
        ["SoundFileSource/src",
         "MixToMono/stm",
         #"Windowing/window",
         "ShiftOutput/shift",
         "Spectrum/spec",
         "PowerSpectrum/pspec",
         "Spectrum2Chroma/chroma",
         "Inject/inj", # add extra sample to hold label
         "WekaSink/wekout"
        ]]
    net = create(netspec)

    net.updControl("SoundFileSource/src/mrs_string/filename", fname2)
    net.updControl("Windowing/window/mrs_natural/zeroPadding", N)
    net.updControl("ShiftOutput/shift/mrs_natural/Interpolation", N)
    #net.updControl("Windowing/window/mrs_natural/size", N)

    notes = [
        'A',  'B',  'C',  'D',  'E',  'F',  'G',
        'A#', 'B#', 'C#', 'D#', 'E#', 'F#', 'G#',
        'Ab', 'Bb', 'Cb', 'Db', 'Eb', 'Fb', 'Gb',
    ]
    quals = ['maj', 'min', 'aug', 'dim', 'sus2', 'sus4']
    labels = [note + ':' + qual for note in notes for qual in quals]
    labels.extend(['X', 'N'])
    net.updControl("WekaSink/wekout/mrs_natural/nLabels", len(labels))
    net.updControl("WekaSink/wekout/mrs_string/labelNames", ','.join(labels))
    net.updControl("WekaSink/wekout/mrs_string/filename", fname2.split('.')[0] + '.arff')

    israte = net.getControl("mrs_real/israte").to_real()
    inSamples = net.getControl("mrs_natural/inSamples");

    for row in time_data:
        nsamples = get_num_samples(row[1], row[0], israte)
        inSamples.setValue_natural(nsamples)
        net.updControl("WekaSink/wekout/mrs_string/labelNames", row[2])
        net.tick()

def get_num_samples(x, y, srate):
    d_time = (x - y)
    nsamps = int(d_time*srate)
    return nsamps

if __name__ == "__main__":
    main()
