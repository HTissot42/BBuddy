import nidaqmx as mx
import time
from time_handling import tic, wait, timestep
from sounds import Sound


sample_rate = 50000
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
            
            light_on.write(1)
            
            if self.verbalize :
                print("Turning on " + self.name)
                
    def turnOff(self) :
        if not self.check_port() :
            return
        
        with mx.Task() as light_off :
            light_off.do_channels.add_do_chan(self.port)
            
            light_off.write(1)
            
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
            play_sound.write([0 for _ in range(sample_rate)],auto_start=True)
    
            #print(len(sample) - succeed)
    
            play_sound.stop()
        

    
detect_rate = 1000
class Piezo(HW_element) :
    def detect_lick(self,duration) :
        if not self.check_port() :
            return
        
        with mx.Task() as d_lick :
            d_lick.di_channels.add_di_chan(self.port)
            d_lick.timing.cfg_samp_clk_timing(detect_rate)
    
            lick_events = d_lick.read(number_of_samples_per_channel = detect_rate*duration, auto_start = True)
        
        return lick_events


class HW_setup:
    def __init__(self, hw_rate) :
        self.speakers = []
        self.pumps = []
        self.lights = []
        self.piezos = []
        
        
        