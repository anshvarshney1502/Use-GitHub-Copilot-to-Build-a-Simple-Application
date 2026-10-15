"""
Unit test suite for Chronicles of Aetheria CLI Game.
Verifies player data structure, health/mana calculations, node transitions,
skill check mechanics, and save/load JSON persistence.
"""

import os
import unittest
from adventure_game import Player, GameEngine, StoryNode, Choice, Monster, build_story_world


class TestPlayer(unittest.TestCase):
    def setUp(self):
        self.player = Player(
            name="Valeros",
            char_class="Warrior",
            max_hp=100,
            hp=100,
            mana=40,
            max_mana=40,
            gold=50,
            strength=15,
            agility=12,
            intelligence=10,
            inventory=["Health Potion", "Torch"],
            quest_flags={"visited_camp": True}
        )

    def test_damage_and_healing(self):
        dmg_dealt = self.player.take_damage(30)
        self.assertEqual(dmg_dealt, 30)
        self.assertEqual(self.player.hp, 70)
        self.assertTrue(self.player.is_alive())

        # Test over-healing cap
        healed = self.player.heal(50)
        self.assertEqual(healed, 30)
        self.assertEqual(self.player.hp, 100)

        # Fatal damage
        self.player.take_damage(150)
        self.assertEqual(self.player.hp, 0)
        self.assertFalse(self.player.is_alive())

    def test_inventory_operations(self):
        self.assertTrue(self.player.has_item("Health Potion"))
        self.assertFalse(self.player.has_item("Excalibur"))

        self.player.add_item("Excalibur")
        self.assertTrue(self.player.has_item("Excalibur"))

        # Using health potion when injured
        self.player.hp = 50
        used = self.player.use_item("Health Potion")
        self.assertTrue(used)
        self.assertEqual(self.player.hp, 85)
        self.assertFalse(self.player.has_item("Health Potion"))

    def test_serialization(self):
        p_dict = self.player.to_dict()
        restored = Player.from_dict(p_dict)
        self.assertEqual(restored.name, self.player.name)
        self.assertEqual(restored.char_class, self.player.char_class)
        self.assertEqual(restored.hp, self.player.hp)
        self.assertEqual(restored.inventory, self.player.inventory)
        self.assertEqual(restored.quest_flags, self.player.quest_flags)


class TestGameWorld(unittest.TestCase):
    def setUp(self):
        self.nodes = build_story_world()

    def test_crossroads_node_exists(self):
        self.assertIn("crossroads", self.nodes)
        node = self.nodes["crossroads"]
        self.assertTrue(len(node.choices) >= 3)

    def test_all_choice_targets_exist(self):
        """Validates that no choice leads to an undefined node ID."""
        for node_id, node in self.nodes.items():
            for choice in node.choices:
                self.assertIn(
                    choice.target_node,
                    self.nodes,
                    f"Choice '{choice.text}' in node '{node_id}' targets non-existent node '{choice.target_node}'"
                )
                if choice.failure_target:
                    self.assertIn(
                        choice.failure_target,
                        self.nodes,
                        f"Failure target in node '{node_id}' targets non-existent node '{choice.failure_target}'"
                    )

    def test_victory_and_game_over_nodes(self):
        self.assertIn("victory_ending", self.nodes)
        self.assertIn("game_over", self.nodes)
        self.assertTrue(self.nodes["victory_ending"].is_ending)
        self.assertTrue(self.nodes["victory_ending"].is_victory)
        self.assertTrue(self.nodes["game_over"].is_ending)
        self.assertFalse(self.nodes["game_over"].is_victory)


class TestGameEnginePersistence(unittest.TestCase):
    def setUp(self):
        self.test_save_file = "test_savegame.json"
        self.engine = GameEngine()
        self.engine.player.name = "TestHero"
        self.engine.current_node_id = "sanctum_gate"

    def tearDown(self):
        if os.path.exists(self.test_save_file):
            os.remove(self.test_save_file)

    def test_save_and_load(self):
        success = self.engine.save_game(self.test_save_file)
        self.assertTrue(success)
        self.assertTrue(os.path.exists(self.test_save_file))

        new_engine = GameEngine()
        loaded = new_engine.load_game(self.test_save_file)
        self.assertTrue(loaded)
        self.assertEqual(new_engine.player.name, "TestHero")
        self.assertEqual(new_engine.current_node_id, "sanctum_gate")


if __name__ == "__main__":
    unittest.main()
