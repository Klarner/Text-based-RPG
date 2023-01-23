from __future__ import annotations
from typing import Type, Union

class Entity:
    def __init__(self, id:int, name:str) -> None:
        self.id:int = id
        self.name:str = name
    
    def behavior(self) -> None:
        pass

class NPC(Entity):
    def __init__(self, id: int, name: str) -> None:
        super().__init__(id, name)
    
    def behavior(self) -> None:
        return super().behavior()
    
    def dialogue(self) -> None:
        pass

    def quest(self) -> None:
        pass

class Enemy(Entity):
    def __init__(self, id: int, name: str, maxHealth:float) -> None:
        self.currentHealth:float = maxHealth
        self.maxHealth:float = maxHealth
        super().__init__(id, name)
    
    def behavior(self) -> None:
        return super().behavior()
    
    # Prompt quiz. This will activate once the player will enter the location.
    def attack(self) -> None:
        pass
