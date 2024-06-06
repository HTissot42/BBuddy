import numpy as np
from tkinter import *
from tkinter import ttk, messagebox

              
import csv
import os


b_f_path = os.path.dirname(__file__)



question =   ['Block number','Repetition per block','Trial duration', 'Light window', \
              'Stim window','Reponse delay','Response window','Motor for target only',\
              'Motor activation', 'Motor desactivation','Light for first task', 'Switch task']
    

var_to_ask = [20, 1, 7,  [0,2], \
              [1,2], 0.5, [2.5,6], False,\
              'Always','IncorrectOnly','Blue', False]

"""
v_types =  [int, int, float,  list, \
              list, float, list, bool,\
                 str, bool]
"""

w_types =    ['Edit', 'Edit', 'Edit', 'Edit', \
              'Edit', 'Edit', 'Edit', 'CheckBox',\
              'Choice AtStart,Always','Choice IncorrectOnly,Both','Choice Blue,Red,NoLight', 'CheckBox']


def unwrap(string) :
    if (type(string) == int) or (type(string) == float) :
        return string
    
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
    
    def load_parameters(self, name) :
        for i in range(len(self.variables)) :
            self.variables[i] = self.widget[i].get()
        """
        n_block, rep_per_block, trial_duration, light_window,\
        stim_window, response_delay, response_window, one_motor, \
        first_light, switch_task = self.variables
        """
        
        #print(trial_duration)
        
        
        with open(b_f_path + '/Buffer/behaviour_param_buffer_' + name + '.csv', 'w', newline='') as csvfile:
            fieldnames = question
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
            writer.writeheader()
            input_dict = {question[i]:self.variables[i] for i in range(len(self.variables))}
            writer.writerow(input_dict)
    
    
    def load_var_from_buffer(self, name, label = question, var = var_to_ask) :
        if os.path.isfile(b_f_path + '/Buffer/behaviour_param_buffer_' + name + '.csv') :
            with open(b_f_path + '/Buffer/behaviour_param_buffer_' + name + '.csv',newline='') as csvfile:
                buffer_reader = csv.reader(csvfile, delimiter=',')
                
                c = 0
                for row in buffer_reader :
                    if c == 0 :   
                        title = row
                    elif c == 1 :            
                        value = row
                    
                    c += 1
                
                i = 0
                for t in title :
                    idx = label.index(t)
                    var[idx] = unwrap(value[i])
                    i+=1
                    
            self.build_queries()

    def build_queries(self) :
        self.variables = []
        self.gui_fields = []
        
        for v in range(len(var_to_ask)) :
            b_query.add_query(var_to_ask[v],question[v],w_types[v])
        
    
b_query = Behaviour_query()
b_query.build_queries()




    





    