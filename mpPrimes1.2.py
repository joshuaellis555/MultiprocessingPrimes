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

def worker(jobs,r,CORES,NUM):
    if NUM==0:
        Primes=[3,5,7]
        iCP=0
        Li=iCP
        Returns={}
        Lens={}
        asdf=True
            
    
    if NUM==0:
        while True:
            if jobs.empty() and iCP<len(Primes)-1 and iCP<=Li+2:
                #print("1",end="")
                START=Primes[iCP]**2+2
                try:
                    END=Primes[iCP+1]**2-2
                except:
                    print(Primes[iCP+1],"\n",Returns)
                    while True:
                        pass
                numj=int((END-START+1)**.2)
                s=START
                for i in range(numj):
                    e=((END-s)//(numj-i))+s
                    e=e if e%2 else e+1
                    jobs.put([numj,iCP,s,e,Primes[:iCP+1]])
                    #print([numj,iCP,s,e,Primes[:iCP+1]])
                    s=e+2
                Returns[iCP]=[]
                Lens[iCP]=numj
                iCP+=1
                
                
            elif len(Returns[Li])==Lens[Li]:
                #print("2",end="")
                #st=time.time()
                #while time.time()<st+.5:
                while len(Returns[Li])!=0:
                    if len(Returns[Li][0])>0:
                        Primes+=[ppl(Returns[Li][0])]
                    else:
                        Returns[Li].pop(0)
                        
                del Returns[Li]
                print("The " + "{:,}".format(len(Primes)+1) + "'th prime is " + str(Primes[-1]))
                Li+=1
                if asdf==False:
                    print(Primes)
                    asdf=True
                                    
                                    
            elif not r.empty():
                #print("3",end="")
                while not r.empty():
                    try:
                        n,i,x=r.get(True,1)
                    except:
                        print("!!!")
                        break
                    if x[0]==0:
                        ppl(x)
                    Returns[i]+=[x]
                    if len(Returns[i])==n:
                        Returns[i].sort()
            #'''    
            elif False:
                #print("4",end="")
                try:
                    n,i,s,e,p=jobs.get(True,1)
                    #print("5",end="")
                    r.put([n,i,doPrimes(s,e,p)])
                except:
                    #print("6",end="")
                    pass
                    
            #'''
            
    elif NUM==1:
        #print("AFSDFASFDASFAFDSA")
        while True:
            n,i,s,e,p=jobs.get()
            a=[n,i,doPrimes(s,e,p)]
            #print(a)
            r.put(a)
    else:
        while True:
            n,i,s,e,p=jobs.get()
            r.put([n,i,doPrimes(s,e,p)])
    print(NUM)
        
        
            
        
    

if __name__ == "__main__":
    import sys
    print(sys.argv[0])

    jobs=mp.Queue()
    CORES=mp.cpu_count()
    r= mp.Queue()
    p={}
    for i in range(CORES):
        p[i] = mp.Process(target = worker, args=[jobs,r,CORES,i])
        p[i].start()
    for i in range(CORES):
        p[i].join()
