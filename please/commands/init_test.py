import unittest
from . import init_please_matcher

class InitTest(unittest.TestCase):
    def test_init_please_matcher(self):
        #just run
        init_please_matcher()

if __name__ == '__main__':
    unittest.main()