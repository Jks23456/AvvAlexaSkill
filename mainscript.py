import avv
import json
from os import path
from Function.MainMenue import MainMenue

if __name__ == '__main__':
    file = None
    if not path.exists("JNFLJNELJÖASFNCOW.json"):
        with open("Data/JNFLJNELJÖASFNCOW,json", 'w') as outfile:
            json.dump("""{"favorite":"None"}""", outfile)
    try:
        file = open("Data/{0}.json".format("JNFLJNELJÖASFNCOW"), "r")
    except FileNotFoundError:
        print("ERROR")

