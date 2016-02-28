import os, shutil, tarfile, datetime
from lib        import logger
from lib.config import Config
from lib.mplib  import ManifestParser

class Pack():
    def __init__(self, args, setup):
        # Create config object
        self.conf = Config(setup.configdir+"/settings.json")

        # args... 
        self.args = args

        # Create manifest parser object
        self.manifest = self.argsManifestFile()
        self.manifest.parseManifest()
        
        # Directories
        self.setup   = setup
        self.tmpdir  = self.setup.archivedir
        self.extract = self.setup.archivedir+"/extraction.csv"
        self.migrate = self.setMigrationLocation()

        # Process
        logger.tear()
        logger.out("Started packing mode...")
        self.showStatusLast()
        self.argsNoAsk()
        self.argsManifestInfo()
        self.calculateTotalSize()
        self.prepairTempDir()
        self.createArchiveDir()
        self.createBackup()

    def calculateTotalSize(self):
        logger.out("Calculating totals...")
        # Total files to be compressed accross all archives
        # Compressing X files and Y folders into Z archives
        files    = 0
        folders  = 0
        archives = 0
        for section in self.manifest.data:
            if self.args.section and (section in self.listManifestSections()):
                archives += 1
                for i in self.manifest.data[section]:
                    if os.path.isdir(i):
                        folders += 1
                    else:
                        files += 1
        if files+folders:
            logger.out("Compressing {0} files and {1} folders into {2} archives...".format(files, folders, archives))
        else:
            logger.out("Nothing to backup! For help adding files and folders, type \"tp manifest --help\"")


    def calculateTotalsPerSection(self):
        pass
        
    def createBackup(self):
        for section in self.manifest.data:
            # for every section of the manifest create a new tarball named after the manifest section
            # if --section is passed, only backup section if it is specified
            # check if archive file is in the way
            tarname = "{tar}.tar.gz".format(tar=section) 
            tarpath = self.tmpdir+tarname
            if self.args.section and (section in self.listManifestSections()):
                if self.askOverwrite(self.migrate+tarname):
                    with tarfile.open(tarpath, "w:gz") as tar:
                        # for every file listed under the given section, add the file to the tarball
                        logger.out("Created new tar archive: {0}".format(tarpath))
                        for item in self.manifest.data[section]:
                            meta = self.createItemMetadata(item)
                            self.addTarItem(tar, item, meta)
                            self.addMetadata(item, meta)

                        self.addExtractionManifest(tar)
            
                    self.migrateArchive(tarname)
                else:
                    logger.out("Skiping: {0}".format(tarname))

        logger.out("Finished!")
        self.updateStatusLast()

    def migrateArchive(self, src):
        old = self.tmpdir+src
        new = self.migrate+src
        logger.out("Moving archive {temp} to {dest}".format(temp=old, dest=new))
        self.createFolderSafely(self.migrate)
        shutil.move(old, new)

    def addExtractionManifest(self, tarball):
        # add extraction manifest file to the archive and delete the original file
        tarball.add(self.extract, arcname="extraction.csv")
        os.remove(self.extract)

    def addTarItem(self, tar, item, meta):
        logger.out("adding: {0}".format(item))
        tar.add(item, arcname=meta[0])

    def addMetadata(self, item, meta):
        with open(self.extract, "a") as man:
            # generate metadata csv line
            x = "{0},{1}\n".format(meta[0], meta[1])
            # write to end of file
            #print("meta: {0}".format(x))
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
            logger.out("Tried to make a temporary directory, but then realized I didn't need to...")
        except Exception as e:
            logger.out(e)

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
        # if a custom location was given, use it instead of the config value!
        if self.args.location:
            return self.fixDirString(self.args.location.format(date=datetime.date.today()))
        else:
            return self.fixDirString(self.conf.data["packing"]["location"].format(date=datetime.date.today()))

    def askOverwrite(self, item):
        # if the archive file already exists, ask to replace it... unless --noask is passed
        if not self.args.noask:
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
        else:
            logger.out("[ NOASK ]Question skipped in NoAsk mode...")
            return True

    def listManifestSections(self):
        # initial unsanitized sections list
        x = self.args.section.split(",")
        # sanitized sections list
        y = []

        for i in x:
            y.append(i.strip())

        return y

    def showStatusLast(self):
        logger.out("Last attempted backup was on {0}".format(self.conf.data["status"]["last"]))

    def updateStatusLast(self):
        date = datetime.date.today()
        time = datetime.datetime.now()

        self.conf.data["status"]["last"] = "{0} at {1}:{2}".format(date, time.hour, time.minute)
        self.conf.save()


    def argsManifestSections(self):
        if self.args.section:
            return True
        else:
            return False

    def argsNoAsk(self):
        if self.args.noask:
            logger.out("[ NOASK ]No-ask mode! WILL OVERWRITE PRE-EXISTING ARCHIVES!")

    def argsManifestInfo(self):
        if self.args.verbose:
            self.manifest.info()

    def argsManifestFile(self):
        if self.args.man:
            return ManifestParser(self.args.man)
        else:
            return ManifestParser(self.conf.data["manifest"]["file"])
