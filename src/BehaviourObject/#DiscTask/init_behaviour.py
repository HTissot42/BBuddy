import numpy as np
import random
import time
from time_handling import tic, wait, timestep
from gui_behaviour import n_block, rep_per_block, trial_duration, starting_delay, \
              stim_window, response_delay, response_window

from init_hardware import hw_setup
from init_stim import stims
from commands import Piezo_set


speaker_to_display = hw_setup.speakers[0]
delivering_pumps = hw_setup.pumps
spout_motors = hw_setup.motors
detecting_piezos = Piezo_set(hw_setup.piezos)


n_stim = len(stims)

ending_delay = trial_duration - response_window[-1]
motor_lapse = 0.35
"""
###---###
n_block = 10
rep_per_block = 2

trial_duration = 5
starting_delay = 1
stim_window = [1,2]
response_delay = 0.5
response_window = [2.5,5]

###---###
"""

class Timeline:
    def __init__(self, duration, starting, stim, delay, response, ending) :
        self.duration = duration
        self.starting = starting
        self.stim = stim
        self.delay = delay
        self.response = response
        self.ending = ending
        
    def compute_timeserie(self) :
        
        T = np.linspace(0,self.duration,int(self.duration//timestep))
        
        stim_window = np.array([False for _ in range(len(T))])
        response_window = np.array([False for _ in range(len(T))])
        
        stim_window[(T >= self.stim[0])&(T <= self.stim[1])] = True
        response_window[(T >= self.response[0])&(T <= self.response[1])] = True
        
        self.stim_window = stim_window
        self.response_window = response_window
        self.times = T
        

class Trial:
    def __init__(self, numero, stim, timeline) :
        self.num = numero
        self.stim = stim
        self.identity = stim.istarget
        self.timeline = timeline
        self.rewarded = False
    
    def run_trial(self) :
        wait(self.timeline.starting)
        

        self.run_stim(speaker_to_display)
        
        wait(self.timeline.delay)
        
        self.run_response(spout_motors,detecting_piezos)
        
        wait(self.timeline.ending)
        
        
    
    def run_stim(self, speaker) :
        speaker.play(self.stim)
        #print(self.stim.duration)
        wait(self.stim.duration)
    
    
    def run_response(self, motors, piezos) :
        
        
        for motor in motors :
            motor.activate()
        
        wait(motor_lapse)
        
        response_duration = self.timeline.response[1] - self.timeline.response[0]
        
        piezos.detect_lick(response_duration, self, isResponse = True)
        

            
        for motor in motors :
            motor.desactivate()
            
    def check_response(self, response) : 
        print(int(self.identity))
        print(response)
        if int(self.identity) == response :
            print('Licked on correct side')
            if not self.rewarded :
                delivering_pumps[response].activate(0.2)
                delivering_pumps[response].desactivate()
                self.rewarded = True
        else :
            print('Licked on incorrect side')
            spout_motors[response].desactivate()
            
            
timeline = Timeline(trial_duration, starting_delay,stim_window,response_delay,response_window,ending_delay)
timeline.compute_timeserie()


def block_stim_id() :
    stim_idx = np.array([[k for _  in range(rep_per_block)] for k in range(n_stim)])
    stim_idx = stim_idx.flatten()
    np.random.shuffle(stim_idx)
    return stim_idx

trials = []
for n in range(n_block) :
    stim_idx = block_stim_id()
    block_trials = [Trial(n_stim*rep_per_block*n + i, stims[stim_idx[i]], timeline) for i in range(len(stim_idx))]
    trials.append(block_trials)

trials = np.array(trials).flatten()