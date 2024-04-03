from tkinter import *
from tkinter import ttk, Canvas, messagebox, filedialog, StringVar, Checkbutton, IntVar, DoubleVar, END
import time
from time_handling import timestep
import numpy as np

class Performance_plot() :
    
    def __init__(self, init_trial , nb_trial ,size ="1000x800") :
        
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
        
        
        self.rec_width = 1000
        self.rec_height = 200
        
        self.new_trial(init_trial)
        self.root.after(100, self.refresh)

    def refresh_header(self) :
        self.header = Frame(self.root,border=50).pack(fill='both',side='top',expand='True')
        Label(self.header,textvariable=self.trial_num).pack(fill='both',side='top')
        
        if self.trial.identity :
            identity = 'Target / Right'
        else :
            identity = 'Reference / Left'
            
        Label(self.header,text=identity).pack(fill='both',side='top')
        
        self.root.update()
    
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
            
        else :
            print('cleared')
            
        self.root.after(int(timestep*1000), self.refresh)
            
        
    def new_trial(self, trial) :
        self.trial = trial
        
        self.cleared = True
        self.clear(self.root)
        
                
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