import os

class VisualVirusLand:
    """Visualization is done by Jonathan's plotting program, which is bin/VisualVirusLand.jar"""
    def __init__(self, vlhome):
        self.cmd = "java -jar ../bin/VisualVirusLand.jar"
        self.vlhome = str(vlhome)
    def exe (self):
        curr = os.getcwd()
        os.chdir(self.vlhome)
        os.system(self.cmd)
        os.chdir(curr)