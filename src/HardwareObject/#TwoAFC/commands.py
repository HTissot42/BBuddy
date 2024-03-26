import nidaqmx as mx
import time
from initialize import hw_rate
from sounds import *


sample_rate = hw_rate

def activate_pump(pump,duration) :
    with mx.Task() as pump_act :
        pump_act.do_channels.add_do_chan(pump.port)
        
        pump_act.write(1)
        
        if pump.verbalize :
            print("Activating " + pump.name + " for " + str(duration) + "s..")
        
        time.sleep(duration)
        
        pump_act.write(0)
        
        if pump.verbalize :
            print("Closing " + pump.name)
        

def turnOn_light(light):
    with mx.Task() as light_on :
        light_on.do_channels.add_do_chan(light.port)
        
        light_on.write(1)
        
        if light.verbalize :
            print("Turning on " + light.name)
        
        
        
def turnOff_light(light):
    with mx.Task() as light_off :
        light_off.do_channels.add_do_chan(light.port)
        
        light_off.write(1)
        
        if light.verbalize :
            print("Turning off " + light.name)
            
            
def play_sound(speaker,sound):
    if not isinstance(sound,Sound) :
        print('Need a correct Sound object to play sound')
        return
    if not isinstance(speaker,Speajer):
        print('Need a correct Speaker object to play sound')
        return
    
    sample = sound.waveform
    
    with mx.Task() as play_sound :
        play_sound.ao_channels.add_ao_voltage_chan(speaker.port)
        play_sound.timing.cfg_samp_clk_timing(sample_rate)
        
        play_sound.write(sample,auto_start=True)
        play_sound.wait_until_done()
        print("Playing")
        #print(sound.duration)
        #for k in range(sound.duration) :
            #print(k+1)
            #time.sleep(1)
        play_sound.stop()
        


        