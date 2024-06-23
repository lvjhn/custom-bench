import time 

class Benchmarker: 
    def __init__(self, **kwargs):
        self.name   = kwargs.get("name", time.time())
        self.outdir = kwargs.get("outdir", f"./benchmarks/{self.name}") 
        self.benchmarks = {}
    