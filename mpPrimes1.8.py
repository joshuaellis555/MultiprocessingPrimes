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
    JTq.put(True)#Report back that a job was taken (mandel: ignore this)
    doPrimes(c,s,e,p,Rq)

def tryWork(Jobs,JTq,Rq):#not used in this program
    try:
        c,s,e,p=Jobs.get(True,0)
        JTq.put(True)#Report back that a job was taken (mandel: ignore this)
        doPrimes(c,s,e,p,Rq)
    except:
        pass


'''
mpPrimes has n threads consisting of 1 main thread(thread 0) and
    n-1 worker threads. mpPrimes calculates new primes based on old primes
    and is intended to run forever.
    
    The mandelbrot set program will only run while needing to render a
    new image. The workers should be the same, each should constanly look
    for new jobs to do and wait if there are none. The big difference will
    be the main thread which only needs to create all the jobs at the begining,
    sort the list of compleated jobs at the end, and add the line's data to the
    graph to create the image.

    I think workers equal to mp.cpu_count() should be created at runtime and not
    closed and recreated each new render.

    the main process should be created each time a new image is rendered
    and closed when done. It will recieve the jobs que as an argument and use
    it to send the workers jobs.
    
    Once the multiprocessing and GUI parts of the project get combined we may
    need to  make sure we only render one image at a time.
'''
def worker(Jobs,JTq,Rq,CORES,NUM):
    if NUM==0:
        Primes=[2,3,5,7]

        def queueJobs(Primes,Jobs,JTq):
            iCP=1#index Current Prime
            JobNo=1
            SIZEGOAL=10000
            while True:
                if iCP < len(Primes)-1:
                    JTq.get()
                    START=Primes[iCP]**2+2
                    #print(JobNo,iCP,(len(Primes)-1-iCP+8)//8,START,end=" ")
                    iCP=min(iCP+4,len(Primes)-1)
                    END=Primes[iCP]**2-2
                    #print(END,iCP)
                    Jobs.put([JobNo,START,END,Primes[1:iCP]])
                    JobNo+=1

        #creates a thread on this process that just makes jobs
        t = threading.Thread(target = queueJobs, args=[Primes,Jobs,JTq])
        t.start()
        
        update=time.time()
        rate=1
        
        Rl={}#Return list
        C=1

        while True:
            #just fill a return list with lines and sort at the end
            x=Rq.get()
            if x[0]==C:
                Primes+=x[1]
                C+=1
            else:
                Rl[x[0]]=x
            while C in Rl:
                Primes+=Rl[C][1]
                del Rl[C]
                C+=1
            ''' for the mandelbort set just fill a queue with the lines and use
                lines.sort() ones all the lines have been gathered ie: len(lines == SIZE)
            '''
            
            if time.time()>=update+rate:
                update+=rate
                print("The " + "{:,}".format(len(Primes)) + "'th prime is " + str(Primes[-1]))

    
    else:
        while True:
            doWork(Jobs,JTq,Rq)
            
        
        
            
        
    

if __name__ == "__main__":
    import sys
    print(sys.argv[0])
    
    Jobs=mp.Queue()
    CORES = max(4, mp.cpu_count())
    Rq= mp.Queue()#Return Queue
    JTq=mp.Queue()#Job Taken Queue
    for i in range(CORES*2):
        JTq.put(True)
    p={}
    for i in range(CORES):
        p[i] = mp.Process(target = worker, args=[Jobs,JTq,Rq,CORES,i])
        p[i].start()
    for i in range(CORES):
        p[i].join()
