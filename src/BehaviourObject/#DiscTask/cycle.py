import numpy as np
import time
import threading


from init_behaviour import trials
from performance import Performance_plot



def cycle():
    N = len(trials)
    n=1
    for trial in trials :
        p_plot.new_trial(trial)
        trial.run_trial()
        p_plot.refresh_plot()
        
        n+=1





p_plot = Performance_plot(trials[0],len(trials))
threading.Thread(target = cycle, daemon=True).start()
p_plot.loop()
