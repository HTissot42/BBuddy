import pprint
import numpy as np 
import nidaqmx
import time
from nidaqmx.constants import AcquisitionType

pp = pprint.PrettyPrinter(indent=4)


class C :
    

    def callback(self,task_handle, every_n_samples_event_type, number_of_samples, callback_data):
           # buffer = np.zeros(num_samples, dtype=np.float32)
            lick_events = self.task.read(1000)
            lick_events = np.array(lick_events)
            print(lick_events)
            if np.any(lick_events) == True :
                print("Lick detected on " + self.name)
                print(lick_events)
                return 1
            else :
                return 0
    def test(self) :
        with nidaqmx.Task() as task:
            self.task = task
            self.task.di_channels.add_di_chan("D0/port0/line3")
        
            self.task.timing.cfg_samp_clk_timing(1000, sample_mode=AcquisitionType.CONTINUOUS)
        
        
            samples = []
        
            
            self.task.register_every_n_samples_acquired_into_buffer_event(1000, self.callback)
        
            self.task.start()
            
            #time.sleep(5)
            
            input("Running task. Press Enter to stop and see number of " "accumulated samples.\n")
        
            print(len(samples))