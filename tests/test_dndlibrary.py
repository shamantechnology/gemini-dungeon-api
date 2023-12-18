"""
TestDNDLibrary

DNDLibrary class tests
"""

import unittest
from dndlibrary import DNDLibrary

class TestDNDLibrary(unittest.TestCase):
    def test_one(self):
        with self.assertRaises(Exception):
            dndlib = DNDLibrary()
            dndlib.run()

if __name__ == "__main__":
    unittest.main()