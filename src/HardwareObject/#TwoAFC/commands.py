import nidaqmx as mx
from nidaqmx.constants import AcquisitionType
from nidaqmx import stream_readers
from nidaqmx import stream_writers

import time
import numpy as np
from time_handling import tic, wait, timestep
from sounds import Sound
import threading
import warnings



sample_rate = 50000

class HW_setup:
    def __init__(self, hw_rate) :
        self.speakers = []
        self.pumps = []
        self.lights = []
        self.motors = []
        self.piezos = []
        self.triggers = []



hw_setup = HW_setup(sample_rate)


class HW_element :
    def __init__(self,name) :
        self.name = name
        self.port = ''
        self.verbalize = False
        self.prepared = False
        
    def configure_port(self,port) :
        self.port = port
     
    def check_port(self) :
        if self.port == '' :
            print('No port provided for ' + self.name)
            return False
        return True        
        

class Pump(HW_element):
    def activate(self, duration) :
        if not self.check_port() :
            return
        
        with mx.Task() as pump_act :
            pump_act.do_channels.add_do_chan(self.port)
            
            pump_act.write(True)
            
            pump_act.wait_until_done()
            
            wait(duration)
        
            if self.verbalize :
                print("Activating " + self.name)
        

        
    def desactivate(self) :
        if not self.check_port() :
            return
        
        with mx.Task() as pump_desact :
            pump_desact.do_channels.add_do_chan(self.port)
            
            pump_desact.write(False)
        
            pump_desact.wait_until_done()
            
            if self.verbalize :
                print("Closing " + self.name)
    
        
class Light(HW_element):
    def prepare_tasks(self) :
        if not self.check_port() :
            return
        
        
        
        self.light_on = mx.Task()
        self.light_on.do_channels.add_do_chan(self.port)
        
        self.light_off = mx.Task()
        self.light_off.do_channels.add_do_chan(self.port)
    
        
        self.prepared = True
        
    def turnOn(self) :
        if not self.check_port() :
            return
        
        with mx.Task() as light_on :
            light_on.do_channels.add_do_chan(self.port)
            
            light_on.write(True)
            
            light_on.wait_until_done()
            
            if self.verbalize :
                print("Turning on " + self.name)
            
    def turnOff(self) :
        if not self.check_port() :
            return

        with mx.Task() as light_off :
            light_off.do_channels.add_do_chan(self.port)
            
            light_off.write(False)
            
            light_off.wait_until_done()
    
            if self.verbalize :
                print("Turning off " + self.name)

class Speaker(HW_element) :
    def play(self,sound) :
        if not self.check_port() :
            return
        
        if not isinstance(sound,Sound) :
            print('Need a correct Sound object to play sound')
            return

        sample = sound.waveform
        with mx.Task() as play_sound :
            play_sound.ao_channels.add_ao_voltage_chan(self.port)
            
            play_sound.timing.cfg_samp_clk_timing(sample_rate, samps_per_chan = int(sample_rate*sound.duration))
    
            print("Playing")
            
            play_sound.write(sample,auto_start=True)
            
            play_sound.wait_until_done()
            play_sound.write([0 for _ in range(sample_rate//100)],auto_start=True)
    
            play_sound.stop()
        



class Piezo(HW_element) :
    pass


detection_per_timestep = 5 # Number of time we check piezo on each trial logic timestep
lick_patience = 1  # Number of licks required on one side to be considered as the response
class Piezo_set() :
    def __init__(self, piezos):
        self.piezos = piezos
        self.lick_events = []
    
    
    def callback(self,task_handle, every_n_samples_event_type, number_of_samples, callback_data):
        
        l_event = self.task.read(detection_per_timestep)

        self.lick_events += l_event
        
        if True in l_event[0] : # Lick detected on piezo 1
            print("Lick detected on " + self.piezos[0].name)
            if self.onResponse :
                
                if self.lick_counts[0] < lick_patience : # If not enough licks increment lick counts to reach lick_patience
                    self.lick_counts[0] += 1
                    
                else : # Enough licks to be considered a response
                    warnings.simplefilter('ignore', ResourceWarning)
                    threading.Thread(target = self.current_trial.check_response, args = (1,), daemon=True).start() # Send the response 1 to the trial object to check what to do
            
        elif True in l_event[1] :  # Lick detected on piezo 2
            print("Lick detected on " + self.piezos[1].name)
            if self.onResponse :
                
                if self.lick_counts[1] < lick_patience :
                    self.lick_counts[1] += 1
                    
                else :
                    warnings.simplefilter('ignore', ResourceWarning)
                    threading.Thread(target = self.current_trial.check_response, args = (-1,), daemon=True).start() # Send the response -1 to the trial object to check what to do
                    
        
        


        return 0


    
    def detect_lick(self,duration, trial, isResponse = False) :
        
        self.lick_counts = [0,0] 
        
        self.onResponse = isResponse # Define if we detect licks during response window or not
        self.current_trial = trial
        
        self.lick_events = []
        
        with mx.Task() as d_task :
            self.task = d_task
    
            for piezo in self.piezos:
                if not piezo.check_port() :
                    return
    
                self.task.di_channels.add_di_chan(piezo.port)
            
            self.task.timing.cfg_samp_clk_timing(int(detection_per_timestep/timestep),sample_mode=AcquisitionType.CONTINUOUS,\
                                                     samps_per_chan = int(detection_per_timestep/timestep*duration))
            
    
            self.task.register_every_n_samples_acquired_into_buffer_event(detection_per_timestep, self.callback)  # Method to chack what to do depending on response
            
            self.task.start()
            
            #self.lick_events = self.task.read(int(detection_per_timestep/timestep*duration))
            
            wait(duration)
            
        output = self.lick_events.copy()
        self.lick_events = []
        
        return output  # Return lick events
        #print(len(self.lick_events))




    
    

class Motor(HW_element) :

    def activate(self) :
        if not self.check_port() :
            return
        
        with mx.Task() as act_motor :
            act_motor.do_channels.add_do_chan(self.port)
            
            act_motor.write(True)
            
            act_motor.wait_until_done()
        
    
    def desactivate(self) :
        if not self.check_port() :
            return
        
        with mx.Task() as desact_motor :
            desact_motor.do_channels.add_do_chan(self.port)
                
            desact_motor.write(False)
            
            desact_motor.wait_until_done()
        
        

class Trigger(HW_element) :
    def activate(self) :
        if not self.check_port() :
            return
        
        with mx.Task() as act_trigger :
            act_trigger.do_channels.add_do_chan(self.port)
            
            act_trigger.write(True)
            
            act_trigger.wait_until_done()
            
    def desactivate(self) :

        
        with mx.Task() as desact_trigger :
            desact_trigger.do_channels.add_do_chan(self.port)
            
            desact_trigger.write(False)
            
            desact_trigger.wait_until_done()

"""
class Tracker(HW_element) :
    def update(self,value) :
        if not self.check_port() :
            return
        
        with mx.Task() as update_v :
            update_v.ao_channels.add_ao_voltage_chan(self.port)
            
            update_v.write(value,auto_start=True)
            
            update_v.wait_until_done()
    
            update_v.stop()
"""
            
class Tracker(HW_element):
    def update(self, value):
        if not self.check_port() :
            return
        voltage = float(value) 
        
        with mx.Task() as update_v :
            update_v.ao_channels.add_ao_voltage_chan(self.port, min_val=0.0, max_val=5.0)
            
            update_v.write(voltage,auto_start=True)
            
            update_v.wait_until_done()

            update_v.stop()
        