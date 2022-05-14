import math
from quart import Blueprint, request, current_app
from .charts import *
from .bdd import *
from .cache import cache

import json

chartBP = Blueprint('chart', __name__)
seuils = [0,2,3]
seuil = 0

# les vues et duree de chaque candidat en %
@cache.memoize(timeout=600)
def dureeEtVue(chartType):
    avList = dateAverage()
    labels = [x[0] for x in avList]
    duree  = [x[1] for x in avList]
    vues   = [x[2] for x in avList]
    
    vuesTot = sum(vues)
    dureeTot = sum(duree)
    vues  = [(x/vuesTot)*100 for x in vues]
    duree = [(x/dureeTot)*100 for x in duree]

    toremove = []
    for i,_ in enumerate(vues):
        if vues[i] < seuil and duree[i] < seuil:
            toremove.append(i)
    duree   = [x for i,x in enumerate(duree) if i not in toremove]
    vues    = [x for i,x in enumerate(vues) if i not in toremove]
    labels  = [x for i,x in enumerate(labels) if i not in toremove]

    chart  = monoElement(chartType, labels, "dureeVue")
    chart.addValue("Durée",duree)
    chart.addValue("Vues",vues)
    return chart.get()

# l'exposition de chaque candidat en %
@cache.memoize(timeout=600)
def dureeMulVue(chartType):
    avList = dateAverage()
    labels = [x[0] for x in avList]
    expo   = [x[1]*x[2] for x in avList]

    expoTot = sum(expo)
    expo  = [(x/expoTot)*100 for x in expo]
    resultats = [0.6, 2.1, 1.7, 4.6, 3.1, 23.1, 27.8, 22, 4.8, 0.8, 2.3, 7.1]

    toremove = []
    for i,_ in enumerate(expo):
        if expo[i] < seuil and resultats[i] < seuil :
            toremove.append(i)
    expo      = [x for i,x in enumerate(expo) if i not in toremove]
    labels    = [x for i,x in enumerate(labels) if i not in toremove]
    resultats = [x for i,x in enumerate(resultats) if i not in toremove]

    chart  = monoElement(chartType, labels, "expoRes")
    chart.addValue("Exposition sur YouTube",expo)
    chart.addValue("Resultats au premier tour",resultats)
    return chart.get()

# pour chaque candidat, évolution de son exposition en fonction du temps
@cache.memoize(timeout=600)
def candidatExpoTime(chartType,parti):
    expoEvol = candidatExpoEvol(parti)
    chart  = multiElement(chartType,"expoTime")
    chart.labels = [x[1].strftime("%d/%m") for x in expoEvol]
    # chart.addValue("Totale",[x[0] for x in expoEvol])

    soutiens = allSoutiens(parti)
    for soutien in soutiens :
        souStats = soutienExpoEvol(parti,soutien)
        souDate = [x[1].strftime("%d/%m") for x in souStats]
        souExpo   = [x[0] for x in souStats]

        for i,date in enumerate(chart.labels) :
            if date not in souDate :
                souExpo.insert(i,0)

        # Prendre juste le nom de famille
        soutien = soutien.split()
        if len(soutien) > 1 :
            soutien = soutien[1]
        else :
            soutien = soutien[0]
        chart.addValue(soutien,souExpo)

    return chart.get()

# pour chaque candidat on regarde d'où viennent leur expositions
@cache.memoize(timeout=600)
def expoByScenario(chartType,parti):
    scParti = scenarioParti(parti)
    labels  = [x[0] for x in scParti]
    expo    = [x[1]*x[2] for x in scParti]

    f = open('./pir/static/groupScenario.txt')
    group = json.load(f)
    newLabels = list(group.keys())
    newExpo   = [0] * len(newLabels)
    values    = list(group.values())

    f = open('./pir/static/candidatParti.txt')
    candidatParti = json.load(f)

    for i in range(len(expo)):
        label = labels[i]
        exp   = expo[i] 
        for k in range(len(values)):
            if label in values[k]:

                if "partisants" in newLabels[k] and label != candidatParti[parti]:
                    break
                
                newExpo[k] += exp
                break

    expoTot = sum(newExpo)
    newExpo    = [(x/expoTot)*100 for x in newExpo]

    # toremove = []
    # for i,_ in enumerate(expo):
    #     if expo[i] < seuils[-1] :
    #         toremove.append(i)
            
    # expo      = [x for i,x in enumerate(expo) if i not in toremove]
    # labels    = [x for i,x in enumerate(labels) if i not in toremove]

    chart  = multiElement(chartType,"expoTime", bgTransparency=.65)
    chart.labels = newLabels
    chart.addValue(parti,newExpo)
    return chart.get()

# Evolution de l'exposition par la pronfondeur et le temps
@cache.memoize(timeout=600)
def candidatDepthEvol(chartType,parti):
    chart        = multiElement(chartType,"expoTime", bgTransparency=.65)
    expoEvol     = candidatExpoEvol(parti)
    chart.labels = [x[1].strftime("%d/%m") for x in expoEvol]

    for i in [3,6,8]:
        expoProf     = bddCandidatDepthEvol(parti,i)
        depthDate    = [x[0].strftime("%d/%m") for x in expoProf]
        expo         = [x[1]*x[2] for x in expoProf]
        for j,date in enumerate(chart.labels) :
            if date not in depthDate :
                expo.insert(j,0)
        chart.addValue("Profondeur {}".format(i),expo)
    return chart.get()

# Evolution de l'exposition par la pronfondeur et le temps
@cache.memoize(timeout=600)
def allCandidatDepth(chartType):
    chart        = multiElement(chartType,"expoTime", bgTransparency=.02)
    chart.labels = []
    partis       = allPartis()

    for parti in partis :
        candiDepth  = candidatDepth(parti)

        expo = [x[0] for x in candiDepth]
        expo[1] += expo.pop(0)
        expo[1] += expo.pop(0)
        expo[0]  = expo[0] / 3
        expo[-2] += expo.pop()
        expo[-2] += expo.pop()
        expo[-2]  = expo[-2] / 3

        profs = [x[1] for x in candiDepth]
        if not chart.labels :
            profs = profs[2:-2]
            chart.labels = profs

        expo  = [math.log(x) for x in expo]
        chart.addValue(parti,expo)
    return chart.get()

# route
@chartBP.route("/", methods=['POST'])
async def chart():
    data = await request.form
    func = data["func"]
    size = int(data["size"])

    global seuil
    if size < 770 :
        seuil = seuils[-1]
    elif size < 1200:
        seuil = seuils[-2]
    else : 
        seuil = seuils[-3]

    return eval(func)