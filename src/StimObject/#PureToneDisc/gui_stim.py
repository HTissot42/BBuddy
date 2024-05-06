import numpy as np
from tkinter import *
from tkinter import ttk, messagebox
import os
import csv


s_f_path = os.path.dirname(__file__)

frequencies = [750,1500,3000,6000]
am_rates = [4,6,9,13.5]
target_pitch = 'Low'
boundary = 2000
amp = 0.01
stim_set = "All"

var_to_ask = [frequencies, am_rates, target_pitch, boundary, amp, stim_set]
question =   ['Sound frequencies', 'AM rates', 'Target', 'Category boundary', 'Amplitude (0.1 max)', 'Stim set']
    
w_types =    ['Edit', 'Edit', 'Choice High,Low', 'Edit', 'Edit', 'Choice All,TargetOnly,RefOnly']

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


class Stim_query:
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
        #for i in range(len(self.variables)) :
        #    self.variables[i] = self.widget[i].get()
            
        #frequencies, target_pitch = self.variables
            
        
        with open(s_f_path + '/Buffer/stim_param_buffer_' + name+ '.csv', 'w', newline='') as csvfile:
            fieldnames = question
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
            writer.writeheader()
            input_dict = {question[i]:self.variables[i] for i in range(len(self.variables))}
            writer.writerow(input_dict)
                
                
        
    def load_var_from_buffer(self, name, label=question, var=var_to_ask) :
        if os.path.isfile(s_f_path + '/Buffer/stim_param_buffer_' + name + '.csv') :
            with open(s_f_path + '/Buffer/stim_param_buffer_' + name + '.csv',newline='') as csvfile:
                buffer_reader = csv.reader(csvfile, delimiter=',')
                
                c = 0
                for row in buffer_reader :
                    if c == 0 :   
                        title = row
                    elif c == 1 :            
                        value = row
                    
                    c += 1
                
                
                for t in title :
                    idx = label.index(t)
                    var[idx] = unwrap(value[idx])
                    
            self.build_queries()
    
    
        
    def build_queries(self) :
        self.variables = []
        self.gui_fields = []
        for v in range(len(var_to_ask)) :
            s_query.add_query(var_to_ask[v],question[v],w_types[v])
                        
s_query = Stim_query()
s_query.build_queries()







    