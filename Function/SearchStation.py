import json
import avv

from abstrClass.Menue import Menue

class SearchStation(Menue):

    def __init__(self):
        super().__init__()
        self.searchData = None
        self.dataCount = 0

    def input(self, pIntent):#["search"]["querry"]
        if pIntent["intent"]=="StationIntent":
            self.searchData = avv.searchForStation(pIntent["selected"])
            if self.searchData["match"]:
                pIntent["searchStation"] = {"err": False,
                                            "result": self.searchData["obj"]}
            else:
                self.nextFunktion = self.noMatch
                pIntent["return"]["type"] = "question"
                pIntent["return"]["msg"] = str("Meinst du vielleicht {}?").format(
                    self.searchData["suggestion"][str(self.dataCount)]["name"])
        else:
            pIntent["err"]=True



    def noMatch(self, pIntent):
        if pIntent["intent"] == "YesIntent":
            pIntent["searchStation"] = {"result": self.searchData["suggestion"][str(self.dataCount)]["obj"]}
        elif pIntent["intent"] == "NoIntent":
            self.dataCount += 1
            if self.dataCount >= 2:
                pIntent["searchStation"] = {"err": True,
                                            "result": ""}
                pIntent["return"]["type"] = "statement"
                pIntent["return"]["msg"] = str("Mhh... Ich konnte dich dann nicht verstehen!")
                pIntent["isComplete"] = True
            else:
                pIntent["return"]["type"] = "question"
                pIntent["return"]["msg"] = str("Meinst du vielleicht {}?").format(self.searchData["suggestion"][str(self.dataCount)]["name"])
