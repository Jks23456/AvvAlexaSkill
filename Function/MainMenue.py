import json
from abstrClass.Menue import Menue

from Function.Board import Board
from Function.Route import Route

class MainMenue(Menue):

    def __init__(self):
        super().__init__()
        self.funcMap ={
            "HaltIntent": Board,
            "RouteIntent": Route
        }

    def input(self, pIntent):
        if pIntent["intent"] in self.funcMap.keys():
            self.openMenue(self.funcMap[pIntent["intent"]]())
            self.nextNode.update(pIntent)
        else:
            pIntent["return"]["type"] = "statement"
            pIntent["return"]["msg"] = "Ein Fehler ist Aufgetreten... Versuch es noch einmal"