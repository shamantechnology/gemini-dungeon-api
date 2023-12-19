"""
TestDNDLibrary

DNDLibrary class tests
"""

import unittest
from dndlibrary import DNDLibrary

class TestDNDLibrary(unittest.TestCase):
    def test_one(self):
        dndlib = DNDLibrary()
        self.assertRaises(dndlib.run())

if __name__ == "__main__":
    unittest.main()