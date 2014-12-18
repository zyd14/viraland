class FaaPack:
    def __init__(self):
        self.folder = '/home/lsb456/vLand/genomes'
        #Change later
        self.out = '/home/lsb456/vLand/faa'
        self.finiFile = None
        self.concatFiles()
    def concatFiles(self):
        self.outCmd = self.folder + '/*/*.faa > ' + self.out + '/allTogether.faa'
        self.finiFile = self.out + '/allTogether.faa'
        os.system('cd ' + self.folder)
        os.system('cat ' + self.outCmd)