import json

from flask import Flask
from flask_ask import Ask, statement, question, session

from Function.MainMenue import MainMenue

intentJson = json.loads(open("Templates/intent.json").read())
mainNode = MainMenue()

app = Flask(__name__)
ask = Ask(app, "/")

@ask.launch
def start_skill():
    speech_text = 'Was möchtest du tuhen?'
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
    return input(js)


@ask.intent("HaltIntent")
def HaltIntent(pTransport, pArtikel):
    js = intentJson.copy()
    js["intent"] = "HaltIntent"
    js["input"]["args"] = {
        "transport": pTransport,
        }
    return input(js)


@ask.intent("RouteIntent")
def RouteIntent(DEP,ARR):
    js = intentJson.copy()
    js["intent"] = "RouteIntent"
    js["input"]["args"] = {
        "dep": str(DEP),
        "arr": str(ARR)
    }
    if js["input"]["args"]["dep"] == "  ":
        js["input"]["args"]["dep"] = "None"

    if js["input"]["args"]["arr"] == "  ":
        js["input"]["args"]["arr"] = "None"

    return input(js)


def input(pIntentJson):
    mainNode.update(pIntentJson)
    if pIntentJson["return"]["type"] == "question":
        return question(pIntentJson["return"]["msg"])
    return statement(pIntentJson["return"]["msg"])


if __name__ == '__main__':
    app.run(debug=True)
