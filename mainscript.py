import avv
import json

if __name__ == '__main__':
    print(avv.getStationBoard(avv.searchForStation("Haaren denkmal")['obj']))
    print(avv.getRoute(avv.searchForStation("Aachen schanz bf")['obj'], avv.searchForStation("Haaren markt")['obj']))