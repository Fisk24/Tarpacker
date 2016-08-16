import tarfile, sys, os, csv, shutil
from lib        import logger
from lib.config import Config

class Unpack():
    def __init__(self, args, setup):
        # Create config object
        self.conf = Config(setup.configdir+"/settings.json")

        # args... 
        self.args = args
        
        # Directories
        self.setup   = setup
        self.tmpdir  = self.setup.archivedir
        self.extract = self.setup.archivedir+"extraction.csv"

        #print(self.args)
        logger.tear()
        logger.out(self.args, 0)
        logger.out("Started unpacking mode...")
        self.argsCheckInFile()
        self.printArchiveMembers()
        if self.askYesNo("Continue?"):
            self.extractArchive()
            self.moveExtractedFiles()

    def moveExtractedFiles(self):
        if os.path.isfile(self.extract):
            self.extractUsingManifest() 
        else:
            logger.out("[ WARN ] No extraction manifest detected! Aborting.")

    def extractUsingManifest(self):
        try:
            with open(self.extract, mode='r', newline='\n') as csvFile:
                csvData = csv.reader(csvFile, delimiter=',')
                for row in csvData:
                    shutil.move(self.tmpdir+row[0], row[1])
        except shutil.Error as e:
            logger.out(e)

    def extractArchive(self):
        archive = self.args.in_file
        with tarfile.open(archive, "r|*") as tar:
            tar.extractall(path=self.tmpdir)

    def printArchiveMembers(self):
        members = []
        archive = self.args.in_file
        with tarfile.open(archive, "r|*") as tar:
            members = tar.getnames()
            for i in members:
                logger.out(i)

        logger.out("{0} files are ready for extraction.".format(len(members)))
                
    def argsCheckInFile(self):
        if not self.args.in_file:
            logger.out("What am I unpacking? Do \"tp unpack -if [archive]\"")
            os._exit(1)

    def askYesNo(self, msg="Are you sure?", yes="yes", no="no"):
        opt = input("{0} [{1}/{2}]:".format(msg, yes, no))
        if opt == yes:
            logger.out("User answered {0} to \"{1}\"".format(yes, msg), 0)
            return 1
        if opt == no:
            logger.out("User answered {0} to \"{1}\"".format(no, msg), 0)
            return 0
        else:
            print("You need to answer \"{0}\" or \"{1}\"".format(yes, no))
            logger.out("User failed to give a proper answer to \"{0}\"".format(msg), 0)
            return 0
