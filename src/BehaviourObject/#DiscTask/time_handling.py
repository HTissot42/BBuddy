import time

timestep = 1/50

def tic() :
    #t1 = time.time()
    time.sleep(timestep)
    #t2 = time.time()
    #print((t2-t1) - timestep)

def wait(duration) :
    t1 = time.time()
    if duration >= timestep :
        print("waiting for " + str(duration) + " s..")
        #print((int(duration//timestep)))
        for t in range(int(duration//timestep)) :
            tic()
            
    t2 = time.time()
    print((t2-t1) - duration)
    