import numpy as np

class ProgressBar:
    current: int = 0
    nitems: int
    ndigits: int
    prefix: str
    suffix: str
    def __enter__(self):
        return self
    def __exit__(self, type, value, traceback):
        self.current = self.nitems-1
        self.step()
    def __init__(self, nitems: int, prefix: str = 'Progress:'):
        self.nitems = nitems
        self.prefix = prefix
        self.ndigits = int(np.floor(np.log10(self.nitems)))
        print(self._info_text())
    def _info_text(self):
        return f"{self.prefix} {self.current:{self.ndigits}d}/{self.nitems:{self.ndigits}d}"
    def step(self, suffix: int = ''):
        self.current += 1
        pbar = self._info_text()+f"   {suffix}"
        nchar = len(pbar)
        i = int(np.floor(nchar*self.current/self.nitems))
        pbar = pbar[:i]+"\033[;0m"+pbar[i:]
        pbar =  "\033[A"+" "*nchar+f"\033[A\n\033[;7m{pbar}\033[;0m"
        print(pbar)
