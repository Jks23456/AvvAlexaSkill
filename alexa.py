import json

from flask import Flask
from flask_ask import Ask, statement, question, session

from Function.MainMenue import MainMenue

intentJson = json.loads(open("Templates/Intent.json").read())
mainNode = MainMenue()

app = Flask(__name__)
ask = Ask(app, "/")

@ask.launch
def start_skill():
    speech_text= 'Was möchtest du tuhen?'
    return question(speech_text).reprompt(speech_text).simple_card(speech_text)

@ask.intent("YesIntent")
def YesIntent():
    js = intentJson.copy()
    js["intent"] = "YesIntent"
    input(js)
    if js["return"]["type"] == "question":
        return question(js["return"]["msg"])
    return statement(js["return"]["msg"])

@ask.intent("NoIntent")
def NoIntent():
    js = intentJson.copy()
    js["intent"] = "NoIntent"
    input(js)
    if js["retType"] == "question":
        return question(js["retMessage"])
    return statement(js["retMessage"])

@ask.intent("HaltIntent")
def HaltIntent(pTransport, pArtikel):
    js = intentJson.copy()
    js["intent"] = "HaltIntent"
    js["input"]["args"] = {
        "transport": pTransport,
        }
    input(js)
    if js["return"]["type"] == "question":
        return question(js["return"]["msg"])
    return statement(js["return"]["msg"])

@ask.intent("RouteIntent")
def RouteIntent(pHDepI, pHDepII, pHDepIII, pHArrI, pHArrII, pHArrIII):
    js = intentJson.copy()
    js["intent"] = "HaltIntent"
    js["input"]["args"] = {
        "Dep": str(pHDepI)+" "+str(pHDepII)+" "+str(pHDepIII),
        "Arr": str(pHArrI)+" "+str(pHArrII)+" "+str(pHArrIII)
    }
    input(js)
    if js["return"]["type"] == "question":
        return question(js["return"]["msg"])
    return statement(js["return"]["msg"])


def input(pIntentJson):
    mainNode.update(pIntentJson)


if __name__ == '__main__':
    app.run(debug=True)
