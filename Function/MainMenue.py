import json
from abstrClass.Menue import Menue
from Function.StationBoard import StationBoard

class MainMenue(Menue):

    def __init__(self):
        print("Test")
        super().__init__()
        self.funcMap ={
            "HaltIntent" : StationBoard
        }

    def input(self, pIntent):
        if pIntent["intent"] in self.funcMap.keys():
            self.nextNode = self.funcMap[pIntent["intent"]]()
            self.nextNode.update(pIntent)
        else:
            pIntent["return"]["type"] = "statement"
            pIntent["return"]["msg"] = "Ein Fehler ist Aufgetreten... Versuch es noch mal"