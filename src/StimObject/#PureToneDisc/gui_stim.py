import numpy as np
from tkinter import *
from tkinter import ttk, messagebox
import os
import csv


s_f_path = os.path.dirname(__file__)

frequencies = [800,2000,4400,10000]
target_pitch = 'High'
boundary = 3000
amp = 0.1

var_to_ask = [frequencies, target_pitch, boundary, amp]
question =   ['Sound frequencies', 'Target', 'Category boundary', 'Amplitude (0.1 max)']
    
w_types =    ['Edit', 'Choice High,Low', 'Edit', 'Edit']

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
    
    def load_parameters(self) :
        #for i in range(len(self.variables)) :
        #    self.variables[i] = self.widget[i].get()
            
        #frequencies, target_pitch = self.variables
            
        
        with open(s_f_path + '/stim_param_buffer.csv', 'w', newline='') as csvfile:
            fieldnames = question
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
            writer.writeheader()
            input_dict = {question[i]:self.variables[i] for i in range(len(self.variables))}
            writer.writerow(input_dict)
                
        
s_query = Stim_query()



def load_var_from_buffer(label, var) :
    with open(s_f_path + '/stim_param_buffer.csv',newline='') as csvfile:
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



if os.path.isfile(s_f_path + '/stim_param_buffer.csv') :
    load_var_from_buffer(question, var_to_ask)




for v in range(len(var_to_ask)) :
    s_query.add_query(var_to_ask[v],question[v],w_types[v])

    