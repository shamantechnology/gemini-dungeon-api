"""
TestGeminiDM
"""

import unittest
from geminidm import GeminiDM
from dotenv import load_dotenv

class TestGeminiDM(unittest.TestCase):
    def test_one(self):
        load_dotenv()
        self.assertRaises(GeminiDM())

if __name__ == "__main__":
    unittest.main()