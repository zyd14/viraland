# Operating parsers to extract files from output of other programs and prepare data for 
import os

class JPaudaParser:
    """Class that extract key information from output of Pauda and save to a new
    file. Example:
    >>> parser = JPaudaParser()
    >>> inpath = "data/run01.fastq"
    >>> outpath = "data/out01.fastq"
    >>> parser.parse(inpath, outpath)
    """
    def __init__(self, config):
        self.cmd1 = config.vlhome + '/krona/Krona_VirusLand/TaxonomyFromGBK.exe"
        self.path = config.vlhome + '/gbks/*/*.gbk' #Replace this with the path where the GBk files are
        self.fileNames = glob.glob(self.path)
        self.createFile()
        self.runTaxFromGBK(config.vlhome + '/krona/Krona_VirusLand/compiledGBKs', config.vlhome + '/krona/Krona_VirusLand/taxOut')

    def createFile(self):
        myFile = open(config.vlhom + 'krona/Krona_VirusLand/compiledGBKs', 'w')  #creates a file called 'jonsFile' and allows it to read and write
        for x in self.fileNames:
            print(x)
            myFile.write(x + '\n')

    def runTaxFromGBK(self, inpath, outpath):
        """Combine input and output file path into a single command and make
        JPauda extract data from input file and save to output file"""
        cmdin = self.cmd1 + " " + str(inpath) + " " + str(outpath)
        print("Cmdin: " + cmdin)
        try:
            os.system(cmdin)
        except:
            print ("Cannot execute command: " + cmdin)

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

