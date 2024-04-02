import numpy as np
from tkinter import *
from tkinter import ttk, messagebox



frequencies = [800,2000,4400,10000]

var_to_ask = [frequencies]
question =   ['Sound frequencies']
    
w_types =    ['Edit']




class Stim_query:
    def __init__(self) :
        self.variables = []
        self.gui_fields = []
        self.widget = []
        self.completed = False
        
    def add_query(self, variable, question, w_type) :
        self.variables.append(variable)
        self.gui_fields.append([question,w_type])
    
    def load_parameters(self) :
        #for i in range(len(self.variables)) :
        #    self.variables[i] = self.widget[i].get()
            
        frequencies = self.variables
            
s_query = Stim_query()

for v in range(len(var_to_ask)) :
    s_query.add_query(var_to_ask[v],question[v],w_types[v])

    