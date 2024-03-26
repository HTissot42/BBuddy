import nidaqmx as mx
from commands import *


card_ID = "D0/"
sample_rate = 1000


class HW_setup :
    def __init__(self,sample_rate) :
        self.s_rate = sample_rate


hw_setup = HW_setup(1000)

    
""" Enter the various hardware elements and corresponding ports """
r_pump = Pump('Right pump')
l_pump = Pump('Left pump')

b_light = Light('Blue light')
r_light = Light('Red light')

r_pump.configure_port(card_ID+"port1/line5")
l_pump.configure_port(card_ID+"port1/line3")

b_light.configure_port(card_ID+"port0/line4")
r_light.configure_port(card_ID+"port2/line3")

speaker1 = Speaker('Speaker 1')
speaker2 = Speaker('Speaker 2')

speaker1.configure_port(card_ID+"ao0")
speaker2.configure_port(card_ID+"ao1")

