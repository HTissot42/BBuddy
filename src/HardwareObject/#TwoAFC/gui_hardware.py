import numpy as np
from tkinter import *
from tkinter import ttk, messagebox
import os
import csv

hw_f_path = os.path.dirname(__file__)

pump_duration = 0.15

var_to_ask = [pump_duration]
question =   ['Pump duration']
w_types =    ['Edit']

def unwrap(string) :
    if ' ' in string :
    
        splitted_string = string.split()
        
        result = []
        for s in splitted_string :
            result.append(float(s))
            
        
        return result
    
    else :
        return float(string)

class Hardware_query:
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

        pump_duration = self.variables
        
        with open(hw_f_path + '/hardware_param_buffer.csv', 'w', newline='') as csvfile:
            fieldnames = question
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
            writer.writeheader()
            input_dict = {question[i]:self.variables[i] for i in range(len(self.variables))}
            writer.writerow(input_dict)
                
hw_query = Hardware_query()


def load_var_from_buffer() :
    with open(hw_f_path + '/hardware_param_buffer.csv',newline='') as csvfile:
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



if os.path.isfile(hw_f_path + '/hardware_param_buffer.csv') :
    load_var_from_buffer()


for v in range(len(var_to_ask)) :
    hw_query.add_query(var_to_ask[v],question[v],w_types[v])

print('In hw :')
print(hw_query.widget)