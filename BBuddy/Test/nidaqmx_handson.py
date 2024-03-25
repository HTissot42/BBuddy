import nidaqmx
from nidaqmx.constants import LineGrouping
import numpy as np

n_sample = 1000
sample_rate = 100

on_and_off = np.array([True for k in range(n_sample//2)] + [False for k in range(n_sample//2)])
off = np.array([False for k in range(n_sample)])

sample = np.stack([off,off,on_and_off])
with nidaqmx.Task() as task:
    
    left_pump = task.do_channels.add_do_chan('D0/port1/line3', line_grouping=LineGrouping.CHAN_FOR_ALL_LINES)
    red_light = task.do_channels.add_do_chan('D0/port2/line3', line_grouping=LineGrouping.CHAN_FOR_ALL_LINES)
    blue_light = task.do_channels.add_do_chan('D0/port0/line4', line_grouping=LineGrouping.CHAN_FOR_ALL_LINES)
    
    task.timing.cfg_samp_clk_timing(rate=sample_rate, source="OnBoardClock", samps_per_chan=n_sample)
    print(task.do_channels.channel_names)
    #task.timing.cfg_samp_clk_timing(1000)
    
    task.write(sample, auto_start=False)
    
    task.start()
    #task.write([False])
    #task.stop()