import numpy as np
from tkinter import *
from tkinter import ttk, messagebox


n_block = 10
rep_per_block = 2

trial_duration = 5
starting_delay = 0
stim_window = [0,1]
response_delay = 0.5
response_window = [1.5,4]
ending_delay = trial_duration - response_window[-1]

one_motor = False

var_to_ask = [n_block, rep_per_block, trial_duration, starting_delay, \
              stim_window, response_delay, response_window, one_motor]
question =   ['Block number','Repetition per block','Trial duration','Starting delay', \
              'Stim window','Reponse delay','Response window','Motor for target only']
    
w_types =    ['Edit', 'Edit', 'Edit', 'Edit', \
              'Edit', 'Edit', 'Edit', 'CheckBox']




class Behaviour_query:
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
        
        n_block, rep_per_block, trial_duration, starting_delay, \
                      stim_window, response_delay, response_window, one_motor = self.variables
                      
        print(n_block)
        
b_query = Behaviour_query()

for v in range(len(var_to_ask)) :
    b_query.add_query(var_to_ask[v],question[v],w_types[v])

    