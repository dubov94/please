import unittest
from . import cmd_or_std_gen_test_info
import os

class CmdOrStdGenTestInfo(unittest.TestCase):
    
    def test_simple_echo(self):
        a = cmd_or_std_gen_test_info.CmdOrStdGenTestInfo("echo", ["1", "2", "3"], {"G" : "gurda"} )
        res = a.tests()
        
        self.assertEqual(open(res[0]).read(), "1 2 3\n")
        os.remove(res[0])
        
        self.assertEqual(a.to_please_format(), "[G = gurda] echo 1 2 3")
        
if __name__ == '__main__':
    unittest.main()