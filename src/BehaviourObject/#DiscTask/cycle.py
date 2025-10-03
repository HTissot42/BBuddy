import numpy as np
import pandas as pd
import time
import threading
import csv
import os  
from init_behaviour import trials, one_motor, correction_p
from performance import Performance_plot


columns = ["Trial index", "Stim frequency","Stim AM rate", "Category", "Response", "Task", "Right licks", "Left licks","Choice rate", "dprimes", "Timeline events", "Flagged","Easy"]
data = {col:[] for col in columns}


animal_name = ''
current_date = ''
saving_dir = ''

def save_data() :
    data_df = pd.DataFrame(data)
    filepath = saving_dir + '/' + animal_name + '/' + animal_name + ' ' + current_date +'.csv'
    data_df.to_csv(filepath)




p_plot = Performance_plot(trials[0],len(trials),one_motor,correction_p)


def add_trial_to_data(t) :
    data["Trial index"].append(t.num)
    data["Stim frequency"].append(t.stim.freq)
    data["Stim AM rate"].append(t.stim.am_rate)
    data["Category"].append(t.identity)
    data["Response"].append(t.response)
    data["Task"].append(t.task)
    data["Right licks"].append(t.right_licks)
    data["Left licks"].append(t.left_licks)
    data["Choice rate"] = p_plot.response_rates
    data["dprimes"] = p_plot.dprimes
    
    data["Timeline events"].append(0)
    data["Flagged"].append(t.flagged)
    data["Easy"].append(t.easy)


def cycle():
    n=0
    trials_to_run = trials
    while n < len(trials):
        trial = trials_to_run[n]
        
        #Define if one (easy trial) or two motors will be active for this trial.
        #One motor if an easy trial is repeated or if we draw a number below the easy ratio value (from performance GUI)
        motor_config = (p_plot.easy_val > np.random.randint(0,100)) or trial.easy
        trial.setup_motors(motor_config)
        
        p_plot.new_trial(trial)
        
        
        trial.run_trial()
        
        if trial.correct == False :
            if p_plot.correction_val > np.random.randint(0,100) :
                print('Correction trial added')
                trials_to_run = np.insert(trials_to_run,(n+1),trial)
        
        add_trial_to_data(trial)
        
        save_data()
        
        p_plot.check_pause()
        
        p_plot.refresh_plot()
        
        n+=1
        
    if p_plot.ask_repetition() :
        cycle()


def run_cycle(animal, date, savedir) :
    global animal_name
    global current_date
    global saving_dir
    
    animal_name = animal
    current_date = date
    saving_dir = savedir

    threading.Thread(target = cycle, daemon=True).start()
    p_plot.loop()

