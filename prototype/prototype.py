from __future__ import annotations
from typing import Type, Union, Any
from copy import deepcopy
from random import choice

class Game:
    def __init__(self, player:Type[Player]) -> None:
        self.commands:list[dict[str, Type[Logic]]] = [] # str is the command to call, Type[Logic] is the logic to be executed.
        self.player:Type[Player] = player

    def set_player(self, player:Type[Player]) -> None:
        self.player = player

    def add_command(self, command:str, logic:Type[Logic]):
        self.commands.append({command:logic})

    def run(self) -> None:
        while True:
            # self.describe()
            if not self.check_player_alive():
                break
            
            userInput = str(input("What would you like to do: ")).lower()

            try:
                match userInput:
                    case "quit":
                        break
                    case other:
                        self.process(userInput)
            except:
                print("An error has occured. But you can still play the game.")

    def process(self, userInput:str) -> None:
        arguments = userInput.split(" ")
        commandCaller = arguments[0]
        arguments.pop(0)

        if commandCaller == "describe":
            self.describe()
            return None
        
        if commandCaller == "":
            return None

        for i in self.commands:
            for _, (j, x) in enumerate(i.items()):
                if commandCaller == j:
                    x.execute(player=self.player, arguments=arguments)
                    return None
        else:
            print("Command not found {}".format(commandCaller))
            return None
    
    def describe(self) -> None:
        # print(self.player.currentLocation.entities)
        self.player.currentLocation.describe(self.player)
        direction = ["north", "east", "south", "west"]
        print("places to go...")
        for i in direction:
            loc:Type[Location] = self.player.currentLocation.get_location(i)
            if loc != None:
                print("{}: {}".format(i, loc.get_name()))
    
    def check_player_alive(self) -> bool:
        if self.player.get_health() <= 0:
            return False
        return True

class Logic:
    def execute(self, player:Type[Player], arguments:list[str]) -> None:
        pass

#

class Player:
    def __init__(self, id:int, name:str, health:Union[float, int], currentLocation:Type[Location]) -> None:
        self.id:int = id
        self.name:str = name
        self.currentHealth:Union[float, int] = health
        self.maxHealth:Union[float, int] = health
        self.currentLocation:Type[Location] = currentLocation
        self.inventory:list[Type[Item]] = []

    def add_item_to_inventory(self, item:Type[Item]):
        self.inventory.append(item)
    
    def add_items_to_inventory(self, items:list[Type[Item]]):
        self.inventory.extend(items)
    
    def remove_item_to_inventory(self, item:Type[Item]):
        itemIndex = self.get_item_id_index(item.id)
        self.inventory.pop(itemIndex)

    def get_item_name(self, itemName:str) -> Union[Type[Item], None]:
        for i in self.inventory:
            if i.name == itemName:
                return i
        return None
    
    def get_item_id(self, itemID:int) -> Union[Type[Item], None]:
        for i in self.inventory:
            if i.id == itemID:
                return i
        return None

    # This is to make sure that you're getting the referenced item instead of a softcopy.
    def get_item_name_index(self, itemName:str) -> Union[int, None]:
        item = self.get_item_name(itemName)
        if item:
            return self.inventory.index(item)
        return None
    
    def get_item_id_index(self, itemID:int) -> Union[int, None]:
        item = self.get_item_id(itemID)
        if item:
            return self.inventory.index(item)
        return None
    
    def check_if_item_exist(self, item:Type[Item]) -> bool:
        for i in self.inventory:
            if i.id == item.id:
                return True
        return False
    
    def check_if_item_exist_name(self, itemName:str) -> bool:
        for i in self.inventory:
            if i.name == itemName:
                return True
        return False
    
    def check_if_item_exist_id(self, itemID:int) -> bool:
        for i in self.inventory:
            if i.id == itemID:
                return True
        return False


    def difference_health(self, amount:Union[float, int]) -> None:
        if self.currentHealth - amount < 0:
            return 0
        return self.currentHealth - amount

    def check_max(self, amount:Union[float, int]) -> None:
        if self.currentHealth + amount > self.maxHealth:
            return self.maxHealth
        return self.currentHealth + amount

    def take_damage(self, amount:Union[float, int]) -> None:
        diff:Union[float, int] = self.difference_health(amount)
        self.currentHealth = diff

    def add_health(self, amount:Union[float, int]) -> None:
        checkMax:Union[float, int] = self.check_max(amount)
        self.currentHealth = checkMax

    def get_health(self) -> Union[float, int]:
        return self.currentHealth

    def change_location(self, direction:str) -> None:
        direction = direction.lower()
        newLocation = self.currentLocation.get_location(direction=direction)
        directions = [self.currentLocation.north, self.currentLocation.east, self.currentLocation.south, self.currentLocation.west]
        for i in directions:
            directions = ["north", "east", "south", "west"]
            if i != None and direction in directions:
                if newLocation.id == i.id:
                    self.currentLocation = i
                    print("You've gone to {}".format(self.currentLocation.name))
                    return None
                print("There's no such location.")
    
    def set_current_location(self, location:Type[Location]) -> None:
        self.currentLocation = location

