from marsyas import *
from marsyas_util import create
from marsyas_util import control2array
from marsyas_util import realvec2array
import sys

fn = sys.argv[1] # Filename, use mono wav
Fs = 44100.0     # Sampling rate

# Use BeatTimesSink ?
hpss = ["Series/hpss", ["SoundFileSource/src", "Gain/gain", "Spectrum/spec", "MedianFilter/mf"]]
hpss_net = create(hpss)
hpss_net.linkControl("mrs_string/filename", "SoundFileSource/src/mrs_string/filename")
hpss_net.updControl("SoundFileSource/src/mrs_string/filename", fn)
hpss_net.updControl("MedianFilter/mf/mrs_real/WindowSize", 1024)

# Extract features

# Output harmonic portion to wav
out = ["Series/output", [hpss_net, "SoundFileSink/dest"]]
out_net = create(out)
out_net.updControl("mrs_natural/inSamples", 512)
out_net.updControl("mrs_real/israte", 44100.0)
out_net.updControl("SoundFileSink/dest/mrs_string/filename", "H.wav")
