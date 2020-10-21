import json
import avv
import random

from abstrClass.Menue import Menue


class StationBoard(Menue):

    def __init__(self):
        super().__init__()
        self.options = json.loads(open("Data/option.json").read())["stationBoard"]
        self.searchJson = avv.searchForStation(self.options["station"])

    def input(self, pIntent):
        data = avv.getStationBoard(self.searchJson["obj"])
        sorKeys = sorted(data.keys())
        ret_msg = str("")

        pIntent["return"]["msg"]="<speak>"
        for group in sorKeys:
            lines = []
            for element in data[group]:
                if group == "None":
                    break
                element = data[group][element]
                data_lex = {"name":element["type"]["name"], "dirText":element["dirText"], "del": "..."}
                #Platform
                if group.startswith("H"):
                    data_lex["pltName"] = group.replace("H.", "Haltestelle ")
                else:
                    data_lex["pltName"] = "Gleis " + str(group)

                #Time
                time = avv.convertTime(element["dep"]["time"])
                data_lex["dep_hours"] = time[0]
                data_lex["dep_minutes"] = time[1]

                if element["dep"]["time"] != element["dep"]["delay"]:
                    time_del = avv.convertTime(element["dep"]["delay"])
                    data_lex["del_hours"] = time_del[0]
                    data_lex["del_minutes"] = time_del[1]
                    if time[0]*60+time[1] < time_del[0]*60+time_del[1]:
                        data_lex["del_extMin"] = (((24-time[0])*60)+time[1])+((time_del[0]*60)+time_del[1])
                    data_lex["del"] = random.choice(self.options["sentences"]["delMsg"]).format(data_lex)

                if len(lines) == 0:
                    lines.append(random.choice(self.options["sentences"]["newPlt"]).format(data_lex))
                elif len(lines)>= self.options["maxItems"]:
                    break
                else:
                    lines.append(random.choice(self.options["sentences"]["fromPlt"]).format(data_lex))

            for i in lines:
                if pIntent["return"]["msg"] == "":
                    pIntent["return"]["msg"] +="""<break time="3s"/> """ + i
                else:
                    pIntent["return"]["msg"] +="""<break time="1s"/>""" +i
        pIntent["return"]["msg"] += "</speak>"
        pIntent["isComplete"] = True