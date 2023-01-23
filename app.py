from prototype import Location, Player, Game, Item, EnemyQuestion, QuestionHandler, Question

firstLocation = Location(id=1, name="test location 1", description="This is a cool place to test stuff.")
secondLocation = Location(id=2, name="test location 2", description="This is also another cool place to test stuff.")
firstLocation.change_north(secondLocation)
secondLocation.change_south(firstLocation)
player = Player(1, "test", 4, firstLocation)

questionHandler = QuestionHandler()
testQuestion = Question("What's 1 + 1?", "2")
questionHandler.add_question(testQuestion)

testEnemy = EnemyQuestion(1, "test enemy", 1, questionHandler)
firstLocation.add_entity_on_location(testEnemy)

game = Game(player=player)
game.run()
