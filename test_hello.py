import unittest
import hello

class TestHello(unittest.TestCase):
    def test_hello(self):
        self.assertEqual(hello.greet('Alice'), 'Hello, Alice!')

if __name__ == '__main__':
    unittest.main()