#

class Item:
    def __init__(self, id:int, name:str) -> None:
        self.id:int = id
        self.name:str = name
    
    def use(self, player: Type[Player]) -> None:
        pass

    def get_id(self) -> int:
        return self.id
    
    def get_name(self) -> str:
        return self.name

#

class Entity:
    def __init__(self, id:int, name:str) -> None:
        self.id:int = id
        self.name:str = name
    
    def behavior(self) -> None:
        pass

#

class NPC(Entity):
    def __init__(self, id: int, name: str, occupation:str) -> None:
        self.occupation = occupation
        self.quest:Type[Quest] = None
        self.defaultDialogue:list[str] = []
        self.thanksDialogue:str = ""
        super().__init__(id, name)
    
    def add_dialogue(self, message:str) -> None:
        self.defaultDialogue.append(message)
    
    def add_dialogues(self, messages:list[str]) -> None:
        self.defaultDialogue.extend(messages)
    
    def set_dialogue(self, messages:list[str]) -> None:
        self.defaultDialogue = messages
    
    def set_thanks_dialogue(self, message:str) -> None:
        self.thanksDialogue = message

    def set_quest(self, quest:Type[Quest]) -> None:
        self.quest = quest

    def behavior(self, player:Type[Player]) -> None:
        self.talk(player)
    
    def talk(self, player:Type[Player]) -> None:
        if self.quest.check_conditions(player=player):
            if not self.quest.get_done():
                self.quest.set_done(isDone=True)
                if self.quest.behavior:
                    self.quest.reward_behavior(player=player)
                else:
                    self.quest.reward_item(player=player)
                player.remove_item_to_inventory(item=self.quest.questItem)
                print(self.thanksDialogue)
                print()
        else:
            if not self.quest.get_done():
                self.quest.prompt_quest_dialogues()
            else:
                for i in self.defaultDialogue:
                    print(i + "\n")

class Quest:
    def __init__(self, questItem:Type[QuestItem] = None, rewardItem:Type[Item] = None, rewardQuantity:int = 1) -> None:
        self.questItem:Type[QuestItem] = questItem
        self.rewardItem:Type[Item] = rewardItem
        self.rewardQuantity:int = rewardQuantity
        self.done:bool = False
        self.behavior:bool = False
        self.questDialogue:list[str] = []

    def set_done(self, isDone:bool) -> None:
        self.done = isDone
    
    def set_behavior(self, isBehavior:bool) -> None:
        self.behavior = isBehavior
    
    def set_quest_item(self, questItem:Type[QuestItem]) -> None:
        self.questItem = questItem
    
    def set_reward_item(self, rewardItem:Type[Item]) -> None:
        self.reward_item = rewardItem
    
    def set_reward_quantity(self, rewardQuantity:int) -> None:
        self.rewardQuantity = rewardQuantity

    def get_done(self) -> bool:
        return self.done

    def check_conditions(self, player:Type[Player]) -> None:
        if player.check_if_item_exist(item=self.questItem):
            # self.set_done(True)
            return True
        return False

    def add_quest_dialogue(self, message:str) -> None:
        self.questDialogue.append(message)
    
    def add_quest_dialogues(self, messages:list[str]) -> None:
        self.questDialogue.extend(messages)
    
    def set_quest_dialogues(self, messages:list[str]) -> None:
        self.questDialogue = messages
    
    def prompt_quest_dialogues(self) -> None:
        for i in self.questDialogue:
            print(i + "\n\n")

    def reward_item(self, player:Type[Player]) -> None:
        if self.rewardQuantity > 1:
            player.add_item_to_inventory(self.rewardItem)
        else:
            for _ in range(self.rewardQuantity):
                player.add_item_to_inventory(self.rewardItem)

    def reward_behavior(self, player:Type[Player]) -> None:
        pass

