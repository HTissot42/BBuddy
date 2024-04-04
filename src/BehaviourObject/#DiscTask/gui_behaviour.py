import numpy as np
from tkinter import *
from tkinter import ttk, messagebox

import csv
import os


b_f_path = os.path.dirname(__file__)



n_block = 10
rep_per_block = 2

trial_duration = 5
light_window = [0,2]
stim_window = [1,2]
response_delay = 0.5
response_window = [2.5,5]


one_motor = False
first_light = 'Blue'
switch_task = False

var_to_ask = [n_block, rep_per_block, trial_duration, light_window, \
              stim_window, response_delay, response_window, one_motor,\
                  first_light ,switch_task]
question =   ['Block number','Repetition per block','Trial duration', 'Light window', \
              'Stim window','Reponse delay','Response window','Motor for target only', \
                'Light for first task', 'Switch task']
    
w_types =    ['Edit', 'Edit', 'Edit', 'Edit', \
              'Edit', 'Edit', 'Edit', 'CheckBox', \
             'Choice Blue,Red,NoLight', 'CheckBox']


def unwrap(string) :
    isText = any(c.isalpha() for c in string)
    
    if isText :
        return string
    else :
        if ' ' in string :
        
            splitted_string = string.split()
            
            result = []
            for s in splitted_string :
                result.append(float(s))
                
            
            return result
        
        else :
            return float(string)
            
class Behaviour_query:
    def __init__(self) :
        self.variables = []
        self.gui_fields = []
        self.widget = []
        self.completed = False
        
    def add_query(self, variable, question, w_type) :
        self.variables.append(variable)
        self.gui_fields.append([question,w_type])
    
    def clear_widget(self) :
        self.widget = []
    
    def load_parameters(self) :
        #for i in range(len(self.variables)) :
        #    self.variables[i] = self.widget[i].get()
        
        n_block, rep_per_block, trial_duration, light_window,\
        stim_window, response_delay, response_window, one_motor, \
        first_light, switch_task = self.variables

        
        
        
        
        with open(b_f_path + '/behaviour_param_buffer.csv', 'w', newline='') as csvfile:
            fieldnames = question
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
            writer.writeheader()
            input_dict = {question[i]:self.variables[i] for i in range(len(self.variables))}
            writer.writerow(input_dict)


b_query = Behaviour_query()




def load_var_from_buffer() :
    with open(b_f_path + '/behaviour_param_buffer.csv',newline='') as csvfile:
        buffer_reader = csv.reader(csvfile, delimiter=',')
        
        c = 0
        for row in buffer_reader :
            if c == 0 :   
                title = row
            elif c == 1 :            
                value = row
            
            c += 1
        
        
        for t in title :
            idx = question.index(t)
            var_to_ask[idx] = unwrap(value[idx]) 



if os.path.isfile(b_f_path + '/behaviour_param_buffer.csv') :
    load_var_from_buffer()



for v in range(len(var_to_ask)) :
    b_query.add_query(var_to_ask[v],question[v],w_types[v])

    