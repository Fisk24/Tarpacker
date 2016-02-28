import os, getpass

class Setup():
    def __init__(self):
        self.configdir   = "/home/{0}/.config/tarpacker".format(getpass.getuser())
        self.archivedir  = self.configdir+"/tmparchives"
        self.manifestdir = self.configdir+"/manifest.mf"
        self.manTemplate = '''[misc]'''
        
        if not os.path.isdir(self.configdir):
            self.createConfigDir()
            self.createTmpArchiveDir()
            self.createDefaultManifest()

    def createDefaultManifest(self):
        with open(self.manifestdir, "w") as man:
            man.write(self.manTemplate)
        print("Created default manifest file at {0}".format(self.manifestdir))

    def createTmpArchiveDir(self):
        # incrementaly create directory tree
        x = ""
        for i in self.archivedir.split("/"):
            x += i+"/"
            try:
                os.mkdir(x)
            except:
                pass
        
        print("Created {0}".format(self.archivedir))

    def createConfigDir(self):
        # incrementaly create directory tree
        x = ""
        for i in self.configdir.split("/"):
            x += i+"/"
            try:
                os.mkdir(x)
            except:
                pass

        print("Created {0}".format(self.configdir))
