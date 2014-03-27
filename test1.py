#!/usr/bin/env python
   
import sys
import numpy as np
import matplotlib.pyplot as p
import math as m

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
    			 "Spectrum/spec",
    			 "PowerSpectrum/pspec",
    			 "Chroma/chroma",
    			 ]]
    net = create(netspec)
    
    
    net.updControl("SoundFileSource/src/mrs_string/filename", fname2)
    israte = net.getControl("mrs_real/israte").to_real()
    
    # Controls for Chroma
    #net.updControl("Chroma/mrs_natural/lowOctNum", ???)
    #net.updControl("Chroma/mrs_natural/highOctNum", ???)
    #net.updControl("Chroma/mrs_real/samplingFreq", ???)
    
    times = [MarControlPtr.from_natural(int((r[1]-r[0])*israte)) for r in time_data]
    
       #create chorma out matrix
    for i, row in enumerate(time_data):
        d_time = row[1]-row[0]
    	nsamples = int(d_time*israte)
    	#print nsamples
    	net.updControl("mrs_natural/inSamples", MarControlPtr.from_natural(nsamples))
    	net.tick()
        #chroma = control2array(net, "mrs_realvec/processedData")
        #print chroma
    	
"""
    while net.getControl("SoundFileSource/src/mrs_bool/hasData").to_bool():
        net.tick()
        chroma = control2array(net, "mrs_realvec/processedData")
        #print chroma
""" 

if __name__ == "__main__":
    main()
