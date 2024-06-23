import uuid 
import datetime 
import time

class BenchmarkItem:
    def __init__(self, **kwargs): 
        """
            Creates a benchmark item (either a Benchmark, Context, or Unit)
        """ 
        # Parameters #
        self.name = \
            kwargs.get("name", uuid.uuid4()) 
        self.description = \
            kwargs.get("description", "A simple benchmark.")
    
        # Automatically Initialized Variables # 
        self.run_datetime = \
            datetime.datetime.today().strftime("%Y-%m-%d %H:%M:%S")

        # Meta Info. # 
        self.meta = { 
            "name"        : self.name, 
            "description" : self.description 
        }

        # Summary Info. #
        self.summary = {
            "start" : None, 
            "end" : None, 
            "skipped" : 0, 
            "duration" : {
                "with_skipped" : 0,
                "no_skipped"   : 0
            }
        }

        # Combined State #
        self.state = {
            "meta"     : self.meta, 
            "summary"  : self.summary
        }

        # Other State Variables 
        self.misc = {
            "skip_start" : None
        }

    def info(self): 
        """ 
            Displays basic information about the benchmark.
        """     

        T  = "" 
        T += "BENCHMARK ITEM ()\n"
        T += "--------------------------------------------------\n"
        T += f"Name             : {self.name}\n"   
        T += f"Description      : {self.description}\n"
        T += f"Run Date/Time    : {self.run_datetime}\n"
        T += "--------------------------------------------------\n"

        return T

    def benchmark_time(self): 
        """ 
            Gets the current benchmark time.
        """ 
        return time.process_time()

    def start(self): 
        """ 
            Marks the starting time of the benchmark. 
        """ 
        _time = self.benchmark_time()
        self.summary["start"] = _time

        self.after_start_fn()

    def end(self, summarize = True): 
        """     
            Marks the ending time of the benchmark.
        """ 
        _time = self.benchmark_time()
        self.summary["end"] = _time

        self.after_end_fn() 

    def skip_start(self): 
        """     
            Marks the start of a skipped portion. 
        """  
        _time = self.benchmark_time()
        self.misc["skip_start"] = _time 

        self.after_skip_start_fn()

    def skip_end(self): 
        """ 
            Marks the end of a skipped portion.
        """ 
        skip_end        = self.benchmark_time() 
        skip_start      = self.misc["skip_start"] 
        skip_duration   = skip_end - skip_start 

        self.summary["skipped"] += skip_duration 
        
        self.after_skip_end_fn(skip_duration)

        return skip_duration

    def after_skip_start_fn(self, duration): 
        """ 
            This function gets called after a skip
            portion has been marked as ended.
        """ 
        pass

    def after_skip_end_fn(self, duration): 
        """ 
            This function gets called after a skip
            portion has been marked as ended.
        """ 
        pass
    
    def after_start_fn(self):
        """ 
            This function gets called after 
            the benchmark item has been marked as started.
        """ 
        pass 

    def after_end_fn(self):
        """     
            This function gets called after the
            benchmark item has been marked as ended.
        """ 
        pass