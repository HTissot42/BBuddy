from tkinter import *
from tkinter import ttk, Canvas, messagebox, filedialog, StringVar, Checkbutton, IntVar, DoubleVar, END
import time
from time_handling import timestep
import numpy as np
from init_hardware import hw_setup
import matplotlib.pyplot as plt 
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from scipy.stats import norm


def compute_dprime(h,fa) :
    return norm.ppf(h) - norm.ppf(fa)


integ_window = 25
def compute_recent_perf(responses, rewards) :
    
    sample_size = min(len(responses),integ_window)
    
    resp_array = np.array(responses)[-sample_size:]
    rew_array = np.array(rewards)[-sample_size:]
    
    response1 = (resp_array == 1)
    response2 = (resp_array == -1)
    no_response = (resp_array == 0)
    
    r1_rate = np.sum(response1)/sample_size
    r2_rate = np.sum(response2)/sample_size
    no_r_rate = np.sum(no_response)/sample_size

    rew1 = rew_array[response1]
    rew2 = rew_array[response2]
    
    h1 = np.sum(rew1 == 1)/sample_size
    fa1 = np.sum(rew1 == 0)/sample_size
    
    h2 = np.sum(rew2 == 1)/sample_size
    fa2 = np.sum(rew2 == 0)/sample_size
    
    if h1 < 0.01 :
        dprime1 = -10
    elif h1 > 0.99 :
        dprime1 = 10
    else :
        dprime1 = compute_dprime(h1,fa1)
    
        
    if h2 < 0.01 :
        dprime2 = -10
    elif h2 > 0.99 :
        dprime2 = 10
    else :
        dprime2 = compute_dprime(h2,fa2)
    
    
    return r1_rate, r2_rate, no_r_rate, dprime1, dprime2


