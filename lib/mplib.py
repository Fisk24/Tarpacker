import re
from lib import logger

class ManifestParser():
    def __init__(self, man):
        self.man  = man
        self.data = {}

    def __str__(self):
        return self.printManifest()

    def info(self):
        logger.out("#==== Mainfest Info ====#")
        logger.out("| {0:21} |".format(self.man))
        logger.out("#=======================#")
        self.printManifest()

    def printManifest(self):
        for key in self.data:
            logger.out(key+":")
            for i in self.data[key]:
                logger.out("\t"+i)

        return ""

    def parseManifest(self):
        # open manifest file, and parse its data into a dictionary self.data
        currentKey = ""
        with open(self.man, 'r') as manifest:
            for line in manifest.readlines():
                if re.search(r"^\[", line):
                    currentKey = self._addDataKey(line)
                elif re.search(r"(^\n)",line):
                    pass
                else:
                    self.data[currentKey].append(line.strip("\n"))
    
    def _addDataKey(self, line):
        # in the class method self.parseManifest, clean up string by removing brackets, then create a dictionary key using the clean string
        x = line
        for i in ["[", "]", "\n"]:
            x = x.replace(i, "")
            
        self.data[x] = []
        return x


