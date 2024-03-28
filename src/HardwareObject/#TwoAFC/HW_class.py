import nidaqmx as mx
from commands import *


class HW_element :
    def __init__(self,name) :
        self.name = name
        self.port = ''
        self.verbalize = False
        
    def configure_port(self,port) :
        self.port = port
        

class Pump(HW_element):
    def activate(self,duration) :
        if self.port == '' :
            print('No port provided for ' + pump.name)
            return
        commands.activate_pump(self,duration)
        
        
class Light(HW_element):
    def turnOn(self) :
        if self.port == '' :
            print('No port provided for ' + pump.name)
            return
        
        commands.turnOn_light(self)
    
    def turnOn(self) :
        if self.port == '' :
            print('No port provided for ' + pump.name)
            return
        
        commands.turnOff_light(self)

class Speaker(HW_element) :
    def play(self,sound) :
        play_sound(self,sound)
    
    
class Piezo(HW_element) :
    


class HW_setup:
    def __init__(self, hw_rate) :
        self.speakers = []
        self.pumps = []
        self.lights = []
        self.piezos = []
        