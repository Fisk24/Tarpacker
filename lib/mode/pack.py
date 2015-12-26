import os, tarfile
from lib.config import Config
from lib.mplib  import ManifestParser

class Pack():
    def __init__(self, args):
        self.conf     = Config("settings.json")
        self.manifest = ManifestParser(self.conf.data["manifest"]["file"])
        self.manifest.parseManifest()

        self.createArchiveDir()
        self.createBackup()
        
    def createBackup(self):
        for section in self.manifest.data:
            print("Tarball({tar}.tar.gz):".format(tar=section))
            for item in self.manifest.data[section]:
                print(self.createItemMetadata(item))

    def createItemMetadata(self, item):
        name = item.split("/")[-1]
        path = ""
        for i in item.split("/")[0:-1]:
            path += i+"/"

        return [name, path]

    def createArchiveDir(self):
        try:
            os.mkdir("archives/")
        except Exception as e:
            print(e)
