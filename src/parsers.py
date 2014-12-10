# Operating parsers to extract files from output of other programs and prepare data for 
import os

class JPaudaParser:

    def __init__(self, vlhome, dirin, dirout):
        self.cmd = "java JPauda"
        self.vlhome = vlhome
        self.dirin = dirin
        self.dirout = dirout

    def parse(self):
        """Combine input and output file path into a single command and make
        JPauda extract data from input file and save to output file"""
        currdir = os.getcwd()
        os.chdir (self.vlhome)
        os.chdir ("../bin")
        print(os.getcwd())
        for fin in os.listdir(self.dirin):
            cmdin = self.cmd + " " + str(self.dirin + "/" + fin) + " " + str(self.dirout + "/" + "out-" + fin)
            try:
                os.system(cmdin)
            except:
                print ("Canno execute command: " + cmdin)
        os.chdir(currdir)

class CPaudaParser:
    def __init__(self, vlhome, dirin, dirout):
        self.cmd = "./cparser"
        self.vlhome = vlhome
        self.dirin = dirin
        self.dirout = dirout
    def parse (self, inpath, outpath):
        cmdin = self.cmd + " " + str(inpath) + " " + str(outpath)
        try:
            os.system(cmdin)
        except:
            print ("Cannot execute command: " + cmdin)

