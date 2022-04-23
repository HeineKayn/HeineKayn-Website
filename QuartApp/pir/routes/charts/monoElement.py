from .general import Chart
import json

# Pour :
# - bar
# - doughnut
# - horizontalBar
# - polarChart
# - pie

# - (bubble et scatter marchent pas)


class monoElement(Chart):

    def __init__(self, type, labels, colorKey):
        super().__init__(colorKey)

        self.type = type
        self.labels = labels

        self.datasets = []
        self.size = 0

        # self.border_color = ['rgba(23, 23, 23,{})', 'rgba(150, 150, 150,{})']

        self.border = 2
        self.borderTransparency = 1
        self.bgTransparency = .7   
        self.hoverTransparency = .9

    def setColor(self, dic, key, val):
        dic[key] = [x.format(val) for x in self.colorList]
        dic[key] = dic[key][:self.size]
        return dic

    def addValue(self, label, data):
        size = len(data)
        valueDic = {}

        valueDic["label"] = label
        valueDic["data"] = data
        valueDic["borderWidth"] = 2

        # self.size = len(data)
        # valueDic = self.setColor(
        #     valueDic, "backgroundColor", self.bgTransparency)
        # valueDic = self.setColor(
        #     valueDic, "hoverBackgroundColor", self.hoverTransparency)
        # valueDic = self.setColor(
        #     valueDic, "borderColor", self.borderTransparency)

        # Bord modif
        # color = self.border_color.pop()
        # valueDic["borderColor"] = color.format(self.borderTransparency)

        color = self.pickColor()
        valueDic["backgroundColor"]      = color.format(self.bgTransparency)
        valueDic["hoverBackgroundColor"] = color.format(self.hoverTransparency)
        valueDic["borderColor"]          = color.format(self.borderTransparency)

        self.datasets.append(valueDic)

    def get(self):
        return json.dumps({
            "type": self.type,
            "data": {
                "labels": self.labels,
                "datasets": self.datasets,
            }
        })
