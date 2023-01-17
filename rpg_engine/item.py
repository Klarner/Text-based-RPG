from __future__ import annotations
from typing import Type

# This file handles item management through the Item class and other accompanying classes.

class Item:
    def __init__(self, name:str, itemID:int, amount:int = 0, maxStack = 1) -> None:
        self.name = name
        self.id = itemID
        self.amount = amount
        self.maxStack = maxStack

class QuestItem(Item):
    def __init__(self, name: str, itemID: int, amount: int = 0, maxStack=1) -> None:
        self.isQuest = True
        super().__init__(name, itemID, amount, maxStack)

# Tools and weapons. If possible, add armor.
class Equipable(Item):
    def __init__(self, name: str, itemID: int, amount: int = 0, maxStack=1, equipableType:int = None) -> None:
        self.isEquipable = True
        self.equipableType = None

        if equipableType != None:
            self.equipableType = equipableType
        else:
            self.equipableType = 0

        super().__init__(name, itemID, amount, maxStack)

class Weapon(Equipable):
    def __init__(self, name: str, itemID: int, amount: int = 0, maxStack=1, damage:float = 0) -> None:
        self.isWeapon = True
        self.damage = damage
        super().__init__(name, itemID, amount, maxStack, equipableType=None)

class Tool(Equipable):
    def __init__(self, name: str, itemID: int, amount: int = 0, maxStack=1) -> None:
        self.isTool = True
        super().__init__(name, itemID, amount, maxStack, equipableType=None)
