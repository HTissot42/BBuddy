import nidaqmx as mx
import numpy as np
import matplotlib.pyplot as plt
import os

""" ----- """
os.chdir("../BehaviourObject/HW")
from initialize import hw_setup

sample_rate = hw_setup.s_rate
""" ----- """

class PureTone:
    def __init__(self,amp, freq, duration, phase = 0) :
        self.amp = amp
        self.freq = freq
        self.duration = duration
        self.phase = phase
        
        T = np.linspace(0,duration,int(duration*sample_rate))

        self.waveform = amp*np.sin(2*np.pi*freq*T)

low_freq = PureTone(0.1,1,20)