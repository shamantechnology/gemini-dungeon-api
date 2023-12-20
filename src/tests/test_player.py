"""
TestPlayer
"""

import unittest
from player import Player


class TestPlayer(unittest.TestCase):
    def test_one(self):
        p = Player("John", "Lee")
        pdesc = p.player_sheet()
        self.assertIsNotNone(pdesc)


if __name__ == "__main__":
    unittest.main()
