import nidaqmx as mx
import numpy as np

sample_rate = 100000

class Sound:
    def __init__(self, duration) :
        self.duration = duration



class PureTone(Sound):
    def __init__(self,amp, freq, duration, phase = 0) :
        self.amp = amp
        self.freq = freq
        self.duration = duration
        self.phase = phase
        
        T = np.linspace(0,duration,sample_rate)
        self.waveform = amp*np.sin(2*np.pi*freq*T)
