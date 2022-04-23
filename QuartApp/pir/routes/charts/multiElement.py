from .general import Chart
import json

# Pour :
# - line
# - radar

class multiElement(Chart):

    def __init__(self, type, colorKey, bgTransparency = .3):
        super().__init__(colorKey)

        self.type = type
        self.datasets = []
        self.labels = []

        self.border = 2
        self.borderTransparency = 1
        self.bgTransparency = bgTransparency

    def addValue(self, label, data):
        color = self.pickColor()
        self.datasets.append({
            "label": label,
            "data": data,
            "backgroundColor": [
                color.format(self.bgTransparency),
            ],
            "borderColor": [
                color.format(self.borderTransparency),
            ],
            "borderWidth": self.border
        })

    def get(self):
        return json.dumps({
            "type": self.type,
            "data": {
                "labels": self.labels,
                "datasets": self.datasets,
            }
        })
