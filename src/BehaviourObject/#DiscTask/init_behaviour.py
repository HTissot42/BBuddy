import sys
import numpy as np
import random
import time
from time_handling import tic, wait, timestep
from gui_behaviour import b_query, unwrap

from init_stim import stims
from commands import Piezo_set
import threading

if 'init_hardware' in sys.modules.keys() :
    del sys.modules['init_hardware']

from init_hardware import hw_setup, right_pump_duration, left_pump_duration

pump_durations = [right_pump_duration,left_pump_duration]


var = b_query.variables.copy()
for i in range(len(var)) :
    var[i] = unwrap(var[i])
    
n_block, rep_per_block, trial_duration, light_window,\
stim_window, response_delay, response_window, one_motor, \
motor_mode, desactivate_mode, correction_p, first_light, switch_task = var



speaker_to_display = hw_setup.speakers[0]
delivering_pumps = hw_setup.pumps
spout_motors = hw_setup.motors
detecting_piezos = Piezo_set(hw_setup.piezos)
light_cues = hw_setup.lights
trial_trigger = hw_setup.triggers[0]

n_stim = len(stims)


ending_delay = trial_duration - response_window[-1]
motor_lapse = 0.4
patience = 0.25


if motor_mode == 'AtStart' :
    motor_lapse = 0



class Timeline:
    def __init__(self, duration, cue, stim, delay, response, ending) :
        self.duration = duration
        self.cue = cue
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
    def __init__(self, numero, stim, timeline, task = 0,isDummy = False) :
        self.num = numero
        self.stim = stim
        self.identity = int(2*stim.istarget - 1)
        self.timeline = timeline
        
        self.piezos = detecting_piezos
        
        
        self.response = 0
        self.rewarded = False
        
        self.checked = False
        self.correct = False
        
        
        self.task = task
        self.isDummy = isDummy
        
        self.flagged = False
        
        self.easy = False
        
        
        if first_light == 'NoLight' :
            self.light_cue = None
        else :
            if first_light == 'Blue':
                light_idx = task
            elif first_light == 'Red':
                light_idx = 1-task
            self.light_cue = light_cues[light_idx]
    
    
    def setup_motors(self, motor_config) :
        #Setup motors at each trial
        if motor_config : #Config = 1 (Only correct motor), = 0 both motors
            if self.task == 0 :
                self.motors = [spout_motors[int(not self.stim.istarget)]]
            else :
                self.motors = [spout_motors[int(self.stim.istarget)]]
            
            print('Easy trial')
            self.easy = True
        
        else :
            self.motors = spout_motors
            self.easy = False
                
        if motor_mode == 'AtStart' :
            for motor in self.motors :
                motor.activate()
            self.motors = []
                
        elif motor_mode == 'Never' :
            self.motors = []
        
    def run_trial(self) :
        self.response = 0
        self.rewarded = False
        
        self.checked = False
        self.correct = False
        
        
        self.start_time = time.time()
        
        if self.isDummy :
            print('This is a dummy trial')
        
        trial_trigger.activate()
        
        threading.Thread(target = self.run_light_cue, args = (self.light_cue,), daemon=True).start()
        
        
        starting_delay = self.timeline.stim[0] - self.timeline.cue[0]
        
        wait(starting_delay)
        
        print("stim at :" + str(time.time() - self.start_time))
        
        self.run_stim(speaker_to_display)
        
        wait(self.timeline.delay)
        
        print("response at :" + str(time.time() - self.start_time))
        
        threading.Thread(target = self.run_response, args = (self.motors,self.piezos), daemon=True).start()
        
        waiting_for_response = self.timeline.response[1] - self.timeline.response[0]
        
        wait(waiting_for_response)
        
        wait(self.timeline.ending)
        
        trial_trigger.desactivate()
        
        """
        if self.correct == False :
            if np.random.rand() <= correction_p :
                print('Correction trial added')
                return True
        else :
            return False
        """
        
        
    def run_light_cue(self, light) :
        
        if (light != None) & (not self.isDummy)  :
            light.turnOn()
            
            light_duration = self.timeline.cue[1] - self.timeline.cue[0] 
            
            wait(light_duration)
        
            
            light.turnOff()
        
        
    def run_stim(self, speaker) :
        
        stim_duration = self.timeline.stim[1] - self.timeline.stim[0]
        
        self.stim.duration = stim_duration
        
        if not self.isDummy :
            
            speaker.play(self.stim)
        
    
    def run_response(self, motors, piezos) :
        
        
        if not self.isDummy :
            for motor in motors :
                motor.activate()
            
        wait(motor_lapse)
        
        response_duration = self.timeline.response[1] - self.timeline.response[0] - motor_lapse
        
        
        if not self.isDummy :
            self.licks = piezos.detect_lick(response_duration, self, isResponse = True)
            
        else :
            wait(response_duration)
            self.response = random.randint(-1,1)
            self.rewarded = (random.randint(0,1) == 1)
        
        print(self.rewarded)
        if self.rewarded :
            wait(1.5)
        
        if not self.isDummy : 
            for motor in motors :
                motor.desactivate()
                
    def check_response(self, response) : 
    
        if int(self.identity) == response :
            print('Licked on correct side')
            
            if not self.checked :
                self.correct = True
                self.checked = True
                
                self.response = response
            
            if (not self.rewarded) :
                
                if (desactivate_mode == 'Both')&(not self.correct) :
                    pass
                
                else :
                    self.rewarded = True
                    
                    if self.correct :
                        pump_duration = pump_durations[int(response < 0)]
                    else :
                        
                        pump_duration = pump_durations[int(response < 0)]/5
                        
                    delivering_pumps[int(response < 0)].activate(pump_duration)
                    
                    print('Pump activated for ' + str(pump_duration) + ' s')
                    delivering_pumps[int(response < 0)].desactivate()
                
        else :
            print('Licked on incorrect side')
            
            self.motors[int((1-response)/2)].desactivate()

            
            if not self.checked :
                
                self.correct = False
                self.error_time = time.time()
                self.checked = True
                
                self.response = response
                
                if (desactivate_mode == 'Both') :
                    for motor in self.motors :
                        motor.desactivate()
    
        
                
        
            
timeline = Timeline(trial_duration,light_window,stim_window,response_delay,response_window,ending_delay)
timeline.compute_timeserie()

def block_stim_id() :
    stim_idx = np.array([[k for _  in range(int(rep_per_block))] for k in range(n_stim)])
    stim_idx = stim_idx.flatten()
    np.random.shuffle(stim_idx)
    return stim_idx

trials = []
for n in range(int(n_block)) :
    stim_idx = block_stim_id()
    block_trials = [Trial(n_stim*rep_per_block*n + i, stims[stim_idx[i]], timeline) for i in range(len(stim_idx))]
    trials.append(block_trials)

trials = np.array(trials).flatten()