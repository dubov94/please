#/bin/python3
import os
import logging

#"" is for commands
langs = ["c", "c++", "c#", "pascal", "delphi", "python2", "python3", "java", ""] 

class Language:
    '''
    This class determines in which programming language given
    source code file is written.
    Currently it's very stupid, so don't mix extensions and
    don't be sad if it has made a mistake.
    
    Example:
    Language lang()
    print(lang().get("test_files/helloworld.pas")) # outputs pascal
    print(lang().get("test_files/helloworld3.py")) # outputs python3
    '''
    def __init__(self):
        pass

    def __by_ext(self, fn):
        ext = os.path.splitext(fn)[1].lower()
        if not ext:
            return 'command'
        dct = { ".c" : "c", 
                ".cpp" : "c++",
                ".c++" : "c++",
                ".cs" : "c#",
                ".pas" : "pascal",
                ".java" : "java",
                ".py" : "?python",
                ".dpr" : "delphi",
                ".tex" : "latex"
                 }
        if (ext in dct):
            return dct[ext]
        else:
            return None

    def __proceed_python(self, path):
        f = open(path, 'r')
        line = f.readline()
        f.close()
        if (line.find("python3") != -1):
            return "python3"
        elif (line.find("python2") != -1):
            return "python2"
        else:
            log = logging.getLogger("please_logger.language")
            log.info("Assuming " + path + " is python2 file. If you want to translate it with python3, insert 'python3' in the first line of this file")        
            return "python2"

    def __by_contents(self, path, info):
        if (info[1:] == "python"):
            return self.__proceed_python(path)
        else:
            return None


    def get(self, path):
        res_by_ext = self.__by_ext(path)
        if (res_by_ext is None):
            return None
        if (res_by_ext[0] != '?'):
            return res_by_ext
        if (not os.path.isfile(path)):
            raise OSError("There is no file " + path)
        res_by_content = self.__by_contents(path, res_by_ext)
        return res_by_content

