import avv
import json

if __name__ == '__main__':
    print(avv.getStationBoard(avv.searchForStation("Hansemannplatz")['obj'],10))
    #print(avv.getRoute(avv.searchForStation("Aachen bushof")['obj'], avv.searchForStation("Aachen hbf")['obj'], 5))