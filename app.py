from prototype import Location, Player, Game, Item, Entity, NPC

firstLocation = Location(id=1, name="test location 1", description="This is a cool place to test stuff.")
secondLocation = Location(id=2, name="test location 2", description="This is also another cool place to test stuff.")
firstLocation.change_north(secondLocation)
secondLocation.change_south(firstLocation)
player = Player(1, "test", 4, firstLocation)

testItem = Item(1, "test item 1", 1, 1)
testItem2 = Item(2, "test item 2", 1, 1)
firstLocation.add_item_on_ground(testItem)
firstLocation.add_item_on_ground(testItem2)
firstLocation.add_item_on_ground(testItem2)

testEntity = Entity(1, "test entity")
testEntity2 = Entity(2, "2nd test entity")
testNPC = NPC(3, "John Doe", occupation="villager")
firstLocation.add_entity_on_location(testEntity)
firstLocation.add_entity_on_location(testEntity2)
firstLocation.add_entity_on_location(testEntity2)
firstLocation.add_entity_on_location(testNPC)

game = Game(player=player)
game.run()
