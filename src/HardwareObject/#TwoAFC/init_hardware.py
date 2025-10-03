



import nidaqmx as mx
from commands import *
from gui_hardware import hw_query, unwrap

'''
###---###
hw_query.load_var_from_buffer(question, var_to_ask)

water_amount = var_to_ask[0]
###---###
'''

var = hw_query.variables.copy()
for i in range(len(var)) :
    var[i] = unwrap(var[i])

water_amount = var[0]
send_trig = var[1]


# Measured by Hugo the 21th of may 2025 (water)
right_pump_rate = 0.1  #mL/s
left_pump_rate = 0.1  #mL/s


right_pump_duration = water_amount/right_pump_rate
left_pump_duration = water_amount/left_pump_rate


#Spout setup : Left: 21 mm, Right: 20.6 mm 

card_ID = "Dev1/"





    
""" Enter the various hardware elements and corresponding ports"""
r_pump = Pump('Right pump')
l_pump = Pump('Left pump')

b_light = Light('Blue light')
r_light = Light('Red light')

r_pump.configure_port(card_ID+"port1/line5")
l_pump.configure_port(card_ID+"port1/line3")

b_light.configure_port(card_ID+"port0/line5")
r_light.configure_port(card_ID+"port1/line4")

speaker = Speaker('Speaker')

speaker.configure_port(card_ID+"ao1")

r_motor = Motor('Right motor')
l_motor = Motor('Left motor')

r_piezo = Piezo('Right Piezo')
l_piezo = Piezo('Left Piezo')

tracker = Tracker('Trial tracker')

r_motor.configure_port(card_ID+"port0/line7")
l_motor.configure_port(card_ID+"port1/line7")

r_piezo.configure_port(card_ID+"port0/line4")
l_piezo.configure_port(card_ID+"port0/line3")

if send_trig :
    tracker.configure_port(card_ID+"ao0")
    #tracker.prepare_task()

r_motor.desactivate()
l_motor.desactivate()

b_light.turnOff()
r_light.turnOff()

r_pump.desactivate()
l_pump.desactivate()

hw_setup.speakers = [speaker]
hw_setup.pumps = [r_pump, l_pump]
hw_setup.lights = [b_light, r_light]
hw_setup.motors = [r_motor, l_motor]
hw_setup.piezos = [r_piezo, l_piezo]
hw_setup.trackers = [tracker]

#for p in hw_setup.pumps :
#    p.prepare_tasks()

#for l in hw_setup.lights :
#    l.prepare_tasks()

#for m in hw_setup.motors :
#    m.prepare_tasks()
    


#hw_setup.elements = hw_setup.speakers + hw_setup.pumps + hw_setup.lights + hw_setup.motors + hw_setup.piezos 