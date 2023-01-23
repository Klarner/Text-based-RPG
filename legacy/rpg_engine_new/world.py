from __future__ import annotations
from typing import Type, Union
from rpg_engine.entities import Entity
from rpg_engine.item import Item

# maps out different locations.
class World:
    pass

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
