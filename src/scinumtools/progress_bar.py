import numpy as np
from collections import deque
import time

class ProgressBar:
    current: int = 0    # current step
    nsteps: int         # number of steps
    times: deque        # list of step times
    ntimes: int = 20    # number of times for a sliding mean
    time_start: float   # starting time
    size: int = 70      # size of the progress bar
    
    def __enter__(self):
        return self
        
    def __exit__(self, type, value, traceback):
        self.close()
        
    def __init__(self, nsteps: int):
        self.nsteps = nsteps
        self.time_start = time.time()
        self.times = deque([self.time_start])
        print(f"|{self._info_text():{self.size}s}|")
        
    def _time_text(self, seconds):
        if seconds*2.777777e-4>=1:
            return f"{seconds*2.777777e-4:.1f}h"
        elif seconds*1.666666e-2>=1:
            return f"{seconds*1.666666e-2:.1f}m"
        else:
            return f"{seconds:.1f}s"
            
    def _info_text(self):
        text =  f"Step {self.current:d}/{self.nsteps:d}"
        if len(self.times)>1:
            times = np.array(self.times)
            dt = times[1:]-times[:-1]
            dt_mean = np.sum(dt)/len(dt)
            rt = dt_mean * (self.nsteps-self.current)
        else:
            rt = 0
        et = time.time()-self.time_start
        text += f" Time "+self._time_text(et)
        text += f"/"+self._time_text(rt+et)
        return text
        
    def close(self):
        self.current = self.nsteps-1
        self.step()
        
    def step(self, info: int = ''):
        self.current += 1
        # Get progress bar text
        pbar = self._info_text()
        if info:
            pbar += f"   {info}"
        # Clean previous line
        print("\033[A"+" "*(self.size+2)+f"\033[A")
        # Print a new line
        i = int(np.floor(self.size*self.current/self.nsteps))
        pbar = f"{pbar:{self.size}s}"
        pbar = "\033[;7m"+pbar[:i]+"\033[;0m"+pbar[i:]+"\033[;0m";
        print(f"|{pbar}|")
        # Update deque
        self.times.append(time.time())
        if len(self.times)>self.ntimes:
            self.times.popleft()
