#import math as M
import multiprocessing as mp
import threading
import time
import math

def doPrimes(c,i,n,START,END,PRIMES,Rq):
    l=list(range(START,END+1,2))
    ln=len(l)
    for prime in PRIMES:
        s=-(-START//prime)*prime
        for x in range(((s if s%2 else s+prime)-START)//2,ln,prime):
            l[x]=0
    if l:
        Rq.put([c,i,n,[x for x in l if x]])
        #print("dp",[c,i,n,[x for x in l if x]])

def doWork(Jobs,Rq):
    c,i,n,s,e,p=Jobs.get()
    doPrimes(c,i,n,s,e,p,Rq)

def tryWork(Jobs,Rq):
    try:
        c,i,n,s,e,p=Jobs.get(True,0)
        doPrimes(c,i,n,s,e,p,Rq)
    except:
        pass

def threadWork(Jobs,Rq):
    try:
        c,i,n,s,e,p=Jobs.get(True,0)
    except:
        return
    t = threading.Thread(target = doPrimes, args=[c,i,n,s,e,p,Rq])
    t.start()

def worker(Jobs,Rq,Pq,CORES,NUM):
    if NUM==0:
        Primes=[3,5,7]
        iCP=0#index Current Prime
        Li=iCP#Lowes used index
        update=time.time()
        UPRATE=2
        t=0
        
        while True:
            doW=True
            t+=1
            #if time.time()-update>UPRATE:
            if t>1000:
                print("The " + "{:,}".format(len(Primes)+1) + "'th prime is " + str(Primes[-1]))
                #update+=UPRATE
                t=0
            if not Pq.empty():
                #print("P")
                doW=False
                Primes+=Pq.get()
                #print("p",Primes)
            if Jobs.empty() and iCP<len(Primes)-1:
                #print("A")
                doW=False
                START=Primes[iCP]**2+2
                END=Primes[iCP+1]**2-2
                numj=int((END-START+1)**.5)#number of jobs
                s=START
                for i in range(numj):
                    e=((END-s)//(numj-i))+s
                    e=e if e%2 else e+1
                    Jobs.put([iCP,i,numj,s,e,Primes[:iCP+1]])
                    #print("j",[iCP,i,numj,s,e,Primes[:iCP+1]])
                    s=e+2
                iCP+=1
            if doW:
                #threadWork(Jobs,Rq)
                pass

    elif NUM==1:
        Rl=[]#Return list
        C=0
        I=0

        while True:
            if not Rq.empty():
                #print("C")
                x=Rq.get()
                Rl+=[x]
                #print("c",Rl[-1])
                if Rl[-1][0]==C and Rl[-1][1]==I:
                    n=Rl[-1][2]
                    y=Rl.pop(-1)[3]
                    #print("y",y)
                    Pq.put(y)
                    I+=1
                    if I==n:
                        I=0
                        C+=1
                else:
                    Rl.sort()
                    while Rl[0][0]==C and Rl[0][1]==I:
                        n=Rl[0][2]
                        x=Rl.pop(0)[3]
                        #print("x",x)
                        Pq.put(x)
                        I+=1
                        if I==n:
                            I=0
                            C+=1
                        if not Rl:
                            break
                    
            else:
                pass
            '''
                try:
                    print(C,I,Rl[0][0],Rl[0][1])
                except:
                    print(C,I,[])
                '''
            
    else:
        while True:
            doWork(Jobs,Rq)
            
        
        
            
        
    

if __name__ == "__main__":
    import sys
    print(sys.argv[0])
    
    Jobs=mp.Queue()
    CORES = max(3, mp.cpu_count())
    Rq= mp.Queue()#Return Queue
    Pq=mp.Queue()#Primes Queue
    p={}
    for i in range(CORES):
        p[i] = mp.Process(target = worker, args=[Jobs,Rq,Pq,CORES,i])
        p[i].start()
    for i in range(CORES):
        p[i].join()
