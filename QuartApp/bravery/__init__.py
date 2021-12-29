from quart import Blueprint, request, render_template, jsonify

import os
from datetime import datetime,timedelta
import json


from bravery.ub.bdd import BDD
from bravery.ub.display import Displayer

# ---------------

ubBlueprint = Blueprint('bravery', __name__, template_folder='templates', static_folder='static')

# ---------------

logPath = "./bravery/static/txt/logs.txt"
ubImgPath = "./bravery/static/image/ubResult"
dateFormat = "Le %d/%m/%Y a %H:%M:%S"
echeanceLog = 1

def clearOldBravery():

    # Si ça fait X heures que le truc est là alors on le tej
    with open(logPath, "r") as f:
        logs = json.load(f)
        for index,log in enumerate(logs) :
            dateNow = datetime.now() - timedelta(hours = echeanceLog)
            dateThen = datetime.strptime(log["date"],dateFormat)
            if dateNow > dateThen :
                logs.pop(index) # On enlève de log.txt
                path = "./bravery" + log["path"][1:]
                os.remove(path)

    with open(logPath, 'w') as f:
        json.dump(logs, f, indent=4)

#------ MAIN

@ubBlueprint.route("/")
async def ultimateBravery():
    bdd  = BDD()
    champions = bdd.get.championsFull()
    clearOldBravery()
    return await render_template('ultimateBravery.html', champions=champions)

@ubBlueprint.route("/start_bravery", methods=['POST'])
async def startBravery():
    dic        = await request.form
    champions  = dic.getlist("champions[]")
    map        = dic["map"]
    difficulte = int(dic["difficulte"])

    # Objets pour bravery
    bdd  = BDD()
    display = Displayer(bdd)
    # pick = pick.Picker(bdd)

    # On fait l'image et on l'enregistre avec un tag unique
    dateNow    = datetime.now()
    datetag    = dateNow.strftime("%m%d%H%f")
    path       = ubImgPath + "/d{}_{}_{}.png".format(difficulte,map,datetag)
    img        = display.run(difficulte,map,champions)
    img.save(path)

    # On écrit dans les logs
    path = path.replace("./","/")

    with open(logPath, "r") as f:
        logs = json.load(f)
    
    with open(logPath, 'w') as f:
        dateString = dateNow.strftime(dateFormat)
        ip = dic["ip"]
        logs.append({"date" : dateString, "ip" : ip, "path" : path})
        json.dump(logs, f, indent=4)

    return path

#------ LOGS

@ubBlueprint.route("/update_logs", methods=['POST'])
async def updateLogs():
    with open(logPath, "r") as f:
        logs = json.load(f)
    return jsonify(await render_template("logs_model.html",logs=logs))

@ubBlueprint.route("/reset_log", methods=['POST'])
async def resetLogs():
    # Efface dans logs.txt
    with open(logPath, 'w') as f:
        json.dump([], f, indent=4)
    # Efface les images sauvegardés
    for f in os.listdir(ubImgPath):
        os.remove(os.path.join(ubImgPath, f))
    return ""

@ubBlueprint.route("/logs")
async def logs():
    with open(logPath, "r") as f:
        logs = json.load(f)
    return await render_template('logs.html',logs=logs)