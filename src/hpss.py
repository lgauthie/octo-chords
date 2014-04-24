import numpy as np
import scipy
import scipy.signal
import sklearn.decomposition
import librosa.core
import scipy.io.wavfile as wave
import sys
import os
import librosa

# Vars
N_FFT = 2048
HOP_LENGTH = N_FFT / 4

# Load file
fn = sys.argv[1]
name, ext = os.path.splitext(fn)
out = name+'-h.wav'
print out

# HPSS
y, sr = librosa.load(fn,sr=None)
D = librosa.stft(y,n_fft=N_FFT,hop_length=HOP_LENGTH)
H, P = librosa.decompose.hpss(D, kernel_size=(23,31))
y_harmonic = librosa.istft(H,hop_length=HOP_LENGTH)
y_percussive = librosa.istft(P,hop_length=HOP_LENGTH)
librosa.output.write_wav('H.wav',y_harmonic,sr)
librosa.output.write_wav('P.wav',y_percussive,sr)
