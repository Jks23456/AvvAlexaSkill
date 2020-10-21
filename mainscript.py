import avv
import json

from Function.MainMenue import MainMenue

if __name__ == '__main__':
    intentJson = json.loads(open("Templates/Intent.json").read())
    intentJson["intent"] = "HaltIntent"

    m = MainMenue()
    m.update(intentJson)

    print(intentJson["return"]["msg"])
