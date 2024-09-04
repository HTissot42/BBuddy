import pandas as pd
import numpy as np
import random
import string
import pickle

L = np.array(range(10))

n = 1
for l in L :
    print(l)
    np.insert(L,n,l)
    n+=1