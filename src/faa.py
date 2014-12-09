class FaaPack:
    def __init__(self):
        self.folder = input('Enter the folder of faas that need to be concatenated')
    def concatFiles(self):
        subprocess.call(['cd', self.folder])
        subprocess.call(['cat', '*', '.faa', '>', '../allTogether.faa'])