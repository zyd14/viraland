# Class of managing Emboss: instantiate this class so that command of Emboss
# cand mathc user's system setting
class EmbossPack:
    #Josh
    def __init__(self, config):
        self.emIn = config.embossin
        self.emOut = config.embossout
        self.ORF_find(str(self.emIn), str(self.emOut))
    def get_leaf(self, path):
        head, tail = ntpath.split(path)
        return tail
    def ORF_find(self, folder, out):
        #folder name will be based on title from config?
        #basepath = os.path.dirname(os.path.realpath(__file__))+'/'+folder
        files = glob.glob(folder+'/*')
        for i in files:
            print i
            k = pipes.quote(i)
            outname =  out + '/' + self.get_leaf(k)
            #outname = basepath+'/f2/'+get_leaf(k)
            args = 'getorf -sequence %s -outseq %s_ORF.fa -minsize 117 -find 3' % (k, outname)
            print(args)
            subprocess.call(args, shell=True)
            print('finished')