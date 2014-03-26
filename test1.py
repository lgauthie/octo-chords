#!/usr/bin/env python
   
import sys
import numpy as np
import matplotlib.pyplot as p

#import marsays as mar
from marsyas import MarControlPtr
from marsyas_util import create
from marsyas_util import control2array

def main():
    fname = sys.argv[1] #Text file
    fname2 = sys.argv[2] #Wav file
    chord_data = []
        
    with open(fname, 'r') as f:
        file_data = np.array([line.split() for line in f if len(line.split()) == 3])
    
    time_data =  file_data[:,0:2]
    chord_data = file_data[:,2:]
    
    #Testing
    #print time_data
    #print chord_data
    
    #Windows sizes given the beat information
    window_sizes = []
    
    netspec = ["Series/net",
    			["SoundFileSource/src", 
    			 "Windowing/win",
    			 "Spectrum/spec",
    			 "PowerSpectrum/pspec",
    			 "Chroma/chroma",
    			 ]]
    net = create(netspec)
    
    net.updControl("SoundFileSource/src/mrs_string/filename", fname2)
    
    # Controls for Chroma
    #net.updControl("Chroma/mrs_natural/lowOctNum", ???)
    #net.updControl("Chroma/mrs_natural/highOctNum", ???)
    #net.updControl("Chroma/mrs_real/samplingFreq", ???)

    while net.getControl("SoundFileSource/src/mrs_bool/hasData").to_bool():
        net.tick()
        chroma = control2array(net, "mrs_realvec/processedData")
        print chroma
    

if __name__ == "__main__":
    main()
