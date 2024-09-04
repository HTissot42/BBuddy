import numpy as np
from sounds import PureTone, Tone_AM_modulated

from gui_stim import s_query, unwrap

###---###

var = s_query.variables.copy()
for i in range(len(var)) :
    var[i]=unwrap(var[i])


frequencies, am_rates ,target_pitch, boundary, amp, stim_set = var

###---###


duration = 5



stims = np.array([[Tone_AM_modulated(amp,freq,am,duration) for freq in frequencies] for am in am_rates])

stims = stims.flatten()

for s in stims:
    if target_pitch == 'High' :
        s.istarget = (s.freq >= boundary)
        
    elif target_pitch == 'Low' :
        s.istarget = (s.freq <= boundary)
        
    else :
        print('Target identity wrongly specified')
    

if (stim_set == 'TargetOnly') :
    mask = np.array([s.istarget for s in stims])
        
elif (stim_set == 'RefOnly') :
    mask = np.array([not s.istarget for s in stims])
    
else :
    mask = np.array([True for s in stims])
    
    
stims = stims[mask]
