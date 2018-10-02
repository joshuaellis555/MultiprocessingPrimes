#import math as M
import multiprocessing as mp
import time

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
    l=list(range(START,END+1,2))
    ln=len(l)
    for prime in PRIMES:
        s=-(-START//prime)*prime
        for i in range(((s if s%2 else s+prime)-START)//2,ln,prime):
            l[i]=0
    return l
    
def ppl(l):
    r=l.pop(0)
    ln=len(l)
    while ln>0 and l[0]==0:
        ln-=1
        l.pop(0)
    return r

def worker(jobs,r,CORES,NUM):
    if NUM==0:
        Primes=[3,5,7,11,13]
        iCP=len(Primes)-2
        Returns=[]
        asdf=False
            
    
    if NUM==0:
        while True:
            if jobs.empty() and iCP<len(Primes)-1:
                START=Primes[iCP]**2
                END=Primes[iCP+1]**2
                numj=int((END-START+1)**.5)
                s=START
                for i in range(numj):
                    e=((END-s)//(numj-i))+s
                    jobs.put([numj,s,e,Primes[:iCP]])
                    s=e+1
                iCP+=1
                
                
            elif len(Returns):
                #st=time.time()
                #while time.time()<st+.5:
                for t in range(100):
                    Primes+=[ppl(Returns[0])]
                    if len(Returns[0])==0:
                        Returns.pop(0)
                        if len(Returns)==0:
                            print("the",len(Primes)+1,"th prime is",Primes[-1])
                            if asdf==False:
                                print(Primes)
                                asdf=True
                            break
                                    
                                    
            elif not r.empty():
                x=r.get()
                n,x=x
                if x[0]==0:
                    ppl(x)
                Returns+=[x]
                for i in range(n-1):
                    t,x=r.get()
                    if x[0]==0:
                        ppl(x)
                        Returns+=[x]
                print("a",len(Returns),n)
                Returns.sort()
                
            else:
                try:
                    n,s,e,p=jobs.get(True,1)
                    r.put([n,doPrimes(s,e,p)])
                except:
                    pass
            
    else:
        while True:
            n,s,e,p=jobs.get()
            r.put([n,doPrimes(s,e,p)])
        
        
            
        
    

if __name__ == "__main__":
    print('mp 1.1')

    jobs=mp.Queue()
    CORES=mp.cpu_count()
    r= mp.Queue()
    for i in range(1,CORES,1):
        p = mp.Process(target = worker, args=[jobs,r,CORES,i])
        p.start()
    worker(jobs,r,CORES,0)