class Performance_plot() :
    
    def __init__(self, init_trial , nb_trial ,size ="900x900") :
        
        root = Tk() 

        root.geometry(size)
        root.protocol("WM_DELETE_WINDOW", self.on_closing)
        root.title("Bbuddy - Real time plot")
        
        root.option_add("*Font", "aerial 15")
        root.option_add("*Label.Font", "aerial 16 bold")
        
        self.root = root
        
        self.n = -1
        self.nb_trial = nb_trial
        self.trial_num = StringVar()
        self.trial_num.set('Trial ' + str(self.n) + '/' + str(self.nb_trial))
        
        self.fig, self.axs = plt.subplots(2,1, figsize=(8,6), dpi=80, facecolor='whitesmoke')
        plt.rcParams.update({'font.size': 15})
        self.plot_formatting()
        
        self.responses = []
        self.rewards = []
        
        self.response_rates = []
        self.dprimes = []
        
        self.rec_width = 900
        self.rec_height = 200
        
        self.new_trial(init_trial)
        self.root.after(100, self.refresh)
        
        
        

        
        plot_canvas = FigureCanvasTkAgg(self.fig, master = self.root)
        plot_canvas.get_tk_widget().pack(fill='both',side='top',expand='True')

    def plot_formatting(self) :
        self.axs[0].spines['top'].set_visible(False)
        self.axs[0].spines['right'].set_visible(False)
        self.axs[1].spines['top'].set_visible(False)
        self.axs[1].spines['right'].set_visible(False)
        
        self.axs[1].set_xlabel('Trials #',fontsize=16)
        self.axs[1].set_yticks([0,0.5,1],['0%','50%','100%'])
        self.axs[1].set_ylim((-0.15,1.15))
        
        
        self.axs[0].set_yticks([-1,0,1,2,3],[-1,0,1,2,3])
        self.axs[0].set_ylim((-1,3))
        
        self.axs[0].set_facecolor('whitesmoke')
        self.axs[1].set_facecolor('whitesmoke')

    def refresh_header(self) :
        
        self.header = Frame(self.root,border=50).pack(fill='both',side='top',expand='True')
        Label(self.header,textvariable=self.trial_num).pack(fill='both',side='top')
        

        if self.trial.identity == 1 :
            identity = 'Target / Right'
        else :
            identity = 'Reference / Left'
            
        Label(self.header,text=identity).pack(fill='both',side='top')
        
        self.root.update()
        
    def refresh_plot(self) :
        self.responses.append(self.trial.response)
        self.rewards.append(self.trial.rewarded)
        
        
        r1_rate, r2_rate, no_r_rate, dprime1, dprime2 = \
            compute_recent_perf(self.responses, self.rewards)
        
        self.response_rates.append([r1_rate, r2_rate, no_r_rate])
        self.dprimes.append([dprime1, dprime2])
    
        self.axs[0].cla()
        self.axs[1].cla()

        self.axs[0].plot(range(1,self.n + 1), np.array(self.dprimes)[:,0], color='blue', \
                         alpha=0.55, linewidth=5 ,label='d\' right') 
        self.axs[0].plot(range(1,self.n + 1), np.array(self.dprimes)[:,1], color='red',\
                         alpha=0.55, linewidth=5 ,label='d\' left') 
        
        self.axs[1].plot(range(1,self.n + 1), np.array(self.response_rates)[:,0], color='cyan', \
                         alpha=0.55, linewidth=5 ,label='Right')
        self.axs[1].plot(range(1,self.n + 1), np.array(self.response_rates)[:,1], color='magenta',\
                         alpha=0.55, linewidth=5 ,label='Left')
        self.axs[1].plot(range(1,self.n + 1), np.array(self.response_rates)[:,2], color='grey',\
                         alpha=0.55, linewidth=5 ,label='No resp')
        
        self.axs[0].legend(loc="upper left")
        self.axs[1].legend(loc="upper left")
        
        self.plot_formatting()
        #plot_canvas = FigureCanvasTkAgg(self.fig, master = self.root)
        #plot_canvas.get_tk_widget().pack(fill='both',side='top',expand='True')
    
    def clear(self,frame) :
        for child in frame.winfo_children() :
            child.destroy()
            
    def loop(self) :
        self.root.mainloop()
    
    def on_closing(self):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.stop_gui()
    
    def stop_gui(self) :
        self.clear(self.root)
        self.root.destroy()
        self.root.quit()
        
    def refresh(self) :
        
        if not self.cleared :
            
            self.c_time = time.time()
            new_x = (self.c_time - self.start_time)*self.rec_width/self.trial.timeline.duration
            self.canvas.moveto(self.c_pos, new_x, 0)
            
            self.root.update()
            
            #print(len(self.trial.piezos.lick_events))
            
            if len(self.trial.piezos.lick_events) > 0 :
                #print(np.shape(self.trial.lick_events))
                last_licks = self.trial.piezos.lick_events[-2:]
                #print(np.shape(last_licks))

                if True in last_licks[0] :
                    #print('L R')
                    self.canvas.create_rectangle(new_x, self.rec_height/2, \
                                                 new_x + 2, self.rec_height, fill = '#0009c2')
                elif True in last_licks[1] :
                    #print('L L')
                    self.canvas.create_rectangle(new_x, self.rec_height/2, \
                                                 new_x + 2, self.rec_height, fill = '#c20029')
            
        self.root.after(int(timestep*1000), self.refresh)
            
        
    def new_trial(self, trial) :
        
        self.trial = trial
        
        self.cleared = True
        self.clear(self.root)
        
        plot_canvas = FigureCanvasTkAgg(self.fig, master = self.root)
        plot_canvas.get_tk_widget().pack(fill='both',side='top',expand='True')
                
        canvas = Canvas(self.root, border = 50)
        canvas.pack(fill='both',side='bottom',expand='True')
        #canvas.grid(row=1,column=1)
                
        self.canvas = canvas
        
        self.canvas.create_rectangle(0, 0, self.rec_width, self.rec_height, fill = '#ddd')
       
        
        timeline = self.trial.timeline
        
        resp_window = np.array(timeline.response)/timeline.duration
        stim_window = np.array(timeline.stim)/timeline.duration
        cue_window =  np.array(timeline.cue)/timeline.duration
        

        self.canvas.create_rectangle(stim_window[0]*self.rec_width, 3*self.rec_height/4, \
                                     stim_window[1]*self.rec_width, self.rec_height, fill = '#b7faf8')
        
        self.canvas.create_rectangle(resp_window[0]*self.rec_width, 2*self.rec_height/3, \
                                     resp_window[1]*self.rec_width, self.rec_height, fill = '#f5e6be')
        
        self.canvas.create_rectangle(cue_window[0]*self.rec_width, 7*self.rec_height/8, \
                                     cue_window[1]*self.rec_width, self.rec_height, fill = '#f5cebe')
       
        
        current_pos = self.canvas.create_rectangle(0, 0, 3, self.rec_height, fill='#4d84f5')
        
        self.c_pos = current_pos 
        self.start_time = time.time()
        self.c_time = time.time()

        self.n += 1
        self.trial_num.set('Trial ' + str(self.n) + '/' + str(self.nb_trial))
        self.refresh_header()
        
        self.cleared = False