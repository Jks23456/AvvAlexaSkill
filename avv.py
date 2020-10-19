import json
import requests
import random

def prepairPayload(pJson):
    pJson["id"]="".join(random.choice(["0", "1", "2", "3", "4", "5", "6", "8", "9", "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]) for i in range(16))
    pJson["auth"]={"type" : "AID",
                   "aid"  : "4vV1AcH3N511icH"
                   }

def searchForStation(pSearchString):
    pSearchString = pSearchString.lower()
    pSearchString = pSearchString.replace(",", "")
    pSearchString = pSearchString.replace(" ", "")
    pSearchString = pSearchString.replace("hauptbahnhof", "hbf")
    pSearchString = pSearchString.replace("bahnhof", "bf")

    payload = json.loads(open("Templates/search.json").read())
    prepairPayload(payload)
    payload["svcReqL"][0]["req"]["input"]["loc"]["name"]=pSearchString

    r = requests.post("https://auskunft.avv.de/bin/mgate.exe?rnd=1602964183882", json=payload)

    data = r.json()
    print(str(data).replace("True","true").replace("False","false"))
    if data["err"] != "OK":
        return None

    try:
        tmp = {"tag": "searchResult",
               "sTerm": pSearchString,
               "match": False
               }
        sug = {}
        for place in data["svcResL"][0]["res"]["match"]["locL"]:
            compString = place["name"]
            compString = compString.lower()
            compString = compString.replace(",", "")
            compString = compString.replace(" ", "")

            if compString == pSearchString:
                tmp["match"] = True
                tmp["obj"] = place
                tmp["suggestions"] = ""
                break
            elif len(sug.keys()) < 5:
                sug[str(len(sug.keys()))] = place
        if not tmp["match"]:
            tmp["obj"] = ""
            tmp["suggestions"] = sug
        return tmp
    except:
        return None

def getStationBoard(pBusStoppJson, pLength):
    payload = json.loads(open("Templates/board.json").read())
    prepairPayload(payload)

    payload["svcReqL"][0]["req"]["stbLoc"]["name"] = pBusStoppJson["name"]
    payload["svcReqL"][0]["req"]["stbLoc"]["lid"] = pBusStoppJson["lid"]

    r = requests.post("https://auskunft.avv.de/bin/mgate.exe?rnd=1602964183882", json=payload)

    con_json = {}
    data = r.json()
    id = -1
    for set in data["svcResL"][0]["res"]["jnyL"]:
        id += 1

        tmp = {}
        tmp["id"] = str(id)
        tmp["haltestelle"] = set["dirTxt"]

        tmp["ankunft"] = set["stbStop"]["dTimeS"]
        if "dTimeR" in set["stbStop"]:
            tmp["verspaetung"] = set["stbStop"]["dTimeR"]
        print(str(set).replace("True","true").replace("False","false"))
        plt = set["dirFlg"]
        if plt in con_json.keys():
            if len(con_json[plt].keys()) < pLength:
                con_json[plt][str(len(con_json[plt].keys()))] = tmp
        else:
            con_json[plt] = {}
            con_json[plt][str(0)] = tmp

    i = 0
    busList = []
    for set in data["svcResL"][0]["res"]["common"]["prodL"]:
        if "pid" in set.keys():
            busList.append(set)

    for plt in con_json:
        for row in con_json[plt]:
            obj = busList[int(con_json[plt][row]["id"])]
            tmp = {}
            tmp["name"] = obj["name"]
            tmp["nummer"] = obj["number"]
            if "prodCtx" in obj.keys() and "catOutL" in obj["prodCtx"].keys():
                tmp["art"] = obj["prodCtx"]["catOutL"]
            else:
                tmp["art"] = ""
            con_json[plt][row]["bus"] = tmp

    return con_json

def getRoute(pBusStationJsonDep, pBusStationJsonArr, pLength):
    payload = json.loads(open("Templates/route.json").read())
    prepairPayload(payload)
    payload["svcReqL"][0]["req"]["depLocL"][0] = {"name" : pBusStationJsonDep["name"],
                                                  "lid"  : pBusStationJsonDep["lid"],
                                                  "type" : pBusStationJsonDep["type"],
                                                  "crd"  : {"x" : pBusStationJsonDep["crd"]["x"],
                                                            "y" : pBusStationJsonDep["crd"]["y"]
                                                            }
                                                  }

    payload["svcReqL"][0]["req"]["arrLocL"][0] = {"name": pBusStationJsonArr["name"],
                                                  "lid": pBusStationJsonArr["lid"],
                                                  "type": pBusStationJsonArr["type"],
                                                  "crd": {"x": pBusStationJsonArr["crd"]["x"],
                                                          "y": pBusStationJsonArr["crd"]["y"]
                                                          }
                                                  }

    r = requests.post("https://auskunft.avv.de/bin/mgate.exe?rnd=1602964183882", json=payload)


    print(str(r.json()).replace("False", "false").replace("True", "true"))

    data = r.json()
    icoX = data["svcResL"][0]["res"]["common"]["icoL"]
    icoXTable = json.loads(open("Data/nameToType.json").read())

    ret_Json = json.loads("{}")

    counter = 0
    for connection in data["svcResL"][0]["res"]["outConL"]:
        conDic = {"dep": connection["dep"]["dTimeS"], "dur" : connection["dur"], "chg" : connection["chg"]}
        conDic["route"] = {}
        id = 0
        for conStep in connection["secL"]:
            tmp={"type" : ""}

            if icoX[conStep["icoX"]]["res"] in icoXTable.keys():
                tmp["type"] = icoXTable[icoX[conStep["icoX"]]["res"]].copy()
            else:
                print(icoX[conStep["icoX"]]["res"])

            if conStep["type"] == "JNY":
                arr = {"name": "",
                       "plattform": conStep["arr"]["aPlatfS"],
                       "difPlattform": conStep["arr"]["aPlatfS"],
                       "time": conStep["arr"]["aTimeS"]
                       }

                if "aPlatR" in conStep["arr"].keys():
                    arr["difPlattform"] = conStep["arr"]["aPlatfR"]

                if "aTimeR" in conStep["arr"].keys():
                    if len(conStep["arr"]["aTimeR"]) == 8:
                        arr["delTime"] = conStep["arr"]["aTimeR"][2:]
                    else:
                        arr["delTime"] = conStep["arr"]["aTimeR"]

                dep = {"name": "",
                       "plattform": conStep["dep"]["dPlatfS"],
                       "difPlattform": conStep["dep"]["dPlatfS"],
                       "time": conStep["dep"]["dTimeS"]
                       }

                if "dPlatfR" in conStep["dep"].keys():
                    dep["difPlattform"] = conStep["dep"]["dPlatfR"]


                if "dTimeR" in conStep["dep"].keys():
                    if len(conStep["arr"]["aTimeR"]) == 8:
                        dep["delTime"] = conStep["dep"]["dTimeR"][2:]
                    else:
                        dep["delTime"] = conStep["dep"]["dTimeR"]

                ctxRecon = str(conStep["jny"]["ctxRecon"]).split("@")
                for s in ctxRecon:
                    if s.startswith("O="):
                        if dep["name"] == "":
                            dep["name"] = s[2:]
                        else:
                            arr["name"] = s[2:]
                    elif s.startswith("$") and not s.startswith("$A="):
                        splt = s.split("$")
                        for i in splt:
                            if i == "":
                                splt.remove(i)

                        if tmp["type"]["type"] == "bus":
                            tmp["type"]["line"] = splt[2].replace(" ", "").replace("Bus", "")
                        else:
                            tmp["type"]["line"] = splt[2].replace(" ", "")
                    tmp["dep"] = dep
                    tmp["arr"] = arr

            elif conStep["type"] == "WALK":
                tmp["dist"] = conStep["gis"]["dist"]
                arr ={"name": "",
                      "time": conStep["arr"]["aTimeS"]
                      }

                dep ={"name": "",
                      "time": conStep["dep"]["dTimeS"]
                      }

                ctxRecon = conStep["gis"]["ctx"]
                for s in str(ctxRecon).split("@"):
                    if s.startswith("O="):
                        if dep["name"] == "":
                            dep["name"] = s[2:]
                        else:
                            arr["name"] = s[2:]

                print([arr,dep])

            conDic["route"][str(id)] = tmp
            id+=1

        ret_Json[str(counter)] = conDic
        counter+=1

        if counter == pLength:
            break

    return ret_Json







