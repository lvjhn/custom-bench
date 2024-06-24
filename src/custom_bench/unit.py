import time 

import custom_bench.templates as templates
from .benchmark_item import BenchmarkItem

import copy

class Unit(BenchmarkItem): 
    """ 
        Unit class which can defines a single unit of 
        testing in a context.
    """ 

    def __init__(self, **kwargs): 
        """ 
            Creates a new Unit object.
        """  
        BenchmarkItem.__init__(self, **kwargs)

        # Parameters 
        self.name = \
            kwargs.get("name", self.default_unit_name()) 
        self.description = \
            kwargs.get("description", self.default_unit_description())
        self.context = \
            kwargs.get("context", None)
        self.parent = \
            self.context

        # Summary 
        self.summary = copy.deepcopy(templates.general_summary)

    def default_unit_name(self): 
        """ 
            Defines the default unit name when the `name`
            parameter is not passed when creating a context.
        """ 
        return f"unit-{time.time()}"

    def default_unit_description(self): 
        """ 
            Defines the default unit description when the 
            `description` parameter is not passed when creating
            a context.
        """ 
        return f"A random unit."
