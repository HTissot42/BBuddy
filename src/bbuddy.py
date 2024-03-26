import sys
import os

f_path = os.path.dirname(__file__)



hw_object = '#TwoAFC'
s_object = '#PureToneDisc'
b_object = '#DiscTask'


sys.path.append(os.path.realpath(f_path + "/BehaviourObject/General"))
sys.path.append(os.path.realpath(f_path + "/BehaviourObject/" + b_object))

sys.path.append(os.path.realpath(f_path + "/StimObject/General"))
sys.path.append(os.path.realpath(f_path + "/StimObject/" + s_object))

sys.path.append(os.path.realpath(f_path + "/HardwareObject/General"))
sys.path.append(os.path.realpath(f_path + "/HardwareObject/" + hw_object))


execfile(f_path + "/HardwareObject/" + hw_object + "/initialize.py")
execfile(f_path + "/StimObject/" + s_object + "/gen_stim.py")
execfile(f_path + "/BehaviourObject/" + b_object + "/gen_trial.py")