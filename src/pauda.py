class PaudaPack:
    #faa from faaPack
    def __init__(self, faa, config):
        self.faaIndex = faa

        self.inFolder = config.embossout
        self.inFiles = glob.glob(config.embossout + '*')
        print(self.inFiles)
        #eventually have it automatically generate unique blastx name
        #for each file run
        self.indexOut = config.paudaindex
        for i in range(0,len(self.inFiles)):
            self.blastxOut = config.paudaout + generateNames(self.inFiles[i]) + '_pauda'
            self.runPauda(self.inFiles[i])
    def runPauda(self, inFile):
        paudaLocation = '/home/lsb456/Desktop/pauda-1.0.1/pauda/bin'
        print(paudaLocation + ' ' + self.faaIndex)
        #os.system(paudaLocation + '/pauda-build ' + self.faaIndex + ' ' + self.indexOut) # + self.faaIndex)
        subprocess.call([paudaLocation + '/pauda-run', '--slow', inFile, self.blastxOut, self.indexOut])