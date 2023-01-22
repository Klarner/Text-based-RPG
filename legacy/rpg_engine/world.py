from __future__ import annotations
from typing import Type
from item import Item
from entities import Entity
# This file is the framework itself.

# The game manager itself that handles everything through its collected data.
class Location:
    def __init__(self, name:str, description:str,entities:list=[], itemsOnGround:list=[], north:Type[Location]=None, east:Type[Location]=None, south:Type[Location]=None, west:Type[Location]=None) -> None:
        self.name = name
        self.description = description
        self.entities = entities
        self.itemsOnGround = itemsOnGround
        self.locationDirections = {
            "north":north,
            "east":east,
            "south":south,
            "west":west,
        }
    
    def describe(self) -> str:
        return self.locationDirections
    
    def replace_location(self, north:Type[Location] = None, east:Type[Location] = None, south:Type[Location] = None, west:Type[Location] = None) -> None:
        # Note, if it's none, then it will not replace that location.
        if north != None:
            self.locationDirections["north"] = north
        
        if  east != None:
            self.locationDirections["east"] = east
        
        if south != None:
            self.locationDirections["south"] = south
        
        if west != None:
            self.locationDirections["west"] = west
    
    def place_entity(self, entity:Type[Entity]):
        self.entities.append(entity)
    
    def place_on_ground(self, item:Type[Item]):
        self.itemsOnGround.append(item)

# This has an economy.
class Settlement(Location):
    def __init__(self, name: str, description: str, entities: list = [], itemsOnGround: list = [], north: Type[Location] = None, east: Type[Location] = None, south: Type[Location] = None, west: Type[Location] = None, villagers:list = []) -> None:
        self.villagers = villagers
        super().__init__(name, description, entities, itemsOnGround, north, east, south, west)
