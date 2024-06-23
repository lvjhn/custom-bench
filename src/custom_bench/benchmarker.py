import uuid
import datetime
import time

from .context import Context
from .benchmark_item import BenchmarkItem
import custom_bench.templates as templates

class Benchmarker(BenchmarkItem):
    """ 
        Benchmarker class used to create a group of benchmark contexts. 
    """

    def __init__(self, **kwargs):
        """ 
            Creates a new benchmarker object.
        """ 
        self.Context = kwargs.get("Context", Context) 

        BenchmarkItem.__init__(self, **kwargs)
        
        # Contexts associated with this benchmark
        self.contexts = templates.multi_items.copy()

        # Combine different substates together 
        self.state["contexts"] = self.contexts
       
    def has_context(self, name): 
        """ 
            Checks if the current benchmark has a context 
            named `name` associated with it.
        """ 
        return name in self.contexts

    def context(self, **kwargs):
        """ 
            Accesses currently existing context or creates a new
            context when it does not exist yet.
        """ 
        name = kwargs.get("name", None)
        description = kwargs.get("description", None)
        with_units = kwargs.get("with_units", True)

        if not self.has_context(name):
            return self.create_context(name, description, with_units)
        else: 
            return self.contexts[name]

    def create_context(self, name, description, with_units): 
        """ 
            Creates a new context with the specified name 
            and description.
        """ 
        
        # create new context
        context = self.Context(
            name=name, 
            description=description,
            with_units=with_units
        )

        # add context to context container
        self.contexts["n_items"] += 1
        self.contexts["items"][name] = context 
        
        return context


   

