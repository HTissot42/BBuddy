import sys
import os

f_path = __file__


b_object = '#TwoAFC'
s_object = ''
t_object = ''


sys.path.append(os.path.realpath(f_path + "/BehaviourObject/General"))
sys.path.append(os.path.realpath(f_path + "/BehaviourObject/" + b_object))

sys.path.append(os.path.realpath(f_path + "/StimObject/General"))
sys.path.append(os.path.realpath(f_path + "/StimObject/" + s_object))

sys.path.append(os.path.realpath(f_path + "/TrialObject/General"))
sys.path.append(os.path.realpath(f_path + "/TrialObject/" + t_object))

print(sys.path)