from quart import Blueprint, request, render_template, jsonify

import os
import datetime
import json

from .ub import *

# ---------------

ubBlueprint = Blueprint('webBravery', __name__, template_folder='templates', static_folder='static', url_prefix='/bravery')

# ---------------

bdd  = bdd.BDD()
display = display.Displayer(bdd)
pick = pick.Picker(bdd)

logPath = "./bravery/static/txt/logs.txt"
ubImgPath = "./bravery/static/image/ubResult"

@ubBlueprint.route("/")
async def ultimateBravery():
    champions = bdd.get.championsFull()
    return await render_template('ultimateBravery.html', champions=champions)

@ubBlueprint.route("/start_bravery", methods=['POST'])
async def startBravery():
    dic = await request.form
    champions  = dic.getlist("champions[]")
    map        = dic["map"]
    difficulte = int(dic["difficulte"])

    date = datetime.datetime.now()

    # On fait l'image et on l'enregistre avec un tag unique
    datetag    = date.strftime("%m%d%H%f")
    path       = ubImgPath + "/d{}_{}_{}.png".format(difficulte,map,datetag)
    img        = display.run(difficulte,map,champions)
    img.save(path)

    # On écrit dans les logs
    path = path.replace("/bravery","")

    with open(logPath, "r") as f:
        logs = json.load(f)
    
    with open(logPath, 'w') as f:
        dateString = date.strftime("Le %d/%m/%Y a %H:%M:%S")
        ip = dic["ip"]
        logs.append({"date" : dateString, "ip" : ip, "path" : path})
        json.dump(logs, f)

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
        json.dump([], f)
    # Efface les images sauvegardés
    for f in os.listdir(ubImgPath):
        os.remove(os.path.join(ubImgPath, f))
    return ""

@ubBlueprint.route("/logs")
async def logs():
    with open(logPath, "r") as f:
        logs = json.load(f)
    return await render_template('logs.html',logs=logs)