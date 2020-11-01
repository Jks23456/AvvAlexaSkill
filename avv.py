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

def getStationBoard(pBusStoppJson):
    payload = json.loads(open("Templates/board.json").read())
    prepairPayload(payload)
    payload["svcReqL"][0]["req"]["stbLoc"]["name"] = pBusStoppJson["name"]
    payload["svcReqL"][0]["req"]["stbLoc"]["lid"] = pBusStoppJson["lid"]
    r = requests.post("https://auskunft.avv.de/bin/mgate.exe?rnd=1602964183882", json=payload)
    data = r.json()
    ret_json = json.loads("{}")
    for set in data["svcResL"][0]["res"]["jnyL"]:
        tmp = {"type": data["svcResL"][0]["res"]["common"]["prodL"][set["prodX"]],
               "dirText": set["dirTxt"],
               "dep": {"time": set["stbStop"]["dTimeS"],
                       "delay": set["stbStop"]["dTimeS"],
                       "platform": "None",
                       "difPlatform":"None"
                      }
               }
        if "dPlatfS" in set["stbStop"].keys():
            tmp["dep"]["platform"] = set["stbStop"]["dPlatfS"]
            tmp["dep"]["difPlatform"] = set["stbStop"]["dPlatfS"]
        else:
            print(set["stbStop"].keys())

        if "dPlatfR" in set["stbStop"].keys():
            tmp["dep"]["difPlatform"] = set["stbStop"]["dPlatfR"]

        if "dTimeR" in set["stbStop"].keys():
            tmp["dep"]["delay"] = set["stbStop"]["dTimeR"]

        if "dPlatR" in set["stbStop"].keys():
            tmp["dep"]["difPlatform"] = set["stbStop"]["dPlatR"]

        if tmp["dep"]["platform"] not in ret_json.keys():
            ret_json[tmp["dep"]["platform"]] = {}

        ret_json[tmp["dep"]["platform"]][len(ret_json[tmp["dep"]["platform"]])] = tmp

    print(ret_json)
    return ret_json

def getRoute(pBusStationJsonDep, pBusStationJsonArr):
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


    #print(str(r.json()).replace("False", "false").replace("True", "true"))

    data = r.json()

    ret_Json = json.loads("{}")

    counter = 0
    for connection in data["svcResL"][0]["res"]["outConL"]:
        add=True
        #print(str(connection).replace("False", "false").replace("True", "true"))
        conDic = {"dep": connection["dep"]["dTimeS"], "dur" : "None", "chg" : ""}

        if "dur" in connection.keys():
            conDic["dur"] = connection["dur"]
        else:
            add = False

        if "chg" in connection.keys():
            conDic["chg"]=connection["chg"]
        else:
            add = False

        conDic["route"] = {}
        id = 0
        for conStep in connection["secL"]:
            tmp = {"travel": conStep["type"], "type": ""}

            if tmp["travel"] == "JNY":
                tmp["type"] = data["svcResL"][0]["res"]["common"]["prodL"][conStep["jny"]["prodX"]]

                arr = {"dirText": "",
                       "platform": conStep["arr"]["aPlatfS"],
                       "difPlatform": conStep["arr"]["aPlatfS"],
                       "time": conStep["arr"]["aTimeS"]
                       }

                if "aPlatR" in conStep["arr"].keys():
                    arr["difPlatform"] = conStep["arr"]["aPlatfR"]

                if "aTimeR" in conStep["arr"].keys():
                    if len(conStep["arr"]["aTimeR"]) == 8:
                        arr["delTime"] = conStep["arr"]["aTimeR"][2:]
                    else:
                        arr["delTime"] = conStep["arr"]["aTimeR"]

                dep = {"dirText": "",
                       "platform": conStep["dep"]["dPlatfS"],
                       "difPlatform": conStep["dep"]["dPlatfS"],
                       "time": conStep["dep"]["dTimeS"]
                       }

                if "dPlatfR" in conStep["dep"].keys():
                    dep["difPlatform"] = conStep["dep"]["dPlatfR"]


                if "dTimeR" in conStep["dep"].keys():
                    if len(conStep["arr"]["aTimeR"]) == 8:
                        dep["delTime"] = conStep["dep"]["dTimeR"][2:]
                    else:
                        dep["delTime"] = conStep["dep"]["dTimeR"]

                ctxRecon = str(conStep["jny"]["ctxRecon"]).split("@")
                for s in ctxRecon:
                    if s.startswith("O="):
                        if dep["dirText"] == "":
                            dep["dirText"] = s[2:]
                        else:
                            arr["dirText"] = s[2:]
                    elif s.startswith("$") and not s.startswith("$A="):
                        splt = s.split("$")
                        for i in splt:
                            if i == "":
                                splt.remove(i)
                    tmp["dep"] = dep
                    tmp["arr"] = arr

            elif tmp["travel"] == "WALK":
                tmp["dist"] = conStep["gis"]["dist"]
                arr ={"dirText": "",
                      "time": conStep["arr"]["aTimeS"]
                      }

                dep ={"dirText": "",
                      "time": conStep["dep"]["dTimeS"]
                      }

                ctxRecon = conStep["gis"]["ctx"]
                for s in str(ctxRecon).split("@"):
                    if s.startswith("O="):
                        if dep["dirText"] == "":
                            dep["dirText"] = s[2:]
                        else:
                            arr["dirText"] = s[2:]

                print([arr,dep])

            conDic["route"][str(id)] = tmp
            id+=1
        if add:
            ret_Json[str(counter)] = conDic
            counter+=1

    return ret_Json

def convertTime(pTime):
    if len(pTime) > 6:
        pTime = pTime[2:]
    h = pTime[0:2]
    m = pTime[2:4]
    return [int(h),int(m)]







