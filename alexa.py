import json
import avv
import random

from os import path
from flask import Flask
from flask_ask import Ask, request, statement, question, session, context

app = Flask(__name__)
ask = Ask(app, "/")

fileSet = None
fileOpt = None
fileChg = False
fileInit = False

flag = "None"

def initData():
    global flag
    global fileOpt
    global fileChg
    global fileSet
    global fileInit

    fileSet = json.loads(open("Data/option.json").read())
    file = None
    if not path.exists("User/{0}.json".format(session.user.userId)):
        file = open("User/{0}.json".format(session.user.userId), "a")
        file.write("""{"favorite":"None"}""")
        file.close()
    try:
        file = open("User/{0}.json".format(session.user.userId), "r")
    except FileNotFoundError:
        print("ERROR")

    fileOpt = json.loads(file.read())
    fileInit = True

@ask.launch
def start_skill():
    if not fileInit:
        initData()

    if (fileOpt["favorite"] == "None"):
        speech_text = "Welche Station möchtest du als Favorit auswählen?"
        flag = "setFavStation"
    else:
        speech_text = "Was möchtest du tuhen?"
        flag = "None"
    return question(speech_text).reprompt(speech_text).simple_card(speech_text)

@ask.intent("AMAZON.CancelIntent")
def AmazonCancelIntent():
    pass

@ask.intent("AMAZON.HelpIntent")
def AmazonHelpIntent():
    pass

@ask.intent("AMAZON.NavigateHomeIntent")
def AmazonNavigateHomeIntent():
    pass

@ask.intent("AMAZON.StopIntent")
def AmazonStopIntent():
    return statement("")

@ask.intent("HaltIntent")
def HaltIntent(STATION, TRANSPORT, ARTIKEL):
    global flag
    global fileOpt
    global fileSet
    global fileChg

    if not fileInit:
        initData()

    station = None
    if fileOpt["favorite"]=="None":
        station = avv.searchForStation("Aachen Hbf")
    else:
        station = avv.searchForStation(fileOpt["favorite"])

    data = None
    if station["match"]:
        data = avv.getStationBoard(station["obj"])
    else:
        print("Error")
        return statement("Das konnte ich leider nicht verstehen!")

    sorKeys = sorted(data.keys())
    ret_msg = "<speak>"
    for group in sorKeys:
        lines = []
        for element in data[group]:
            if group == "None":
                break
            element = data[group][element]
            data_lex = {"name": element["type"]["name"], "dirText": element["dirText"], "del": "..."}
            # Platform
            if group.startswith("H"):
                data_lex["pltName"] = group.replace("H.", "Haltestelle ")
            else:
                data_lex["pltName"] = "Gleis " + str(group)

            # Time
            time = avv.convertTime(element["dep"]["time"])
            data_lex["dep_hours"] = time[0]
            data_lex["dep_minutes"] = time[1]

            if element["dep"]["time"] != element["dep"]["delay"]:
                time_del = avv.convertTime(element["dep"]["delay"])
                data_lex["del_hours"] = time_del[0]
                data_lex["del_minutes"] = time_del[1]
                if time[0] * 60 + time[1] < time_del[0] * 60 + time_del[1]:
                    data_lex["del_extMin"] = (((24 - time[0]) * 60) + time[1]) + ((time_del[0] * 60) + time_del[1])
                data_lex["del"] = random.choice(fileSet["board"]["sentences"]["delMsg"]).format(data_lex)

            if len(lines) == 0:
                lines.append(random.choice(fileSet["board"]["sentences"]["newPlt"]).format(data_lex))
            elif len(lines) >= fileSet["board"]["maxItems"]:
                break
            else:
                lines.append(random.choice(fileSet["board"]["sentences"]["fromPlt"]).format(data_lex))
        first = True
        for i in lines:
            if ret_msg == "<speak>":
                ret_msg += i
                first = False
            elif first:
                first = False
                ret_msg += """<break time="1.5s"/> """ + i
            else:
                ret_msg += """<break time="0.5s"/>""" + i
    ret_msg += "</speak>"
    return statement(ret_msg)

@ask.intent("RouteIntent")
def RouteIntent(DEP,ARR):
    global flag
    global fileOpt
    global fileChg
    global fileSet
    global fileInit

    if not fileInit:
        initData()

@ask.intent("StationIntent")
def StationIntent(STATION):
    global flag
    global fileOpt
    global fileChg

    if flag == "setFavStation":
        fileOpt["favorite"] = STATION
        with open("Data/{0}.json".format(session.user.userId), 'w') as outfile:
            json.dump(fileOpt, outfile)
        return statement("Okey... Ich setze {} als Favorite".format(STATION))
    return statement("Das konnte ich leider nicht verstehen!")


if __name__ == '__main__':
    app.run(debug=True)