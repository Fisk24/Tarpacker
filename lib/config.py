import json, sys

class Config():
    def __init__(self, cfile):
        self.default = {
                "conf_file":cfile,
                "packing"  :{
                    "location":"/home/fisk/BKUP-{date}"
                    },
                "manifest" :{
                    "file" :"manifest.mf"
                    },
                "ssh":{
                    "user"  :"",
                    "pwd"   :"",
                    "server":""
                    }
                }

        self.data = {}
        self.load()

    def save(self):
        with open(self.default["conf_file"], "w") as file:
            json.dump(self.data, file)

    def load(self):
        try:
            with open(self.default["conf_file"], "r") as file:
                self.data = json.load(file)
        except FileNotFoundError as e:
            print("SETTINGS NOT FOUND! Generating...")
            self.gen()
            self.load()

    def gen(self):
        with open(self.default["conf_file"], "w") as file:
            json.dump(self.default, file)

if __name__ == "__main__":
    # Config test, run as standalone
    conf = Config("settings.json")
    #conf.gen()
    conf.load()
    print(conf.data)
    conf.save()
