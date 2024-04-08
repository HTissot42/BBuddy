import numpy as np
from sounds import PureTone
from gui_stim import load_var_from_buffer, var_to_ask, question


###---###

load_var_from_buffer(question, var_to_ask)


frequencies, target_pitch, boundary, amp, stim_set = var_to_ask


###---###


duration = 5

print(boundary)


stims = np.array([PureTone(amp,freq,duration) for freq in frequencies])

for s in stims:
    if target_pitch == 'High' :
        s.istarget = (s.freq >= boundary)
        
    elif target_pitch == 'Low' :
        s.istarget = (s.freq <= boundary)
        
    else :
        print('Target identity wrongly specified')
    


if (stim_set == 'All') :
    mask = np.array([True for s in stims])

elif (stim_set == 'TargetOnly') :
    mask = np.array([s.istarget for s in stims])
        
elif (stim_set == 'RefOnly')&(s.istarget) :
    mask = np.array([not s.istarget for s in stims])
    

stims = stims[mask]