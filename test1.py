#!/usr/bin/env python

import sys
import numpy as np
import matplotlib.pyplot as p
import time

import marsyas as mar
from marsyas import MarControlPtr
from marsyas_util import create
from marsyas_util import add
from marsyas_util import control2array

def main():
    fname = sys.argv[1] #Text file
    fname2 = sys.argv[2] #Wav file
    chord_data = []

    with open(fname, 'r') as f:
        file_data = np.array([line.split() for line in f if len(line.split()) == 3])

    time_data =  np.array([[float(item[0]), float(item[1])] for item in file_data[:,0:2]])
    chord_data = file_data[:,2:]

    # Get number of rows in time_data
    (rows, _) = time_data.shape

    #print rows
    #print cols

    #Testing
    #print time_data
    #print chord_data

    netspec = ["Series/net",
        ["SoundFileSource/src",
        "MixToMono/stm",
        "Spectrum/spec",
        "PowerSpectrum/pspec",
        "Chroma/chroma",
        "Gain/dummy"
         ]]
    net = create(netspec)

    #redundant_net = ["Series/redundant_net"]
    #redundant_net.addMarSystem(net)



    net.updControl("SoundFileSource/src/mrs_string/filename", fname2)

    israte = net.getControl("mrs_real/israte").to_real()
    inSamples = net.getControl("mrs_natural/inSamples");

    # Controls for Chroma
    #net.updControl("Chroma/mrs_natural/lowOctNum", ???)
    #net.updControl("Chroma/mrs_natural/highOctNum", ???)
    #net.updControl("Chroma/mrs_real/samplingFreq", ???)

    for row in time_data:
        nsamples = get_num_samples(row[1], row[0], israte)
        inSamples.setValue_natural(nsamples)
        net.tick()
        chroma = control2array(net, "Chroma/chroma/mrs_realvec/processedData")
        print chroma

def get_num_samples(x, y, srate):
    d_time = (x - y)
    nsamps = int(d_time*srate)
    return nsamps

"""
    while net.getControl("SoundFileSource/src/mrs_bool/hasData").to_bool():
        net.tick()
        chroma = control2array(net, "mrs_realvec/processedData")
        #print chroma
"""


if __name__ == "__main__":
    main()
