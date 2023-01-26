# First, import everything from rpg_lib.py
from rpg_lib import *

# Second, create a location.
firstLocation = Location(id=1, name="test location 1", description="This is a cool place to test stuff.", items=[], entities=[])
secondLocation = Location(id=2, name="test location 2", description="This is also another cool place to test stuff.", items=[], entities=[])

# If you want to set the location of a certain direction, do the following:
firstLocation.change_north(secondLocation)
secondLocation.change_south(firstLocation)

# Third, make the player. The "test" string is the name of the player. The third argument is its lives. And the final argument is its current location.
# The first argument is the ID, ignore that as that's for special use for the engine.
player = Player(1, "test", 4, firstLocation)

# If you want to create a custom item with custom behavior, use this code below.
# The use method is how you would use the item.
class TestItem(Item):
    def __init__(self, id: int, name: str) -> None:
        super().__init__(id, name)
    
    def use(self, player: Type[Player]) -> None:
        player.add_health(amount=2)

# The first argument is the ID. Again, for special case. As for the second argument, it's the name of the item.
testItem = TestItem(1, "test item")

# This is how you would declare a 'normal item'. A normal item doesn't have a use method, it just exist.
testItem2 = Item(2, "an item")

# If you want to create your own custom command, do the following:
class UseLogic(Logic):
    # Initialize everything and inherit from the Logic class.
    def __init__(self) -> None:
        super().__init__()
    
    # This method is responsible for using items. Every execute method needs a player argument and an arguments list.
    # The purpose of the player argument is to interact with the player directly.
    # The purpose of the arguments list is to process what the player is trying to command.
    # For example, if the player says "use test quest item".
    # The test quest item is within the arguments list and are split.
    # We use the .join() method to join them together in order to find that item in the player's inventory.
    def execute(self, player: Type[Player], arguments: list[str]) -> None:
        itemIndex:int = player.get_item_name_index(itemName=" ".join(arguments))
        if itemIndex != None:
            player.inventory[itemIndex].use(player)
            return None
        print("Item does not exist!\n")

# Below are commands that will be useful to the game.
class GoLogic(Logic):
    def __init__(self) -> None:
        super().__init__()
    
    def execute(self, player: Type[Player], arguments: list[str]) -> None:
        player.change_location(direction=arguments[0])

class PickUpLogic(Logic):
    def __init__(self) -> None:
        super().__init__()
    
    def execute(self, player: Type[Player], arguments: list[str]) -> None:
        itemsOnGround:list[Type[Item]] = player.currentLocation.items
        itemName:str = " ".join(arguments)
        for i in itemsOnGround:
            if i.name == itemName:
                player.add_item_to_inventory(item=i)
                player.currentLocation.items.remove(i)
                print("{} has been added to your inventory.\n".format(i.name))
                return None
        else:
            print("No such item on the ground.\n")
            return None

class CheckInventoryLogic(Logic):
    def __init__(self) -> None:
        super().__init__()
    
    def execute(self, player: Type[Player], arguments: list[str]) -> None:
        print("\nThe Items on your inventory are...")
        print(", ".join(i.name for i in player.inventory))
        print()

class TalkLogic(Logic):
    def __init__(self) -> None:
        super().__init__()
    
    def execute(self, player: Type[Player], arguments: list[str]) -> None:
        npcName = " ".join(arguments)
        for i in player.currentLocation.entities:
            if i.name.lower() == npcName:
                print()
                i.behavior(player)

# Exercise, try to create a help method that gathers all of the commands and print it.
class HelpLogic(Logic):
    def __init__(self, game:Game) -> None:
        self.game = game
        super().__init__()
    
    def execute(self, player: Type[Player], arguments: list[str]) -> None:
        commands = self.game.commands
        # complete this

# In order to create an enemy, you must first create a question handler object.
questionHandler = QuestionHandler()

# If you want to add question, make a question object.
# The first argument is the question and the second one is the answer. The second one must be a string.
testQuestion = Question("What's 1 + 1?", "2")

# In order to add testQuestion to the question handler object, do the following:
questionHandler.add_question(testQuestion)

# If you want to create an enemy, use the Enemy object.
# The enemy object has four arguments.
# The first is the ID, it must be unique.
# The second is the name of the enemy.
# The third is the lives of the enemy. This will be reduced everytime the player answers correctly.
# And finally, the fourth. This contains every question possible to prompt to the player.
testEnemy = EnemyQuestion(1, "test enemy", 1, questionHandler)
firstLocation.add_entity_on_location(testEnemy)

# If you want to create an NPC, do the following.
testNPC = NPC(1, "John Doe", "Villager")
# This adds a dialogue.
testNPC.add_dialogue("Hello there!")
# This creates a quest item.
testQuestItem = QuestItem(1, "test quest item")
# A reward item that's a 'normal item'.
testReward = Item(2, "test reward item")
# This creates a quest, it takes in a quest item to be fulfilled and a reward item to be rewarded.
testQuest = Quest(questItem=testQuestItem, rewardItem=testReward)
# This adds a quest dialogue that hints to the player on what to do
testQuest.add_quest_dialogue("I need an item called test quest item. For it, I will give you test reward item.")
# And finally, this sets the quest to the NPC.
testNPC.set_quest(testQuest)
# This adds a thanks dialogue whenever the quest is complete.
testNPC.set_thanks_dialogue("Thank you so much! Here, take this test reward item.")

# If you want to add an entity or an item, use the add_entity/item_on_location method.
# If you want to add a list, use the add_entities_on_location and add_items_on_location.
# Both of these methods takes a list.
firstLocation.add_entity_on_location(testEnemy)
firstLocation.add_entity_on_location(testNPC)
secondLocation.add_item_on_ground(testQuestItem)

# If you're finally done, create the game object and set its player to the player object that you've created.
game = Game(player=player)

# Note that every time you create a logic, you need to add a command with its accompanying caller.
# The first argument is the caller and the second argument is the Logic you've created.
game.add_command("go", GoLogic())
game.add_command("use", UseLogic())
game.add_command("take", PickUpLogic())
game.add_command("inventory", CheckInventoryLogic())
game.add_command("talk", TalkLogic())

# The help logic for the exercise that you've done.
game.add_command("help", HelpLogic())

# If you're finally done, run the game.
# You can do this without the __name__ thingy.
if __name__ == '__main__':
    playerName = str(input("What is your name, young one?"))
    player.set_name(playerName)
    print("I see, nice to meet you {}!".format(player.get_name()))
    game.run()