class QuestItem(Item):
    # __slots__ = ['id', 'name']
    def __init__(self, id: int, name: str) -> None:
        super().__init__(id, name)
    
    def use(self) -> None:
        return super().use()

#

class Enemy(Entity):
    def __init__(self, id: int, name: str, health:Union[float, int]) -> None:
        self.currentHealth:Union[float, int] = health
        self.maxHealth:Union[float, int] = health
        super().__init__(id, name)
    
    def behavior(self, player:Type[Player]) -> None:
        return super().behavior()

    # How the enemy will take damage.
    def take_damage(self) -> None:
        pass

    # How the enemy will attack.
    def attack(self) -> None:
        pass

#

class EnemyQuestion(Enemy):
    def __init__(self, id: int, name: str, health: Union[float, int], questionHandler:Type[QuestionHandler]) -> None:
        self.questionHandler:Type[QuestionHandler] = questionHandler
        self.dialogue:list[str] = []
        super().__init__(id, name, health)
    
    def behavior(self, player:Type[Player]) -> None:
        self.prompt_dialogue()
        self.attack(player)
    
    def get_health(self) -> Union[float, int]:
        return self.currentHealth

    def check_alive(self) -> bool:
        if self.get_health() <= 0:
            return False
        return True

    def take_damage(self, amount:Union[float, int]) -> None:
        self.currentHealth -= amount
    
    #

    def get_dialogue(self) -> list[str]:
        return self.dialogue
    
    def set_dialogue(self, dialogue:list[str]) -> None:
        self.dialogue = dialogue
    
    def add_dialogue(self, message:str) -> None:
        self.dialogue.append(message)
    
    def add_dialogues(self, messages:list[str]) -> None:
        self.dialogue.extend(messages)
    
    def prompt_dialogue(self) -> None:
        for i in self.get_dialogue():
            print(i + '\n')

    # The attack should be prompting a question.
    def attack(self, player:Type[Player]) -> None:
        while True:
            if not self.check_alive():
                break

            # This if is for debug purposes to check if parent while loop that checks if the player is alive.
            if player.get_health() <= 0:
                print("Game over!")
                break

            self.questionHandler.set_current_question_random()
            print()
            self.questionHandler.prompt_question()
            answer = str(input("\nWhat's your answer? "))
            
            if self.questionHandler.check_answer(answer):
                # right
                print()
                print("Correct!")
                print()
                self.take_damage(1)
            else:
                # wrong
                print()
                print("Wrong!")
                player.take_damage(1)

class QuestionHandler:
    def __init__(self) -> None:
        self.questions:list[Type[Question]] = []
        self.currentQuestion:Type[Question] = None
    
    def set_current_question(self, index:int) -> None:
        try:
            self.currentQuestion = self.questions[index]
        except:
            self.currentQuestion = None
    
    def set_current_question_random(self) -> None:
        self.currentQuestion = choice(self.questions)

    def prompt_question(self) -> None:
        print(self.currentQuestion.get_question())
    
    def check_answer(self, answer:Any) -> bool:
        if answer == self.currentQuestion.get_answer():
            return True
        return False
    
    def add_question(self, question:Type[Question]) -> None:
        self.questions.append(question)
    
    def add_questions(self, question:list[Type[Question]]) -> None:
        self.questions.extend(question)

