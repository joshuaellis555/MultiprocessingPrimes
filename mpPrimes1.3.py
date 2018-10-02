#import math as M
import multiprocessing as mp
import threading
import time
import math

'''
Primes=[2,3,5,7,11,13]
EndPoint=Primes[-1]
iMainPrime=len(Primes)-2
NextMPrimeSqrd=Primes[iMainPrime+1]**2

print('1.5')

while True:
    for dummy in range(700):
        StartPoint=EndPoint+2
        EndPoint+=Primes[iMainPrime]-1
        if EndPoint >= NextMPrimeSqrd:
            EndPoint=NextMPrimeSqrd
            iMainPrime+=1
            NextMPrimeSqrd=Primes[iMainPrime+1]**2
        CurrentList=list(range(StartPoint,EndPoint+1,2))
        lcl=len(CurrentList)
        
        for prime in Primes[1:iMainPrime+1]:
            c=-(-StartPoint//prime)*prime
            for i in range(((c if c%2 else c+prime)-StartPoint)//2,lcl,prime):
                CurrentList[i]=0


        Primes+=[x for x in CurrentList if x]
    print('The '+str(len(Primes))+"'th prime is "+str(Primes[-1]))
'''

def doPrimes(START,END,PRIMES):
    #print(START,END,PRIMES)
    l=list(range(START,END+1,2))
    #print(l)
    ln=len(l)
    #print(ln)
    for prime in PRIMES:
        s=-(-START//prime)*prime
        for i in range(((s if s%2 else s+prime)-START)//2,ln,prime):
            l[i]=0
    #print(l)
    return l
    
def ppl(l):
    r=l.pop(0)
    ln=len(l)
    while ln>0 and l[0]==0:
        ln-=1
        l.pop(0)
    return r

def doWork(Jobs,Rq):
    n,i,c,s,e,p=Jobs.get()
    Rq.put([n,i,c,doPrimes(s,e,p)])

def doWork(Jobs,Rq):
    try:
        n,i,c,s,e,p=Jobs.get(True,0)
        Rq.put([n,i,c,doPrimes(s,e,p)])
    except:
        pass

def threadWork(Jobs,Rq):
    try:
        t = threading.Thread(target = tryWork, args=[Jobs,Rq])
        t.start()
    except:
        pass

def worker(Jobs,Rq,Rlenq,Rpq,Pq,CORES,NUM):
    if NUM==0:
        Primes=[3,5,7]
        iCP=0#index Current Prime
        Li=iCP#Lowes used index
        Rlens={}#return lengths
        update=time.time()
        
        while True:
            doW=True
            if time.time()-update>1:
                print("the " + str(len(Primes)+1) + "'th prime is " + str(Primes[-1]))
                update+=1
            if not Pq.empty():
                print("P")
                doW=False
                Primes+=Pq.get()
            if Jobs.empty() and iCP<len(Primes)-1:
                print("A")
                doW=False
                START=Primes[iCP]**2+2
                END=Primes[iCP+1]**2-2
                numj=int((END-START+1)**.5)#number of jobs
                s=START
                for i in range(numj):
                    e=((END-s)//(numj-i))+s
                    e=e if e%2 else e+1
                    Jobs.put([numj-1,i,iCP,s,e,Primes[:iCP+1]])
                    s=e+2
                iCP+=1
            if doW:
                #threadWork(Jobs,Rq)
                pass
                
    elif NUM==1:
        while True:
            if not Rpq.empty():
                print("B")
                primes=Rpq.get()
                p=[]
                while primes:
                    p+=[ppl(primes)]
                print("1",p)
                Pq.put(p)
            else:
                #threadWork(Jobs,Rq)
                pass

    elif NUM==2:
        Li={}
        Mi={}
        Curc=0
        Rl={}#Return list
        Rl[0]=[]

        while True:
            if not Rq.empty():
                print("C")
                n,i,c,x=Rq.get()
                print("2",x)
                if x[0]==0:
                    ppl(x)
                if x:
                    if c not in Li:
                        Li[c]=0
                        Mi[c]=n
                        Rl[c]=[]
                    if Curc==c and Li[c]==i:
                        Rpq.put(x)
                        Li[c]+=1
                        if Li[c]==Mi[c]:
                            print("@@@@@@@@@@@@@")
                            del Rl[c]
                            del Li[c]
                            del Mi[c]
                            Curc+=1
                            if Curc not in Rl:
                                Rl[Curc]=[]
                    else:
                        Rl[c]+=[[i,x]]
                        Rl[c].sort()
                    if Rl[Curc]:
                        print("???",Rl[Curc][0][0],Li[Curc])
                        while Rl[Curc][0][0]==Li[Curc]:
                            print("w",Rl[Curc][0][0])
                            i,x=Rl[Curc].pop(0)
                            Rpq.put(x)
                            Li[Curc]+=1
                            if i==Mi[Curc]:
                                print("!!!!!!!!!!!!!!")
                                del Rl[Curc]
                                del Li[Curc]
                                del Mi[Curc]
                                Curc+=1
                                Li[Curc]=0
                                if Curc not in Rl:
                                    Rl[Curc]=[]
                                    break
                            if not Rl[Curc]:
                                break
            else:
                #threadWork(Jobs,Rq)
                pass
            
    else:
        while True:
            doWork(Jobs,Rq)
            
        
        
            
        
    

if __name__ == "__main__":
    import sys
    print(sys.argv[0])

    
    Jobs=mp.Queue()
    CORES = max(3, mp.cpu_count())
    Rq= mp.Queue()#Return Queue
    p={}
    Rlenq=mp.Queue()#Return lenght Queue
    Rpq=Pq=mp.Queue()#Return Primes Queue
    Pq=mp.Queue()#Primes Queue
    for i in range(CORES):
        p[i] = mp.Process(target = worker, args=[Jobs,Rq,Rlenq,Rpq,Pq,CORES,i])
        p[i].start()
    for i in range(CORES):
        p[i].join()
