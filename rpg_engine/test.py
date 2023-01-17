from __future__ import annotations
from typing import Type, Union
from engine import Game, Command, Logic
from player import Player
from item import Equipable, Weapon
from world import Location

# Doing something

class Do(Command):
    def __init__(self) -> None:
        super().__init__(commands=["do", "doing"], logics = [])
    
    def execute(self, arguments:list) -> None:
        self.logics[0].activate(arguments)

class PrintSomething(Logic):
    def __init__(self) -> None:
        super().__init__()
    
    def activate(self, text) -> None:
        print(text) # This shouldn't use print, but rather should return something or communicate directly with the game object.

# Go to and changing location

class GoTo(Command):
    def __init__(self, game:Game) -> None:
        self.game = game
        super().__init__(commands=["go"], logics=[])

    def execute(self, arguments: list) -> None:
        stringArgs = " ".join(arguments)
        self.logics[0].activate(stringArgs, self.game)
        

class ChangeLocation(Logic):
    # This shouldn't use print, but rather should return something or communicate directly with the game object.
    def __init__(self) -> None:
        super().__init__()
    
    def activate(self, location:str, game:Game) -> None:
        player = game.player
        currentLocation = player.get_current_location()
        newLocation = None
        for i in currentLocation.locationDirections:
            if currentLocation.locationDirections[i] != None:
                if currentLocation.locationDirections[i].name == location:
                    newLocation:Location = currentLocation.locationDirections[i]
                    player.set_current_location(newLocation)
                    print("You've gone to %s" % newLocation.name)
                    return None
        print("No such location")
        return None

# Changing Weapon

class Equip(Command):
    def __init__(self, game:Game) -> None:
        self.game = game
        super().__init__(commands=["equip"], logics=[])
    
    def execute(self, arguments: list) -> None:
        stringArgs = " ".join(arguments)
        self.logics[0].activate(stringArgs, self.game)

class ChangeEquipable(Logic):
    def __init__(self) -> None:
        super().__init__()
    
    def activate(self, item:str, game:Game) -> Union[str, None]:
        itemType = game.get_item_type(item)
        try:
            if itemType.isWeapon:
                playerItem = game.player.currentWeapon
                itemFromInventory = None
                for i in game.player.inventory:
                    if i.id == itemType.id:
                        itemFromInventory = i
                        break
                if playerItem != None:
                    if playerItem.id == itemFromInventory.id:
                        print("Item is already in use")
                        return "Item is already in use."
                    else:
                        game.player.currentWeapon = itemFromInventory
                        print("You've equipped %s" % itemFromInventory.name)
                        return None
                else:
                    game.player.currentWeapon = itemFromInventory
                    print("You've equipped %s" % itemFromInventory.name)
                    return None
        except:
            if itemType.isEquipable:
                for i in game.player.equipables:
                    slot = i
                    itemFromInventory = None
                    for z in game.player.inventory:
                        if z.id == itemType.id:
                            itemFromInventory = z
                            break
                    
                    if game.player.equipables[i] == None:
                        game.player.equipables[i] = itemFromInventory
                        print("You've equipped %s" % itemFromInventory.name)
                        return None
                    if itemFromInventory.id == game.player.equipables[i].id:
                        print("You've already equiped this item.")
                        return None
                    elif slot == itemType.equipableType:
                        game.player.equipables[i] = itemFromInventory
                        print("You've equipped %s" % itemFromInventory.name)
                        return None
                    else:
                        continue
            print("No such item found in inventory.")
            return "No such item found in inventory."


# Example of implementation.

# To do: Create logic and Player object.

game = Game()
game.processor.add_word_exclusion_list(["to"])

testHelmet = Equipable("iron helmet", 1, 1, 1, 1)
testTorso = Equipable("iron chestplate", 2, 1, 1, 2)
testLeggings = Equipable("iron leggings", 3, 1, 1, 3)
testReplaceHelmet = Equipable("gold helmet", 4, 1, 1, 1)
game.add_item_type(testHelmet)
game.add_item_type(testTorso)
game.add_item_type(testLeggings)
game.add_item_type(testReplaceHelmet)

sword = Weapon("iron sword", 5, 1, 1, 100.0)
dagger = Weapon("dagger", 6, 1, 1, 50.0)
game.add_item_type(sword)
game.add_item_type(dagger)

player = Player(name="test", maxHealth=100.0)
game.set_player(player=player)

game.player.add_equipable_type(1) # Helmet
game.player.add_equipable_type(2) # Torso
game.player.add_equipable_type(3) # Leggings

game.player.add_to_inventory(testHelmet)
game.player.add_to_inventory(testTorso)
game.player.add_to_inventory(testLeggings)
game.player.add_to_inventory(testReplaceHelmet)
game.player.add_to_inventory(sword)
game.player.add_to_inventory(dagger)

testLocation = Location("test location", "a debugging location")
testLocationNorthExtension = Location("test location north extension", "a nothern extension of the test location")
testLocation.replace_location(north=testLocationNorthExtension)
testLocationNorthExtension.replace_location(south=testLocation)
game.player.set_current_location(testLocation)

do = Do()
do.add_logic(PrintSomething())
game.processor.add_command(do)

goTo = GoTo(game=game)
goTo.add_logic(ChangeLocation())
game.processor.add_command(goTo)

equip = Equip(game=game)
equip.add_logic(ChangeEquipable())
game.processor.add_command(equip)

# Main event loop.
while True:
    userInput = str(input("What would you like to do? (Type quit if done): ")).lower()
    
    if userInput == "quit":
        break
    else:
        game.processor.process(userInput)
