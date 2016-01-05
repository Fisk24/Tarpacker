import os, shutil, tarfile, datetime
from lib.config import Config
from lib.mplib  import ManifestParser

class Pack():
    def __init__(self, args):
        self.conf     = Config("settings.json")
        self.manifest = ManifestParser(self.conf.data["manifest"]["file"])
        self.manifest.parseManifest()

        self.args    = args
        self.tmpdir  = "archives/"
        self.extract = self.tmpdir+"extraction.csv"
        self.migrate = self.setMigrationLocation()
        
        self.calculateTotalSize()
        self.prepairTempDir()
        self.createArchiveDir()
        self.createBackup()

    def calculateTotalSize(self):
        print("Calculating totals...")
        # Total files to be compressed accross all archives
        # Compressing X files and Y folders into Z archives
        files    = 0
        folders  = 0
        archives = 0
        for section in self.manifest.data:
            archives += 1
            for i in self.manifest.data[section]:
                if os.path.isdir(i):
                    folders += 1
                else:
                    files += 1

        print("Compressing {0} files and {1} folders into {2} archives...".format(files, folders, archives))


    def calculateTotalsPerSection(self):
        pass
        
    def createBackup(self):
        for section in self.manifest.data:
            # for every section of the manifest create a new tarball named after the manifest
            # check if archive file is in the way
            tarname = "{tar}.tar.gz".format(tar=section) 
            tarpath = self.tmpdir+tarname
            if self.askOverwrite(self.migrate+tarname):
                with tarfile.open(tarpath, "w:gz") as tar:
                    # for every file listed under the given section, add the file to the tarball
                    print("Created new tar archive: {0}".format(tarpath))
                    for item in self.manifest.data[section]:
                        meta = self.createItemMetadata(item)
                        self.addTarItem(tar, item, meta)
                        self.addMetadata(item, meta)

                    self.addExtractionManifest(tar)
            
                self.migrateArchive(tarname)
            else:
                print("Skiping: {0}".format(tarname))
                    
        print("Finished!")

    def migrateArchive(self, src):
        old = self.tmpdir+src
        new = self.migrate+src
        print("Moving archive {temp} to {dest}".format(temp=old, dest=new))
        self.createFolderSafely(self.migrate)
        shutil.move(old, new)

    def addExtractionManifest(self, tarball):
        # add extraction manifest file to the archive and delete the original file
        print("Cleaning...")
        tarball.add(self.extract, arcname="extraction.csv")
        os.remove(self.extract)

    def addTarItem(self, tar, item, meta):
        print("adding: {0}".format(item))
        tar.add(item, arcname=meta[0])

    def addMetadata(self, item, meta):
        with open(self.extract, "a") as man:
            # generate metadata csv line
            x = "{0},{1}".format(meta[0], meta[1])
            # write to end of file
            print("meta: {0}".format(x))
            man.write(x)

    def createItemMetadata(self, item):
        name = item.split("/")[-1]
        path = ""
        for i in item.split("/")[0:-1]:
            path += i+"/"

        return [name, path]

    def createArchiveDir(self):
        try:
            os.mkdir(self.tmpdir)
        except FileExistsError:
            print("Tried to make a temporary directory, but then realized I didn't need to...")
        except Exception as e:
            print(e)

    def createFolderSafely(self, fol, echo=0):
        try:
            os.mkdir(fol)
        except Exception as e:
            if echo:
                print(e)

    def prepairTempDir(self):
        shutil.rmtree(self.tmpdir)

    def fixDirString(self, text):
        # change any given string to have a '/' at the end
        if text[-1] == "/":
            return text
        else:
            return text+"/"

    def setMigrationLocation(self):
        if self.args.location:
            return self.fixDirString(self.args.location)
        else:
            return self.fixDirString(self.conf.data["packing"]["location"].format(date=datetime.date.today()))

    def askOverwrite(self, item):
        if os.path.isfile(item):
            print("{0} exists. Overwrite?".format(item))
            while 1:
                opt = input("[Y/N]")
                if opt.lower()=="y":
                    return True
                elif opt.lower()=="n":
                    return False
                else:
                    print("Press \"Y\" or \"N\"!")

        else:
            return True
































