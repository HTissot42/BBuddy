import nidaqmx as mx
from commands import *

card_ID = "D0/"





    
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

r_motor = Motor('Right motor')
l_motor = Motor('Left motor')

r_piezo = Piezo('Right Piezo')
l_piezo = Piezo('Left Piezo')

r_motor.configure_port(card_ID+"port0/line7")
l_motor.configure_port(card_ID+"port1/line7")

r_piezo.configure_port(card_ID+"port0/line5")
l_piezo.configure_port(card_ID+"port0/line3")

hw_setup.speakers = [speaker]
hw_setup.pumps = [r_pump, l_pump]
hw_setup.lights = [b_light, r_light]
hw_setup.motors = [r_motor, l_motor]
hw_setup.piezos = [r_piezo, l_piezo]