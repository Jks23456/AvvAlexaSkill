import avv
import json

from Function.MainMenue import MainMenue

if __name__ == '__main__':
    intentJson = json.loads(open("Templates/intent.json").read())
    main = MainMenue()

    while(True):
        intent = intentJson.copy()
        print("Intent:")
        intent["intent"] = input()
        print("Input:")
        intent["input:"] = input()
        main.update(intent)
        print(intent)
        print(" ")