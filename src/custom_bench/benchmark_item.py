import uuid 
import datetime 
import time
import copy

import custom_bench.templates as templates

from .summarizer import Summarizer

class BenchmarkItem:

    def __init__(self, **kwargs): 
        """
            Creates a benchmark item (either a Benchmark, Context, or Unit)
        """ 
        # Parameters 
        self.name = \
            kwargs.get("name", uuid.uuid4()) 
        self.description = \
            kwargs.get("description", "A simple benchmark item.")
        self.datetime_format = \
            kwargs.get("datetime_format", "%Y-%m-%d %H:%M:%S")
        self.Summarizer = \
            kwargs.get("Summarizer", Summarizer)

        # Create summarizer
        self.summarizer = self.Summarizer(self)
    
        # Items Configuration
        self.has_items = kwargs.get("has_items", False) 
        self.items_name = kwargs.get("items_name", None)

        # Automatically Initialized Variables 
        self.run_datetime = \
            datetime.datetime.today().strftime(self.datetime_format)

        # Meta Info. 
        self.meta = { 
            "name"        : self.name, 
            "description" : self.description,
            "ran_at"      : self.run_datetime
        }

        # Summary Info. 
        self.summary = copy.deepcopy(templates.general_summary)

        # Combined State 
        self.state = {
            "meta"     : self.meta, 
            "summary"  : self.summary
        }

        # Other State Variables 
        self.misc = {
            "skip_start" : None
        }

        # Parent (Optional)
        self.parent = None

        # No. of Children 
        self.n_children = 0

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

    def after_skip_start_fn(self): 
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
        if self.parent:
            self.parent.add_skip_time(duration)
            return True 
        else: 
            return False
    
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
        self.summarizer.summarize()

    def add_skip_time(self, skip_time): 
        """     
            Adds skip time to the currently tracked
            skip time when a contained item has marked
            its end of a skipped portion.
        """ 
        self.summary["skipped"] += skip_time
         
    def children(self): 
        """ 
            Gets the items in the current benchmark item.
        """ 
        return self.state["children"]["items"]  

    def add_children(self): 
        """ 
            Adds a children, increments the children count 
            `n_children`.
        """ 
        self.n_children += 1

    def collect(self): 
        """ 
            Transforms benchmark state into a JSON serializable
            object. Extracting states from BenchmarkItem based 
            component classes. 
        """ 
        root        = self.state 
        has_items   = self.has_items 

        if has_items: 
            items       = self.state["children"]["items"]
            root_items  = root["children"]["items"] 
            for item in items: 
                root_items[item] = items[item].collect() 

        return root