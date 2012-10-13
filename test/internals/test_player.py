from test.framework import FrameworkTestGame

class TestPlayer(FrameworkTestGame):
    def test_class(self):
        self.assertIsInstance(self.player, Player)
        self.assertIsInstance(self.player, Creature)

    def test_talking(self):
        # These are NOT globals.
        from game.creature_talking import PlayerTalking, CreatureTalking
        
        self.assertIsInstance(self.player, PlayerTalking)
        self.assertIsInstance(self.player, CreatureTalking)
        self.player.say("Hello world!")
        
    def test_move(self):
        # These are NOT globals.
        from game.creature_movement import CreatureMovement

        self.assertIsInstance(self.player, CreatureMovement)
        newPosition = self.player.positionInDirection(SOUTH)
        self.player.move(SOUTH)
        
        self.assertEqual(newPosition, self.player.position)
        
    def test_teleport(self):
        newPosition = self.player.positionInDirection(SOUTH)
        self.player.teleport(newPosition)
        
        self.assertEqual(newPosition, self.player.position)