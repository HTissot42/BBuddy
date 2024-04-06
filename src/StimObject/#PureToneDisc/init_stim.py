import numpy as np
from sounds import PureTone
from gui_stim import load_var_from_buffer, var_to_ask, question


###---###

load_var_from_buffer(question, var_to_ask)


frequencies, target_pitch, boundary, amp, stim_set = var_to_ask


###---###


duration = 5



stims = [PureTone(amp,freq,duration) for freq in frequencies]

for s in stims:
    if target_pitch == 'High' :
        s.istarget = (s.freq >= boundary)
        
    elif target_pitch == 'Low' :
        s.istarget = (s.freq <= boundary)
        
    else :
        print('Target identity wrongly specified')
        
    if (stim_set == 'TargetOnly')&(not s.istarget) :
        stims.remove(s)
        
    elif (stim_set == 'RefOnly')&(s.istarget) :
        stims.remove(s)
        
stims = np.array(stims)