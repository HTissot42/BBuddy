import nidaqmx as mx
import numpy as np

sample_rate = 50000

class Sound:
    def __init__(self, duration) :
        self.duration = duration
        self.istarget = None



class PureTone(Sound):
    def __init__(self,amp, freq, duration, phase = 0) :
        self.amp = amp
        self.freq = freq
        self.phase = phase
        
        super().__init__(duration)
        
        T = np.linspace(0,duration,sample_rate)
        self.waveform = amp*np.sin(2*np.pi*freq*T)

class Tone_AM_modulated(Sound) :
    def __init__(self,amp, freq, am_rate, duration, phase = 0) :
        self.amp = amp
        self.freq = freq
        self.am_rate = am_rate
        self.phase = phase
        
        super().__init__(duration)
        
        T = np.linspace(0,duration,sample_rate*duration)
        self.waveform = amp*np.cos(2*np.pi*am_rate*T)*np.sin(2*np.pi*freq*T)