import numpy as np
from gen_stim import stims
import time
from commands import *
from initialize import hw_setup

timestep = 1/1000

def tic() :
    time.sleep(timestep)

def wait(duration) :
    if duration >= timestep :
        for t in range(duration//timestep) :
            tic()


speaker_to_display = hw_setup.speakers[0]

starting_window = [0,1]
stim_window = [1,3]
delay_window = [3,3]
response_window = [3,4]
ending_window = [4,5]

class TimeLine:
    def __init__(self, starting, stim, delay, response, ending) :
        self.starting = starting
        self.stim = stim
        self.delay = delay
        self.response = response
        self.ending = ending



class Trial:
    def __init__(self, numero, stim, timeline) :
        self.num = numero
        self.stim = stim
        self.identity = stim.istarget
        self.timeline = timeline
    
    
    def run_trial(self) :
        starting_period = self.timeline.starting[1] - self.timeline.starting[0]
        wait(starting_period)
        
        self.run_stim(speaker_to_display)
        
        delay_period = self.timeline.delay[1] - self.timeline.delay[0]
        wait(delay_period)
        
        self.run_response(spout_motors, detecting_piezos)
        
        ending_period = self.timeline.ending[1] - self.timeline.ending[0]
        wait(ending_period)
        
        
    
    def run_stim(self, speaker) :
        play_sound(self.stim, speaker)
        wait(stim.duration)
    
    
    def run_response(self, motors, piezos) :
        activate_motor(motors)
        detect_licks(piezos)
        response_duration = self.timeline.response[1] - self.timeline.response[0]
        wait(response_duration)
        
    
    
        


trials = []