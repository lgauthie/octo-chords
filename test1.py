#!/usr/bin/env python
   
import sys
import numpy as np

#import marsays as mar
from marsyas import MarControlPtr
from marsyas_util import create
from marsyas_util import control2array

def main():
    fname = sys.argv[1]
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
    			["SoundFileSource/input", 
    			 "Windowing/win",
    			 "Spectrum/spec",
    			 "PowerSpectrum/pspec",
    			 "Chroma/chroma",
    			 ]]
    net = create(netspec)

    while True:
        net.tick()

if __name__ == "__main__":
    main()
