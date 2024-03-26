import numpy as np
from sounds import *


target_pitch = "High"

amp = 1
duration = 1
boundary = 1000
frequencies = [200,600,2600,8000]

stims = np.array([PureTone(amp,freq,duration) for freq in frequencies])


for s in stims:
    if target_pitch == 'High' :
        s.istarget = (s.freq >= boundary)
    elif target_pitch == 'Low' :
        s.istarget = (s.freq <= boundary)
        
    else :
        print('Target identity wrongly specified')
