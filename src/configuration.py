# Configure viraland run-time environment. This includes commands for packages 
# needed for viraland, corresponding command configurations, and I/O directories
# 
# author: yubing hou
# date: 2014/12/08

class Configuration:
    """Configuration class takes a configuration file and set up the environment parameters for execution."""

    def __init__(self, fpath):
        """take a configuration file set up configurations for one run"""
        self.title = None
        self.vlhome = None
        self.dir = None
        self.log = None
        self.keep = None
        self.velvetin = None
        self.velvetformat = ".fasta"
        self.velvetkmer = 32
        self.velvetreadtype = None
        self.velvetout = None
        self.embossin = None
        self.embossout = None
        self.paudain = None
        self.paudaout = None
        self.parsein = None
        self.parseout = None
        self.setconfig(str(fpath))

    def info (self):
        """get the output of configuration. This should be mostly used for debugging use."""
        print ("[TITLE] " + str(self.title))
        print ("[VL-HOME] " + str(self.vlhome))
        print ("[DIR] " + str(self.dir))
        print ("[LOG] " + str(self.log))
        print ("[KEEP] " + str(self.keep))
        print ("[VELVET-INPUT] " + str(self.velvetin))
        print ("[VELVET-FORMAT] " + str(self.velvetformat))
        print ("[VELVET-KMER] " + str(self.velvetkmer))
        print ("[VELVET-READTYPE] " + str(self.velvetreadtype))
        print ("[VELVET-OUTPUT] " + str(self.velvetout))
        print ("[EMBOSS-INPUT] " + str(self.embossin))
        print ("[EMBOSS-OUTPUT] " + str(self.embossout))
        print ("[PAUDA-INPUT] " + str(self.paudain))
        print ("[PAUDA-OUTPUT] " + str(self.paudaout))
        print ("[PARSE-INPUT] " + str(self.parsein))
        print ("[PARSE-OUTPUT] " + str(self.parseout))

    def setconfig (self, fpath):
        """get values for field variables. If error is encountered, error message will be printed out"""
        try:
            fd = open(fpath, "r")
            for line in fd:
                # Get the title of this run
                if line.startswith("[TITLE]"):
                    self.title = line.split("[TITLE]")[1].strip()
                # Get the home directory of virusland
                if line.startswith ("[VL-HOME]"):
                    self.vlhome = line.split("[VL-HOME]")[1].strip()
                # Get working directory
                if line.startswith("[DIR]"):
                    self.dir = line.split("[DIR]")[1].strip()
                # Get user's configuration of saving log
                if line.startswith("[LOG]"):
                    option = line.split("[LOG]")[1].strip()
                    if option.lower() == "yes":
                        self.log = True
                    else:
                        print ("[WARNING] No log will be kept!")
                        self.log = False
                # Get user's configuration of keeping intermediate file
                if line.startswith("[KEEP]"):
                    option = line.split("[KEEP]")[1].strip()
                    if option.lower() == "yes":
                        self.keep = True
                    else:
                        print ("[WARNING] No intermediate file will be kept!")
                        self.keep = False
                # Get user's configuration of input for velvet
                if line.startswith("[VELVET-INPUT]"):
                    option = line.split("[VELVET-INPUT]")[1].strip()
                    if option != "":
                        self.velvetin = option
                    else:
                        print ("[Error] Cannot find input for velvet!")
                        sys.exit()
                # Get user's configuration of input file format for velvet
                # If nothing is specified, then use default setting
                if line.startswith ("[VELVET-FORMAT]"):
                    option = line.split("[VELVET-FORMAT]")[1].strip()
                    if option != "":
                        self.velvetformat = option
                # Get user's configuration of k-mer length for velvet
                # if nothing is specified, then use default k-mer length: 32
                if line.startswith ("[VELVET-KMER]"):
                    option = line.split("[VELVET-KMER]")[1].strip()
                    if option != "":
                        try:
                            self.velvetkmer = int(option)
                        except:
                            pass
                # Get user's configuration of output for velvet
                if line.startswith("[VELVET-OUTPUT]"):
                    option = line.split("[VELVET-OUTPUT]")[1].strip()
                    if option != "":
                        self.velvetout = option
                    else:
                        print ("[Error] Cannot find output for velvet!")
                        sys.exit()
                # Get user's configuration of input for emboss
                if line.startswith("[EMBOSS-INPUT]"):
                    option = line.split("[EMBOSS-INPUT]")[1].strip()
                    if option != "":
                        self.embossin = option
                    else:
                        print ("[Error] Cannot find input for emboss!")
                        sys.exit()
                # Get user's configuration of output for emboss
                if line.startswith("[EMBOSS-OUTPUT]"):
                    option = line.split("[EMBOSS-OUTPUT]")[1].strip()
                    if option != "":
                        self.embossout = option
                    else:
                        print ("[Error] Cannot find output for emboss!")
                        sys.exit()
                # Get user's configuration of input for velvet
                if line.startswith("[PAUDA-INPUT]"):
                    option = line.split("[PAUDA-INPUT]")[1].strip()
                    if option != "":
                        self.paudain = option
                    else:
                        print ("[Error] Cannot find input for pauda!")
                        sys.exit()
                # Get user's configuration of output for velvet
                if line.startswith("[PAUDA-OUTPUT]"):
                    option = line.split("[PAUDA-OUTPUT]")[1].strip()
                    if option != "":
                        self.paudaout = option
                    else:
                        print ("[Error] Cannot find output for pauda!")
                        sys.exit()
                # Get user's configuration of input for velvet
                if line.startswith("[PARSE-INPUT]"):
                    option = line.split("[PARSE-INPUT]")[1].strip()
                    if option != "":
                        self.parsein = option
                    else:
                        print ("[Error] Cannot find input for parser!")
                        sys.exit()
                # Get user's configuration of output for velvet
                if line.startswith("[PARSE-OUTPUT]"):
                    option = line.split("[PARSE-OUTPUT]")[1].strip()
                    if option != "":
                        self.parseout = option
                    else:
                        print ("[Error] Cannot find output for parser!")
                        sys.exit()
                # Stop when encounter [STOP] sign
                if line.startswith("[STOP]"):
                    return None
        except:
            traceback.print_stack()
