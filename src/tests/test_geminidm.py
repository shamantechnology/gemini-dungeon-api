"""
TestGeminiDM
"""

import unittest
import uuid
from geminidm import GeminiDM
from player import Player
from dotenv import load_dotenv


class TestGeminiDM(unittest.TestCase):
    def test_one(self):
        load_dotenv()
        # create and save new session id
        session_id = str(uuid.uuid4()).replace("-", "")

        # create new player
        player = Player()

        gdm = GeminiDM(agent=True)
        with self.assertRaises(Exception):
            resp = gdm.chat(
                user_msg="Hello, please introduce me to the campaign, current area, who you are and other information.",
                session_id=session_id,
                player=player
            )

            print(f"resp: {resp}")

if __name__ == "__main__":
    unittest.main()
