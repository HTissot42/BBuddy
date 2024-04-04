from tkinter import *
from tkinter import ttk, messagebox, filedialog, StringVar, Checkbutton, IntVar, DoubleVar, END
import csv
import os
import sys
from bbuddy import b_object, s_object, hw_object, refresh_path, initialize_object, execfile

f_path = os.path.dirname(__file__)




def execute_all_gui() :
    execfile(f_path + "/HardwareObject/" + hw_object + "/gui_hardware.py")
    execfile(f_path + "/BehaviourObject/" + b_object + "/gui_behaviour.py")
    execfile(f_path + "/StimObject/" + s_object + "/gui_stim.py")
"""
def execute_all_gui() :
    exec(open(f_path + "/HardwareObject/" + hw_object + "/gui_hardware.py").read())
    exec(open(f_path + "/BehaviourObject/" + b_object + "/gui_behaviour.py").read())
    exec(open(f_path + "/StimObject/" + s_object + "/gui_stim.py").read())
"""

execute_all_gui()


b_files = os.listdir(f_path + '/BehaviourObject/')
s_files = os.listdir(f_path + '/StimObject/')
hw_files = os.listdir(f_path + '/HardwareObject/')

b_obj_list = []
for b_file in b_files :
    if b_file.startswith("#") :
        b_obj_list.append(b_file)
        
s_obj_list = []
for s_file in s_files :
    if s_file.startswith("#") :
        s_obj_list.append(s_file)
        
hw_obj_list = []
for hw_file in hw_files :
    if hw_file.startswith("#") :
        hw_obj_list.append(hw_file)
        



def set_entry_value(entry, value):
    entry.delete(0, END)  # Clear the existing value in the entry
    entry.insert(0, value)



