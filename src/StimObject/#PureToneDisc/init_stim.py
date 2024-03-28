import numpy as np
from sounds import PureTone


target_pitch = "High"

amp = 0.1
duration = 2
boundary = 1000
frequencies = [400,1000,4000,10000]

stims = np.array([PureTone(amp,freq,duration) for freq in frequencies])


for s in stims:
    if target_pitch == 'High' :
        s.istarget = (s.freq >= boundary)
    elif target_pitch == 'Low' :
        s.istarget = (s.freq <= boundary)
        
    else :
        print('Target identity wrongly specified')
