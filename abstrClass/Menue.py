class Menue:

    def __init__(self):
        self.nextNode = None
        self.mainMsg = ""

    def update(self, pIntent):
        if self.nextNode != None:
            self.nextNode.update(pIntent)
            if pIntent["isComplete"]:
                self.nextNode = None
                pIntent["isComplete"] = False
                self.input(pIntent)
        else:
            self.input(pIntent)

    def openMenue(self, pMenueClass):
        self.nextNode = pMenueClass

    def input(self, pIntent):
        pass