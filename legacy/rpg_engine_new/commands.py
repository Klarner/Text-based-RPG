from __future__ import annotations
from typing import Type

class Logic:
    def activate(self) -> None:
        pass

class Command:
    def __init__(self, commands:list, logics:list, game) -> None:
        self.commands = commands
        self.logics = logics
        self.game = game
    
    def add_logic(self, logic:Type[Logic]) -> None:
        self.logics.append(logic)
    
    def execute(self, arguments:list) -> None:
        pass

    def set_game(self, game) -> None:
        self.game = game

#

class Describe(Command):
    def __init__(self) -> None:
        super().__init__(commands=["describe"], logics=[DescribingScene()], game=None)
    
    def execute(self, arguments: list) -> None:
        self.logics[0].activate(self.game)

class DescribingScene(Logic):
    def __init__(self) -> None:
        super().__init__()
    
    def activate(self, game) -> None:
        print("Hello, world!")

#

class Use(Command):
    def __init__(self) -> None:
        super().__init__(commands=["use"], logics=[], game=None)
    
    def execute(self, arguments: list) -> None:
        self.logics[0].activate(self.game)

class Using(Logic):
    def __init__(self) -> None:
        super().__init__()
    
    def activate(self, game) -> None:
        pass

describe = Describe()

commands = [describe]

