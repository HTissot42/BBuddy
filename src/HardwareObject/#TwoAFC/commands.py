import nidaqmx as mx
from nidaqmx.constants import AcquisitionType
from nidaqmx import stream_readers
from nidaqmx import stream_writers

import time
import numpy as np
from time_handling import tic, wait, timestep
from sounds import Sound


sample_rate = 50000


class HW_setup:
    def __init__(self, hw_rate) :
        self.speakers = []
        self.pumps = []
        self.lights = []
        self.motors = []
        self.piezos = []



hw_setup = HW_setup(sample_rate)


class HW_element :
    def __init__(self,name) :
        self.name = name
        self.port = ''
        self.verbalize = False
        
    def configure_port(self,port) :
        self.port = port
     
    def check_port(self) :
        if self.port == '' :
            print('No port provided for ' + self.name)
            return False
        return True        
        

class Pump(HW_element):
    def activate(self,duration) :
        if self.port == '' :
            print('No port provided for ' + self.name)
            return
        with mx.Task() as pump_act :
            pump_act.do_channels.add_do_chan(self.port)
            
            pump_act.write(1)
            
            if self.verbalize :
                print("Activating " + self.name + " for " + str(duration) + "s..")
            
            wait(duration)
            
            pump_act.write(0)
            
            if self.verbalize :
                print("Closing " + self.name)
        
        
class Light(HW_element):
    def turnOn(self) :
        if not self.check_port() :
            return
        
        with mx.Task() as light_on :
            light_on.do_channels.add_do_chan(self.port)
            
            light_on.write(True)
            
            if self.verbalize :
                print("Turning on " + self.name)
                
    def turnOff(self) :
        if not self.check_port() :
            return
        
        with mx.Task() as light_off :
            light_off.do_channels.add_do_chan(self.port)
            
            light_off.write(False)
            
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
            
            play_sound.timing.cfg_samp_clk_timing(sample_rate, samps_per_chan = sample_rate*sound.duration)
    
            print("Playing")
            
            play_sound.write(sample,auto_start=True)
            play_sound.wait_until_done()
            play_sound.write([0 for _ in range(sample_rate//100)],auto_start=True)
    
            #print(len(sample) - succeed)
    
            play_sound.stop()
        



class Piezo(HW_element) :
    pass


detection_per_timestep = 5
class Piezo_set() :
    def __init__(self, piezos):
        self.piezos = piezos

    
    
    def callback(self,task_handle, every_n_samples_event_type, number_of_samples, callback_data):
        print("OK callback")
        l_event = self.task.read(int(detection_per_timestep))
        print(l_event)
        self.lick_events += l_event
        
        
        #if np.any(lick_events) == True :
         #   print("Lick detected on " + self.name)
          #  print(lick_events)
           # return 1
        #else :
        return 0


    
    
    def detect_lick(self,duration) :
        
        print('OK')
        self.lick_events = []
        with mx.Task() as d_task :
            self.task = d_task
            for piezo in self.piezos:
                if not piezo.check_port() :
                    return

                self.task.di_channels.add_di_chan(piezo.port)
            
            self.task.timing.cfg_samp_clk_timing(int(detection_per_timestep/timestep),sample_mode=AcquisitionType.CONTINUOUS,\
                                                     samps_per_chan = int(detection_per_timestep/timestep*duration))
            self.task.register_every_n_samples_acquired_into_buffer_event(detection_per_timestep, self.callback)
                
            self.task.start()
                
            wait(duration)
    
        return self.lick_events




    
    
    
class Motor(HW_element) :
    def activate(self) :
        if not self.check_port() :
            return
        
        with mx.Task() as act_motor :
            act_motor.do_channels.add_do_chan(self.port)
            
            act_motor.write(True)
            
    
    def desactivate(self) :
        if not self.check_port() :
            return
        
        with mx.Task() as des_motor :
            des_motor.do_channels.add_do_chan(self.port)
            
            des_motor.write(False)

        
        
        