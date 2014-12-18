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
        #Call velvet with parameters provided in contig file
        #if more than 1 file, check to see if the reads are paired or unpaired
        print ('velvet output directory: ' + self.out)
        print ('Read folder size', len(self.inFolder))
        print ('Paired: ', self.readType)
        if len(self.inFolder) > 1 and 'Paired' in self.readType:
            #process as paired reads
            print('process as paired reads in folder')
            i = 1
            
            while i < len(self.inFolder):
                r1 = self.inFolder[i-1]
                r2 = self.inFolder[i]

                #Generate unique names 
                r1Name = self.generateNames(r1)
                r2Name = self.generateNames(r2)
                print('r1: ', r1Name, 'r2:', r2Name)
                fileName = r1Name + 'X' + r2Name
                outFolder = self.out + '/' + fileName

                print('velvet hashing' + fileName)
                #print('velveth', outFolder, str(self.kmer), self.readType, self.fmt, r1, r2)
                subprocess.call(['velveth', outFolder, str(self.kmer), self.fmt, self.readType,  r1, r2])
                print('velvet graphing' + r1Name + 'X' + r2Name)
                x = '-exp_cov auto'
                os.system('velvetg ' + outFolder + ' ' + x)

                self.moveFiles(outFolder, fileName)
                
                i += 2
        elif len(self.inFolder) > 1:
            print('process single reads in folder')
            #process reads 1 by 1
            i = 0
            while i < len(self.inFolder):
                r1 = self.inFolder[i]
                r1Name = self.generateNames(r1)
                outFolder = self.out + '/' + r1Name
                print('velvet hashing' + r1)
                subprocess.call(['velveth', self.out, str(self.kmer), self.readType, self.fmt, r1])
                print('velvet graphing' + r1)
                subprocess.call(['echo', 'velvetg', self.out, '-exp_cov\ auto'])
        else:
            print("Something is wrong with the input files or config file")

    def getFolder(self):
        #Get files from directory specified by user
        print('Looking for: '+ self.inFiles +'*.' + self.fmt )
        folder = glob.glob(self.inFiles+'*.' + self.fmt)
        return folder

    def moveFiles(self, folder, fileName):
        contigFile = folder+'/contigs.fa'
        fileRename = self.out + '/' + fileName + '.fa'
        os.system('cd ' + folder)
        os.system('mv ' + contigFile + ' ' + fileRename)
        os.system('rm -r ' + folder)

    #Generate unique file names
    def generateNames(self, fileN):
        #select file name without path and extension to be used for unique name
        j = len(fileN)-1
        rName = ''
        while fileN[j] != '.':
            j-=1
        j-=1
        while fileN[j] != '/' and j >= 0:
            rName += fileN[j]
            j-=1
        #reverse string
        out = rName[::-1]
        return out
