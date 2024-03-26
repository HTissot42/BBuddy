import nidaqmx as mx
from commands import *
from HW_class import *


card_ID = "D0/"
hw_rate = 1000
        

hw_setup = HW_setup(hw_rate)


    
""" Enter the various hardware elements and corresponding ports"""
r_pump = Pump('Right pump')
l_pump = Pump('Left pump')

b_light = Light('Blue light')
r_light = Light('Red light')

r_pump.configure_port(card_ID+"port1/line5")
l_pump.configure_port(card_ID+"port1/line3")

b_light.configure_port(card_ID+"port0/line4")
r_light.configure_port(card_ID+"port2/line3")

speaker = Speaker('Speaker')


speaker.configure_port(card_ID+"ao1")
#speaker2.configure_port(card_ID+"ao1")


hw_setup.speakers.append([speaker])
hw_setup.pumps.append([r_pump, l_pump])
hw_setup.lights.append([b_light, r_light])
