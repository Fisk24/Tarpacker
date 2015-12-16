import re

class ManifestParser():
    def __init__(self, man):
        self.man  = man
        self.data = {}

    def __str__(self):
        return self.printManifest()

    def printManifest(self):
        for key in self.data:
            print(key+":")
            for i in self.data[key]:
                print("\t"+i)

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


