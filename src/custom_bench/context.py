
import time

from .unit import Unit
from .benchmark_item import BenchmarkItem

class Context(BenchmarkItem): 
    """ 
        Context class which can define a single benchmark
        test or group units together. 
    """ 

    def __init__(self, **kwargs): 
        """ 
            Creates a new Context object. 
        """ 
        self.Unit = kwargs.get("Unit", Unit)

        BenchmarkItem.__init__(self, **kwargs)

        # Parameters 
        self.name = \
            kwargs.get("name", self.default_context_name()) 
        self.description = \
            kwargs.get("description", self.default_context_description())

        # Summary 
        self.summary = {
            "start" : None, 
            "end" : None,
            "skipped" : 0, 
            "duration" : {
                "with_skipped" : 0,
                "no_skipped" : 0
            }
        }

        # Units 
        self.units = {
            "meta" : {
                "n_units" : 0,
            },  
            "summary" : {
                
            }
        }

        # Base state 
        self.state = {
            "summary" : self.summary, 
            "units" : self.units
        }



    def default_context_name(self): 
        """ 
            Defines the default context name when the `name`
            parameter is not passed when creating a context.
        """ 
        return f"context-{time.time()}"

    def default_context_description(self): 
        """ 
            Defines the default context description when the 
            `description` parameter is not passed when creating
            a context.
        """ 
        return f"A simple demo benchmark."
