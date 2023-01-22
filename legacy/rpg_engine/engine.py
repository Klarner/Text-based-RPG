from __future__ import annotations
from typing import Type, Union
from item import Item
from player import Player
# This handles the engine processing of the game.

# Make sure that the game class initializes everything.
# The operation that needs to be done is that when a developer makes the game, the developer needs to create a game instance with a game logic that's part of the argument.
# Or the logic itself can be added through something like game.add_logic(). Logcis ensures the flow and mechanics of the game.

class Game:
    def __init__(self, player:Player = None) -> None:
        self.player = player
        self.processor = TextProcessor()
        self.itemTypeList = []
    
    def add_item_type(self, item:Type[Item]) -> Union[str, None]:
        self.itemTypeList.append(item)

    def get_item_type(self, item:str) -> Union[Type[Item], None]:
        for i in self.itemTypeList:
            if i.name == item:
                return i
        return None

    def set_player(self, player:Player) -> None:
        self.player = player

class Logic:
    def activate(self) -> None:
        pass

class Command:
    def __init__(self, commands:list, logics:list) -> None:
        self.commands = commands
        self.logics = logics
    
    def add_logic(self, logic:Type[Logic]) -> None:
        self.logics.append(logic)
    
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
