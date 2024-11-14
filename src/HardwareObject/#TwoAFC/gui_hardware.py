import numpy as np
from tkinter import *
from tkinter import ttk, messagebox
import os
import csv

hw_f_path = os.path.dirname(__file__)

question =   ['Water amount (mL)', 'Trigger at trial start']
var_to_ask = [0.2, True]
w_types =    ['Edit', 'CheckBox']

def unwrap(string) :
    if (type(string) == int) or (type(string) == float) :
        return string
    
    
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
    
    def load_parameters(self, name) :
        
        for i in range(len(self.variables)) :
            self.variables[i] = self.widget[i].get()
        
        
        pump_duration = self.variables
        
        with open(hw_f_path + '/Buffer/hardware_param_buffer_' + name + '.csv', 'w', newline='') as csvfile:
            fieldnames = question
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
            writer.writeheader()
            input_dict = {question[i]:self.variables[i] for i in range(len(self.variables))}
            writer.writerow(input_dict)
            
                
        
    def load_var_from_buffer(self, name, label=question, var=var_to_ask) :
        if os.path.isfile(hw_f_path + '/Buffer/hardware_param_buffer_' + name + '.csv') :
            with open(hw_f_path + '/Buffer/hardware_param_buffer_' + name + '.csv',newline='') as csvfile:
                buffer_reader = csv.reader(csvfile, delimiter=',')
                
                c = 0
                for row in buffer_reader :
                    if c == 0 :   
                        title = row
                    elif c == 1 :            
                        value = row
                    
                    c += 1
                
                i=0
                for t in title :
                    idx = label.index(t)
                    var[idx] = unwrap(value[i])
                    i+=1
                    
                    
            self.build_queries()
                
    def build_queries(self):
        self.variables = []
        self.gui_fields = []
        for v in range(len(var_to_ask)) :
            hw_query.add_query(var_to_ask[v],question[v],w_types[v])
                

                
hw_query = Hardware_query()
hw_query.build_queries



