import re
from lib.config import Config as Conf

class Config():
    def __init__(self, args, setup):
        self.args  = args
        self.setup = setup

        self.conf  = Conf(self.setup.configdir+"/settings.json")

        self.processArgs()

    def processArgs(self):
        if self.args.set:
            self.setValue()
        if self.args.get:
            self.getValue()
        if self.args.list:
            self.listValues()

    def setValue(self):
        try:
            # itterate through the values each key returns. Assuming each returned value is a dictionary, use the next key in the previously returned dictionary.
            keys = self.args.set[0].split(".")
            self.conf.data[keys[0]][keys[1]]
            self.conf.data[keys[0]][keys[1]] = self.args.set[1]
            self.conf.save()

            print(self.conf.data[keys[0]][keys[1]])

        except IndexError:
            print("Too few arguments")

        except TypeError as e:
            print("Invalid value...")
        except KeyError as e:
            print("The key {0} does not exist! Use \"tp config --list\" to see available values.".format(self.args.get))


    def getValue(self):
        try:
            # itterate through the values each key returns. Assuming each returned value is a dictionary, use the next key in the previously returned dictionary.
            keys = self.args.get.split(".")
            data = self.conf.data
            for key in keys:
                data = data[key]

            print("{key} = {value}".format(key=self.args.get, value=data))
        except TypeError as e:
            print("Invalid value...")
        except KeyError as e:
            print("The key {0} does not exist! Use \"tp config --list\" to see available values.".format(self.args.get))

    def listValues(self):
        for section in self.conf.data:
            if section != "conf_file" and section != "status":
                print("{0}:".format(section))
                for key in self.conf.data[section]:
                    print(" |--> {0} = {1}".format(key, self.conf.data[section][key]))
