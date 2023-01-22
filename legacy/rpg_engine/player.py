from __future__ import annotations
from typing import Type, Union
from entities import Entity, Enemy, Lifeform
from item import Item, Equipable, Weapon
from world import Location
from copy import deepcopy

# This file handles player interactibility and player data.

class Player:
    def __init__(self, name:str, maxHealth: float, currentLocation:Type[Location] = None, weapon:Type[Item] = None, helmet:Type[Equipable] = None, torso:Type[Equipable] = None, leggings:Type[Equipable] = None, footwear:Type[Equipable] = None) -> None:
        self.name:str = name
        self.currentHealth:float = maxHealth
        self.maxHealth:float = maxHealth
        self.inventory:list = []
        self.currentWeapon:Weapon = weapon
        self.equipables:dict = {}
        self.currentLocation:Location = None
        
        # {
        #     "helmet":helmet,
        #     "torso":torso,
        #     "leggings":leggings,
        #     "footwear":footwear,
        # }
    
    def add_equipable_type(self, equipableTypeID:int = None) -> None:
        self.equipables.update(
            {equipableTypeID:None}
        )
        # for i in self.equipables:
        #     if equipableTypeID == i:
        #         return "Type already exists"
        #     else:
        #         self.equipables.update(
        #             {equipableTypeID:None}
        #         )
        #         return None
    
    def attack(self, entity:Type[Entity]) -> None:
        # Ignore NPC attacks.
        if entity is Enemy or entity is Lifeform:
            pass
    
    # To do: Change the item argument with a string type that would search into the database instead of passing it directly.
    def change_weapon(self, item:Type[Weapon]) -> Union[str, None]:
        for i in self.inventory:
            if i is Weapon and item.id == i.id and (i.isWeapon and item.isWeapon):
                self.currentWeapon = item
                return None
        return "No such item in inventory."
    
    def change_equipable(self, item:Type[Equipable]) -> Union[str, None]:
        for i in self.inventory:
            if i is Equipable and item.id == i.id and (i.isEquipable and item.isEquipable):
                self.armor[item.equipableType] = item
                return None
        return "No such item in inventory."
    
    def add_to_inventory(self, item:Type[Item]) -> Union[str, None]:
        if len(self.inventory) == 0:
            self.inventory.append(item)
        else:
            for i in self.inventory:
                if i.name == item.name and i.id == item.id and (item.amount + i.amount) <= i.maxStack:
                    i.amount += item.amount
                    return None
                elif i.name == item.name and i.id == item.id and (item.amount + i.amount) > i.maxStack:
                    difference = abs(item.amount - i.amount)
                    i.amount += difference
                    newItem = deepcopy(item)
                    newItem.amount = abs(difference - item.amount)
                    self.inventory.append(newItem)
                    return None
                else:
                    self.inventory.append(item)
                    return None
        return "Cannot add to inventory."
    
    def set_current_location(self, location:Type[Location]) -> None:
        self.currentLocation = location
    
    def get_current_location(self) -> str:
        return self.currentLocation

class Quest:
    pass
