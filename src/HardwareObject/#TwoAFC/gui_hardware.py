import numpy as np
from tkinter import *
from tkinter import ttk, messagebox


pump_duration = 0.15

var_to_ask = [pump_duration]
question =   ['Pump duration']
w_types =    ['Edit']



class Hardware_query:
    def __init__(self) :
        self.variables = []
        self.gui_fields = []
        self.widget = []
        self.completed = False
        
    def add_query(self, variable, question, w_type) :
        self.variables.append(variable)
        self.gui_fields.append([question,w_type])
    
    def load_parameters(self) :
        #print(self.widget)
        #print(self.widget[0].get())
        #for i in range(len(self.variables)) :
        #    self.variables[i] = self.widget[i].get()
            
        pump_duration = self.variables
            
hw_query = Hardware_query()

for v in range(len(var_to_ask)) :
    hw_query.add_query(var_to_ask[v],question[v],w_types[v])

    