class GUI :
    def __init__(self, size ="900x900"):
        
        
        root = Tk() 

        root.geometry(size)
        root.protocol("WM_DELETE_WINDOW", self.on_closing)
        root.title("Bbuddy")
        
        root.option_add("*Font", "aerial 15")
        root.option_add("*Label.Font", "aerial 16 bold")
        
        #root.wm_attributes("-alpha", 0.7)
        
        self.root = root
        
        self.header = Frame(root, border = 25)
        
        self.header.pack(fill='both',side='top')
        Label(self.header,text = 'Ferret name').pack(fill='both',side='left')
        #Label(self.header,text = 'Ferret name').grid(row=0,column=0)
        animal_entry = Entry(self.header)
        
        
        #Label(self.header,text = 'Save directory').grid(row=0,column=2)
        btn_text = StringVar()
        self.btn_text = btn_text
        save_path = Button(self.header,text=self.btn_text, command=self.browse_button)
        
        #animal_entry.grid(row = 1, column = 0)
        #save_path.grid(row = 1, column = 2)
        
        animal_entry.pack(fill='both',side='left')
        save_path.pack(fill='both',side='right')
        
        self.animal_entry = animal_entry
        
        Label(self.header,text = 'Save directory').pack(fill='both',side='right')
            
        
        if os.path.isfile(f_path + '/general_param_buffer.csv') :
            self.load_var_from_buffer()
        
        else :
            self.animal = ''
            self.dirname = ''
        
        set_entry_value(self.animal_entry, self.animal)
        
        
        last_line = Frame(self.root)
        last_line.pack(fill='both',side='bottom')
        
        start_button = Button(last_line,text='Start', command=self.load_all_params)
        start_button.pack(fill='both',side='right', expand='True')
        #start_button.grid(row = 20, column = 2)
        start_button.configure(bg='blue')
        
        
        stop_button = Button(last_line,text='Stop', command=self.stop_gui)
        stop_button.pack(fill='both',side='left', expand='True')
        #stop_button.grid(row = 20, column = 0)
        stop_button.configure(bg='red')

        
        
        self.bfrm = Frame(root,border=25)
        #b_frm.grid(row = 2, column = 0)
        self.bfrm.pack(fill='both', side='left')
        
        
        
        self.sfrm = Frame(root,border=25)
        #s_frm.grid(row = 2, column = 1)
        self.sfrm.pack(fill='both',side='left')
        
        
        self.hwfrm = Frame(root,border=25)
        
        #hw_frm.grid(row = 2, column = 2)
        self.hwfrm.pack(fill='both',side='left')
        

        self.load_choice_box()

    
    def load_general(self) :
        self.animal = self.animal_entry.get()

    def browse_button(self):
        self.dirname = filedialog.askdirectory()
        self.btn_text.set(self.dirname)
        
        return self.dirname
    
    
    def load_choice_box(self) :
        b_choicebox = Label(self.bfrm, text = "Behaviour object:")
        b_choicebox.pack(fill='both',side='top')
        #b_choicebox.grid(row=0,column=0)
        
        s_choicebox = Label(self.sfrm, text = "Stim object:")
        s_choicebox.pack(fill='both',side='top')
        #s_choicebox.grid(row=0,column=0)
        
        hw_choicebox = Label(self.hwfrm, text = "Hardware object:")
        hw_choicebox.pack(fill='both',side='top')
        #hw_choicebox.grid(row=0,column=0)
        
        b_choicelist = ttk.Combobox(self.bfrm, values=b_obj_list)
        b_choicelist.pack(fill='both',side='top')
        #b_choicelist.grid(row=1,column=0)
        b_choicelist.current(0)
        b_object = b_obj_list[0]
        
        self.b_choice = b_choicelist

        s_choicelist = ttk.Combobox(self.sfrm, values=s_obj_list)
        s_choicelist.pack(fill='both',side='top')
        #s_choicelist.grid(row=1,column=0)
        s_choicelist.current(0)
        s_object = s_obj_list[0]
        
        self.s_choice = s_choicelist

        hw_choicelist = ttk.Combobox(self.hwfrm, values=hw_obj_list)
        hw_choicelist.pack(fill='both',side='top')
        #hw_choicelist.grid(row=1,column=0)
        hw_choicelist.current(0)
        hw_object = hw_obj_list[0]
        
        self.hw_choice = hw_choicelist
        
        self.refresh_object()
        
        #self.b_choice.bind('<<ComboboxSelected>>',self.test)
        self.b_choice.bind('<<ComboboxSelected>>',self.load_gui_behaviour)
        self.s_choice.bind('<<ComboboxSelected>>',self.load_gui_stim)
        self.hw_choice.bind('<<ComboboxSelected>>',self.load_gui_hardware)
        
        b_entries = Frame(self.bfrm)
        b_entries.pack(fill='both',side='top')
        #b_entries.grid(row=2,column=0)
        self.b_entries = b_entries
        
        s_entries = Frame(self.sfrm)
        s_entries.pack(fill='both',side='top')
        #s_entries.grid(row=2,column=0)
        self.s_entries = s_entries

        hw_entries = Frame(self.hwfrm)
        hw_entries.pack(fill='both',side='top')
        #hw_entries.grid(row=2,column=0)
        self.hw_entries = hw_entries
        
        self.load_gui_behaviour(None)
        self.load_gui_stim(None)
        self.load_gui_hardware(None)
    
    def refresh_object(self) :
        b_object = self.b_choice.get()
        s_object = self.s_choice.get()
        hw_object = self.hw_choice.get()
        
        refresh_path(b_object, s_object, hw_object)
        
        execute_all_gui()
        
        
    def load_gui_behaviour(self, event):
        self.refresh_object()
        
        from gui_behaviour import b_query
        
        b_query.clear_widget()
        
        self.b_query = b_query
        
        self.build_window(self.b_entries, self.b_query)
        
        
    def load_gui_stim(self, event):
        self.refresh_object()
        
        from gui_stim import s_query
        
        s_query.clear_widget()
        
        self.s_query = s_query
        
        self.build_window(self.s_entries, self.s_query)
        
        
    def load_gui_hardware(self, event):
        self.refresh_object()
        
        from gui_hardware import hw_query
        
        hw_query.clear_widget()
        
        self.hw_query = hw_query
        
        self.build_window(self.hw_entries, self.hw_query)
    
    def clear(self,frame) :
        for child in frame.winfo_children() :
            child.destroy()
    
    def build_window(self, parent, query) :
        
        self.clear(parent)
        c = 0
        for field in query.gui_fields :
            label = Label(parent, text = field[0])
            label.pack(fill='both',side='top', expand='True')
            #label.grid(row = c, column = 0)
            if field[1] == 'Edit' :
                widg = Entry(parent)
                widg.pack(fill='both',side='top', expand='True')
                #widg.grid(row = c+1, column = 0)
                set_entry_value(widg, query.variables[int(c/2)])
                #if not query.completed :
                query.widget.append(widg)
                    
                
            elif field[1] == 'CheckBox' :
                var = IntVar()
                var.set(bool(query.variables[int(c/2)]))
                widg = Checkbutton(parent, variable = var)
                widg.pack(fill='both',side='top', expand='True')
                #widg.grid(row = c+1, column = 0)
                #if not query.completed :
                query.widget.append(var)
            
            elif field[1][:7] == 'Choice ' :
                possibilities = field[1][7:].split(',')
                widg = ttk.Combobox(parent, values=possibilities)
                widg.pack(fill='both',side='top', expand='True')
                #widg.grid(row = c+1, column = 0)
                
                choice_idx = possibilities.index(query.variables[int(c/2)])
                widg.current(choice_idx)
                
                #if not query.completed :
                query.widget.append(widg)
                        
            
            c+=2
        query.completed = True
                
    
    def load_all_params(self) :
        for i in range(len(self.hw_query.variables)) :
            self.hw_query.variables[i] = self.hw_query.widget[i].get()
        
        for i in range(len(self.b_query.variables)) :
            self.b_query.variables[i] = self.b_query.widget[i].get()
            
        for i in range(len(self.s_query.variables)) :
            self.s_query.variables[i] = self.s_query.widget[i].get()
        
        
        self.hw_query.load_parameters()
        self.b_query.load_parameters()
        self.s_query.load_parameters()
        self.load_general()
        self.write_buffer()
        
        
        self.stop_gui()
        
        initialize_object()

        #exec(open(f_path + "/BehaviourObject/" + b_object + "/cycle.py").read())
        execfile(f_path + "/BehaviourObject/" + b_object + "/cycle.py")
        
    
    def loop(self) :
        self.root.mainloop()
    
    def on_closing(self):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.stop_gui()
    
    def stop_gui(self) :
        self.clear(self.root)
        self.root.destroy()
        self.root.quit()
        
        
    def write_buffer(self) :
    
        with open(f_path + '/general_param_buffer.csv', 'w', newline='') as csvfile:
            fieldnames = ['Animal', 'Save directory']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
            writer.writeheader()
            input_dict = {'Animal' : self.animal, 'Save directory' : self.dirname}
            writer.writerow(input_dict)
            
        
    def load_var_from_buffer(self) :
        with open(f_path + '/general_param_buffer.csv',newline='') as csvfile:
            buffer_reader = csv.reader(csvfile, delimiter=',')
            
            c = 0
            for row in buffer_reader :
                if c == 0 :   
                    title = row
                elif c == 1 :            
                    value = row
                
                c += 1
            
            
            for t in title :
                if t == 'Animal' :
                    self.animal = value[title.index(t)]
                elif t == 'Save directory' :
                    self.dirname = value[title.index(t)]



gui = GUI()

gui.loop()


