
class Context: 
    """ 
        Unit class which can defines a single unit of 
        testing in a context.
    """ 

    def __init__(self, **kwargs): 
        """ 
            Creates a new Unit object. 

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
            kwargs.get("name", self.default_unit_name()) 
        self.description = \
            kwargs.get("description", self.default_unit_description())


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
