import please.language_configurator.java as javaconf
import os
import unittest

class JavaTest(unittest.TestCase):
    def test_win_compile(self):
        java = javaconf.JavaWindowsConfigurator()
        out = java.get_compile_command("test.java")
        self.assertEqual(out, ["javac", "-d", os.path.join(".please", "test.java_javac"), "-cp", ".", "test.java"])
        
    def test_win_run1(self):
        java = javaconf.JavaWindowsConfigurator()
        out = java.get_run_command("abacaba.java")
        self.assertEqual(out, ["java", "-cp", os.path.join(".please", "abacaba.java_javac"), "abacaba"])
        
    def test_win_run2(self):
        java = javaconf.JavaWindowsConfigurator()
        out = java.get_run_command("aba/caba.java")
        self.assertEqual(out, ["java", "-cp", os.path.join(".please", "caba.java_javac"), "caba"])
        
    def test_linux_compile(self):
        java = javaconf.JavaLinuxConfigurator()
        out = java.get_compile_command("test.java")
        self.assertEqual(out, ["javac" ,"-d", os.path.join(".please", "test.java_javac"), "-cp", ".", "test.java"])
        
    def test_linux_run(self):
        java = javaconf.JavaLinuxConfigurator()
        out = java.get_run_command("abacaba.java")
        self.assertEqual(out, ["java" ,"-cp", os.path.join(".please", "abacaba.java_javac"), "abacaba"])
        
    def test_linux_run2(self):
        java = javaconf.JavaLinuxConfigurator()
        out = java.get_run_command("aba/caba.java")
        self.assertEqual(out, ["java", "-cp", os.path.join(".please", "caba.java_javac"), "caba"])

    #TODO: add tests for is_compile_garbage and get_binary_name
    #TODO: add tests for compiling in another dir
        
if __name__ == '__main__':
    unittest.main()