import nidaqmx as mx
import numpy as np
import matplotlib.pyplot as plt
import os
from initialize import hw_rate

sample_rate = hw_rate

class Sound:
    def __init__(self, duration) :
        self.duration = duration



class PureTone(Sound):
    def __init__(self,amp, freq, duration, phase = 0) :
        self.amp = amp
        self.freq = freq
        self.duration = duration
        self.phase = phase
        
        T = np.linspace(0,duration,int(duration*sample_rate))

        self.waveform = amp*np.sin(2*np.pi*freq*T)
