import numpy as np
from tkinter import *
from tkinter import ttk, messagebox

n_block = 10
rep_per_block = 2

trial_duration = 5
starting_delay = 1
stim_window = [1,3]
response_delay = 0
response_window = [3,4]
ending_delay = trial_duration - response_window[-1]


var_to_ask = [n_block, rep_per_block, trial_duration, starting_delay, \
              stim_window, response_delay, response_window]
question =   ['Block number','Repetition per block','Trial duration','Starting delay', \
              'Stim window','Reponse delay','Response window']
    
w_types =    ['Edit', 'Edit', 'Edit', 'Edit', \
              'Slider', 'Edit', 'Slider']




class Behaviour_query:
    def __init__(self) :
        self.variables = []
        self.gui_fields = []
        self.gui_widget = []
        self.completed = False
        
    def add_query(self, variable, question, w_type) :
        self.variables.append(variable)
        self.gui_fields.append([question,w_type])


b_query = Behaviour_query()

for v in range(len(var_to_ask)) :
    b_query.add_query(var_to_ask[v],question[v],w_types[v])

    
        
class MyFirstGUI:
    def __init__(self, master):
        self.master = master
        master.title("A simple GUI")

        self.label = Label(master, text="This is our first GUI!")
        self.label.pack()

        self.greet_button = Button(master, text="Greet", command=self.greet)
        self.greet_button.pack()

        self.close_button = Button(master, text="Close", command=master.quit)
        self.close_button.pack()

    def greet(self):
        print("Greetings!")

