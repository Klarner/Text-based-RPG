from prototype import Location, Player, Game, Item, EnemyQuestion, QuestionHandler, Question, Logic, NPC, Quest, QuestItem
from typing import Type

firstLocation = Location(id=1, name="test location 1", description="This is a cool place to test stuff.", items=[], entities=[])
secondLocation = Location(id=2, name="test location 2", description="This is also another cool place to test stuff.", items=[], entities=[])
firstLocation.change_north(secondLocation)
secondLocation.change_south(firstLocation)
player = Player(1, "test", 4, firstLocation)

class GoLogic(Logic):
    def __init__(self) -> None:
        super().__init__()
    
    def execute(self, player: Type[Player], arguments: list[str]) -> None:
        player.change_location(direction=arguments[0])

class UseLogic(Logic):
    def __init__(self) -> None:
        super().__init__()
    
    def execute(self, player: Type[Player], arguments: list[str]) -> None:
        itemIndex:int = player.get_item_name_index(itemName=" ".join(arguments))
        # print(itemIndex)
        if itemIndex != None:
            player.inventory[itemIndex].use(player)
            return None
        print("Item does not exist!\n")

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

# class TestItem(Item):
#     def __init__(self, id: int, name: str) -> None:
#         super().__init__(id, name)
    
#     def use(self, player: Type[Player]) -> None:
#         print("hello, world!")

# firstLocation.add_item_on_ground(TestItem(1, "test item"))

# questionHandler = QuestionHandler()
# testQuestion = Question("What's 1 + 1?", "2")
# questionHandler.add_question(testQuestion)

# testEnemy = EnemyQuestion(1, "test enemy", 1, questionHandler)
# firstLocation.add_entity_on_location(testEnemy)

testNPC = NPC(1, "John Doe", "Villager")
testNPC.add_dialogue("Hello there!")
testNPC.set_thanks_dialogue("Thank you so much! Here, take this test reward item.")

testQuestItem = QuestItem(1, "test quest item")
testReward = Item(2, "test reward item")
testQuest = Quest(questItem=testQuestItem, rewardItem=testReward)
testQuest.add_quest_dialogue("I need an item called test quest item. For it, I will give you test reward item.")
testNPC.set_quest(testQuest)

firstLocation.add_entity_on_location(testNPC)
secondLocation.add_item_on_ground(testQuestItem)

game = Game(player=player)

# print(testQuestItem.id)

game.add_command("go", GoLogic())
game.add_command("use", UseLogic())
game.add_command("take", PickUpLogic())
game.add_command("inventory", CheckInventoryLogic())
game.add_command("talk", TalkLogic())

game.run()
