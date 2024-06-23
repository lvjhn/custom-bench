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
            "skipped_duration" : 0, 
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

    def start(self): 
        """ 
            Marks the starting time of the benchmark. 
        """ 
        _time = time.process_time() 
        self.summary["start"] = _time

    def end(self, summarize = True): 
        """     
            Marks the ending time of the benchmark.
        """ 
        _time = time.process_time()
        self.summary["end"] = _time

    def start_skip(self): 
        """     
            Marks the start of a skipped portion. 
        """  