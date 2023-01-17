from __future__ import annotations
from typing import Type, Union

# Basic functions of the game for engine.py

class Game:
    pass

class Logic:
    def activate(self) -> None:
        pass

class Command:
    def __init__(self, commands:list) -> None:
        self.commands = commands
    
    def execute(self, arguments:list) -> None:
        pass

class WordExclusionList:
    def __init__(self, wordList:list=[]) -> None: # mainly includes prepositions.
        self.wordList = wordList

class TextProcessor():
    def __init__(self) -> None:
        self.commands:list = []
        self.wordList:list = []
    
    def add_command(self, command:Type[Command]) -> None:
        self.commands.append(command)
    
    def add_word_exclusion_list(self, wordList:list) -> None:
        self.wordList.append(WordExclusionList(wordList))
    
    def check_command(self, command:str, arguments:list) -> Union[bool, None]:
        for i in self.commands:
            for z in i.commands:
                if z == command:
                    i.execute(arguments)
                    return None
            # if i.command == command:
            #     i.execute(arguments)
            #     return None
        return True
    
    def process(self, text: str) -> None:
        token = text.split(" ")
        firstCommand = token[0]
        
        arguments = []
        token.remove(firstCommand)
        for i in token:
            arguments.append(i)
        
        for i in arguments:
            for z in self.wordList:
                for y in z.wordList:
                    if i == y:
                        arguments.remove(i)
        
        if self.check_command(firstCommand, arguments):
            print("Error, no such command: %s" % firstCommand) # This shouldn't use print, but rather should return something or communicate directly with the game object.

# Game manager for world.py

class World:
    pass

# Locations and place handling for world.py

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

class Settlement(Location):
    def __init__(self, name: str, description: str, entities: list = [], itemsOnGround: list = [], north: Type[Location] = None, east: Type[Location] = None, south: Type[Location] = None, west: Type[Location] = None, villagers:list = []) -> None:
        self.villagers = villagers
        super().__init__(name, description, entities, itemsOnGround, north, east, south, west)

# Entities and handling entities for entities.py.

class Entity:
    def __init__(self, name:str, maxHealth:float) -> None:
        self.name = name
        self.currentHealth = maxHealth
        self.maxHealth = maxHealth

class Enemy(Entity):
    pass

class NPC(Entity):
    pass

class Lifeform(Entity):
    pass

# Player and player handling for player.py.

class Player:
    def __init__(self, name:str, maxHealth: float) -> None:
        self.name = name
        self.currentHealth = maxHealth
        self.maxHealth = maxHealth
        self.inventory = []
        self.currentWeapon = None
    
    def attack(self, entity:Type[Entity]):
        # Ignore NPC attacks.
        if entity is Enemy or entity is Lifeform:
            pass

# Handling quests and missions.

class Quest:
    pass

# Handling items and quest items for item.py.

class Item:
    pass

class QuestItem(Item):
    def __init__(self) -> None:
        super().__init__()

# Example usage.

processor = TextProcessor()
processor.add_word_exclusion_list(["to"])

class Do(Command):
    def __init__(self) -> None:
        super().__init__(commands=["do", "doing"])
        self.logics = []
    
    def add_logic(self, logic: Type[Logic]):
        self.logics.append(logic)
    
    def execute(self, arguments:list) -> None:
        self.logics[0].activate(arguments)

class GoTo(Command):
    def __init__(self) -> None:
        super().__init__(commands=["go"])
    
    def execute(self, arguments: list) -> None:
        # Reference the player to change its current location with a logic.
        pass

class PrintSomething(Logic):
    def __init__(self) -> None:
        super().__init__()
    
    def activate(self, text) -> None:
        print(text) # This shouldn't use print, but rather should return something or communicate directly with the game object.

class ChangeLocation(Logic):
    def __init__(self) -> None:
        super().__init__()
    
    def activate(self) -> None:
        # Reference the player directly to change its current location.
        pass

# Example of implementation.

do = Do()
do.add_logic(PrintSomething())
processor.add_command(do)

while True:
    userInput = str(input("What would you like to do? (Type quit if done): ")).lower()
    
    if userInput == "quit":
        break
    else:
        processor.process(userInput)
