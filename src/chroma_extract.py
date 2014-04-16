#!/usr/bin/env python

import sys
import numpy as np
import matplotlib.pyplot as plt

from random import randrange

from marsyas import MarControlPtr
from marsyas_util import create
from marsyas_util import control2array

def main():
    N = 2**14
    fname = sys.argv[1] #Text file
    fname2 = sys.argv[2] #Wav file

    with open(fname, 'r') as f:
        file_data = np.array([line.split() for line in f if len(line.split()) == 3])

    time_data =  [(float(item[0]), float(item[1]), item[2]) for item in file_data[:,0:3]]
    print time_data[1]

    rows = len(time_data)

    netspec = ["Series/net",
        ["SoundFileSource/src",
         "MixToMono/stm",
         "Windowing/window",
         "ShiftOutput/shift",
         "Spectrum/spec",
         "PowerSpectrum/pspec",
         "Chroma/chroma",
         "Windowing/pad",
         "WekaSink/wekout"
        ]]
    net = create(netspec)

    net.updControl("SoundFileSource/src/mrs_string/filename", fname2)
    net.updControl("Windowing/window/mrs_natural/zeroPadding", N)
    net.updControl("ShiftOutput/shift/mrs_natural/Interpolation", N)
    net.updControl("Windowing/window/mrs_natural/size", N)
    #net.updControl("Windowing/window/mrs_bool/zeroPhasing", MarControlPtr.from_bool(True))

    # Pad to fix chroma output to arff, last chroma was missing as it was replaced by WekaSink with label
    net.updControl("", )

    net.updControl("WekaSink/wekout/mrs_string/filename", fname2.split('.')[0] + '.arff')
    net.updControl("WekaSink/wekout/mrs_natural/nLabels", 1)

    israte = net.getControl("mrs_real/israte").to_real()
    inSamples = net.getControl("mrs_natural/inSamples");

    chromas = np.array([])
    for row in time_data:
        nsamples = get_num_samples(row[1], row[0], israte)
        inSamples.setValue_natural(nsamples)
        net.updControl("WekaSink/wekout/mrs_string/labelNames", row[2])
        net.tick()
        #net.updControl("Windowing/window/mrs_natural/size", 2048*6)
        chroma = control2array(net, "mrs_realvec/processedData")
        print chroma.size
        #chromas = np.append(chromas, chroma)

        #print net.getControl("Spectrum/spec/mrs_natural/inSamples").to_natural()
        #print chroma
    chromas = chromas.reshape(12,np.size(chromas)/12)
    #fig = plt.figure()
    #plt.clf()
    #ax = fig.add_subplot(111)
    #ax.set_aspect(1)
    #ax.imshow(chromas, cmap='Blues', interpolation='nearest')
    #import ipdb; ipdb.set_trace()
    #ax.imshow(chromas[:,1000:1200], interpolation='nearest')
    #ax.pcolormesh(chromas)#, interpolation='nearest')
    #plt.show()

def get_num_samples(x, y, srate):
    d_time = (x - y)
    nsamps = int(d_time*srate)
    return nsamps

if __name__ == "__main__":
    main()
