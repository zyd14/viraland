# Class of managing velvet: instantiate this class so that command of velvet
# can match user's system settings.
# author: Zach Romer
# date: 2014/12/08

class VelvetPackage:
	"""VelvetPackage takes a configuration and set up execution environment for
	velvet assembler"""
	
	VELVETH = "velveth"
	VELVETG = "velvetg"
	
    def __init__(self, config):
    	if config isinstance Configuration:
		    self.fmt = config.velvetformat
		    self.out = config.velvetout
		    self.inFiles = config.velvetin
		    self.kmer = config.velvetkmer
		    self.inFolder = self.getFolder()
		    self.readType = config.velvetreadtype
		    self.vCmd = None
		    self.r1 = None
		    self.r2 = None
		    self.callVelvet()

    def callVelvet(self):
        """Call velvet with parameters provided in contig file
       	if more than 1 file, check to see if the reads are paired or unpaired
        file writing for testing -****- delete later"""
        print ('velvet output directory: ' + self.out)
        print ('Read folder size', len(self.inFolder))
        print ('Paired: ', self.readType)
        if len(self.inFolder) > 1 and 'Paired' in self.readType:
            #process as paired reads
            print('process as paired reads in folder')
            i = 0
            while i < len(self.inFolder):
                self.r1 = self.inFolder[i]
                self.r2 = self.inFolder[i+1]
                print('velvet hashing' + self.r1 + self.r2)
                f = open(self.out + 'file' + str(i), 'w')
                f.write('velveth' + self.r1 + self.r2)
                subprocess.call(['echo', 'velveth', self.out, str(self.kmer), self.readType, self.fmt, self.r1, self.r2])
                f.write('velvetg' + self.r1 + self.r2)
                print('velvet graphing' + self.r1 + self.r2)
                subprocess.call(['echo', 'velvetg', self.out, '-exp_cov auto'])
                i += 2
                f.close()
        elif len(self.inFolder) > 1:
            print('process single reads in folder')
            #process reads 1 by 1
            i = 0
            while i < len(self.inFolder):
                self.r1 = self.inFolder[i]
                f = open(self.out + 'file' + str(i), 'w')
                f.write('velveth' + self.r1)
                print('velvet hashing' + self.r1)
                subprocess.call(['echo', 'velveth', self.out, self.kmer, self.readType, self.fmt, self.r1])
                f.write('velvetg' + self.r1)
                print('velvet graphing' + self.r1)
                subprocess.call(['echo', 'velvetg', self.out, '-exp_cov auto'])
                i += 1
                f.close()
        else:
            print("Didn't do anything")

    def getFolder(self):
        #Get files from directory specified by user
        print('Looking for: '+ self.inFiles +'*.' + self.fmt )
        folder = glob.glob(self.inFiles+'*.' + self.fmt)
        return folder
