"""
Test suite for the hello.py module.
"""

import unittest
from hello import say_hello


class TestHello(unittest.TestCase):
    """
    Test cases for the say_hello function in the hello.py module.
    """

    def test_say_hello(self):
        self.assertEqual(say_hello(), "Hello, World!")


if __name__ == '__main__':
    unittest.main()
