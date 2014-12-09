# Class of managing Emboss: instantiate this class so that command of Emboss
# cand mathc user's system setting
# TODO: finish this class
class EmbossPack:
    #Josh
    def __init__(self, inDirectory):
        #self.inFiles = inDirectory
        self.ORF_find(str(inDirectory))
    def get_leaf(path):
        head, tail = ntpath.split(path)
        return tail
    def ORF_find(self, folder):
        #folder name will be based on title
        #basepath = os.path.dirname(os.path.realpath(__file__))+'/'+folder
        files = glob.glob(folder+'/*')
        for i in files:
            print i
            #k = pipes.quote(i)
            #outname = basepath+'/f2/'+get_leaf(k)
            #args = 'getorf -sequence %s -outseq %s_ORF.fa -minsize 117 -find 3' % (k, outname)
            #subprocess.call(args, shell=True)