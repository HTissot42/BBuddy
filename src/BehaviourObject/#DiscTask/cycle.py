import numpy as np
import time
import threading
import csv

from init_behaviour import trials
from performance import Performance_plot


columns = ["Trial index", "Stim frequency","Stim AM rate", "Category", "Response", "Task", "Licks", "Choice rate", "dprimes", "Timeline events"]
data = {col:[] for col in columns}

animal_name = ''
current_date = ''
saving_dir = ''

def save_data() :
    with open(saving_dir + '/' + animal_name + ' ' + current_date +'.csv', 'w', newline='') as csvfile:
        w = csv.DictWriter(csvfile, fieldnames=columns)
        w.writeheader()
        w.writerow(data)



p_plot = Performance_plot(trials[0],len(trials))


def add_trial_to_data(t) :
    data["Trial index"].append(t.num)
    data["Stim frequency"].append(t.stim.freq)
    data["Stim AM rate"].append(t.stim.am_rate)
    data["Category"].append(t.identity)
    data["Response"].append(t.response)
    data["Task"].append(t.task)
    data["Licks"].append(t.licks)
    data["Choice rate"] = p_plot.response_rates
    data["dprimes"] = p_plot.dprimes
    
    data["Timeline events"].append(0)


def cycle():
    N = len(trials)
    n=1
    for trial in trials :
        p_plot.new_trial(trial)
        
        trial.run_trial()
        
        add_trial_to_data(trial)
        
        save_data()
        
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

