"""
TODO:
    make it so that askYesNo can ask multiple times in case of a typo in the responce
    perhaps a limit on the number of trys that the user has, can also be implimented
"""

import tarfile, sys, os, csv, shutil
from distutils.dir_util import copy_tree
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
        self.warnNoAsk()
        self.argsCheckInFile()
        self.printArchiveMembers()
        if self.askYesNo("Continue?"):
            self.extractArchive()
            self.moveExtractedFiles()

    def moveFilesSafely(self, item, target):
        # copy file using shutil.move(), potentialy overwriting existing files, and creating directories as needed
        try:
            # Check if copying would result in overwriting files. if so, ask the user if it is ok to overwrite.
            if (os.path.isdir(target+item) or os.path.isfile(target+item)):
                #if the user answers no, return so as to avoid moving the files
                if not self.askYesNo(msg="The file or directory \"{path}\" exists!/nWould you like to overwrite it?".format(path=target+item)):
                    logger.out("[ INFO ] Item skipped...")
                    return
            if os.path.isdir(self.tmpdir+item):
                copy_tree(self.tmpdir+item, target+item, verbose=1)
                shutil.rmtree(self.tmpdir+item)
            elif os.path.isfile(self.tmpdir+item):
                shutil.copy2(self.tmpdir+item, target+item)
                os.remove(self.tmpdir+item)
        except FileNotFoundError as e:
            logger.out("[ FATAL ] {}".format(e))
            os._exit(1)

    def moveExtractedFiles(self):
        # move extracted files from the temporary directory 
        # into the location specified in the extraction manifest
        if os.path.isfile(self.extract):
            # if the exctraction manifest exists, then extract according to its contents
            self.extractUsingManifest() 
        else:
            # otherwise abort
            logger.out("[ ERROR ] No extraction manifest detected! Aborting.")

    def extractUsingManifest(self):
        # open the extraction manifest and...
        try:
            with open(self.extract, mode='r', newline='\n') as csvFile:
                csvData = csv.reader(csvFile, delimiter=',')
                for row in csvData:
                    # for every item found there in, copy the file from the temp directory 
                    # to the one contained in the current itteration of the for loop
                    # the extraction manifest data structure is: 0:child_file, 1:target_directory
                    self.moveFilesSafely(row[0], row[1])
        except shutil.Error as e:
            logger.out(e)

    def extractArchive(self):
        archive = self.args.in_file
        with tarfile.open(archive, "r|*") as tar:
            
            import os
            
            def is_within_directory(directory, target):
                
                abs_directory = os.path.abspath(directory)
                abs_target = os.path.abspath(target)
            
                prefix = os.path.commonprefix([abs_directory, abs_target])
                
                return prefix == abs_directory
            
            def safe_extract(tar, path=".", members=None, *, numeric_owner=False):
            
                for member in tar.getmembers():
                    member_path = os.path.join(path, member.name)
                    if not is_within_directory(path, member_path):
                        raise Exception("Attempted Path Traversal in Tar File")
            
                tar.extractall(path, members, numeric_owner=numeric_owner) 
                
            
            safe_extract(tar, path=self.tmpdir)

    def printArchiveMembers(self):
        members = []
        archive = self.args.in_file
        with tarfile.open(archive, "r|*") as tar:
            members = tar.getnames()
            for i in members:
                logger.out(i)

        logger.out("{0} files are ready for extraction.".format(len(members)))

    def warnNoAsk(self):
        if self.args.noask:
            logger.out("### WARNING NOASK FLAG HAS BEEN PASSED. SKIPPING ALL QUESTIONS ###")
                
    def argsCheckInFile(self):
        if not self.args.in_file:
            logger.out("What am I unpacking? Do \"tp unpack -if [archive]\"")
            os._exit(1)

    def askYesNo(self, msg="Are you sure?", yes="yes", no="no"):
        if not self.args.noask:
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
        else:
            logger.out("[ WARN ] Question skipped in NOASK mode...")
            return 1
