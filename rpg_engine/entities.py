from __future__ import annotations
from typing import Type, Union
from item import Weapon

# This file handles the entities of the world.

class Entity:
    # Entity can only use one weapon and doesn't have an inventory.
    def __init__(self, name:str, maxHealth:float, weapon:Type[Weapon] = None) -> None:
        self.name = name
        self.currentHealth = maxHealth
        self.maxHealth = maxHealth
        self.weapon = weapon

class Enemy(Entity):
    def __init__(self, name: str, maxHealth: float, weapon: Type[Weapon] = None) -> None:
        self.isEnemy = True
        super().__init__(name, maxHealth, weapon)

# Create the dialogue system
class NPC(Entity):
    def __init__(self, name: str, maxHealth: float, weapon: Type[Weapon] = None) -> None:
        self.isEnemy = True
        super().__init__(name, maxHealth, weapon)

# Animals, supernaturals that's not part of the NPC class, etc.
class Lifeform(Entity):
    # Can either attack back or not with their weapon. Their weapon can be claws if they're an animal.
    def __init__(self, name: str, maxHealth: float, weapon: Type[Weapon] = None) -> None:
        self.isLifeform = True
        self.canAttack = False
        super().__init__(name, maxHealth, weapon)
