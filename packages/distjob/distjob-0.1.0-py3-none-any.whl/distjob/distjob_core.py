



##### Two threads -> one for receiving jobs and responding about the status, second for execution


import queue
import threading
import time
import sys



threads=[]


class Thread(threading.Thread):
    def __init__(self,name,function,args,frequency=0.5,daemon=True):
        super().__init__(daemon=daemon)
        self.name=name
        self.exit_flag=False
        self.function=function
        self.args=args
        self.frequency=frequency
        
    def run(self):
        print(f"Starting: {self.name}")

        
        while not self.exit_flag:
            self.function(self.args)
            
            time.sleep(self.frequency)
        print(f"Exiting: {self.name}")
        
    def run_function(self,function):
        function()
        
    
    

from distjob_context import djc
class DistJobServer:
    
    def __init__(self,host="0.0.0.0",port=10100):
        self.host=host
        self.port=port
        
        
        djc.host=host
        djc.port=port

        
        global threads
        
           
        
        print("Main Thread")
        
        lock=threading.Lock()
        queue1=queue.Queue()
        
        def run_api(args):
            from distjob_api import run_api
            run_api()
            print("API RUNNING!")
            
        
        def new_thread(name,function,function_args,frequency=0.5):
            global threads
            thread=Thread(name,function,function_args,frequency)
            threads.append(thread)
            thread.start()
        
        
        def run_worker(args): #needs to have one parameter
            from distjob_worker import run
            try:
                run()
            except (KeyboardInterrupt, SystemExit): #close thread on CTRL+C
                djc.ARE_ALL_THREADS_FINISHED=True
                sys.exit()
       
        
    
        new_thread("ApplicationThread-1",run_worker,1)
        
            
        print("LOADING DISTJOB API...")
        new_thread("APIThread-4",run_api,None,10)
        time.sleep(1)
        
        
        
        
        def check_for_finishing_of_threads(args):
            print("CHECK",args,djc.ARE_ALL_THREADS_FINISHED)
            if djc.ARE_ALL_THREADS_FINISHED:
                for thread in threads:
                    thread.exit_flag=True
                    thread.join()
                
        
        new_thread("ThreadingMonitoringThread-6",check_for_finishing_of_threads,None,3)
        time.sleep(1)
        
    
        time.sleep(1)
         
        
        
        for thread in threads:
            thread.exit_flag=True
            thread.join()
        
        
        print("Exiting Main Thread")

        

if __name__=="__main__":
    
    try:
        dist_job_server=DistJobServer(port=djc.port)
    except (KeyboardInterrupt, SystemExit): #close thread on CTRL+C
        djc.ARE_ALL_THREADS_FINISHED=True
        sys.exit()