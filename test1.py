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

    time_data =  np.array([[float(item[0]), float(item[1])] for item in file_data[:,0:2]])

    (rows, _) = time_data.shape

    netspec = ["Series/net",
        ["SoundFileSource/src",
         "MixToMono/stm",
         "Windowing/window",
         "ShiftOutput/shift",
         "Spectrum/spec",
         "PowerSpectrum/pspec",
         "Chroma/chroma",
         #"Gain/dummy"
        ]]
    net = create(netspec)

    net.updControl("SoundFileSource/src/mrs_string/filename", fname2)
    net.updControl("Windowing/window/mrs_natural/zeroPadding", N)
    net.updControl("ShiftOutput/shift/mrs_natural/Interpolation", N)
    net.updControl("Windowing/window/mrs_natural/size", N)
    #net.updControl("Windowing/window/mrs_bool/zeroPhasing", MarControlPtr.from_bool(True))

    israte = net.getControl("mrs_real/israte").to_real()
    inSamples = net.getControl("mrs_natural/inSamples");

    chromas = np.array([])
    for row in time_data:
        nsamples = get_num_samples(row[1], row[0], israte)
        inSamples.setValue_natural(nsamples)
        #net.updControl("Windowing/window/mrs_natural/size", 2048*6)
        net.tick()
        chroma = control2array(net, "mrs_realvec/processedData")
        chromas = np.append(chromas, chroma)
        #print net.getControl("Spectrum/spec/mrs_natural/inSamples").to_natural()
        #print chroma
    chromas = chromas.reshape(12,np.size(chromas)/12)
    fig = plt.figure()
    plt.clf()
    ax = fig.add_subplot(111)
    #ax.set_aspect(1)
    #ax.imshow(chromas, cmap='Blues', interpolation='nearest')
    #import ipdb; ipdb.set_trace()
    #ax.imshow(chromas[:,1000:1200], interpolation='nearest')
    ax.pcolormesh(chromas)#, interpolation='nearest')
    plt.show()

def get_num_samples(x, y, srate):
    d_time = (x - y)
    nsamps = int(d_time*srate)
    return nsamps

if __name__ == "__main__":
    main()
