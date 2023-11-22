from Simulation.item import Item

class Location:
    """
    A class to represent a location in the simulated environment

    Attributes:
    name: string
        The name of the location
    description: string
        A short description of the location
    locations:
        A collection of places in this location. Can be empty
    items:
        A collection of things that can be interacted with in this environment.

    """
    def __init__(self, name, description, locations=None, items=None):
        self.name = name
        self.description = description
        self.locations = locations
        self.items = items

    def describe(self):
        return f"{self.name}: {self.description}"