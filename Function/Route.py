import json

from abstrClass.Menue import Menue
from Function.SearchStation import SearchStation

class Route(Menue):

    def __init__(self):
        super().__init__()
        self.options = json.loads(open("Data/option.json").read())
        self.arr = {}
        self.dep = {}

    def input(self, pIntent):
        if "dep" not in pIntent["input"].keys():
            self.dep = self.options["board"]["station"]
        else:
            pass

        if "arr" not in pIntent["input"].keys():
            self.openMenue(SearchStation())
            self.nextFunktion=self.searchResult
            pIntent["return"]["type"] = "question"
            pIntent["return"]["msg"] = "Wo hin möchtest du fahren?"

    def searchResult(self, pInte):
        pass