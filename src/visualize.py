class VisualPack:
    """
        VisualPack is for automate plotting data from given input files
    """
    def __init__(self):
        self.paths = []
        self.cmd = None
    def setcmd (self, instr):
        """
            Set a ploting command. For example, if program is called "myplot"
            and it takes 1 command line argument for plotting, it should be like
            this:
            >>> visual = VisualPack()
            >>> visual.setcmd ("myplot")
        """
        self.cmd = str(instr)
    def addfile (self, path):
        self.paths.append(path)
    def plot(self, item):
        if item in self.paths:
            exe = self.cmd + " " + item
            os.system(exe)
        else:
            print ("[System] Cannot find item:", item)
    def plotall(self):
        """
            applying plot command on all input file that is in file list.
            Example:
                >>> visual = VisualPack()
                >>> visual.addfile(myfile.txt)
                >>> visual.setcmd ("java viralplot")
                >>> visual.plotall()
        """
        for item in self.paths:
            exe = self.cmd + " " + item
            try:
                os.system(exe)
            except:
                print ("[Viraland] Unexpected error.", exe, "cannot be executed.")
    def reset (self):
        """
            reset all configuration of an instance of VisualPack. Example:
        """
        self.path = []
        self.cmd = None
    def status (self):
        """
            Get the complete configuration of visualization. Example:
            >>> visual = VisualPack()
            >>> visual.setcmd ("java viralplot")
            >>> visual.addfile ("data_01.txt")
            >>> visual.addfile ("data_02.txt")
            >>> visual.status()
            command = java viralplot
            file(s):
                data_01.txt
                data_02.txt
            >>>
        """
        print ("command =", self.cmd)
        print ("file(s):")
        for item in self.paths:
            print ("\t", item)
