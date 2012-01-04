from . import test_info
import tempfile
class EchoTestInfo(test_info.TestInfo):
    def __init__(self, line, tags={}, comment = ''):
        """
            example: line = "abacabadabacaba"
        """
        self.__line = str(line)
        super(EchoTestInfo, self).__init__(tags, comment)
        
    def tests(self):
        stdout = tempfile.NamedTemporaryFile(delete = False)
        with open(stdout.name, 'w') as f:
            f.write(self.__line + '\n')
        self.set_desc( ['echo output'] )
        return [stdout.name]
    
    def to_please_format(self):
        return ' '.join([self.get_prefix(), "echo", self.__line, self.get_suffix()]).strip()