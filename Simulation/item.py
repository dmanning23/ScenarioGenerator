class Item:
    """
    An item in the simulation that can be interacted with

    Attributes:
    name: string
        The name of the thing
    description: string
        A short description of the thing
    state: string
        The current state of the thing
    """
    def __init__(self, name, description, state):
        self.name = name
        self.description = description
        self.state = state

    def describe(self):
        return f"{self.name}: {self.description}. It is currently {self.state}"