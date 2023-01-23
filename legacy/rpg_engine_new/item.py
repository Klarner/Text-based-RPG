from __future__ import annotations
from typing import Union

# This file handles item management through the Item class and other accompanying classes.

class Item:
    def __init__(self, name:str, itemID:int, amount:int = 0, maxAmount:int = 1) -> None:
        self.name = name
        self.id = itemID
        self.amount = amount
        self.maxAmount = maxAmount
    
    def check_max(self, amount:int) -> bool:
        if amount + self.amount > self.maxAmount:
            return False
        return True
    
    def check_min(self, amount:int) -> bool:
        if amount - self.amount < 0:
            return False
        return True

    def add_to_amount(self, amount:int) -> Union[str, None]:
        if self.check_max(amount=amount):
            self.amount += amount
            return None
        return "The item is at max already."
    
    def remove_from_amount(self, amount:int) -> Union[str, None]:
        if self.check_min(amount):
            self.amount -= amount
            return None
        return "Cannot remove item as what you're asking is too big than what this item already has."
    
    def use(self) -> None:
        pass

class QuestItem(Item):
    def __init__(self, name: str, itemID: int, amount: int = 0, maxStack=1) -> None:
        self.isQuest = True
        super().__init__(name, itemID, amount, maxStack)
