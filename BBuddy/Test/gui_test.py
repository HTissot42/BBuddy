from tkinter import Tk, Label, Button, messagebox

def on_closing():
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        root.destroy()



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

root = Tk()

root.protocol("WM_DELETE_WINDOW", on_closing)
my_gui = MyFirstGUI(root)
root.mainloop()

#help(my_gui.master)

