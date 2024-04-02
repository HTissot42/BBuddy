import sys
import os

f_path = os.path.dirname(__file__)



hw_object = '#TwoAFC'
s_object = '#PureToneDisc'
b_object = '#DiscTask'

b_path = os.path.realpath(f_path + "/BehaviourObject/" + b_object)
s_path = os.path.realpath(f_path + "/StimObject/" + s_object)
hw_path = os.path.realpath(f_path + "/HardwareObject/" + hw_object)

sys.path.append(b_path)
sys.path.append(s_path)
sys.path.append(hw_path)

sys.path.append(os.path.realpath(f_path + "/BehaviourObject/General"))
sys.path.append(os.path.realpath(f_path + "/StimObject/General"))
sys.path.append(os.path.realpath(f_path + "/HardwareObject/General"))


def refresh_path(b_obj, s_obj, hw_obj) :
    global b_path
    global s_path
    global hw_path
    
    sys.path.remove(b_path)
    sys.path.remove(s_path)
    sys.path.remove(hw_path)
        
    b_path = os.path.realpath(f_path + "/BehaviourObject/" + b_obj)
    s_path = os.path.realpath(f_path + "/StimObject/" + s_obj)
    hw_path = os.path.realpath(f_path + "/HardwareObject/" + hw_obj)
    
    sys.path.append(b_path)
    sys.path.append(s_path)
    sys.path.append(hw_path)


#execfile(f_path + "/gui.py")



execfile(f_path + "/HardwareObject/" + hw_object + "/init_hardware.py")
execfile(f_path + "/StimObject/" + s_object + "/init_stim.py")
execfile(f_path + "/BehaviourObject/" + b_object + "/init_behaviour.py")