class Question:
    def __init__(self, question:str, answer:Any) -> None:
        self.question:str = question
        self.answer:Any = answer
    
    def get_question(self) -> str:
        return self.question
    
    def get_answer(self) -> Any:
        return self.answer

#

class Location:
    def __init__(self, id:int, name:str, description:str, north:Type[Location] = None, items:list[Type[Item]] = [], entities:list[Type[Entity]] = [], east:Type[Location] = None, south:Type[Location] = None, west:Type[Location] = None) -> None:
        self.id:int = id
        self.name:str = name
        self.description:str = description
        self.items:list[Type[Item]] = items
        self.entities:list[Type[Entity]] = entities
        self.north:Type[Location] = north
        self.east:Type[Location] = east
        self.south:Type[Location] = south
        self.west:Type[Location] = west
    
    #

    def activate(self, player:Type[Player]) -> None:
        enemies:list[Type[Enemy]] = []
        for i in self.entities:
            if type(i) is EnemyQuestion:
                enemies.append(i)
        
        for i in enemies:
            print()
            print("{} is going to attack you! Answer this question to attack this enemy back!".format(i.name))
            i.behavior(player)

    def describe(self, player:Type[Player]) -> None:
        currentEntities:dict[str, str] = {}
        for i in self.entities:
            if type(i) is NPC:
                currentEntities.update({i.name:"a/an {} by the named".format(i.occupation)})
        
        currentItems:list[str] = []
        for i in self.items:
            currentItems.append(i.name)
        
        entitiesDescribe:str = ", ".join("{} {}".format(entityCount, entityName) for _, (entityName, entityCount) in enumerate(currentEntities.items()))
        itemsDescribe:str = ", ".join(currentItems)#("{} {}".format(itemCount, itemName) for _, (itemName, itemCount) in enumerate(currentItems.items()))
        generalDescribe:str = self.description

        if currentEntities != {}:
            generalDescribe += ".\nEntities being {}".format(entitiesDescribe)
        if currentItems != []:
            generalDescribe += ".\nThere is {}.".format(itemsDescribe)
        
        print(generalDescribe)

        if self.entities != []:
            self.activate(player)

    #

    def change_north(self, location:Type[Location]) -> None:
        self.north = location
    
    def change_east(self, location:Type[Location]) -> None:
        self.east = location
    
    def change_south(self, location:Type[Location]) -> None:
        self.south = location
    
    def change_west(self, location:Type[Location]) -> None:
        self.west = location
    
    def change_location(self, direction:str, location:Type[Location]) -> None:
        direction = direction.lower()
        match direction:
            case "north":
                self.change_north(location)
            case "east":
                self.change_east(location)
            case "south":
                self.change_south(location)
            case "west":
                self.change_west(location)
    #

    def get_north(self) -> Type[Location]:
        return self.north
    
    def get_east(self) -> Type[Location]:
        return self.east
    
    def get_south(self) -> Type[Location]:
        return self.south
    
    def get_west(self) -> Type[Location]:
        return self.west

    def get_location(self, direction:str) -> Type[Location]:
        direction = direction.lower()
        match direction:
            case "north":
                return self.get_north()
            case "east":
                return self.get_east()
            case "south":
                return self.get_south()
            case "west":
                return self.get_west()

    def get_name(self) -> str:
        return self.name

    def add_item_on_ground(self, item:Type[Item]) -> None:
        self.items.append(item)
    
    def add_items_on_gruond(self, items:list[Type[Item]]) -> None:
        self.items.extend(items)
    
    def add_entity_on_location(self, entity:Type[Entity]) -> None:
        self.entities.append(entity)
    
    def add_entities_on_location(self, entities:list[Type[Entity]]) -> None:
        self.entities.extend(entities)

class World:
    pass
