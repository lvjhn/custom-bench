
import time

from .unit import Unit
from .benchmark_item import BenchmarkItem
import custom_bench.templates as templates

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
        self.benchmark = \
            kwargs.get("benchmark", None)
        self.with_units = \
            kwargs.get("with_units", False)

        # Summary 
        self.summary = templates.general_summary.copy()

        # Units 
        self.units = templates.multi_items.copy()

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

    def has_unit(self, name): 
        """ 
            Checks if the current context has a unit with
            the specified name.
        """ 
        return name in self.units

    def unit(self, **kwargs):
        """ 
            Accesses currently existing unit or creates a new
            unit when it does not exist yet.
        """ 
        name = kwargs.get("name", None)
        description = kwargs.get("description", None)

        if not self.has_unit(name):
            return self.create_unit(name, description)
        else: 
            return self.units[name]

    def create_unit(self, name, description):
        """ 
            Creates a new unit with the specified name 
            and description.
        """ 
        
        # create new context
        unit = self.Unit(
            name=name, 
            description=description,
            context=self
        )

        # add context to context container
        self.units["n_items"] += 1
        self.units["items"][name] = unit 
        
        return unit