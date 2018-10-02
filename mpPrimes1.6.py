#import math as M
import multiprocessing as mp
import threading
import time

def doPrimes(c,START,END,PRIMES,Rq):
    l=list(range(START,END+1,2))
    ln=len(l)
    for prime in PRIMES:
        s=-(-START//prime)*prime
        for x in range(((s if s%2 else s+prime)-START)//2,ln,prime):
            l[x]=0
    if l:
        Rq.put([c,[x for x in l if x]])

def doWork(Jobs,JTq,Rq):
    c,s,e,p=Jobs.get()
    JTq.put(True)
    doPrimes(c,s,e,p,Rq)

def tryWork(Jobs,JTq,Rq):
    try:
        c,s,e,p=Jobs.get(True,0)
        doPrimes(c,s,e,p,Rq)
    except:
        pass

def threadWork(Jobs,JTq,Rq):
    try:
        c,s,e,p=Jobs.get(True,0)
    except:
        return
    t = threading.Thread(target = doPrimes, args=[c,s,e,p,Rq])
    t.start()
    JTq.put(True)


def worker(Jobs,JTq,Rq,Pq,CORES,NUM):
    if NUM==0:
        Primes=[2,3,5,7]

        def queueJobs(Primes,Jobs,JTq):
            iCP=1#index Current Prime
            while True:
                if iCP < len(Primes)-1:
                    JTq.get()
                    START=Primes[iCP]**2+2
                    END=Primes[iCP+1]**2-2
                    Jobs.put([iCP,START,END,Primes[1:iCP+1]])
                    iCP+=1
        
        t = threading.Thread(target = queueJobs, args=[Primes,Jobs,JTq])
        t.start()
        
        update=time.time()
        rate=1
        
        while True:
            if time.time()>=update+rate:
                update+=rate
                print("The " + "{:,}".format(len(Primes)) + "'th prime is " + str(Primes[-1]))
            Primes+=Pq.get()

            
            

    elif NUM==1:
        Rl={}#Return list
        C=1

        while True:
            x=Rq.get()
            if x[0]==C:
                Pq.put(x[1])
                C+=1
            else:
                Rl[x[0]]=x
            while C in Rl:
                Pq.put(Rl[C][1])
                del Rl[C]
                C+=1
            
    else:
        while True:
            doWork(Jobs,JTq,Rq)
            
        
        
            
        
    

if __name__ == "__main__":
    import sys
    print(sys.argv[0])
    
    Jobs=mp.Queue()
    CORES = 2*max(2, mp.cpu_count())
    Rq= mp.Queue()#Return Queue
    Pq=mp.Queue()#Primes Queue
    JTq=mp.Queue()#Job Taken Queue
    for i in range(CORES*2):
        JTq.put(True)
    p={}
    for i in range(CORES):
        p[i] = mp.Process(target = worker, args=[Jobs,JTq,Rq,Pq,CORES,i])
        p[i].start()
    for i in range(CORES):
        p[i].join()
