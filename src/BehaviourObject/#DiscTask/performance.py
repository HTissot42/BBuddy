from tkinter import *
from tkinter import ttk, Canvas, messagebox, filedialog, StringVar, Checkbutton, IntVar, DoubleVar, END, Button, Scale
import time
from time_handling import timestep
import numpy as np
from init_hardware import hw_setup
import matplotlib.pyplot as plt 
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from scipy.stats import norm
import os



b_f_path = os.path.dirname(__file__)

def compute_dprime(h,fa) :
    return norm.ppf(h) - norm.ppf(fa)


integ_window = 25
eps = 10**(-5)
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
    

    h1 = eps + np.sum(rew1 == 1)/(np.sum(response1) + eps)
    fa1 = eps + np.sum(rew1 == 0)/(np.sum(response1) + eps)
    
    h2 = eps + np.sum(rew2 == 1)/(np.sum(response2) + eps)
    fa2 = eps + np.sum(rew2 == 0)/(np.sum(response2) + eps)
    
  
    dprime1 = compute_dprime(h1,fa1)
    dprime2 = compute_dprime(h2,fa2)
    
    
    return r1_rate, r2_rate, no_r_rate, dprime1, dprime2, h1, h2


class Performance_plot() :    
    def __init__(self, init_trial , nb_trial, easy, correction, size ="900x1000+300+0") :
        
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
        
        self.plot_canvas = FigureCanvasTkAgg(self.fig, master = self.root)
        self.plot_canvas.get_tk_widget().pack(fill='both',side='top',expand='True')
        
        self.plot_formatting()
        
        self.responses = []
        self.corrects = []
        
        self.response_rates = [[0,0,0]]
        self.accuracies = [[0,0]]
        self.dprimes = [[0,0]]
        
        self.rec_width = 900
        self.rec_height = 200
        
        #print(os.getcwd())
        
        self.pause_image = PhotoImage(file = b_f_path + '/Pictures/pause_button.png')
        self.play_image = PhotoImage(file = b_f_path + '/Pictures/play_button.png')
        
        self.flag_image = PhotoImage(file = b_f_path + '/Pictures/flag.png')
        self.w_flag_image = PhotoImage(file = b_f_path + '/Pictures/w_flag.png')
        
        self.in_pause = False
        self.flagging = False
        self.easy_val = 100*easy
        self.correction_val = 100*correction
    
        
        self.new_trial(init_trial)
        self.root.after(100, self.refresh)
        


    def plot_formatting(self) :
        self.axs[0].spines['top'].set_visible(False)
        self.axs[0].spines['right'].set_visible(False)
        self.axs[1].spines['top'].set_visible(False)
        self.axs[1].spines['right'].set_visible(False)
        
        self.axs[1].set_xlabel('Trials #',fontsize=16)
        self.axs[1].set_yticks([0,0.5,1],['0%','50%','100%'])
        self.axs[1].set_ylim((-0.15,1.15))
        
        
        #self.axs[0].set_yticks([-1,0,1,2,3],[-1,0,1,2,3])
        #self.axs[0].set_ylim((-1,3))
        self.axs[0].set_ylim((-0.05,1.05))
        
        self.axs[0].axhline(0,linestyle='--',color='black',linewidth=0.5)
        self.axs[0].axhline(2,linestyle='--',color='black',linewidth=0.5)
        self.axs[0].axhline(1,linestyle='--',color='black',linewidth=0.5)
        
        self.axs[0].set_facecolor('whitesmoke')
        self.axs[1].set_facecolor('whitesmoke')
        
        #self.plot_canvas.get_tk_widget().pack(fill='both',side='top',expand='True')

    def refresh_header(self) :
        
        self.header = Frame(self.root,border=40).pack(fill='both',side='top',expand='True')
        Label(self.header,textvariable=self.trial_num).pack(fill='both',side='top')
        

        if self.trial.identity == 1 :
            identity = 'Target/Right'
        else :
            identity = 'Reference/Left'
            
        if self.trial.easy :
            identity += '\n Easy'
        else :
            identity += '\n Difficult'
            
        Label(self.header,text=identity).pack(fill='both',side='top')
        button_line = Frame(self.header,height = 160)
        button_line.pack(fill='both',side='top')
        
        self.pause_button = Button(button_line, command = self.switch_pause, image = self.pause_image, height=40, width=40, bg='white')
        self.pause_button.place(x=self.rec_width/2 - 60, y=40)
        
        if self.flagging :
            self.flag_button = Button(button_line, command = self.flag_trial, image = self.flag_image, height=40, width=40, bg='white')
        else :
            self.flag_button = Button(button_line, command = self.flag_trial, image = self.w_flag_image, height=40, width=40, bg='white')
            
        self.flag_button.place(x=self.rec_width/2 + 20, y=40)
        
        slider_label = Label(button_line, text = "Easy trial ratio")
        slider_label.place(x = self.rec_width/2 + 160, y=0)
        
        self.slider_easy = Scale(button_line, from_=0, to=100,  length=150, orient=HORIZONTAL)
        self.slider_easy.place(x = self.rec_width/2 + 160, y=25)
        self.slider_easy.set(self.easy_val)
        
        slider_label = Label(button_line, text = "Correction trial ratio")
        slider_label.place(x = self.rec_width/2 - 335, y=0)
        
        self.slider_correction = Scale(button_line, from_=0, to=100,  length=150, orient=HORIZONTAL)
        self.slider_correction.place(x = self.rec_width/2 - 310, y=25)
        self.slider_correction.set(self.correction_val)

        
        
        self.root.update()
        
    def refresh_plot(self) :
        self.responses.append(self.trial.response)
        self.corrects.append(self.trial.correct)
        
        
        
        r1_rate, r2_rate, no_r_rate, dprime1, dprime2, h1, h2 = \
            compute_recent_perf(self.responses, self.corrects)
        
        self.response_rates.append([r1_rate, r2_rate, no_r_rate])
        self.accuracies.append([h1,h2])
        self.dprimes.append([dprime1, dprime2])
    
        self.axs[0].cla()
        self.axs[1].cla()

        #self.axs[0].plot(range(0,self.n + 1), np.array(self.dprimes)[:,0], color='blue', \
        #                 alpha=0.55, linewidth=5 ,label='d\' right') 
        #self.axs[0].plot(range(0,self.n + 1), np.array(self.dprimes)[:,1], color='red',\
        #                 alpha=0.55, linewidth=5 ,label='d\' left') 
        
        self.axs[0].plot(range(0,self.n + 1), np.array(self.accuracies)[:,0], color='blue', \
                         alpha=0.55, linewidth=5 ,label='d\' right') 
        self.axs[0].plot(range(0,self.n + 1), np.array(self.accuracies)[:,1], color='red',\
                         alpha=0.55, linewidth=5 ,label='d\' left') 
        
        self.axs[1].plot(range(0,self.n + 1), np.array(self.response_rates)[:,0], color='cyan', \
                         alpha=0.55, linewidth=5 ,label='Right')
        self.axs[1].plot(range(0,self.n + 1), np.array(self.response_rates)[:,1], color='magenta',\
                         alpha=0.55, linewidth=5 ,label='Left')
        self.axs[1].plot(range(0,self.n + 1), np.array(self.response_rates)[:,2], color='grey',\
                         alpha=0.55, linewidth=5 ,label='No resp')
        
        self.axs[0].legend(loc="upper left")
        self.axs[1].legend(loc="upper left")
        
        self.plot_formatting()
    
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
        
        os._exit(00)
        
    def refresh(self) :
        
        if not self.cleared :  #Every command that interacts with a widget should be in this statement
            
            # New tkinter version syntax
            delta_x = self.rec_width *  (time.time() - self.c_time)/self.trial.timeline.duration
            self.canvas.move(self.c_pos, delta_x, 0)
            
            self.c_time = time.time()
            
            new_x = (self.c_time - self.start_time)*self.rec_width/self.trial.timeline.duration
            # Old tkinter version syntax
            #self.canvas.moveto(self.c_pos, new_x, 0)
            
            self.root.update()
            
            if len(self.trial.piezos.lick_events) > 0 :
                last_licks = self.trial.piezos.lick_events[-2:]

                if True in last_licks[0] :
                    self.canvas.create_rectangle(new_x, self.rec_height/2, \
                                                 new_x + 2, self.rec_height, fill = '#0009c2')
                elif True in last_licks[1] :
                    self.canvas.create_rectangle(new_x, self.rec_height/2, \
                                                 new_x + 2, self.rec_height, fill = '#c20029')
                        
            self.easy_val = self.slider_easy.get()
            self.correction_val = self.slider_correction.get()
        
        self.trial.flagged = self.flagging
        
        
        self.root.after(int(timestep*1000), self.refresh)
            
        
    def new_trial(self, trial) :
        
        self.trial = trial
        
        self.cleared = True
        self.clear(self.root)
        
        self.plot_canvas = FigureCanvasTkAgg(self.fig, master = self.root)
        self.plot_canvas.get_tk_widget().pack(fill='both',side='top',expand='True')
        
        canvas = Canvas(self.root, border = 40)
        canvas.pack(fill='both',side='bottom',expand='True')
                
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
    
    def switch_pause(self) :
        if self.in_pause:
            self.pause_button.config(image = self.pause_image)

        else :
            self.pause_button.config(image = self.play_image)
        
        self.in_pause = not self.in_pause
        
    def flag_trial(self) :
        if self.flagging:
            self.flag_button.config(image = self.w_flag_image)

        else :
            self.flag_button.config(image = self.flag_image)
        
        self.flagging = not self.flagging
        
            
        
    def check_pause(self) :
        while self.in_pause :
            pass
    
    def ask_repetition(self) :
        user_answer = messagebox.askquestion(title="Session finished !", message="Repeat the session ?")
        if user_answer == 'yes' :
            return True
        
        elif user_answer == 'no' :
            return False
        