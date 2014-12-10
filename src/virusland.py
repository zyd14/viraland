# Viraland is a batch-job controlling program, especially for bioinfomatics data
# file flow control and analysis. Viraland can be run directly in Python 3
# console or be run with a configuration file.
# This program also supply a good amount of API to make data processing more
# flexible.
#
# author: Yubing Hou
# author: Zach Romer
# license: GPL v3

import os
import sys
from setup import Compile
from configuration import Configuration
from parsers import JPaudaParser
from visualize import VisualVirusLand

class Viraland:
    def __init__(self, configpath):
        self.config = Configuration(configpath) # setup configuration
        if not os.path.isdir(self.config.dir):
            try:
                os.makedirs (self.config.dir)
            except:
                self.config.dir = os.getenv("HOME") # if directory not found, make it home
        if self.config.log != None and self.config.log == True:
            self.logf = open (self.config.dir +"/log.txt", "w+")
        self.logc = []
    def run (self):
        self.logc.append(self.config.title)
        parser = JPaudaParser(self.config.vlhome, self.config.parsein, self.config.parseout)
        parser.parse()
        self.logc.append("Parsing complete")
        for entry in self.logc:
            self.logf.write(entry + "\n")
        self.logf.close()

# Get argument
argv = sys.argv
argc = len (argv)

# VirusLand will only execute when these is exactly one argument and it is a configuration file
if argc == 2 and ".vl" in argv[1]:
    vl= Viraland(argv[1])
    
    # prepare binary files
    c = Compile(vl.config.vlhome)
    c.exe()
    vl.run()
if argc == 2 and argv[1] == "-v":
    vlhome = input("Enter path of the home directory of VirusLand: ")
    try:
        vs = VisualVirusLand(vlhome)
        vs.exe()
    except:
        print ("Run time error:")
