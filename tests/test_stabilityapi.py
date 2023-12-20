"""
TestStabilityAPI
"""

import unittest
from stabilityapi import StabilityAPI
from dotenv import load_dotenv

class TestStabilityAPI(unittest.TestCase):
    def test_one(self):
        load_dotenv()
        test_prompt = "A beautiful rose"
        sapi = StabilityAPI()
        img = sapi.generate_image(test_prompt)
        # print(img)
        self.assertIsNotNone(img)

if __name__ == "__main__":
    unittest.main()
