
import time

class Context: 
    """ 
        Context class which can define a single benchmark
        test or group units together. 
    """ 

    def __init__(self, **kwargs): 
        """ 
            Creates a new Context object. 

            Args: 
                ...
                **name (string) : 
                    The name of the benchmark set. 
                **description (string) : 
                    Brief description of what the benchmark is about. 
                ...
        """  

        # Parameters #
        self.name = \
            kwargs.get("name", self.default_context_name()) 
        self.description = \
            kwargs.get("description", self.default_context_description())


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
